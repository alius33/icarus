from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.division_profile import DivisionProfile
from app.schemas.division_profile import DivisionProfileSchema, DivisionProfileCreate, DivisionProfileUpdate

router = APIRouter(tags=["divisions"])


def _schema(d: DivisionProfile) -> DivisionProfileSchema:
    return DivisionProfileSchema(
        id=d.id,
        name=d.name,
        status=d.status or "not_engaged",
        current_tools=d.current_tools,
        pain_points=d.pain_points,
        key_contact=d.key_contact,
        notes=d.notes,
    )


@router.get("/divisions", response_model=list[DivisionProfileSchema])
async def list_divisions(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(DivisionProfile).order_by(DivisionProfile.name))
    return [_schema(d) for d in result.scalars().all()]


@router.get("/divisions/{division_id}", response_model=DivisionProfileSchema)
async def get_division(division_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(DivisionProfile).where(DivisionProfile.id == division_id))
    d = result.scalar_one_or_none()
    if not d:
        raise HTTPException(status_code=404, detail="Division profile not found")
    return _schema(d)


@router.post("/divisions", response_model=DivisionProfileSchema, status_code=201)
async def create_division(body: DivisionProfileCreate, db: AsyncSession = Depends(get_db)):
    d = DivisionProfile(
        name=body.name,
        status=body.status,
        current_tools=body.current_tools,
        pain_points=body.pain_points,
        key_contact=body.key_contact,
        notes=body.notes,
    )
    db.add(d)
    await db.commit()
    await db.refresh(d)
    return _schema(d)


@router.patch("/divisions/{division_id}", response_model=DivisionProfileSchema)
async def update_division(division_id: int, body: DivisionProfileUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(DivisionProfile).where(DivisionProfile.id == division_id))
    d = result.scalar_one_or_none()
    if not d:
        raise HTTPException(status_code=404, detail="Division profile not found")

    for field in ["name", "status", "current_tools", "pain_points", "key_contact", "notes"]:
        val = getattr(body, field)
        if val is not None:
            setattr(d, field, val)

    d.updated_at = datetime.utcnow()
    await db.commit()
    await db.refresh(d)
    return _schema(d)


@router.delete("/divisions/{division_id}")
async def delete_division(division_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(DivisionProfile).where(DivisionProfile.id == division_id))
    d = result.scalar_one_or_none()
    if not d:
        raise HTTPException(status_code=404, detail="Division profile not found")
    await db.delete(d)
    await db.commit()
    return {"ok": True}
