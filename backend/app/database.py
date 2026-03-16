from datetime import datetime, timezone

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from app.config import settings

_pool_kwargs = {}
if "sqlite" not in settings.DATABASE_URL:
    _pool_kwargs = dict(
        pool_size=10,
        max_overflow=5,
        pool_recycle=300,
        pool_pre_ping=True,
    )

engine = create_async_engine(settings.DATABASE_URL, echo=False, **_pool_kwargs)
async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


def utcnow() -> datetime:
    """UTC now as a naive datetime (no tzinfo). Drop-in replacement for
    the deprecated ``datetime.utcnow()`` that avoids the deprecation
    warning while staying compatible with ``TIMESTAMP WITHOUT TIME ZONE``
    columns used throughout the schema."""
    return datetime.now(timezone.utc).replace(tzinfo=None)


class Base(DeclarativeBase):
    pass


async def get_db():
    async with async_session() as session:
        yield session
