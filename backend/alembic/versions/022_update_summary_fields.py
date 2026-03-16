"""Add summary to project_updates, make transcript_id nullable on project_summaries,
add project_update_id to project_summaries, add source_update_id to weekly_plan_actions.

Revision ID: 022
Revises: 021
"""

from alembic import op
import sqlalchemy as sa

revision = "022"
down_revision = "021"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # 1. Add summary column to project_updates
    op.add_column("project_updates", sa.Column("summary", sa.Text(), nullable=True))

    # 2. Make transcript_id nullable on project_summaries and add project_update_id
    op.alter_column(
        "project_summaries",
        "transcript_id",
        existing_type=sa.Integer(),
        nullable=True,
    )
    op.add_column(
        "project_summaries",
        sa.Column(
            "project_update_id",
            sa.Integer(),
            sa.ForeignKey("project_updates.id", ondelete="CASCADE"),
            nullable=True,
        ),
    )
    op.create_index(
        "idx_project_summaries_update",
        "project_summaries",
        ["project_update_id"],
    )

    # 3. Add source_update_id to weekly_plan_actions
    op.add_column(
        "weekly_plan_actions",
        sa.Column(
            "source_update_id",
            sa.Integer(),
            sa.ForeignKey("project_updates.id", ondelete="SET NULL"),
            nullable=True,
        ),
    )


def downgrade() -> None:
    op.drop_column("weekly_plan_actions", "source_update_id")
    op.drop_index("idx_project_summaries_update", table_name="project_summaries")
    op.drop_column("project_summaries", "project_update_id")
    op.alter_column(
        "project_summaries",
        "transcript_id",
        existing_type=sa.Integer(),
        nullable=False,
    )
    op.drop_column("project_updates", "summary")
