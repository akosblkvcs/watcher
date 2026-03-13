from __future__ import annotations

from collections.abc import Sequence

from sqlalchemy import select

from adapters.outgoing.persistence.repositories.base import RepositoryBase
from domain.models.target import Target


class TargetRepository(RepositoryBase):
    """DB access helpers for Target."""

    def list_active(self) -> Sequence[Target]:
        """Return all active targets."""
        stmt = select(Target).where(Target.active.is_(True))
        return self._session.scalars(stmt).all()

    def get(self, target_id: int) -> Target | None:
        """Return a target by id, or None if missing."""
        return self._session.get(Target, target_id)

    def add(self, target: Target) -> None:
        """Add a target to the session for persistence."""
        self._session.add(target)
