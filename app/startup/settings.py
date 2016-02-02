import os
from os.path import join, dirname
import sys

### SETTINGS THAT SHOULD ALWAYS BE UPDATED ###

# The root location of the app. Should not need to be changed.
ROOT_DIR = os.path.realpath(
    join(join(os.path.dirname(__file__), os.path.pardir), os.path.pardir))
    
# Root path for generated data
DATA_DIR = join(ROOT_DIR,'data')

# ***********************************
# Settings common to all environments
# ***********************************

# Application settings
APP_NAME = "INcDb"
APP_SYSTEM_ERROR_SUBJECT_LINE = APP_NAME + " system error"

# Flask settings
CSRF_ENABLED = True

# Flask-User settings
USER_APP_NAME = APP_NAME
USER_ENABLE_CHANGE_PASSWORD = True  # Allow users to change their password
USER_ENABLE_CHANGE_USERNAME = False  # Allow users to change their username
USER_ENABLE_CONFIRM_EMAIL = True  # Force users to confirm their email
USER_ENABLE_FORGOT_PASSWORD = True  # Allow users to reset their passwords
USER_ENABLE_EMAIL = True  # Register with Email
USER_ENABLE_REGISTRATION = True  # Allow new users to register
USER_ENABLE_RETYPE_PASSWORD = True  # Prompt for `retype password` in:
USER_ENABLE_USERNAME = False  # Register and Login with username
USER_AFTER_LOGIN_ENDPOINT = 'core.index'
USER_AFTER_LOGOUT_ENDPOINT = 'core.index'

### SHOULD NOT NEED TO BE UPDATED ###

# Path to main assets (pickled Dataset, study files, etc.)
ASSET_DIR = join(DATA_DIR, 'assets')
RESET_ASSETS = False

# Path to pickled Neurosynth Dataset instance
PICKLE_DATABASE = join(ASSET_DIR, 'neurosynth_dataset.pkl')

# Main image folder
IMAGE_DIR = join(DATA_DIR, 'images')

# Path to analysis/location flat filies
LOCATION_ANALYSIS_DIR = join(DATA_DIR, 'locations', 'analyses')


# Static content
STATIC_FOLDER = join(ROOT_DIR, 'nsweb', 'static')

# Templates
TEMPLATE_FOLDER = join(ROOT_DIR, 'nsweb', 'templates')


### DECODER-RELATED PATHS ###
# Path to decoded images
DECODED_IMAGE_DIR = join(DATA_DIR, 'images', 'decoded')

# Path to saved decoding image array--this is kept active in memory
DECODING_DATA = join(ASSET_DIR, 'decoding.msg')

# Path to output decoding results (flat .txt files)
DECODING_RESULTS_DIR = join(DATA_DIR, 'decoding', 'results')

# Path to output decoded image scatter plots
DECODING_SCATTERPLOTS_DIR = join(DATA_DIR, 'decoding', 'scatterplots')

# Whether or not to cache decoder results. When True, will not re-run the
# decoder on an image unless the image has been modified since the
# last decoding; when False, will re-run the decoder every time.
CACHE_DECODINGS = True

# Path to memory-mapped arrays of image data.
# Note: when running a development build inside a docker container or other VM,
# memmapping may fail. In such a case, this shoudl point to a directory on the
# local disk image rather than the host.
MEMMAP_DIR = join(DATA_DIR, 'memmaps')


### CONTENT-SPECIFIC DIRECTORIES ###
MASK_DIR = join(IMAGE_DIR, 'masks')
TOPIC_DIR = join(DATA_DIR, 'topics')
GENE_IMAGE_DIR = join(IMAGE_DIR, 'genes')


### DATABASE CONFIGURATION ###
# Adapter to use--either 'mysql' or 'sqlite'
SQL_ADAPTER = 'sqlite'

# SQLite pat
SQLALCHEMY_DATABASE_URI = 'sqlite:///../app.sqlite'

### Logging ###
LOGGING_PATH = join(DATA_DIR, 'log.txt')
LOGGING_LEVEL = 'DEBUG'

### Celery settings for background tasks ###
CELERY_BROKER_URL = 'redis://localhost:6379'
CELERY_RESULT_BACKEND = 'redis://localhost:6379'

# Error logging with Opbeat
OPBEAT_ENABLED = False
OPBEAT_ORGANIZATION_ID = "..."
OPBEAT_APP_ID = "..."
OPBEAT_SECRET_TOKEN = "..."
OPBEAT_DEBUG = True

### Flask-Mail settings ###
MAIL_ENABLE = False
MAIL_USERNAME = os.getenv('MAIL_USERNAME', 'email@example.com')
MAIL_PASSWORD = os.getenv('MAIL_PASSWORD', 'password')
MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER',
                                '"MyApp" <noreply@example.com>')
MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
MAIL_PORT = int(os.getenv('MAIL_PORT', '465'))
MAIL_USE_SSL = int(os.getenv('MAIL_USE_SSL', True))

### App-level configuration ###
DEBUG = True
PROTOTYPE = True
