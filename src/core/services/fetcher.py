from __future__ import annotations

import sys
from dataclasses import dataclass

import httpx

from core.config.settings import settings

if settings.env == "development" and sys.platform.startswith("win"):
    import truststore

    truststore.inject_into_ssl()


@dataclass(frozen=True)
class FetchResult:
    """HTTP fetch result class."""

    status_code: int
    text: str


def fetch_html(url: str) -> FetchResult:
    """Fetch HTML from a URL and return status code plus response text."""
    headers = {"User-Agent": settings.user_agent}
    transport = httpx.HTTPTransport(retries=settings.http_retries)

    with httpx.Client(
        transport=transport,
        headers=headers,
        timeout=settings.http_timeout_seconds,
        follow_redirects=True,
    ) as client:
        resp = client.get(url)
        resp.raise_for_status()
        return FetchResult(status_code=resp.status_code, text=resp.text)
