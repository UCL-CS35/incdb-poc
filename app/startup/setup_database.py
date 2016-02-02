from app import app, db

from app.startup import database_builder
from app.startup import settings

import os

def setup_database():

	print "Setting up database..."

	dataset = settings.PICKLE_DATABASE

	builder = database_builder.DatabaseBuilder(
        db, dataset=dataset,
        studies=os.path.join(settings.ASSET_DIR, 'database.txt'),
        features=os.path.join(settings.ASSET_DIR, 'features.txt'),
        reset_db=True, reset_dataset=False)

	analyses = ['emotion', 'language', 'memory', 'pain', 'visual',
                    'attention', 'sensory']
	# analyses = None

	print "Adding analyses..."
	builder.add_term_analyses(analyses=analyses, add_images=True, reset=True)

	print "Adding feature-based meta-analysis images..."
	builder.generate_analysis_images(
		analyses=analyses, add_to_db=False, overwrite=True)

	print "Memory-mapping key image sets..."
	builder.memory_map_images(include=['terms'], reset=True)