"""Add source_transcript_id and context to weekly_plan_actions

Revision ID: 020
Revises: 019
"""

from alembic import op
import sqlalchemy as sa

revision = "020"
down_revision = "019"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "weekly_plan_actions",
        sa.Column(
            "source_transcript_id",
            sa.Integer(),
            sa.ForeignKey("transcripts.id", ondelete="SET NULL"),
            nullable=True,
        ),
    )
    op.add_column(
        "weekly_plan_actions",
        sa.Column("context", sa.Text(), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("weekly_plan_actions", "context")
    op.drop_column("weekly_plan_actions", "source_transcript_id")
