from flask import Blueprint, request
from server.models import User
from server.extensions import db
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity,
    verify_jwt_in_request,
    exceptions
)

auth_bp = Blueprint("auth", __name__)


# SIGNUP

@auth_bp.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()

    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return {"errors": ["Username and password required"]}, 400

    if User.query.filter_by(username=username).first():
        return {"errors": ["Username already exists"]}, 409

    user = User(username=username)
    user.set_password(password)

    db.session.add(user)
    db.session.commit()

    token = create_access_token(identity=user.id)

    return {
        "token": token,
        "user": {
            "id": user.id,
            "username": user.username
        }
    }, 201


# LOGIN

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return {"errors": ["Username and password required"]}, 400

    user = User.query.filter_by(username=username).first()

    if not user or not user.check_password(password):
        return {"errors": ["Invalid credentials"]}, 401

    token = create_access_token(identity=user.id)

    return {
        "token": token,
        "user": {
            "id": user.id,
            "username": user.username
        }
    }, 200


# ME - Get current user info based on JWT token (if valid)

@auth_bp.route("/me", methods=["GET"])
def me():
    try:
        verify_jwt_in_request()
        user_id = get_jwt_identity()
    except exceptions.NoAuthorizationError:
        return {}, 200
    except Exception:
        return {}, 200

    user = User.query.get(user_id)

    if not user:
        return {}, 200

    return {
        "id": user.id,
        "username": user.username
    }, 200