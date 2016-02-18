from flask import redirect, render_template, render_template_string, Blueprint
from flask import request, url_for
from flask_user import current_user, login_required, roles_accepted

from app import app, db
from app.core.forms import UserProfileForm, CollectionForm
from app.models.collections import Collection
from app.models.users import User
from app.initializers import settings

from uuid import uuid4

import os, time
import json
import glob

from sqlalchemy import *

import zipfile

contribute_blueprint = Blueprint('contribute', __name__, url_prefix='/')

@contribute_blueprint.route('contribute/new', methods=["POST", "GET"])
@login_required  # Limits access to authenticated users
def new_collection():

    form = CollectionForm(request.form)
    
    # Process valid POST
    if request.method == 'POST' and form.validate():

        # Copy form fields to collection fields
        collection = Collection()
        form.populate_obj(collection)

        current_user.collections.append(collection)

        db.session.add(collection)

        # Save collection
        db.session.commit()

        return redirect(url_for("contribute.upload_files", collection=collection.name))

    return render_template("contribute/new.html", form=form)


@contribute_blueprint.route('contribute/upload/')
@login_required  # Limits access to authenticated users
def upload_files():
    c = request.args.get('collection')
    return render_template("contribute/upload.html", collection=c)


@contribute_blueprint.route('upload', methods=["POST"])
@login_required  # Limits access to authenticated users
def upload():
    """Handle the upload of a file."""
    form = request.form

    # Create a unique "session ID" for this particular batch of uploads.
    uuid = str(request.args.get('collection'))
    # uuid = str(uuid4())
    upload_key = str(current_user.id) + "/" + uuid

    # Is the upload using Ajax, or a direct POST by the form?
    is_ajax = False
    if form.get("__ajax", None) == "true":
        is_ajax = True

    # Target folder for these uploads.
    target = "uploads/{}".format(current_user.id)
    if not os.path.exists(target):
        try:
            os.mkdir(target)
        except:
            if is_ajax:
                return ajax_response(False, "Couldn't create user directory: {}".format(target))
            else:
                return "Couldn't create user directory: {}".format(target)

    # Target folder for these uploads.
    target = "uploads/{}".format(upload_key)
    if not os.path.exists(target):
        try:
            os.mkdir(target)
        except:
            if is_ajax:
                return ajax_response(False, "Couldn't create upload directory: {}".format(target))
            else:
                return "Couldn't create upload directory: {}".format(target)

    for upload in request.files.getlist("file"):
        filename = upload.filename.rsplit("/")[0]
        unzip(upload, target)

    if is_ajax:
        return ajax_response(True, uuid)
    else:
        return redirect(url_for("contribute.collection") + '/' + uuid)

def unzip(source_filename, dest_dir):
    with zipfile.ZipFile(source_filename) as zf:
        for member in zf.infolist():
            # Path traversal defense copied from
            # http://hg.python.org/cpython/file/tip/Lib/http/server.py#l789
            words = member.filename.split('/')
            if words[0] == '__MACOSX': continue
            path = dest_dir
            for word in words[:-1]:
                drive, word = os.path.splitdrive(word)
                head, word = os.path.split(word)
                if word in (os.curdir, os.pardir, ''): continue
            zf.extract(member, path)

def ajax_response(status, msg):
    status_code = "ok" if status else "error"
    return json.dumps(dict(
        status=status_code,
        msg=msg,
    ))

@contribute_blueprint.route('collection/<collection_name>/')
@login_required  # Limits access to authenticated users
def collection(collection_name):

    collection = Collection.query.filter_by(name=collection_name).first()
    user = User.query.filter_by(id=collection.user_id).first()
    files = dict()

    # Get their files.
    user_dir = "uploads/{}".format(collection.user_id)
    if not os.path.isdir(user_dir):
        return render_template("contribute/collection.html", collection=collection, files=files, user=user)

    # Get their files.
    collection_dir = user_dir + '/' + str(collection_name)
    if not os.path.isdir(collection_dir):
        return render_template("contribute/collection.html", collection=collection, files=files, user=user)

    for file in glob.glob("{}/*".format(collection_dir)):
        fname = file.split(os.sep)[-1]
        modified_time = time.ctime(os.path.getmtime(file))
        if fname in files:
            files[fname].append(modified_time)
        else:
            files[fname] = modified_time

    return render_template("contribute/collection.html", collection=collection, files=files, user=user)


app.register_blueprint(contribute_blueprint)