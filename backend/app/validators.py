"""Validações simples usadas pela API do Equilibra."""

import math


def validate_credentials(data: dict) -> tuple[str, str]:
    """Valida username e senha usados no cadastro e no login."""
    username = data.get("username")
    password = data.get("password")

    if not isinstance(username, str):
        raise ValueError("Usuário é obrigatório.")

    username = username.strip().lower()
    if len(username) < 3 or len(username) > 50:
        raise ValueError("Usuário deve ter entre 3 e 50 caracteres.")

    if not isinstance(password, str):
        raise ValueError("Senha é obrigatória.")

    if len(password) < 6 or len(password) > 128:
        raise ValueError("Senha deve ter entre 6 e 128 caracteres.")

    return username, password


def validate_profile(data: dict) -> dict:
    """Valida e normaliza idade, altura, peso e objetivo.

    Regras principais:
    - idade não pode ser negativa;
    - altura deve ser informada em metros e ser >= 1.00;
    - peso deve ser maior que 1 kg;
    - objetivo é obrigatório.

    Os limites máximos apenas evitam erros evidentes de digitação.
    """
    try:
        age_value = data.get("age")
        age_float = float(age_value)
        height_m = float(data.get("height_m"))
        weight_kg = float(data.get("weight_kg"))
    except (TypeError, ValueError, OverflowError):
        raise ValueError("Idade, altura e peso devem ser numéricos.") from None

    if (
        not math.isfinite(age_float)
        or not math.isfinite(height_m)
        or not math.isfinite(weight_kg)
    ):
        raise ValueError("Idade, altura e peso devem ser numéricos.")

    if not age_float.is_integer():
        raise ValueError("A idade deve ser informada em anos inteiros.")

    age = int(age_float)
    goal_value = data.get("goal")
    goal = goal_value.strip() if isinstance(goal_value, str) else ""

    if age < 0:
        raise ValueError("A idade não pode ser negativa.")
    if age > 120:
        raise ValueError("A idade informada está fora da faixa aceita pelo sistema.")
    if height_m < 1.0:
        raise ValueError("A altura deve ser informada em metros e ser no mínimo 1.00.")
    if height_m > 2.60:
        raise ValueError("A altura informada está fora da faixa aceita pelo sistema.")
    if weight_kg <= 1:
        raise ValueError("O peso deve ser maior que 1 kg.")
    if weight_kg > 500:
        raise ValueError("O peso informado está fora da faixa aceita pelo sistema.")
    if not goal:
        raise ValueError("O objetivo é obrigatório.")
    if len(goal) > 200:
        raise ValueError("O objetivo deve ter no máximo 200 caracteres.")

    return {
        "age": age,
        "height_m": round(height_m, 2),
        "weight_kg": round(weight_kg, 2),
        "goal": goal,
    }
