"""API endpoints for transcript notes and attachments."""

import io

from fastapi import APIRouter, Depends, File, UploadFile
from fastapi.responses import StreamingResponse
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.exceptions import NotFoundError
from app.models.transcript import Transcript
from app.models.transcript_attachment import TranscriptAttachment
from app.models.transcript_note import TranscriptNote
from app.schemas.transcript_attachment import (
    TranscriptAttachmentBase,
    TranscriptAttachmentDetail,
    TranscriptContextResponse,
)
from app.schemas.transcript_note import (
    TranscriptNoteBase,
    TranscriptNoteCurrent,
    TranscriptNoteHistory,
    TranscriptNoteUpdate,
)
from app.services.attachment_service import (
    delete_attachment,
    save_attachment,
    write_context_notes_file,
)

router = APIRouter(tags=["transcript-extras"])


# ── Helpers ──────────────────────────────────────────────────────────

async def _get_transcript_or_404(transcript_id: int, db: AsyncSession) -> Transcript:
    result = await db.execute(
        select(Transcript).where(Transcript.id == transcript_id)
    )
    transcript = result.scalar_one_or_none()
    if not transcript:
        raise NotFoundError("Transcript", transcript_id)
    return transcript


# ── Notes endpoints ──────────────────────────────────────────────────

@router.get("/transcripts/{transcript_id}/notes", response_model=TranscriptNoteCurrent | None)
async def get_transcript_notes(
    transcript_id: int,
    db: AsyncSession = Depends(get_db),
):
    """Get the latest note for a transcript, with version count."""
    await _get_transcript_or_404(transcript_id, db)

    # Get latest version
    result = await db.execute(
        select(TranscriptNote)
        .where(TranscriptNote.transcript_id == transcript_id)
        .order_by(TranscriptNote.version.desc())
        .limit(1)
    )
    latest = result.scalar_one_or_none()
    if not latest:
        return None

    # Get version count
    count_result = await db.execute(
        select(func.count(TranscriptNote.id)).where(
            TranscriptNote.transcript_id == transcript_id
        )
    )
    version_count = count_result.scalar_one()

    return TranscriptNoteCurrent(
        content=latest.content,
        version=latest.version,
        created_at=latest.created_at.isoformat() if latest.created_at else "",
        version_count=version_count,
    )


@router.get("/transcripts/{transcript_id}/notes/history", response_model=TranscriptNoteHistory)
async def get_transcript_note_history(
    transcript_id: int,
    db: AsyncSession = Depends(get_db),
):
    """Get all note versions for a transcript (newest first)."""
    await _get_transcript_or_404(transcript_id, db)

    result = await db.execute(
        select(TranscriptNote)
        .where(TranscriptNote.transcript_id == transcript_id)
        .order_by(TranscriptNote.version.desc())
    )
    notes = result.scalars().all()

    return TranscriptNoteHistory(
        versions=[
            TranscriptNoteBase(
                id=n.id,
                transcript_id=n.transcript_id,
                content=n.content,
                version=n.version,
                created_at=n.created_at.isoformat() if n.created_at else "",
            )
            for n in notes
        ]
    )


@router.put("/transcripts/{transcript_id}/notes", response_model=TranscriptNoteCurrent)
async def update_transcript_note(
    transcript_id: int,
    body: TranscriptNoteUpdate,
    db: AsyncSession = Depends(get_db),
):
    """Save a note (creates a new version)."""
    await _get_transcript_or_404(transcript_id, db)

    # Get current max version
    result = await db.execute(
        select(func.max(TranscriptNote.version)).where(
            TranscriptNote.transcript_id == transcript_id
        )
    )
    max_version = result.scalar_one() or 0
    new_version = max_version + 1

    note = TranscriptNote(
        transcript_id=transcript_id,
        content=body.content,
        version=new_version,
    )
    db.add(note)
    await db.flush()

    # Regenerate context notes file
    await write_context_notes_file(transcript_id, db)

    await db.commit()
    await db.refresh(note)

    # Get version count
    count_result = await db.execute(
        select(func.count(TranscriptNote.id)).where(
            TranscriptNote.transcript_id == transcript_id
        )
    )
    version_count = count_result.scalar_one()

    return TranscriptNoteCurrent(
        content=note.content,
        version=note.version,
        created_at=note.created_at.isoformat() if note.created_at else "",
        version_count=version_count,
    )


# ── Attachment endpoints ─────────────────────────────────────────────

def _attachment_base(a: TranscriptAttachment) -> TranscriptAttachmentBase:
    return TranscriptAttachmentBase(
        id=a.id,
        transcript_id=a.transcript_id,
        original_filename=a.original_filename,
        file_type=a.file_type,
        size_bytes=a.size_bytes,
        has_extracted_text=a.extracted_text is not None and len(a.extracted_text) > 0,
        created_at=a.created_at.isoformat() if a.created_at else "",
    )


