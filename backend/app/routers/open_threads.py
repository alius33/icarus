from fastapi import APIRouter, Depends, Query
from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db, utcnow
from app.exceptions import NotFoundError
from app.models.deleted_import import DeletedImport
from app.models.open_thread import OpenThread
from app.services.thread_writeback import (
    append_thread,
    move_thread,
    remove_thread,
    update_thread_fields,
)
from app.models.project_link import ProjectLink
from app.schemas.open_thread import (
    OpenThreadCreate,
    OpenThreadPositionUpdate,
    OpenThreadSchema,
    OpenThreadUpdate,
    ThreadBoardColumn,
    ThreadBoardResponse,
)

router = APIRouter(tags=["open_threads"])

THREAD_STATUSES = ["OPEN", "WATCHING", "CLOSED"]
THREAD_STATUS_CONFIG = {
    "OPEN":     {"label": "Open",     "color": "red",    "order": 0},
    "WATCHING": {"label": "Watching", "color": "yellow", "order": 1},
    "CLOSED":   {"label": "Closed",   "color": "green",  "order": 2},
}


def _thread_schema(t: OpenThread) -> OpenThreadSchema:
    return OpenThreadSchema(
        id=t.id,
        title=t.title,
        description=t.context,
        status=t.status,
        priority=t.severity,
        owner=None,
        opened_date=t.first_raised,
        last_discussed=None,
        project=None,
        severity=t.severity,
        trend=t.trend,
        position=t.position,
        question=t.question,
        why_it_matters=t.why_it_matters,
        resolution=t.resolution,
        is_manual=t.is_manual,
    )


# --- List (flat) ---
@router.get("/open-threads", response_model=list[OpenThreadSchema])
async def list_open_threads(
    status: str | None = Query(None),
    severity: str | None = Query(None),
    trend: str | None = Query(None),
    search: str | None = Query(None),
    project_id: int | None = Query(None),
    db: AsyncSession = Depends(get_db),
):
    query = select(OpenThread)
    if project_id is not None:
        linked_ids = select(ProjectLink.entity_id).where(
            ProjectLink.project_id == project_id,
            ProjectLink.entity_type == "open_thread",
        )
        query = query.where(OpenThread.id.in_(linked_ids))
    if status is not None:
        query = query.where(OpenThread.status == status)
    if severity is not None:
        query = query.where(OpenThread.severity == severity)
    if trend is not None:
        query = query.where(OpenThread.trend == trend)
    if search:
        pattern = f"%{search}%"
        query = query.where(or_(
            OpenThread.title.ilike(pattern),
            OpenThread.context.ilike(pattern),
            OpenThread.question.ilike(pattern),
        ))
    result = await db.execute(query.order_by(OpenThread.position, OpenThread.id))
    return [_thread_schema(t) for t in result.scalars().all()]


# --- Board (grouped by status) ---
@router.get("/open-threads/board", response_model=ThreadBoardResponse)
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

    columns_map: dict[str, list[OpenThreadSchema]] = {s: [] for s in THREAD_STATUSES}
    for t in rows:
        bucket = t.status if t.status in columns_map else "OPEN"
        columns_map[bucket].append(_thread_schema(t))

    columns = []
    total = 0
    for status in THREAD_STATUSES:
        cfg = THREAD_STATUS_CONFIG.get(status, {"label": status, "color": "gray", "order": 99})
        threads = columns_map[status]
        total += len(threads)
        columns.append(ThreadBoardColumn(
            status=status,
            label=cfg["label"],
            color=cfg["color"],
            order=cfg["order"],
            threads=threads,
            count=len(threads),
        ))

    return ThreadBoardResponse(columns=columns, total=total)


# --- Single thread ---
@router.get("/open-threads/{thread_id}", response_model=OpenThreadSchema)
async def get_open_thread(thread_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(OpenThread).where(OpenThread.id == thread_id))
    thread = result.scalar_one_or_none()
    if not thread:
        raise NotFoundError("Open thread", thread_id)
    return _thread_schema(thread)


