from flask import redirect, render_template, render_template_string, Blueprint
from flask import request, url_for
from flask_user import current_user, login_required, roles_accepted
from flask import send_from_directory

from app import app, db
from app.core.forms import UserProfileForm, CollectionForm
from app.models import *
from app.models.decodings import Decoding
from app.initializers import settings
from app.initializers.settings import *

from uuid import uuid4

import os, time
from os import unlink, listdir, mkdir
from os.path import join, basename, exists, isdir
import json
import glob

from sqlalchemy import *

components_blueprint = Blueprint('component', __name__, url_prefix='/component')

@components_blueprint.route('/<component_uuid>')
def select_component(component_uuid):
    component = Decoding.query.filter_by(uuid=component_uuid).first()

    
    filename = os.path.join(settings.DECODING_RESULTS_DIR, component.movie, component.filename + '.txt')
    terms = []
    with open(filename, 'r') as f:
    #with f = open(infile, "r") :
    	for line in f:
    		
    		termPair = line.split('\t')
    		termPair[1] = termPair[1].strip('\n')
    		terms.append(termPair)
    print terms


    return render_template("components/selected_component.html", selected_component = component, terms=terms)


app.register_blueprint(components_blueprint)

@app.route('/data/images/decoded/<path:movie_name>/<path:file_name>')
def load_component(movie_name, file_name):
    return send_from_directory(os.path.join(DECODED_IMAGE_DIR,movie_name), file_name, as_attachment=True)