"""
WatchRun repository.
"""

# pylint: disable=import-error

from __future__ import annotations

from sqlalchemy.orm import Session

from core.db.models.watch_run import WatchRun


class WatchRunRepository:
    """DB access helpers for WatchRun."""

    def __init__(self, session: Session) -> None:
        self._session = session

    def add(self, run: WatchRun) -> None:
        """Add a watch run to the session for persistence."""
        self._session.add(run)

    def get(self, run_id: int) -> WatchRun | None:
        """Return a watch run by id, or None if missing."""
        return self._session.get(WatchRun, run_id)
