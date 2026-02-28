"""
HTTP fetching helpers for downloading HTML pages.
"""

from __future__ import annotations

import sys
from dataclasses import dataclass

import httpx


if sys.platform.startswith("win"):
    import truststore

    truststore.inject_into_ssl()


@dataclass(frozen=True)
class FetchResult:
    """HTTP fetch result container."""
    status_code: int
    text: str


def fetch_html(url: str, user_agent: str, timeout_seconds: int) -> FetchResult:
    """Fetch HTML from a URL and return status code plus response text."""
    headers = {"User-Agent": user_agent}
    with httpx.Client(
        headers=headers,
        timeout=timeout_seconds,
        follow_redirects=True
    ) as client:
        resp = client.get(url)
        resp.raise_for_status()
        return FetchResult(status_code=resp.status_code, text=resp.text)
