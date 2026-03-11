from datetime import date

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.exceptions import NotFoundError
from app.models.contradiction import Contradiction
from app.schemas.contradiction import (
    ContradictionBase,
    ContradictionCreate,
    ContradictionUpdate,
)
from app.services.contradiction_writeback import (
    append_contradiction as wb_append_contradiction,
    append_gap as wb_append_gap,
    remove_contradiction as wb_remove_contradiction,
    remove_gap as wb_remove_gap,
    update_contradiction_resolution as wb_update_resolution,
)

router = APIRouter(tags=["contradictions"])


def _schema(s: Contradiction) -> ContradictionBase:
    return ContradictionBase(
        id=s.id,
        date=str(s.date) if s.date else None,
        contradiction_type=s.contradiction_type,
        person=s.person,
        statement_a=s.statement_a,
        date_a=str(s.date_a) if s.date_a else None,
        statement_b=s.statement_b,
        date_b=str(s.date_b) if s.date_b else None,
        severity=s.severity,
        resolution=s.resolution or "unresolved",
        confidence=s.confidence,
        gap_description=s.gap_description,
        expected_source=s.expected_source,
        last_mentioned=str(s.last_mentioned) if s.last_mentioned else None,
        meetings_absent=s.meetings_absent,
        entry_kind=s.entry_kind or "contradiction",
        transcript_id=s.transcript_id,
        is_manual=s.is_manual,
    )


@router.get("/contradictions", response_model=list[ContradictionBase])
async def list_contradictions(
    entry_kind: str | None = Query(None),
    person: str | None = Query(None),
    severity: str | None = Query(None),
    db: AsyncSession = Depends(get_db),
):
    query = select(Contradiction)
    if entry_kind is not None:
        query = query.where(Contradiction.entry_kind == entry_kind)
    if person is not None:
        query = query.where(Contradiction.person == person)
    if severity is not None:
        query = query.where(Contradiction.severity == severity)
    query = query.order_by(Contradiction.date.desc().nullslast(), Contradiction.id.desc())
    result = await db.execute(query)
    return [_schema(s) for s in result.scalars().all()]


@router.get("/contradictions/gaps", response_model=list[ContradictionBase])
async def list_gaps(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Contradiction)
        .where(Contradiction.entry_kind == "gap")
        .order_by(Contradiction.date.desc().nullslast(), Contradiction.id.desc())
    )
    return [_schema(s) for s in result.scalars().all()]


@router.get("/contradictions/by-person/{name}", response_model=list[ContradictionBase])
async def contradictions_by_person(name: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Contradiction)
        .where(Contradiction.person.ilike(f"%{name}%"))
        .order_by(Contradiction.date.desc().nullslast(), Contradiction.id.desc())
    )
    return [_schema(s) for s in result.scalars().all()]


@router.get("/contradictions/{contradiction_id}", response_model=ContradictionBase)
async def get_contradiction(contradiction_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Contradiction).where(Contradiction.id == contradiction_id)
    )
    signal = result.scalar_one_or_none()
    if not signal:
        raise NotFoundError("Contradiction", contradiction_id)
    return _schema(signal)


@router.post("/contradictions", response_model=ContradictionBase, status_code=201)
async def create_contradiction(body: ContradictionCreate, db: AsyncSession = Depends(get_db)):
    record = Contradiction(
        date=date.fromisoformat(body.date) if body.date else None,
        contradiction_type=body.contradiction_type,
        person=body.person,
        statement_a=body.statement_a,
        date_a=date.fromisoformat(body.date_a) if body.date_a else None,
        statement_b=body.statement_b,
        date_b=date.fromisoformat(body.date_b) if body.date_b else None,
        severity=body.severity,
        resolution=body.resolution,
        confidence=body.confidence,
        gap_description=body.gap_description,
        expected_source=body.expected_source,
        last_mentioned=date.fromisoformat(body.last_mentioned) if body.last_mentioned else None,
        meetings_absent=body.meetings_absent,
        entry_kind=body.entry_kind,
        transcript_id=body.transcript_id,
        is_manual=True,
    )
    db.add(record)
    await db.commit()
    await db.refresh(record)

    # Writeback to markdown
    if record.entry_kind == "gap":
        wb_append_gap(
            entry_date=record.date,
            gap_description=record.gap_description,
            expected_source=record.expected_source,
            last_mentioned=record.last_mentioned,
            meetings_absent=record.meetings_absent,
            severity=record.severity,
        )
    else:
        wb_append_contradiction(
            entry_date=record.date,
            contradiction_type=record.contradiction_type,
            person=record.person,
            statement_a=record.statement_a,
            date_a=record.date_a,
            statement_b=record.statement_b,
            date_b=record.date_b,
            severity=record.severity,
            resolution=record.resolution,
            confidence=record.confidence,
        )

    return _schema(record)


@router.patch("/contradictions/{contradiction_id}", response_model=ContradictionBase)
async def update_contradiction(
    contradiction_id: int,
    body: ContradictionUpdate,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Contradiction).where(Contradiction.id == contradiction_id)
    )
    record = result.scalar_one_or_none()
    if not record:
        raise NotFoundError("Contradiction", contradiction_id)

    if body.date is not None:
        record.date = date.fromisoformat(body.date)
    if body.contradiction_type is not None:
        record.contradiction_type = body.contradiction_type
    if body.person is not None:
        record.person = body.person
    if body.statement_a is not None:
        record.statement_a = body.statement_a
    if body.date_a is not None:
        record.date_a = date.fromisoformat(body.date_a)
    if body.statement_b is not None:
        record.statement_b = body.statement_b
    if body.date_b is not None:
        record.date_b = date.fromisoformat(body.date_b)
    if body.severity is not None:
        record.severity = body.severity
    if body.resolution is not None:
        record.resolution = body.resolution
    if body.confidence is not None:
        record.confidence = body.confidence
    if body.gap_description is not None:
        record.gap_description = body.gap_description
    if body.expected_source is not None:
        record.expected_source = body.expected_source
    if body.last_mentioned is not None:
        record.last_mentioned = date.fromisoformat(body.last_mentioned)
    if body.meetings_absent is not None:
        record.meetings_absent = body.meetings_absent
    if body.entry_kind is not None:
        record.entry_kind = body.entry_kind
    if body.transcript_id is not None:
        record.transcript_id = body.transcript_id

    await db.commit()
    await db.refresh(record)

    # Writeback resolution changes to markdown
    if body.resolution is not None and record.entry_kind != "gap" and record.person and record.statement_a:
        wb_update_resolution(record.person, record.statement_a, record.resolution)

    return _schema(record)


@router.delete("/contradictions/{contradiction_id}")
async def delete_contradiction(contradiction_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Contradiction).where(Contradiction.id == contradiction_id)
    )
    record = result.scalar_one_or_none()
    if not record:
        raise NotFoundError("Contradiction", contradiction_id)

    # Writeback: remove from markdown before deleting from DB
    if record.entry_kind == "gap" and record.gap_description:
        wb_remove_gap(record.gap_description)
    elif record.person and record.statement_a:
        wb_remove_contradiction(record.person, record.statement_a)

    await db.delete(record)
    await db.commit()
    return {"ok": True}
