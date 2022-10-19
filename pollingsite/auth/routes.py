from flask import (
    Blueprint,
    request,
    render_template
)
from pollingsite import db, bcrypt
from pollingsite.forms import FormSingup
from pollingsite.models import User


auth = Blueprint('auth', __name__)


def format_user(user: User) -> dict:
    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "created_at": user.created_at,
    }


@auth.route("/user/<int:id>")
def get_user(id):
    user = User.query.filter(User.id == id).first()
    return format_user(user)


# @auth.route("/singup", methods=["POST"])
# def create_user():
#     user = request.json
#     user["password"] = (
#         bcrypt
#         .generate_password_hash(user["password"])
#         .decode("utf-8")
#     )
#     new_user = User(**user)
#     db.session.add(new_user)
#     db.session.commit()
#     db.session.refresh(new_user)
#     return format_user(new_user)

@auth.route("/singup", methods=["GET", "POST"])
def create_user():
    form = FormSingup(request.form)
    if form.validate_on_submit():
        form.data["password"] = (
            bcrypt
            .generate_password_hash(form.data["password"])
            .decode("utf-8")
        )
        new_user = User(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data
        )
        db.session.add(new_user)
        db.session.commit()
        db.session.refresh(new_user)
        return format_user(new_user)
    return render_template("singup.html", form=form)


@auth.route("/login", methods=["POST"])
def login_user():
    form = request.json
    user = User.query.filter(User.email == form["email"]).first()
    if user:
        if bcrypt.check_password_hash(user.password, form["password"]):
            return {"message": "Logged in successfully."}
    return {"message": "Bad email or password"}
