# INcDb Proof of Concept

## Setup

Install Virtual Environment using pip:

    pip install virtualenv

Cloning the app

    mkdir INcDb
    cd INcDb
    git clone https://github.com/UCL-CS35/incdb-user.git incdb-user

Create the 'incdb-user' virtual environment
    
    mkvirtualenv incdb_user_env

Install required Python packages
    
    cd /path/to/incdb-user
    workon incdb_user_env
    pip install -r requirements.txt
    
## Configuring the app

Settings common to all environments are found in app/startup/common_settings.py

The example environment-specific settings are found in app/env_settings_example.py

Copy the `app/env_settings_example.py` to an `env_settings.py` that resides **outside** the code directory and point the OS environment variable `ENV_SETTINGS_FILE` to this file.

    # Copy env_settings.py and place it outside of the code directory
    cd /path/to/project
    cp app/env_settings_example.py ../env_settings.py
    
    # Point the OS environment variable `ENV_SETTINGS_FILE` to this file
    export ENV_SETTINGS_FILE=/path/to/env_settings.py

Note: DO NOT edit app/config/settings.py because checking this into the core repository will expose security sensitive information.

Before we deploying this application, we will have to configure the database URL and SMTP account that will be used to access the database and to send emails.

## Initializing the Database

    # Create DB tables and populate the roles and users tables
    python manage.py init_db

## Running the app

    # Start the Flask development web server
    ./runserver.sh    # will run "python manage.py runserver"

Point your web browser to http://localhost:5000/

You can make use of the following users:
- email `jeremy@incdb.com` with password `Password1`.
- email `ong@incdb.com` with password `Password1`.
- email `johnson@incdb.com` with password `Password1`.
- email `rajind@incdb.com` with password `Password1`.

## Testing the app

    # Run all the automated tests in the tests/ directory
    ./runtests.sh         # will run "py.test -s tests/"


## Generating a test coverage report

    # Run tests and show a test coverage report
    ./runcoverage.sh      # will run py.test with coverage options

## Database migrations

    # Show all DB migration commands
    python manage.py db

## Troubleshooting
If you make changes in the Models and run into DB schema issues, delete the sqlite DB file `app/app.sqlite`.

## Acknowledgements

[Flask-User-starter-app](https://github.com/lingthio/Flask-User-starter-app) was used as a starting point for this code repository.

