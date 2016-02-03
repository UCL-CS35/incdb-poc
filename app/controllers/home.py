from flask import redirect, render_template, render_template_string, Blueprint

from app import app, db


from sqlalchemy import *

home_blueprint = Blueprint('home', __name__, url_prefix='/')

# The Index page is accessible to anyone
@home_blueprint.route('')
def index():
    return render_template('index.html')


# Register blueprint
app.register_blueprint(home_blueprint)
