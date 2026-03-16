from datetime import date, timedelta

from fastapi import APIRouter, BackgroundTasks, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, joinedload

from app.database import get_db
from app.exceptions import NotFoundError
from app.models.weekly_plan import WeeklyPlan
from app.models.weekly_plan_action import WeeklyPlanAction
from app.models.deliverable_progress_snapshot import DeliverableProgressSnapshot
from app.schemas.weekly_plan import (
    WeeklyPlanActionBase,
    WeeklyPlanActionCreate,
    WeeklyPlanActionUpdate,
    WeeklyPlanBase,
    WeeklyPlanCreate,
    WeeklyPlanFull,
    WeeklyPlanUpdate,
)
from app.schemas.programme_deliverable import ProgressSnapshotBase
from app.services.weekly_plan_export import export_plans_to_seed

router = APIRouter(tags=["weekly-plans"])

PROGRAMME_START = date(2026, 2, 23)  # Monday 23 Feb 2026


def _current_week_number() -> int:
    """Calculate current week number based on programme start date."""
    today = date.today()
    days_elapsed = (today - PROGRAMME_START).days
    if days_elapsed < 0:
        return 1
    return (days_elapsed // 7) + 1


def _week_dates(week_num: int) -> tuple[date, date]:
    """Get Mon-Fri dates for a given week number."""
    start = PROGRAMME_START + timedelta(weeks=week_num - 1)
    end = start + timedelta(days=4)  # Friday
    return start, end


def _action_schema(a: WeeklyPlanAction) -> WeeklyPlanActionBase:
    # Resolve transcript title from relationship if available
    transcript_title = None
    if a.source_transcript_id and a.source_transcript:
        transcript_title = a.source_transcript.title
    return WeeklyPlanActionBase(
        id=a.id,
        weekly_plan_id=a.weekly_plan_id,
        category=a.category,
        title=a.title,
        description=a.description,
        priority=a.priority,
        owner=a.owner,
        status=a.status,
        deliverable_id=a.deliverable_id,
        position=a.position,
        is_ai_generated=a.is_ai_generated,
        carried_from_week=a.carried_from_week,
        source_transcript_id=a.source_transcript_id,
        source_transcript_title=transcript_title,
        context=a.context,
    )


def _snapshot_schema(s: DeliverableProgressSnapshot) -> ProgressSnapshotBase:
    return ProgressSnapshotBase(
        id=s.id,
        deliverable_id=s.deliverable_id,
        weekly_plan_id=s.weekly_plan_id,
        week_number=s.week_number,
        rag_status=s.rag_status,
        progress_percent=s.progress_percent,
        milestones_completed=s.milestones_completed,
        milestones_total=s.milestones_total,
        narrative=s.narrative,
    )


def _plan_schema(p: WeeklyPlan) -> WeeklyPlanBase:
    return WeeklyPlanBase(
        id=p.id,
        week_number=p.week_number,
        week_start_date=str(p.week_start_date),
        week_end_date=str(p.week_end_date),
        deliverable_progress_summary=p.deliverable_progress_summary,
        programme_actions_summary=p.programme_actions_summary,
        status=p.status,
    )


def _plan_full(p: WeeklyPlan) -> WeeklyPlanFull:
    actions = sorted(p.actions, key=lambda a: (a.category, a.position)) if p.actions else []
    snaps = list(p.snapshots) if p.snapshots else []
    return WeeklyPlanFull(
        id=p.id,
        week_number=p.week_number,
        week_start_date=str(p.week_start_date),
        week_end_date=str(p.week_end_date),
        deliverable_progress_summary=p.deliverable_progress_summary,
        programme_actions_summary=p.programme_actions_summary,
        status=p.status,
        actions=[_action_schema(a) for a in actions],
        snapshots=[_snapshot_schema(s) for s in snaps],
    )


@router.get("/weekly-plans", response_model=list[WeeklyPlanBase])
async def list_plans(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(WeeklyPlan).order_by(WeeklyPlan.week_number.desc())
    )
    return [_plan_schema(p) for p in result.scalars().all()]


@router.get("/weekly-plans/current", response_model=WeeklyPlanFull | None)
async def get_current_plan(db: AsyncSession = Depends(get_db)):
    week_num = _current_week_number()
    result = await db.execute(
        select(WeeklyPlan)
        .options(
            selectinload(WeeklyPlan.actions).selectinload(WeeklyPlanAction.source_transcript),
            selectinload(WeeklyPlan.snapshots),
        )
        .where(WeeklyPlan.week_number == week_num)
    )
    p = result.scalar_one_or_none()
    if not p:
        # Try the latest plan instead
        result = await db.execute(
            select(WeeklyPlan)
            .options(
                selectinload(WeeklyPlan.actions).selectinload(WeeklyPlanAction.source_transcript),
                selectinload(WeeklyPlan.snapshots),
            )
            .order_by(WeeklyPlan.week_number.desc())
            .limit(1)
        )
        p = result.scalar_one_or_none()
    if not p:
        return None
    return _plan_full(p)


@router.get("/weekly-plans/{plan_id}", response_model=WeeklyPlanFull)
async def get_plan(plan_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(WeeklyPlan)
        .options(
            selectinload(WeeklyPlan.actions).selectinload(WeeklyPlanAction.source_transcript),
            selectinload(WeeklyPlan.snapshots),
        )
        .where(WeeklyPlan.id == plan_id)
    )
    p = result.scalar_one_or_none()
    if not p:
        raise NotFoundError("WeeklyPlan", plan_id)
    return _plan_full(p)


@router.post("/weekly-plans", response_model=WeeklyPlanFull, status_code=201)
async def create_plan(body: WeeklyPlanCreate, bg: BackgroundTasks, db: AsyncSession = Depends(get_db)):
    start_date = date.fromisoformat(body.week_start_date)
    end_date = date.fromisoformat(body.week_end_date)

    plan = WeeklyPlan(
        week_number=body.week_number,
        week_start_date=start_date,
        week_end_date=end_date,
        deliverable_progress_summary=body.deliverable_progress_summary,
        programme_actions_summary=body.programme_actions_summary,
        status=body.status,
    )
    db.add(plan)
    await db.flush()  # Get plan.id

    # Create actions
    for i, action_data in enumerate(body.actions):
        action = WeeklyPlanAction(
            weekly_plan_id=plan.id,
            category=action_data.category,
            title=action_data.title,
            description=action_data.description,
            priority=action_data.priority,
            owner=action_data.owner,
            status=action_data.status,
            deliverable_id=action_data.deliverable_id,
            position=action_data.position if action_data.position else i,
            is_ai_generated=action_data.is_ai_generated,
            carried_from_week=action_data.carried_from_week,
            source_transcript_id=action_data.source_transcript_id,
            context=action_data.context,
        )
        db.add(action)

    # Create progress snapshots
    for snap_data in body.snapshots:
        snap = DeliverableProgressSnapshot(
            deliverable_id=snap_data.deliverable_id,
            weekly_plan_id=plan.id,
            week_number=snap_data.week_number,
            rag_status=snap_data.rag_status,
            progress_percent=snap_data.progress_percent,
            milestones_completed=snap_data.milestones_completed,
            milestones_total=snap_data.milestones_total,
            narrative=snap_data.narrative,
        )
        db.add(snap)

    await db.commit()

    # Auto-export all plans to seed JSON for Railway deploys
    await export_plans_to_seed(db)

    # Re-fetch with relationships
    result = await db.execute(
        select(WeeklyPlan)
        .options(
            selectinload(WeeklyPlan.actions).selectinload(WeeklyPlanAction.source_transcript),
            selectinload(WeeklyPlan.snapshots),
        )
        .where(WeeklyPlan.id == plan.id)
    )
    return _plan_full(result.scalar_one())


@router.patch("/weekly-plans/{plan_id}", response_model=WeeklyPlanFull)
async def update_plan(plan_id: int, body: WeeklyPlanUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(WeeklyPlan)
        .options(
            selectinload(WeeklyPlan.actions).selectinload(WeeklyPlanAction.source_transcript),
            selectinload(WeeklyPlan.snapshots),
        )
        .where(WeeklyPlan.id == plan_id)
    )
    p = result.scalar_one_or_none()
    if not p:
        raise NotFoundError("WeeklyPlan", plan_id)

    if body.deliverable_progress_summary is not None:
        p.deliverable_progress_summary = body.deliverable_progress_summary
    if body.programme_actions_summary is not None:
        p.programme_actions_summary = body.programme_actions_summary
    if body.status is not None:
        p.status = body.status

    await db.commit()
    await db.refresh(p, ["actions", "snapshots"])

    # Auto-export all plans to seed JSON for Railway deploys
    await export_plans_to_seed(db)

    return _plan_full(p)


@router.post("/weekly-plans/{plan_id}/actions", response_model=WeeklyPlanActionBase, status_code=201)
async def add_action(plan_id: int, body: WeeklyPlanActionCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(WeeklyPlan).where(WeeklyPlan.id == plan_id))
    if not result.scalar_one_or_none():
        raise NotFoundError("WeeklyPlan", plan_id)

    action = WeeklyPlanAction(
        weekly_plan_id=plan_id,
        category=body.category,
        title=body.title,
        description=body.description,
        priority=body.priority,
        owner=body.owner,
        status=body.status,
        deliverable_id=body.deliverable_id,
        position=body.position,
        is_ai_generated=body.is_ai_generated,
        carried_from_week=body.carried_from_week,
        source_transcript_id=body.source_transcript_id,
        context=body.context,
    )
    db.add(action)
    await db.commit()
    await db.refresh(action, ["source_transcript"])
    return _action_schema(action)


@router.patch("/weekly-plans/actions/{action_id}", response_model=WeeklyPlanActionBase)
async def update_action(action_id: int, body: WeeklyPlanActionUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(WeeklyPlanAction).where(WeeklyPlanAction.id == action_id)
    )
    a = result.scalar_one_or_none()
    if not a:
        raise NotFoundError("WeeklyPlanAction", action_id)

    if body.category is not None:
        a.category = body.category
    if body.title is not None:
        a.title = body.title
    if body.description is not None:
        a.description = body.description
    if body.priority is not None:
        a.priority = body.priority
    if body.owner is not None:
        a.owner = body.owner
    if body.status is not None:
        a.status = body.status
    if body.deliverable_id is not None:
        a.deliverable_id = body.deliverable_id
    if body.position is not None:
        a.position = body.position
    if body.is_ai_generated is not None:
        a.is_ai_generated = body.is_ai_generated
    if body.source_transcript_id is not None:
        a.source_transcript_id = body.source_transcript_id
    if body.context is not None:
        a.context = body.context

    await db.commit()
    await db.refresh(a, ["source_transcript"])

    # Auto-export all plans to seed JSON for Railway deploys
    await export_plans_to_seed(db)

    return _action_schema(a)


@router.delete("/weekly-plans/actions/{action_id}")
async def delete_action(action_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(WeeklyPlanAction).where(WeeklyPlanAction.id == action_id)
    )
    a = result.scalar_one_or_none()
    if not a:
        raise NotFoundError("WeeklyPlanAction", action_id)
    await db.delete(a)
    await db.commit()
    return {"ok": True}
