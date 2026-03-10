from collections import defaultdict
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.glossary import GlossaryEntry
from app.models.deleted_import import DeletedImport
from app.schemas.glossary import GlossaryEntrySchema, GlossaryGrouped, GlossaryCreate, GlossaryUpdate

router = APIRouter(tags=["glossary"])


def _entry_schema(entry: GlossaryEntry) -> GlossaryEntrySchema:
    return GlossaryEntrySchema(
        id=entry.id, term=entry.term, definition=entry.definition,
        category=entry.category or "Uncategorized", aliases=[], is_manual=entry.is_manual,
    )


@router.get("/glossary", response_model=GlossaryGrouped)
async def list_glossary(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(GlossaryEntry).order_by(GlossaryEntry.category, GlossaryEntry.term))
    grouped: dict[str, list[GlossaryEntrySchema]] = defaultdict(list)
    for entry in result.scalars().all():
        grouped[entry.category or "Uncategorized"].append(_entry_schema(entry))
    return dict(grouped)


@router.get("/glossary/{entry_id}", response_model=GlossaryEntrySchema)
async def get_glossary_entry(entry_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(GlossaryEntry).where(GlossaryEntry.id == entry_id))
    entry = result.scalar_one_or_none()
    if not entry:
        raise HTTPException(status_code=404, detail="Glossary entry not found")
    return _entry_schema(entry)


@router.post("/glossary", response_model=GlossaryEntrySchema)
async def create_glossary_entry(body: GlossaryCreate, db: AsyncSession = Depends(get_db)):
    existing = await db.execute(select(GlossaryEntry).where(GlossaryEntry.term == body.term))
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=409, detail="Term already exists")

    entry = GlossaryEntry(term=body.term, definition=body.definition, category=body.category,
                           is_manual=True, source_file="manual", file_hash="")
    db.add(entry)
    await db.commit()
    await db.refresh(entry)
    return _entry_schema(entry)


@router.patch("/glossary/{entry_id}", response_model=GlossaryEntrySchema)
async def update_glossary_entry(entry_id: int, body: GlossaryUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(GlossaryEntry).where(GlossaryEntry.id == entry_id))
    entry = result.scalar_one_or_none()
    if not entry:
        raise HTTPException(status_code=404, detail="Glossary entry not found")

    if body.definition is not None:
        entry.definition = body.definition
    if body.category is not None:
        entry.category = body.category
    entry.is_manual = True
    entry.updated_at = datetime.utcnow()
    await db.commit()
    await db.refresh(entry)
    return _entry_schema(entry)


@router.delete("/glossary/{entry_id}")
async def delete_glossary_entry(entry_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(GlossaryEntry).where(GlossaryEntry.id == entry_id))
    entry = result.scalar_one_or_none()
    if not entry:
        raise HTTPException(status_code=404, detail="Glossary entry not found")

    if not entry.is_manual:
        db.add(DeletedImport(entity_type="glossary", unique_key=entry.term))
    await db.delete(entry)
    await db.commit()
    return {"ok": True}
