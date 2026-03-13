from __future__ import annotations

from flask import Blueprint, render_template
from flask.views import MethodView

bp = Blueprint("home", __name__)


class HomeView(MethodView):
    """Dashboard landing page."""

    def get(self) -> str:
        """Render the dashboard."""
        return render_template("home.html")


bp.add_url_rule("/", view_func=HomeView.as_view("index"))
