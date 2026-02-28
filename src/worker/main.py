"""
Provides the main entry point for the watcher worker service.
"""

from __future__ import annotations

from sqlalchemy import text

from core.config.settings import Settings
from core.db.engine import build_engine


def main() -> int:
    """Main entry point for the watcher worker service."""

    settings = Settings()
    engine = build_engine(settings.database_url)

    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
    print("db_ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
