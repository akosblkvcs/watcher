"""
Defines the WatchRun model for the database.
"""

# pylint: disable=not-callable,too-few-public-methods

from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from core.db.base import Base


class WatchRun(Base):
    """ORM model for a watch run."""

    __tablename__ = "watch_runs"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    started_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
    finished_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )
    error_summary: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )
