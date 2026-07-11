"""Orchestrates a single watcher run across all active targets."""

from __future__ import annotations

import logging
from dataclasses import dataclass
from datetime import datetime

from django.db import transaction
from django.utils import timezone

from watch.models import Observation, Run, Target
from watch.services.extractor import extract_texts
from watch.services.fetcher import fetch_html
from watch.services.processors import PROCESSORS

log = logging.getLogger(__name__)


@dataclass(frozen=True)
class RunResult:
    """Execution summary for a watcher run."""

    run_id: int
    targets_total: int
    targets_succeeded: int
    targets_failed: int


def run_all() -> RunResult:
    """Check all active targets once and persist per-target results."""
    run = Run.objects.create(status=Run.Status.PARTIAL)
    targets = list(Target.objects.filter(active=True))
    ok = 0

    for target in targets:
        if _process_target(run, target):
            ok += 1

    fail = len(targets) - ok

    run.finished_at = timezone.now()

    if fail == 0:
        run.status = Run.Status.SUCCESS
    elif ok == 0:
        run.status = Run.Status.FAILURE
    else:
        run.status = Run.Status.PARTIAL

    run.error_summary = None if fail == 0 else f"{fail} targets failed"
    run.save(update_fields=["finished_at", "status", "error_summary"])

    return RunResult(
        run_id=run.pk,
        targets_total=len(targets),
        targets_succeeded=ok,
        targets_failed=fail,
    )


def _process_target(run: Run, target: Target) -> bool:
    """Check a single target. Returns True on success, else False."""
    started = timezone.now()

    try:
        html_text = fetch_html(target.url)
        texts = extract_texts(html_text, target.selector_type, target.selector)
        raw = ", ".join(texts)

        processor = PROCESSORS[target.processor_type]
        processed = processor(texts, target.processor_config or {})

    except Exception as ex:
        log.exception("Target %s (%s) failed", target.pk, target.name)
        _record_failure(run, target, started, error=f"{type(ex).__name__}: {ex}")
        return False

    _record_success(run, target, started, raw=raw, processed=processed)
    return True


def _record_success(
    run: Run,
    target: Target,
    started: datetime,
    *,
    raw: str,
    processed: str,
) -> None:
    """Persist the observation and updated target state for a success."""
    finished = timezone.now()
    duration_ms = _duration_ms(started, finished)
    previous = target.last_processed_text
    changed = is_changed(previous, processed)

    with transaction.atomic():
        Observation.objects.create(
            run=run,
            target=target,
            raw_text=raw,
            processed_text=processed,
            changed=changed,
            previous_processed_text=previous,
            duration_ms=duration_ms,
        )

        target.last_run_at = finished
        target.last_status = Target.Status.SUCCESS
        target.last_raw_text = raw
        target.last_processed_text = processed
        target.last_error_message = None
        target.last_duration_ms = duration_ms
        target.save(
            update_fields=[
                "last_run_at",
                "last_status",
                "last_raw_text",
                "last_processed_text",
                "last_error_message",
                "last_duration_ms",
                "updated_at",
            ]
        )


def _record_failure(
    run: Run,
    target: Target,
    started: datetime,
    *,
    error: str,
) -> None:
    """Persist the observation and updated target state for a failure."""
    finished = timezone.now()
    duration_ms = _duration_ms(started, finished)

    with transaction.atomic():
        Observation.objects.create(
            run=run,
            target=target,
            changed=False,
            previous_processed_text=target.last_processed_text,
            error_message=error,
            duration_ms=duration_ms,
        )

        target.last_run_at = finished
        target.last_status = Target.Status.FAILURE
        target.last_error_message = error
        target.last_duration_ms = duration_ms
        target.save(
            update_fields=[
                "last_run_at",
                "last_status",
                "last_error_message",
                "last_duration_ms",
                "updated_at",
            ]
        )


def is_changed(previous: str | None, current: str | None) -> bool:
    """Return True if the normalized values differ, treating None as missing."""
    if previous is None and current is None:
        return False
    if previous is None or current is None:
        return True

    return previous.strip() != current.strip()


def _duration_ms(started: datetime, finished: datetime) -> int:
    """Convert elapsed time to milliseconds."""
    return int((finished - started).total_seconds() * 1000)
