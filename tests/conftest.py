"""Fixtures compartilhadas pelos testes da Issue 2."""

import pytest

from app import create_app


@pytest.fixture()
def app(tmp_path):
    """Cria a aplicação apontando para um users.db temporário."""
    application = create_app(
        {
            "TESTING": True,
            "AUTH_DB_PATH": str(tmp_path / "users.db"),
            "JWT_SECRET": "equilibra-chave-jwt-apenas-para-testes-123456789",
            "TOKEN_EXP_HOURS": 1,
        }
    )
    yield application


@pytest.fixture()
def client(app):
    """Cliente HTTP de teste do Flask."""
    return app.test_client()


@pytest.fixture()
def token(client):
    """Cria um usuário de teste e devolve seu JWT."""
    client.post(
        "/api/v1/auth/register",
        json={"username": "aluno", "password": "senha123"},
    )
    response = client.post(
        "/api/v1/auth/login",
        json={"username": "aluno", "password": "senha123"},
    )
    return response.get_json()["token"]
