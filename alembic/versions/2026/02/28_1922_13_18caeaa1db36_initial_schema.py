"""Initial schema.

Revision ID: 18caeaa1db36
Revises:
Create Date: 2026-02-28 19:22:13.733397
"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# Revision identifiers used by Alembic.
revision: str = "18caeaa1db36"
down_revision: str | Sequence[str] | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "watch_runs",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column(
            "started_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("finished_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("status", sa.String(length=20), nullable=False),
        sa.Column("error_summary", sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "watch_targets",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(length=200), nullable=False),
        sa.Column("url", sa.Text(), nullable=False),
        sa.Column("selector_type", sa.String(length=10), server_default="css", nullable=False),
        sa.Column("selector", sa.Text(), nullable=False),
        sa.Column(
            "processor_type", sa.String(length=50), server_default="raw_text", nullable=False
        ),
        sa.Column("processor_config", sa.JSON(), nullable=True),
        sa.Column("last_run_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("last_status", sa.String(length=20), nullable=True),
        sa.Column("last_raw_text", sa.Text(), nullable=True),
        sa.Column("last_processed_text", sa.Text(), nullable=True),
        sa.Column("last_error_message", sa.Text(), nullable=True),
        sa.Column("last_duration_ms", sa.Integer(), nullable=True),
        sa.Column("active", sa.Boolean(), server_default="true", nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "watch_observations",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("run_id", sa.Integer(), nullable=False),
        sa.Column("target_id", sa.Integer(), nullable=False),
        sa.Column(
            "observed_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("raw_text", sa.Text(), nullable=True),
        sa.Column("processed_text", sa.Text(), nullable=True),
        sa.Column("changed", sa.Boolean(), server_default="false", nullable=False),
        sa.Column("previous_processed_text", sa.Text(), nullable=True),
        sa.Column("error_message", sa.Text(), nullable=True),
        sa.Column("duration_ms", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(["run_id"], ["watch_runs.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["target_id"], ["watch_targets.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_watch_observations_run_id"), "watch_observations", ["run_id"], unique=False
    )
    op.create_index(
        op.f("ix_watch_observations_target_id"), "watch_observations", ["target_id"], unique=False
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f("ix_watch_observations_target_id"), table_name="watch_observations")
    op.drop_index(op.f("ix_watch_observations_run_id"), table_name="watch_observations")
    op.drop_table("watch_observations")
    op.drop_table("watch_targets")
    op.drop_table("watch_runs")
