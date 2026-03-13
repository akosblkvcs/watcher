"""Domain exception hierarchy."""

from __future__ import annotations

from domain.enums import ProcessorType


class AppError(Exception):
    """Base exception for all watcher domain errors."""


class FetchError(AppError):
    """Raised when an HTTP fetch fails."""


class ExtractionError(AppError):
    """Raised when HTML content extraction fails."""


class ProcessorError(AppError):
    """Raised when a text processor encounters an error."""

    def __init__(self, processor_type: ProcessorType, detail: str) -> None:
        """Create with the processor name and failure detail."""
        self.processor_type = processor_type
        super().__init__(f"Processor '{processor_type}' failed: {detail}")


class TargetNotFoundError(AppError):
    """Raised when a watch target cannot be found."""

    def __init__(self, target_id: int) -> None:
        """Create with the missing target id."""
        self.target_id = target_id
        super().__init__(f"Watch target {target_id} not found")
