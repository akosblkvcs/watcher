from __future__ import annotations

import enum


class SelectorType(enum.StrEnum):
    """Supported HTML selector strategies."""

    CSS = "css"
    XPATH = "xpath"


class RunStatus(enum.StrEnum):
    """Outcome status for a watch run."""

    SUCCESS = "success"
    PARTIAL = "partial"


class TargetStatus(enum.StrEnum):
    """Outcome status for an individual target check."""

    SUCCESS = "success"
    FAILURE = "failure"
