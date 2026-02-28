"""
Manages a database session and transaction boundaries using the Unit of Work
pattern.
"""

from __future__ import annotations

from contextlib import AbstractContextManager
from types import TracebackType
from typing import Callable, TypeVar

from sqlalchemy.orm import Session


ExcT = TypeVar("ExcT", bound=BaseException)


class UnitOfWork(AbstractContextManager["UnitOfWork"]):
    """Session + transaction boundary for a single logical operation."""

    def __init__(self, session_factory: Callable[[], Session]) -> None:
        self._session_factory = session_factory
        self.session: Session | None = None

    def __enter__(self) -> "UnitOfWork":
        self.session = self._session_factory()
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        assert self.session is not None

        try:
            if exc_type is None:
                self.session.commit()
            else:
                self.session.rollback()
        finally:
            self.session.close()
            self.session = None
