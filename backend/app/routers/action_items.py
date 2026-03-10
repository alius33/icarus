from datetime import date, datetime

from fastapi import APIRouter, Depends, Query
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.exceptions import NotFoundError
from app.models.action_item import ActionItem
from app.models.deleted_import import DeletedImport
from app.schemas.action_item import ActionItemCreate, ActionItemSchema, ActionItemUpdate
from app.services.action_writeback import update_action_status_in_markdown

router = APIRouter(tags=["action_items"])


def _action_schema(a: ActionItem) -> ActionItemSchema:
    return ActionItemSchema(
        id=a.id,
        title=f"Action {a.number}",
        description=a.description,
        status=a.status,
        owner=a.owner,
        due_date=a.deadline,
        source_transcript_id=None,
        source_transcript_title=None,
        workstream=None,
        is_manual=a.is_manual,
    )


@router.get("/action-items", response_model=list[ActionItemSchema])
async def list_action_items(
    status: str | None = Query(None),
    owner: str | None = Query(None),
    db: AsyncSession = Depends(get_db),
):
    query = select(ActionItem)
    if status is not None:
        query = query.where(ActionItem.status == status)
    if owner is not None:
        query = query.where(ActionItem.owner == owner)
    result = await db.execute(query.order_by(ActionItem.action_date, ActionItem.number))
    return [_action_schema(a) for a in result.scalars().all()]


@router.get("/action-items/{item_id}", response_model=ActionItemSchema)
async def get_action_item(item_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(ActionItem).where(ActionItem.id == item_id))
    item = result.scalar_one_or_none()
    if not item:
        raise NotFoundError("Action item", item_id)
    return _action_schema(item)


@router.post("/action-items", response_model=ActionItemSchema)
async def create_action_item(body: ActionItemCreate, db: AsyncSession = Depends(get_db)):
    max_result = await db.execute(
        select(func.count()).select_from(ActionItem).where(ActionItem.number.like("M-%"))
    )
    count = max_result.scalar_one()
    number = f"M-{count + 1:03d}"

    item = ActionItem(
        number=number,
        action_date=datetime.utcnow().date(),
        description=body.description,
        owner=body.owner,
        deadline=body.deadline,
        context=body.context,
        status=body.status,
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
    result = await db.execute(select(ActionItem).where(ActionItem.id == item_id))
    item = result.scalar_one_or_none()
    if not item:
        raise NotFoundError("Action item", item_id)

    old_status = item.status
    if body.description is not None:
        item.description = body.description
    if body.owner is not None:
        item.owner = body.owner
    if body.deadline is not None:
        item.deadline = body.deadline
    if body.context is not None:
        item.context = body.context
    if body.status is not None:
        item.status = body.status
        if body.status == "COMPLETED" and not item.completed_date:
            item.completed_date = date.today()

    item.is_manual = True
    item.updated_at = datetime.utcnow()
    await db.commit()
    await db.refresh(item)

    if body.status and body.status != old_status:
        update_action_status_in_markdown(item.number, item.status)

    return _action_schema(item)


@router.post("/action-items/{item_id}/complete", response_model=ActionItemSchema)
async def complete_action_item(item_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(ActionItem).where(ActionItem.id == item_id))
    item = result.scalar_one_or_none()
    if not item:
        raise NotFoundError("Action item", item_id)

    item.status = "COMPLETED"
    item.completed_date = date.today()
    item.is_manual = True
    item.updated_at = datetime.utcnow()
    await db.commit()
    await db.refresh(item)

    update_action_status_in_markdown(item.number, "COMPLETED")
    return _action_schema(item)


@router.delete("/action-items/{item_id}")
async def delete_action_item(item_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(ActionItem).where(ActionItem.id == item_id))
    item = result.scalar_one_or_none()
    if not item:
        raise NotFoundError("Action item", item_id)

    if not item.is_manual:
        db.add(DeletedImport(entity_type="action_item", unique_key=f"{item.number}:{item.status}"))

    await db.delete(item)
    await db.commit()
    return {"ok": True}
