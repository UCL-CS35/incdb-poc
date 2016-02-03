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

terms_blueprint = Blueprint('terms', __name__, url_prefix='/terms')

@terms_blueprint.route('/')
def index():
    #terms = Decoding.query.distinct(Decoding.term).all()
    terms = db.session.query(Decoding.term).distinct()
    return render_template("terms/all_terms.html", terms=terms)

@terms_blueprint.route('/<selected_term>')
def select_term(selected_term):
    components = Decoding.query.filter_by(term = selected_term).all()
    return render_template("terms/selected_term.html", components = components, selected_term = selected_term)


app.register_blueprint(terms_blueprint)