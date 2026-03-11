from datetime import datetime

from fastapi import APIRouter, Depends, Query
from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.open_thread import OpenThread
from app.models.project_link import ProjectLink
from app.routers.board_mixin import BoardConfig, add_board_routes
from app.routers.crud_factory import CRUDConfig, WritebackHooks, create_crud_router
from app.schemas.open_thread import (
    OpenThreadCreate,
    OpenThreadSchema,
    OpenThreadUpdate,
)
from app.services.thread_writeback import (
    append_thread,
    move_thread,
    remove_thread,
    update_thread_fields,
)

THREAD_STATUSES = ["OPEN", "WATCHING", "CLOSED"]
THREAD_STATUS_CONFIG = {
    "OPEN":     {"label": "Open",     "color": "red",    "order": 0},
    "WATCHING": {"label": "Watching", "color": "yellow", "order": 1},
    "CLOSED":   {"label": "Closed",   "color": "green",  "order": 2},
}


def _to_schema(t: OpenThread) -> OpenThreadSchema:
    return OpenThreadSchema(
        id=t.id,
        title=t.title,
        description=t.context,
        status=t.status,
        priority=t.severity,
        owner=None,
        opened_date=t.first_raised,
        last_discussed=None,
        workstream=None,
        severity=t.severity,
        trend=t.trend,
        position=t.position,
        question=t.question,
        why_it_matters=t.why_it_matters,
        resolution=t.resolution,
        is_manual=t.is_manual,
    )


async def _create_to_orm(body: OpenThreadCreate, db: AsyncSession) -> dict:
    max_num = await db.execute(select(func.coalesce(func.max(OpenThread.number), 0)))
    next_number = max_num.scalar_one() + 1

    max_pos = await db.execute(
        select(func.coalesce(func.max(OpenThread.position), 0))
        .where(OpenThread.status == body.status)
    )
    next_position = max_pos.scalar_one() + 1000

    return {
        "number": next_number,
        "title": body.title,
        "status": body.status,
        "first_raised": body.first_raised or datetime.utcnow().strftime("%Y-%m-%d"),
        "context": body.context,
        "question": body.question,
        "why_it_matters": body.why_it_matters,
        "severity": body.severity,
        "trend": body.trend,
        "position": next_position,
        "is_manual": True,
        "source_file": "manual",
        "file_hash": "",
    }


def _on_create(item: OpenThread, body: OpenThreadCreate):
    append_thread(
        number=item.number,
        title=body.title,
        status=body.status or "OPEN",
        first_raised=body.first_raised or datetime.utcnow().strftime("%Y-%m-%d"),
        context=body.context,
        question=body.question,
        why_it_matters=body.why_it_matters,
    )


def _on_update(item: OpenThread, body: OpenThreadUpdate):
    if body.status is not None:
        # Status changed — move in markdown
        move_thread(item.number, item.status, body.status, body.resolution)
    else:
        update_thread_fields(
            number=item.number,
            current_status=item.status,
            title=body.title,
            context=body.context,
            question=body.question,
            why_it_matters=body.why_it_matters,
            resolution=body.resolution,
            first_raised=body.first_raised,
        )


def _on_delete(item: OpenThread):
    remove_thread(item.number, item.status)


def _on_position_change(item: OpenThread, old_status: str, new_status: str):
    move_thread(item.number, old_status, new_status)


# ── Custom endpoints first (before /{item_id}) ───────────────────────

router = APIRouter(tags=["open_threads"])


@router.get("/open-threads/board")
async def get_thread_board(
    project_id: int | None = Query(None),
    db: AsyncSession = Depends(get_db),
):
    query = select(OpenThread).order_by(OpenThread.position, OpenThread.id)
    if project_id is not None:
        linked_ids = select(ProjectLink.entity_id).where(
            ProjectLink.project_id == project_id,
            ProjectLink.entity_type == "open_thread",
        )
        query = query.where(OpenThread.id.in_(linked_ids))
    result = await db.execute(query)
    rows = result.scalars().all()

    columns_map: dict[str, list] = {s: [] for s in THREAD_STATUSES}
    for t in rows:
        bucket = t.status if t.status in columns_map else "OPEN"
        columns_map[bucket].append(_to_schema(t))

    columns = []
    total = 0
    for status in THREAD_STATUSES:
        cfg = THREAD_STATUS_CONFIG.get(status, {"label": status, "color": "gray", "order": 99})
        threads = columns_map[status]
        total += len(threads)
        columns.append({
            "status": status,
            "label": cfg["label"],
            "color": cfg["color"],
            "order": cfg["order"],
            "threads": threads,
            "count": len(threads),
        })

    return {"columns": columns, "total": total}


# ── Position endpoint via board mixin ────────────────────────────────

add_board_routes(router, BoardConfig(
    model=OpenThread,
    schema=OpenThreadSchema,
    to_schema=_to_schema,
    status_field="status",
    status_values=THREAD_STATUSES,
    status_config=THREAD_STATUS_CONFIG,
    entity_name="Open thread",
    items_key="threads",
    uses_project_links=True,
    project_link_entity_type="open_thread",
    on_position_change=_on_position_change,
), prefix="/open-threads")

# ── CRUD routes ──────────────────────────────────────────────────────

config = CRUDConfig(
    model=OpenThread,
    schema=OpenThreadSchema,
    schema_create=OpenThreadCreate,
    schema_update=OpenThreadUpdate,
    prefix="/open-threads",
    entity_name="Open thread",
    tags=["open_threads"],
    to_schema=_to_schema,
    create_to_orm=_create_to_orm,
    search_fields=["title", "context", "question"],
    ordering=[("position", "asc"), ("id", "asc")],
    track_deletions=True,
    deletion_entity_type="open_thread",
    deletion_key=lambda t: f"{t.number}:{t.status}",
    writeback=WritebackHooks(
        on_create=_on_create,
        on_update=_on_update,
        on_delete=_on_delete,
    ),
)

create_crud_router(config, router=router)