@router.get(
    "/transcripts/{transcript_id}/attachments",
    response_model=list[TranscriptAttachmentBase],
)
async def list_transcript_attachments(
    transcript_id: int,
    db: AsyncSession = Depends(get_db),
):
    """List all attachments for a transcript (metadata only, no binary)."""
    await _get_transcript_or_404(transcript_id, db)

    result = await db.execute(
        select(TranscriptAttachment)
        .where(TranscriptAttachment.transcript_id == transcript_id)
        .order_by(TranscriptAttachment.created_at)
    )
    attachments = result.scalars().all()
    return [_attachment_base(a) for a in attachments]


@router.post(
    "/transcripts/{transcript_id}/attachments",
    response_model=list[TranscriptAttachmentBase],
)
async def upload_transcript_attachments(
    transcript_id: int,
    files: list[UploadFile] = File(...),
    db: AsyncSession = Depends(get_db),
):
    """Upload one or more attachment files for a transcript."""
    await _get_transcript_or_404(transcript_id, db)

    results = []
    for file in files:
        attachment = await save_attachment(transcript_id, file, db)
        results.append(_attachment_base(attachment))

    await db.commit()
    return results


@router.get(
    "/transcripts/{transcript_id}/attachments/{attachment_id}",
    response_model=TranscriptAttachmentDetail,
)
async def get_transcript_attachment(
    transcript_id: int,
    attachment_id: int,
    db: AsyncSession = Depends(get_db),
):
    """Get attachment metadata including extracted text."""
    result = await db.execute(
        select(TranscriptAttachment).where(
            TranscriptAttachment.id == attachment_id,
            TranscriptAttachment.transcript_id == transcript_id,
        )
    )
    attachment = result.scalar_one_or_none()
    if not attachment:
        raise NotFoundError("Attachment", attachment_id)

    return TranscriptAttachmentDetail(
        id=attachment.id,
        transcript_id=attachment.transcript_id,
        original_filename=attachment.original_filename,
        file_type=attachment.file_type,
        size_bytes=attachment.size_bytes,
        has_extracted_text=attachment.extracted_text is not None and len(attachment.extracted_text) > 0,
        created_at=attachment.created_at.isoformat() if attachment.created_at else "",
        extracted_text=attachment.extracted_text,
    )


@router.get("/transcripts/{transcript_id}/attachments/{attachment_id}/download")
async def download_transcript_attachment(
    transcript_id: int,
    attachment_id: int,
    db: AsyncSession = Depends(get_db),
):
    """Download the attachment file."""
    result = await db.execute(
        select(TranscriptAttachment).where(
            TranscriptAttachment.id == attachment_id,
            TranscriptAttachment.transcript_id == transcript_id,
        )
    )
    attachment = result.scalar_one_or_none()
    if not attachment:
        raise NotFoundError("Attachment", attachment_id)

    return StreamingResponse(
        io.BytesIO(attachment.file_data),
        media_type=attachment.mime_type,
        headers={
            "Content-Disposition": f'attachment; filename="{attachment.original_filename}"',
            "Content-Length": str(attachment.size_bytes),
        },
    )


@router.delete("/transcripts/{transcript_id}/attachments/{attachment_id}")
async def delete_transcript_attachment(
    transcript_id: int,
    attachment_id: int,
    db: AsyncSession = Depends(get_db),
):
    """Delete an attachment."""
    await delete_attachment(attachment_id, transcript_id, db)
    await db.commit()
    return {"status": "deleted"}


# ── Context endpoint (for analysis workflow) ─────────────────────────

@router.get(
    "/transcripts/{transcript_id}/context",
    response_model=TranscriptContextResponse,
)
async def get_transcript_context(
    transcript_id: int,
    db: AsyncSession = Depends(get_db),
):
    """Get all analysis context for a transcript (notes + attachment text).

    Used by the analysis workflow to include supporting context.
    """
    await _get_transcript_or_404(transcript_id, db)

    # Get latest note
    note_result = await db.execute(
        select(TranscriptNote)
        .where(TranscriptNote.transcript_id == transcript_id)
        .order_by(TranscriptNote.version.desc())
        .limit(1)
    )
    latest_note = note_result.scalar_one_or_none()

    # Get attachments with extracted text
    att_result = await db.execute(
        select(TranscriptAttachment)
        .where(TranscriptAttachment.transcript_id == transcript_id)
        .order_by(TranscriptAttachment.created_at)
    )
    attachments = att_result.scalars().all()

    return TranscriptContextResponse(
        notes=latest_note.content if latest_note else None,
        attachments=[
            {
                "filename": a.original_filename,
                "extracted_text": a.extracted_text,
            }
            for a in attachments
        ],
    )
