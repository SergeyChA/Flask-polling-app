from flask import (
    Blueprint,
    render_template,
    request,
    flash,
    redirect,
    url_for,
)
from .forms import FormAccountUpdate
from pollingsite import db
from flask_login import login_required, current_user
from .utils import save_picture


account = Blueprint('account', __name__, url_prefix='/account')


@account.route("/", methods=['GET', 'POST'])
@login_required
def profile():
    form = FormAccountUpdate()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = form.picture.data
            current_user.image_avatar = save_picture(picture_file)
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Ваши данные обновлены', 'success')
        return redirect(url_for('account.profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_avatar = url_for(
        'static', filename='images/' + current_user.image_avatar
    )
    return render_template(
        'account.html', title='Account', image_avatar=image_avatar, form=form
    )
