"""Testes unitários das regras de perfil da Issue 3."""

import re

import pytest

from app.validators import validate_profile
from tests.data_providers import ProfileInvalidClassData

pytestmark = pytest.mark.unit


def test_fact_perfil_valido_retorna_dados_normalizados():
    # Arrange
    payload = {
        "age": 25,
        "height_m": 1.756,
        "weight_kg": 70.126,
        "goal": "  ganhar massa  ",
    }

    # Act
    result = validate_profile(payload)

    # Assert
    assert result == {
        "age": 25,
        "height_m": 1.76,
        "weight_kg": 70.13,
        "goal": "ganhar massa",
    }


@pytest.mark.parametrize("weight", [-10, 0, 1])
def test_inline_data_peso_deve_ser_maior_que_um(weight):
    payload = {"age": 25, "height_m": 1.75, "weight_kg": weight, "goal": "saúde"}

    with pytest.raises(ValueError, match="peso deve ser maior que 1"):
        validate_profile(payload)


@pytest.mark.parametrize("height", [-2, 0, 0.99])
def test_inline_data_altura_deve_ser_no_minimo_um_metro(height):
    payload = {"age": 25, "height_m": height, "weight_kg": 70, "goal": "saúde"}

    with pytest.raises(ValueError, match="altura deve ser informada em metros"):
        validate_profile(payload)


@pytest.mark.parametrize("age", [-50, -1])
def test_inline_data_idade_nao_pode_ser_negativa(age):
    payload = {"age": age, "height_m": 1.75, "weight_kg": 70, "goal": "saúde"}

    with pytest.raises(ValueError, match="idade não pode ser negativa"):
        validate_profile(payload)


def test_fact_limites_minimos_validos_sao_aceitos():
    result = validate_profile(
        {"age": 0, "height_m": 1.0, "weight_kg": 1.01, "goal": "bem-estar"}
    )

    assert result["age"] == 0
    assert result["height_m"] == 1.0
    assert result["weight_kg"] == 1.01


@pytest.mark.parametrize("payload,expected_message", ProfileInvalidClassData())
def test_class_data_perfis_invalidos_geram_excecao(payload, expected_message):
    with pytest.raises(ValueError, match=re.escape(expected_message)):
        validate_profile(payload)
