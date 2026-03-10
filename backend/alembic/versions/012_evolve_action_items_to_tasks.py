"""Evolve action_items table to tasks with PM fields

Revision ID: 012
Revises: 011
Create Date: 2026-03-10

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import ARRAY

revision: str = '012'
down_revision: Union[str, None] = '011'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Add new columns to action_items BEFORE renaming
    op.add_column('action_items', sa.Column('title', sa.String(), nullable=True))
    op.add_column('action_items', sa.Column('identifier', sa.String(), nullable=True))
    op.add_column('action_items', sa.Column('priority', sa.String(), server_default='NONE', nullable=False))
    op.add_column('action_items', sa.Column('labels', ARRAY(sa.String()), server_default='{}', nullable=False))
    op.add_column('action_items', sa.Column('start_date', sa.Date(), nullable=True))
    op.add_column('action_items', sa.Column('due_date', sa.Date(), nullable=True))
    op.add_column('action_items', sa.Column('estimate', sa.Integer(), nullable=True))
    op.add_column('action_items', sa.Column('position', sa.Integer(), server_default='0', nullable=False))
    op.add_column('action_items', sa.Column('project_id', sa.Integer(), nullable=True))
    op.add_column('action_items', sa.Column('parent_id', sa.Integer(), nullable=True))
    op.add_column('action_items', sa.Column('created_date', sa.Date(), nullable=True))
    op.add_column('action_items', sa.Column('assignee', sa.String(), nullable=True))

    # 2. Populate title from description (first sentence or 200 chars)
    op.execute("""
        UPDATE action_items SET title = CASE
            WHEN position('.' in description) > 0 AND position('.' in description) <= 200
            THEN left(description, position('.' in description) - 1)
            ELSE left(description, 200)
        END
    """)
    # Make title NOT NULL now that it's populated
    op.alter_column('action_items', 'title', nullable=False)

    # 3. Copy owner → assignee, action_date → created_date
    op.execute("UPDATE action_items SET assignee = owner")
    op.execute("UPDATE action_items SET created_date = action_date")

    # 4. Parse deadline string → due_date where possible
    op.execute("""
        UPDATE action_items SET due_date = deadline::date
        WHERE deadline IS NOT NULL AND deadline ~ '^\\d{4}-\\d{2}-\\d{2}$'
    """)

    # 5. Map statuses
    op.execute("""
        UPDATE action_items SET status = CASE
            WHEN status = 'OPEN' THEN 'TODO'
            WHEN status = 'IN PROGRESS' THEN 'IN_PROGRESS'
            WHEN status = 'COMPLETED' THEN 'DONE'
            WHEN status = 'BLOCKED' THEN 'BACKLOG'
            WHEN status = 'LIKELY_COMPLETED' THEN 'IN_REVIEW'
            WHEN status = 'LIKELY COMPLETED' THEN 'IN_REVIEW'
            ELSE status
        END
    """)

    # 6. Populate project_id from project_links
    op.execute("""
        UPDATE action_items ai SET project_id = (
            SELECT pl.project_id FROM project_links pl
            WHERE pl.entity_type = 'action_item' AND pl.entity_id = ai.id
            LIMIT 1
        )
    """)

    # 7. Generate identifiers
    op.execute("""
        WITH numbered AS (
            SELECT ai.id,
                   COALESCE(
                       (SELECT upper(replace(left(p.name, 5), ' ', ''))
                        FROM projects p WHERE p.id = ai.project_id),
                       'TASK'
                   ) AS prefix,
                   ROW_NUMBER() OVER (
                       PARTITION BY COALESCE(ai.project_id, 0)
                       ORDER BY ai.action_date NULLS LAST, ai.id
                   ) AS seq
            FROM action_items ai
        )
        UPDATE action_items SET identifier = numbered.prefix || '-' || numbered.seq
        FROM numbered WHERE action_items.id = numbered.id
    """)
    # Make identifier NOT NULL + unique
    op.alter_column('action_items', 'identifier', nullable=False)

    # 8. Set positions within status groups
    op.execute("""
        WITH positioned AS (
            SELECT id,
                   ROW_NUMBER() OVER (
                       PARTITION BY status ORDER BY action_date NULLS LAST, id
                   ) * 1000 AS pos
            FROM action_items
        )
        UPDATE action_items SET position = positioned.pos
        FROM positioned WHERE action_items.id = positioned.id
    """)

    # 9. Rename the table
    op.rename_table('action_items', 'tasks')

    # 10. Add foreign keys
    op.create_foreign_key(
        'fk_tasks_project', 'tasks', 'projects',
        ['project_id'], ['id'], ondelete='SET NULL'
    )
    op.create_foreign_key(
        'fk_tasks_parent', 'tasks', 'tasks',
        ['parent_id'], ['id'], ondelete='SET NULL'
    )

    # 11. Drop old indexes and create new ones
    op.drop_index('idx_actions_status', table_name='tasks')
    op.drop_index('idx_actions_owner', table_name='tasks')
    op.drop_index('idx_actions_search', table_name='tasks')

    op.create_index('idx_tasks_status', 'tasks', ['status'])
    op.create_index('idx_tasks_assignee', 'tasks', ['assignee'])
    op.create_index('idx_tasks_priority', 'tasks', ['priority'])
    op.create_index('idx_tasks_project', 'tasks', ['project_id'])
    op.create_index('idx_tasks_parent', 'tasks', ['parent_id'])
    op.create_index('idx_tasks_identifier', 'tasks', ['identifier'], unique=True)
    op.create_index('idx_tasks_search', 'tasks', ['search_vector'], postgresql_using='gin')

    # 12. Update project_links entity_type
    op.execute("UPDATE project_links SET entity_type = 'task' WHERE entity_type = 'action_item'")

    # 13. Update deleted_imports entity_type
    op.execute("UPDATE deleted_imports SET entity_type = 'task' WHERE entity_type = 'action_item'")


def downgrade() -> None:
    # Reverse entity_type updates
    op.execute("UPDATE project_links SET entity_type = 'action_item' WHERE entity_type = 'task'")
    op.execute("UPDATE deleted_imports SET entity_type = 'action_item' WHERE entity_type = 'task'")

    # Drop new indexes
    op.drop_index('idx_tasks_search', table_name='tasks')
    op.drop_index('idx_tasks_identifier', table_name='tasks')
    op.drop_index('idx_tasks_parent', table_name='tasks')
    op.drop_index('idx_tasks_project', table_name='tasks')
    op.drop_index('idx_tasks_priority', table_name='tasks')
    op.drop_index('idx_tasks_assignee', table_name='tasks')
    op.drop_index('idx_tasks_status', table_name='tasks')

    # Drop foreign keys
    op.drop_constraint('fk_tasks_parent', 'tasks', type_='foreignkey')
    op.drop_constraint('fk_tasks_project', 'tasks', type_='foreignkey')

    # Rename table back
    op.rename_table('tasks', 'action_items')

    # Restore old indexes
    op.create_index('idx_actions_status', 'action_items', ['status'])
    op.create_index('idx_actions_owner', 'action_items', ['owner'])
    op.create_index('idx_actions_search', 'action_items', ['search_vector'], postgresql_using='gin')

    # Reverse status mapping
    op.execute("""
        UPDATE action_items SET status = CASE
            WHEN status = 'TODO' THEN 'OPEN'
            WHEN status = 'IN_PROGRESS' THEN 'IN PROGRESS'
            WHEN status = 'DONE' THEN 'COMPLETED'
            WHEN status = 'BACKLOG' THEN 'OPEN'
            WHEN status = 'IN_REVIEW' THEN 'LIKELY_COMPLETED'
            WHEN status = 'CANCELLED' THEN 'COMPLETED'
            ELSE status
        END
    """)

    # Copy assignee back to owner
    op.execute("UPDATE action_items SET owner = assignee")

    # Drop new columns
    op.drop_column('action_items', 'assignee')
    op.drop_column('action_items', 'created_date')
    op.drop_column('action_items', 'parent_id')
    op.drop_column('action_items', 'project_id')
    op.drop_column('action_items', 'position')
    op.drop_column('action_items', 'estimate')
    op.drop_column('action_items', 'due_date')
    op.drop_column('action_items', 'start_date')
    op.drop_column('action_items', 'labels')
    op.drop_column('action_items', 'priority')
    op.drop_column('action_items', 'identifier')
    op.drop_column('action_items', 'title')
