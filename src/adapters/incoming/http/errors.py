"""Flask error handlers for domain and HTTP exceptions."""

# pyright: reportUnusedFunction=false

from __future__ import annotations

import logging

from flask import Flask, render_template, request

from domain.exceptions import AppError, TargetNotFoundError

log = logging.getLogger(__name__)


def register_error_handlers(app: Flask) -> None:
    """Attach error handlers to the Flask application."""

    @app.errorhandler(404)
    def not_found(error: Exception) -> tuple[str, int]:
        log.warning(
            "HTTP 404: path=%s method=%s error=%s",
            request.path,
            request.method,
            error,
        )
        return render_template("errors/404.html"), 404

    @app.errorhandler(500)
    def server_error(error: Exception) -> tuple[str, int]:
        log.exception(
            "HTTP 500: path=%s method=%s",
            request.path,
            request.method,
        )
        return render_template("errors/500.html"), 500

    @app.errorhandler(TargetNotFoundError)
    def target_not_found(error: TargetNotFoundError) -> tuple[str, int]:
        log.warning(
            "Target not found: path=%s method=%s error=%s",
            request.path,
            request.method,
            error,
        )
        return render_template("errors/404.html"), 404

    @app.errorhandler(AppError)
    def watcher_error(error: AppError) -> tuple[str, int]:
        log.exception(
            "Application error: path=%s method=%s",
            request.path,
            request.method,
        )
        return render_template("errors/500.html"), 500