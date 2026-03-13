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
from app.models.transcript_attachment import TranscriptAttachment
from app.models.transcript_note import TranscriptNote
from app.schemas.summary import SummaryBase, SummaryDetail
from app.schemas.transcript import TranscriptBase, TranscriptDetail, TranscriptList
from app.services.upload_service import process_uploaded_transcript

router = APIRouter(tags=["transcripts"])


async def _resolve_project_names(
    db: AsyncSession, transcripts: list
) -> dict[int, str]:
    """Fetch project names for all project IDs referenced by transcripts."""
    project_ids_set: set[int] = set()
    for t in transcripts:
        for pid in (t.primary_project_id, t.secondary_project_id, t.tertiary_project_id):
            if pid:
                project_ids_set.add(pid)
    if not project_ids_set:
        return {}
    p_result = await db.execute(
        select(Project.id, Project.name).where(Project.id.in_(project_ids_set))
    )
    return dict(p_result.all())


def _transcript_base(
    t: Transcript,
    has_summary: bool,
    project_names: dict[int, str] | None = None,
    has_notes: bool = False,
    attachments_count: int = 0,
) -> TranscriptBase:
    pn = project_names or {}
    return TranscriptBase(
        id=t.id,
        file_name=t.filename,
        title=t.title,
        date=str(t.meeting_date) if t.meeting_date else None,
        participant_count=len(t.participants) if t.participants else 0,
        word_count=t.word_count or 0,
        has_summary=has_summary,
        has_notes=has_notes,
        attachments_count=attachments_count,
        primary_project_id=t.primary_project_id,
        primary_project_name=pn.get(t.primary_project_id) if t.primary_project_id else None,
        secondary_project_id=t.secondary_project_id,
        secondary_project_name=pn.get(t.secondary_project_id) if t.secondary_project_id else None,
        tertiary_project_id=t.tertiary_project_id,
        tertiary_project_name=pn.get(t.tertiary_project_id) if t.tertiary_project_id else None,
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

    # Fetch all project names referenced
    project_names = await _resolve_project_names(db, transcripts)

    # Check which transcripts have notes
    notes_result = await db.execute(
        select(TranscriptNote.transcript_id)
        .where(TranscriptNote.transcript_id.in_(transcript_ids))
        .distinct()
    )
    notes_transcript_ids = {row[0] for row in notes_result.all()}

    # Count attachments per transcript
    att_result = await db.execute(
        select(
            TranscriptAttachment.transcript_id,
            func.count(TranscriptAttachment.id),
        )
        .where(TranscriptAttachment.transcript_id.in_(transcript_ids))
        .group_by(TranscriptAttachment.transcript_id)
    )
    att_counts = dict(att_result.all())

    pages = math.ceil(total / limit) if limit else 1

    return TranscriptList(
        items=[
            _transcript_base(
                t,
                t.id in summary_transcript_ids,
                project_names,
                has_notes=t.id in notes_transcript_ids,
                attachments_count=att_counts.get(t.id, 0),
            )
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

    # Get project names
    project_names = await _resolve_project_names(db, [transcript])

    # Check for notes
    notes_result = await db.execute(
        select(func.count(TranscriptNote.id)).where(
            TranscriptNote.transcript_id == transcript_id
        )
    )
    has_notes = (notes_result.scalar_one() or 0) > 0

    # Count attachments
    att_result = await db.execute(
        select(func.count(TranscriptAttachment.id)).where(
            TranscriptAttachment.transcript_id == transcript_id
        )
    )
    attachments_count = att_result.scalar_one() or 0

    return TranscriptDetail(
        id=transcript.id,
        file_name=transcript.filename,
        title=transcript.title,
        date=str(transcript.meeting_date) if transcript.meeting_date else None,
        participant_count=len(transcript.participants) if transcript.participants else 0,
        word_count=transcript.word_count or 0,
        has_summary=summary is not None,
        has_notes=has_notes,
        attachments_count=attachments_count,
        primary_project_id=transcript.primary_project_id,
        primary_project_name=project_names.get(transcript.primary_project_id) if transcript.primary_project_id else None,
        secondary_project_id=transcript.secondary_project_id,
        secondary_project_name=project_names.get(transcript.secondary_project_id) if transcript.secondary_project_id else None,
        tertiary_project_id=transcript.tertiary_project_id,
        tertiary_project_name=project_names.get(transcript.tertiary_project_id) if transcript.tertiary_project_id else None,
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


async def _ensure_project_link(
    db: AsyncSession, project_id: int, entity_type: str, entity_id: int
) -> bool:
    """Create a ProjectLink if it doesn't already exist. Returns True if created."""
    existing = await db.execute(
        select(ProjectLink).where(
            ProjectLink.project_id == project_id,
            ProjectLink.entity_type == entity_type,
            ProjectLink.entity_id == entity_id,
        )
    )
    if existing.scalar_one_or_none():
        return False
    db.add(ProjectLink(
        project_id=project_id,
        entity_type=entity_type,
        entity_id=entity_id,
    ))
    return True


@router.patch("/transcripts/{transcript_id}", response_model=TranscriptBase)
async def update_transcript(
    transcript_id: int,
    primary_project_id: int | None = Query(None),
    secondary_project_id: int | None = Query(None),
    tertiary_project_id: int | None = Query(None),
    db: AsyncSession = Depends(get_db),
):
    """Update transcript project assignments."""
    result = await db.execute(
        select(Transcript).where(Transcript.id == transcript_id)
    )
    transcript = result.scalar_one_or_none()
    if not transcript:
        raise NotFoundError("Transcript", transcript_id)

    # Update each project field if provided, and create ProjectLinks
    for field, pid in [
        ("primary_project_id", primary_project_id),
        ("secondary_project_id", secondary_project_id),
        ("tertiary_project_id", tertiary_project_id),
    ]:
        if pid is not None:
            # Verify project exists
            p_result = await db.execute(
                select(Project).where(Project.id == pid)
            )
            if not p_result.scalar_one_or_none():
                raise NotFoundError("Project", pid)
            setattr(transcript, field, pid)
            await _ensure_project_link(db, pid, "transcript", transcript_id)

    await db.commit()
    await db.refresh(transcript)

    # Get summary status
    summary_result = await db.execute(
        select(Summary).where(Summary.transcript_id == transcript_id)
    )
    has_summary = summary_result.scalar_one_or_none() is not None

    project_names = await _resolve_project_names(db, [transcript])
    return _transcript_base(transcript, has_summary, project_names)


MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB


@router.post("/transcripts/upload")
async def upload_transcripts(
    files: list[UploadFile] = File(...),
    project_ids: str | None = Form(None),
    secondary_project_ids: str | None = Form(None),
    tertiary_project_ids: str | None = Form(None),
    db: AsyncSession = Depends(get_db),
):
    """Upload one or more .txt transcript files.

    Parses each file using the existing transcript parser, upserts into the
    database (skip if unchanged, update if modified, insert if new), and
    rebuilds stakeholder mentions for each uploaded transcript.

    Optionally accepts JSON-encoded arrays (one entry per file, in the same
    order) for ``project_ids`` (primary), ``secondary_project_ids``, and
    ``tertiary_project_ids``.
    """

    def _parse_ids(raw: str | None) -> list[int | None]:
        if not raw:
            return []
        try:
            return json.loads(raw)
        except (json.JSONDecodeError, TypeError):
            return []

    parsed_primary = _parse_ids(project_ids)
    parsed_secondary = _parse_ids(secondary_project_ids)
    parsed_tertiary = _parse_ids(tertiary_project_ids)

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

        # Determine projects for this file
        file_primary = parsed_primary[idx] if idx < len(parsed_primary) and parsed_primary[idx] else None
        file_secondary = parsed_secondary[idx] if idx < len(parsed_secondary) and parsed_secondary[idx] else None
        file_tertiary = parsed_tertiary[idx] if idx < len(parsed_tertiary) and parsed_tertiary[idx] else None

        # Process the transcript
        try:
            result = await process_uploaded_transcript(
                filename=upload_file.filename,
                content_bytes=content_bytes,
                db=db,
                primary_project_id=file_primary,
                secondary_project_id=file_secondary,
                tertiary_project_id=file_tertiary,
            )
            # Create ProjectLinks for all assigned projects
            if result.get("id") and result["status"] in ("inserted", "updated", "skipped"):
                for pid in (file_primary, file_secondary, file_tertiary):
                    if pid:
                        await _ensure_project_link(db, pid, "transcript", result["id"])
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
