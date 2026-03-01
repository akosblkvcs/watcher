"""
Target listing routes (HTML views).
"""

from __future__ import annotations

from flask import Blueprint, render_template

from core.config.settings import Settings
from core.db.session import build_session_maker
from core.db.uow import UnitOfWork
from core.repositories.watch_targets import WatchTargetRepository

bp = Blueprint("targets", __name__)


@bp.get("/targets")
def targets():
    """Render the active watch targets page."""
    settings = Settings()
    settings.validate_required()

    session_maker = build_session_maker(settings.database_url)

    with UnitOfWork(session_maker) as uow:
        assert uow.session is not None
        repo = WatchTargetRepository(uow.session)
        items = repo.list_active()

    return render_template("targets.html", targets=items)
