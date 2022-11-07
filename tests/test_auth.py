import pytest
from flask import session
from pollingsite import db
from pollingsite.models import User


def test_login_and_logout(test_client, init_database):
    response = test_client.post(
        '/login',
        data={
            'email': 'test@mail.ru',
            'password': 'password',
        },
    )
    assert response.headers["Location"] == "/account/"
    assert session['_user_id'] == '1'
    response = test_client.get('/logout')
    assert '_user_id' not in session


@pytest.mark.parametrize((
    'email',
    'password',
    'message'
    ), (
        ('example@mail.ru', 'password', 'Ошибка. Неверный пароль или почта'),
        ('testmail.ru', 'example', 'Неверная почта'),
        ('test@mail.ru', 'ex', 'Пароль должен быть не менее 6 символов'),
        ('', 'password', 'Введите почту'),
        ('example1@mail.ru', '', 'Введите пароль'),
    )
)
def test_login_input(test_client, init_database, email, password, message):
    response = test_client.post(
        '/login',
        data={'email': email, 'password': password},
    )
    assert response.status_code == 200
    assert message in response.text


def test_registration(test_client, init_database):
    response = test_client.post(
        '/singup',
        data={
            'email': 'test1@mail.ru',
            'username': 'example',
            'password': 'password',
            'confirm_password': 'password',
        },
        follow_redirects=True
    )
    assert response.status_code == 200
    assert 'Вы зарегистрированы!' in response.text
    user = db.session.execute(
        db.select(User).filter(User.username == 'example')
    ).scalar()
    assert str(user) == 'example'
    assert user.email == 'test1@mail.ru'


@pytest.mark.parametrize((
    'email',
    'username',
    'password',
    'confirm_password',
    'message'
    ), (
        ('test@mail.ru', 'example', 'password', 'password', 'Такая почта уже занята'),
        ('example@mail.ru', 'test', 'password', 'password', 'Такое имя уже занято'),
        ('test.ru', 'example', 'password', 'password', 'Неверная почта'),
        ('example1@mail.ru', 'te', 'password', 'password', 'Имя должно быть от 3 до 30 символов'),
        ('example@mail.ru', 'test1', 'pass', 'password', 'Пароль должен быть не менее 6 символов'),
        ('example@mail.ru', 'test1', 'password', 'passw', 'Пароли не совпадают')
    )
)
def test_registration_input(
    test_client,
    init_database,
    email,
    username,
    password,
    confirm_password,
    message
):
    response = test_client.post(
        '/singup',
        data={
            'email': email,
            'username': username,
            'password': password,
            'confirm_password': confirm_password,
        },
    )
    assert response.status_code == 200
    assert message in response.text
