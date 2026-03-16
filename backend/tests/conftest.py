"""
Shared test fixtures for the Icarus backend test suite.

Uses an async SQLite in-memory database so tests run fast without requiring
PostgreSQL. PostgreSQL-specific column types (TSVECTOR, ARRAY, JSON with the
pg dialect) and GIN indexes are patched to SQLite-compatible equivalents
before table creation.

IMPORTANT: Environment variables and type patches must happen before ANY
app module is imported, because app.database creates the engine at import
time and app.config.Settings reads DATABASE_URL at import time.
"""

import os

# ---------------------------------------------------------------------------
# 1. Set DATABASE_URL to SQLite BEFORE any app module is loaded.
#    This ensures app.config.Settings picks up the test URL and
#    app.database creates a SQLite engine (no asyncpg import needed).
# ---------------------------------------------------------------------------
os.environ["DATABASE_URL"] = "sqlite+aiosqlite:///:memory:"
os.environ["SYNC_DATABASE_URL"] = "sqlite:///:memory:"

# ---------------------------------------------------------------------------
# 2. Patch PostgreSQL dialect types BEFORE any model is imported.
#    This ensures Column definitions using TSVECTOR, ARRAY, or JSON from
#    the pg dialect resolve to SQLite-compatible types.
# ---------------------------------------------------------------------------
import json as _json

from sqlalchemy import Text, String, types as sa_types  # noqa: E402

import sqlalchemy.dialects.postgresql as pg_dialect  # noqa: E402

_original_tsvector = pg_dialect.TSVECTOR
_original_array = pg_dialect.ARRAY
_original_json = pg_dialect.JSON

pg_dialect.TSVECTOR = Text


class _SQLiteJSON(sa_types.TypeDecorator):
    """Store JSON-compatible values as text in SQLite."""

    impl = Text
    cache_ok = True

    def process_bind_param(self, value, dialect):
        if value is not None:
            return _json.dumps(value)
        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            return _json.loads(value)
        return value


pg_dialect.JSON = _SQLiteJSON


class _SQLiteArray(sa_types.TypeDecorator):
    """Store ARRAY values as JSON-encoded text in SQLite."""

    impl = Text
    cache_ok = True

    def __init__(self, *args, **kwargs):
        super().__init__()

    def process_bind_param(self, value, dialect):
        if value is not None:
            return _json.dumps(value)
        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            return _json.loads(value)
        return value


pg_dialect.ARRAY = _SQLiteArray

# ---------------------------------------------------------------------------
# 3. Now it is safe to import app modules.  The engine will use SQLite,
#    and model columns will use the patched types.
# ---------------------------------------------------------------------------
from typing import AsyncGenerator  # noqa: E402

import pytest  # noqa: E402
from sqlalchemy import event  # noqa: E402
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker  # noqa: E402

from app.database import Base, get_db  # noqa: E402
from app.models import (  # noqa: E402, F401
    Transcript, Summary, WeeklyReport,
    Stakeholder, Decision, OpenThread, ActionItem, GlossaryEntry,
    TranscriptMention, Document, Project, ProjectLink, DeletedImport,
    Dependency, ResourceAllocation, ScopeItem, ProgrammeWin,
    AdoptionMetric, Outreach, OutreachLink, DivisionProfile,
    SentimentSignal, Commitment, CrossProjectLink,
)

# ---------------------------------------------------------------------------
# Async SQLite engine + session factory for tests
# ---------------------------------------------------------------------------
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

engine = create_async_engine(TEST_DATABASE_URL, echo=False)
TestingSessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


# ---------------------------------------------------------------------------
# Event listener: remove GIN indexes that SQLite cannot handle.
# ---------------------------------------------------------------------------
_gin_indexes_cleaned = False


@event.listens_for(Base.metadata, "before_create")
def _remove_gin_indexes(target, connection, **kwargs):
    """Strip postgresql GIN indexes so create_all works on SQLite."""
    global _gin_indexes_cleaned
    if _gin_indexes_cleaned:
        return
    for table in target.tables.values():
        to_drop = [
            idx for idx in table.indexes
            if idx.dialect_options.get("postgresql", {}).get("using") == "gin"
        ]
        for idx in to_drop:
            table.indexes.discard(idx)
    _gin_indexes_cleaned = True


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture(autouse=True)
async def _setup_database():
    """Create all tables before each test, drop them after."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    """Provide a transactional test database session."""
    async with TestingSessionLocal() as session:
        yield session


@pytest.fixture
async def client():
    """Async HTTP test client with the get_db dependency overridden."""
    from httpx import ASGITransport, AsyncClient
    from app.main import app

    async def _override_get_db():
        async with TestingSessionLocal() as session:
            yield session

    app.dependency_overrides[get_db] = _override_get_db

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

    app.dependency_overrides.clear()
