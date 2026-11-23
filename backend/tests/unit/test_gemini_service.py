"""Testes unitários da integração Gemini sem chamadas de rede."""

from types import SimpleNamespace

import pytest

from app.gemini_service import GeminiServiceError, generate_wellbeing_guidance

pytestmark = pytest.mark.unit


@pytest.fixture()
def profile():
    return {"age": 30, "height_m": 1.75, "weight_kg": 70, "goal": "bem-estar"}


def test_fact_chamada_valida_retorna_texto_limpo(profile, monkeypatch):
    captured = {}

    class FakeModels:
        def generate_content(self, *, model, contents):
            captured["model"] = model
            captured["contents"] = contents
            return SimpleNamespace(text="  orientação simulada  ")

    class FakeClient:
        def __init__(self, api_key):
            captured["api_key"] = api_key
            self.models = FakeModels()

    monkeypatch.setattr("app.gemini_service.genai.Client", FakeClient)

    result = generate_wellbeing_guidance(
        profile, api_key="fake", models=("modelo-x",)
    )

    assert result.text == "orientação simulada"
    assert result.model == "modelo-x"
    assert captured["api_key"] == "fake"
    assert captured["model"] == "modelo-x"
    assert "Objetivo: bem-estar" in captured["contents"]


@pytest.mark.parametrize(
    "api_key,models,expected",
    [
        ("", ("modelo-x",), "GEMINI_API_KEY não configurada"),
        ("fake", (), "Nenhum modelo Gemini foi configurado"),
    ],
)
def test_inline_data_configuracao_obrigatoria(profile, api_key, models, expected):
    with pytest.raises(GeminiServiceError, match=expected):
        generate_wellbeing_guidance(profile, api_key=api_key, models=models)


def test_fact_excecao_do_sdk_vira_erro_controlado(profile, monkeypatch):
    class BrokenClient:
        def __init__(self, api_key):
            raise RuntimeError("falha externa")

    monkeypatch.setattr("app.gemini_service.genai.Client", BrokenClient)

    with pytest.raises(GeminiServiceError, match="Falha ao iniciar"):
        generate_wellbeing_guidance(
            profile, api_key="fake", models=("modelo-x",)
        )


def test_fact_falha_no_primeiro_modelo_usa_o_proximo(profile, monkeypatch):
    attempted_models = []

    class FakeModels:
        def generate_content(self, *, model, contents):
            attempted_models.append(model)
            if model == "modelo-indisponivel":
                raise RuntimeError("503 temporário")
            return SimpleNamespace(text="orientação pelo fallback")

    class FakeClient:
        def __init__(self, api_key):
            self.models = FakeModels()

    monkeypatch.setattr("app.gemini_service.genai.Client", FakeClient)

    result = generate_wellbeing_guidance(
        profile,
        api_key="fake",
        models=("modelo-indisponivel", "modelo-fallback", "modelo-reserva"),
    )

    assert attempted_models == ["modelo-indisponivel", "modelo-fallback"]
    assert result.text == "orientação pelo fallback"
    assert result.model == "modelo-fallback"


@pytest.mark.parametrize("invalid_text", [None, "", "   ", 123])
def test_inline_data_resposta_vazia_ou_invalida_e_rejeitada(
    profile, monkeypatch, invalid_text
):
    class FakeModels:
        def generate_content(self, *, model, contents):
            return SimpleNamespace(text=invalid_text)

    class FakeClient:
        def __init__(self, api_key):
            self.models = FakeModels()

    monkeypatch.setattr("app.gemini_service.genai.Client", FakeClient)

    with pytest.raises(GeminiServiceError, match="nenhum dos modelos"):
        generate_wellbeing_guidance(
            profile, api_key="fake", models=("modelo-x",)
        )


def test_fact_todos_os_modelos_sao_tentados_antes_do_erro(profile, monkeypatch):
    attempted_models = []

    class FakeModels:
        def generate_content(self, *, model, contents):
            attempted_models.append(model)
            raise RuntimeError(f"falha em {model}")

    class FakeClient:
        def __init__(self, api_key):
            self.models = FakeModels()

    monkeypatch.setattr("app.gemini_service.genai.Client", FakeClient)

    with pytest.raises(GeminiServiceError, match="nenhum dos modelos"):
        generate_wellbeing_guidance(
            profile,
            api_key="fake",
            models=("modelo-a", "modelo-b", "modelo-c"),
        )

    assert attempted_models == ["modelo-a", "modelo-b", "modelo-c"]
