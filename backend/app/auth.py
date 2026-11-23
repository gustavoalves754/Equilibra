"""Criação e validação de tokens JWT do Equilibra."""

from datetime import datetime, timedelta, timezone
from functools import wraps

import jwt
from flask import current_app, g, jsonify, request


def create_token(user_id: int) -> str:
    """Cria um JWT temporário para o usuário autenticado."""
    now = datetime.now(timezone.utc)
    expires = now + timedelta(hours=current_app.config["TOKEN_EXP_HOURS"])

    payload = {
        "sub": str(user_id),
        "iat": now,
        "exp": expires,
    }

    return jwt.encode(
        payload,
        current_app.config["JWT_SECRET"],
        algorithm="HS256",
    )


def token_required(view_function):
    """Protege uma rota exigindo Authorization: Bearer <token>."""

    @wraps(view_function)
    def wrapper(*args, **kwargs):
        authorization = request.headers.get("Authorization", "")

        if not authorization.startswith("Bearer "):
            return jsonify({"error": "Token de acesso não informado."}), 401

        token = authorization.removeprefix("Bearer ").strip()
        if not token:
            return jsonify({"error": "Token de acesso não informado."}), 401

        try:
            payload = jwt.decode(
                token,
                current_app.config["JWT_SECRET"],
                algorithms=["HS256"],
            )
            g.user_id = int(payload["sub"])
        except (jwt.InvalidTokenError, KeyError, TypeError, ValueError):
            return jsonify({"error": "Token inválido ou expirado."}), 401

        return view_function(*args, **kwargs)

    return wrapper
