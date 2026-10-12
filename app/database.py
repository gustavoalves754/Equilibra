"""Acesso ao banco SQLite de autenticação do Equilibra."""

from contextlib import contextmanager
from pathlib import Path
import sqlite3
from typing import Iterator

from flask import Flask, current_app


def _connect(path: str) -> sqlite3.Connection:
    """Abre uma conexão SQLite configurada para acessar colunas pelo nome."""
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(path)
    connection.row_factory = sqlite3.Row
    return connection


@contextmanager
def get_auth_db() -> Iterator[sqlite3.Connection]:
    """Abre o users.db e garante commit, rollback e fechamento da conexão."""
    connection = _connect(current_app.config["AUTH_DB_PATH"])

    try:
        yield connection
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()


def init_auth_database(app: Flask) -> None:
    """Cria somente a tabela de usuários desta etapa do projeto."""
    with app.app_context():
        with get_auth_db() as db:
            db.execute(
                """
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL UNIQUE,
                    password_hash TEXT NOT NULL,
                    created_at TEXT NOT NULL
                )
                """
            )
