from flask import render_template, Blueprint
from flask_user import roles_accepted

from app import app
from app.models import *

from sqlalchemy import *

admin_blueprint = Blueprint('admin', __name__, url_prefix='/admin')


# The Admin page is accessible to users with the 'admin' role
@admin_blueprint.route('/')
@roles_accepted('admin')  # Limits access to users with the 'admin' role
def index():
    return render_template('admin/admin_page.html')

# Register blueprint
app.register_blueprint(admin_blueprint)
