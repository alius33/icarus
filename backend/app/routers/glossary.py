from collections import defaultdict

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.exceptions import DuplicateError
from app.models.glossary import GlossaryEntry
from app.routers.crud_factory import CRUDConfig, create_crud_router
from app.schemas.glossary import (
    GlossaryCreate,
    GlossaryEntrySchema,
    GlossaryGrouped,
    GlossaryUpdate,
)


def _to_schema(entry: GlossaryEntry) -> GlossaryEntrySchema:
    return GlossaryEntrySchema(
        id=entry.id,
        term=entry.term,
        definition=entry.definition,
        category=entry.category or "Uncategorized",
        aliases=[],
        is_manual=entry.is_manual,
    )


async def _create_to_orm(body: GlossaryCreate, db) -> dict:
    existing = await db.execute(
        select(GlossaryEntry).where(GlossaryEntry.term == body.term)
    )
    if existing.scalar_one_or_none():
        raise DuplicateError("Glossary entry", "term", body.term)

    return {
        "term": body.term,
        "definition": body.definition,
        "category": body.category,
        "is_manual": True,
        "source_file": "manual",
        "file_hash": "",
    }


config = CRUDConfig(
    model=GlossaryEntry,
    schema=GlossaryEntrySchema,
    schema_create=GlossaryCreate,
    schema_update=GlossaryUpdate,
    prefix="/glossary",
    entity_name="Glossary entry",
    tags=["glossary"],
    to_schema=_to_schema,
    create_to_orm=_create_to_orm,
    ordering=[("category", "asc"), ("term", "asc")],
    track_deletions=True,
    deletion_entity_type="glossary",
    deletion_key=lambda entry: entry.term,
)

router = create_crud_router(config)
