# __init__.py is a special Python file that allows a directory to become
# a Python package so it can be accessed using the 'import' statement.

from flask import Flask
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_migrate import Migrate, MigrateCommand
from flask_user import UserManager, SQLAlchemyAdapter
from flask_wtf.csrf import CsrfProtect

from app.initializers import settings

import os

app = Flask(__name__)           # The WSGI compliant web application object
db = SQLAlchemy(app)            # Setup Flask-SQLAlchemy
manager = Manager(app)          # Setup Flask-Script


@app.before_first_request
def initialize_app_on_first_request():
    """ Before the first request to this instance of the application """
    print "First request..."


def create_app(extra_config_settings={}):
    """ Initialize Flask applicaton """

    # ***** Initialize app config settings *****

    # Read common settings from 'app/initializers/common_settings.py' file
    app.config.from_object('app.initializers.settings')

    # Read environment-specific settings from file defined
    # by OS environment variable 'ENV_SETTINGS_FILE'
    env_settings_file = os.environ.get(
        'ENV_SETTINGS_FILE',
        'env_settings_example.py')
    app.config.from_pyfile(env_settings_file)

    # Read extra config settings from function
    # parameter 'extra_config_settings'
    # Overwrite with 'extra_config_settings' parameter
    app.config.update(extra_config_settings)

    # Disable CSRF checks while testing
    if app.testing:
        app.config['WTF_CSRF_ENABLED'] = False

    # Setup Flask-Migrate
    migrate = Migrate(app, db)
    manager.add_command('db', MigrateCommand)

    # Setup Flask-Mail
    mail = Mail(app)

    # Setup WTForms CsrfProtect
    CsrfProtect(app)


    # Define bootstrap_is_hidden_field for flask-bootstrap's bootstrap_wtf.html
    from wtforms.fields import HiddenField

    def is_hidden_field_filter(field):
        return isinstance(field, HiddenField)

    app.jinja_env.globals['bootstrap_is_hidden_field'] = is_hidden_field_filter

    # Setup an error-logger to send emails to app.config.ADMINS
    init_email_error_handler(app)

    # Setup Flask-User to handle user account related forms
    from app.models.users import User
    from app.core.forms import MyRegisterForm
    from app.controllers.user import user_account

    db_adapter = SQLAlchemyAdapter(db, User)  # Setup the SQLAlchemy DB Adapter
    user_manager = UserManager(
        db_adapter,
        app,  # Init Flask-User and bind to app
        register_form=MyRegisterForm,  # using a custom register form with UserProfile fields
        user_profile_view_function=user_account,
    )

    # Load all blueprints with their manager commands, models and views
    from app import core, models
    from app.controllers import home, contribute
    from app.controllers import movies, terms, components
    from app.controllers import user, admin

    return app


def init_email_error_handler(app):
    """
    Initialize a logger to send emails on error-level messages.
    Unhandled exceptions will now send an email message to app.config.ADMINS.
    """

    if app.debug:
        return  # Do not send error emails while developing

    # Retrieve email settings from app.config
    host = settings.MAIL_SERVER
    port = settings.MAIL_PORT
    from_addr = settings.MAIL_DEFAULT_SENDER
    username = settings.MAIL_USERNAME
    password = settings.MAIL_PASSWORD
    secure = () if app.config.get('MAIL_USE_TLS') else None

    # Retrieve app settings from app.config
    to_addr_list = app.config['ADMINS']
    subject = app.config.get('APP_SYSTEM_ERROR_SUBJECT_LINE', 'System Error')

    # Setup an SMTP mail handler for error-level messages
    import logging
    from logging.handlers import SMTPHandler

    mail_handler = SMTPHandler(
        mailhost=(host, port),  # Mail host and port
        fromaddr=from_addr,  # From address
        toaddrs=to_addr_list,  # To address
        subject=subject,  # Subject line
        credentials=(username, password),  # Credentials
        secure=secure,
    )
    mail_handler.setLevel(logging.ERROR)
    app.logger.addHandler(mail_handler)

    # Log errors using: app.logger.error('Some error message')
