"""Create project_updates table

Revision ID: 021
Revises: 020
"""

from alembic import op
import sqlalchemy as sa

revision = "021"
down_revision = "020"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "project_updates",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("raw_content", sa.Text(), nullable=True),
        sa.Column("content_type", sa.String(), nullable=False, server_default="note"),
        sa.Column("is_processed", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("processed_at", sa.DateTime(), nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.text("now()")),
    )
    op.create_index("idx_project_updates_created", "project_updates", ["created_at"])
    op.create_index("idx_project_updates_processed", "project_updates", ["is_processed"])


def downgrade() -> None:
    op.drop_index("idx_project_updates_processed", table_name="project_updates")
    op.drop_index("idx_project_updates_created", table_name="project_updates")
    op.drop_table("project_updates")
