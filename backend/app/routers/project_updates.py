from fastapi import APIRouter, Depends, Query
from sqlalchemy import select, func, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db, utcnow
from app.exceptions import NotFoundError
from app.models.project import Project
from app.models.project_link import ProjectLink
from app.models.project_update import ProjectUpdate
from app.schemas.project_update import (
    ProjectUpdateBase,
    ProjectUpdateCreate,
    ProjectUpdateDetail,
    ProjectUpdateUpdate,
)
from app.services.teams_parser import detect_teams_chat, parse_teams_chat

router = APIRouter(tags=["project-updates"])


# ── Helpers ──────────────────────────────────────────────────────────────

async def _get_project_ids(update_id: int, db: AsyncSession) -> list[int]:
    result = await db.execute(
        select(ProjectLink.project_id)
        .where(ProjectLink.entity_type == "project_update", ProjectLink.entity_id == update_id)
    )
    return [row[0] for row in result.all()]


async def _get_project_names_map(project_ids: list[int], db: AsyncSession) -> dict[int, str]:
    if not project_ids:
        return {}
    result = await db.execute(
        select(Project.id, Project.name).where(Project.id.in_(project_ids))
    )
    return dict(result.all())


async def _build_base(u: ProjectUpdate, db: AsyncSession) -> ProjectUpdateBase:
    pids = await _get_project_ids(u.id, db)
    names_map = await _get_project_names_map(pids, db)
    return ProjectUpdateBase(
        id=u.id,
        title=u.title,
        content=u.content,
        content_type=u.content_type,
        summary=u.summary,
        is_processed=u.is_processed,
        created_at=u.created_at.isoformat() if u.created_at else "",
        updated_at=u.updated_at.isoformat() if u.updated_at else "",
        project_ids=pids,
        project_names=[names_map.get(pid, "") for pid in pids],
    )


async def _build_detail(u: ProjectUpdate, db: AsyncSession) -> ProjectUpdateDetail:
    pids = await _get_project_ids(u.id, db)
    names_map = await _get_project_names_map(pids, db)
    return ProjectUpdateDetail(
        id=u.id,
        title=u.title,
        content=u.content,
        raw_content=u.raw_content,
        content_type=u.content_type,
        summary=u.summary,
        is_processed=u.is_processed,
        created_at=u.created_at.isoformat() if u.created_at else "",
        updated_at=u.updated_at.isoformat() if u.updated_at else "",
        project_ids=pids,
        project_names=[names_map.get(pid, "") for pid in pids],
    )


async def _sync_project_links(update_id: int, project_ids: list[int], db: AsyncSession):
    """Reconcile ProjectLink entries for a project update."""
    # Delete existing links
    await db.execute(
        delete(ProjectLink).where(
            ProjectLink.entity_type == "project_update",
            ProjectLink.entity_id == update_id,
        )
    )
    # Create new links
    for pid in project_ids:
        db.add(ProjectLink(project_id=pid, entity_type="project_update", entity_id=update_id))


# ── Endpoints ────────────────────────────────────────────────────────────

@router.get("/project-updates", response_model=list[ProjectUpdateBase])
async def list_project_updates(
    project_id: int | None = Query(None),
    content_type: str | None = Query(None),
    is_processed: bool | None = Query(None),
    db: AsyncSession = Depends(get_db),
):
    query = select(ProjectUpdate).order_by(ProjectUpdate.created_at.desc())

    if is_processed is not None:
        query = query.where(ProjectUpdate.is_processed == is_processed)
    if content_type:
        query = query.where(ProjectUpdate.content_type == content_type)

    # Filter by project via ProjectLink
    if project_id is not None:
        linked_ids = select(ProjectLink.entity_id).where(
            ProjectLink.project_id == project_id,
            ProjectLink.entity_type == "project_update",
        )
        query = query.where(ProjectUpdate.id.in_(linked_ids))

    result = await db.execute(query)
    updates = result.scalars().all()
    return [await _build_base(u, db) for u in updates]


@router.get("/project-updates/unprocessed", response_model=list[ProjectUpdateBase])
async def list_unprocessed(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(ProjectUpdate)
        .where(ProjectUpdate.is_processed == False)
        .order_by(ProjectUpdate.created_at.asc())
    )
    updates = result.scalars().all()
    return [await _build_base(u, db) for u in updates]


@router.get("/project-updates/{update_id}", response_model=ProjectUpdateDetail)
async def get_project_update(update_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(ProjectUpdate).where(ProjectUpdate.id == update_id))
    u = result.scalar_one_or_none()
    if not u:
        raise NotFoundError("Project update", update_id)
    return await _build_detail(u, db)


@router.post("/project-updates", response_model=ProjectUpdateBase, status_code=201)
async def create_project_update(body: ProjectUpdateCreate, db: AsyncSession = Depends(get_db)):
    content = body.content
    raw_content = None
    content_type = body.content_type

    # Auto-detect and parse Teams chat
    if content_type == "teams_chat" or detect_teams_chat(body.content):
        content_type = "teams_chat"
        raw_content = body.content
        content = parse_teams_chat(body.content)

    u = ProjectUpdate(
        title=body.title,
        content=content,
        raw_content=raw_content,
        content_type=content_type,
    )
    db.add(u)
    await db.flush()  # get the id

    # Create project links
    await _sync_project_links(u.id, body.project_ids, db)

    await db.commit()
    await db.refresh(u)
    return await _build_base(u, db)


@router.patch("/project-updates/{update_id}", response_model=ProjectUpdateBase)
async def update_project_update(
    update_id: int, body: ProjectUpdateUpdate, db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(ProjectUpdate).where(ProjectUpdate.id == update_id))
    u = result.scalar_one_or_none()
    if not u:
        raise NotFoundError("Project update", update_id)

    if body.title is not None:
        u.title = body.title
    if body.content is not None:
        ct = body.content_type or u.content_type
        if ct == "teams_chat" or detect_teams_chat(body.content):
            u.content_type = "teams_chat"
            u.raw_content = body.content
            u.content = parse_teams_chat(body.content)
        else:
            u.content = body.content
            u.raw_content = None
            if body.content_type:
                u.content_type = body.content_type
    elif body.content_type is not None:
        u.content_type = body.content_type

    if body.summary is not None:
        u.summary = body.summary
    if body.project_ids is not None:
        await _sync_project_links(u.id, body.project_ids, db)

    u.updated_at = utcnow()
    await db.commit()
    await db.refresh(u)
    return await _build_base(u, db)


@router.patch("/project-updates/{update_id}/processed", response_model=ProjectUpdateBase)
async def mark_processed(update_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(ProjectUpdate).where(ProjectUpdate.id == update_id))
    u = result.scalar_one_or_none()
    if not u:
        raise NotFoundError("Project update", update_id)

    u.is_processed = True
    u.processed_at = utcnow()
    u.updated_at = utcnow()
    await db.commit()
    await db.refresh(u)
    return await _build_base(u, db)


@router.delete("/project-updates/{update_id}")
async def delete_project_update(update_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(ProjectUpdate).where(ProjectUpdate.id == update_id))
    u = result.scalar_one_or_none()
    if not u:
        raise NotFoundError("Project update", update_id)

    # Delete project links first
    await db.execute(
        delete(ProjectLink).where(
            ProjectLink.entity_type == "project_update",
            ProjectLink.entity_id == update_id,
        )
    )
    await db.delete(u)
    await db.commit()
    return {"ok": True}
