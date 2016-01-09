from flask import redirect, render_template, render_template_string, Blueprint
from flask import request, url_for
from flask_user import current_user, login_required, roles_accepted
from app import app, db
from app.core.forms import UserProfileForm, CollectionForm
from uuid import uuid4
from app.core.models import Collection

import os, time
import json
import glob


core_blueprint = Blueprint('core', __name__, url_prefix='/')

# The Index page is accessible to anyone
@core_blueprint.route('')
def index():
    return render_template('index.html')


@core_blueprint.route('contribute/new')
def new_collection():
    form = CollectionForm(request.form)
    return render_template("contribute/new.html", form=form)


@core_blueprint.route('collection/create', methods=["POST"])
def create_collection():
    
    form = CollectionForm(request.form)
    collection = Collection()

    # Process valid POST
    if request.method == 'POST' and form.validate():
        # Copy form fields to user_profile fields
        form.populate_obj(collection)

        current_user.collections.append(collection)

        db.session.add(collection)

        # Save user_profile
        db.session.commit()

        return redirect(url_for("core.upload_files", collection=collection.name))

    return render_template("contribute/new.html", form=form)


@core_blueprint.route('collection/<collection_name>/')
def collection(collection_name):

    collection = Collection.query.filter_by(name=collection_name).first()

    # Get their files.
    root = "uploads/{}".format(collection.user_id)
    if not os.path.isdir(root):
        return "Error: User not found!"

    # Get their files.
    collection_dir = root + '/' + str(collection_name)
    if not os.path.isdir(root):
        return "Error: Collection not found!"

    files = dict()
    for file in glob.glob("{}/*".format(collection_dir)):
        fname = file.split(os.sep)[-1]
        modified_time = time.ctime(os.path.getmtime(file))
        if fname in files:
            files[fname].append(modified_time)
        else:
            files[fname] = modified_time

    return render_template("contribute/collection.html", collection=collection, files=files)


@core_blueprint.route('contribute/upload/')
@login_required  # Limits access to authenticated users
def upload_files():
    c = request.args.get('collection')
    return render_template("contribute/upload.html", collection=c)


@core_blueprint.route('upload', methods=["POST"])
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
    try:
        os.mkdir(target)
    except:
        if is_ajax:
            return ajax_response(False, "Couldn't create upload directory: {}".format(target))
        else:
            return "Couldn't create upload directory: {}".format(target)

    for upload in request.files.getlist("file"):
        filename = upload.filename.rsplit("/")[0]
        destination = "/".join([target, filename])
        print "Accept incoming file:", filename
        print "Save it to:", destination
        upload.save(destination)

    if is_ajax:
        return ajax_response(True, uuid)
    else:
        return redirect(url_for("core.upload_success", uuid=uuid))


@core_blueprint.route('contribute/success/<uuid>')
def upload_success(uuid):
    """The location we send them to at the end of the upload."""

    # Get their files.
    root = "uploads/" + str(current_user.id) + "/" + str(uuid)
    if not os.path.isdir(root):
        return "Error: UUID not found!"

    files = []
    for file in glob.glob("{}/*.*".format(root)):
        fname = file.split(os.sep)[-1]
        files.append(fname)

    return render_template("contribute/success.html",
        uuid=uuid,
        files=files
    )


def ajax_response(status, msg):
    status_code = "ok" if status else "error"
    return json.dumps(dict(
        status=status_code,
        msg=msg,
    ))


# The Admin page is accessible to users with the 'admin' role
@core_blueprint.route('admin/')
@roles_accepted('admin')  # Limits access to users with the 'admin' role
def admin_page():
    return render_template('admin/admin_page.html')


@core_blueprint.route('user/profile/', methods=['GET', 'POST'])
@login_required
def user_account():
    # Initialize form
    form = UserProfileForm(request.form, current_user)

    # Process valid POST
    if request.method == 'POST' and form.validate():
        # Copy form fields to user_profile fields
        form.populate_obj(current_user)

        # Save user_profile
        db.session.commit()

        # Redirect to home page
        return redirect(url_for('core.index'))

    # Process GET or invalid POST
    return render_template('user/user_profile_page.html',
                           form=form)


@core_blueprint.route('user/collections/')
@login_required  # Limits access to authenticated users
def user_collections():

    return render_template("user/collections.html",
        collections=current_user.collections
    )


# Register blueprint
app.register_blueprint(core_blueprint)
