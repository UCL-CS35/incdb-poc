from flask import redirect, render_template, Blueprint
from flask import request, url_for
from flask_user import current_user, login_required

from app import app, db
from app.core.forms import UserProfileForm
from app.models.collections import Collection
from app.models import *

from app.initializers import mycelery
from app.initializers.settings import *
from app.initializers.celerydb import db_session

import celery
import shutil

from sqlalchemy import *

user_blueprint = Blueprint('user', __name__, url_prefix='/user')

class SqlAlchemyTask(celery.Task):
    """ An abstract Celery Task that ensures that the connection the the
    database is closed on task completion """
    abstract = True

    def after_return(self, status, retval, task_id, args, kwargs, einfo):
        db_session.remove()

def delete_Collection(user, collection):
    collection_dir = os.path.join(UPLOAD_DIR,user,collection)
    if(os.path.exists(collection_dir)):
        shutil.rmtree(collection_dir)
        print "Deletion successful"
    collection_db = db_session.query(Collection).filter_by(user_id = user, name=collection)
    for list in collection_db:
        print list.id
        db_session.delete(list)
    db_session.commit()
    print "Deleted entry"

@user_blueprint.route('/account/', methods=['GET', 'POST'])
@login_required
def user_account():
    """ Fetch and update user account """
    form = UserProfileForm(request.form, current_user)

    if request.method == 'POST' and form.validate():
        form.populate_obj(current_user)
        db.session.commit()
        return redirect(url_for('home.index'))

    return render_template(
        'user/account.html',
        form=form)


@user_blueprint.route('/collections/')
@login_required  # Limits access to authenticated users
def user_collections():
    """ Fetch current user's collections """
    return render_template(
        "user/collections.html",
        collections=current_user.collections)

@user_blueprint.route('/collections/refresh')
@login_required  # Limits access to authenticated users
def refresh_user_collections():
    userid = request.args.get('user')
    collection_name = request.args.get('collection')
    delete_Collection(userid, collection_name)
    """ Fetch current user's collections """
    return render_template(
        "user/collections.html",
        collections=current_user.collections)


# Register blueprint
app.register_blueprint(user_blueprint)
