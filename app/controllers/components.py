from flask import redirect, render_template, render_template_string, Blueprint
from flask import request, url_for
from flask_user import current_user, login_required, roles_accepted

from app import app, db
from app.core.forms import UserProfileForm, CollectionForm
from app.models import *
from app.models.decodings import Decoding
from app.initializers import settings

from uuid import uuid4

import os, time
import json
import glob

from sqlalchemy import *

components_blueprint = Blueprint('component', __name__, url_prefix='/component')

@components_blueprint.route('/<component_uuid>')
def select_component(component_uuid):
    component = Decoding.query.filter_by(uuid=component_uuid).first()
    return render_template("components/selected_component.html", selected_component = component)


app.register_blueprint(components_blueprint)