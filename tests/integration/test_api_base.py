"""Testes de integração da estrutura base Flask."""

import pytest

from app import create_app

pytestmark = pytest.mark.integration


def test_fact_index_retorna_identificacao_da_api(client):
    # Arrange: client criado pela fixture.
    # Act
    response = client.get("/api/v1/")
    # Assert
    assert response.status_code == 200
    assert response.get_json() == {"name": "Equilibra API", "version": "1.0"}


def test_fact_health_retorna_ok(client):
    response = client.get("/api/v1/health")

    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}


def test_fact_rota_inexistente_retorna_404(client):
    response = client.get("/api/v1/nao-existe")

    assert response.status_code == 404


def test_fact_application_factory_aceita_configuracao_de_teste():
    # Arrange
    test_config = {
        "TESTING": True,
        "TEST_MARKER": "issue-01",
    }
 
    # Act
    app = create_app(test_config)
 
    # Assert
    assert app.config["TESTING"] is True
    assert app.config["TEST_MARKER"] == "issue-01"