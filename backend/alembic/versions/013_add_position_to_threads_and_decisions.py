"""Add position column to open_threads and decisions for board ordering

Revision ID: 013
Revises: 012
"""

from alembic import op
import sqlalchemy as sa

revision = "013"
down_revision = "012"


def upgrade():
    # Add position column to open_threads
    op.add_column("open_threads", sa.Column("position", sa.Integer(), server_default="0", nullable=False))
    op.create_index("idx_threads_position", "open_threads", ["position"])

    # Populate position from row ordering within each status group
    op.execute("""
        UPDATE open_threads SET position = sub.pos FROM (
            SELECT id, (ROW_NUMBER() OVER (PARTITION BY status ORDER BY number)) * 1000 AS pos
            FROM open_threads
        ) sub WHERE open_threads.id = sub.id
    """)

    # Add position column to decisions
    op.add_column("decisions", sa.Column("position", sa.Integer(), server_default="0", nullable=False))
    op.create_index("idx_decisions_position", "decisions", ["position"])

    # Populate position from row ordering within each execution_status group
    op.execute("""
        UPDATE decisions SET position = sub.pos FROM (
            SELECT id, (ROW_NUMBER() OVER (
                PARTITION BY COALESCE(execution_status, 'made')
                ORDER BY decision_date NULLS LAST, number
            )) * 1000 AS pos
            FROM decisions
        ) sub WHERE decisions.id = sub.id
    """)


def downgrade():
    op.drop_index("idx_decisions_position", table_name="decisions")
    op.drop_column("decisions", "position")
    op.drop_index("idx_threads_position", table_name="open_threads")
    op.drop_column("open_threads", "position")
