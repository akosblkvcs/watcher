"""
WatchObservation repository.
"""

# pylint: disable=import-error,too-few-public-methods

from __future__ import annotations

from sqlalchemy.orm import Session

from core.db.models.watch_observation import WatchObservation


class WatchObservationRepository:
    """DB access helpers for WatchObservation."""

    def __init__(self, session: Session) -> None:
        self._session = session

    def add(self, obs: WatchObservation) -> None:
        """Add an observation to the session for persistence."""
        self._session.add(obs)
