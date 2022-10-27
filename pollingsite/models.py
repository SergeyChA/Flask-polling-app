from datetime import datetime
from pollingsite import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(30), unique=True, nullable=False)
    username = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    image_avatar = db.Column(db.String, nullable=False, default='default.png')
    created_at = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return self.username

    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.password = password
