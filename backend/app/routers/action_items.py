"""Backward-compatible action items router.

Thin wrapper over the Task model that maps new task fields back to the
legacy ActionItemSchema so existing consumers keep working.
"""
from datetime import date, datetime

from fastapi import APIRouter, Depends, Query
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.exceptions import NotFoundError
from app.models.deleted_import import DeletedImport
from app.models.task import Task
from app.schemas.action_item import ActionItemCreate, ActionItemSchema, ActionItemUpdate
from app.services.action_writeback import update_action_status_in_markdown

router = APIRouter(tags=["action_items"])

# Map new task statuses back to legacy action item statuses
_TASK_TO_ACTION_STATUS = {
    "TODO": "OPEN",
    "IN_PROGRESS": "IN PROGRESS",
    "IN_REVIEW": "LIKELY_COMPLETED",
    "DONE": "COMPLETED",
    "CANCELLED": "COMPLETED",
}

_ACTION_TO_TASK_STATUS = {
    "OPEN": "TODO",
    "IN PROGRESS": "IN_PROGRESS",
    "COMPLETED": "DONE",
    "LIKELY_COMPLETED": "IN_REVIEW",
    "BLOCKED": "TODO",
}


def _action_schema(t: Task) -> ActionItemSchema:
    return ActionItemSchema(
        id=t.id,
        title=t.title or f"Action {t.number}",
        description=t.description,
        status=_TASK_TO_ACTION_STATUS.get(t.status, t.status),
        owner=t.assignee or t.owner,
        due_date=str(t.due_date) if t.due_date else t.deadline,
        source_transcript_id=None,
        source_transcript_title=None,
        project=None,
        is_manual=t.is_manual,
    )


@router.get("/action-items", response_model=list[ActionItemSchema])
async def list_action_items(
    status: str | None = Query(None),
    owner: str | None = Query(None),
    db: AsyncSession = Depends(get_db),
):
    query = select(Task)
    if status is not None:
        # Map legacy status to task status for filtering
        task_status = _ACTION_TO_TASK_STATUS.get(status, status)
        query = query.where(Task.status == task_status)
    if owner is not None:
        query = query.where(Task.assignee == owner)
    result = await db.execute(query.order_by(Task.created_date, Task.number))
    return [_action_schema(t) for t in result.scalars().all()]


@router.get("/action-items/{item_id}", response_model=ActionItemSchema)
async def get_action_item(item_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Task).where(Task.id == item_id))
    item = result.scalar_one_or_none()
    if not item:
        raise NotFoundError("Action item", item_id)
    return _action_schema(item)


@router.post("/action-items", response_model=ActionItemSchema)
async def create_action_item(body: ActionItemCreate, db: AsyncSession = Depends(get_db)):
    max_result = await db.execute(
        select(func.count()).select_from(Task).where(Task.number.like("M-%"))
    )
    count = max_result.scalar_one()
    number = f"M-{count + 1:03d}"

    task_status = _ACTION_TO_TASK_STATUS.get(body.status, body.status)

    item = Task(
        identifier=f"TASK-{count + 1}",
        number=number,
        title=body.description[:200] if body.description else "Untitled",
        description=body.description,
        assignee=body.owner,
        owner=body.owner,
        deadline=body.deadline,
        context=body.context,
        status=task_status,
        priority="NONE",
        labels=[],
        created_date=date.today(),
        action_date=date.today(),
        position=0,
        is_manual=True,
        source_file="manual",
        file_hash="",
    )
    db.add(item)
    await db.commit()
    await db.refresh(item)
    return _action_schema(item)


@router.patch("/action-items/{item_id}", response_model=ActionItemSchema)
async def update_action_item(item_id: int, body: ActionItemUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Task).where(Task.id == item_id))
    item = result.scalar_one_or_none()
    if not item:
        raise NotFoundError("Action item", item_id)

    old_status = item.status
    if body.description is not None:
        item.description = body.description
        item.title = body.description[:200]
    if body.owner is not None:
        item.assignee = body.owner
        item.owner = body.owner
    if body.deadline is not None:
        item.deadline = body.deadline
    if body.context is not None:
        item.context = body.context
    if body.status is not None:
        task_status = _ACTION_TO_TASK_STATUS.get(body.status, body.status)
        item.status = task_status
        if task_status == "DONE" and not item.completed_date:
            item.completed_date = date.today()

    item.is_manual = True
    item.updated_at = datetime.utcnow()
    await db.commit()
    await db.refresh(item)

    if body.status and _ACTION_TO_TASK_STATUS.get(body.status, body.status) != old_status:
        update_action_status_in_markdown(item.number, body.status)

    return _action_schema(item)


@router.post("/action-items/{item_id}/complete", response_model=ActionItemSchema)
async def complete_action_item(item_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Task).where(Task.id == item_id))
    item = result.scalar_one_or_none()
    if not item:
        raise NotFoundError("Action item", item_id)

    item.status = "DONE"
    item.completed_date = date.today()
    item.is_manual = True
    item.updated_at = datetime.utcnow()
    await db.commit()
    await db.refresh(item)

    update_action_status_in_markdown(item.number, "COMPLETED")
    return _action_schema(item)


@router.delete("/action-items/{item_id}")
async def delete_action_item(item_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Task).where(Task.id == item_id))
    item = result.scalar_one_or_none()
    if not item:
        raise NotFoundError("Action item", item_id)

    if not item.is_manual:
        db.add(DeletedImport(entity_type="task", unique_key=f"{item.number}:{item.status}"))

    await db.delete(item)
    await db.commit()
    return {"ok": True}
