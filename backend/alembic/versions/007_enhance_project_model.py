"""enhance project model with keywords, division, last_analysed_date

Revision ID: 007
Revises: 006
Create Date: 2026-03-10

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = '007'
down_revision: Union[str, None] = '006'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('projects', sa.Column('keywords', sa.Text(), nullable=True))
    op.add_column('projects', sa.Column('division', sa.String(), nullable=True))
    op.add_column('projects', sa.Column('last_analysed_date', sa.Date(), nullable=True))


def downgrade() -> None:
    op.drop_column('projects', 'last_analysed_date')
    op.drop_column('projects', 'division')
    op.drop_column('projects', 'keywords')
