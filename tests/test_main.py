

def test_main(test_client):
    response = test_client.get("/")
    assert response.status_code == 200
    test_client.get("/").data == response.data


def test_login(test_client):
    response = test_client.get("/login")
    assert response.status_code == 200


def test_singup(test_client):
    response = test_client.get("/singup")
    assert response.status_code == 200


def test_account(test_client):
    response = test_client.get("/account/")
    assert response.status_code == 401
