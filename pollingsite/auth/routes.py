from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    flash,
)
from pollingsite import db, bcrypt
from pollingsite.auth.forms import FormSingup, FormLogin
from pollingsite.models import User
from flask_login import login_user, logout_user


auth = Blueprint('auth', __name__)


@auth.route("/singup", methods=["GET", "POST"])
def register():
    form = FormSingup()
    if form.validate_on_submit():
        form.password.data = (
            bcrypt
            .generate_password_hash(form.password.data)
            .decode("utf-8")
        )
        new_user = User(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data
        )
        db.session.add(new_user)
        db.session.commit()
        flash('Вы зарегистрированы!', 'success')
        return redirect(url_for('auth.login'))
    return render_template("singup.html", title="Регистрация", form=form)


@auth.route("/login", methods=["GET", "POST"])
def login():
    form = FormLogin()
    if form.validate_on_submit():
        user = db.session.execute(
            db.select(User).filter(User.email == form.email.data)
        ).scalar()
        if user and bcrypt.check_password_hash(
            user.password, form.password.data
        ):
            login_user(user, remember=form.remember.data)
            return redirect(url_for("account.profile"))
        else:
            flash('Ошибка. Неверный пароль или почта', 'danger')
    return render_template("login.html", title="Авторизация", form=form)


@auth.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))
