from flask import render_template, Blueprint
from flask import request, jsonify
from app.models.decodings import Decoding

from app import app, db

from sqlalchemy import *
import flask_sqlalchemy as sqlalchemy

home_blueprint = Blueprint('home', __name__, url_prefix='/')


# The Index page is accessible to anyone
@home_blueprint.route('')
def index():
    movies = db.session.query(Decoding.movie, Decoding.image_decoded_at)
    movies = movies.distinct().limit(10)
    return render_template('index.html', movies=movies)


@home_blueprint.route('_search_movie')
def search_movie():
    search = request.args.get('term')
    results = db.session.query(Decoding.movie, Decoding.movie)
    results = results.filter(Decoding.movie.like('%' + search + '%'))
    results = results.distinct()
    return jsonify(results)


@home_blueprint.route('search')
def search():
    search = request.args.get('movie')
    results = db.session.query(Decoding.movie, Decoding.movie)
    results = results.filter(Decoding.movie.like('%' + search + '%'))
    results = results.distinct()
    return render_template('search.html', movies=list(results))


@home_blueprint.route('faq')
def faq():
    return render_template('faq.html')


def paginate(query, page, per_page=20, error_out=True):
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
    return render_template('404.html'), 404

# Register blueprint
app.register_blueprint(home_blueprint)
