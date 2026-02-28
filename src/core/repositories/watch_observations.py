"""
WatchObservation repository.
"""

# pylint: disable=import-error,too-few-public-methods

from __future__ import annotations

from core.db.models.watch_observation import WatchObservation
from core.repositories.base import RepositoryBase


class WatchObservationRepository(RepositoryBase):
    """DB access helpers for WatchObservation."""

    def add(self, obs: WatchObservation) -> None:
        """Add an observation to the session for persistence."""
        self._session.add(obs)
