import pytest

from pollingsite import create_app, db
from pollingsite.models import User
from pollingsite import config


@pytest.fixture(scope='module')
def new_user():
    user = User('test@gmail.com', 'test')
    return user


@pytest.fixture(scope='module')
def test_client():
    # Create a Flask app configured for testing
    flask_app = create_app()
    flask_app.config.from_object(config)

    # Create a test client using the Flask application configured for testing
    with flask_app.test_client() as testing_client:
        # Establish an application context
        with flask_app.app_context():
            yield testing_client  # this is where the testing happens!


@pytest.fixture(scope='module')
def init_database(test_client):
    # Create the database and the database table
    db.drop_all()
    db.create_all()

    # Insert user data
    user1 = User(email='test1111@mail.ru',
                 password='password',
                 username='test1111')
    user2 = User(email='test2222@mail.ru',
                 password='password',
                 username='test2222')
    db.session.add(user1)
    db.session.add(user2)

    # Commit the changes for the users
    db.session.commit()

    yield  # this is where the testing happens!


@pytest.fixture(scope='function')
def login_default_user(test_client):
    test_client.post('/login',
                     data=dict(email='test111@mail.ru', password='password'),
                     follow_redirects=True)

    yield  # this is where the testing happens!

    test_client.get('/logout', follow_redirects=True)
