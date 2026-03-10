"""add sentiment_signals and commitments tables

Revision ID: 008
Revises: 007
Create Date: 2026-03-10

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = '008'
down_revision: Union[str, None] = '007'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'sentiment_signals',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('stakeholder_id', sa.Integer(), sa.ForeignKey('stakeholders.id', ondelete='CASCADE'), nullable=False),
        sa.Column('transcript_id', sa.Integer(), sa.ForeignKey('transcripts.id', ondelete='SET NULL'), nullable=True),
        sa.Column('date', sa.Date(), nullable=True),
        sa.Column('sentiment', sa.String(), nullable=False),
        sa.Column('shift', sa.String(), nullable=True),
        sa.Column('topic', sa.String(), nullable=True),
        sa.Column('quote', sa.Text(), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('is_manual', sa.Boolean(), server_default=sa.text('false'), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index('idx_sentiment_stakeholder', 'sentiment_signals', ['stakeholder_id'])
    op.create_index('idx_sentiment_date', 'sentiment_signals', ['date'])

    op.create_table(
        'commitments',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('person', sa.String(), nullable=False),
        sa.Column('commitment', sa.Text(), nullable=False),
        sa.Column('transcript_id', sa.Integer(), sa.ForeignKey('transcripts.id', ondelete='SET NULL'), nullable=True),
        sa.Column('date_made', sa.Date(), nullable=True),
        sa.Column('deadline_text', sa.String(), nullable=True),
        sa.Column('deadline_resolved', sa.Date(), nullable=True),
        sa.Column('deadline_type', sa.String(), nullable=True),
        sa.Column('condition', sa.String(), nullable=True),
        sa.Column('linked_action_id', sa.Integer(), sa.ForeignKey('action_items.id', ondelete='SET NULL'), nullable=True),
        sa.Column('status', sa.String(), nullable=False, server_default='pending'),
        sa.Column('verified_date', sa.Date(), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('is_manual', sa.Boolean(), server_default=sa.text('false'), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index('idx_commitment_person', 'commitments', ['person'])
    op.create_index('idx_commitment_status', 'commitments', ['status'])
    op.create_index('idx_commitment_date', 'commitments', ['date_made'])


def downgrade() -> None:
    op.drop_table('commitments')
    op.drop_table('sentiment_signals')
