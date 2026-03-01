"""
Flask application factory for the watcher web API.
"""

from __future__ import annotations

from flask import Flask

from web.routes.health import bp as health_bp
from web.routes.targets import bp as targets_bp
from web.routes.observations import bp as observations_bp


def create_app() -> Flask:
    """Create and configure the Flask app with registered blueprints."""
    app = Flask(__name__)

    app.register_blueprint(health_bp)
    app.register_blueprint(targets_bp)
    app.register_blueprint(observations_bp)

    return app
