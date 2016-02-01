from app import db

from app.core.models import *
from app.startup import settings

from uuid import uuid4

import json
import glob

from neurosynth import Masker
import numpy as np
import pandas as pd
import nibabel as nb

from datetime import datetime
from os import unlink, listdir
from os.path import join, basename, exists

import traceback
from collections import OrderedDict

def load_image(masker, filename, save_resampled=True):
    """ Load an image, resampling into MNI space if needed. """
    
    f = join(settings.IMAGE_DIR, 'anatomical.nii.gz')
    anatomical = nb.load(f)

    filename = join(settings.DECODED_IMAGE_DIR, filename)
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
        mm_file = join(settings.MEMMAP_DIR, name + '_images.dat')
        self.data = np.memmap(mm_file, dtype='float32', mode='r',
                              shape=(n_voxels, n_images))
        # Link to labels
        lab_file = join(settings.MEMMAP_DIR, name + '_labels.txt')
        _labels = open(lab_file).read().splitlines()
        self.labels = OrderedDict(zip(_labels, range(len(_labels))))

        # Image stats
        stat_file = join(settings.MEMMAP_DIR, name + '_stats.txt')
        self.stats = pd.read_csv(stat_file, sep='\t')

def decode_folder(directory):

	decoding_set = DecodingSet.query.filter_by(name='terms_20k').first() 

	for filename in listdir(directory):
		decoding = Decoding(filename=filename, uuid=uuid4().hex, decoding_set=decoding_set)
		result = decode_image(decoding_set, filename)
		if result:
			decoding.image_decoded_at = datetime.utcnow()
			db.session.add(decoding)
			db.session.commit()

def decode_image(decoding_set, filename, drop_zeros=False):

    print 'Decoding image...'
    mm_dir = settings.MEMMAP_DIR
    try:
        memmaps = {}
        for f in glob.glob(join(settings.MEMMAP_DIR, '*_metadata.json')):
            md = json.load(open(f))
            memmaps[md['name']] = Reference(**md)
   
        ref = memmaps[decoding_set.name]

        masker = Masker(join(settings.IMAGE_DIR, 'anatomical.nii.gz'))
        data = load_image(masker, filename)

        # Select voxels in sampling mask if it exists
        if ref.is_subsampled:
            index_file = join(mm_dir, ref.name + '_voxels.npy')
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
        outfile = join(settings.DECODING_RESULTS_DIR, filename + '.txt')
        labels = ref.labels.keys()
        pd.Series(r, index=labels).to_csv(outfile, sep='\t')

        print r
        return True

    except Exception, e:
        print traceback.format_exc()
        return False