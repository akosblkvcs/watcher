from __future__ import annotations

from sqlalchemy import select

from adapters.outgoing.persistence.repositories.base import RepositoryBase
from domain.models.observation import Observation


class ObservationRepository(RepositoryBase):
    """DB access helpers for Observation."""

    def add(self, obs: Observation) -> None:
        """Add an observation to the session for persistence."""
        self._session.add(obs)

    def list_recent(self, *, limit: int) -> list[Observation]:
        """Return the most recent observations (newest first)."""
        stmt = select(Observation).order_by(Observation.id.desc()).limit(limit)
        rows = self._session.scalars(stmt).all()
        return list(rows)
