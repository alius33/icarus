from datetime import date

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.exceptions import NotFoundError
from app.models.project_summary import ProjectSummary
from app.schemas.project_summary import (
    ProjectSummaryBase,
    ProjectSummaryCreate,
)

router = APIRouter(tags=["project-summaries"])


def _schema(s: ProjectSummary) -> ProjectSummaryBase:
    return ProjectSummaryBase(
        id=s.id,
        project_id=s.project_id,
        transcript_id=s.transcript_id,
        project_update_id=s.project_update_id,
        date=str(s.date) if s.date else None,
        relevance=s.relevance,
        content=s.content,
        source_file=s.source_file,
    )


@router.get(
    "/projects/{project_id}/project-summaries",
    response_model=list[ProjectSummaryBase],
)
async def list_project_summaries(
    project_id: int,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(ProjectSummary)
        .where(ProjectSummary.project_id == project_id)
        .order_by(ProjectSummary.date.desc().nullslast(), ProjectSummary.id.desc())
    )
    return [_schema(s) for s in result.scalars().all()]


@router.get("/project-summaries/{summary_id}", response_model=ProjectSummaryBase)
async def get_project_summary(summary_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(ProjectSummary).where(ProjectSummary.id == summary_id)
    )
    record = result.scalar_one_or_none()
    if not record:
        raise NotFoundError("Project summary", summary_id)
    return _schema(record)


@router.post("/project-summaries", response_model=ProjectSummaryBase, status_code=201)
async def create_project_summary(body: ProjectSummaryCreate, db: AsyncSession = Depends(get_db)):
    if body.transcript_id is None and body.project_update_id is None:
        raise HTTPException(400, "Either transcript_id or project_update_id must be provided")
    record = ProjectSummary(
        project_id=body.project_id,
        transcript_id=body.transcript_id,
        project_update_id=body.project_update_id,
        date=date.fromisoformat(body.date) if body.date else None,
        relevance=body.relevance,
        content=body.content,
        source_file=body.source_file,
    )
    db.add(record)
    await db.commit()
    await db.refresh(record)
    return _schema(record)


@router.delete("/project-summaries/{summary_id}")
async def delete_project_summary(summary_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(ProjectSummary).where(ProjectSummary.id == summary_id)
    )
    record = result.scalar_one_or_none()
    if not record:
        raise NotFoundError("Project summary", summary_id)
    await db.delete(record)
    await db.commit()
    return {"ok": True}
