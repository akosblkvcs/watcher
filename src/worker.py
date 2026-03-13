"""Worker entry point — executes a single run.

Usage:
    python -m worker
"""

from __future__ import annotations

from adapters.outgoing.persistence.uow import UnitOfWork
from bootstrap import create_runner, create_session


def main() -> int:
    """Run all active targets once and exit."""
    session = create_session()

    with UnitOfWork(session) as uow:
        runner = create_runner(uow.session)
        result = runner.execute()

    print(
        f"run_id={result.run_id} total={result.targets_total} "
        f"ok={result.targets_succeeded} fail={result.targets_failed}"
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
