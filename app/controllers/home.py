from flask import render_template, Blueprint
from flask import request, jsonify

from app import app, db
from app.models.decodings import Decoding
from app.initializers.settings import *

from sqlalchemy import *
import flask_sqlalchemy as sqlalchemy

from os.path import join
import simplejson as json


home_blueprint = Blueprint('home', __name__, url_prefix='/')


@home_blueprint.route('')
def index():
    """ Fetch 10 latest movies """
    movies = db.session.query(
        Decoding.movie,
        Decoding.image_decoded_at)
    movies = movies.distinct(Decoding.movie).group_by(Decoding.movie)
    movies = movies.limit(10)

    return render_template('index.html', movies=movies)


@home_blueprint.route('guide')
def guide():
    return render_template('guide.html')


@home_blueprint.route('_search_movie')
def search_movie():
    """ Autocomplete with query for Movie column in Decoding table """
    search = request.args.get('movie')
    results = db.session.query(Decoding.movie, Decoding.movie)
    results = results.filter(Decoding.movie.like('%' + search + '%'))
    results = results.distinct(Decoding.movie).group_by(Decoding.movie)

    return jsonify(results)


@home_blueprint.route('search')
def search():
    """ Match query with Movie column in Decoding table """
    search = request.args.get('movie')
    results = db.session.query(Decoding.movie, Decoding.movie)
    results = results.filter(Decoding.movie.like('%' + search + '%'))
    results = results.distinct(Decoding.movie).group_by(Decoding.movie)

    return render_template('search.html', movies=list(results))


@home_blueprint.route('faq/')
def faq():
    """ Display FAQ from json source file """
    data = json.load(open(join(ROOT_DIR, 'data', 'faq.json')))

    return render_template(
        'faq.html',
        data=data)


def paginate(query, page, per_page=20, error_out=True):
    """ Custom pagination for query """
    if error_out and page < 1:
        abort(404)

    items = query.limit(per_page).offset((page - 1) * per_page).all()
    if not items and page != 1 and error_out:
        abort(404)

    # No need to count if we're on the first page and there are fewer
    # items than we expected.
    if page == 1 and len(items) < per_page:
        total = len(items)
    else:
        total = query.order_by(None).count()

    return sqlalchemy.Pagination(query, page, per_page, total, items)


@app.errorhandler(404)
def page_not_found(e):
    """ Display custom 404 page """
    return render_template('404.html'), 404

# Register blueprint
app.register_blueprint(home_blueprint)
