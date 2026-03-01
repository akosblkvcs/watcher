"""
Health check endpoints.
"""

from __future__ import annotations

from flask import Blueprint

bp = Blueprint("health", __name__)


@bp.get("/healthz")
def healthz() -> dict[str, str]:
    """Return service health status."""
    return {"status": "ok"}
