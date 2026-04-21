def test_create_expense(client, auth_token):
    res = client.post("/expenses", json={
        "title": "Lunch",
        "amount": 20,
        "category": "Food"
    }, headers={"Authorization": f"Bearer {auth_token}"})

    assert res.status_code == 201


def test_get_expenses_requires_auth(client):
    res = client.get("/expenses")
    assert res.status_code == 401


def test_create_expense_missing_fields(client, auth_token):
    res = client.post("/expenses", json={}, headers={
        "Authorization": f"Bearer {auth_token}"
    })

    assert res.status_code == 400


def test_get_expenses_pagination(client, auth_token):
    res = client.get("/expenses?page=1&per_page=2", headers={
        "Authorization": f"Bearer {auth_token}"
    })

    data = res.get_json()

    assert "expenses" in data
    assert "page" in data
    assert "pages" in data


def test_update_expense(client, auth_token):
    create = client.post("/expenses", json={
        "title": "Dinner",
        "amount": 50
    }, headers={"Authorization": f"Bearer {auth_token}"})

    expense_id = create.get_json()["expense"]["id"]

    res = client.patch(f"/expenses/{expense_id}", json={
        "amount": 100
    }, headers={"Authorization": f"Bearer {auth_token}"})

    assert res.status_code == 200


def test_delete_expense(client, auth_token):
    create = client.post("/expenses", json={
        "title": "Snack",
        "amount": 10
    }, headers={"Authorization": f"Bearer {auth_token}"})

    expense_id = create.get_json()["expense"]["id"]

    res = client.delete(f"/expenses/{expense_id}", headers={
        "Authorization": f"Bearer {auth_token}"
    })

    assert res.status_code == 200


def test_update_nonexistent_expense(client, auth_token):
    res = client.patch("/expenses/9999", json={
        "amount": 999
    }, headers={"Authorization": f"Bearer {auth_token}"})

    assert res.status_code in [403, 404]


def test_delete_nonexistent_expense(client, auth_token):
    res = client.delete("/expenses/9999", headers={
        "Authorization": f"Bearer {auth_token}"
    })

    assert res.status_code in [403, 404]


def test_ownership_enforcement(client):
    # user A
    client.post("/signup", json={"username": "a", "password": "a"})
    token_a = client.post("/login", json={
        "username": "a", "password": "a"
    }).get_json()["access_token"]

    # create expense
    res = client.post("/expenses", json={
        "title": "Secret",
        "amount": 100
    }, headers={"Authorization": f"Bearer {token_a}"})

    expense_id = res.get_json()["expense"]["id"]

    # user B
    client.post("/signup", json={"username": "b", "password": "b"})
    token_b = client.post("/login", json={
        "username": "b", "password": "b"
    }).get_json()["access_token"]

    # attempt unauthorized access
    res = client.patch(f"/expenses/{expense_id}", json={
        "amount": 999
    }, headers={"Authorization": f"Bearer {token_b}"})

    assert res.status_code in [403, 404]


def test_invalid_token(client):
    res = client.get("/expenses", headers={
        "Authorization": "Bearer invalidtoken"
    })

    assert res.status_code in [401, 422]