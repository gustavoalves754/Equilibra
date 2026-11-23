"""Entrada WSGI usada pelo Gunicorn no container."""

from app import create_app

app = create_app()
