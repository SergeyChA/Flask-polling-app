import pytest

from pollingsite import db
from pollingsite.models import User
from pathlib import Path

resources = Path(__file__).parent / "resources"


def test_login_and_logout(test_client, init_database):
    response = test_client.post(
        '/login',
        data={
            'email': 'test@mail.ru',
            'password': 'password',
        },
        follow_redirects=True
    )
    assert response.status_code == 200
    assert 'test@mail.ru' in response.text


def test_account_changes(test_client, init_database):
    response = test_client.post(
        '/account/',
        data={
            'email': 'newtest@mail.ru',
            'username': 'newusername',
            'picture': (resources / 'profile.png').open('rb'),
        },
        follow_redirects=True
    )
    assert response.status_code == 200
    assert 'Ваши данные обновлены' in response.text
    assert 'newtest@mail.ru' in response.text
    assert 'newusername' in response.text
    user = db.session.execute(
        db.select(User).filter(User.username == 'newusername')
    ).scalar()
    assert user.username == 'newusername'
    assert user.email == 'newtest@mail.ru'


@pytest.mark.parametrize((
    'email',
    'username',
    'picture',
    'message'
    ), (
        ('example@mail.ru', 'user', '', 'Такое имя уже занято'),
        ('example1@mail.ru', 'te', '', 'Имя должно быть от 3 до 30 символов'),
        ('testmail.ru', 'example', '', 'Неверная почта'),
        ('user@mail.ru', 'example', '', 'Такая почта уже занята'),
        ('', 'example', '', 'Введите почту'),
        ('example1@mail.ru', '', '', 'Введите имя'),
        ('example1@mail.ru', 'example', (resources / 'test.gif').open('rb'), 'Формат изображения только jpg, png'),
    )
)
def test_account_changes_input(
    test_client,
    init_database,
    email,
    username,
    picture,
    message
):
    response = test_client.post(
        '/account/',
        data={
            'email': email,
            'username': username,
            'picture': picture,
        },
        follow_redirects=True
    )
    assert response.status_code == 200
    assert message in response.text
