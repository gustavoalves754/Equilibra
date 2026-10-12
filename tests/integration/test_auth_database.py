"""Testes de integração da persistência do users.db temporário."""

import pytest

from app.database import get_auth_db

pytestmark = pytest.mark.integration


def test_fact_tabela_users_existe_no_banco_temporario(app):
    with app.app_context():
        with get_auth_db() as db:
            table = db.execute(
                """
                SELECT name
                FROM sqlite_master
                WHERE type = 'table' AND name = 'users'
                """
            ).fetchone()

    assert table is not None
    assert table["name"] == "users"


def test_fact_contexto_do_banco_faz_rollback_quando_ocorre_excecao(app):
    with app.app_context():
        with pytest.raises(RuntimeError):
            with get_auth_db() as db:
                db.execute(
                    """
                    INSERT INTO users (username, password_hash, created_at)
                    VALUES (?, ?, ?)
                    """,
                    ("rollback", "hash", "2026-10-12T00:00:00+00:00"),
                )
                raise RuntimeError("erro proposital")

        with get_auth_db() as db:
            count = db.execute(
                "SELECT COUNT(*) AS total FROM users WHERE username = ?",
                ("rollback",),
            ).fetchone()["total"]

    assert count == 0
