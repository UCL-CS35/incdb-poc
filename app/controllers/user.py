from flask import redirect, render_template, Blueprint
from flask import request, url_for
from flask_user import current_user, login_required

from app import app, db
from app.core.forms import UserProfileForm
from app.models import *

from sqlalchemy import *

user_blueprint = Blueprint('user', __name__, url_prefix='/user')


@user_blueprint.route('/account/', methods=['GET', 'POST'])
@login_required
def user_account():

    form = UserProfileForm(request.form, current_user)

    if request.method == 'POST' and form.validate():
        form.populate_obj(current_user)
        db.session.commit()
        return redirect(url_for('home.index'))

    # Process GET or invalid POST
    return render_template(
        'user/account.html',
        form=form)


@user_blueprint.route('/collections/')
@login_required  # Limits access to authenticated users
def user_collections():

    return render_template(
        "user/collections.html",
        collections=current_user.collections)

# Register blueprint
app.register_blueprint(user_blueprint)
