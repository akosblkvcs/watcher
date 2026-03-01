"""
WatchObservation repository.
"""

from __future__ import annotations

from sqlalchemy import select

from core.db.models.watch_observation import WatchObservation
from core.repositories.base import RepositoryBase


class WatchObservationRepository(RepositoryBase):
    """DB access helpers for WatchObservation."""

    def add(self, obs: WatchObservation) -> None:
        """Add an observation to the session for persistence."""
        self._session.add(obs)

    def list_recent(self, *, limit: int) -> list[WatchObservation]:
        """Return the most recent observations (newest first)."""
        stmt = (
            select(WatchObservation)
            .order_by(WatchObservation.id.desc())
            .limit(limit)
        )
        rows = self._session.scalars(
            stmt
        ).all()
        return list(rows)
