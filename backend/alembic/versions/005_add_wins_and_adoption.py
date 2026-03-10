"""add programme_wins and adoption_metrics tables

Revision ID: 005
Revises: 004
Create Date: 2026-03-10

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = '005'
down_revision: Union[str, None] = '004'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Programme Wins
    op.create_table(
        'programme_wins',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('category', sa.String(), nullable=False),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('before_state', sa.String(), nullable=True),
        sa.Column('after_state', sa.String(), nullable=True),
        sa.Column('workstream', sa.String(), nullable=True),
        sa.Column('confidence', sa.String(), nullable=False, server_default='estimated'),
        sa.Column('date_recorded', sa.Date(), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('is_manual', sa.Boolean(), nullable=False, server_default=sa.text('true')),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.func.now()),
    )
    op.create_index('idx_wins_category', 'programme_wins', ['category'])
    op.create_index('idx_wins_confidence', 'programme_wins', ['confidence'])

    # Adoption Metrics
    op.create_table(
        'adoption_metrics',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('date', sa.Date(), nullable=False),
        sa.Column('metric_type', sa.String(), nullable=False),
        sa.Column('value', sa.Integer(), nullable=False),
        sa.Column('workstream', sa.String(), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now()),
    )
    op.create_index('idx_adoption_date', 'adoption_metrics', ['date'])
    op.create_index('idx_adoption_metric_type', 'adoption_metrics', ['metric_type'])


def downgrade() -> None:
    op.drop_table('adoption_metrics')
    op.drop_table('programme_wins')
