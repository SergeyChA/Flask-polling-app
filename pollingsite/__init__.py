from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from pollingsite import config


db = SQLAlchemy()
bcrypt = Bcrypt()


def create_app():
    app = Flask(__name__)
    app.config.from_object(config)
    db.init_app(app)
    bcrypt.init_app(app)
    # Create Tables
    # with app.app_context():
    #     db.create_all()

    from pollingsite.home.routes import home
    from pollingsite.auth.routes import auth
    app.register_blueprint(home)
    app.register_blueprint(auth)

    return app
