from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    from pollingsite.main.routes import main
    from pollingsite.auth.routes import auth
    from pollingsite.account.routes import account
    app.register_blueprint(main)
    app.register_blueprint(auth)
    app.register_blueprint(account)

    return app
