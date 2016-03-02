from flask import render_template, Blueprint
from flask import request

from app import app, db
from app.models import *
from app.models.decodings import Decoding

from sqlalchemy import *

movies_blueprint = Blueprint('movies', __name__, url_prefix='/movies')


@movies_blueprint.route('/')
def index():
    movies = db.session.query(Decoding.movie, Decoding.image_decoded_at).distinct()
    return render_template("movies/index.html", movies=movies)


@movies_blueprint.route('/<selected_movie>')
def select_movie(selected_movie):
    components = Decoding.query.filter_by(movie = selected_movie).all()
    terms = Decoding.query.filter_by(movie = selected_movie).group_by(Decoding.term)
    return render_template(
      "movies/select_movie.html",
      components=components,
      selected_movie=selected_movie,
      terms=terms)


@movies_blueprint.route('/<selected_movie>/<selected_term>')
def select_movie_term(selected_movie, selected_term):
    components = Decoding.query.filter(and_(Decoding.movie == selected_movie, Decoding.term == selected_term)).all()
    return render_template(
        "movies/select_term.html",
        components=components,
        selected_term=selected_term)


@movies_blueprint.route('/search_movie')
def search():
    search = request.args.get('movie')
    results = db.session.query(Decoding.movie, Decoding.movie).filter(Decoding.movie.like('%' + search + '%')).distinct()
    return render_template(
        'movies/search_movie.html',
        movies=list(results))

app.register_blueprint(movies_blueprint)
