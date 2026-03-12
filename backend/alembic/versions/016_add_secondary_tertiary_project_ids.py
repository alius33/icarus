"""Add secondary_project_id and tertiary_project_id to transcripts

Revision ID: 016
Revises: 015
"""

from alembic import op
import sqlalchemy as sa

revision = "016"
down_revision = "015"


def upgrade():
    op.add_column(
        "transcripts",
        sa.Column(
            "secondary_project_id",
            sa.Integer(),
            sa.ForeignKey("projects.id", ondelete="SET NULL"),
            nullable=True,
        ),
    )
    op.add_column(
        "transcripts",
        sa.Column(
            "tertiary_project_id",
            sa.Integer(),
            sa.ForeignKey("projects.id", ondelete="SET NULL"),
            nullable=True,
        ),
    )
    op.create_index(
        "idx_transcripts_secondary_project",
        "transcripts",
        ["secondary_project_id"],
    )
    op.create_index(
        "idx_transcripts_tertiary_project",
        "transcripts",
        ["tertiary_project_id"],
    )


def downgrade():
    op.drop_index("idx_transcripts_tertiary_project", table_name="transcripts")
    op.drop_index("idx_transcripts_secondary_project", table_name="transcripts")
    op.drop_column("transcripts", "tertiary_project_id")
    op.drop_column("transcripts", "secondary_project_id")
