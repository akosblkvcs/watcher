"""Management command: run all active targets once.

Usage:
    python manage.py run_watch
"""

from __future__ import annotations

from typing import Any

from django.core.management.base import BaseCommand

from watch.services.runner import run_all


class Command(BaseCommand):
    """Run all active watch targets once and report the result."""

    help = "Check all active watch targets once."

    def handle(self, *args: Any, **options: Any) -> None:
        """Execute the run and print a summary."""
        result = run_all()

        self.stdout.write(
            f"run_id={result.run_id} total={result.targets_total} "
            f"ok={result.targets_succeeded} fail={result.targets_failed}"
        )
