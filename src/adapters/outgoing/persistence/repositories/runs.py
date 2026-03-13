from __future__ import annotations

from adapters.outgoing.persistence.repositories.base import RepositoryBase
from domain.models.run import Run


class RunRepository(RepositoryBase):
    """DB access helpers for Run."""

    def add(self, run: Run) -> None:
        """Add a run to the session for persistence."""
        self._session.add(run)

    def get(self, run_id: int) -> Run | None:
        """Return a run by id, or None if missing."""
        return self._session.get(Run, run_id)
