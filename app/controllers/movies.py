from flask import render_template, Blueprint
from flask import request, abort
from flask import send_from_directory

from app import app, db
from app.models import *
from app.models.decodings import Decoding
from app.models.collections import Collection
from app.controllers.home import paginate
from app.initializers.settings import *

from sqlalchemy import *

import os

movies_blueprint = Blueprint('movies', __name__, url_prefix='/movies')


@movies_blueprint.route('/', methods=['GET', 'POST'])
@movies_blueprint.route('/<int:page>', methods=['GET', 'POST'])
def index(page=1):
    """ Fetch all Movies """
    movies = db.session.query(
        Decoding.movie,
        Decoding.image_decoded_at)
    movies = movies.distinct(Decoding.movie).group_by(Decoding.movie)
    movies = paginate(movies, page, 10, False)

    return render_template(
      "movies/index.html",
      movies=movies)


@movies_blueprint.route('/<selected_movie>/', methods=['GET'])
def select_movie(selected_movie, page=1):
    """ Fetch Components, Collections and Terms for Movie """
    tmp = request.args.get('page')
    if tmp is not None:
        page = int(tmp)

    components = Decoding.query.filter_by(movie=selected_movie)
    if components.count() == 0:
        abort(404)
    components = components.paginate(page, 10, False)

    collections = Collection.query.filter_by(movie_name=selected_movie)

    # TODO Update correlation formula
    terms = Decoding.query.filter_by(movie=selected_movie)
    total_count = terms.count()
    decodings = terms
    terms = terms.group_by(Decoding.term)
    finalterms = []
    for term in terms:
        selected_term_decodings = decodings.filter_by(term=term.term)
        correlation = 0
        for decoding in selected_term_decodings:
            correlation += decoding.correlation
        term_count = selected_term_decodings.count()
        mean_corr = correlation / term_count
        ratio = float(term_count) / total_count
        term_corr = mean_corr * ratio
        one_term = [term.term, term_corr]
        finalterms.append(one_term)

    return render_template(
        "movies/select_movie.html",
        components=components,
        selected_movie=selected_movie,
        collections=collections,
        terms=finalterms)


@movies_blueprint.route('/<selected_movie>/<selected_term>')
@movies_blueprint.route('/<selected_movie>/<selected_term>/<int:page>')
def select_movie_term(selected_movie, selected_term, page=1):
    """ Fetch Components and Collections for Movie's Terms """
    condition = Decoding.movie == selected_movie
    condition = and_(condition, Decoding.term == selected_term)
    components = Decoding.query.filter(condition)

    collection = Collection.query.filter_by(movie_name=selected_movie).first()
    if components.count() == 0:
        abort(404)
    components = components.paginate(page, 10, False)

    return render_template(
        "movies/select_term.html",
        collection=collection,
        components=components,
        selected_term=selected_term,
        selected_movie=selected_movie)


@app.route('/data/images/processed/<path:selected_movie>/terms/<path:term_name>')
def load_term_component(selected_movie, term_name):
    """ Fetch Component from Processed Image folder """
    return send_from_directory(
        os.path.join(PROCESSED_IMAGE_DIR, selected_movie, "terms"),
        term_name,
        as_attachment=True)


@movies_blueprint.route('/search_movie')
def search():
    """ Match query with Movie column in Decoding table """
    search = request.args.get('movie')

    results = db.session.query(Decoding.movie, Decoding.image_decoded_at)
    results = results.filter(Decoding.movie.like('%' + search + '%'))
    results = results.distinct()

    return render_template(
        'movies/search_movie.html',
        movies=list(results))

# Register blueprint
app.register_blueprint(movies_blueprint)
