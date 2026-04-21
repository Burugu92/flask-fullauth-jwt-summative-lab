import pytest
import sys
import os

# allow imports from server
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from server.app import create_app
from server.extensions import db


@pytest.fixture
def app():
    app = create_app()

    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["JWT_SECRET_KEY"] = "test-secret"

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def auth_token(client):
    client.post("/signup", json={
        "username": "testuser",
        "password": "testpass"
    })

    res = client.post("/login", json={
        "username": "testuser",
        "password": "testpass"
    })

    return res.get_json()["access_token"]