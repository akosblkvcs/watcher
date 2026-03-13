from __future__ import annotations

from typing import Any

from sqlalchemy.orm import Session
from sqlalchemy.orm.scoping import scoped_session


class RepositoryBase:
    """Base repository providing access to a SQLAlchemy session."""

    def __init__(self, session: Session | scoped_session[Any]) -> None:
        """Create repository using the given SQLAlchemy session."""
        self._session = session

    def flush(self) -> None:
        """Flush pending changes so ids are available."""
        self._session.flush()
