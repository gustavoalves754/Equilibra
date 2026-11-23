"""Testes de integração do equilibra.db temporário e separado do users.db."""

import sqlite3

import pytest

from app.database import get_app_db

pytestmark = pytest.mark.integration


def _table_names(path: str) -> set[str]:
    connection = sqlite3.connect(path)
    try:
        rows = connection.execute(
            "SELECT name FROM sqlite_master WHERE type = 'table'"
        ).fetchall()
        return {row[0] for row in rows}
    finally:
        connection.close()


def test_fact_users_db_e_equilibra_db_sao_separados(app):
    auth_path = app.config["AUTH_DB_PATH"]
    app_path = app.config["APP_DB_PATH"]

    auth_tables = _table_names(auth_path)
    app_tables = _table_names(app_path)

    assert auth_path != app_path
    assert "users" in auth_tables
    assert "profiles" not in auth_tables
    assert "profiles" in app_tables
    assert "users" not in app_tables


def test_fact_banco_funcional_persiste_perfil(app):
    with app.app_context():
        with get_app_db() as db:
            db.execute(
                """
                INSERT INTO profiles (user_id, age, height_m, weight_kg, goal, updated_at)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (1, 30, 1.80, 80, "bem-estar", "2026-10-12T00:00:00+00:00"),
            )

        with get_app_db() as db:
            row = db.execute(
                "SELECT goal FROM profiles WHERE user_id = ?",
                (1,),
            ).fetchone()

    assert row["goal"] == "bem-estar"


def test_fact_contexto_do_equilibra_db_faz_rollback_em_excecao(app):
    with app.app_context():
        with pytest.raises(RuntimeError):
            with get_app_db() as db:
                db.execute(
                    """
                    INSERT INTO profiles (user_id, age, height_m, weight_kg, goal, updated_at)
                    VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (1, 30, 1.80, 80, "rollback", "2026-10-12T00:00:00+00:00"),
                )
                raise RuntimeError("erro proposital")

        with get_app_db() as db:
            count = db.execute(
                "SELECT COUNT(*) AS total FROM profiles WHERE goal = ?",
                ("rollback",),
            ).fetchone()["total"]

    assert count == 0
