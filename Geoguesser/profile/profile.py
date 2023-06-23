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

from .. import db
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
    picture_path = os.path.join(app.root_path, 'profile/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

@profile_bp.route('/', methods=['GET', 'POST'])
@login_required
def profile():
    avatar_file = url_for('profile_bp', filename='profile_pics/' + current_user.avatar_file)
    return render_template('profile.html', title='Account', avatar_file=avatar_file)

@profile_bp.route('/update/', methods=['GET', 'POST'])
@login_required
def update_profile():
    user = User.query.get_or_404(current_user.id)
    form = UpdateUserForm()

    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            user.avatar_file = picture_file
        user.username = save_picture(form.username.data)
        user.email = save_picture(form.email.data)
        user.firstname = save_picture(form.firstname.data)
        user.lastname = save_picture(form.lastname.data)
        db.session.commit()
        flash('Your acount has been updated', 'complete')
        return redirect(url_for('profile_bp.profile'))

    elif request.method == 'GET':
        form.username.data = user.username
        form.email.data = user.email
        form.firstname.data = user.firstname
        form.lastname.data = user.lastname

    avatar_file = url_for('profile_bp', filename='profile_pics/' + user.avatar_file)
    return render_template('profile_update.html', title='Edit Profile', avatar_file=avatar_file, form=form)