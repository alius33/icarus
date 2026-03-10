"""Add analysis engine tables and slug to projects

Revision ID: 014
Revises: 013
"""

from alembic import op
import sqlalchemy as sa

revision = "014"
down_revision = "013"


def upgrade():
    # Add slug column to projects
    op.add_column("projects", sa.Column("slug", sa.String(), nullable=True))
    op.create_index("idx_projects_slug", "projects", ["slug"], unique=True)

    # Create topic_signals table
    op.create_table(
        "topic_signals",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("date", sa.Date(), nullable=True),
        sa.Column("topic", sa.String(), nullable=False),
        sa.Column("category", sa.String(), nullable=True),
        sa.Column("intensity", sa.String(), nullable=True),
        sa.Column("first_raised", sa.Date(), nullable=True),
        sa.Column("meetings_count", sa.Integer(), server_default="1"),
        sa.Column("trend", sa.String(), nullable=True),
        sa.Column("key_quote", sa.Text(), nullable=True),
        sa.Column("confidence", sa.String(), nullable=True),
        sa.Column(
            "transcript_id",
            sa.Integer(),
            sa.ForeignKey("transcripts.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column("is_manual", sa.Boolean(), server_default="false", nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
        ),
    )
    op.create_index("ix_topic_signals_id", "topic_signals", ["id"])
    op.create_index("ix_topic_signals_date", "topic_signals", ["date"])
    op.create_index("ix_topic_signals_topic", "topic_signals", ["topic"])

    # Create influence_signals table
    op.create_table(
        "influence_signals",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("date", sa.Date(), nullable=True),
        sa.Column("person", sa.String(), nullable=False),
        sa.Column("influence_type", sa.String(), nullable=False),
        sa.Column("direction", sa.String(), nullable=True),
        sa.Column("target_person", sa.String(), nullable=True),
        sa.Column("topic", sa.String(), nullable=True),
        sa.Column("evidence", sa.Text(), nullable=True),
        sa.Column("strength", sa.String(), nullable=True),
        sa.Column("confidence", sa.String(), nullable=True),
        sa.Column("coalition_name", sa.String(), nullable=True),
        sa.Column("coalition_members", sa.String(), nullable=True),
        sa.Column("alignment", sa.String(), nullable=True),
        sa.Column(
            "transcript_id",
            sa.Integer(),
            sa.ForeignKey("transcripts.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column("is_manual", sa.Boolean(), server_default="false", nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
        ),
    )
    op.create_index("ix_influence_signals_id", "influence_signals", ["id"])
    op.create_index("ix_influence_signals_date", "influence_signals", ["date"])
    op.create_index("ix_influence_signals_person", "influence_signals", ["person"])

    # Create contradictions table
    op.create_table(
        "contradictions",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("date", sa.Date(), nullable=True),
        sa.Column("contradiction_type", sa.String(), nullable=False),
        sa.Column("person", sa.String(), nullable=True),
        sa.Column("statement_a", sa.Text(), nullable=True),
        sa.Column("date_a", sa.Date(), nullable=True),
        sa.Column("statement_b", sa.Text(), nullable=True),
        sa.Column("date_b", sa.Date(), nullable=True),
        sa.Column("severity", sa.String(), nullable=True),
        sa.Column("resolution", sa.String(), server_default="unresolved"),
        sa.Column("confidence", sa.String(), nullable=True),
        sa.Column("gap_description", sa.Text(), nullable=True),
        sa.Column("expected_source", sa.String(), nullable=True),
        sa.Column("last_mentioned", sa.Date(), nullable=True),
        sa.Column("meetings_absent", sa.Integer(), nullable=True),
        sa.Column("entry_kind", sa.String(), server_default="contradiction", nullable=False),
        sa.Column(
            "transcript_id",
            sa.Integer(),
            sa.ForeignKey("transcripts.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column("is_manual", sa.Boolean(), server_default="false", nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
        ),
    )
    op.create_index("ix_contradictions_id", "contradictions", ["id"])
    op.create_index("ix_contradictions_date", "contradictions", ["date"])
    op.create_index("ix_contradictions_person", "contradictions", ["person"])

    # Create meeting_scores table
    op.create_table(
        "meeting_scores",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column(
            "transcript_id",
            sa.Integer(),
            sa.ForeignKey("transcripts.id", ondelete="CASCADE"),
            nullable=False,
            unique=True,
        ),
        sa.Column("date", sa.Date(), nullable=True),
        sa.Column("meeting_title", sa.String(), nullable=True),
        sa.Column("meeting_type", sa.String(), nullable=True),
        sa.Column("overall_score", sa.Integer(), nullable=False),
        sa.Column("decision_velocity", sa.Float(), nullable=True),
        sa.Column("action_clarity", sa.Float(), nullable=True),
        sa.Column("engagement_balance", sa.Float(), nullable=True),
        sa.Column("topic_completion", sa.Float(), nullable=True),
        sa.Column("follow_through", sa.Float(), nullable=True),
        sa.Column("participant_count", sa.Integer(), nullable=True),
        sa.Column("duration_category", sa.String(), nullable=True),
        sa.Column("recommendations", sa.Text(), nullable=True),
        sa.Column("is_manual", sa.Boolean(), server_default="false", nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
        ),
    )
    op.create_index("ix_meeting_scores_id", "meeting_scores", ["id"])
    op.create_index("ix_meeting_scores_date", "meeting_scores", ["date"])

    # Create risk_entries table
    op.create_table(
        "risk_entries",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("risk_id", sa.String(), nullable=False, unique=True),
        sa.Column("date", sa.Date(), nullable=True),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("category", sa.String(), nullable=True),
        sa.Column("severity", sa.String(), nullable=False),
        sa.Column("trajectory", sa.String(), nullable=True),
        sa.Column("source_type", sa.String(), nullable=True),
        sa.Column("owner", sa.String(), nullable=True),
        sa.Column("mitigation", sa.Text(), nullable=True),
        sa.Column("last_reviewed", sa.Date(), nullable=True),
        sa.Column("meetings_mentioned", sa.Integer(), server_default="1"),
        sa.Column("confidence", sa.String(), nullable=True),
        sa.Column(
            "transcript_id",
            sa.Integer(),
            sa.ForeignKey("transcripts.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column("is_manual", sa.Boolean(), server_default="false", nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
        ),
    )
    op.create_index("ix_risk_entries_id", "risk_entries", ["id"])
    op.create_index("ix_risk_entries_risk_id", "risk_entries", ["risk_id"])
    op.create_index("ix_risk_entries_date", "risk_entries", ["date"])

    # Create project_summaries table
    op.create_table(
        "project_summaries",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column(
            "project_id",
            sa.Integer(),
            sa.ForeignKey("projects.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "transcript_id",
            sa.Integer(),
            sa.ForeignKey("transcripts.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("date", sa.Date(), nullable=True),
        sa.Column("relevance", sa.String(), nullable=True),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("source_file", sa.String(), nullable=True),
        sa.Column("file_hash", sa.String(64), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
        ),
    )
    op.create_index("ix_project_summaries_id", "project_summaries", ["id"])
    op.create_index("ix_project_summaries_project_id", "project_summaries", ["project_id"])
    op.create_index("ix_project_summaries_date", "project_summaries", ["date"])


def downgrade():
    op.drop_table("project_summaries")
    op.drop_table("risk_entries")
    op.drop_table("meeting_scores")
    op.drop_table("contradictions")
    op.drop_table("influence_signals")
    op.drop_table("topic_signals")
    op.drop_index("idx_projects_slug", table_name="projects")
    op.drop_column("projects", "slug")
