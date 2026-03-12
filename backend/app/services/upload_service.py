"""
Service for processing uploaded transcript files.

Reuses parsing logic from scripts/parsers/transcript_parser.py and
mention-building logic from scripts/import_data.py, adapted to work
with in-memory file bytes rather than filesystem paths.
"""

import hashlib
import logging
import re
from datetime import datetime
from pathlib import Path

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.models.stakeholder import Stakeholder
from app.models.transcript import Transcript
from app.models.transcript_mention import TranscriptMention

# Import parsing helpers from existing transcript parser
from scripts.parsers.transcript_parser import (
    _extract_participants,
    _parse_date_and_title,
)

logger = logging.getLogger(__name__)


def _compute_hash(content_bytes: bytes) -> str:
    """Compute SHA256 hash of raw bytes."""
    return hashlib.sha256(content_bytes).hexdigest()


def _save_to_filesystem(filename: str, content: str) -> None:
    """Write transcript to Transcripts/ directory on disk.

    This ensures uploaded transcripts are available on the host filesystem
    for offline analysis by Claude Code. Failures are logged but never
    raised — the DB is the primary store.
    """
    transcripts_dir = Path(settings.DATA_ROOT) / "Transcripts"
    try:
        transcripts_dir.mkdir(parents=True, exist_ok=True)
        filepath = transcripts_dir / filename
        filepath.write_text(content, encoding="utf-8")
        logger.info("Saved transcript to filesystem: %s", filepath)
    except OSError as e:
        logger.warning("Could not save transcript to filesystem: %s", e)


async def _rebuild_mentions_for_transcript(
    session: AsyncSession, transcript: Transcript
) -> dict:
    """Build transcript_mentions for a single transcript.

    Matches stakeholder names against transcript content and participants,
    mirroring the logic in import_data.build_transcript_mentions() but
    scoped to one transcript.
    """
    stats = {"speaker": 0, "mentioned": 0}

    # Clear existing mentions for this transcript
    await session.execute(
        delete(TranscriptMention).where(
            TranscriptMention.transcript_id == transcript.id
        )
    )

    # Load all stakeholders
    result = await session.execute(select(Stakeholder))
    stakeholders = result.scalars().all()

    if not stakeholders:
        return stats

    # Build name variants for each stakeholder
    stakeholder_variants: dict[int, list[str]] = {}
    for sh in stakeholders:
        variants = [sh.name]
        parts = sh.name.split()
        if len(parts) > 1:
            first = parts[0]
            if len(first) > 3:
                variants.append(first)
        paren_match = re.match(r"^(.+?)\s*\((.+?)\)", sh.name)
        if paren_match:
            variants.append(paren_match.group(1).strip())
            variants.append(paren_match.group(2).strip())
        stakeholder_variants[sh.id] = variants

    participants_lower = [p.lower() for p in (transcript.participants or [])]
    content_lower = transcript.content.lower() if transcript.content else ""

    for sh in stakeholders:
        variants = stakeholder_variants[sh.id]
        is_speaker = False
        mention_count = 0

        # Check if any variant matches a participant (speaker)
        for variant in variants:
            variant_lower = variant.lower()
            for participant in participants_lower:
                if variant_lower in participant or participant in variant_lower:
                    is_speaker = True
                    break
            if is_speaker:
                break

        # Count mentions in content
        for variant in variants:
            variant_lower = variant.lower()
            if len(variant_lower) < 3:
                continue
            if len(variant_lower) <= 5:
                pattern = r"\b" + re.escape(variant_lower) + r"\b"
                mention_count += len(re.findall(pattern, content_lower))
            else:
                mention_count += content_lower.count(variant_lower)

        if is_speaker:
            session.add(
                TranscriptMention(
                    transcript_id=transcript.id,
                    stakeholder_id=sh.id,
                    mention_type="speaker",
                    mention_count=mention_count if mention_count > 0 else 1,
                )
            )
            stats["speaker"] += 1
        elif mention_count > 0:
            session.add(
                TranscriptMention(
                    transcript_id=transcript.id,
                    stakeholder_id=sh.id,
                    mention_type="mentioned",
                    mention_count=mention_count,
                )
            )
            stats["mentioned"] += 1

    return stats


