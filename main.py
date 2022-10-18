from flask import Flask, request
from models import db, User


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:password@localhost:5432/polling_db"
db.init_app(app)

# Create Tables
# with app.app_context():
#     db.create_all()


def format_user(user: User) -> dict:
    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "created_at": user.created_at,
    }


@app.route("/")
def hello_world():
    return {"message": "HELLO WORLD"}


@app.route("/user", methods=["GET"])
def get_user():
    user = User.query.first()
    return format_user(user)


@app.route("/user", methods=["POST"])
def add_user():
    user = request.json
    new_user = User(**user)
    db.session.add(new_user)
    db.session.commit()
    db.session.refresh(new_user)
    return format_user(new_user)
