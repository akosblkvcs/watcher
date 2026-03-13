"""Outbound port definitions for the application layer.

These protocols define what the application needs from infrastructure
(HTTP fetching, HTML extraction) without knowing the concrete implementation.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from domain.enums import SelectorType


@dataclass(frozen=True)
class FetchResult:
    """Result of fetching a web page."""

    status_code: int
    text: str


@dataclass(frozen=True)
class ExtractResult:
    """Result of extracting text from HTML."""

    texts: list[str]


class Fetcher(Protocol):
    """Port for fetching HTML from a URL."""

    def __call__(self, url: str) -> FetchResult:
        """Fetch a URL and return the response."""
        ...


class Extractor(Protocol):
    """Port for extracting text from HTML content."""

    def __call__(
        self,
        html_text: str,
        selector_type: SelectorType,
        selector: str,
    ) -> ExtractResult:
        """Extract text nodes from HTML using the given selector."""
        ...
