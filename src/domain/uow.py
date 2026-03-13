"""Unit of Work port definition."""

from __future__ import annotations

from typing import Protocol


class UnitOfWorkPort(Protocol):
    """Port for transactional operations.

    Abstracts persistence-level session management so the application
    layer can flush pending changes without knowing about SQLAlchemy.
    """

    def flush(self) -> None:
        """Flush pending changes so generated ids are available."""
        ...
