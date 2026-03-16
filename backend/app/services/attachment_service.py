"""Service for managing transcript attachments and generating context files."""

import logging
import os
import re
import uuid
from pathlib import Path

from fastapi import UploadFile
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.models.transcript import Transcript
from app.models.transcript_attachment import TranscriptAttachment
from app.models.transcript_note import TranscriptNote
from app.services.text_extraction import extract_text

logger = logging.getLogger(__name__)

MAX_ATTACHMENT_SIZE = 25 * 1024 * 1024  # 25 MB
MAX_ATTACHMENTS_PER_TRANSCRIPT = 10
ALLOWED_EXTENSIONS = {".pdf", ".pptx", ".docx"}

MIME_MAP = {
    ".pdf": "application/pdf",
    ".pptx": "application/vnd.openxmlformats-officedocument.presentationml.presentation",
    ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
}


def _sanitize_filename(name: str) -> str:
    """Remove unsafe characters from filename."""
    name = os.path.basename(name)
    name = re.sub(r'[^\w\s\-.]', '', name)
    return name.strip() or "attachment"


async def save_attachment(
    transcript_id: int,
    file: UploadFile,
    db: AsyncSession,
) -> TranscriptAttachment:
    """Save an uploaded attachment file.

    Stores binary in DB (for Railway persistence) and optionally on filesystem.
    Extracts text content for analysis.
    """
    # Validate extension
    original_filename = file.filename or "unknown"
    ext = os.path.splitext(original_filename)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise ValueError(f"File type {ext} not allowed. Accepted: {', '.join(ALLOWED_EXTENSIONS)}")

    # Read and validate size
    file_bytes = await file.read()
    if len(file_bytes) > MAX_ATTACHMENT_SIZE:
        raise ValueError(
            f"File too large ({len(file_bytes) // (1024*1024)}MB). "
            f"Max is {MAX_ATTACHMENT_SIZE // (1024*1024)}MB."
        )

    # Check attachment count limit
    count_result = await db.execute(
        select(func.count(TranscriptAttachment.id)).where(
            TranscriptAttachment.transcript_id == transcript_id
        )
    )
    current_count = count_result.scalar_one()
    if current_count >= MAX_ATTACHMENTS_PER_TRANSCRIPT:
        raise ValueError(
            f"Maximum {MAX_ATTACHMENTS_PER_TRANSCRIPT} attachments per transcript."
        )

    # Generate stored filename
    sanitized = _sanitize_filename(original_filename)
    stored_filename = f"{uuid.uuid4().hex[:12]}_{sanitized}"
    file_type = ext.lstrip(".")
    mime_type = MIME_MAP.get(ext, "application/octet-stream")

    # Extract text
    extracted_text = extract_text(file_bytes, file_type)

    # Write to filesystem (best-effort for local dev)
    storage_path = None
    try:
        attach_dir = Path(settings.DATA_ROOT) / "Attachments" / str(transcript_id)
        attach_dir.mkdir(parents=True, exist_ok=True)
        file_path = attach_dir / stored_filename
        file_path.write_bytes(file_bytes)
        storage_path = f"Attachments/{transcript_id}/{stored_filename}"
    except Exception as e:
        logger.warning("Failed to write attachment to filesystem: %s", e)

    # Create DB record
    attachment = TranscriptAttachment(
        transcript_id=transcript_id,
        original_filename=original_filename,
        stored_filename=stored_filename,
        file_type=file_type,
        mime_type=mime_type,
        size_bytes=len(file_bytes),
        file_data=file_bytes,
        extracted_text=extracted_text,
        storage_path=storage_path,
    )
    db.add(attachment)
    await db.flush()

    # Regenerate context notes file
    await write_context_notes_file(transcript_id, db)

    return attachment


async def delete_attachment(
    attachment_id: int,
    transcript_id: int,
    db: AsyncSession,
) -> None:
    """Delete an attachment from DB and filesystem."""
    result = await db.execute(
        select(TranscriptAttachment).where(
            TranscriptAttachment.id == attachment_id,
            TranscriptAttachment.transcript_id == transcript_id,
        )
    )
    attachment = result.scalar_one_or_none()
    if not attachment:
        raise ValueError("Attachment not found")

    # Remove from filesystem
    if attachment.storage_path:
        try:
            file_path = Path(settings.DATA_ROOT) / attachment.storage_path
            if file_path.exists():
                file_path.unlink()
        except Exception as e:
            logger.warning("Failed to delete attachment file: %s", e)

    await db.delete(attachment)
    await db.flush()

    # Regenerate context notes file
    await write_context_notes_file(transcript_id, db)


def _format_size(size_bytes: int) -> str:
    """Format bytes as human-readable string."""
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    else:
        return f"{size_bytes / (1024 * 1024):.1f} MB"


async def write_context_notes_file(
    transcript_id: int,
    db: AsyncSession,
) -> None:
    """Generate/update the offline context notes markdown file.

    Writes to analysis/context_notes/{YYYY-MM-DD_-_Title}.md
    """
    from app.database import utcnow

    # Get transcript info for filename
    t_result = await db.execute(
        select(Transcript).where(Transcript.id == transcript_id)
    )
    transcript = t_result.scalar_one_or_none()
    if not transcript:
        return

    # Get latest note
    note_result = await db.execute(
        select(TranscriptNote)
        .where(TranscriptNote.transcript_id == transcript_id)
        .order_by(TranscriptNote.version.desc())
        .limit(1)
    )
    latest_note = note_result.scalar_one_or_none()

    # Get all attachments
    att_result = await db.execute(
        select(TranscriptAttachment)
        .where(TranscriptAttachment.transcript_id == transcript_id)
        .order_by(TranscriptAttachment.created_at)
    )
    attachments = att_result.scalars().all()

    # If no notes and no attachments, remove context file if it exists
    if not latest_note and not attachments:
        _remove_context_file(transcript)
        return

    # Build filename stem from transcript filename
    stem = os.path.splitext(transcript.filename)[0]

    # Build markdown content
    lines = [
        f"# Context Notes: {transcript.title}",
        f"**Transcript:** {transcript.filename}",
        f"**Last updated:** {utcnow().isoformat()}Z",
        "",
    ]

    if latest_note:
        lines.extend([
            "## Analyst Notes",
            latest_note.content,
            "",
        ])

    if attachments:
        lines.append("## Supporting Documents")
        lines.append("")
        for att in attachments:
            size_str = _format_size(att.size_bytes)
            lines.append(f"### {att.original_filename} ({att.file_type.upper()}, {size_str})")
            if att.extracted_text:
                lines.append(att.extracted_text)
            else:
                lines.append("*[Text extraction not available]*")
            lines.append("")

    # Write file
    try:
        context_dir = Path(settings.DATA_ROOT) / "analysis" / "context_notes"
        context_dir.mkdir(parents=True, exist_ok=True)
        file_path = context_dir / f"{stem}.md"
        file_path.write_text("\n".join(lines), encoding="utf-8")
        logger.info("Wrote context notes file: %s", file_path)
    except Exception as e:
        logger.warning("Failed to write context notes file: %s", e)


def _remove_context_file(transcript: Transcript) -> None:
    """Remove context notes file if it exists."""
    try:
        stem = os.path.splitext(transcript.filename)[0]
        file_path = Path(settings.DATA_ROOT) / "analysis" / "context_notes" / f"{stem}.md"
        if file_path.exists():
            file_path.unlink()
    except Exception as e:
        logger.warning("Failed to remove context notes file: %s", e)
