from collections.abc import Callable

import httpx
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

from watch.models import Target

FetchBackend = Callable[[str], str]
"""A fetch backend: takes a URL, returns the page's HTML as text."""


def fetch_html(fetch_method: str, url: str) -> str:
    """Fetch a URL using the selected method."""
    fetcher = FETCHERS.get(fetch_method)

    if fetcher is None:
        raise ValueError(f"Unknown fetch_method: {fetch_method}")

    return fetcher(url)


def fetch_with_httpx(url: str) -> str:
    """Fetch a URL directly with httpx and return the response body."""
    transport = httpx.HTTPTransport(retries=settings.HTTP_RETRIES)

    with httpx.Client(
        transport=transport,
        headers={"User-Agent": settings.USER_AGENT},
        timeout=settings.HTTP_TIMEOUT_SECONDS,
        follow_redirects=True,
    ) as client:
        resp = client.get(url)
        resp.raise_for_status()

        return resp.text


def fetch_with_brightdata(url: str) -> str:
    """Fetch a URL through Bright Data's Web Unlocker API."""
    api_key = settings.BRIGHTDATA_API_KEY

    if not api_key:
        raise ImproperlyConfigured("BRIGHTDATA_API_KEY must be set")

    transport = httpx.HTTPTransport(retries=settings.HTTP_RETRIES)

    with httpx.Client(transport=transport, timeout=settings.HTTP_TIMEOUT_SECONDS) as client:
        resp = client.post(
            "https://api.brightdata.com/request",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            json={
                "zone": "watcher",
                "url": url,
                "format": "raw",
            },
        )
        resp.raise_for_status()
        return resp.text


FETCHERS: dict[str, FetchBackend] = {
    Target.FetchMethod.HTTPX: fetch_with_httpx,
    Target.FetchMethod.BRIGHTDATA: fetch_with_brightdata,
}
