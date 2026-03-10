from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.exceptions import NotFoundError
from app.models.scope_item import ScopeItem
from app.schemas.scope_item import ScopeItemCreate, ScopeItemSchema, ScopeItemUpdate

router = APIRouter(tags=["scope"])


def _schema(s: ScopeItem) -> ScopeItemSchema:
    return ScopeItemSchema(
        id=s.id,
        name=s.name,
        scope_type=s.scope_type,
        workstream=s.workstream,
        added_date=s.added_date,
        estimated_effort=s.estimated_effort,
        budgeted=s.budgeted or False,
        status=s.status or "planned",
        description=s.description,
        impact_notes=s.impact_notes,
    )


@router.get("/scope", response_model=list[ScopeItemSchema])
async def list_scope_items(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(ScopeItem).order_by(ScopeItem.scope_type, ScopeItem.created_at.desc()))
    return [_schema(s) for s in result.scalars().all()]


@router.get("/scope/{item_id}", response_model=ScopeItemSchema)
async def get_scope_item(item_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(ScopeItem).where(ScopeItem.id == item_id))
    item = result.scalar_one_or_none()
    if not item:
        raise NotFoundError("Scope item", item_id)
    return _schema(item)


@router.post("/scope", response_model=ScopeItemSchema, status_code=201)
async def create_scope_item(body: ScopeItemCreate, db: AsyncSession = Depends(get_db)):
    item = ScopeItem(
        name=body.name,
        scope_type=body.scope_type,
        workstream=body.workstream,
        added_date=body.added_date or datetime.utcnow().strftime("%Y-%m-%d"),
        estimated_effort=body.estimated_effort,
        budgeted=body.budgeted,
        status=body.status,
        description=body.description,
        impact_notes=body.impact_notes,
    )
    db.add(item)
    await db.commit()
    await db.refresh(item)
    return _schema(item)


@router.patch("/scope/{item_id}", response_model=ScopeItemSchema)
async def update_scope_item(item_id: int, body: ScopeItemUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(ScopeItem).where(ScopeItem.id == item_id))
    item = result.scalar_one_or_none()
    if not item:
        raise NotFoundError("Scope item", item_id)

    for field in ["name", "scope_type", "workstream", "added_date",
                  "estimated_effort", "budgeted", "status",
                  "description", "impact_notes"]:
        val = getattr(body, field)
        if val is not None:
            setattr(item, field, val)

    item.updated_at = datetime.utcnow()
    await db.commit()
    await db.refresh(item)
    return _schema(item)


@router.delete("/scope/{item_id}")
async def delete_scope_item(item_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(ScopeItem).where(ScopeItem.id == item_id))
    item = result.scalar_one_or_none()
    if not item:
        raise NotFoundError("Scope item", item_id)
    await db.delete(item)
    await db.commit()
    return {"ok": True}
