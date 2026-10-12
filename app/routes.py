"""Rotas HTTP disponíveis até a Issue 2 do Equilibra."""

from datetime import datetime, timezone
import sqlite3

from flask import Blueprint, g, jsonify, request
from werkzeug.security import check_password_hash, generate_password_hash

from .auth import create_token, token_required
from .database import get_auth_db
from .validators import validate_credentials

api = Blueprint("api", __name__)


def _now() -> str:
    """Retorna data e hora UTC no formato ISO 8601."""
    return datetime.now(timezone.utc).isoformat()


@api.get("/")
def index():
    """Retorna a identificação da API."""
    return jsonify({"name": "Equilibra API", "version": "1.0"}), 200


@api.get("/health")
def health():
    """Confirma que a API está disponível."""
    return jsonify({"status": "ok"}), 200


@api.post("/auth/register")
def register():
    """Cadastra um usuário no users.db com senha armazenada como hash."""
    data = request.get_json(silent=True) or {}

    try:
        username, password = validate_credentials(data)
    except ValueError as error:
        return jsonify({"error": str(error)}), 400

    try:
        with get_auth_db() as db:
            cursor = db.execute(
                """
                INSERT INTO users (username, password_hash, created_at)
                VALUES (?, ?, ?)
                """,
                (username, generate_password_hash(password), _now()),
            )
            user_id = cursor.lastrowid
    except sqlite3.IntegrityError:
        return jsonify({"error": "Este usuário já existe."}), 409

    return jsonify({"id": user_id, "username": username}), 201


@api.post("/auth/login")
def login():
    """Valida usuário e senha e devolve um token JWT."""
    data = request.get_json(silent=True) or {}

    try:
        username, password = validate_credentials(data)
    except ValueError as error:
        return jsonify({"error": str(error)}), 400

    with get_auth_db() as db:
        user = db.execute(
            """
            SELECT id, username, password_hash
            FROM users
            WHERE username = ?
            """,
            (username,),
        ).fetchone()

    if user is None or not check_password_hash(user["password_hash"], password):
        return jsonify({"error": "Usuário ou senha inválidos."}), 401

    return jsonify(
        {
            "token": create_token(user["id"]),
            "token_type": "Bearer",
            "user": {
                "id": user["id"],
                "username": user["username"],
            },
        }
    ), 200


@api.get("/me")
@token_required
def me():
    """Retorna os dados básicos do usuário autenticado."""
    with get_auth_db() as db:
        user = db.execute(
            """
            SELECT id, username, created_at
            FROM users
            WHERE id = ?
            """,
            (g.user_id,),
        ).fetchone()

    if user is None:
        return jsonify({"error": "Usuário não encontrado."}), 404

    return jsonify(dict(user)), 200
