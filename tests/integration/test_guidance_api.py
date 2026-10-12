"""Testes de integração da rota de orientação com Gemini simulado."""

import pytest

from app.database import get_app_db
from app.gemini_service import GeminiServiceError

pytestmark = pytest.mark.integration


def test_fact_guidance_exige_token(client):
    response = client.post("/api/v1/guidance")
    assert response.status_code == 401


def test_fact_guidance_exige_perfil(client, auth_headers):
    response = client.post("/api/v1/guidance", headers=auth_headers)
    assert response.status_code == 400
    assert "Cadastre o perfil" in response.get_json()["error"]


def test_fact_falha_do_gemini_retorna_503(
    client, auth_headers, valid_profile, monkeypatch
):
    client.put("/api/v1/profile", headers=auth_headers, json=valid_profile)

    def fake_failure(profile, api_key, model):
        raise GeminiServiceError("falha simulada")

    monkeypatch.setattr("app.routes.generate_wellbeing_guidance", fake_failure)
    response = client.post("/api/v1/guidance", headers=auth_headers)

    assert response.status_code == 503
    assert response.get_json()["error"] == "Não foi possível consultar o Gemini agora."


def test_fact_falha_do_gemini_nao_salva_historico(
    app, client, auth_headers, valid_profile, monkeypatch
):
    client.put("/api/v1/profile", headers=auth_headers, json=valid_profile)

    def fake_failure(profile, api_key, model):
        raise GeminiServiceError("falha simulada")

    monkeypatch.setattr("app.routes.generate_wellbeing_guidance", fake_failure)
    client.post("/api/v1/guidance", headers=auth_headers)

    with app.app_context():
        with get_app_db() as db:
            total = db.execute("SELECT COUNT(*) FROM guidance_history").fetchone()[0]

    assert total == 0


def test_fact_guidance_sucesso_salva_e_devolve_id(
    client, auth_headers, valid_profile, monkeypatch
):
    client.put("/api/v1/profile", headers=auth_headers, json=valid_profile)
    monkeypatch.setattr(
        "app.routes.generate_wellbeing_guidance",
        lambda profile, api_key, model: "Resposta simulada do Gemini.",
    )

    response = client.post("/api/v1/guidance", headers=auth_headers)

    assert response.status_code == 201
    body = response.get_json()
    assert body["id"] > 0
    assert body["guidance"] == "Resposta simulada do Gemini."
    assert body["model"] == "modelo-teste"
    assert body["profile"]["goal"] == valid_profile["goal"]
