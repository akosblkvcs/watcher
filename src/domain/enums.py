"""Domain vocabulary as enumeration types."""

from __future__ import annotations

import enum


class ProcessorType(enum.StrEnum):
    """Supported text processors."""

    RAW_TEXT = "raw_text"
    MIN_VALUE = "min_value"


class SelectorType(enum.StrEnum):
    """Supported HTML selector strategies."""

    CSS = "css"
    XPATH = "xpath"


class RunStatus(enum.StrEnum):
    """Outcome status for a watch run."""

    SUCCESS = "success"
    PARTIAL = "partial"
    FAILURE = "failure"


class TargetStatus(enum.StrEnum):
    """Outcome status for an individual target check."""

    SUCCESS = "success"
    FAILURE = "failure"
