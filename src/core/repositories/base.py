"""
Shared repository base for SQLAlchemy session helpers.
"""

# pylint: disable=too-few-public-methods

from __future__ import annotations

from sqlalchemy.orm import Session


class RepositoryBase:
    """Base repository providing access to a SQLAlchemy session."""

    def __init__(self, session: Session) -> None:
        """Create repository using the given SQLAlchemy session."""
        self._session = session

    def flush(self) -> None:
        """Flush pending changes so PKs (ids) are available."""
        self._session.flush()
