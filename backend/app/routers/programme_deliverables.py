from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.database import get_db
from app.exceptions import NotFoundError
from app.models.programme_deliverable import ProgrammeDeliverable
from app.models.deliverable_milestone import DeliverableMilestone
from app.models.deliverable_progress_snapshot import DeliverableProgressSnapshot
from app.schemas.programme_deliverable import (
    DeliverableMilestoneBase,
    DeliverableMilestoneCreate,
    DeliverableMilestoneUpdate,
    DeliverableOverview,
    DeliverableWithHistory,
    DeliverableWithMilestones,
    PillarSummary,
    ProgrammeDeliverableUpdate,
    ProgressSnapshotBase,
)

router = APIRouter(tags=["programme-deliverables"])


def _calc_progress(milestones: list) -> int:
    """Auto-calculate progress from milestone completion."""
    if not milestones:
        return 0
    completed = sum(1 for m in milestones if m.status == "COMPLETED")
    return round(completed / len(milestones) * 100)


def _milestone_schema(m: DeliverableMilestone) -> DeliverableMilestoneBase:
    return DeliverableMilestoneBase(
        id=m.id,
        deliverable_id=m.deliverable_id,
        title=m.title,
        description=m.description,
        status=m.status,
        target_week=m.target_week,
        completed_week=m.completed_week,
        evidence=m.evidence,
        position=m.position,
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


def _deliverable_schema(d: ProgrammeDeliverable, snapshots: list | None = None) -> DeliverableWithMilestones:
    ms = list(d.milestones) if d.milestones else []
    progress = _calc_progress(ms)
    latest = None
    if snapshots:
        latest = _snapshot_schema(snapshots[-1])
    return DeliverableWithMilestones(
        id=d.id,
        pillar=d.pillar,
        pillar_name=d.pillar_name,
        title=d.title,
        description=d.description,
        position=d.position,
        project_id=d.project_id,
        rag_status=d.rag_status,
        progress_percent=progress,
        notes=d.notes,
        milestones=[_milestone_schema(m) for m in ms],
        latest_snapshot=latest,
    )


def _aggregate_rag(deliverables: list[DeliverableWithMilestones]) -> str:
    statuses = [d.rag_status for d in deliverables]
    if "RED" in statuses:
        return "RED"
    if "AMBER" in statuses:
        return "AMBER"
    return "GREEN"


@router.get("/programme-deliverables", response_model=list[DeliverableWithMilestones])
async def list_deliverables(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(ProgrammeDeliverable)
        .options(selectinload(ProgrammeDeliverable.milestones))
        .order_by(ProgrammeDeliverable.pillar, ProgrammeDeliverable.position)
    )
    deliverables = result.scalars().all()

    # Get latest snapshot per deliverable
    snap_result = await db.execute(
        select(DeliverableProgressSnapshot).order_by(DeliverableProgressSnapshot.week_number)
    )
    all_snaps = snap_result.scalars().all()
    snaps_by_del = {}
    for s in all_snaps:
        snaps_by_del.setdefault(s.deliverable_id, []).append(s)

    return [_deliverable_schema(d, snaps_by_del.get(d.id)) for d in deliverables]


@router.get("/programme-deliverables/overview", response_model=DeliverableOverview)
async def get_overview(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(ProgrammeDeliverable)
        .options(selectinload(ProgrammeDeliverable.milestones))
        .order_by(ProgrammeDeliverable.pillar, ProgrammeDeliverable.position)
    )
    deliverables = result.scalars().all()

    pillars_map: dict[int, list] = {}
    pillar_names: dict[int, str] = {}
    for d in deliverables:
        pillars_map.setdefault(d.pillar, []).append(d)
        pillar_names[d.pillar] = d.pillar_name

    pillar_summaries = []
    for pillar_num in sorted(pillars_map.keys()):
        dels = [_deliverable_schema(d) for d in pillars_map[pillar_num]]
        avg_progress = round(sum(d.progress_percent for d in dels) / len(dels)) if dels else 0
        pillar_summaries.append(PillarSummary(
            pillar=pillar_num,
            pillar_name=pillar_names[pillar_num],
            deliverables=dels,
            aggregate_progress=avg_progress,
            aggregate_rag=_aggregate_rag(dels),
        ))

    return DeliverableOverview(pillars=pillar_summaries)


@router.get("/programme-deliverables/{deliverable_id}", response_model=DeliverableWithHistory)
async def get_deliverable(deliverable_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(ProgrammeDeliverable)
        .options(selectinload(ProgrammeDeliverable.milestones))
        .where(ProgrammeDeliverable.id == deliverable_id)
    )
    d = result.scalar_one_or_none()
    if not d:
        raise NotFoundError("ProgrammeDeliverable", deliverable_id)

    snap_result = await db.execute(
        select(DeliverableProgressSnapshot)
        .where(DeliverableProgressSnapshot.deliverable_id == deliverable_id)
        .order_by(DeliverableProgressSnapshot.week_number)
    )
    snaps = snap_result.scalars().all()

    ms = list(d.milestones) if d.milestones else []
    return DeliverableWithHistory(
        id=d.id,
        pillar=d.pillar,
        pillar_name=d.pillar_name,
        title=d.title,
        description=d.description,
        position=d.position,
        project_id=d.project_id,
        rag_status=d.rag_status,
        progress_percent=_calc_progress(ms),
        notes=d.notes,
        milestones=[_milestone_schema(m) for m in ms],
        snapshots=[_snapshot_schema(s) for s in snaps],
    )


@router.patch("/programme-deliverables/{deliverable_id}", response_model=DeliverableWithMilestones)
async def update_deliverable(
    deliverable_id: int,
    body: ProgrammeDeliverableUpdate,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(ProgrammeDeliverable)
        .options(selectinload(ProgrammeDeliverable.milestones))
        .where(ProgrammeDeliverable.id == deliverable_id)
    )
    d = result.scalar_one_or_none()
    if not d:
        raise NotFoundError("ProgrammeDeliverable", deliverable_id)

    if body.rag_status is not None:
        d.rag_status = body.rag_status
    if body.progress_percent is not None:
        d.progress_percent = body.progress_percent
    if body.notes is not None:
        d.notes = body.notes

    await db.commit()
    await db.refresh(d, ["milestones"])
    return _deliverable_schema(d)


@router.post("/programme-deliverables/{deliverable_id}/milestones", response_model=DeliverableMilestoneBase, status_code=201)
async def add_milestone(
    deliverable_id: int,
    body: DeliverableMilestoneCreate,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(ProgrammeDeliverable).where(ProgrammeDeliverable.id == deliverable_id)
    )
    if not result.scalar_one_or_none():
        raise NotFoundError("ProgrammeDeliverable", deliverable_id)

    m = DeliverableMilestone(
        deliverable_id=deliverable_id,
        title=body.title,
        description=body.description,
        status=body.status,
        target_week=body.target_week,
        completed_week=body.completed_week,
        evidence=body.evidence,
        position=body.position,
    )
    db.add(m)
    await db.commit()
    await db.refresh(m)
    return _milestone_schema(m)


@router.patch("/programme-deliverables/milestones/{milestone_id}", response_model=DeliverableMilestoneBase)
async def update_milestone(
    milestone_id: int,
    body: DeliverableMilestoneUpdate,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(DeliverableMilestone).where(DeliverableMilestone.id == milestone_id)
    )
    m = result.scalar_one_or_none()
    if not m:
        raise NotFoundError("DeliverableMilestone", milestone_id)

    if body.title is not None:
        m.title = body.title
    if body.description is not None:
        m.description = body.description
    if body.status is not None:
        m.status = body.status
    if body.target_week is not None:
        m.target_week = body.target_week
    if body.completed_week is not None:
        m.completed_week = body.completed_week
    if body.evidence is not None:
        m.evidence = body.evidence
    if body.position is not None:
        m.position = body.position

    await db.commit()
    await db.refresh(m)
    return _milestone_schema(m)


@router.delete("/programme-deliverables/milestones/{milestone_id}")
async def delete_milestone(milestone_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(DeliverableMilestone).where(DeliverableMilestone.id == milestone_id)
    )
    m = result.scalar_one_or_none()
    if not m:
        raise NotFoundError("DeliverableMilestone", milestone_id)
    await db.delete(m)
    await db.commit()
    return {"ok": True}
