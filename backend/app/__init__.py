"""Application factory do backend Equilibra."""

import os
from pathlib import Path

from flask import Flask

from .config import Config
from .database import init_databases
from .routes import api


def create_app(test_config: dict | None = None) -> Flask:
    """Cria e configura a aplicação Flask."""
    default_frontend_dir = Path(__file__).resolve().parents[2] / "frontend"
    frontend_dir = Path(os.getenv("FRONTEND_DIR", default_frontend_dir))

    app = Flask(
        __name__,
        static_folder=str(frontend_dir),
        static_url_path="",
    )
    app.config.from_object(Config)

    if test_config:
        app.config.update(test_config)

    init_databases(app)
    app.register_blueprint(api, url_prefix="/api/v1")

    @app.get("/")
    def frontend_index():
        """Entrega a página principal do frontend."""
        return app.send_static_file("index.html")

    return app
