from flask import redirect, render_template, render_template_string, Blueprint
from flask import request, jsonify
from app.models.decodings import Decoding

from app import app, db


from sqlalchemy import *

home_blueprint = Blueprint('home', __name__, url_prefix='/')

# The Index page is accessible to anyone
@home_blueprint.route('')
def index():
    return render_template('index.html')

@home_blueprint.route('_search_movie')
def search_movie():
    search = request.args.get('term')
    results = db.session.query(Decoding.movie, Decoding.movie).filter(Decoding.movie.like('%' + search + '%')).distinct()
    return jsonify(results)

@home_blueprint.route('search')
def search():
	search = request.args.get('movie')
	results = db.session.query(Decoding.movie, Decoding.movie).filter(Decoding.movie.like('%' + search + '%')).distinct()
	return render_template('search.html', movies=list(results))

# Register blueprint
app.register_blueprint(home_blueprint)
