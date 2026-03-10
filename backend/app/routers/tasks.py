from datetime import date, datetime

from fastapi import APIRouter, Depends, Query
from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.exceptions import NotFoundError
from app.models.deleted_import import DeletedImport
from app.models.project import Project
from app.models.task import Task, TASK_STATUSES
from app.schemas.task import (
    TaskBoardColumn,
    TaskBoardResponse,
    TaskCreate,
    TaskPositionUpdate,
    TaskSchema,
    TaskTimelineItem,
    TaskTimelineResponse,
    TaskUpdate,
)
from app.services.action_writeback import update_action_status_in_markdown

router = APIRouter(tags=["tasks"])

STATUS_CONFIG = {
    "TODO":        {"label": "Todo",        "color": "blue",   "order": 0},
    "IN_PROGRESS": {"label": "In Progress", "color": "yellow", "order": 1},
    "IN_REVIEW":   {"label": "In Review",   "color": "purple", "order": 2},
    "DONE":        {"label": "Done",        "color": "green",  "order": 3},
    "CANCELLED":   {"label": "Cancelled",   "color": "red",    "order": 4},
}

# Reverse mapping for markdown writeback
_TASK_TO_MARKDOWN_STATUS = {
    "TODO": "OPEN",
    "IN_PROGRESS": "IN PROGRESS",
    "IN_REVIEW": "LIKELY_COMPLETED",
    "DONE": "COMPLETED",
    "CANCELLED": "COMPLETED",
}


async def _task_schema(t: Task, db: AsyncSession) -> TaskSchema:
    """Convert a Task ORM instance to a TaskSchema response."""
    project_name = None
    if t.project_id:
        p_result = await db.execute(select(Project.name).where(Project.id == t.project_id))
        project_name = p_result.scalar_one_or_none()

    parent_identifier = None
    if t.parent_id:
        p_result = await db.execute(select(Task.identifier).where(Task.id == t.parent_id))
        parent_identifier = p_result.scalar_one_or_none()

    sub_count_result = await db.execute(
        select(func.count(Task.id)).where(Task.parent_id == t.id)
    )
    sub_task_count = sub_count_result.scalar_one()

    return TaskSchema(
        id=t.id,
        identifier=t.identifier,
        title=t.title,
        description=t.description,
        status=t.status,
        priority=t.priority or "NONE",
        assignee=t.assignee,
        labels=t.labels or [],
        due_date=str(t.due_date) if t.due_date else None,
        start_date=str(t.start_date) if t.start_date else None,
        estimate=t.estimate,
        position=t.position or 0,
        project_id=t.project_id,
        project_name=project_name,
        parent_id=t.parent_id,
        parent_identifier=parent_identifier,
        sub_task_count=sub_task_count,
        created_date=str(t.created_date) if t.created_date else None,
        completed_date=str(t.completed_date) if t.completed_date else None,
        is_manual=t.is_manual,
    )


async def _task_schema_light(t: Task, project_name: str | None = None) -> TaskSchema:
    """Lightweight conversion without extra DB lookups (for list views)."""
    return TaskSchema(
        id=t.id,
        identifier=t.identifier,
        title=t.title,
        description=t.description,
        status=t.status,
        priority=t.priority or "NONE",
        assignee=t.assignee,
        labels=t.labels or [],
        due_date=str(t.due_date) if t.due_date else None,
        start_date=str(t.start_date) if t.start_date else None,
        estimate=t.estimate,
        position=t.position or 0,
        project_id=t.project_id,
        project_name=project_name,
        parent_id=t.parent_id,
        parent_identifier=None,
        sub_task_count=0,
        created_date=str(t.created_date) if t.created_date else None,
        completed_date=str(t.completed_date) if t.completed_date else None,
        is_manual=t.is_manual,
    )


async def _generate_identifier(project_id: int | None, db: AsyncSession) -> str:
    """Generate a human-readable identifier like CLARA-42."""
    prefix = "TASK"
    if project_id:
        p_result = await db.execute(select(Project.name).where(Project.id == project_id))
        name = p_result.scalar_one_or_none()
        if name:
            prefix = name.upper().replace(" ", "")[:5]

    count_result = await db.execute(
        select(func.count(Task.id)).where(Task.identifier.like(f"{prefix}-%"))
    )
    count = count_result.scalar_one()
    return f"{prefix}-{count + 1}"


# ── List ─────────────────────────────────────────────────────────────

