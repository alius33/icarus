from datetime import datetime

from fastapi import APIRouter, Depends, Query
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.exceptions import NotFoundError
from app.models.deleted_import import DeletedImport
from app.models.open_thread import OpenThread
from app.schemas.open_thread import OpenThreadCreate, OpenThreadSchema, OpenThreadUpdate

router = APIRouter(tags=["open_threads"])


def _thread_schema(t: OpenThread) -> OpenThreadSchema:
    return OpenThreadSchema(
        id=t.id,
        title=t.title,
        description=t.context,
        status=t.status,
        priority=None,
        owner=None,
        opened_date=t.first_raised,
        last_discussed=None,
        workstream=None,
        severity=t.severity,
        trend=t.trend,
        is_manual=t.is_manual,
    )


@router.get("/open-threads", response_model=list[OpenThreadSchema])
async def list_open_threads(
    status: str | None = Query(None),
    db: AsyncSession = Depends(get_db),
):
    query = select(OpenThread)
    if status is not None:
        query = query.where(OpenThread.status == status)
    result = await db.execute(query.order_by(OpenThread.number))
    return [_thread_schema(t) for t in result.scalars().all()]


@router.get("/open-threads/{thread_id}", response_model=OpenThreadSchema)
async def get_open_thread(thread_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(OpenThread).where(OpenThread.id == thread_id))
    thread = result.scalar_one_or_none()
    if not thread:
        raise NotFoundError("Open thread", thread_id)
    return _thread_schema(thread)


@router.post("/open-threads", response_model=OpenThreadSchema)
async def create_open_thread(body: OpenThreadCreate, db: AsyncSession = Depends(get_db)):
    max_num = await db.execute(select(func.coalesce(func.max(OpenThread.number), 0)))
    next_number = max_num.scalar_one() + 1

    thread = OpenThread(
        number=next_number,
        title=body.title,
        status=body.status,
        first_raised=body.first_raised or datetime.utcnow().strftime("%Y-%m-%d"),
        context=body.context,
        question=body.question,
        why_it_matters=body.why_it_matters,
        is_manual=True,
        source_file="manual",
        file_hash="",
    )
    db.add(thread)
    await db.commit()
    await db.refresh(thread)
    return _thread_schema(thread)


@router.patch("/open-threads/{thread_id}", response_model=OpenThreadSchema)
async def update_open_thread(thread_id: int, body: OpenThreadUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(OpenThread).where(OpenThread.id == thread_id))
    thread = result.scalar_one_or_none()
    if not thread:
        raise NotFoundError("Open thread", thread_id)

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
    thread.updated_at = datetime.utcnow()
    await db.commit()
    await db.refresh(thread)
    return _thread_schema(thread)


@router.delete("/open-threads/{thread_id}")
async def delete_open_thread(thread_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(OpenThread).where(OpenThread.id == thread_id))
    thread = result.scalar_one_or_none()
    if not thread:
        raise NotFoundError("Open thread", thread_id)

    if not thread.is_manual:
        db.add(DeletedImport(entity_type="open_thread", unique_key=f"{thread.number}:{thread.status}"))

    await db.delete(thread)
    await db.commit()
    return {"ok": True}
