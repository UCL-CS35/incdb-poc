from app.startup import settings
from app.models.users import User, Role, UsersRoles
from app.models.analysis import AnalysisSet, Analysis, TermAnalysis
from app.models.collections import Collection
from app.models.decodings import DecodingSet, DecodingSet
from app.models.images import Image, TermAnalysisImage

import os
from os.path import join, basename, exists

from neurosynth import Masker
from neurosynth.base.dataset import Dataset
from neurosynth.analysis import meta
import neurosynth as ns

import numpy as np
import pandas as pd

import random
from glob import glob
import json
import re
import shutil
import urllib

class DatabaseBuilder:

    def __init__(self, db, dataset=None, studies=None, features=None,
                 reset_db=False, reset_dataset=False, download_data=True):
        """
        Initialize instance from a pickled Neurosynth Dataset instance or a
        pair of study and analysis .txt files.
        Args:
            db: the SQLAlchemy database connection to use.
            dataset: an optional filename of a pickled neurosynth Dataset
                instance.
                Note that the Dataset must contain the list of Mappables (i.e.,
                    save() must have been called with keep_mappables set to
                    True).
            studies: name of file containing activation data. If passed, a new
                Dataset instance will be constructed.
            features: name of file containing feature data.
            reset_db: if True, will drop and re-create all database tables
                before adding new content. If False (default), will add content
                incrementally.
            reset_dataset: if True, will regenerate the pickled Neurosynth
                dataset.
            download_data: if True, ignores any existing files and downloads the
                latest Neurosynth data files from GitHub.
        """

        if (studies is not None and not os.path.exists(studies)) \
                or settings.RESET_ASSETS:
            print "WARNING: RESETTING ALL NEUROSYNTH ASSETS!"
            self.reset_assets(download_data)

        # Load or create Neurosynth Dataset instance
        if dataset is None or reset_dataset or (isinstance(dataset, basestring)
                                               and not os.path.exists(dataset)
                                               ):
           print "\tInitializing a new Dataset..."
           if (studies is None) or (features is None):
               raise ValueError(
                   "To generate a new Dataset instance, both studies and "
                   "analyses must be provided.")
           dataset = Dataset(studies)
           dataset.add_features(features)
           dataset.save(settings.PICKLE_DATABASE, keep_mappables=True)
        else:
            print "\tLoading existing Dataset..."
            dataset = Dataset.load(dataset)
            if features is not None:
               dataset.add_features(features)

        self.dataset = dataset
        self.db = db

        if reset_db:
            print "WARNING: RESETTING DATABASE!!!"
            self.reset_database()

    def reset_assets(self, download=True):
        # Create data directories if needed
        check_dirs = [
            settings.ASSET_DIR,
            settings.IMAGE_DIR,
            join(settings.IMAGE_DIR, 'analyses'),
            join(settings.IMAGE_DIR, 'coactivation'),
            join(settings.IMAGE_DIR, 'custom'),
            settings.DECODING_RESULTS_DIR,
            settings.DECODING_SCATTERPLOTS_DIR,
            settings.DECODED_IMAGE_DIR,
            settings.MASK_DIR,
            settings.TOPIC_DIR,
            settings.MEMMAP_DIR
        ]
        for d in check_dirs:
            if not exists(d):
                os.makedirs(d)

        # Retrieve remote assets
        def retrieve_file(url, filename):
            try:
                if not exists(filename) or settings.RESET_ASSETS:
                    urllib.urlretrieve(url, filename)
            except:
                raise ValueError("Could not save remote URL %s to local path %s. ")

        for u, f in {
            'ftp://ftp.ebi.ac.uk/pub/databases/genenames/hgnc_complete_set.txt.gz':
            join(settings.ASSET_DIR, 'hgnc_complete_set.txt.gz')
        }.items():
            retrieve_file(u, f)

        # Copy anatomical image
        anat = join(settings.ROOT_DIR, 'default', 'anatomical.nii.gz')
        shutil.copy(anat, join(settings.IMAGE_DIR))

        if download:
            ns.dataset.download(path=settings.ASSET_DIR, unpack=True)

        # Raise warnings for missing resources we can't retrieve from web
        assets = [
            (join(settings.ASSET_DIR, 'misc'), "The misc directory contains "
                "various support files--e.g., stopword lists for topic "
                "modeling."),
            (join(settings.ASSET_DIR, 'abstracts.txt'), "This file is required "
                "for topic modeling of article abstracts. Without it, the "
                "topic-based analyses will not appear on the website."),
            (settings.GENE_IMAGE_DIR, "This directory contains all gene images "
                "from the Allen Institute for Brain Science's gene expression "
                "database. Without it, the /genes functionality will not work."),
            (join(settings.IMAGE_DIR, 'fcmri'), "This directory contains 300 "
                "GB of functional connectivity images from the Brain "
                "SuperStruct project, provided courtesy of Thomas Yeo and "
                "Randy Buckner. These images must be obtained directly. "
                "Without them, no functional connectivity images will be "
                "displayed on the website.")
        ]
        # for (asset, desc) in assets:
        #     if not exists(asset):
        #         raise RuntimeWarning("Asset %s doesn't seem to exist, and "
        #             "can't be retrieved automatically. %s" % (asset, desc))

        from nsweb.tasks import MASK_FILES
        for k, v in MASK_FILES.items():
            if not exists(join(settings.MASK_DIR, v)):
                raise RuntimeWarning("The image file for the '%s' mask "
                    "cannot be found at %s. This mask will be gracefully "
                    "ignored in all decoder scatterplots.")

    def reset_database(self):
        ''' Drop and re-create all tables. '''
        self.db.drop_all()
        self.db.create_all()

    def add_term_analyses(self, analyses=None, add_images=False,
                          image_dir=None, reset=False):
        ''' Add Analysis records to the DB.
        Args:
            analyses: A list of analysis names to add to the db. If None,
                will use all analyses in the Dataset.
            image_dir: folder to save generated analysis images in. If None,
                do not save any images.
        '''
        if reset:
            for a in TermAnalysis.query.all():
                self.db.session.delete(a)
            for s in AnalysisSet.query.filter_by(type='terms').all():
                self.db.session.delete(s)

        if analyses is None:
            analyses = self._get_feature_names()
        else:
            analyses = list(set(self._get_feature_names()) & set(analyses))

        term_set = AnalysisSet(name='abstract terms', type='terms',
                               description='Term-based meta-analyses. Studies '
                               'are identified for inclusion based on the '
                               'presence of terms in abstracts.')
        # Store analyses for faster counting of studies/activations
        self.analyses = {}

        for f in analyses:

            analysis = TermAnalysis(name=f)

            # elements are the Analysis instance, # of studies, and # of
            # activations
            self.analyses[f] = [analysis, 0, 0]

            if add_images:
                self.add_analysis_images(analysis, image_dir)

            term_set.analyses.append(analysis)
            self.db.session.add(analysis)

        term_set.n_analyses = len(term_set.analyses)
        self.db.session.commit()

    def add_analysis_images(self, analysis, image_dir=None, reset=True):
        """
        Create DB records for the reverse and forward meta-analysis images for
        the given analysis.
        Args:
            analysis: Either a Analysis instance or the (string) name of an
                analysis to update. If a string, first check self.analyses, and
                only retrieve from DB if not found.
            image_dir: Location to find images in
            reset: If True, deletes any existing AnalysisImages before adding
                new ones
        """

        if isinstance(analysis, basestring):
            if hasattr(self, 'analyses') and analysis in self.analyses:
                analysis = self.analyses[analysis][0]
            else:
                analyses = TermAnalysis.query.filter_by(name=analyses).all()
                if len(analyses) > 1:
                    raise ValueError("More than 1 analysis has the name %s! "
                                     "Please resolve the conflict and try "
                                     "again." % analysis)
                elif not analyses:
                    return
                else:
                    analysis = analyses[0]

        analysis.images = []

        name = analysis.name

        if image_dir is None:
            image_dir = join(settings.IMAGE_DIR, 'analyses')

        # Image class depends on Analysis class. TopicAnalysis objects have
        # a terms field that cross-links to top-loading terms.
        if hasattr(analysis, 'terms'):
            image_class = TopicAnalysisImage
        else:
            image_class = TermAnalysisImage

        analysis.images.extend([
            image_class(image_file=join(image_dir, name +
                                        '_pAgF_z_FDR_0.01.nii.gz'),
                        label='%s: forward inference' % name,
                        stat='z-score'),
            image_class(image_file=join(image_dir, name +
                                        '_pFgA_z_FDR_0.01.nii.gz'),
                        label='%s: reverse inference' % name,
                        stat='z-score')
        ])

        self.db.session.add(analysis)
        self.db.session.commit()

    def _map_analysis_to_studies(self, analysis):
        pass

    def _update_analysis_counts(self):
        """ Update the num_studies and num_activations fields for all analyses.
        """
        for k, f in self.analyses.items():
            f[0].n_studies = f[1]
            f[0].n_activations = f[2]
