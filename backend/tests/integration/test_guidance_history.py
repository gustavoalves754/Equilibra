"""Testes de integração do histórico de orientações."""

import pytest

pytestmark = pytest.mark.integration


def _register_and_login(client, username: str) -> dict[str, str]:
    password = "123456"
    client.post(
        "/api/v1/auth/register",
        json={"username": username, "password": password},
    )
    response = client.post(
        "/api/v1/auth/login",
        json={"username": username, "password": password},
    )
    return {"Authorization": f"Bearer {response.get_json()['token']}"}


def test_fact_historico_exige_token(client):
    response = client.get("/api/v1/guidance/history")
    assert response.status_code == 401


def test_fact_historico_vazio_retorna_lista_vazia(client, auth_headers):
    response = client.get("/api/v1/guidance/history", headers=auth_headers)
    assert response.status_code == 200
    assert response.get_json() == []


def test_fact_historico_lista_orientacoes_mais_recentes_primeiro(
    client, auth_headers, valid_profile, monkeypatch
):
    client.put("/api/v1/profile", headers=auth_headers, json=valid_profile)

    responses = iter(["Primeira orientação", "Segunda orientação"])
    monkeypatch.setattr(
        "app.routes.generate_wellbeing_guidance",
        lambda profile, api_key, model: next(responses),
    )

    client.post("/api/v1/guidance", headers=auth_headers)
    client.post("/api/v1/guidance", headers=auth_headers)

    response = client.get("/api/v1/guidance/history", headers=auth_headers)
    history = response.get_json()

    assert response.status_code == 200
    assert len(history) == 2
    assert history[0]["response_text"] == "Segunda orientação"
    assert history[1]["response_text"] == "Primeira orientação"


def test_fact_historico_preserva_snapshot_do_perfil(
    client, auth_headers, valid_profile, monkeypatch
):
    monkeypatch.setattr(
        "app.routes.generate_wellbeing_guidance",
        lambda profile, api_key, model: "Orientação antiga",
    )

    client.put("/api/v1/profile", headers=auth_headers, json=valid_profile)
    client.post("/api/v1/guidance", headers=auth_headers)

    updated_profile = dict(valid_profile)
    updated_profile["weight_kg"] = valid_profile["weight_kg"] + 5
    updated_profile["goal"] = "novo objetivo"
    client.put("/api/v1/profile", headers=auth_headers, json=updated_profile)

    history = client.get(
        "/api/v1/guidance/history", headers=auth_headers
    ).get_json()

    assert history[0]["weight_kg"] == valid_profile["weight_kg"]
    assert history[0]["goal"] == valid_profile["goal"]


def test_fact_historico_e_isolado_por_usuario(client, valid_profile, monkeypatch):
    headers_a = _register_and_login(client, "usuario_a")
    headers_b = _register_and_login(client, "usuario_b")

    monkeypatch.setattr(
        "app.routes.generate_wellbeing_guidance",
        lambda profile, api_key, model: "Orientação do usuário A",
    )

    client.put("/api/v1/profile", headers=headers_a, json=valid_profile)
    client.post("/api/v1/guidance", headers=headers_a)

    history_a = client.get(
        "/api/v1/guidance/history", headers=headers_a
    ).get_json()
    history_b = client.get(
        "/api/v1/guidance/history", headers=headers_b
    ).get_json()

    assert len(history_a) == 1
    assert history_a[0]["response_text"] == "Orientação do usuário A"
    assert history_b == []
