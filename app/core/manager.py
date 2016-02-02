from app import manager
from app.core.decode import decode_folder
from app.startup import settings

@manager.command
def init_db():
	from app.startup.setup_database import setup_database
	setup_database()

@manager.command
def decode():
	decode_folder(settings.DECODED_IMAGE_DIR)