@router.get("/tasks", response_model=list[TaskSchema])
async def list_tasks(
    status: str | None = Query(None),
    priority: str | None = Query(None),
    assignee: str | None = Query(None),
    project_id: int | None = Query(None),
    label: str | None = Query(None),
    search: str | None = Query(None),
    db: AsyncSession = Depends(get_db),
):
    query = select(Task, Project.name.label("project_name")).outerjoin(
        Project, Task.project_id == Project.id
    )

    if status:
        query = query.where(Task.status == status)
    if priority:
        query = query.where(Task.priority == priority)
    if assignee:
        query = query.where(Task.assignee == assignee)
    if project_id:
        query = query.where(Task.project_id == project_id)
    if label:
        query = query.where(Task.labels.any(label))
    if search:
        pattern = f"%{search}%"
        query = query.where(or_(
            Task.title.ilike(pattern),
            Task.description.ilike(pattern),
            Task.identifier.ilike(pattern),
        ))

    query = query.order_by(Task.position, Task.id)
    result = await db.execute(query)
    rows = result.all()

    return [await _task_schema_light(t, pn) for t, pn in rows]


# ── Board ────────────────────────────────────────────────────────────

@router.get("/tasks/board", response_model=TaskBoardResponse)
async def get_task_board(
    project_id: int | None = Query(None),
    db: AsyncSession = Depends(get_db),
):
    query = select(Task, Project.name.label("project_name")).outerjoin(
        Project, Task.project_id == Project.id
    )
    if project_id:
        query = query.where(Task.project_id == project_id)

    query = query.order_by(Task.position, Task.id)
    result = await db.execute(query)
    rows = result.all()

    # Group by status
    columns_map: dict[str, list[TaskSchema]] = {s: [] for s in TASK_STATUSES}
    for t, pn in rows:
        schema = await _task_schema_light(t, pn)
        bucket = t.status if t.status in columns_map else "TODO"
        columns_map[bucket].append(schema)

    columns = []
    total = 0
    for status in TASK_STATUSES:
        cfg = STATUS_CONFIG.get(status, {"label": status, "color": "gray", "order": 99})
        tasks = columns_map[status]
        total += len(tasks)
        columns.append(TaskBoardColumn(
            status=status,
            label=cfg["label"],
            color=cfg["color"],
            order=cfg["order"],
            tasks=tasks,
            count=len(tasks),
        ))

    return TaskBoardResponse(columns=columns, total=total)


# ── Timeline ─────────────────────────────────────────────────────────

@router.get("/tasks/timeline", response_model=TaskTimelineResponse)
async def get_task_timeline(
    project_id: int | None = Query(None),
    from_date: str | None = Query(None),
    to_date: str | None = Query(None),
    db: AsyncSession = Depends(get_db),
):
    query = select(Task, Project.name.label("project_name")).outerjoin(
        Project, Task.project_id == Project.id
    ).where(or_(Task.start_date.isnot(None), Task.due_date.isnot(None)))

    if project_id:
        query = query.where(Task.project_id == project_id)
    if from_date:
        query = query.where(or_(
            Task.due_date >= from_date,
            Task.start_date >= from_date,
        ))
    if to_date:
        query = query.where(or_(
            Task.start_date <= to_date,
            Task.due_date <= to_date,
        ))

    query = query.order_by(Task.start_date.nulls_last(), Task.due_date.nulls_last(), Task.id)
    result = await db.execute(query)
    rows = result.all()

    tasks = [
        TaskTimelineItem(
            id=t.id,
            identifier=t.identifier,
            title=t.title,
            status=t.status,
            priority=t.priority or "NONE",
            assignee=t.assignee,
            start_date=str(t.start_date) if t.start_date else None,
            due_date=str(t.due_date) if t.due_date else None,
            project_name=pn,
        )
        for t, pn in rows
    ]

    return TaskTimelineResponse(tasks=tasks, total=len(tasks))


# ── Labels ───────────────────────────────────────────────────────────

@router.get("/tasks/labels", response_model=list[str])
async def get_task_labels(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(func.unnest(Task.labels)).distinct()
    )
    return sorted([row[0] for row in result.all() if row[0]])


# ── Single ───────────────────────────────────────────────────────────

@router.get("/tasks/{task_id}", response_model=TaskSchema)
async def get_task(task_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Task).where(Task.id == task_id))
    task = result.scalar_one_or_none()
    if not task:
        raise NotFoundError("Task", task_id)
    return await _task_schema(task, db)


# ── Create ───────────────────────────────────────────────────────────

