"""Testes de integração de cadastro, login, hash de senha e JWT."""

from datetime import datetime, timedelta, timezone

import jwt
import pytest
from werkzeug.security import check_password_hash

from app.database import get_auth_db
from tests.data_providers import CredentialMemberData

pytestmark = pytest.mark.integration


def test_fact_cadastro_salva_hash_e_nao_senha_em_texto_puro(app, client):
    # Arrange
    password = "senha123"

    # Act
    response = client.post(
        "/api/v1/auth/register",
        json={"username": "gustavo", "password": password},
    )

    # Assert
    assert response.status_code == 201
    assert "password" not in response.get_json()

    with app.app_context():
        with get_auth_db() as db:
            row = db.execute(
                "SELECT password_hash FROM users WHERE username = ?",
                ("gustavo",),
            ).fetchone()

    assert row["password_hash"] != password
    assert check_password_hash(row["password_hash"], password)


def test_fact_login_valido_retorna_jwt(client):
    # Arrange
    client.post(
        "/api/v1/auth/register",
        json={"username": "gustavo", "password": "senha123"},
    )

    # Act
    response = client.post(
        "/api/v1/auth/login",
        json={"username": "gustavo", "password": "senha123"},
    )

    # Assert
    body = response.get_json()
    assert response.status_code == 200
    assert body["token_type"] == "Bearer"
    assert isinstance(body["token"], str)
    assert body["user"]["username"] == "gustavo"


def test_fact_login_com_senha_errada_retorna_401(client):
    client.post(
        "/api/v1/auth/register",
        json={"username": "gustavo", "password": "senha123"},
    )

    response = client.post(
        "/api/v1/auth/login",
        json={"username": "gustavo", "password": "senha999"},
    )

    assert response.status_code == 401
    assert response.get_json()["error"] == "Usuário ou senha inválidos."


def test_fact_usuario_duplicado_retorna_409(client):
    payload = {"username": "gustavo", "password": "senha123"}
    client.post("/api/v1/auth/register", json=payload)

    response = client.post("/api/v1/auth/register", json=payload)

    assert response.status_code == 409


def test_fact_login_de_usuario_inexistente_retorna_401(client):
    response = client.post(
        "/api/v1/auth/login",
        json={"username": "inexistente", "password": "senha123"},
    )

    assert response.status_code == 401


def test_fact_cadastro_normaliza_username_para_minusculo(client):
    response = client.post(
        "/api/v1/auth/register",
        json={"username": "  Gustavo  ", "password": "senha123"},
    )

    assert response.status_code == 201
    assert response.get_json()["username"] == "gustavo"


@pytest.mark.parametrize(
    "payload,_expected_message",
    CredentialMemberData.INVALID_CASES,
)
def test_member_data_cadastro_rejeita_credenciais_invalidas(
    client,
    payload,
    _expected_message,
):
    response = client.post("/api/v1/auth/register", json=payload)

    assert response.status_code == 400


def test_fact_rota_protegida_sem_token_retorna_401(client):
    response = client.get("/api/v1/me")

    assert response.status_code == 401
    assert response.get_json()["error"] == "Token de acesso não informado."


def test_fact_rota_protegida_com_token_invalido_retorna_401(client):
    response = client.get(
        "/api/v1/me",
        headers={"Authorization": "Bearer token-invalido"},
    )

    assert response.status_code == 401


def test_fact_rota_protegida_com_token_expirado_retorna_401(app, client):
    expired_token = jwt.encode(
        {
            "sub": "1",
            "exp": datetime.now(timezone.utc) - timedelta(seconds=1),
        },
        app.config["JWT_SECRET"],
        algorithm="HS256",
    )

    response = client.get(
        "/api/v1/me",
        headers={"Authorization": f"Bearer {expired_token}"},
    )

    assert response.status_code == 401


def test_fact_me_retorna_usuario_autenticado(client, token):
    response = client.get(
        "/api/v1/me",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    assert response.get_json()["username"] == "aluno"

def test_fact_rota_protegida_com_token_vazio_retorna_401(client):
    # Arrange / Act
    response = client.get(
        "/api/v1/me",
        headers={"Authorization": "Bearer "},
    )
 
    # Assert
    assert response.status_code == 401
    assert response.get_json()["error"] == "Token de acesso não informado."
 
 
def test_fact_rota_protegida_com_subject_invalido_retorna_401(app, client):
    # Arrange
    invalid_token = jwt.encode(
        {
            "sub": "usuario-invalido",
            "exp": datetime.now(timezone.utc) + timedelta(hours=1),
        },
        app.config["JWT_SECRET"],
        algorithm="HS256",
    )
 
    # Act
    response = client.get(
        "/api/v1/me",
        headers={"Authorization": f"Bearer {invalid_token}"},
    )
 
    # Assert
    assert response.status_code == 401
    assert response.get_json()["error"] == "Token inválido ou expirado."