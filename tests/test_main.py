from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_root_deve_retornar_200():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"mensagem": "A API do Equilibra está online."}

def test_health_check_deve_retornar_ok():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "servico": "equilibra-api"}