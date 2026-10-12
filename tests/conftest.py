"""Fixtures compartilhadas pelos testes unitários e de integração."""

import pytest

from app import create_app


@pytest.fixture()
def app(tmp_path):
    """Cria a aplicação apontando para dois bancos SQLite temporários."""
    return create_app(
        {
            "TESTING": True,
            "AUTH_DB_PATH": str(tmp_path / "users_test.db"),
            "APP_DB_PATH": str(tmp_path / "equilibra_test.db"),
            "JWT_SECRET": "segredo-exclusivo-de-teste",
            "TOKEN_EXP_HOURS": 1,
            "GEMINI_API_KEY": "fake-key",
            "GEMINI_MODEL": "modelo-teste",
        }
    )


@pytest.fixture()
def client(app):
    """Cliente HTTP do Flask para testes de integração."""
    return app.test_client()


@pytest.fixture()
def register_and_login(client):
    """Cria e autentica um usuário, retornando o JWT."""

    def _register_and_login(username="aluno", password="senha123"):
        register_response = client.post(
            "/api/v1/auth/register",
            json={"username": username, "password": password},
        )
        assert register_response.status_code == 201

        login_response = client.post(
            "/api/v1/auth/login",
            json={"username": username, "password": password},
        )
        assert login_response.status_code == 200
        return login_response.get_json()["token"]

    return _register_and_login


@pytest.fixture()
def token(register_and_login):
    """JWT válido de um usuário padrão."""
    return register_and_login()


@pytest.fixture()
def auth_headers(token):
    """Cabeçalho Authorization pronto para rotas protegidas."""
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture()
def valid_profile():
    """Perfil funcional válido usado em vários cenários."""
    return {
        "age": 30,
        "height_m": 1.80,
        "weight_kg": 82.5,
        "goal": "melhorar a alimentação e perder peso gradualmente",
    }