# --- Create ---
@router.post("/open-threads", response_model=OpenThreadSchema)
async def create_open_thread(body: OpenThreadCreate, db: AsyncSession = Depends(get_db)):
    max_num = await db.execute(select(func.coalesce(func.max(OpenThread.number), 0)))
    next_number = max_num.scalar_one() + 1

    max_pos = await db.execute(
        select(func.coalesce(func.max(OpenThread.position), 0))
        .where(OpenThread.status == body.status)
    )
    next_position = max_pos.scalar_one() + 1000

    thread = OpenThread(
        number=next_number,
        title=body.title,
        status=body.status,
        first_raised=body.first_raised or utcnow().strftime("%Y-%m-%d"),
        context=body.context,
        question=body.question,
        why_it_matters=body.why_it_matters,
        severity=body.severity,
        trend=body.trend,
        position=next_position,
        is_manual=True,
        source_file="manual",
        file_hash="",
    )
    db.add(thread)
    await db.commit()
    await db.refresh(thread)

    # Writeback to markdown
    append_thread(
        number=thread.number,
        title=body.title,
        status=body.status or "OPEN",
        first_raised=body.first_raised or utcnow().strftime("%Y-%m-%d"),
        context=body.context,
        question=body.question,
        why_it_matters=body.why_it_matters,
    )

    return _thread_schema(thread)


# --- Update ---
@router.patch("/open-threads/{thread_id}", response_model=OpenThreadSchema)
async def update_open_thread(thread_id: int, body: OpenThreadUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(OpenThread).where(OpenThread.id == thread_id))
    thread = result.scalar_one_or_none()
    if not thread:
        raise NotFoundError("Open thread", thread_id)

    # Capture old status before mutation for writeback
    old_status = thread.status

    if body.title is not None:
        thread.title = body.title
    if body.context is not None:
        thread.context = body.context
    if body.question is not None:
        thread.question = body.question
    if body.why_it_matters is not None:
        thread.why_it_matters = body.why_it_matters
    if body.status is not None:
        thread.status = body.status
    if body.resolution is not None:
        thread.resolution = body.resolution
    if body.first_raised is not None:
        thread.first_raised = body.first_raised
    if body.severity is not None:
        thread.severity = body.severity
    if body.trend is not None:
        thread.trend = body.trend

    thread.is_manual = True
    thread.updated_at = utcnow()
    await db.commit()
    await db.refresh(thread)

    # Writeback to markdown
    if body.status is not None and body.status != old_status:
        move_thread(thread.number, old_status, body.status, body.resolution)
    else:
        update_thread_fields(
            number=thread.number,
            current_status=thread.status,
            title=body.title,
            context=body.context,
            question=body.question,
            why_it_matters=body.why_it_matters,
            resolution=body.resolution,
            first_raised=body.first_raised,
        )

    return _thread_schema(thread)


# --- Position update (drag-and-drop) ---
@router.patch("/open-threads/{thread_id}/position", response_model=OpenThreadSchema)
async def update_thread_position(
    thread_id: int, body: OpenThreadPositionUpdate, db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(OpenThread).where(OpenThread.id == thread_id))
    thread = result.scalar_one_or_none()
    if not thread:
        raise NotFoundError("Open thread", thread_id)

    # Capture old status before mutation for writeback
    old_status = thread.status

    thread.status = body.status
    thread.position = body.position
    thread.is_manual = True
    thread.updated_at = utcnow()
    await db.commit()
    await db.refresh(thread)

    # Writeback to markdown (status change from drag-and-drop)
    if body.status != old_status:
        move_thread(thread.number, old_status, body.status)

    return _thread_schema(thread)


# --- Delete ---
@router.delete("/open-threads/{thread_id}")
async def delete_open_thread(thread_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(OpenThread).where(OpenThread.id == thread_id))
    thread = result.scalar_one_or_none()
    if not thread:
        raise NotFoundError("Open thread", thread_id)

    # Writeback to markdown (before delete)
    remove_thread(thread.number, thread.status)

    if not thread.is_manual:
        db.add(DeletedImport(entity_type="open_thread", unique_key=f"{thread.number}:{thread.status}"))

    await db.delete(thread)
    await db.commit()
    return {"ok": True}
