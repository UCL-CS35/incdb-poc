from flask import render_template, Blueprint
from flask import request, send_from_directory
from flask_user import roles_accepted

from app import app
from app.controllers import contribute
from app.models.decodings import *
from app.models.collections import *
from app.models.analysis import *
from app.initializers.settings import *

from app.core.decode import decode_collection

from sqlalchemy import *

import os
import zipfile

admin_blueprint = Blueprint('admin', __name__, url_prefix='/admin')


@admin_blueprint.route('/')
@roles_accepted('admin')  # Limits access to users with the 'admin' role
def index():
    """ Fetches and display all collections """
    collections = Collection.query

    return render_template(
        'admin/index.html',
        collections=collections)


@admin_blueprint.route('/upload/', methods=['POST'])
def upload():
    """ Upload processed dataset and start background task """
    if request.method == 'POST':
        collection_name = str(request.args.get('collection'))
        file = request.files['file']
        if file:
            path = os.path.join(PROCESSED_IMAGE_DIR, collection_name)
            unzip(file, path)
            collection = Collection.query
            collection = collection.filter_by(name=collection_name).first()
            decode_collection.delay(
                settings.PROCESSED_IMAGE_DIR,
                collection_name,
                collection.movie_name)
            # TODO(Johnson) Set collection.decoded to true after the celery task
            collection.decoded = False
            db.session.commit()
        else:
            print "No file found"

    return contribute.collection(collection_name)


def unzip(source_filename, dest_dir):
    """ Extract content from zip file """
    with zipfile.ZipFile(source_filename) as zf:
        for member in zf.infolist():
            # Path traversal defense copied from
            # http://hg.python.org/cpython/file/tip/Lib/http/server.py#l789
            words = member.filename.split('/')
            if words[0] == '__MACOSX':
                continue
            path = dest_dir
            for word in words[:-1]:
                drive, word = os.path.splitdrive(word)
                head, word = os.path.split(word)
                if word in (os.curdir, os.pardir, ''):
                    continue
            zf.extract(member, path)


@admin_blueprint.route('/download/<path:user_id>/<path:collection_name>')
def download_folder(user_id, collection_name):
    """" Prepare and download raw dataset """
    collection_folder = os.path.join(UPLOAD_DIR, user_id, collection_name)
    zipped = "%s.zip" % (collection_name)
    zfile = os.path.join(UPLOAD_DIR, user_id, zipped)
    zfile = zipfile.ZipFile(zfile, 'w', zipfile.ZIP_DEFLATED)

    for root, dirs, files in os.walk(collection_folder):
        print root
        for file in files:
            zfile.write(os.path.join(root, file), file)
            print file

    zfile.close()
    path = os.path.join(UPLOAD_DIR, user_id)

    return send_from_directory(path, zipped, as_attachment=True)

# Register blueprint
app.register_blueprint(admin_blueprint)
