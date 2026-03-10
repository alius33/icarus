"""add programme intelligence tables and fields

Revision ID: 004
Revises: 003
Create Date: 2026-03-09

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSON

revision: str = '004'
down_revision: Union[str, None] = '003'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # --- New columns on existing tables ---

    # OpenThread: severity + trend for risk register
    op.add_column('open_threads', sa.Column('severity', sa.String(), nullable=True))
    op.add_column('open_threads', sa.Column('trend', sa.String(), nullable=True))

    # Workstream: blocker_reason + assigned_fte for health dashboard
    op.add_column('workstreams', sa.Column('blocker_reason', sa.Text(), nullable=True))
    op.add_column('workstreams', sa.Column('assigned_fte', sa.String(), nullable=True))

    # Stakeholder: risk_level + morale_notes for flight risk tracking
    op.add_column('stakeholders', sa.Column('risk_level', sa.String(), nullable=True))
    op.add_column('stakeholders', sa.Column('morale_notes', sa.Text(), nullable=True))

    # --- New tables ---

    # Dependencies / Integration Queue
    op.create_table(
        'dependencies',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('dependency_type', sa.String(), nullable=False, server_default='integration'),
        sa.Column('status', sa.String(), nullable=False, server_default='pending'),
        sa.Column('blocking_reason', sa.Text(), nullable=True),
        sa.Column('estimated_effort', sa.String(), nullable=True),
        sa.Column('assigned_to', sa.String(), nullable=True),
        sa.Column('affected_workstreams', sa.Text(), nullable=True),
        sa.Column('priority', sa.String(), server_default='MEDIUM'),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.func.now()),
    )
    op.create_index('idx_dependencies_status', 'dependencies', ['status'])
    op.create_index('idx_dependencies_priority', 'dependencies', ['priority'])

    # Resource Allocations
    op.create_table(
        'resource_allocations',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('person_name', sa.String(), nullable=False),
        sa.Column('role', sa.String(), nullable=True),
        sa.Column('allocations', JSON(), server_default='[]'),
        sa.Column('capacity_status', sa.String(), server_default='available'),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('start_date', sa.String(), nullable=True),
        sa.Column('end_date', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.func.now()),
    )
    op.create_index('idx_resources_capacity', 'resource_allocations', ['capacity_status'])

    # Scope Items
    op.create_table(
        'scope_items',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('scope_type', sa.String(), nullable=False, server_default='addition'),
        sa.Column('workstream', sa.String(), nullable=True),
        sa.Column('added_date', sa.String(), nullable=True),
        sa.Column('estimated_effort', sa.String(), nullable=True),
        sa.Column('budgeted', sa.Boolean(), server_default=sa.text('false')),
        sa.Column('status', sa.String(), server_default='planned'),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('impact_notes', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.func.now()),
    )
    op.create_index('idx_scope_type', 'scope_items', ['scope_type'])
    op.create_index('idx_scope_status', 'scope_items', ['status'])


def downgrade() -> None:
    op.drop_table('scope_items')
    op.drop_table('resource_allocations')
    op.drop_table('dependencies')
    op.drop_column('stakeholders', 'morale_notes')
    op.drop_column('stakeholders', 'risk_level')
    op.drop_column('workstreams', 'assigned_fte')
    op.drop_column('workstreams', 'blocker_reason')
    op.drop_column('open_threads', 'trend')
    op.drop_column('open_threads', 'severity')
