from __future__ import annotations

from flask import Flask, render_template

from domain.exceptions import AppError, TargetNotFoundError


def register_error_handlers(app: Flask) -> None:
    """Attach error handlers to the Flask application."""

    @app.errorhandler(404)
    def not_found(_error: Exception):
        return render_template("errors/404.html"), 404

    @app.errorhandler(500)
    def server_error(_error: Exception):
        return render_template("errors/500.html"), 500

    @app.errorhandler(TargetNotFoundError)
    def target_not_found(error: TargetNotFoundError):
        return render_template("errors/404.html", message=str(error)), 404

    @app.errorhandler(AppError)
    def watcher_error(error: AppError):
        return render_template("errors/500.html", message=str(error)), 500
