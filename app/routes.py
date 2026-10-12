"""Rotas HTTP disponíveis até a Issue 5 do Equilibra."""

from datetime import datetime, timezone
import sqlite3

from flask import Blueprint, current_app, g, jsonify, request
from werkzeug.security import check_password_hash, generate_password_hash

from .auth import create_token, token_required
from .database import get_app_db, get_auth_db
from .gemini_service import GeminiServiceError, generate_wellbeing_guidance
from .validators import validate_credentials, validate_profile

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


@api.put("/profile")
@token_required
def save_profile():
    """Cria ou atualiza idade, altura, peso e objetivo do usuário."""
    data = request.get_json(silent=True) or {}

    try:
        profile = validate_profile(data)
    except ValueError as error:
        return jsonify({"error": str(error)}), 400

    with get_app_db() as db:
        db.execute(
            """
            INSERT INTO profiles (user_id, age, height_m, weight_kg, goal, updated_at)
            VALUES (?, ?, ?, ?, ?, ?)
            ON CONFLICT(user_id) DO UPDATE SET
                age = excluded.age,
                height_m = excluded.height_m,
                weight_kg = excluded.weight_kg,
                goal = excluded.goal,
                updated_at = excluded.updated_at
            """,
            (
                g.user_id,
                profile["age"],
                profile["height_m"],
                profile["weight_kg"],
                profile["goal"],
                _now(),
            ),
        )

    return jsonify({"message": "Perfil salvo com sucesso.", "profile": profile}), 200


@api.get("/profile")
@token_required
def get_profile():
    """Consulta o perfil do usuário autenticado."""
    with get_app_db() as db:
        profile = db.execute(
            """
            SELECT age, height_m, weight_kg, goal, updated_at
            FROM profiles
            WHERE user_id = ?
            """,
            (g.user_id,),
        ).fetchone()

    if profile is None:
        return jsonify({"error": "Perfil ainda não cadastrado."}), 404

    return jsonify(dict(profile)), 200


@api.post("/guidance")
@token_required
def create_guidance():
    """Chama o Gemini e salva uma cópia da orientação no histórico."""
    with get_app_db() as db:
        row = db.execute(
            """
            SELECT age, height_m, weight_kg, goal
            FROM profiles
            WHERE user_id = ?
            """,
            (g.user_id,),
        ).fetchone()

    if row is None:
        return jsonify({"error": "Cadastre o perfil antes de gerar orientação."}), 400

    profile = dict(row)

    try:
        response_text = generate_wellbeing_guidance(
            profile,
            api_key=current_app.config["GEMINI_API_KEY"],
            model=current_app.config["GEMINI_MODEL"],
        )
    except GeminiServiceError:
        return jsonify({"error": "Não foi possível consultar o Gemini agora."}), 503

    with get_app_db() as db:
        cursor = db.execute(
            """
            INSERT INTO guidance_history (
                user_id, age, height_m, weight_kg, goal,
                response_text, model, created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                g.user_id,
                profile["age"],
                profile["height_m"],
                profile["weight_kg"],
                profile["goal"],
                response_text,
                current_app.config["GEMINI_MODEL"],
                _now(),
            ),
        )
        guidance_id = cursor.lastrowid

    return jsonify(
        {
            "id": guidance_id,
            "profile": profile,
            "guidance": response_text,
            "model": current_app.config["GEMINI_MODEL"],
        }
    ), 201


@api.get("/guidance/history")
@token_required
def guidance_history():
    """Lista somente as orientações geradas pelo usuário autenticado."""
    with get_app_db() as db:
        rows = db.execute(
            """
            SELECT id, age, height_m, weight_kg, goal,
                   response_text, model, created_at
            FROM guidance_history
            WHERE user_id = ?
            ORDER BY id DESC
            """,
            (g.user_id,),
        ).fetchall()

    return jsonify([dict(row) for row in rows]), 200
