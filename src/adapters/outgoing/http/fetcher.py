"""HTTP client for fetching target web pages."""

from __future__ import annotations

import sys

import httpx

from application.ports import FetchResult
from config import settings

if settings.env == "development" and sys.platform.startswith("win"):
    import truststore

    truststore.inject_into_ssl()


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
