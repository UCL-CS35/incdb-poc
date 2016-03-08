from flask import render_template, Blueprint, send_from_directory
from flask_user import roles_accepted

from app.initializers.settings import *
from app import app
from app.models.decodings import *
from app.models.collections import *

from sqlalchemy import *

import os
import zipfile

admin_blueprint = Blueprint('admin', __name__, url_prefix='/admin')


# The Admin page is accessible to users with the 'admin' role
@admin_blueprint.route('/')
@roles_accepted('admin')  # Limits access to users with the 'admin' role
def index():
	collections = Collection.query
	movies = db.session.query(Decoding.movie, Decoding.image_decoded_at)
	movies = movies.distinct()
	return render_template(
		'admin/index.html',
		collections=collections,
		movies=movies)



@admin_blueprint.route('/download/<path:user_id>/<path:collection_name>')
def download_folder(user_id, collection_name):
	collection_folder = os.path.join(UPLOAD_DIR, user_id, collection_name)
	zipped = "%s.zip" % (collection_name)
	zfile = zipfile.ZipFile(os.path.join(UPLOAD_DIR, user_id, zipped), 'w', zipfile.ZIP_DEFLATED)
	
	for root, dirs, files in os.walk(collection_folder):
		print root
		for file in files:
			zfile.write(os.path.join(root, file), file)
			print file

	zfile.close()
	return send_from_directory(os.path.join(UPLOAD_DIR, user_id),zipped, as_attachment=True)

# Register blueprint
app.register_blueprint(admin_blueprint)
