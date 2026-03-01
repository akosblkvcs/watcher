from __future__ import annotations

from collections.abc import Callable
from contextlib import AbstractContextManager
from types import TracebackType

from sqlalchemy.orm import Session


class UnitOfWork(AbstractContextManager["UnitOfWork"]):
    """Transaction boundary for a single logical operation."""

    def __init__(self, session_factory: Callable[[], Session]) -> None:
        """Initialize the unit of work."""
        self._session_factory = session_factory
        self.session: Session | None = None

    def __enter__(self) -> UnitOfWork:
        """Create and bind a new session."""
        self.session = self._session_factory()
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        _exc: BaseException | None,
        _tb: TracebackType | None,
    ) -> None:
        """Commit or rollback transaction, then close session."""
        assert self.session is not None

        try:
            if exc_type is None:
                self.session.commit()
            else:
                self.session.rollback()
        finally:
            self.session.close()
            self.session = None
