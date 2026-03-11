import math

import json

from fastapi import APIRouter, Depends, File, Form, Query, UploadFile
from sqlalchemy import asc, desc, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.exceptions import NotFoundError
from app.models.project import Project
from app.models.project_link import ProjectLink
from app.models.summary import Summary
from app.models.transcript import Transcript
from app.schemas.summary import SummaryBase, SummaryDetail
from app.schemas.transcript import TranscriptBase, TranscriptDetail, TranscriptList
from app.services.upload_service import process_uploaded_transcript

router = APIRouter(tags=["transcripts"])


def _transcript_base(
    t: Transcript, has_summary: bool, project_name: str | None = None
) -> TranscriptBase:
    return TranscriptBase(
        id=t.id,
        file_name=t.filename,
        title=t.title,
        date=str(t.meeting_date) if t.meeting_date else None,
        participant_count=len(t.participants) if t.participants else 0,
        word_count=t.word_count or 0,
        has_summary=has_summary,
        primary_project_id=t.primary_project_id,
        primary_project_name=project_name,
    )


def _summary_base(s: Summary, transcript_title: str | None) -> SummaryBase:
    return SummaryBase(
        id=s.id,
        transcript_id=s.transcript_id or 0,
        transcript_title=transcript_title,
        date=None,
        tldr=None,
    )


@router.get("/transcripts", response_model=TranscriptList)
async def list_transcripts(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    sort: str = Query("meeting_date_desc"),
    db: AsyncSession = Depends(get_db),
):
    sort_map = {
        "meeting_date_desc": desc(Transcript.meeting_date),
        "meeting_date_asc": asc(Transcript.meeting_date),
        "title_asc": asc(Transcript.title),
        "title_desc": desc(Transcript.title),
    }
    order = sort_map.get(sort, desc(Transcript.meeting_date))

    total_result = await db.execute(select(func.count(Transcript.id)))
    total = total_result.scalar_one()

    offset = (page - 1) * limit
    result = await db.execute(
        select(Transcript).order_by(order).offset(offset).limit(limit)
    )
    transcripts = result.scalars().all()

    # Check which transcripts have summaries
    transcript_ids = [t.id for t in transcripts]
    summary_result = await db.execute(
        select(Summary.transcript_id).where(Summary.transcript_id.in_(transcript_ids))
    )
    summary_transcript_ids = {row[0] for row in summary_result.all()}

    # Fetch project names for transcripts with primary_project_id
    project_ids_set = {t.primary_project_id for t in transcripts if t.primary_project_id}
    project_names: dict[int, str] = {}
    if project_ids_set:
        p_result = await db.execute(
            select(Project.id, Project.name).where(Project.id.in_(project_ids_set))
        )
        project_names = dict(p_result.all())

    pages = math.ceil(total / limit) if limit else 1

    return TranscriptList(
        items=[
            _transcript_base(t, t.id in summary_transcript_ids, project_names.get(t.primary_project_id))
            for t in transcripts
        ],
        total=total,
        page=page,
        limit=limit,
        pages=pages,
    )


@router.get("/transcripts/{transcript_id}", response_model=TranscriptDetail)
async def get_transcript(
    transcript_id: int,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Transcript).where(Transcript.id == transcript_id)
    )
    transcript = result.scalar_one_or_none()
    if not transcript:
        raise NotFoundError("Transcript", transcript_id)

    # Check for summary
    summary_result = await db.execute(
        select(Summary).where(Summary.transcript_id == transcript_id)
    )
    summary = summary_result.scalar_one_or_none()

    summary_schema = _summary_base(summary, transcript.title) if summary else None

    # Get project name if set
    project_name = None
    if transcript.primary_project_id:
        p_result = await db.execute(
            select(Project.name).where(Project.id == transcript.primary_project_id)
        )
        project_name = p_result.scalar_one_or_none()

    return TranscriptDetail(
        id=transcript.id,
        file_name=transcript.filename,
        title=transcript.title,
        date=str(transcript.meeting_date) if transcript.meeting_date else None,
        participant_count=len(transcript.participants) if transcript.participants else 0,
        word_count=transcript.word_count or 0,
        has_summary=summary is not None,
        primary_project_id=transcript.primary_project_id,
        primary_project_name=project_name,
        raw_text=transcript.content,
        participants=transcript.participants or [],
        summary=summary_schema,
    )


@router.get("/transcripts/{transcript_id}/summary", response_model=SummaryDetail)
async def get_transcript_summary(
    transcript_id: int,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Summary).where(Summary.transcript_id == transcript_id)
    )
    summary = result.scalar_one_or_none()
    if not summary:
        raise NotFoundError("Summary for transcript", transcript_id)

    # Get transcript title
    t_result = await db.execute(
        select(Transcript.title).where(Transcript.id == transcript_id)
    )
    transcript_title = t_result.scalar_one_or_none()

    return SummaryDetail(
        id=summary.id,
        transcript_id=summary.transcript_id or 0,
        transcript_title=transcript_title,
        date=None,
        tldr=None,
        full_summary=summary.content,
        key_decisions=[],
        action_items=[],
        risks_and_concerns=[],
        follow_ups=[],
    )


