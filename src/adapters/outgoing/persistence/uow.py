from __future__ import annotations

from contextlib import AbstractContextManager
from types import TracebackType
from typing import Any

from sqlalchemy.orm import Session
from sqlalchemy.orm.scoping import scoped_session


class UnitOfWork(AbstractContextManager["UnitOfWork"]):
    """Transaction boundary that wraps an existing SQLAlchemy session.

    Use as a context manager around write operations.  On clean exit the
    session is committed; on exception it is rolled back.

    For read-only operations you can use the session directly without
    wrapping it in a UnitOfWork.
    """

    def __init__(self, session: Session | scoped_session[Any]) -> None:
        """Initialize with an active session (e.g. ``db.session``)."""
        self._session = session

    @property
    def session(self) -> Session | scoped_session[Any]:
        """Return the underlying SQLAlchemy session."""
        return self._session

    def __enter__(self) -> UnitOfWork:
        """Enter the transactional scope."""
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        _exc: BaseException | None,
        _tb: TracebackType | None,
    ) -> None:
        """Commit on success, rollback on failure."""
        if exc_type is None:
            self._session.commit()
        else:
            self._session.rollback()

    def commit(self) -> None:
        """Explicitly commit the current transaction."""
        self._session.commit()

    def rollback(self) -> None:
        """Explicitly rollback the current transaction."""
        self._session.rollback()
