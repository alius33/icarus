"""Add transcript_notes and transcript_attachments tables

Revision ID: 017
Revises: 016
"""

from alembic import op
import sqlalchemy as sa

revision = "017"
down_revision = "016"


def upgrade():
    # Transcript notes (versioned)
    op.create_table(
        "transcript_notes",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "transcript_id",
            sa.Integer(),
            sa.ForeignKey("transcripts.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("version", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()),
    )
    op.create_index(
        "idx_transcript_notes_tid_version",
        "transcript_notes",
        ["transcript_id", "version"],
    )

    # Transcript attachments (with binary storage)
    op.create_table(
        "transcript_attachments",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "transcript_id",
            sa.Integer(),
            sa.ForeignKey("transcripts.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("original_filename", sa.String(), nullable=False),
        sa.Column("stored_filename", sa.String(), nullable=False),
        sa.Column("file_type", sa.String(), nullable=False),
        sa.Column("mime_type", sa.String(), nullable=False),
        sa.Column("size_bytes", sa.Integer(), nullable=False),
        sa.Column("file_data", sa.LargeBinary(), nullable=False),
        sa.Column("extracted_text", sa.Text(), nullable=True),
        sa.Column("storage_path", sa.String(), nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()),
    )
    op.create_index(
        "idx_transcript_attachments_tid",
        "transcript_attachments",
        ["transcript_id"],
    )


def downgrade():
    op.drop_index("idx_transcript_attachments_tid", table_name="transcript_attachments")
    op.drop_table("transcript_attachments")
    op.drop_index("idx_transcript_notes_tid_version", table_name="transcript_notes")
    op.drop_table("transcript_notes")
