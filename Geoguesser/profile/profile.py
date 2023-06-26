from flask import (
    Blueprint, 
    current_app as app,
    render_template, 
    url_for, 
    redirect,
    request,
    flash,
    abort
)
from flask_login import current_user, login_required

from PIL import Image
from .. import db
from ..models import User
from Geoguesser.auth.forms import UpdateUserForm
import os
import secrets

#bp
profile_bp = Blueprint('profile_bp', 
__name__, 
url_prefix='/profile', 
template_folder='templates', 
static_folder='static')


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'profile/static/profile_pics/', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

@profile_bp.route('/', methods=['GET', 'POST'])
@login_required
def profile():
    avatar = url_for('profile_bp.static', filename='profile_pics/'+ current_user.avatar)
    print(avatar)
    return render_template('profile.html', title='Account', avatar=avatar, user=current_user)

@profile_bp.route('/update/', methods=['GET', 'POST'])
@login_required
def update_profile():
    user = User.query.get_or_404(current_user.id)
    form = UpdateUserForm()

    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            user.avatar = picture_file
        user.alias = form.username.data
        user.email = form.email.data
        user.firstname = form.firstname.data
        user.lastname = form.lastname.data
        db.session.commit()
        flash('Your acount has been updated', 'complete')
        return redirect(url_for('profile_bp.profile'))

    elif request.method == 'GET':
        form.username.data = user.alias
        form.email.data = user.email
        form.firstname.data = user.firstname
        form.lastname.data = user.lastname

    avatar = url_for('profile_bp.static', filename='profile_pics/'+current_user.avatar)
    print(avatar)
    return render_template('profile_update.html', title='Edit Profile', avatar=avatar, form=form)