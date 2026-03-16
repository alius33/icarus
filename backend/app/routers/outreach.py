from datetime import datetime

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db, utcnow
from app.exceptions import NotFoundError
from app.models.outreach import Outreach
from app.schemas.outreach import OutreachCreate, OutreachSchema, OutreachUpdate

router = APIRouter(tags=["outreach"])


def _parse_date(date_str: str | None):
    """Parse a YYYY-MM-DD string into a date or return None."""
    if not date_str:
        return None
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        return None


def _schema(o: Outreach) -> OutreachSchema:
    return OutreachSchema(
        id=o.id,
        contact_name=o.contact_name,
        contact_role=o.contact_role,
        division=o.division,
        status=o.status or "initial_contact",
        interest_level=o.interest_level or 1,
        first_contact_date=str(o.first_contact_date) if o.first_contact_date else None,
        last_contact_date=str(o.last_contact_date) if o.last_contact_date else None,
        meeting_count=o.meeting_count or 0,
        notes=o.notes,
        next_step=o.next_step,
        next_step_date=str(o.next_step_date) if o.next_step_date else None,
        external_id=o.external_id,
        external_source=o.external_source,
    )


@router.get("/outreach", response_model=list[OutreachSchema])
async def list_outreach(
    status: str | None = Query(None),
    division: str | None = Query(None),
    db: AsyncSession = Depends(get_db),
):
    query = select(Outreach)
    if status:
        query = query.where(Outreach.status == status)
    if division:
        query = query.where(Outreach.division == division)

    result = await db.execute(
        query.order_by(Outreach.last_contact_date.desc().nullslast(), Outreach.created_at.desc())
    )
    return [_schema(o) for o in result.scalars().all()]


@router.get("/outreach/{outreach_id}", response_model=OutreachSchema)
async def get_outreach(outreach_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Outreach).where(Outreach.id == outreach_id))
    o = result.scalar_one_or_none()
    if not o:
        raise NotFoundError("Outreach contact", outreach_id)
    return _schema(o)


@router.post("/outreach", response_model=OutreachSchema, status_code=201)
async def create_outreach(body: OutreachCreate, db: AsyncSession = Depends(get_db)):
    o = Outreach(
        contact_name=body.contact_name,
        contact_role=body.contact_role,
        division=body.division,
        status=body.status,
        interest_level=body.interest_level,
        first_contact_date=_parse_date(body.first_contact_date),
        last_contact_date=_parse_date(body.last_contact_date),
        meeting_count=body.meeting_count,
        notes=body.notes,
        next_step=body.next_step,
        next_step_date=_parse_date(body.next_step_date),
        external_id=body.external_id,
        external_source=body.external_source,
    )
    db.add(o)
    await db.commit()
    await db.refresh(o)
    return _schema(o)


@router.patch("/outreach/{outreach_id}", response_model=OutreachSchema)
async def update_outreach(outreach_id: int, body: OutreachUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Outreach).where(Outreach.id == outreach_id))
    o = result.scalar_one_or_none()
    if not o:
        raise NotFoundError("Outreach contact", outreach_id)

    for field in ["contact_name", "contact_role", "division", "status",
                  "interest_level", "meeting_count", "notes", "next_step",
                  "external_id", "external_source"]:
        val = getattr(body, field)
        if val is not None:
            setattr(o, field, val)

    for date_field in ["first_contact_date", "last_contact_date", "next_step_date"]:
        val = getattr(body, date_field)
        if val is not None:
            setattr(o, date_field, _parse_date(val))

    o.updated_at = utcnow()
    await db.commit()
    await db.refresh(o)
    return _schema(o)


@router.delete("/outreach/{outreach_id}")
async def delete_outreach(outreach_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Outreach).where(Outreach.id == outreach_id))
    o = result.scalar_one_or_none()
    if not o:
        raise NotFoundError("Outreach contact", outreach_id)
    await db.delete(o)
    await db.commit()
    return {"ok": True}
