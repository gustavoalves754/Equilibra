"""Testes unitários da validação de usuário e senha."""

import re

import pytest

from app.validators import validate_credentials
from tests.data_providers import CredentialMemberData

pytestmark = pytest.mark.unit


def test_fact_credenciais_validas_sao_normalizadas():
    # Arrange
    data = {"username": "  Gustavo  ", "password": "senha123"}

    # Act
    username, password = validate_credentials(data)

    # Assert
    assert username == "gustavo"
    assert password == "senha123"


@pytest.mark.parametrize(
    "payload,expected_message",
    CredentialMemberData.INVALID_CASES,
)
def test_member_data_credenciais_invalidas_geram_excecao(payload, expected_message):
    # Arrange: dados fornecidos pelo MemberData equivalente.
    # Act / Assert
    with pytest.raises(ValueError, match=re.escape(expected_message)):
        validate_credentials(payload)
