from app import manager


@manager.command
def init_db():
    from app.startup.create_users import create_users

    create_users()