from datetime import datetime

from fastapi import APIRouter, Depends, Query
from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.exceptions import NotFoundError
from app.models.decision import Decision
from app.models.deleted_import import DeletedImport
from app.services.decision_writeback import (
    append_decision,
    remove_decision,
    update_decision_status,
)
from app.models.project_link import ProjectLink
from app.schemas.decision import (
    DecisionBoardColumn,
    DecisionBoardResponse,
    DecisionCreate,
    DecisionPositionUpdate,
    DecisionSchema,
    DecisionTimelineItem,
    DecisionTimelineResponse,
    DecisionUpdate,
)

router = APIRouter(tags=["decisions"])

DECISION_STATUSES = ["made", "in_progress", "implemented", "reversed", "superseded"]
DECISION_STATUS_CONFIG = {
    "made":        {"label": "Made",        "color": "blue",   "order": 0},
    "in_progress": {"label": "In Progress", "color": "yellow", "order": 1},
    "implemented": {"label": "Implemented", "color": "green",  "order": 2},
    "reversed":    {"label": "Reversed",    "color": "red",    "order": 3},
    "superseded":  {"label": "Superseded",  "color": "gray",   "order": 4},
}


def _decision_schema(d: Decision) -> DecisionSchema:
    return DecisionSchema(
        id=d.id,
        number=d.number,
        title=d.decision[:120] if d.decision else f"Decision #{d.number}",
        description=d.decision,
        date=str(d.decision_date) if d.decision_date else None,
        status=d.execution_status or "made",
        execution_status=d.execution_status or "made",
        rationale=d.rationale,
        key_people=d.key_people or [],
        owner=", ".join(d.key_people) if d.key_people else None,
        project_id=d.project_id,
        project_name=None,
        position=d.position,
        transcript_id=None,
        transcript_title=None,
        is_manual=d.is_manual,
    )


# --- List (flat with filters) ---
@router.get("/decisions", response_model=list[DecisionSchema])
async def list_decisions(
    project_id: int | None = Query(None),
    execution_status: str | None = Query(None),
    key_person: str | None = Query(None),
    search: str | None = Query(None),
    db: AsyncSession = Depends(get_db),
):
    query = select(Decision)
    if project_id is not None:
        linked_ids = select(ProjectLink.entity_id).where(
            ProjectLink.project_id == project_id,
            ProjectLink.entity_type == "decision",
        )
        query = query.where(Decision.id.in_(linked_ids))
    if execution_status is not None:
        query = query.where(Decision.execution_status == execution_status)
    if key_person:
        query = query.where(Decision.key_people.any(key_person))
    if search:
        pattern = f"%{search}%"
        query = query.where(or_(
            Decision.decision.ilike(pattern),
            Decision.rationale.ilike(pattern),
        ))
    result = await db.execute(
        query.order_by(Decision.position, Decision.id)
    )
    return [_decision_schema(d) for d in result.scalars().all()]


# --- Board (grouped by execution_status) ---
@router.get("/decisions/board", response_model=DecisionBoardResponse)
async def get_decision_board(
    project_id: int | None = Query(None),
    db: AsyncSession = Depends(get_db),
):
    query = select(Decision).order_by(Decision.position, Decision.id)
    if project_id is not None:
        linked_ids = select(ProjectLink.entity_id).where(
            ProjectLink.project_id == project_id,
            ProjectLink.entity_type == "decision",
        )
        query = query.where(Decision.id.in_(linked_ids))
    result = await db.execute(query)
    rows = result.scalars().all()

    columns_map: dict[str, list[DecisionSchema]] = {s: [] for s in DECISION_STATUSES}
    for d in rows:
        bucket = (d.execution_status or "made") if (d.execution_status or "made") in columns_map else "made"
        columns_map[bucket].append(_decision_schema(d))

    columns = []
    total = 0
    for status in DECISION_STATUSES:
        cfg = DECISION_STATUS_CONFIG.get(status, {"label": status, "color": "gray", "order": 99})
        decisions = columns_map[status]
        total += len(decisions)
        columns.append(DecisionBoardColumn(
            status=status,
            label=cfg["label"],
            color=cfg["color"],
            order=cfg["order"],
            decisions=decisions,
            count=len(decisions),
        ))

    return DecisionBoardResponse(columns=columns, total=total)


