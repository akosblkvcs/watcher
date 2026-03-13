from __future__ import annotations

from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix

from adapters.incoming.http.errors import register_error_handlers
from adapters.incoming.http.extensions import db
from adapters.incoming.http.views import register_views
from config import settings


def create_app() -> Flask:
    """Create and configure the Flask application."""
    app = Flask(__name__)

    # --- Configuration ---
    app.config["SQLALCHEMY_DATABASE_URI"] = str(settings.database_url)
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {"pool_pre_ping": True}

    # --- Middleware ---
    # Tells Flask it is behind a proxy (Coolify/Traefik).
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

    # --- Extensions ---
    db.init_app(app)

    # --- Views & error handlers ---
    register_views(app)
    register_error_handlers(app)

    return app
