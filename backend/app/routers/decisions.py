from datetime import datetime

from fastapi import APIRouter, Depends, Query
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.decision import Decision
from app.models.project_link import ProjectLink
from app.routers.board_mixin import BoardConfig, add_board_routes
from app.routers.crud_factory import CRUDConfig, WritebackHooks, create_crud_router
from app.schemas.decision import (
    DecisionCreate,
    DecisionSchema,
    DecisionTimelineItem,
    DecisionTimelineResponse,
    DecisionUpdate,
)
from app.services.decision_writeback import (
    append_decision,
    remove_decision,
    update_decision_status,
)

DECISION_STATUSES = ["made", "in_progress", "implemented", "reversed", "superseded"]
DECISION_STATUS_CONFIG = {
    "made":        {"label": "Made",        "color": "blue",   "order": 0},
    "in_progress": {"label": "In Progress", "color": "yellow", "order": 1},
    "implemented": {"label": "Implemented", "color": "green",  "order": 2},
    "reversed":    {"label": "Reversed",    "color": "red",    "order": 3},
    "superseded":  {"label": "Superseded",  "color": "gray",   "order": 4},
}


def _to_schema(d: Decision) -> DecisionSchema:
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
        workstream=None,
        position=d.position,
        transcript_id=None,
        transcript_title=None,
        is_manual=d.is_manual,
    )


async def _create_to_orm(body: DecisionCreate, db: AsyncSession) -> dict:
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

    return {
        "number": next_number,
        "decision_date": decision_date,
        "decision": body.decision,
        "rationale": body.rationale,
        "key_people": body.key_people or [],
        "execution_status": es,
        "position": next_position,
        "is_manual": True,
        "source_file": "manual",
        "file_hash": "",
    }


def _on_create(item: Decision, body: DecisionCreate):
    append_decision(
        number=item.number,
        decision_date=item.decision_date,
        decision=body.decision or "",
        rationale=body.rationale,
        key_people=body.key_people or [],
        execution_status=item.execution_status or "made",
    )


def _on_update(item: Decision, body: DecisionUpdate):
    update_decision_status(item.number, item.execution_status or "made")


def _on_delete(item: Decision):
    remove_decision(item.number)


def _on_position_change(item: Decision, old_status: str, new_status: str):
    update_decision_status(item.number, new_status)


# ── Register custom endpoints first (before /{item_id}) ──────────────

router = APIRouter(tags=["decisions"])


@router.get("/decisions/board")
async def get_decision_board(
    workstream_id: int | None = Query(None),
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
    if workstream_id is not None:
        query = query.where(Decision.workstream_id == workstream_id)
    result = await db.execute(query)
    rows = result.scalars().all()

    columns_map: dict[str, list] = {s: [] for s in DECISION_STATUSES}
    for d in rows:
        bucket = (d.execution_status or "made") if (d.execution_status or "made") in columns_map else "made"
        columns_map[bucket].append(_to_schema(d))

    columns = []
    total = 0
    for status in DECISION_STATUSES:
        cfg = DECISION_STATUS_CONFIG.get(status, {"label": status, "color": "gray", "order": 99})
        decisions = columns_map[status]
        total += len(decisions)
        columns.append({
            "status": status,
            "label": cfg["label"],
            "color": cfg["color"],
            "order": cfg["order"],
            "decisions": decisions,
            "count": len(decisions),
        })

    return {"columns": columns, "total": total}


@router.get("/decisions/timeline", response_model=DecisionTimelineResponse)
async def get_decision_timeline(
    workstream_id: int | None = Query(None),
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
    if workstream_id is not None:
        query = query.where(Decision.workstream_id == workstream_id)
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
            workstream=None,
        )
        for d in rows
    ]
    return DecisionTimelineResponse(decisions=items, total=len(items))


# ── Position endpoint via board mixin ────────────────────────────────

add_board_routes(router, BoardConfig(
    model=Decision,
    schema=DecisionSchema,
    to_schema=_to_schema,
    status_field="execution_status",
    status_values=DECISION_STATUSES,
    status_config=DECISION_STATUS_CONFIG,
    entity_name="Decision",
    items_key="decisions",
    uses_project_links=True,
    project_link_entity_type="decision",
    on_position_change=_on_position_change,
), prefix="/decisions")

# ── CRUD routes (list, detail, create, update, delete) ───────────────

config = CRUDConfig(
    model=Decision,
    schema=DecisionSchema,
    schema_create=DecisionCreate,
    schema_update=DecisionUpdate,
    prefix="/decisions",
    entity_name="Decision",
    tags=["decisions"],
    to_schema=_to_schema,
    create_to_orm=_create_to_orm,
    search_fields=["decision", "rationale"],
    ordering=[("position", "asc"), ("id", "asc")],
    track_deletions=True,
    deletion_entity_type="decision",
    deletion_key=lambda d: str(d.number),
    date_fields=["date"],
    writeback=WritebackHooks(
        on_create=_on_create,
        on_update=_on_update,
        on_delete=_on_delete,
    ),
)

create_crud_router(config, router=router)