@router.post("/tasks", response_model=TaskSchema, status_code=201)
async def create_task(body: TaskCreate, db: AsyncSession = Depends(get_db)):
    identifier = await _generate_identifier(body.project_id, db)

    # Generate backward-compat M-number
    count_result = await db.execute(
        select(func.count(Task.id)).where(Task.number.like("M-%"))
    )
    m_count = count_result.scalar_one()
    number = f"M-{m_count + 1:03d}"

    # Get max position in target status column
    max_pos_result = await db.execute(
        select(func.coalesce(func.max(Task.position), 0))
        .where(Task.status == body.status)
    )
    max_pos = max_pos_result.scalar_one()

    due_date_val = None
    if body.due_date:
        try:
            due_date_val = date.fromisoformat(body.due_date)
        except ValueError:
            pass

    start_date_val = None
    if body.start_date:
        try:
            start_date_val = date.fromisoformat(body.start_date)
        except ValueError:
            pass

    task = Task(
        identifier=identifier,
        number=number,
        title=body.title,
        description=body.description,
        status=body.status,
        priority=body.priority,
        assignee=body.assignee,
        owner=body.assignee,  # backward compat
        labels=body.labels or [],
        due_date=due_date_val,
        start_date=start_date_val,
        deadline=body.due_date,  # backward compat string
        estimate=body.estimate,
        position=max_pos + 1000,
        project_id=body.project_id,
        parent_id=body.parent_id,
        created_date=date.today(),
        action_date=date.today(),  # backward compat
        is_manual=True,
        source_file="manual",
        file_hash="",
    )
    db.add(task)
    await db.commit()
    await db.refresh(task)
    return await _task_schema(task, db)


# ── Update ───────────────────────────────────────────────────────────

@router.patch("/tasks/{task_id}", response_model=TaskSchema)
async def update_task(task_id: int, body: TaskUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Task).where(Task.id == task_id))
    task = result.scalar_one_or_none()
    if not task:
        raise NotFoundError("Task", task_id)

    old_status = task.status

    if body.title is not None:
        task.title = body.title
    if body.description is not None:
        task.description = body.description
    if body.status is not None:
        task.status = body.status
        if body.status == "DONE" and not task.completed_date:
            task.completed_date = date.today()
    if body.priority is not None:
        task.priority = body.priority
    if body.assignee is not None:
        task.assignee = body.assignee
        task.owner = body.assignee  # backward compat
    if body.labels is not None:
        task.labels = body.labels
    if body.due_date is not None:
        try:
            task.due_date = date.fromisoformat(body.due_date)
            task.deadline = body.due_date
        except ValueError:
            task.deadline = body.due_date
    if body.start_date is not None:
        try:
            task.start_date = date.fromisoformat(body.start_date)
        except ValueError:
            pass
    if body.estimate is not None:
        task.estimate = body.estimate
    if body.project_id is not None:
        task.project_id = body.project_id
    if body.parent_id is not None:
        task.parent_id = body.parent_id

    task.is_manual = True
    task.updated_at = datetime.utcnow()
    await db.commit()
    await db.refresh(task)

    # Markdown writeback on status change
    if body.status and body.status != old_status:
        md_status = _TASK_TO_MARKDOWN_STATUS.get(body.status, body.status)
        update_action_status_in_markdown(task.number, md_status)

    return await _task_schema(task, db)


# ── Position (drag-and-drop) ─────────────────────────────────────────

@router.patch("/tasks/{task_id}/position", response_model=TaskSchema)
async def update_task_position(
    task_id: int, body: TaskPositionUpdate, db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Task).where(Task.id == task_id))
    task = result.scalar_one_or_none()
    if not task:
        raise NotFoundError("Task", task_id)

    old_status = task.status
    task.status = body.status
    task.position = body.position
    task.updated_at = datetime.utcnow()

    if body.status == "DONE" and not task.completed_date:
        task.completed_date = date.today()

    task.is_manual = True
    await db.commit()
    await db.refresh(task)

    if body.status != old_status:
        md_status = _TASK_TO_MARKDOWN_STATUS.get(body.status, body.status)
        update_action_status_in_markdown(task.number, md_status)

    return await _task_schema(task, db)


# ── Complete ─────────────────────────────────────────────────────────

@router.post("/tasks/{task_id}/complete", response_model=TaskSchema)
async def complete_task(task_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Task).where(Task.id == task_id))
    task = result.scalar_one_or_none()
    if not task:
        raise NotFoundError("Task", task_id)

    task.status = "DONE"
    task.completed_date = date.today()
    task.is_manual = True
    task.updated_at = datetime.utcnow()
    await db.commit()
    await db.refresh(task)

    update_action_status_in_markdown(task.number, "COMPLETED")
    return await _task_schema(task, db)


# ── Delete ───────────────────────────────────────────────────────────

@router.delete("/tasks/{task_id}")
async def delete_task(task_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Task).where(Task.id == task_id))
    task = result.scalar_one_or_none()
    if not task:
        raise NotFoundError("Task", task_id)

    if not task.is_manual:
        db.add(DeletedImport(entity_type="task", unique_key=f"{task.number}:{task.status}"))

    await db.delete(task)
    await db.commit()
    return {"ok": True}


