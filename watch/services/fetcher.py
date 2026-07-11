"""HTTP client for fetching target web pages."""

from __future__ import annotations

import httpx
from django.conf import settings


def fetch_html(url: str) -> str:
    """Fetch a URL and return the response body as text.

    Raises ``httpx.HTTPStatusError`` on non-2xx responses.
    """
    transport = httpx.HTTPTransport(retries=settings.WATCHER_HTTP_RETRIES)

    with httpx.Client(
        transport=transport,
        headers={"User-Agent": settings.WATCHER_USER_AGENT},
        timeout=settings.WATCHER_HTTP_TIMEOUT_SECONDS,
        follow_redirects=True,
    ) as client:
        resp = client.get(url)
        resp.raise_for_status()

        return resp.text
