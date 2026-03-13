from __future__ import annotations

from flask import Blueprint, render_template
from flask.views import MethodView

from adapters.incoming.http.extensions import db
from adapters.outgoing.persistence.repositories.observations import ObservationRepository

bp = Blueprint("observations", __name__)


class ObservationListView(MethodView):
    """List recent observations."""

    def get(self):
        """Render the most recent observations page."""
        repo = ObservationRepository(db.session)
        items = repo.list_recent(limit=10)
        return render_template("observations.html", observations=items)


bp.add_url_rule("/observations", view_func=ObservationListView.as_view("list"))
