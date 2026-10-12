"""Configurações do backend carregadas por variáveis de ambiente."""

import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"


class Config:
    """Configuração padrão da aplicação."""

    AUTH_DB_PATH = os.getenv("AUTH_DB_PATH", str(DATA_DIR / "users.db"))
    APP_DB_PATH = os.getenv("APP_DB_PATH", str(DATA_DIR / "equilibra.db"))

    JWT_SECRET = os.getenv("JWT_SECRET", "troque-esta-chave-em-desenvolvimento")
    TOKEN_EXP_HOURS = int(os.getenv("TOKEN_EXP_HOURS", "8"))

    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
    GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")
