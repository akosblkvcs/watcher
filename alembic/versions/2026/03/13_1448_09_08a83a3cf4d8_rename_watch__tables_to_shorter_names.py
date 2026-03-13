"""Rename watch_ tables to shorter names.

Revision ID: 08a83a3cf4d8
Revises: 18caeaa1db36
Create Date: 2026-03-13 14:48:09.478144
"""

from collections.abc import Sequence

from alembic import op

# Revision identifiers, used by Alembic.
revision: str = "08a83a3cf4d8"
down_revision: str | Sequence[str] | None = "18caeaa1db36"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Rename watch_* tables and their indexes."""
    # Drop old indexes (they reference old table names)
    op.drop_index("ix_watch_observations_run_id", table_name="watch_observations")
    op.drop_index("ix_watch_observations_target_id", table_name="watch_observations")

    # Rename tables
    op.rename_table("watch_runs", "runs")
    op.rename_table("watch_targets", "targets")
    op.rename_table("watch_observations", "observations")

    # Recreate indexes with new names
    op.create_index("ix_observations_run_id", "observations", ["run_id"])
    op.create_index("ix_observations_target_id", "observations", ["target_id"])


def downgrade() -> None:
    """Revert table renames."""
    op.drop_index("ix_observations_run_id", table_name="observations")
    op.drop_index("ix_observations_target_id", table_name="observations")

    op.rename_table("observations", "watch_observations")
    op.rename_table("targets", "watch_targets")
    op.rename_table("runs", "watch_runs")

    op.create_index("ix_watch_observations_run_id", "watch_observations", ["run_id"])
    op.create_index("ix_watch_observations_target_id", "watch_observations", ["target_id"])
