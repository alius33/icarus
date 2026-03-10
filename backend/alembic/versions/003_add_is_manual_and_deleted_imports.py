"""add is_manual column and deleted_imports table

Revision ID: 003
Revises: 002
Create Date: 2026-03-09

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = '003'
down_revision: Union[str, None] = '002'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add is_manual column to 5 entity tables
    for table in ['decisions', 'action_items', 'open_threads', 'stakeholders', 'glossary_entries']:
        op.add_column(
            table,
            sa.Column('is_manual', sa.Boolean(), nullable=False, server_default=sa.text('false')),
        )

    # Create deleted_imports table for re-import suppression
    op.create_table(
        'deleted_imports',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('entity_type', sa.String(), nullable=False),
        sa.Column('unique_key', sa.String(), nullable=False),
        sa.Column('deleted_at', sa.DateTime(), server_default=sa.func.now()),
    )
    op.create_unique_constraint(
        'uq_deleted_imports_entity',
        'deleted_imports',
        ['entity_type', 'unique_key'],
    )


def downgrade() -> None:
    op.drop_table('deleted_imports')
    for table in ['decisions', 'action_items', 'open_threads', 'stakeholders', 'glossary_entries']:
        op.drop_column(table, 'is_manual')
