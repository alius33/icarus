"""add execution_status to decisions table

Revision ID: 010
Revises: 009
Create Date: 2026-03-10

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = '010'
down_revision: Union[str, None] = '009'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        'decisions',
        sa.Column('execution_status', sa.String(), server_default='made', nullable=True),
    )


def downgrade() -> None:
    op.drop_column('decisions', 'execution_status')
