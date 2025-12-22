from flask import Blueprint, request, jsonify
from sqlalchemy.exc import IntegrityError
from db import SessionLocal
from repositories.user_repository import UserRepository
from services.auth_service import AuthService
from schemas.auth import SignupRequest, LoginRequest
from pydantic import ValidationError

auth_bp = Blueprint("auth", __name__)
auth_service = AuthService()

def _json_error(message, status=400):
    return jsonify({"message": message}), status

@auth_bp.route("/api/register", methods=["POST"])
def register():
    data = request.get_json(silent=True) or {}
    try:
        payload = SignupRequest(**data)
    except ValidationError as e:
        return jsonify({"message": "Invalid data", "errors": e.errors()}), 400
    session = SessionLocal()
    repo = UserRepository(session)
    try:
        if repo.get_by_username(payload.username):
            return _json_error("Username already exists")
        if repo.get_by_email(payload.email):
            return _json_error("Email already exists")
        user = repo.create_user(payload.username, payload.email, auth_service.hash_password(payload.password))
        token = auth_service.create_token({"sub": str(user.id)})
        return jsonify({"token": token, "user": {"id": user.id, "username": user.username}}), 201
    except IntegrityError:
        session.rollback()
        return _json_error("User already exists")
    finally:
        session.close()

@auth_bp.route("/api/login", methods=["POST"])
def login():
    data = request.get_json(silent=True) or {}
    try:
        payload = LoginRequest(**data)
    except ValidationError as e:
        return jsonify({"message": "Invalid data", "errors": e.errors()}), 400
    session = SessionLocal()
    repo = UserRepository(session)
    try:
        user = repo.get_by_username(payload.username)
        if not user:
            return _json_error("Invalid credentials", 401)
        if not auth_service.verify_password(payload.password, user.password_hash):
            return _json_error("Invalid credentials", 401)
        token = auth_service.create_token({"sub": str(user.id)})
        return jsonify({"token": token, "user": {"id": user.id, "username": user.username}})
    finally:
        session.close()

