from app import manager
from app.core.decode import decode_folder
from app.initializers import settings

@manager.command
def init_db():
	from app.initializers.setup_database import setup_database
	setup_database()

@manager.command
def decode():
	print "Decode folder " + settings.DECODED_IMAGE_DIR
	decode_folder(settings.DECODED_IMAGE_DIR)