

def test_login_already_logged_in(test_client):
    response = test_client.post('/login',
                                data={
                                    'email': 'test1111@mail.ru',
                                    'password': 'password'},
                                follow_redirects=True)
    assert response.status_code == 200


def test_valid_registration(test_client, init_database):
    response = test_client.post('/singup',
                                data=dict(
                                    email='test333@mail.ru',
                                    username='test333',
                                    password='password',
                                    confirm_password='password'),
                                follow_redirects=True)
    assert response.status_code == 200
