"""initial schema

Revision ID: 001
Revises:
Create Date: 2026-03-09

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '001'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Transcripts
    op.create_table(
        'transcripts',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('filename', sa.String(), nullable=False, unique=True),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('meeting_date', sa.Date(), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('word_count', sa.Integer()),
        sa.Column('participants', postgresql.ARRAY(sa.String()), default=[]),
        sa.Column('search_vector', postgresql.TSVECTOR()),
        sa.Column('source_file', sa.String(), nullable=False),
        sa.Column('file_hash', sa.String(), nullable=False),
        sa.Column('imported_at', sa.DateTime(), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.func.now()),
    )
    op.create_index('idx_transcripts_date', 'transcripts', ['meeting_date'])
    op.create_index('idx_transcripts_search', 'transcripts', ['search_vector'], postgresql_using='gin')

    # Summaries
    op.create_table(
        'summaries',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('transcript_id', sa.Integer(), sa.ForeignKey('transcripts.id', ondelete='CASCADE'), nullable=True),
        sa.Column('filename', sa.String(), nullable=False, unique=True),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('search_vector', postgresql.TSVECTOR()),
        sa.Column('source_file', sa.String(), nullable=False),
        sa.Column('file_hash', sa.String(), nullable=False),
        sa.Column('imported_at', sa.DateTime(), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.func.now()),
    )
    op.create_index('idx_summaries_search', 'summaries', ['search_vector'], postgresql_using='gin')

    # Weekly Reports
    op.create_table(
        'weekly_reports',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('filename', sa.String(), nullable=False, unique=True),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('week_start', sa.Date(), nullable=True),
        sa.Column('week_end', sa.Date(), nullable=True),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('search_vector', postgresql.TSVECTOR()),
        sa.Column('source_file', sa.String(), nullable=False),
        sa.Column('file_hash', sa.String(), nullable=False),
        sa.Column('imported_at', sa.DateTime(), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.func.now()),
    )
    op.create_index('idx_weekly_reports_search', 'weekly_reports', ['search_vector'], postgresql_using='gin')

    # Workstreams
    op.create_table(
        'workstreams',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('code', sa.String(), nullable=False, unique=True),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('lead', sa.String()),
        sa.Column('status', sa.String(), nullable=False),
        sa.Column('description', sa.Text()),
        sa.Column('current_state', sa.Text()),
        sa.Column('next_steps', sa.Text()),
        sa.Column('risks', sa.Text()),
        sa.Column('search_vector', postgresql.TSVECTOR()),
        sa.Column('source_file', sa.String(), nullable=False, server_default='context/workstreams.md'),
        sa.Column('file_hash', sa.String(), nullable=False),
        sa.Column('imported_at', sa.DateTime(), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.func.now()),
    )
    op.create_index('idx_workstreams_search', 'workstreams', ['search_vector'], postgresql_using='gin')

    # Workstream Milestones
    op.create_table(
        'workstream_milestones',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('workstream_id', sa.Integer(), sa.ForeignKey('workstreams.id', ondelete='CASCADE'), nullable=False),
        sa.Column('milestone_date', sa.Date(), nullable=True),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('source_file', sa.String(), nullable=False),
        sa.Column('imported_at', sa.DateTime(), server_default=sa.func.now()),
    )
    op.create_index('idx_milestones_date', 'workstream_milestones', ['milestone_date'])

    # Stakeholders
    op.create_table(
        'stakeholders',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(), nullable=False, unique=True),
        sa.Column('tier', sa.Integer(), nullable=False),
        sa.Column('role', sa.String()),
        sa.Column('engagement_level', sa.String()),
        sa.Column('communication_style', sa.Text()),
        sa.Column('concerns', sa.Text()),
        sa.Column('key_contributions', sa.Text()),
        sa.Column('notes', sa.Text()),
        sa.Column('search_vector', postgresql.TSVECTOR()),
        sa.Column('source_file', sa.String(), nullable=False, server_default='context/stakeholders.md'),
        sa.Column('file_hash', sa.String(), nullable=False),
        sa.Column('imported_at', sa.DateTime(), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.func.now()),
    )
    op.create_index('idx_stakeholders_tier', 'stakeholders', ['tier'])
    op.create_index('idx_stakeholders_search', 'stakeholders', ['search_vector'], postgresql_using='gin')

    # Decisions
    op.create_table(
        'decisions',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('number', sa.Integer(), nullable=False, unique=True),
        sa.Column('decision_date', sa.Date(), nullable=False),
        sa.Column('decision', sa.Text(), nullable=False),
        sa.Column('rationale', sa.Text()),
        sa.Column('key_people', postgresql.ARRAY(sa.String()), default=[]),
        sa.Column('workstream_id', sa.Integer(), sa.ForeignKey('workstreams.id'), nullable=True),
        sa.Column('search_vector', postgresql.TSVECTOR()),
        sa.Column('source_file', sa.String(), nullable=False, server_default='context/decisions.md'),
        sa.Column('file_hash', sa.String(), nullable=False),
        sa.Column('imported_at', sa.DateTime(), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.func.now()),
    )
    op.create_index('idx_decisions_date', 'decisions', ['decision_date'])
    op.create_index('idx_decisions_search', 'decisions', ['search_vector'], postgresql_using='gin')

    # Open Threads
    op.create_table(
        'open_threads',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('number', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('status', sa.String(), nullable=False),
        sa.Column('first_raised', sa.String()),
        sa.Column('context', sa.Text()),
        sa.Column('question', sa.Text()),
        sa.Column('why_it_matters', sa.Text()),
        sa.Column('resolution', sa.Text()),
        sa.Column('search_vector', postgresql.TSVECTOR()),
        sa.Column('source_file', sa.String(), nullable=False, server_default='context/open_threads.md'),
        sa.Column('file_hash', sa.String(), nullable=False),
        sa.Column('imported_at', sa.DateTime(), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.func.now()),
    )
    op.create_index('idx_threads_status', 'open_threads', ['status'])
    op.create_index('idx_threads_search', 'open_threads', ['search_vector'], postgresql_using='gin')

    # Action Items
    op.create_table(
        'action_items',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('number', sa.String(), nullable=False),
        sa.Column('action_date', sa.Date(), nullable=True),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('owner', sa.String()),
        sa.Column('deadline', sa.String()),
        sa.Column('context', sa.Text()),
        sa.Column('status', sa.String(), nullable=False, server_default='OPEN'),
        sa.Column('completed_date', sa.Date(), nullable=True),
        sa.Column('search_vector', postgresql.TSVECTOR()),
        sa.Column('source_file', sa.String(), nullable=False, server_default='analysis/trackers/action_items.md'),
        sa.Column('file_hash', sa.String(), nullable=False),
        sa.Column('imported_at', sa.DateTime(), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.func.now()),
    )
    op.create_index('idx_actions_status', 'action_items', ['status'])
    op.create_index('idx_actions_owner', 'action_items', ['owner'])
    op.create_index('idx_actions_search', 'action_items', ['search_vector'], postgresql_using='gin')

    # Glossary Entries
    op.create_table(
        'glossary_entries',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('term', sa.String(), nullable=False, unique=True),
        sa.Column('category', sa.String()),
        sa.Column('definition', sa.Text(), nullable=False),
        sa.Column('search_vector', postgresql.TSVECTOR()),
        sa.Column('source_file', sa.String(), nullable=False, server_default='context/glossary.md'),
        sa.Column('file_hash', sa.String(), nullable=False),
        sa.Column('imported_at', sa.DateTime(), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.func.now()),
    )
    op.create_index('idx_glossary_search', 'glossary_entries', ['search_vector'], postgresql_using='gin')

    # Transcript Mentions
    op.create_table(
        'transcript_mentions',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('transcript_id', sa.Integer(), sa.ForeignKey('transcripts.id', ondelete='CASCADE'), nullable=False),
        sa.Column('stakeholder_id', sa.Integer(), sa.ForeignKey('stakeholders.id', ondelete='CASCADE'), nullable=False),
        sa.Column('mention_type', sa.String(), nullable=False),
        sa.Column('mention_count', sa.Integer(), default=1),
        sa.UniqueConstraint('transcript_id', 'stakeholder_id', 'mention_type'),
    )
    op.create_index('idx_mentions_stakeholder', 'transcript_mentions', ['stakeholder_id'])
    op.create_index('idx_mentions_transcript', 'transcript_mentions', ['transcript_id'])

    # Documents
    op.create_table(
        'documents',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('filename', sa.String(), nullable=False, unique=True),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('doc_type', sa.String(), nullable=False),
        sa.Column('search_vector', postgresql.TSVECTOR()),
        sa.Column('source_file', sa.String(), nullable=False),
        sa.Column('file_hash', sa.String(), nullable=False),
        sa.Column('imported_at', sa.DateTime(), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.func.now()),
    )
    op.create_index('idx_documents_search', 'documents', ['search_vector'], postgresql_using='gin')

    # Full-text search triggers
    op.execute("""
        CREATE OR REPLACE FUNCTION update_search_vector_transcripts() RETURNS TRIGGER AS $$
        BEGIN
            NEW.search_vector :=
                setweight(to_tsvector('english', COALESCE(NEW.title, '')), 'A') ||
                setweight(to_tsvector('english', COALESCE(array_to_string(NEW.participants, ' '), '')), 'B') ||
                setweight(to_tsvector('english', COALESCE(NEW.content, '')), 'C');
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;
        CREATE TRIGGER trg_search_transcripts BEFORE INSERT OR UPDATE ON transcripts
            FOR EACH ROW EXECUTE FUNCTION update_search_vector_transcripts();
    """)

    op.execute("""
        CREATE OR REPLACE FUNCTION update_search_vector_summaries() RETURNS TRIGGER AS $$
        BEGIN
            NEW.search_vector := to_tsvector('english', COALESCE(NEW.content, ''));
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;
        CREATE TRIGGER trg_search_summaries BEFORE INSERT OR UPDATE ON summaries
            FOR EACH ROW EXECUTE FUNCTION update_search_vector_summaries();
    """)

    op.execute("""
        CREATE OR REPLACE FUNCTION update_search_vector_weekly_reports() RETURNS TRIGGER AS $$
        BEGIN
            NEW.search_vector :=
                setweight(to_tsvector('english', COALESCE(NEW.title, '')), 'A') ||
                setweight(to_tsvector('english', COALESCE(NEW.content, '')), 'C');
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;
        CREATE TRIGGER trg_search_weekly_reports BEFORE INSERT OR UPDATE ON weekly_reports
            FOR EACH ROW EXECUTE FUNCTION update_search_vector_weekly_reports();
    """)

    op.execute("""
        CREATE OR REPLACE FUNCTION update_search_vector_workstreams() RETURNS TRIGGER AS $$
        BEGIN
            NEW.search_vector :=
                setweight(to_tsvector('english', COALESCE(NEW.name, '')), 'A') ||
                setweight(to_tsvector('english', COALESCE(NEW.description, '')), 'B') ||
                setweight(to_tsvector('english', COALESCE(NEW.current_state, '')), 'C') ||
                setweight(to_tsvector('english', COALESCE(NEW.risks, '')), 'C');
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;
        CREATE TRIGGER trg_search_workstreams BEFORE INSERT OR UPDATE ON workstreams
            FOR EACH ROW EXECUTE FUNCTION update_search_vector_workstreams();
    """)

    op.execute("""
        CREATE OR REPLACE FUNCTION update_search_vector_stakeholders() RETURNS TRIGGER AS $$
        BEGIN
            NEW.search_vector :=
                setweight(to_tsvector('english', COALESCE(NEW.name, '')), 'A') ||
                setweight(to_tsvector('english', COALESCE(NEW.role, '')), 'B') ||
                setweight(to_tsvector('english', COALESCE(NEW.notes, '')), 'C');
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;
        CREATE TRIGGER trg_search_stakeholders BEFORE INSERT OR UPDATE ON stakeholders
            FOR EACH ROW EXECUTE FUNCTION update_search_vector_stakeholders();
    """)

    op.execute("""
        CREATE OR REPLACE FUNCTION update_search_vector_decisions() RETURNS TRIGGER AS $$
        BEGIN
            NEW.search_vector :=
                setweight(to_tsvector('english', COALESCE(NEW.decision, '')), 'A') ||
                setweight(to_tsvector('english', COALESCE(NEW.rationale, '')), 'B') ||
                setweight(to_tsvector('english', COALESCE(array_to_string(NEW.key_people, ' '), '')), 'B');
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;
        CREATE TRIGGER trg_search_decisions BEFORE INSERT OR UPDATE ON decisions
            FOR EACH ROW EXECUTE FUNCTION update_search_vector_decisions();
    """)

    op.execute("""
        CREATE OR REPLACE FUNCTION update_search_vector_open_threads() RETURNS TRIGGER AS $$
        BEGIN
            NEW.search_vector :=
                setweight(to_tsvector('english', COALESCE(NEW.title, '')), 'A') ||
                setweight(to_tsvector('english', COALESCE(NEW.question, '')), 'B') ||
                setweight(to_tsvector('english', COALESCE(NEW.context, '')), 'C') ||
                setweight(to_tsvector('english', COALESCE(NEW.why_it_matters, '')), 'C');
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;
        CREATE TRIGGER trg_search_open_threads BEFORE INSERT OR UPDATE ON open_threads
            FOR EACH ROW EXECUTE FUNCTION update_search_vector_open_threads();
    """)

    op.execute("""
        CREATE OR REPLACE FUNCTION update_search_vector_action_items() RETURNS TRIGGER AS $$
        BEGIN
            NEW.search_vector :=
                setweight(to_tsvector('english', COALESCE(NEW.description, '')), 'A') ||
                setweight(to_tsvector('english', COALESCE(NEW.owner, '')), 'B') ||
                setweight(to_tsvector('english', COALESCE(NEW.context, '')), 'C');
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;
        CREATE TRIGGER trg_search_action_items BEFORE INSERT OR UPDATE ON action_items
            FOR EACH ROW EXECUTE FUNCTION update_search_vector_action_items();
    """)

    op.execute("""
        CREATE OR REPLACE FUNCTION update_search_vector_glossary() RETURNS TRIGGER AS $$
        BEGIN
            NEW.search_vector :=
                setweight(to_tsvector('english', COALESCE(NEW.term, '')), 'A') ||
                setweight(to_tsvector('english', COALESCE(NEW.definition, '')), 'B');
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;
        CREATE TRIGGER trg_search_glossary BEFORE INSERT OR UPDATE ON glossary_entries
            FOR EACH ROW EXECUTE FUNCTION update_search_vector_glossary();
    """)

    op.execute("""
        CREATE OR REPLACE FUNCTION update_search_vector_documents() RETURNS TRIGGER AS $$
        BEGIN
            NEW.search_vector :=
                setweight(to_tsvector('english', COALESCE(NEW.title, '')), 'A') ||
                setweight(to_tsvector('english', COALESCE(NEW.content, '')), 'C');
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;
        CREATE TRIGGER trg_search_documents BEFORE INSERT OR UPDATE ON documents
            FOR EACH ROW EXECUTE FUNCTION update_search_vector_documents();
    """)


def downgrade() -> None:
    op.drop_table('transcript_mentions')
    op.drop_table('workstream_milestones')
    op.drop_table('summaries')
    op.drop_table('documents')
    op.drop_table('glossary_entries')
    op.drop_table('action_items')
    op.drop_table('open_threads')
    op.drop_table('decisions')
    op.drop_table('weekly_reports')
    op.drop_table('stakeholders')
    op.drop_table('workstreams')
    op.drop_table('transcripts')
