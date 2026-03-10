"""Add primary_project_id to transcripts

Revision ID: 015
Revises: 014
"""

from alembic import op
import sqlalchemy as sa

revision = "015"
down_revision = "014"


def upgrade():
    op.add_column(
        "transcripts",
        sa.Column(
            "primary_project_id",
            sa.Integer(),
            sa.ForeignKey("projects.id", ondelete="SET NULL"),
            nullable=True,
        ),
    )
    op.create_index(
        "idx_transcripts_primary_project",
        "transcripts",
        ["primary_project_id"],
    )


def downgrade():
    op.drop_index("idx_transcripts_primary_project", table_name="transcripts")
    op.drop_column("transcripts", "primary_project_id")
