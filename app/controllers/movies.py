from flask import render_template, Blueprint
from flask import request, abort

from app import app, db
from app.models import *
from app.models.decodings import Decoding
from app.controllers.home import paginate

from sqlalchemy import *

movies_blueprint = Blueprint('movies', __name__, url_prefix='/movies')


@movies_blueprint.route('/', methods=['GET', 'POST'])
@movies_blueprint.route('/<int:page>', methods=['GET', 'POST'])
def index(page=1):
    movies = db.session.query(Decoding.movie, Decoding.image_decoded_at)
    movies = movies.distinct()
    movies = paginate(movies, page, 10, False)
    return render_template(
      "movies/index.html",
      movies=movies)


@movies_blueprint.route('/<selected_movie>/', methods=['GET'])
def select_movie(selected_movie, page=1):
    tmp = request.args.get('page')
    if tmp is not None:
        page = int(tmp)
    components = Decoding.query.filter_by(movie=selected_movie)

    if components.count() == 0:
        abort(404)

    components = components.paginate(page, 10, False)
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
        terms=finalterms)


@movies_blueprint.route('/<selected_movie>/<selected_term>')
@movies_blueprint.route('/<selected_movie>/<selected_term>/<int:page>')
def select_movie_term(selected_movie, selected_term, page=1):
    condition = Decoding.movie == selected_movie
    condition = and_(condition, Decoding.term == selected_term)
    components = Decoding.query.filter(condition)
    if components.count() == 0:
        abort(404)
    components = components.paginate(page, 10, False)
    return render_template(
        "movies/select_term.html",
        components=components,
        selected_term=selected_term,
        selected_movie=selected_movie)


@movies_blueprint.route('/search_movie')
def search():
    search = request.args.get('movie')
    results = db.session.query(Decoding.movie, Decoding.image_decoded_at)
    results = results.filter(Decoding.movie.like('%' + search + '%'))
    results = results.distinct()
    return render_template(
        'movies/search_movie.html',
        movies=list(results))


app.register_blueprint(movies_blueprint)
