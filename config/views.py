"""Project-level views that belong to no single app."""

from django.http import HttpRequest, JsonResponse


def healthz(_request: HttpRequest) -> JsonResponse:
    """Return application liveness status."""
    return JsonResponse({"status": "ok"})
