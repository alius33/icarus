from datetime import date

from fastapi import APIRouter, Depends
from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.exceptions import NotFoundError
from app.models.cross_project_link import CrossProjectLink
from app.schemas.cross_project_link import (
    CrossProjectLinkBase,
    CrossProjectLinkCreate,
    CrossProjectLinkUpdate,
)

router = APIRouter(tags=["cross_project_links"])


def _schema(link: CrossProjectLink) -> CrossProjectLinkBase:
    return CrossProjectLinkBase(
        id=link.id,
        source_project_id=link.source_project_id,
        target_project_id=link.target_project_id,
        link_type=link.link_type,
        description=link.description,
        transcript_id=link.transcript_id,
        date_detected=str(link.date_detected) if link.date_detected else None,
        severity=link.severity,
        status=link.status,
        is_manual=link.is_manual,
    )


@router.get("/cross-project-links", response_model=list[CrossProjectLinkBase])
async def list_cross_project_links(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(CrossProjectLink).order_by(CrossProjectLink.created_at.desc())
    )
    return [_schema(link) for link in result.scalars().all()]


@router.get(
    "/cross-project-links/project/{project_id}",
    response_model=list[CrossProjectLinkBase],
)
async def get_project_links(project_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(CrossProjectLink).where(
            or_(
                CrossProjectLink.source_project_id == project_id,
                CrossProjectLink.target_project_id == project_id,
            )
        ).order_by(CrossProjectLink.created_at.desc())
    )
    return [_schema(link) for link in result.scalars().all()]


@router.post("/cross-project-links", response_model=CrossProjectLinkBase, status_code=201)
async def create_cross_project_link(
    body: CrossProjectLinkCreate, db: AsyncSession = Depends(get_db)
):
    link = CrossProjectLink(
        source_project_id=body.source_project_id,
        target_project_id=body.target_project_id,
        link_type=body.link_type,
        description=body.description,
        transcript_id=body.transcript_id,
        date_detected=date.fromisoformat(body.date_detected) if body.date_detected else None,
        severity=body.severity,
        status=body.status,
        is_manual=True,
    )
    db.add(link)
    await db.commit()
    await db.refresh(link)
    return _schema(link)


@router.patch("/cross-project-links/{link_id}", response_model=CrossProjectLinkBase)
async def update_cross_project_link(
    link_id: int,
    body: CrossProjectLinkUpdate,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(CrossProjectLink).where(CrossProjectLink.id == link_id)
    )
    link = result.scalar_one_or_none()
    if not link:
        raise NotFoundError("Cross-project link", link_id)

    if body.source_project_id is not None:
        link.source_project_id = body.source_project_id
    if body.target_project_id is not None:
        link.target_project_id = body.target_project_id
    if body.link_type is not None:
        link.link_type = body.link_type
    if body.description is not None:
        link.description = body.description
    if body.transcript_id is not None:
        link.transcript_id = body.transcript_id
    if body.date_detected is not None:
        link.date_detected = date.fromisoformat(body.date_detected)
    if body.severity is not None:
        link.severity = body.severity
    if body.status is not None:
        link.status = body.status

    await db.commit()
    await db.refresh(link)
    return _schema(link)


@router.delete("/cross-project-links/{link_id}")
async def delete_cross_project_link(link_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(CrossProjectLink).where(CrossProjectLink.id == link_id)
    )
    link = result.scalar_one_or_none()
    if not link:
        raise NotFoundError("Cross-project link", link_id)
    await db.delete(link)
    await db.commit()
    return {"ok": True}