# --- Timeline ---
@router.get("/decisions/timeline", response_model=DecisionTimelineResponse)
async def get_decision_timeline(
    project_id: int | None = Query(None),
    db: AsyncSession = Depends(get_db),
):
    query = select(Decision).where(Decision.decision_date.isnot(None))
    if project_id is not None:
        linked_ids = select(ProjectLink.entity_id).where(
            ProjectLink.project_id == project_id,
            ProjectLink.entity_type == "decision",
        )
        query = query.where(Decision.id.in_(linked_ids))
    result = await db.execute(query.order_by(Decision.decision_date.asc(), Decision.number.asc()))
    rows = result.scalars().all()

    items = [
        DecisionTimelineItem(
            id=d.id,
            number=d.number,
            title=d.decision[:120] if d.decision else f"Decision #{d.number}",
            execution_status=d.execution_status or "made",
            key_people=d.key_people or [],
            decision_date=str(d.decision_date) if d.decision_date else None,
            project_name=None,
        )
        for d in rows
    ]
    return DecisionTimelineResponse(decisions=items, total=len(items))


# --- Single decision ---
@router.get("/decisions/{decision_id}", response_model=DecisionSchema)
async def get_decision(decision_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Decision).where(Decision.id == decision_id))
    d = result.scalar_one_or_none()
    if not d:
        raise NotFoundError("Decision", decision_id)
    return _decision_schema(d)


# --- Create ---
@router.post("/decisions", response_model=DecisionSchema)
async def create_decision(body: DecisionCreate, db: AsyncSession = Depends(get_db)):
    max_num = await db.execute(select(func.coalesce(func.max(Decision.number), 0)))
    next_number = max_num.scalar_one() + 1

    es = body.execution_status or "made"
    max_pos = await db.execute(
        select(func.coalesce(func.max(Decision.position), 0))
        .where(Decision.execution_status == es)
    )
    next_position = max_pos.scalar_one() + 1000

    decision_date = None
    if body.date:
        try:
            decision_date = datetime.strptime(body.date, "%Y-%m-%d").date()
        except ValueError:
            decision_date = datetime.utcnow().date()
    else:
        decision_date = datetime.utcnow().date()

    d = Decision(
        number=next_number,
        decision_date=decision_date,
        decision=body.decision,
        rationale=body.rationale,
        key_people=body.key_people or [],
        execution_status=es,
        project_id=body.project_id,
        position=next_position,
        is_manual=True,
        source_file="manual",
        file_hash="",
    )
    db.add(d)
    await db.commit()
    await db.refresh(d)

    # Writeback to markdown
    append_decision(
        number=d.number,
        decision_date=decision_date,
        decision=body.decision or "",
        rationale=body.rationale,
        key_people=body.key_people or [],
        execution_status=es,
    )

    return _decision_schema(d)


# --- Update ---
@router.patch("/decisions/{decision_id}", response_model=DecisionSchema)
async def update_decision(decision_id: int, body: DecisionUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Decision).where(Decision.id == decision_id))
    d = result.scalar_one_or_none()
    if not d:
        raise NotFoundError("Decision", decision_id)

    if body.decision is not None:
        d.decision = body.decision
    if body.rationale is not None:
        d.rationale = body.rationale
    if body.key_people is not None:
        d.key_people = body.key_people
    if body.execution_status is not None:
        d.execution_status = body.execution_status
    if body.project_id is not None:
        d.project_id = body.project_id
    if body.date is not None:
        try:
            d.decision_date = datetime.strptime(body.date, "%Y-%m-%d").date()
        except ValueError:
            pass

    d.is_manual = True
    d.updated_at = datetime.utcnow()
    await db.commit()
    await db.refresh(d)

    # Writeback to markdown
    update_decision_status(d.number, d.execution_status or "made")

    return _decision_schema(d)


# --- Position update (drag-and-drop) ---
@router.patch("/decisions/{decision_id}/position", response_model=DecisionSchema)
async def update_decision_position(
    decision_id: int, body: DecisionPositionUpdate, db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Decision).where(Decision.id == decision_id))
    d = result.scalar_one_or_none()
    if not d:
        raise NotFoundError("Decision", decision_id)

    d.execution_status = body.execution_status
    d.position = body.position
    d.is_manual = True
    d.updated_at = datetime.utcnow()
    await db.commit()
    await db.refresh(d)

    # Writeback to markdown
    update_decision_status(d.number, body.execution_status)

    return _decision_schema(d)


# --- Delete ---
@router.delete("/decisions/{decision_id}")
async def delete_decision(decision_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Decision).where(Decision.id == decision_id))
    d = result.scalar_one_or_none()
    if not d:
        raise NotFoundError("Decision", decision_id)

    # Writeback to markdown (before delete so we have the number)
    remove_decision(d.number)

    if not d.is_manual:
        db.add(DeletedImport(entity_type="decision", unique_key=str(d.number)))

    await db.delete(d)
    await db.commit()
    return {"ok": True}
