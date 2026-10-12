"""Configurações da aplicação carregadas por variáveis de ambiente."""

import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"


class Config:
    """Configuração padrão usada pelo Equilibra."""

    AUTH_DB_PATH = os.getenv("AUTH_DB_PATH", str(DATA_DIR / "users.db"))
    JWT_SECRET = os.getenv("JWT_SECRET", "chave-local-apenas-para-desenvolvimento")
    TOKEN_EXP_HOURS = int(os.getenv("TOKEN_EXP_HOURS", "8"))
