"""
Observation listing routes.
"""

from __future__ import annotations

from flask import Blueprint, render_template

from core.config.settings import Settings
from core.db.session import build_session_maker
from core.db.uow import UnitOfWork
from core.repositories.watch_observations import WatchObservationRepository

bp = Blueprint("observations", __name__)


@bp.get("/observations")
def observations():
    """Render the most recent observations page."""
    settings = Settings()
    settings.validate_required()

    session_maker = build_session_maker(settings.database_url)

    with UnitOfWork(session_maker) as uow:
        assert uow.session is not None
        repo = WatchObservationRepository(uow.session)
        items = repo.list_recent(limit=100)

    return render_template("observations.html", observations=items)
