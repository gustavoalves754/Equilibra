"""Validações simples usadas pela API do Equilibra."""


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
