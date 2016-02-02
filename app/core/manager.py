from app import manager

@manager.command
def init_db():
	from app.startup.setup_database import setup_database
	setup_database()