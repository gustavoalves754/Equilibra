"""Application factory do backend Equilibra."""

from flask import Flask

from .config import Config
from .database import init_databases
from .routes import api


def create_app(test_config: dict | None = None) -> Flask:
    """Cria e configura a aplicação Flask."""
    app = Flask(__name__)
    app.config.from_object(Config)

    if test_config:
        app.config.update(test_config)

    init_databases(app)
    app.register_blueprint(api, url_prefix="/api/v1")

    return app