@router.patch("/transcripts/{transcript_id}", response_model=TranscriptBase)
async def update_transcript(
    transcript_id: int,
    primary_project_id: int | None = None,
    db: AsyncSession = Depends(get_db),
):
    """Update transcript fields (currently supports primary_project_id)."""
    result = await db.execute(
        select(Transcript).where(Transcript.id == transcript_id)
    )
    transcript = result.scalar_one_or_none()
    if not transcript:
        raise NotFoundError("Transcript", transcript_id)

    if primary_project_id is not None:
        # Verify project exists
        p_result = await db.execute(
            select(Project).where(Project.id == primary_project_id)
        )
        if not p_result.scalar_one_or_none():
            raise NotFoundError("Project", primary_project_id)
        transcript.primary_project_id = primary_project_id

        # Also create ProjectLink if not exists
        existing_link = await db.execute(
            select(ProjectLink).where(
                ProjectLink.project_id == primary_project_id,
                ProjectLink.entity_type == "transcript",
                ProjectLink.entity_id == transcript_id,
            )
        )
        if not existing_link.scalar_one_or_none():
            db.add(ProjectLink(
                project_id=primary_project_id,
                entity_type="transcript",
                entity_id=transcript_id,
            ))

    await db.commit()
    await db.refresh(transcript)

    # Get summary status
    summary_result = await db.execute(
        select(Summary).where(Summary.transcript_id == transcript_id)
    )
    has_summary = summary_result.scalar_one_or_none() is not None

    # Get project name
    project_name = None
    if transcript.primary_project_id:
        pn_result = await db.execute(
            select(Project.name).where(Project.id == transcript.primary_project_id)
        )
        project_name = pn_result.scalar_one_or_none()

    return _transcript_base(transcript, has_summary, project_name)


MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB


@router.post("/transcripts/upload")
async def upload_transcripts(
    files: list[UploadFile] = File(...),
    project_ids: str | None = Form(None),
    db: AsyncSession = Depends(get_db),
):
    """Upload one or more .txt transcript files.

    Parses each file using the existing transcript parser, upserts into the
    database (skip if unchanged, update if modified, insert if new), and
    rebuilds stakeholder mentions for each uploaded transcript.

    Optionally accepts a JSON-encoded ``project_ids`` array (one entry per
    file, in the same order) to set each transcript's primary project.
    """
    # Parse project_ids if provided
    parsed_project_ids: list[int | None] = []
    if project_ids:
        try:
            parsed_project_ids = json.loads(project_ids)
        except (json.JSONDecodeError, TypeError):
            parsed_project_ids = []

    results = []

    for idx, upload_file in enumerate(files):
        # Validate file extension
        if not upload_file.filename or not upload_file.filename.endswith(".txt"):
            results.append({
                "status": "error",
                "id": None,
                "filename": upload_file.filename or "unknown",
                "title": None,
                "error": "Only .txt files are accepted",
            })
            continue

        # Read and validate file size
        content_bytes = await upload_file.read()
        if len(content_bytes) > MAX_FILE_SIZE:
            results.append({
                "status": "error",
                "id": None,
                "filename": upload_file.filename,
                "title": None,
                "error": f"File too large ({len(content_bytes)} bytes). Max is {MAX_FILE_SIZE} bytes.",
            })
            continue

        # Determine project for this file
        file_project_id = None
        if idx < len(parsed_project_ids) and parsed_project_ids[idx]:
            file_project_id = parsed_project_ids[idx]

        # Process the transcript
        try:
            result = await process_uploaded_transcript(
                filename=upload_file.filename,
                content_bytes=content_bytes,
                db=db,
                primary_project_id=file_project_id,
            )
            # Create ProjectLink if project was assigned and transcript was created/updated
            if file_project_id and result.get("id") and result["status"] in ("inserted", "updated", "skipped"):
                existing_link = await db.execute(
                    select(ProjectLink).where(
                        ProjectLink.project_id == file_project_id,
                        ProjectLink.entity_type == "transcript",
                        ProjectLink.entity_id == result["id"],
                    )
                )
                if not existing_link.scalar_one_or_none():
                    db.add(ProjectLink(
                        project_id=file_project_id,
                        entity_type="transcript",
                        entity_id=result["id"],
                    ))
                    await db.commit()

            results.append(result)
        except Exception as e:
            results.append({
                "status": "error",
                "id": None,
                "filename": upload_file.filename,
                "title": None,
                "error": str(e),
            })

    uploaded_count = sum(1 for r in results if r["status"] in ("inserted", "updated"))

    return {
        "uploaded": uploaded_count,
        "total": len(results),
        "results": results,
    }
