"""Acesso aos dois bancos SQLite usados até a Issue 5."""

from contextlib import contextmanager
from pathlib import Path
import sqlite3
from typing import Iterator

from flask import Flask, current_app


def _connect(path: str) -> sqlite3.Connection:
    """Abre uma conexão SQLite permitindo acessar colunas pelo nome."""
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(path)
    connection.row_factory = sqlite3.Row
    return connection


@contextmanager
def get_auth_db() -> Iterator[sqlite3.Connection]:
    """Abre o users.db e garante commit, rollback e fechamento."""
    connection = _connect(current_app.config["AUTH_DB_PATH"])

    try:
        yield connection
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()


@contextmanager
def get_app_db() -> Iterator[sqlite3.Connection]:
    """Abre o equilibra.db e garante commit, rollback e fechamento."""
    connection = _connect(current_app.config["APP_DB_PATH"])

    try:
        yield connection
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()


def init_databases(app: Flask) -> None:
    """Cria as tabelas necessárias até a Issue 5."""
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

        with get_app_db() as db:
            db.execute(
                """
                CREATE TABLE IF NOT EXISTS profiles (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL UNIQUE,
                    age INTEGER NOT NULL,
                    height_m REAL NOT NULL,
                    weight_kg REAL NOT NULL,
                    goal TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                )
                """
            )
            db.execute(
                """
                CREATE TABLE IF NOT EXISTS guidance_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    age INTEGER NOT NULL,
                    height_m REAL NOT NULL,
                    weight_kg REAL NOT NULL,
                    goal TEXT NOT NULL,
                    response_text TEXT NOT NULL,
                    model TEXT NOT NULL,
                    created_at TEXT NOT NULL
                )
                """
            )
