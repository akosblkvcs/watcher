from __future__ import annotations

from django.apps import AppConfig


class WatchConfig(AppConfig):
    """App configuration for the watch app."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "watch"
