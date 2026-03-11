from datetime import date

from fastapi import APIRouter, Depends, Query
from sqlalchemy import case, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.exceptions import NotFoundError
from app.models.risk_entry import RiskEntry
from app.schemas.risk_entry import (
    RiskEntryBase,
    RiskEntryCreate,
    RiskEntryUpdate,
)
from app.services.risk_writeback import (
    append_risk_entry as wb_append_risk,
    remove_risk_entry as wb_remove_risk,
    update_risk_fields as wb_update_risk,
)

router = APIRouter(tags=["risk-entries"])

SEVERITY_ORDER = case(
    (RiskEntry.severity == "CRITICAL", 0),
    (RiskEntry.severity == "HIGH", 1),
    (RiskEntry.severity == "MEDIUM", 2),
    (RiskEntry.severity == "LOW", 3),
    else_=4,
)


def _schema(s: RiskEntry) -> RiskEntryBase:
    return RiskEntryBase(
        id=s.id,
        risk_id=s.risk_id,
        date=str(s.date) if s.date else None,
        title=s.title,
        description=s.description,
        category=s.category,
        severity=s.severity,
        trajectory=s.trajectory,
        source_type=s.source_type,
        owner=s.owner,
        mitigation=s.mitigation,
        last_reviewed=str(s.last_reviewed) if s.last_reviewed else None,
        meetings_mentioned=s.meetings_mentioned or 1,
        confidence=s.confidence,
        transcript_id=s.transcript_id,
        is_manual=s.is_manual,
    )


@router.get("/risk-entries", response_model=list[RiskEntryBase])
async def list_risk_entries(
    severity: str | None = Query(None),
    trajectory: str | None = Query(None),
    category: str | None = Query(None),
    db: AsyncSession = Depends(get_db),
):
    query = select(RiskEntry)
    if severity is not None:
        query = query.where(RiskEntry.severity == severity)
    if trajectory is not None:
        query = query.where(RiskEntry.trajectory == trajectory)
    if category is not None:
        query = query.where(RiskEntry.category == category)
    query = query.order_by(SEVERITY_ORDER, RiskEntry.date.desc().nullslast(), RiskEntry.id.desc())
    result = await db.execute(query)
    return [_schema(s) for s in result.scalars().all()]


@router.get("/risk-entries/heatmap")
async def risk_heatmap(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(RiskEntry))
    entries = result.scalars().all()

    cat_map: dict[str, dict[str, int]] = {}
    for e in entries:
        cat = e.category or "uncategorised"
        if cat not in cat_map:
            cat_map[cat] = {"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0}
        sev = e.severity if e.severity in ("CRITICAL", "HIGH", "MEDIUM", "LOW") else "LOW"
        cat_map[cat][sev] += 1

    rows = [
        {"category": cat, **counts}
        for cat, counts in sorted(cat_map.items())
    ]
    return {"rows": rows}


@router.get("/risk-entries/trajectory", response_model=list[RiskEntryBase])
async def escalating_risks(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(RiskEntry)
        .where(RiskEntry.trajectory == "escalating")
        .order_by(SEVERITY_ORDER, RiskEntry.date.desc().nullslast(), RiskEntry.id.desc())
    )
    return [_schema(s) for s in result.scalars().all()]


@router.get("/risk-entries/{entry_id}", response_model=RiskEntryBase)
async def get_risk_entry(entry_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(RiskEntry).where(RiskEntry.id == entry_id)
    )
    entry = result.scalar_one_or_none()
    if not entry:
        raise NotFoundError("Risk entry", entry_id)
    return _schema(entry)


@router.post("/risk-entries", response_model=RiskEntryBase, status_code=201)
async def create_risk_entry(body: RiskEntryCreate, db: AsyncSession = Depends(get_db)):
    record = RiskEntry(
        risk_id=body.risk_id,
        date=date.fromisoformat(body.date) if body.date else None,
        title=body.title,
        description=body.description,
        category=body.category,
        severity=body.severity,
        trajectory=body.trajectory,
        source_type=body.source_type,
        owner=body.owner,
        mitigation=body.mitigation,
        last_reviewed=date.fromisoformat(body.last_reviewed) if body.last_reviewed else None,
        meetings_mentioned=body.meetings_mentioned,
        confidence=body.confidence,
        transcript_id=body.transcript_id,
        is_manual=True,
    )
    db.add(record)
    await db.commit()
    await db.refresh(record)

    # Writeback to markdown
    wb_append_risk(
        risk_id=record.risk_id,
        entry_date=record.date,
        title=record.title,
        description=record.description,
        category=record.category,
        severity=record.severity,
        trajectory=record.trajectory,
        source_type=record.source_type,
        owner=record.owner,
        mitigation=record.mitigation,
        last_reviewed=record.last_reviewed,
        meetings_mentioned=record.meetings_mentioned,
        confidence=record.confidence,
    )

    return _schema(record)


@router.patch("/risk-entries/{entry_id}", response_model=RiskEntryBase)
async def update_risk_entry(
    entry_id: int,
    body: RiskEntryUpdate,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(RiskEntry).where(RiskEntry.id == entry_id)
    )
    record = result.scalar_one_or_none()
    if not record:
        raise NotFoundError("Risk entry", entry_id)

    if body.risk_id is not None:
        record.risk_id = body.risk_id
    if body.date is not None:
        record.date = date.fromisoformat(body.date)
    if body.title is not None:
        record.title = body.title
    if body.description is not None:
        record.description = body.description
    if body.category is not None:
        record.category = body.category
    if body.severity is not None:
        record.severity = body.severity
    if body.trajectory is not None:
        record.trajectory = body.trajectory
    if body.source_type is not None:
        record.source_type = body.source_type
    if body.owner is not None:
        record.owner = body.owner
    if body.mitigation is not None:
        record.mitigation = body.mitigation
    if body.last_reviewed is not None:
        record.last_reviewed = date.fromisoformat(body.last_reviewed)
    if body.meetings_mentioned is not None:
        record.meetings_mentioned = body.meetings_mentioned
    if body.confidence is not None:
        record.confidence = body.confidence
    if body.transcript_id is not None:
        record.transcript_id = body.transcript_id

    await db.commit()
    await db.refresh(record)

    # Writeback to markdown
    if record.risk_id:
        wb_update_risk(
            risk_id=record.risk_id,
            severity=record.severity,
            trajectory=record.trajectory,
            owner=record.owner,
            mitigation=record.mitigation,
            last_reviewed=record.last_reviewed,
        )

    return _schema(record)


@router.delete("/risk-entries/{entry_id}")
async def delete_risk_entry(entry_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(RiskEntry).where(RiskEntry.id == entry_id)
    )
    record = result.scalar_one_or_none()
    if not record:
        raise NotFoundError("Risk entry", entry_id)

    # Writeback: remove from markdown before deleting from DB
    if record.risk_id:
        wb_remove_risk(record.risk_id)

    await db.delete(record)
    await db.commit()
    return {"ok": True}
