import math

from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File
from sqlalchemy import select, func, desc, asc
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.transcript import Transcript
from app.models.summary import Summary
from app.schemas.transcript import TranscriptBase, TranscriptDetail, TranscriptList
from app.schemas.summary import SummaryBase, SummaryDetail
from app.services.upload_service import process_uploaded_transcript

router = APIRouter(tags=["transcripts"])


def _transcript_base(t: Transcript, has_summary: bool) -> TranscriptBase:
    return TranscriptBase(
        id=t.id,
        file_name=t.filename,
        title=t.title,
        date=str(t.meeting_date) if t.meeting_date else None,
        participant_count=len(t.participants) if t.participants else 0,
        word_count=t.word_count or 0,
        has_summary=has_summary,
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

    pages = math.ceil(total / limit) if limit else 1

    return TranscriptList(
        items=[_transcript_base(t, t.id in summary_transcript_ids) for t in transcripts],
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
        raise HTTPException(status_code=404, detail="Transcript not found")

    # Check for summary
    summary_result = await db.execute(
        select(Summary).where(Summary.transcript_id == transcript_id)
    )
    summary = summary_result.scalar_one_or_none()

    summary_schema = _summary_base(summary, transcript.title) if summary else None

    return TranscriptDetail(
        id=transcript.id,
        file_name=transcript.filename,
        title=transcript.title,
        date=str(transcript.meeting_date) if transcript.meeting_date else None,
        participant_count=len(transcript.participants) if transcript.participants else 0,
        word_count=transcript.word_count or 0,
        has_summary=summary is not None,
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
        raise HTTPException(status_code=404, detail="Summary not found for this transcript")

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


MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB


@router.post("/transcripts/upload")
async def upload_transcripts(
    files: list[UploadFile] = File(...),
    db: AsyncSession = Depends(get_db),
):
    """Upload one or more .txt transcript files.

    Parses each file using the existing transcript parser, upserts into the
    database (skip if unchanged, update if modified, insert if new), and
    rebuilds stakeholder mentions for each uploaded transcript.
    """
    results = []

    for upload_file in files:
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

        # Process the transcript
        try:
            result = await process_uploaded_transcript(
                filename=upload_file.filename,
                content_bytes=content_bytes,
                db=db,
            )
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
