from app.models.decodings import Decoding, DecodingSet
from app.models.decodings import *
from app.models.collections import *
from app.models.analysis import *
from app.models.analysis import Analysis
from app.models.images import TermAnalysisImage

from app.controllers.components import component_directory

from app.initializers import mycelery
from app.initializers.settings import *
from app.initializers.celerydb import db_session

from uuid import uuid4

import json
import glob

from neurosynth import Masker
import numpy as np
import pandas as pd
import nibabel as nb

from datetime import datetime

from os import unlink, listdir, mkdir
from os.path import join, exists, isdir
import shutil

import traceback
from collections import OrderedDict

from nilearn.image import resample_img
from nipype.interfaces import afni as afni

import celery


def load_image(masker, collection, filename, save_resampled=True):
    """ Load an image, resampling into MNI space if needed. """
    f = join(IMAGE_DIR, 'anatomical.nii.gz')
    anatomical = nb.load(f)

    filename = join(PROCESSED_IMAGE_DIR, collection, filename)
    img = nb.load(filename)
    if img.shape[:3] != (91, 109, 91):
        img = resample_img(
            img, target_affine=anatomical.get_affine(),
            target_shape=(91, 109, 91), interpolation='nearest')
        if save_resampled:
            unlink(filename)
            img.to_filename(filename)

    return masker.mask(img)


class Reference(object):

    def __init__(self, name, n_voxels, n_images, is_subsampled):

        self.name = name
        self.n_voxels = n_voxels
        self.n_images = n_images
        self.is_subsampled = is_subsampled

        # Link to memmap data
        mm_file = join(MEMMAP_DIR, name + '_images.dat')
        self.data = np.memmap(mm_file, dtype='float32',
                            mode='r', shape=(n_voxels, n_images))
        # Link to labels
        lab_file = join(MEMMAP_DIR, name + '_labels.txt')
        _labels = open(lab_file).read().splitlines()
        self.labels = OrderedDict(zip(_labels, range(len(_labels))))

        # Image stats
        stat_file = join(MEMMAP_DIR, name + '_stats.txt')
        self.stats = pd.read_csv(stat_file, sep='\t')


class SqlAlchemyTask(celery.Task):
    """ An abstract Celery Task that ensures that the connection the the
    database is closed on task completion """
    abstract = True

    def after_return(self, status, retval, task_id, args, kwargs, einfo):
        db_session.remove()


@celery.task(base=SqlAlchemyTask)
def decode_collection(directory, collection, movie_name):
    """ Celery task to decode processed dataset """
    decoding_set = db_session.query(DecodingSet).filter_by(name='terms_20k')
    decoding_set = decoding_set.first()

    print directory
    print collection

    if isdir(join(directory, collection)):

        decode_movie_folder = join(DECODING_RESULTS_DIR, collection)

        if not exists(decode_movie_folder):
            mkdir(decode_movie_folder)

        decodings = db_session.query(Decoding).filter_by(collection=collection)
        for a in decodings:
            db_session.delete(a)
        db_session.commit()

        time = datetime.utcnow()
        for filename in listdir(join(directory, collection)):
            if filename == ".DS_Store":
                continue
            decoding = Decoding(filename=filename, uuid=uuid4().hex,
                        decoding_set=decoding_set, movie=movie_name,
                        collection=collection)
            decoding = decode_image(decoding, decoding_set,
                        collection, filename)
            if decoding is not None:
                decoding.image_decoded_at = time
                db_session.add(decoding)
                db_session.commit()

    analysis = db_session.query(Analysis.name)
    movie_decode = db_session.query(Decoding.filename, Decoding.movie, Decoding.term)
    movie_decode = movie_decode.filter_by(movie=movie_name)

    for term in analysis:
        print term.name
        movie_decode_term = movie_decode.filter_by(term=term.name)
        if movie_decode_term.count() == 0:
            print 'There are no components for this term'
        else:
            imgs = []
            collection_name = collection
            for component in movie_decode_term:
                file = component_directory(collection_name, component.filename)
                print "Now decoding for" + term.name
                imgs.append(file)
            concat_components(imgs, term.name, collection_name)


def decode_image(
    decoding, decoding_set, collection,
        filename, drop_zeros=False):
    """ Decode image and save correlation values to file """

    print 'Decoding ' + filename + '...'
    try:
        memmaps = {}
        for f in glob.glob(join(MEMMAP_DIR, '*_metadata.json')):
            md = json.load(open(f))
            memmaps[md['name']] = Reference(**md)

        ref = memmaps[decoding_set.name]

        masker = Masker(join(IMAGE_DIR, 'anatomical.nii.gz'))
        data = load_image(masker, collection, filename)

        # Select voxels in sampling mask if it exists
        if ref.is_subsampled:
            index_file = join(MEMMAP_DIR, ref.name + '_voxels.npy')
            if exists(index_file):
                voxels = np.load(index_file)
                data = data[voxels]

        # Drop voxels with zeros or NaN in input image
        voxels = np.arange(len(data))
        if drop_zeros:
            voxels = np.where((data != 0) & np.isfinite(data))[0]
            data = data[voxels]
        # Otherwise we still need to replace NaNs or bad things happen
        data = np.nan_to_num(data)

        # standardize image and get correlation
        data = (data - data.mean()) / data.std()
        r = np.dot(ref.data[voxels].T, data) / ref.n_voxels
        outfile = join(DECODING_RESULTS_DIR, collection)
        outfile = join(outfile, filename + '.txt')
        labels = ref.labels.keys()
        series = pd.Series(r, index=labels).sort_values(ascending=False)
        series.to_csv(outfile, sep='\t')

        # topFiveTerms = series.tail(5)
        highestCorrelationTerm = labels[np.argmax(r, axis=0)]
        highestCorrelation = series.head(n=1)[0]

        decoding.term = highestCorrelationTerm
        decoding.correlation = highestCorrelation

        return decoding

    except Exception, e:
        print e
        print traceback.format_exc()
        return None


def concat_components(componentList, term, movie):
    # TODO(Rajind) Describe function for documentation
    term_name = term
    movie_name = movie
    merge = afni.Merge()
    merge.inputs.in_files = componentList
    merge.inputs.doall = True
    merge.inputs.out_file = term_name + '.nii.gz'
    res = merge.run()

    filename = join(ROOT_DIR, term_name + '.nii.gz')
    source_dir = join(PROCESSED_IMAGE_DIR, movie_name)
    term_folder = join(source_dir, "terms")
    print term_folder
    if not os.path.exists(term_folder):
        os.mkdir(term_folder)
    file_dir = os.path.join(term_folder,term_name + '.nii.gz')
    if os.path.exists(file_dir):
        print file_dir
        print "Removing existing file"
        os.remove(file_dir)
    shutil.move(filename, term_folder)
    # filename = join(DECODED_IMAGE_DIR, movie_name, term_name)
    # nib.save(image4D, filename)
