"""
Provides the main entry point for the watcher worker service.
"""

from __future__ import annotations

from core.config.settings import Settings
from core.db.session import build_session_maker
from core.db.uow import UnitOfWork
from core.db.models.watch_target import WatchTarget
from core.repositories.watch_targets import WatchTargetRepository


def main() -> int:
    """Main entry point for the watcher worker service."""

    settings = Settings()
    settings.validate_required()

    session_maker = build_session_maker(settings.database_url)

    with UnitOfWork(session_maker) as uow:
        assert uow.session is not None
        repo = WatchTargetRepository(uow.session)

        targets = repo.list_active()
        print(f"targets_active={len(targets)}")

        if not targets:
            repo.add(
                WatchTarget(
                    name="Example",
                    url="https://example.com",
                    selector_type="css",
                    selector="h1",
                    processor_type="raw_text",
                    active=True,
                )
            )

    with UnitOfWork(session_maker) as uow:
        assert uow.session is not None
        repo = WatchTargetRepository(uow.session)
        targets = repo.list_active()
        print(f"targets_active_after_insert={len(targets)}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
