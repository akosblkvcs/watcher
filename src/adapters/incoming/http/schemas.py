"""Pydantic request/response schemas for the HTTP API."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, HttpUrl

from domain.enums import ProcessorType, SelectorType, TargetStatus


class TargetCreate(BaseModel):
    """Validated input for creating a new target."""

    name: str
    url: HttpUrl
    selector_type: SelectorType = SelectorType.CSS
    selector: str
    processor_type: ProcessorType = ProcessorType.RAW_TEXT
    processor_config: dict[str, object] | None = None
    active: bool = True


class TargetUpdate(BaseModel):
    """Validated input for updating an existing target (partial)."""

    name: str | None = None
    url: HttpUrl | None = None
    selector_type: SelectorType | None = None
    selector: str | None = None
    processor_type: ProcessorType | None = None
    processor_config: dict[str, object] | None = None
    active: bool | None = None


class TargetRead(BaseModel):
    """Serialised representation of a target."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    url: HttpUrl
    selector_type: SelectorType
    selector: str
    processor_type: ProcessorType
    processor_config: dict[str, object] | None
    active: bool
    last_run_at: datetime | None
    last_status: TargetStatus | None
    last_processed_text: str | None
    last_error_message: str | None
    last_duration_ms: int | None
