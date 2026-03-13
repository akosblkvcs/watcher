from __future__ import annotations

from flask import Blueprint

bp = Blueprint("healthz", __name__)


@bp.get("/healthz")
def healthz() -> tuple[dict[str, str], int]:
    """Return application liveness status."""
    return {"status": "ok"}, 200
