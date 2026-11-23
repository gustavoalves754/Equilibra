"""Testes de integração da criação, consulta e atualização do perfil."""

import pytest

from tests.data_providers import ProfileInvalidClassData

pytestmark = pytest.mark.integration


def test_fact_criar_e_consultar_perfil(client, auth_headers, valid_profile):
    # Arrange: usuário já autenticado pelas fixtures.
    # Act
    save_response = client.put(
        "/api/v1/profile",
        headers=auth_headers,
        json=valid_profile,
    )
    get_response = client.get("/api/v1/profile", headers=auth_headers)

    # Assert
    assert save_response.status_code == 200
    assert get_response.status_code == 200
    assert get_response.get_json()["age"] == valid_profile["age"]
    assert get_response.get_json()["goal"] == valid_profile["goal"]


def test_fact_atualizar_perfil_substitui_dados_anteriores(
    client, auth_headers, valid_profile
):
    client.put("/api/v1/profile", headers=auth_headers, json=valid_profile)
    updated = {
        "age": 31,
        "height_m": 1.80,
        "weight_kg": 79.2,
        "goal": "manter hábitos saudáveis",
    }

    update_response = client.put(
        "/api/v1/profile",
        headers=auth_headers,
        json=updated,
    )
    get_response = client.get("/api/v1/profile", headers=auth_headers)

    assert update_response.status_code == 200
    assert get_response.get_json()["age"] == 31
    assert get_response.get_json()["weight_kg"] == 79.2
    assert get_response.get_json()["goal"] == "manter hábitos saudáveis"


def test_fact_consultar_perfil_inexistente_retorna_404(client, auth_headers):
    response = client.get("/api/v1/profile", headers=auth_headers)

    assert response.status_code == 404


def test_fact_salvar_perfil_sem_token_retorna_401(client, valid_profile):
    response = client.put("/api/v1/profile", json=valid_profile)

    assert response.status_code == 401


def test_fact_json_invalido_no_perfil_retorna_400(client, auth_headers):
    response = client.put(
        "/api/v1/profile",
        headers=auth_headers,
        data="{invalido",
        content_type="application/json",
    )

    assert response.status_code == 400


@pytest.mark.parametrize("payload,_expected_message", ProfileInvalidClassData())
def test_class_data_endpoint_rejeita_perfis_invalidos(
    client,
    auth_headers,
    payload,
    _expected_message,
):
    response = client.put(
        "/api/v1/profile",
        headers=auth_headers,
        json=payload,
    )

    assert response.status_code == 400


def test_fact_perfil_de_um_usuario_nao_aparece_para_outro(
    client,
    register_and_login,
    valid_profile,
):
    token_a = register_and_login("usuario_a", "senha123")
    token_b = register_and_login("usuario_b", "senha123")

    client.put(
        "/api/v1/profile",
        headers={"Authorization": f"Bearer {token_a}"},
        json=valid_profile,
    )

    response_b = client.get(
        "/api/v1/profile",
        headers={"Authorization": f"Bearer {token_b}"},
    )

    assert response_b.status_code == 404
