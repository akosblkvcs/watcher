from __future__ import annotations

from flask import Blueprint, render_template

from core.db.session import build_session_maker
from core.db.uow import UnitOfWork
from core.repositories.watch_observations import WatchObservationRepository

bp = Blueprint("observations", __name__)


@bp.get("/observations")
def observations():
    """Render the most recent observations page."""
    session_maker = build_session_maker()

    with UnitOfWork(session_maker) as uow:
        assert uow.session is not None

        repo = WatchObservationRepository(uow.session)
        items = repo.list_recent(limit=100)

    return render_template("observations.html", observations=items)
