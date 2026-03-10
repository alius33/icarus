"""add outreach, outreach_links, and division_profiles tables

Revision ID: 006
Revises: 005
Create Date: 2026-03-10

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = '006'
down_revision: Union[str, None] = '005'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Outreach contacts
    op.create_table(
        'outreach',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('contact_name', sa.String(), nullable=False),
        sa.Column('contact_role', sa.String(), nullable=True),
        sa.Column('division', sa.String(), nullable=True),
        sa.Column('status', sa.String(), nullable=False, server_default='initial_contact'),
        sa.Column('interest_level', sa.Integer(), server_default=sa.text('1')),
        sa.Column('first_contact_date', sa.Date(), nullable=True),
        sa.Column('last_contact_date', sa.Date(), nullable=True),
        sa.Column('meeting_count', sa.Integer(), server_default=sa.text('0')),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('next_step', sa.String(), nullable=True),
        sa.Column('next_step_date', sa.Date(), nullable=True),
        sa.Column('external_id', sa.String(), nullable=True),
        sa.Column('external_source', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.func.now()),
    )
    op.create_index('idx_outreach_status', 'outreach', ['status'])
    op.create_index('idx_outreach_division', 'outreach', ['division'])

    # Outreach-to-Transcript links
    op.create_table(
        'outreach_links',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('outreach_id', sa.Integer(), sa.ForeignKey('outreach.id', ondelete='CASCADE'), nullable=False),
        sa.Column('transcript_id', sa.Integer(), sa.ForeignKey('transcripts.id', ondelete='CASCADE'), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now()),
    )
    op.create_index('idx_outreach_links_outreach', 'outreach_links', ['outreach_id'])
    op.create_index('idx_outreach_links_transcript', 'outreach_links', ['transcript_id'])
    op.create_unique_constraint('uq_outreach_transcript', 'outreach_links', ['outreach_id', 'transcript_id'])

    # Division Profiles
    op.create_table(
        'division_profiles',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(), nullable=False, unique=True),
        sa.Column('status', sa.String(), nullable=False, server_default='not_engaged'),
        sa.Column('current_tools', sa.Text(), nullable=True),
        sa.Column('pain_points', sa.Text(), nullable=True),
        sa.Column('key_contact', sa.String(), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.func.now()),
    )
    op.create_index('idx_division_status', 'division_profiles', ['status'])


def downgrade() -> None:
    op.drop_table('division_profiles')
    op.drop_table('outreach_links')
    op.drop_table('outreach')