async def process_uploaded_transcript(
    filename: str,
    content_bytes: bytes,
    db: AsyncSession,
    primary_project_id: int | None = None,
    secondary_project_id: int | None = None,
    tertiary_project_id: int | None = None,
) -> dict:
    """Process a single uploaded transcript file.

    Parses the filename for date/title, extracts speakers from content,
    computes a SHA256 hash, and upserts into the transcripts table.
    Then rebuilds transcript mentions for this transcript.

    Returns:
        Dict with keys: status ("inserted"|"updated"|"skipped"),
        id, filename, title
    """
    file_hash = _compute_hash(content_bytes)
    content = content_bytes.decode("utf-8", errors="replace")

    # Parse filename for date and title
    meeting_date, title = _parse_date_and_title(filename)

    if meeting_date is None:
        return {
            "status": "error",
            "id": None,
            "filename": filename,
            "title": title,
            "error": f"Could not parse date from filename: {filename}",
        }

    # Extract participants and compute word count
    participants = _extract_participants(content)
    word_count = len(content.split())

    # Check for existing transcript with same filename
    result = await db.execute(
        select(Transcript).where(Transcript.filename == filename)
    )
    existing = result.scalar_one_or_none()

    if existing:
        if existing.file_hash == file_hash:
            # Even if content unchanged, update projects if provided
            changed = False
            if primary_project_id is not None and existing.primary_project_id != primary_project_id:
                existing.primary_project_id = primary_project_id
                changed = True
            if secondary_project_id is not None and existing.secondary_project_id != secondary_project_id:
                existing.secondary_project_id = secondary_project_id
                changed = True
            if tertiary_project_id is not None and existing.tertiary_project_id != tertiary_project_id:
                existing.tertiary_project_id = tertiary_project_id
                changed = True
            if changed:
                await db.flush()
                await db.commit()
            return {
                "status": "skipped",
                "id": existing.id,
                "filename": filename,
                "title": existing.title,
            }
        # Update existing
        existing.title = title
        existing.meeting_date = meeting_date
        existing.content = content
        existing.word_count = word_count
        existing.participants = participants
        existing.file_hash = file_hash
        existing.source_file = f"Transcripts/{filename}"
        existing.updated_at = datetime.utcnow()
        if primary_project_id is not None:
            existing.primary_project_id = primary_project_id
        if secondary_project_id is not None:
            existing.secondary_project_id = secondary_project_id
        if tertiary_project_id is not None:
            existing.tertiary_project_id = tertiary_project_id
        await db.flush()

        # Rebuild mentions for this transcript
        await _rebuild_mentions_for_transcript(db, existing)
        await db.commit()

        _save_to_filesystem(filename, content)

        return {
            "status": "updated",
            "id": existing.id,
            "filename": filename,
            "title": title,
        }
    else:
        # Insert new
        transcript = Transcript(
            filename=filename,
            title=title,
            meeting_date=meeting_date,
            content=content,
            word_count=word_count,
            participants=participants,
            primary_project_id=primary_project_id,
            secondary_project_id=secondary_project_id,
            tertiary_project_id=tertiary_project_id,
            source_file=f"Transcripts/{filename}",
            file_hash=file_hash,
        )
        db.add(transcript)
        await db.flush()  # Get the ID

        # Rebuild mentions for this transcript
        await _rebuild_mentions_for_transcript(db, transcript)
        await db.commit()

        _save_to_filesystem(filename, content)

        return {
            "status": "inserted",
            "id": transcript.id,
            "filename": filename,
            "title": title,
        }
