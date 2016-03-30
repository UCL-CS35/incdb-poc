from app import db

from app.initializers import database_builder
from app.initializers import settings

import os
import shutil


def setup_database():
    """ Create dataset, database and users """

    print "Setting up database..."

    dataset = settings.PICKLE_DATABASE

    builder = database_builder.DatabaseBuilder(
        db,
        dataset=dataset,
        studies=os.path.join(settings.ASSET_DIR, 'database.txt'),
        features=os.path.join(settings.ASSET_DIR, 'features.txt'),
        reset_db=True,
        reset_dataset=False)

    # TODO(all) all analyses
    analyses = ['emotion',
                'language',
                'memory',
                'pain',
                'visual',
                'attention',
                'sensory']

    print "Adding analyses..."
    builder.add_term_analyses(analyses=analyses, add_images=True, reset=True)

    print "Adding feature-based meta-analysis images..."
    builder.generate_analysis_images(
        analyses=analyses,
        add_to_db=False,
        overwrite=True)

    print "Memory-mapping key image sets..."
    builder.memory_map_images(include=['terms'], reset=True)

    from .create_users import create_users
    create_users()

    print "Clear uploads..."
    shutil.rmtree('uploads', ignore_errors=True)
    os.mkdir('uploads')
