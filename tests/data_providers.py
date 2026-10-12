"""Dados reutilizáveis dos testes, adaptando MemberData e ClassData do xUnit."""


class CredentialMemberData:
    """MemberData equivalente: casos de credenciais expostos por um membro."""

    INVALID_CASES = [
        ({}, "Usuário é obrigatório."),
        ({"username": 123, "password": "senha123"}, "Usuário é obrigatório."),
        (
            {"username": "ab", "password": "senha123"},
            "Usuário deve ter entre 3 e 50 caracteres.",
        ),
        (
            {"username": "a" * 51, "password": "senha123"},
            "Usuário deve ter entre 3 e 50 caracteres.",
        ),
        ({"username": "gustavo"}, "Senha é obrigatória."),
        ({"username": "gustavo", "password": 123456}, "Senha é obrigatória."),
        (
            {"username": "gustavo", "password": "12345"},
            "Senha deve ter entre 6 e 128 caracteres.",
        ),
        (
            {"username": "gustavo", "password": "a" * 129},
            "Senha deve ter entre 6 e 128 caracteres.",
        ),
    ]


class ProfileInvalidClassData:
    """ClassData equivalente: classe separada que fornece perfis inválidos."""

    def __iter__(self):
        yield (
            {"age": -1, "height_m": 1.70, "weight_kg": 70, "goal": "saúde"},
            "idade não pode ser negativa",
        )
        yield (
            {"age": 121, "height_m": 1.70, "weight_kg": 70, "goal": "saúde"},
            "idade informada está fora",
        )
        yield (
            {"age": 30, "height_m": 0.99, "weight_kg": 70, "goal": "saúde"},
            "altura deve ser informada em metros",
        )
        yield (
            {"age": 30, "height_m": 2.61, "weight_kg": 70, "goal": "saúde"},
            "altura informada está fora",
        )
        yield (
            {"age": 30, "height_m": 1.70, "weight_kg": 1, "goal": "saúde"},
            "peso deve ser maior que 1",
        )
        yield (
            {"age": 30, "height_m": 1.70, "weight_kg": 501, "goal": "saúde"},
            "peso informado está fora",
        )
        yield (
            {"age": 30, "height_m": 1.70, "weight_kg": 70, "goal": "   "},
            "objetivo é obrigatório",
        )
        yield (
            {"age": 30, "height_m": 1.70, "weight_kg": 70, "goal": None},
            "objetivo é obrigatório",
        )
        yield (
            {"age": 30, "height_m": 1.70, "weight_kg": 70, "goal": "x" * 201},
            "objetivo deve ter no máximo 200",
        )
        yield (
            {"age": "abc", "height_m": 1.70, "weight_kg": 70, "goal": "saúde"},
            "devem ser numéricos",
        )
        yield (
            {"age": 25.5, "height_m": 1.70, "weight_kg": 70, "goal": "saúde"},
            "idade deve ser informada em anos inteiros",
        )
