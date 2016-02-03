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

movies_blueprint = Blueprint('movies', __name__, url_prefix='/movies')

@movies_blueprint.route('/')
def index():
    movies = db.session.query(Decoding.movie).distinct()
    return render_template("movies/index.html", movies=movies)

@movies_blueprint.route('/<selected_movie>')
def select_movie(selected_movie):
    components = Decoding.query.filter_by(movie = selected_movie).all()
    terms = Decoding.query.filter_by(movie = selected_movie).group_by(Decoding.term)
    return render_template("movies/select_movie.html", components = components, selected_movie = selected_movie, terms=terms)

@movies_blueprint.route('/<selected_movie>/<selected_term>')
def select_movie_term(selected_movie, selected_term):
    components = Decoding.query.filter(and_(Decoding.movie == selected_movie, Decoding.term == selected_term)).all()
    return render_template("movies/select_term.html", components = components, selected_term = selected_term)

app.register_blueprint(movies_blueprint)