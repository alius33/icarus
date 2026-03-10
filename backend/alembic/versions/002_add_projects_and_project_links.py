"""add projects and project_links tables

Revision ID: 002
Revises: 001
Create Date: 2026-03-09

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = '002'
down_revision: Union[str, None] = '001'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Projects table
    op.create_table(
        'projects',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('description', sa.Text()),
        sa.Column('workstream_id', sa.Integer(), sa.ForeignKey('workstreams.id', ondelete='SET NULL'), nullable=True, unique=True),
        sa.Column('is_custom', sa.Boolean(), nullable=False, server_default=sa.text('false')),
        sa.Column('status', sa.String(), nullable=False, server_default='active'),
        sa.Column('color', sa.String(), nullable=True),
        sa.Column('icon', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.func.now()),
    )
    op.create_index('idx_projects_workstream', 'projects', ['workstream_id'])

    # Project links table
    op.create_table(
        'project_links',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('project_id', sa.Integer(), sa.ForeignKey('projects.id', ondelete='CASCADE'), nullable=False),
        sa.Column('entity_type', sa.String(), nullable=False),
        sa.Column('entity_id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now()),
    )
    op.create_index('idx_project_links_project', 'project_links', ['project_id'])
    op.create_index('idx_project_links_entity', 'project_links', ['entity_type', 'entity_id'])
    op.create_unique_constraint('uq_project_entity', 'project_links', ['project_id', 'entity_type', 'entity_id'])

    # Auto-seed projects from existing workstreams
    op.execute("""
        INSERT INTO projects (name, description, workstream_id, is_custom, status, created_at, updated_at)
        SELECT w.name, w.description, w.id, false, w.status, now(), now()
        FROM workstreams w
        ON CONFLICT DO NOTHING
    """)

    # Auto-populate decision links from existing workstream_id FK
    op.execute("""
        INSERT INTO project_links (project_id, entity_type, entity_id, created_at)
        SELECT p.id, 'decision', d.id, now()
        FROM decisions d
        JOIN projects p ON p.workstream_id = d.workstream_id
        WHERE d.workstream_id IS NOT NULL
        ON CONFLICT DO NOTHING
    """)


def downgrade() -> None:
    op.drop_table('project_links')
    op.drop_table('projects')
