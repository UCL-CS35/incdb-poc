from flask import redirect, render_template, render_template_string, Blueprint
from flask import request, url_for
from flask_user import current_user, login_required, roles_accepted

from app import app, db
from app.core.forms import UserProfileForm, CollectionForm
from app.models import *
from app.models.decodings import Decoding
from app.initializers import settings

from uuid import uuid4

import os, time
import json
import glob

from sqlalchemy import *

user_blueprint = Blueprint('user', __name__, url_prefix='/user')

# The Admin page is accessible to users with the 'admin' role
@user_blueprint.route('admin/')
@roles_accepted('admin')  # Limits access to users with the 'admin' role
def admin_page():
    return render_template('admin/admin_page.html')


@user_blueprint.route('/account/', methods=['GET', 'POST'])
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
        return redirect(url_for('home.index'))

    # Process GET or invalid POST
    return render_template('user/account.html',
                           form=form)


@user_blueprint.route('/collections/')
@login_required  # Limits access to authenticated users
def user_collections():

    return render_template("user/collections.html",
        collections=current_user.collections
    )

# Register blueprint
app.register_blueprint(user_blueprint)
