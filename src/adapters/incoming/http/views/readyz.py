from __future__ import annotations

import logging

from flask import Blueprint
from sqlalchemy import text

from bootstrap import create_session

log = logging.getLogger(__name__)
bp = Blueprint("readyz", __name__)


@bp.get("/readyz")
def readyz() -> tuple[dict[str, str], int]:
    """Return application readiness status."""
    session = None

    try:
        session = create_session()
        session.execute(text("SELECT 1"))
        return {"status": "ready"}, 200
    except Exception:
        log.exception("Readiness check failed")

        return {"status": "not ready"}, 503
    finally:
        if session is not None:
            session.close()
