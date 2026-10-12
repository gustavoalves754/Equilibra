"""Fixtures compartilhadas pelos testes até a Issue 3."""

import pytest

from app import create_app


@pytest.fixture()
def app(tmp_path):
    """Cria a aplicação usando dois bancos SQLite temporários."""
    application = create_app(
        {
            "TESTING": True,
            "AUTH_DB_PATH": str(tmp_path / "users.db"),
            "APP_DB_PATH": str(tmp_path / "equilibra.db"),
            "JWT_SECRET": "equilibra-segredo-exclusivo-testes-32-caracteres",
            "TOKEN_EXP_HOURS": 1,
        }
    )
    yield application


@pytest.fixture()
def client(app):
    """Cliente HTTP de teste do Flask."""
    return app.test_client()


@pytest.fixture()
def register_and_login(client):
    """Cria e autentica um usuário e retorna seu JWT."""

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
    """Perfil válido reutilizado nos testes de integração."""
    return {
        "age": 30,
        "height_m": 1.80,
        "weight_kg": 82.5,
        "goal": "melhorar a alimentação e perder peso gradualmente",
    }
