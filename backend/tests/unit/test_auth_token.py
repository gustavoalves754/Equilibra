"""Testes unitários da criação de JWT."""

import jwt
import pytest

from app.auth import create_token

pytestmark = pytest.mark.unit


def test_fact_create_token_contem_id_do_usuario(app):
    # Arrange
    user_id = 7

    # Act
    with app.app_context():
        token = create_token(user_id)
        payload = jwt.decode(
            token,
            app.config["JWT_SECRET"],
            algorithms=["HS256"],
        )

    # Assert
    assert payload["sub"] == "7"
    assert "iat" in payload
    assert "exp" in payload
