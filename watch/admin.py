"""Admin registrations — full CRUD for targets, read-mostly for results."""

from __future__ import annotations

from django.contrib import admin

from watch.models import Observation, Run, Target


@admin.register(Target)
class TargetAdmin(admin.ModelAdmin[Target]):
    """Manage watch targets."""

    list_display = (
        "name",
        "url",
        "selector_type",
        "selector",
        "processor_type",
        "active",
        "last_run_at",
        "last_status",
        "last_duration_ms",
    )
    list_filter = ("active", "selector_type", "processor_type", "last_status")
    search_fields = ("name", "url", "selector")
    readonly_fields = (
        "last_run_at",
        "last_status",
        "last_raw_text",
        "last_processed_text",
        "last_error_message",
        "last_duration_ms",
        "created_at",
        "updated_at",
    )


@admin.register(Run)
class RunAdmin(admin.ModelAdmin[Run]):
    """Inspect watch runs."""

    list_display = ("id", "started_at", "finished_at", "status", "error_summary")
    list_filter = ("status",)


@admin.register(Observation)
class ObservationAdmin(admin.ModelAdmin[Observation]):
    """Inspect observations."""

    list_display = (
        "id",
        "run",
        "target",
        "observed_at",
        "changed",
        "processed_text",
        "error_message",
        "duration_ms",
    )
    list_filter = ("changed", "target")
    list_select_related = ("run", "target")
