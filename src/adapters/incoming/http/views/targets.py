from __future__ import annotations

from flask import Blueprint, render_template
from flask.views import MethodView

from adapters.incoming.http.extensions import db
from adapters.outgoing.persistence.repositories.targets import TargetRepository

bp = Blueprint("targets", __name__)


class TargetListView(MethodView):
    """List and create targets."""

    def get(self):
        """Render the active targets page."""
        repo = TargetRepository(db.session)
        items = repo.list_active()
        return render_template("targets.html", targets=items)


bp.add_url_rule("/targets", view_func=TargetListView.as_view("list"))
