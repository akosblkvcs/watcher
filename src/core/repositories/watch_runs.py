"""
WatchRun repository.
"""

# pylint: disable=import-error

from __future__ import annotations

from core.db.models.watch_run import WatchRun
from core.repositories.base import RepositoryBase


class WatchRunRepository(RepositoryBase):
    """DB access helpers for WatchRun."""

    def add(self, run: WatchRun) -> None:
        """Add a watch run to the session for persistence."""
        self._session.add(run)

    def get(self, run_id: int) -> WatchRun | None:
        """Return a watch run by id, or None if missing."""
        return self._session.get(WatchRun, run_id)
