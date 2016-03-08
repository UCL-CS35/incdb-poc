from flask import render_template, Blueprint
from flask import request
from flask_user import roles_accepted

from app import app
from app.controllers import contribute
from app.models.decodings import *
from app.models.collections import *
from app.initializers import settings

from app.core.decode import decode_collection

from sqlalchemy import *

import os
import zipfile

admin_blueprint = Blueprint('admin', __name__, url_prefix='/admin')


@admin_blueprint.route('/')
@roles_accepted('admin')  # Limits access to users with the 'admin' role
def index():
    collections = Collection.query
    return render_template(
        'admin/index.html',
        collections=collections)


@admin_blueprint.route(
    '/upload/',
    methods=['POST'])
def upload():
    if request.method == 'POST':
        collection_name = str(request.args.get('collection'))
        file = request.files['file']
        if file:
            path = os.path.join(settings.DECODED_IMAGE_DIR, collection_name)
            unzip(file, path)
            collection = Collection.query
            collection = collection.filter_by(name=collection_name).first()
            decode_collection(
                settings.DECODED_IMAGE_DIR,
                collection_name,
                collection.movie_name)
            collection.decoded = True
            db.session.commit()
            # file.save(path)
        else:
            print "No file found"
    return contribute.collection(collection_name)


def unzip(source_filename, dest_dir):
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

# Register blueprint
app.register_blueprint(admin_blueprint)
