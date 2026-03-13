from __future__ import annotations

from datetime import datetime
from typing import Any

from sqlalchemy import JSON, Boolean, DateTime, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from domain.enums import ProcessorType, SelectorType
from domain.models.base import Base


class Target(Base):
    """ORM model for a target."""

    __tablename__ = "targets"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    name: Mapped[str] = mapped_column(String(200), nullable=False)

    url: Mapped[str] = mapped_column(Text, nullable=False)

    selector_type: Mapped[SelectorType] = mapped_column(
        String(10),
        nullable=False,
        server_default="css",
    )
    selector: Mapped[str] = mapped_column(Text, nullable=False)

    processor_type: Mapped[ProcessorType] = mapped_column(
        String(50),
        nullable=False,
        server_default="raw_text",
    )
    processor_config: Mapped[dict[str, Any] | None] = mapped_column(
        JSON,
        nullable=True,
    )

    last_run_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    last_status: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True,
    )
    last_raw_text: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )
    last_processed_text: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )
    last_error_message: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )
    last_duration_ms: Mapped[int | None] = mapped_column(
        nullable=True,
    )

    active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        server_default="true",
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )
