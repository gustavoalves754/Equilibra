"""Testes unitários do prompt enviado ao Gemini."""

import pytest

from app.prompts import build_wellbeing_prompt

pytestmark = pytest.mark.unit


def test_fact_prompt_adulto_contem_dados_e_regras_de_seguranca():
    # Arrange
    profile = {"age": 30, "height_m": 1.80, "weight_kg": 82, "goal": "emagrecer"}

    # Act
    prompt = build_wellbeing_prompt(profile)

    # Assert
    assert "30 anos" in prompt
    assert "1.8 m" in prompt
    assert "82 kg" in prompt
    assert "emagrecer" in prompt
    assert "Não faça diagnóstico médico" in prompt
    assert '"Resumo"' in prompt
    assert '"Atenção"' in prompt
    assert "menor que 18 anos" not in prompt


@pytest.mark.parametrize("age", [0, 10, 17])
def test_inline_data_prompt_de_menor_inclui_cuidado_adicional(age):
    profile = {"age": age, "height_m": 1.70, "weight_kg": 60, "goal": "bem-estar"}

    prompt = build_wellbeing_prompt(profile)

    assert "menor que 18 anos" in prompt
    assert "responsável" in prompt
