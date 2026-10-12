"""Dados reutilizáveis dos testes, equivalentes ao MemberData do xUnit."""


class CredentialMemberData:
    """Casos inválidos reutilizados nos testes de credenciais."""

    INVALID_CASES = [
        ({}, "Usuário é obrigatório."),
        ({"username": 123, "password": "senha123"}, "Usuário é obrigatório."),
        ({"username": "ab", "password": "senha123"}, "Usuário deve ter entre 3 e 50 caracteres."),
        ({"username": "a" * 51, "password": "senha123"}, "Usuário deve ter entre 3 e 50 caracteres."),
        ({"username": "gustavo"}, "Senha é obrigatória."),
        ({"username": "gustavo", "password": 123456}, "Senha é obrigatória."),
        ({"username": "gustavo", "password": "12345"}, "Senha deve ter entre 6 e 128 caracteres."),
        ({"username": "gustavo", "password": "a" * 129}, "Senha deve ter entre 6 e 128 caracteres."),
    ]
