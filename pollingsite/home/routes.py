from flask import Blueprint


home = Blueprint('home', __name__)


@home.route("/")
def hello_world():
    return {"message": "HELLO WORLD"}