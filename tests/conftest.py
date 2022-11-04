import pytest

from pollingsite import create_app, db, bcrypt
from pollingsite.models import User
from pollingsite import test_config


@pytest.fixture(scope='module')
def test_client():
    # Create a Flask app configured for testing
    flask_app = create_app(test_config)
    # Create a test client using the Flask application configured for testing
    with flask_app.test_client() as testing_client:
        # Establish an application context
        with flask_app.app_context():
            yield testing_client  # this is where the testing happens!


@pytest.fixture(scope='module')
def init_database(test_client):
    # Delete and Create the database and the database table
    db.drop_all()
    db.create_all()
    # Insert user data
    user = User(
        email='test@mail.ru',
        password=(
            bcrypt
            .generate_password_hash('password')
            .decode("utf-8")
        ),
        username='test'
    )
    db.session.add(user)
    db.session.commit()
    yield  # this is where the testing happens!
