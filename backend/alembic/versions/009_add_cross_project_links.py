"""add cross_project_links table

Revision ID: 009
Revises: 008
Create Date: 2026-03-10

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = '009'
down_revision: Union[str, None] = '008'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'cross_project_links',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('source_project_id', sa.Integer(), sa.ForeignKey('projects.id', ondelete='CASCADE'), nullable=False),
        sa.Column('target_project_id', sa.Integer(), sa.ForeignKey('projects.id', ondelete='CASCADE'), nullable=False),
        sa.Column('link_type', sa.String(), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('transcript_id', sa.Integer(), sa.ForeignKey('transcripts.id', ondelete='SET NULL'), nullable=True),
        sa.Column('date_detected', sa.Date(), nullable=True),
        sa.Column('severity', sa.String(), nullable=False, server_default='info'),
        sa.Column('status', sa.String(), nullable=False, server_default='active'),
        sa.Column('is_manual', sa.Boolean(), server_default=sa.text('false'), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index('idx_cross_link_source', 'cross_project_links', ['source_project_id'])
    op.create_index('idx_cross_link_target', 'cross_project_links', ['target_project_id'])
    op.create_unique_constraint(
        'uq_cross_project_link',
        'cross_project_links',
        ['source_project_id', 'target_project_id', 'link_type'],
    )


def downgrade() -> None:
    op.drop_table('cross_project_links')
