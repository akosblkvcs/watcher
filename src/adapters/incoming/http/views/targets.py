from __future__ import annotations

from collections.abc import Callable
from typing import Any

from flask import Blueprint, render_template
from flask.views import MethodView
from sqlalchemy.orm import Session
from sqlalchemy.orm.scoping import scoped_session

from adapters.incoming.http.extensions import db
from domain.repositories import TargetRepo

type TargetRepoFactory = Callable[[Session | scoped_session[Any]], TargetRepo]


class TargetListView(MethodView):
    """List active targets."""

    init_every_request = False

    def __init__(self, repo_factory: TargetRepoFactory) -> None:
        """Accept a repository factory to create a repository for the current session."""
        self._repo_factory = repo_factory

    def get(self) -> str:
        """Render the active targets page."""
        repo = self._repo_factory(db.session)
        items = repo.list_active()
        return render_template("targets.html", targets=items)


def create_blueprint(repo_factory: TargetRepoFactory) -> Blueprint:
    """Create the targets blueprint with injected dependencies."""
    bp = Blueprint("targets", __name__)
    bp.add_url_rule(
        "/targets",
        view_func=TargetListView.as_view(
            "list",
            repo_factory=repo_factory,
        ),
    )
    return bp
