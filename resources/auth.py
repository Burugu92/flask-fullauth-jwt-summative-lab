from flask import Blueprint, request, jsonify
from server.models import User
from server.extensions import db
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity
)

auth_bp = Blueprint("auth", __name__)


# Signup route

@auth_bp.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()

    username = data.get("username")
    password = data.get("password")

    # Validation
    if not username or not password:
        return {"error": "Username and password required"}, 400

    # Check if user exists
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return {"error": "Username already exists"}, 409

    # Create user
    user = User(username=username)
    user.set_password(password)

    db.session.add(user)
    db.session.commit()

    return {
        "message": "User created successfully",
        "user": {
            "id": user.id,
            "username": user.username
        }
    }, 201


# Login route

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    username = data.get("username")
    password = data.get("password")

    # Validation
    if not username or not password:
        return {"error": "Username and password required"}, 400

    # Find user
    user = User.query.filter_by(username=username).first()

    # Check credentials
    if not user or not user.check_password(password):
        return {"error": "Invalid credentials"}, 401

    # Create JWT token
    access_token = create_access_token(identity=user.id)

    return {
        "access_token": access_token,
        "user": {
            "id": user.id,
            "username": user.username
        }
    }, 200


# Current user route (requires authentication)

@auth_bp.route("/me", methods=["GET"])
@jwt_required()
def me():
    user_id = get_jwt_identity()

    user = User.query.get(user_id)

    if not user:
        return {"error": "User not found"}, 404

    return {
        "id": user.id,
        "username": user.username
    }, 200