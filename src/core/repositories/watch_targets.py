from __future__ import annotations

from sqlalchemy import select

from core.db.models.watch_target import WatchTarget
from core.repositories.base import RepositoryBase


class WatchTargetRepository(RepositoryBase):
    """DB access helpers for WatchTarget."""

    def list_active(self) -> list[WatchTarget]:
        """Return all active watch targets."""
        stmt = select(WatchTarget).where(WatchTarget.active.is_(True))
        return list(self._session.scalars(stmt).all())

    def get(self, target_id: int) -> WatchTarget | None:
        """Return a watch target by id, or None if missing."""
        return self._session.get(WatchTarget, target_id)

    def add(self, target: WatchTarget) -> None:
        """Add a watch target to the session for persistence."""
        self._session.add(target)
