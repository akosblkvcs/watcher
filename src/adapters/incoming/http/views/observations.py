from __future__ import annotations

from collections.abc import Callable
from typing import Any

from flask import Blueprint, render_template
from flask.views import MethodView
from sqlalchemy.orm import Session
from sqlalchemy.orm.scoping import scoped_session

from adapters.incoming.http.extensions import db
from domain.repositories import ObservationRepo

type ObservationRepoFactory = Callable[[Session | scoped_session[Any]], ObservationRepo]


class ObservationListView(MethodView):
    """List recent observations."""

    init_every_request = False

    def __init__(self, repo_factory: ObservationRepoFactory) -> None:
        """Accept a repository factory to create a repository for the current session."""
        self._repo_factory = repo_factory

    def get(self) -> str:
        """Render the most recent observations page."""
        repo = self._repo_factory(db.session)
        items = repo.list_recent(limit=10)
        return render_template("observations.html", observations=items)


def create_blueprint(repo_factory: ObservationRepoFactory) -> Blueprint:
    """Create the observations blueprint with injected dependencies."""
    bp = Blueprint("observations", __name__)
    bp.add_url_rule(
        "/observations",
        view_func=ObservationListView.as_view(
            "list",
            repo_factory=repo_factory,
        ),
    )
    return bp
