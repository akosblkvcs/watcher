from __future__ import annotations

from flask import Flask

from adapters.incoming.http.views.healthz import bp as healthz_bp
from adapters.incoming.http.views.home import bp as home_bp
from adapters.incoming.http.views.observations import (
    create_blueprint as create_observations_blueprint,
)
from adapters.incoming.http.views.readyz import bp as readyz_bp
from adapters.incoming.http.views.targets import (
    create_blueprint as create_targets_blueprint,
)
from adapters.outgoing.persistence.repositories.observations import ObservationRepository
from adapters.outgoing.persistence.repositories.targets import TargetRepository


def register_views(app: Flask) -> None:
    """Register all view blueprints with the app."""
    app.register_blueprint(healthz_bp)
    app.register_blueprint(home_bp)
    app.register_blueprint(create_observations_blueprint(ObservationRepository))
    app.register_blueprint(readyz_bp)
    app.register_blueprint(create_targets_blueprint(TargetRepository))
