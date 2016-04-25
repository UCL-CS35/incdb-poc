from flask import render_template, Blueprint
from flask import send_from_directory, abort

from app import app
from app.models import *
from app.models.decodings import Decoding
from app.models.collections import Collection
from app.initializers.settings import *

from sqlalchemy import *

import os

components_blueprint = Blueprint(
    'component',
    __name__,
    url_prefix='/component')


@components_blueprint.route('/<component_uuid>')
def select_component(component_uuid):
    """ Fetch Component from Decoding table """
    component = Decoding.query.filter_by(uuid=component_uuid).first()
    if component is None:
        abort(404)

    filename = os.path.join(
        DECODING_RESULTS_DIR,
        component.collection,
        component.filename + '.txt')
    terms = get_terms(filename)

    collection = Collection.query.filter_by(name=component.collection)
    collection = collection.first()

    return render_template(
        "components/selected_component.html",
        selected_component=component,
        collection=collection,
        terms=terms)


def get_terms(filename):
    """ Fetch terms and correlation from text file """
    terms = []
    with open(filename, 'r') as f:
        for line in f:
            termPair = line.split('\t')
            termPair[1] = termPair[1].strip('\n')
            terms.append(termPair)

    return terms


@app.route('/data/images/processed/<path:collection>/<path:file_name>')
def load_component(collection, file_name):
    """ Fetch Component from Processed Image folder """
    return send_from_directory(
        os.path.join(PROCESSED_IMAGE_DIR, collection),
        file_name,
        as_attachment=True)


@app.route('/data/images/processed/<path:collection>/<path:file_name>')
def component_directory(collection, file_name):
    """ Return path for Component """
    return os.path.join(PROCESSED_IMAGE_DIR, collection, file_name)


@app.route('/data/images/<path:comp_name>')
def load_brain_def(comp_name):
    """ Fetch Brain Definition from image folder """
    return send_from_directory(
        IMAGE_DIR,
        comp_name,
        as_attachment=True)

# Register blueprint
app.register_blueprint(components_blueprint)
