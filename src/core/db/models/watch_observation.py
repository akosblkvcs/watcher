from __future__ import annotations

from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from core.db.base import Base


class WatchObservation(Base):
    """ORM model for a watch observation."""

    __tablename__ = "watch_observations"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    run_id: Mapped[int] = mapped_column(
        ForeignKey("watch_runs.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    target_id: Mapped[int] = mapped_column(
        ForeignKey("watch_targets.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    observed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    raw_text: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )
    processed_text: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    changed: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        server_default="false",
    )
    previous_processed_text: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    error_message: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )
    duration_ms: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )
