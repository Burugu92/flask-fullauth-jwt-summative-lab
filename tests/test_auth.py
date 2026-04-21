# test sign up, login, and /me endpoints

def test_signup_success(client):
    res = client.post("/signup", json={
        "username": "user1",
        "password": "pass123"
    })
    assert res.status_code == 201


def test_signup_duplicate(client):
    client.post("/signup", json={
        "username": "dup",
        "password": "pass"
    })

    res = client.post("/signup", json={
        "username": "dup",
        "password": "pass"
    })

    assert res.status_code in [400, 409]


def test_signup_missing_fields(client):
    res = client.post("/signup", json={
        "username": ""
    })
    assert res.status_code == 400


def test_login_success(client):
    client.post("/signup", json={
        "username": "loginuser",
        "password": "pass123"
    })

    res = client.post("/login", json={
        "username": "loginuser",
        "password": "pass123"
    })

    assert res.status_code == 200
    assert "access_token" in res.get_json()


def test_login_invalid(client):
    res = client.post("/login", json={
        "username": "wrong",
        "password": "wrong"
    })

    assert res.status_code == 401


def test_me_requires_token(client):
    res = client.get("/me")
    assert res.status_code == 401