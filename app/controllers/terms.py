from flask import render_template, Blueprint
from flask import request, abort
from flask import send_from_directory

from app import app, db
from app.models import *
from app.models.decodings import Decoding
from app.controllers.home import paginate
from app.initializers.settings import *

from sqlalchemy import *

terms_blueprint = Blueprint('terms', __name__, url_prefix='/terms')


@terms_blueprint.route('/', methods=['GET', 'POST'])
@terms_blueprint.route('/<int:page>', methods=['GET', 'POST'])
def index(page=1):
    """ Fetch all Movies from Decoding table """
    terms = db.session.query(Decoding.term).distinct()
    terms = paginate(terms, page, 10, False)

    return render_template(
      "terms/index.html",
      terms=terms)


@terms_blueprint.route('/<selected_term>/', methods=['GET'])
def select_term(selected_term, page=1):
    """ Fetch Movies and Components for Term """
    tmp = request.args.get('page')
    if tmp is not None:
        page = int(tmp)

    components = Decoding.query.filter_by(term=selected_term)
    if components.count() == 0:
        abort(404)
    components = components.paginate(page, 10, False)

    movies = Decoding.query.filter_by(term=selected_term)
    movies = movies.group_by(Decoding.movie)

    return render_template(
      "terms/select_term.html",
      components=components,
      selected_term=selected_term,
      movies=movies)


@app.route('/data/images/analyses/<path:term_name>')
def load_term(term_name):
    """ Fetch Term for Location Analysis folder """
    return send_from_directory(
        LOCATION_ANALYSIS_DIR,
        term_name,
        as_attachment=True)


@terms_blueprint.route('/search_term')
def search():
    """ Match query with Term column in Decoding table """
    search = request.args.get('term')

    results = db.session.query(Decoding.term, Decoding.term)
    results = results.filter(Decoding.term.like('%' + search + '%'))
    results = results.distinct()

    return render_template(
        'terms/search_term.html',
        terms=list(results))


# Register blueprint
app.register_blueprint(terms_blueprint)
