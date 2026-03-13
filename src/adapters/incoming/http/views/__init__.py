from __future__ import annotations

from flask import Flask

from adapters.incoming.http.views.home import bp as home_bp
from adapters.incoming.http.views.observations import bp as observations_bp
from adapters.incoming.http.views.targets import bp as targets_bp


def register_views(app: Flask) -> None:
    """Register all view blueprints with the app."""
    app.register_blueprint(home_bp)
    app.register_blueprint(targets_bp)
    app.register_blueprint(observations_bp)