#            self.db.session.update(f)
        self.db.session.commit()

    def generate_analysis_images(self, image_dir=None, analyses=None,
                                 add_to_db=True, overwrite=True, **kwargs):
        """ Create a full set of analysis meta-analysis images via Neurosynth.
        Args:
            image_dir: Folder in which to store images. If None, uses default
                location specified in SETTINGS.
            analyses: Optional list of analyses to limit meta-analysis to.
                If None, all available analyses are processed.
            add_to_db: if True, will create new AnalysisImage records, and
                associate them with the corresponding Analysis record.
            overwrite: if True, always generate new meta-analysis images. If
                False, will skip any analyses that already have images.
            kwargs: optional keyword arguments to pass onto the Neurosynth
                meta-analysis.
        """
        # Set up defaults
        if image_dir is None:
            image_dir = join(settings.IMAGE_DIR, 'analyses')
            if not os.path.exists(image_dir):
                os.makedirs(image_dir)
                os.makedirs(join(settings.IMAGE_DIR, 'custom'))

        if analyses is None:
            analyses = self._get_feature_names()

        # Remove analyses that already exist
        if not overwrite:
            files = glob(
                join(settings.IMAGE_DIR, 'analyses', '*_pFgA_z.nii.gz'))
            existing = [basename(f).split('_')[0] for f in files]
            analyses = list(set(analyses) - set(existing))

        # Meta-analyze all images
        meta.analyze_features(self.dataset, analyses, output_dir=image_dir,
                              q=0.01, **kwargs)

        # Create AnalysisImage records
        if add_to_db:
            for f in analyses:
                self.add_analysis_images(f, image_dir)

            self.db.session.commit()

    def add_cognitive_atlas_nodes(self):
        """ Store data from the Cognitive Atlas for all available nodes. """
        RDF_PATH = join(settings.ASSET_DIR, 'misc')
        rdf_files = glob(join(RDF_PATH, '*.rdf'))
        if not rdf_files:
            raise IOError("No RDF files found in %s. Please make sure to "
                          "place all .rdf dumps from the Cognitive Atlas in "
                          "this directory." % RDF_PATH)

        nodes = {}
        for f in rdf_files:
            text = open(f).read()
            patt = 'rdf:about="(.*?)">.*?' \
                   '<skos:definition>(.*?)</skos.*?' \
                   '<skos:prefLabel>(.*?)</skos:prefLabel>'
            for m in re.findall(patt, text, re.S):
                url, definition, name = m
                nodes[name] = {
                    'definition': definition.strip(),
                    'url': url
                }

        for ta in TermAnalysis.query.all():
            if ta.name in nodes:
                ta.cog_atlas = json.dumps(nodes[ta.name])
                self.db.session.add(ta)
        self.db.session.commit()

    def memory_map_images(self, include=['terms', 'topics', 'genes'],
                          reset=False):
        """ Create memory-mapped arrays containing all image data for one or
        more AnalysisSets.
        """

        mm_dir = settings.MEMMAP_DIR
        if not exists(mm_dir):
            os.makedirs(mm_dir)

        # Get mask
        masker = Masker(join(settings.IMAGE_DIR, 'anatomical.nii.gz'))
        mask_voxels = np.sum(masker.current_mask)

        def save_memmap(name, analysis_set, images, labels, voxels=None):

            # Delete old versions
            if reset:
                dec = DecodingSet.query.filter_by(name=name).all()
                for ds in dec:
                    self.db.session.delete(ds)

            # print term_labels
            open(join(mm_dir, '%s_labels.txt' % name), 'w') \
                .write('\n'.join(labels))

            sampled_vox = np.arange(mask_voxels)
            is_subsampled = (voxels is not None)
            if voxels is not None:
                # Either randomly select voxels, or use what was passed
                # TODO: sample uniformly from a 3D grid instead of randomly
                if isinstance(voxels, int):
                    sampled_vox = np.random.choice(sampled_vox, voxels,
                                                   replace=False)
                else:
                    sampled_vox = voxels
                np.save(join(mm_dir, '%s_voxels.npy' % name), sampled_vox)

            # Initialize memmap
            n_images = len(images)
            mm_file = join(mm_dir, '%s_images.dat' % name)
            mm = np.memmap(mm_file, dtype='float32', mode='w+',
                           shape=(len(sampled_vox), n_images))

            # Save key image stats--will need these to reconstruct raw values
            stats = np.zeros((n_images, 4))

            # Populate with standardized image data
            for i, img in enumerate(images):
                # Use unthresholded maps when possible
                img_file = re.sub('_FDR_*nii.gz', '.nii.gz', img)
                data = masker.mask(img_file)[sampled_vox]
                std, mean = data.std(), data.mean()
                mm[:, i] = (data - mean) / std
                stats[i, :] = [data.min(), data.max(), mean, std]

            stats = pd.DataFrame(stats, index=labels,
                                 columns=['min', 'max', 'mean', 'std'])
            stats.to_csv(join(mm_dir, '%s_stats.txt' % name), sep='\t')

            # Write metadata
            metadata = {
                'name': name,
                'n_voxels': len(sampled_vox),
                'n_images': n_images,
                'is_subsampled': is_subsampled
            }
            md_file = join(mm_dir, '%s_metadata.json' % name)
            open(md_file, 'w').write(json.dumps(metadata))

            # Flush
            del mm

            # Create DB record
            self.db.session.add(
                DecodingSet(name=name, n_images=n_images,
                            n_voxels=len(sampled_vox),
                            is_subsampled=is_subsampled,
                            analysis_set=analysis_set))
            self.db.session.commit()

        ### TERMS ###
        if 'terms' in include:

            print "\tCreating memmap of term image data..."

            analysis_set = AnalysisSet.query \
                .filter_by(type='terms').first()

            # Get all images and save labels
            images = [a.images[1].image_file for a in analysis_set.analyses]
            labels = [a.name for a in analysis_set.analyses]

            print "\t\tFound %d images." % len(images)

            # save both full and 20k voxel arrays
            save_memmap('terms_full', analysis_set, images, labels)
            save_memmap('terms_20k', analysis_set, images, labels, 20000)
            # also save posterior probability images
            images = [img.replace('_pFgA_z_FDR_0.01', '_pFgA_given_pF=0.50')
                      for img in images]
            save_memmap('terms_pp', analysis_set, images, labels)


    def _filter_analyses(self, analyses):
        """ Remove any invalid analysis names """
        # Remove analyses that start with a number
        analyses = [f for f in analyses if re.match('[a-zA-Z]+', f)]
        return analyses

    def _get_feature_names(self):
        """ Return all (filtered) analysis names in the Dataset instance """
        return self._filter_analyses(self.dataset.get_feature_names())
