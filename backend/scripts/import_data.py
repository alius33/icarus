"""
Main data import orchestrator for the Icarus dashboard.

Imports all parsed data into PostgreSQL using async SQLAlchemy.
Supports idempotent upsert: skip if hash matches, update if changed, insert if new.

Usage:
    python -m scripts.import_data --data-root /path/to/icarus --db-url postgresql+asyncpg://...
    python -m scripts.import_data --data-root /path/to/icarus --verbose
"""

import argparse
import asyncio
import hashlib
import os
import re
import sys
import traceback
from datetime import datetime
from pathlib import Path

from sqlalchemy import delete, select, text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

# Add the backend directory to the path so we can import app models
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.models import (
    ActionItem,
    Commitment,
    Contradiction,
    Decision,
    DeletedImport,
    Document,
    GlossaryEntry,
    InfluenceSignal,
    MeetingScore,
    OpenThread,
    Project,
    ProjectSummary,
    RiskEntry,
    SentimentSignal,
    Stakeholder,
    Summary,
    TopicSignal,
    Transcript,
    TranscriptMention,
    WeeklyReport,
    Workstream,
    WorkstreamMilestone,
)
from scripts.parsers.action_item_parser import parse_action_items
from scripts.parsers.commitment_parser import parse_commitments
from scripts.parsers.contradiction_parser import parse_contradictions
from scripts.parsers.decision_parser import parse_decisions
from scripts.parsers.glossary_parser import parse_glossary
from scripts.parsers.influence_signal_parser import parse_influence_signals
from scripts.parsers.meeting_score_parser import parse_meeting_scores
from scripts.parsers.open_thread_parser import parse_open_threads
from scripts.parsers.project_summary_parser import parse_project_summaries
from scripts.parsers.risk_entry_parser import parse_risk_entries
from scripts.parsers.sentiment_parser import parse_sentiments
from scripts.parsers.stakeholder_parser import parse_stakeholders
from scripts.parsers.topic_signal_parser import parse_topic_signals
from scripts.parsers.transcript_parser import parse_transcript
from scripts.parsers.workstream_parser import parse_workstreams


def _compute_file_hash(filepath: Path) -> str:
    """Compute SHA256 hash of file contents."""
    sha256 = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            sha256.update(chunk)
    return sha256.hexdigest()


def _log(msg: str, verbose: bool = True):
    """Print a log message if verbose mode is on."""
    if verbose:
        print(f"  {msg}")


def _slugify(name: str) -> str:
    """Generate a URL-friendly slug from a project name."""
    slug = name.lower().strip()
    slug = re.sub(r'[^a-z0-9]+', '-', slug)
    slug = slug.strip('-')
    return slug


# ---------------------------------------------------------------------------
# Import functions for each entity type
# ---------------------------------------------------------------------------


async def import_transcripts(
    session: AsyncSession, data_root: Path, verbose: bool
) -> dict:
    """Import transcript files from Transcripts/*.txt."""
    stats = {"inserted": 0, "updated": 0, "skipped": 0, "errors": 0}
    transcript_dir = data_root / "Transcripts"

    if not transcript_dir.exists():
        _log("Transcripts directory not found, skipping.", verbose)
        return stats

    txt_files = sorted(transcript_dir.glob("*.txt"))
    _log(f"Found {len(txt_files)} transcript files.", verbose)

    for filepath in txt_files:
        try:
            data = parse_transcript(filepath)
            if data["meeting_date"] is None:
                _log(f"  WARNING: Could not parse date from {filepath.name}, skipping.", verbose)
                stats["errors"] += 1
                continue

            result = await session.execute(
                select(Transcript).where(Transcript.filename == data["filename"])
            )
            existing = result.scalar_one_or_none()

            if existing:
                if existing.file_hash == data["file_hash"]:
                    stats["skipped"] += 1
                    continue
                # Update existing record
                for key, val in data.items():
                    if hasattr(existing, key):
                        setattr(existing, key, val)
                existing.updated_at = datetime.utcnow()
                stats["updated"] += 1
                _log(f"  Updated: {filepath.name}", verbose)
            else:
                session.add(Transcript(**data))
                stats["inserted"] += 1
                _log(f"  Inserted: {filepath.name}", verbose)

        except Exception as e:
            stats["errors"] += 1
            _log(f"  ERROR parsing {filepath.name}: {e}", verbose)
            if verbose:
                traceback.print_exc()

    await session.commit()
    return stats


async def import_stakeholders(
    session: AsyncSession, data_root: Path, verbose: bool
) -> dict:
    """Import stakeholders from context/stakeholders.md."""
    stats = {"inserted": 0, "updated": 0, "skipped": 0, "errors": 0}
    filepath = data_root / "context" / "stakeholders.md"

    if not filepath.exists():
        _log("stakeholders.md not found, skipping.", verbose)
        return stats

    try:
        stakeholder_list = parse_stakeholders(filepath)
        _log(f"Parsed {len(stakeholder_list)} stakeholders.", verbose)

        for data in stakeholder_list:
            try:
                result = await session.execute(
                    select(Stakeholder).where(Stakeholder.name == data["name"])
                )
                existing = result.scalar_one_or_none()

                if existing:
                    if existing.is_manual:
                        stats["skipped"] += 1
                        continue
                    if existing.file_hash == data["file_hash"]:
                        stats["skipped"] += 1
                        continue
                    for key, val in data.items():
                        if hasattr(existing, key):
                            setattr(existing, key, val)
                    existing.updated_at = datetime.utcnow()
                    stats["updated"] += 1
                    _log(f"  Updated: {data['name']}", verbose)
                else:
                    del_check = await session.execute(
                        select(DeletedImport).where(
                            DeletedImport.entity_type == "stakeholder",
                            DeletedImport.unique_key == data["name"],
                        )
                    )
                    if del_check.scalar_one_or_none():
                        stats["skipped"] += 1
                        continue
                    session.add(Stakeholder(**data))
                    stats["inserted"] += 1
                    _log(f"  Inserted: {data['name']}", verbose)

            except Exception as e:
                stats["errors"] += 1
                _log(f"  ERROR importing stakeholder {data.get('name', '?')}: {e}", verbose)

        await session.commit()

    except Exception as e:
        stats["errors"] += 1
        _log(f"ERROR parsing stakeholders.md: {e}", verbose)
        if verbose:
            traceback.print_exc()

    return stats


async def import_decisions(
    session: AsyncSession, data_root: Path, verbose: bool
) -> dict:
    """Import decisions from context/decisions.md."""
    stats = {"inserted": 0, "updated": 0, "skipped": 0, "errors": 0}
    filepath = data_root / "context" / "decisions.md"

    if not filepath.exists():
        _log("decisions.md not found, skipping.", verbose)
        return stats

    try:
        decision_list = parse_decisions(filepath)
        _log(f"Parsed {len(decision_list)} decisions.", verbose)

        for data in decision_list:
            try:
                result = await session.execute(
                    select(Decision).where(Decision.number == data["number"])
                )
                existing = result.scalar_one_or_none()

                if existing:
                    if existing.is_manual:
                        stats["skipped"] += 1
                        continue
                    if existing.file_hash == data["file_hash"]:
                        stats["skipped"] += 1
                        continue
                    for key, val in data.items():
                        if hasattr(existing, key):
                            setattr(existing, key, val)
                    existing.updated_at = datetime.utcnow()
                    stats["updated"] += 1
                    _log(f"  Updated: Decision #{data['number']}", verbose)
                else:
                    del_check = await session.execute(
                        select(DeletedImport).where(
                            DeletedImport.entity_type == "decision",
                            DeletedImport.unique_key == str(data["number"]),
                        )
                    )
                    if del_check.scalar_one_or_none():
                        stats["skipped"] += 1
                        continue
                    session.add(Decision(**data))
                    stats["inserted"] += 1
                    _log(f"  Inserted: Decision #{data['number']}", verbose)

            except Exception as e:
                stats["errors"] += 1
                _log(f"  ERROR importing decision #{data.get('number', '?')}: {e}", verbose)

        await session.commit()

    except Exception as e:
        stats["errors"] += 1
        _log(f"ERROR parsing decisions.md: {e}", verbose)
        if verbose:
            traceback.print_exc()

    return stats


async def import_workstreams(
    session: AsyncSession, data_root: Path, verbose: bool
) -> dict:
    """Import workstreams and milestones from context/workstreams.md."""
    stats = {
        "workstreams": {"inserted": 0, "updated": 0, "skipped": 0, "errors": 0},
        "milestones": {"inserted": 0, "skipped": 0, "errors": 0},
    }
    filepath = data_root / "context" / "workstreams.md"

    if not filepath.exists():
        _log("workstreams.md not found, skipping.", verbose)
        return stats

    try:
        workstream_list, milestone_list = parse_workstreams(filepath)
        _log(f"Parsed {len(workstream_list)} workstreams, {len(milestone_list)} milestones.", verbose)

        # Import workstreams
        ws_code_to_id = {}
        for data in workstream_list:
            try:
                result = await session.execute(
                    select(Workstream).where(Workstream.code == data["code"])
                )
                existing = result.scalar_one_or_none()

                if existing:
                    if existing.file_hash == data["file_hash"]:
                        stats["workstreams"]["skipped"] += 1
                        ws_code_to_id[data["code"]] = existing.id
                        continue
                    for key, val in data.items():
                        if hasattr(existing, key):
                            setattr(existing, key, val)
                    existing.updated_at = datetime.utcnow()
                    stats["workstreams"]["updated"] += 1
                    ws_code_to_id[data["code"]] = existing.id
                    _log(f"  Updated: {data['code']}", verbose)
                else:
                    ws = Workstream(**data)
                    session.add(ws)
                    await session.flush()
                    ws_code_to_id[data["code"]] = ws.id
                    stats["workstreams"]["inserted"] += 1
                    _log(f"  Inserted: {data['code']}", verbose)

            except Exception as e:
                stats["workstreams"]["errors"] += 1
                _log(f"  ERROR importing workstream {data.get('code', '?')}: {e}", verbose)

        await session.commit()

        # Clear existing milestones for these workstreams and re-import
        for code, ws_id in ws_code_to_id.items():
            await session.execute(
                delete(WorkstreamMilestone).where(
                    WorkstreamMilestone.workstream_id == ws_id
                )
            )

        # Import milestones
        for data in milestone_list:
            try:
                ws_code = data.pop("workstream_code")
                ws_id = ws_code_to_id.get(ws_code)
                if ws_id is None:
                    stats["milestones"]["errors"] += 1
                    _log(f"  WARNING: No workstream found for milestone code {ws_code}", verbose)
                    continue
                milestone = WorkstreamMilestone(workstream_id=ws_id, **data)
                session.add(milestone)
                stats["milestones"]["inserted"] += 1
            except Exception as e:
                stats["milestones"]["errors"] += 1
                _log(f"  ERROR importing milestone: {e}", verbose)

        await session.commit()

    except Exception as e:
        stats["workstreams"]["errors"] += 1
        _log(f"ERROR parsing workstreams.md: {e}", verbose)
        if verbose:
            traceback.print_exc()

    return stats


async def import_open_threads(
    session: AsyncSession, data_root: Path, verbose: bool
) -> dict:
    """Import open threads from context/open_threads.md."""
    stats = {"inserted": 0, "updated": 0, "skipped": 0, "errors": 0}
    filepath = data_root / "context" / "open_threads.md"

    if not filepath.exists():
        _log("open_threads.md not found, skipping.", verbose)
        return stats

    try:
        thread_list = parse_open_threads(filepath)
        _log(f"Parsed {len(thread_list)} open threads.", verbose)

        for data in thread_list:
            try:
                # Use number + status as unique key (numbers restart per section)
                result = await session.execute(
                    select(OpenThread).where(
                        OpenThread.number == data["number"],
                        OpenThread.status == data["status"],
                    )
                )
                existing = result.scalar_one_or_none()

                if existing:
                    if existing.is_manual:
                        stats["skipped"] += 1
                        continue
                    if existing.file_hash == data["file_hash"]:
                        stats["skipped"] += 1
                        continue
                    for key, val in data.items():
                        if hasattr(existing, key):
                            setattr(existing, key, val)
                    existing.updated_at = datetime.utcnow()
                    stats["updated"] += 1
                    _log(f"  Updated: Thread #{data['number']} ({data['status']})", verbose)
                else:
                    del_check = await session.execute(
                        select(DeletedImport).where(
                            DeletedImport.entity_type == "open_thread",
                            DeletedImport.unique_key == f"{data['number']}:{data['status']}",
                        )
                    )
                    if del_check.scalar_one_or_none():
                        stats["skipped"] += 1
                        continue
                    session.add(OpenThread(**data))
                    stats["inserted"] += 1
                    _log(f"  Inserted: Thread #{data['number']} - {data['title']}", verbose)

            except Exception as e:
                stats["errors"] += 1
                _log(f"  ERROR importing thread #{data.get('number', '?')}: {e}", verbose)

        await session.commit()

    except Exception as e:
        stats["errors"] += 1
        _log(f"ERROR parsing open_threads.md: {e}", verbose)
        if verbose:
            traceback.print_exc()

    return stats


async def import_action_items(
    session: AsyncSession, data_root: Path, verbose: bool
) -> dict:
    """Import action items from analysis/trackers/action_items.md."""
    stats = {"inserted": 0, "updated": 0, "skipped": 0, "errors": 0}
    filepath = data_root / "analysis" / "trackers" / "action_items.md"

    if not filepath.exists():
        _log("action_items.md not found, skipping.", verbose)
        return stats

    try:
        item_list = parse_action_items(filepath)
        _log(f"Parsed {len(item_list)} action items.", verbose)

        for data in item_list:
            try:
                # Map old status to new Task status
                _STATUS_MAP = {
                    "OPEN": "TODO",
                    "IN PROGRESS": "IN_PROGRESS",
                    "COMPLETED": "DONE",
                    "LIKELY COMPLETED": "IN_REVIEW",
                    "LIKELY_COMPLETED": "IN_REVIEW",
                    "BLOCKED": "TODO",
                }
                raw_status = data.get("status", "OPEN")
                data["status"] = _STATUS_MAP.get(raw_status, raw_status)

                # Populate title from description for Task model
                if "title" not in data or not data.get("title"):
                    desc = data.get("description", "")
                    data["title"] = (desc[:200] if desc else f"Action {data.get('number', '?')}")
                # Default new Task fields — use status suffix to avoid
                # collisions when same number appears in OPEN + COMPLETED
                if "identifier" not in data or not data.get("identifier"):
                    num = data.get('number', '0')
                    status_suffix = data.get("status", "TODO")
                    if status_suffix in ("DONE", "IN_REVIEW", "IN_PROGRESS"):
                        data["identifier"] = f"ACT-{num}-{status_suffix}"
                    else:
                        data["identifier"] = f"ACT-{num}"
                # Map parser fields to Task model fields for the UI
                if data.get("owner") and not data.get("assignee"):
                    data["assignee"] = data["owner"]
                if data.get("action_date") and not data.get("created_date"):
                    data["created_date"] = data["action_date"]
                data.setdefault("priority", "NONE")
                data.setdefault("labels", [])
                data.setdefault("position", 0)

                # Use number + mapped status as unique key
                result = await session.execute(
                    select(ActionItem).where(
                        ActionItem.number == data["number"],
                        ActionItem.status == data["status"],
                    )
                )
                existing = result.scalar_one_or_none()

                if existing:
                    if existing.is_manual:
                        stats["skipped"] += 1
                        continue
                    if existing.file_hash == data["file_hash"]:
                        stats["skipped"] += 1
                        continue
                    for key, val in data.items():
                        if hasattr(existing, key):
                            setattr(existing, key, val)
                    existing.updated_at = datetime.utcnow()
                    stats["updated"] += 1
                    _log(f"  Updated: Action #{data['number']}", verbose)
                else:
                    del_check = await session.execute(
                        select(DeletedImport).where(
                            DeletedImport.entity_type.in_(["action_item", "task"]),
                            DeletedImport.unique_key == f"{data['number']}:{data['status']}",
                        )
                    )
                    if del_check.scalar_one_or_none():
                        stats["skipped"] += 1
                        continue
                    session.add(ActionItem(**data))
                    stats["inserted"] += 1
                    _log(f"  Inserted: Action #{data['number']} - {data['description'][:60]}", verbose)

            except Exception as e:
                stats["errors"] += 1
                _log(f"  ERROR importing action #{data.get('number', '?')}: {e}", verbose)

        await session.commit()

    except Exception as e:
        stats["errors"] += 1
        _log(f"ERROR parsing action_items.md: {e}", verbose)
        if verbose:
            traceback.print_exc()

    return stats


async def import_glossary(
    session: AsyncSession, data_root: Path, verbose: bool
) -> dict:
    """Import glossary entries from context/glossary.md."""
    stats = {"inserted": 0, "updated": 0, "skipped": 0, "errors": 0}
    filepath = data_root / "context" / "glossary.md"

    if not filepath.exists():
        _log("glossary.md not found, skipping.", verbose)
        return stats

    try:
        entry_list = parse_glossary(filepath)
        _log(f"Parsed {len(entry_list)} glossary entries.", verbose)

        for data in entry_list:
            try:
                result = await session.execute(
                    select(GlossaryEntry).where(GlossaryEntry.term == data["term"])
                )
                existing = result.scalar_one_or_none()

                if existing:
                    if existing.is_manual:
                        stats["skipped"] += 1
                        continue
                    if existing.file_hash == data["file_hash"]:
                        stats["skipped"] += 1
                        continue
                    for key, val in data.items():
                        if hasattr(existing, key):
                            setattr(existing, key, val)
                    existing.updated_at = datetime.utcnow()
                    stats["updated"] += 1
                    _log(f"  Updated: {data['term']}", verbose)
                else:
                    del_check = await session.execute(
                        select(DeletedImport).where(
                            DeletedImport.entity_type == "glossary",
                            DeletedImport.unique_key == data["term"],
                        )
                    )
                    if del_check.scalar_one_or_none():
                        stats["skipped"] += 1
                        continue
                    session.add(GlossaryEntry(**data))
                    stats["inserted"] += 1
                    _log(f"  Inserted: {data['term']}", verbose)

            except Exception as e:
                stats["errors"] += 1
                _log(f"  ERROR importing glossary term '{data.get('term', '?')}': {e}", verbose)

        await session.commit()

    except Exception as e:
        stats["errors"] += 1
        _log(f"ERROR parsing glossary.md: {e}", verbose)
        if verbose:
            traceback.print_exc()

    return stats


async def import_summaries(
    session: AsyncSession, data_root: Path, verbose: bool
) -> dict:
    """Import summary files from analysis/summaries/*.md."""
    stats = {"inserted": 0, "updated": 0, "skipped": 0, "errors": 0}
    summaries_dir = data_root / "analysis" / "summaries"

    if not summaries_dir.exists():
        _log("analysis/summaries directory not found, skipping.", verbose)
        return stats

    md_files = sorted(summaries_dir.glob("*.md"))
    if not md_files:
        _log("No summary files found.", verbose)
        return stats

    _log(f"Found {len(md_files)} summary files.", verbose)

    for filepath in md_files:
        try:
            filename = filepath.name
            content = filepath.read_text(encoding="utf-8", errors="replace")
            file_hash = _compute_file_hash(filepath)
            source_file = str(filepath.relative_to(data_root))

            # Try to link to a transcript by matching date + title
            transcript_id = None
            base_name = filepath.stem  # e.g., "2026-01-06_-_Ben_explains_new_dashboard"

            # Parse date from summary filename (YYYY-MM-DD prefix)
            date_match = re.match(r'^(\d{4})-(\d{2})-(\d{2})', base_name)
            if date_match:
                try:
                    summary_date = datetime.strptime(
                        f"{date_match.group(1)}-{date_match.group(2)}-{date_match.group(3)}",
                        "%Y-%m-%d"
                    ).date()
                    # Query transcripts with matching meeting_date
                    result = await session.execute(
                        select(Transcript).where(
                            Transcript.meeting_date == summary_date
                        )
                    )
                    candidates = result.scalars().all()
                    if len(candidates) == 1:
                        transcript_id = candidates[0].id
                    elif len(candidates) > 1:
                        # Multiple transcripts on the same date — fuzzy match title
                        # Extract title portion after date prefix
                        title_part = re.sub(r'^\d{4}-\d{2}-\d{2}[_\s]*-?[_\s]*', '', base_name)
                        title_norm = title_part.replace("_", " ").lower().strip()
                        best_score = 0
                        best_match = None
                        for t in candidates:
                            t_stem = Path(t.filename).stem
                            # Strip date prefix (DD-MM-YYYY or YYYY-MM-DD)
                            t_title = re.sub(r'^[\d-]+[_\s]*-?[_\s]*', '', t_stem)
                            t_title_norm = t_title.replace("_", " ").lower().strip()
                            # Simple overlap score: count common words
                            s_words = set(title_norm.split())
                            t_words = set(t_title_norm.split())
                            overlap = len(s_words & t_words)
                            if overlap > best_score:
                                best_score = overlap
                                best_match = t
                        if best_match and best_score > 0:
                            transcript_id = best_match.id
                except ValueError:
                    pass

            # Fallback: try direct LIKE match
            if transcript_id is None:
                result = await session.execute(
                    select(Transcript).where(
                        Transcript.filename.like(f"{base_name}%")
                    )
                )
                matching_transcript = result.scalar_one_or_none()
                if matching_transcript:
                    transcript_id = matching_transcript.id

            result = await session.execute(
                select(Summary).where(Summary.filename == filename)
            )
            existing = result.scalar_one_or_none()

            if existing:
                if existing.file_hash == file_hash:
                    stats["skipped"] += 1
                    continue
                existing.content = content
                existing.file_hash = file_hash
                existing.source_file = source_file
                existing.transcript_id = transcript_id
                existing.updated_at = datetime.utcnow()
                stats["updated"] += 1
                _log(f"  Updated: {filename}", verbose)
            else:
                session.add(Summary(
                    filename=filename,
                    content=content,
                    source_file=source_file,
                    file_hash=file_hash,
                    transcript_id=transcript_id,
                ))
                stats["inserted"] += 1
                _log(f"  Inserted: {filename}", verbose)

        except Exception as e:
            stats["errors"] += 1
            _log(f"  ERROR importing summary {filepath.name}: {e}", verbose)

    await session.commit()
    return stats


async def import_weekly_reports(
    session: AsyncSession, data_root: Path, verbose: bool
) -> dict:
    """Import weekly report files from analysis/weekly/*.md."""
    stats = {"inserted": 0, "updated": 0, "skipped": 0, "errors": 0}
    weekly_dir = data_root / "analysis" / "weekly"

    if not weekly_dir.exists():
        _log("analysis/weekly directory not found, skipping.", verbose)
        return stats

    md_files = sorted(weekly_dir.glob("*.md"))
    if not md_files:
        _log("No weekly report files found.", verbose)
        return stats

    _log(f"Found {len(md_files)} weekly report files.", verbose)

    for filepath in md_files:
        try:
            filename = filepath.name
            content = filepath.read_text(encoding="utf-8", errors="replace")
            file_hash = _compute_file_hash(filepath)
            source_file = str(filepath.relative_to(data_root))

            # Extract title from first heading or filename
            title = filename.replace(".md", "").replace("_", " ").replace("-", " ")
            for line in content.splitlines():
                if line.startswith("# "):
                    title = line.lstrip("# ").strip()
                    break

            # Try to parse week dates from filename
            # Expected patterns: "week_2026-01-06_to_2026-01-12.md" or similar
            week_start = None
            week_end = None
            date_matches = re.findall(r'(\d{4}-\d{2}-\d{2})', filename)
            if len(date_matches) >= 2:
                try:
                    week_start = datetime.strptime(date_matches[0], "%Y-%m-%d").date()
                    week_end = datetime.strptime(date_matches[1], "%Y-%m-%d").date()
                except ValueError:
                    pass
            elif len(date_matches) == 1:
                try:
                    week_start = datetime.strptime(date_matches[0], "%Y-%m-%d").date()
                except ValueError:
                    pass

            result = await session.execute(
                select(WeeklyReport).where(WeeklyReport.filename == filename)
            )
            existing = result.scalar_one_or_none()

            if existing:
                if existing.file_hash == file_hash:
                    stats["skipped"] += 1
                    continue
                existing.title = title
                existing.content = content
                existing.week_start = week_start
                existing.week_end = week_end
                existing.file_hash = file_hash
                existing.source_file = source_file
                existing.updated_at = datetime.utcnow()
                stats["updated"] += 1
                _log(f"  Updated: {filename}", verbose)
            else:
                session.add(WeeklyReport(
                    filename=filename,
                    title=title,
                    content=content,
                    week_start=week_start,
                    week_end=week_end,
                    source_file=source_file,
                    file_hash=file_hash,
                ))
                stats["inserted"] += 1
                _log(f"  Inserted: {filename}", verbose)

        except Exception as e:
            stats["errors"] += 1
            _log(f"  ERROR importing weekly report {filepath.name}: {e}", verbose)

    await session.commit()
    return stats


async def import_programme_debrief(
    session: AsyncSession, data_root: Path, verbose: bool
) -> dict:
    """Import programme_debrief.md as a document."""
    stats = {"inserted": 0, "updated": 0, "skipped": 0, "errors": 0}
    filepath = data_root / "programme_debrief.md"

    if not filepath.exists():
        _log("programme_debrief.md not found, skipping.", verbose)
        return stats

    try:
        filename = filepath.name
        content = filepath.read_text(encoding="utf-8", errors="replace")
        file_hash = _compute_file_hash(filepath)
        source_file = str(filepath.relative_to(data_root))

        # Extract title from first heading
        title = "Programme Debrief"
        for line in content.splitlines():
            if line.startswith("# "):
                title = line.lstrip("# ").strip()
                break

        result = await session.execute(
            select(Document).where(Document.filename == filename)
        )
        existing = result.scalar_one_or_none()

        if existing:
            if existing.file_hash == file_hash:
                stats["skipped"] += 1
                _log(f"  Skipped (unchanged): {filename}", verbose)
            else:
                existing.title = title
                existing.content = content
                existing.doc_type = "debrief"
                existing.file_hash = file_hash
                existing.source_file = source_file
                existing.updated_at = datetime.utcnow()
                stats["updated"] += 1
                _log(f"  Updated: {filename}", verbose)
        else:
            session.add(Document(
                filename=filename,
                title=title,
                content=content,
                doc_type="debrief",
                source_file=source_file,
                file_hash=file_hash,
            ))
            stats["inserted"] += 1
            _log(f"  Inserted: {filename}", verbose)

        await session.commit()

    except Exception as e:
        stats["errors"] += 1
        _log(f"ERROR importing programme_debrief.md: {e}", verbose)
        if verbose:
            traceback.print_exc()

    return stats


async def import_project_pages(
    session: AsyncSession, data_root: Path, verbose: bool
) -> dict:
    """Import project pages from context/projects/*.md as Documents."""
    stats = {"inserted": 0, "updated": 0, "skipped": 0, "errors": 0}
    projects_dir = data_root / "context" / "projects"

    if not projects_dir.exists():
        _log("context/projects directory not found, skipping.", verbose)
        return stats

    md_files = sorted(projects_dir.glob("*.md"))
    if not md_files:
        _log("No project files found.", verbose)
        return stats

    _log(f"Found {len(md_files)} project files.", verbose)

    for filepath in md_files:
        try:
            filename = filepath.name
            content = filepath.read_text(encoding="utf-8", errors="replace")
            file_hash = _compute_file_hash(filepath)
            source_file = str(filepath.relative_to(data_root))

            # Extract title from first heading
            title = filename.replace(".md", "").replace("_", " ").title()
            for line in content.splitlines():
                if line.startswith("# "):
                    title = line.lstrip("# ").strip()
                    break

            result = await session.execute(
                select(Document).where(
                    Document.filename == filename,
                    Document.doc_type == "project",
                )
            )
            existing = result.scalar_one_or_none()

            if existing:
                if existing.file_hash == file_hash:
                    stats["skipped"] += 1
                    continue
                existing.title = title
                existing.content = content
                existing.file_hash = file_hash
                existing.source_file = source_file
                existing.updated_at = datetime.utcnow()
                stats["updated"] += 1
                _log(f"  Updated: {filename}", verbose)
            else:
                session.add(Document(
                    filename=filename,
                    title=title,
                    content=content,
                    doc_type="project",
                    source_file=source_file,
                    file_hash=file_hash,
                ))
                stats["inserted"] += 1
                _log(f"  Inserted: {filename}", verbose)

        except Exception as e:
            stats["errors"] += 1
            _log(f"  ERROR importing project page {filepath.name}: {e}", verbose)

    await session.commit()
    return stats


async def build_transcript_mentions(
    session: AsyncSession, verbose: bool
) -> dict:
    """Build the transcript_mentions table.

    For each transcript, check each stakeholder:
      - If the stakeholder appears in participants => mention_type "speaker"
      - If the stakeholder name appears in content => mention_type "mentioned" with count

    Uses first-name matching for common references (e.g., "Richard" matches
    "Richard Dosoo").
    """
    stats = {"speaker": 0, "mentioned": 0, "cleared": 0}

    # Clear existing mentions
    result = await session.execute(delete(TranscriptMention))
    stats["cleared"] = result.rowcount
    await session.flush()
    _log(f"  Cleared {stats['cleared']} existing mentions.", verbose)

    # Load all stakeholders
    result = await session.execute(select(Stakeholder))
    stakeholders = result.scalars().all()

    # Load all transcripts
    result = await session.execute(select(Transcript))
    transcripts = result.scalars().all()

    _log(f"  Building mentions: {len(transcripts)} transcripts x {len(stakeholders)} stakeholders", verbose)

    # Build name variants for each stakeholder
    # e.g., "Richard Dosoo" => ["Richard Dosoo", "Richard"]
    # "BenVH (Van Houten)" => ["BenVH", "Van Houten", "BenVH (Van Houten)"]
    stakeholder_variants: dict[int, list[str]] = {}
    for sh in stakeholders:
        variants = [sh.name]
        # Add first name if the name has multiple parts
        parts = sh.name.split()
        if len(parts) > 1:
            first = parts[0]
            # Only add first name if it's reasonably distinctive (>3 chars)
            if len(first) > 3:
                variants.append(first)
        # Handle parenthetical names like "BenVH (Van Houten)" or "Natalia (Plant)"
        paren_match = re.match(r'^(.+?)\s*\((.+?)\)', sh.name)
        if paren_match:
            variants.append(paren_match.group(1).strip())
            variants.append(paren_match.group(2).strip())
        stakeholder_variants[sh.id] = variants

    for transcript in transcripts:
        participants_lower = [p.lower() for p in (transcript.participants or [])]
        content_lower = transcript.content.lower() if transcript.content else ""

        for sh in stakeholders:
            variants = stakeholder_variants[sh.id]
            is_speaker = False
            mention_count = 0

            # Check if any variant matches a participant (speaker)
            for variant in variants:
                variant_lower = variant.lower()
                # Check participants list
                for participant in participants_lower:
                    if variant_lower in participant or participant in variant_lower:
                        is_speaker = True
                        break
                if is_speaker:
                    break

            # Count mentions in content (using all variants)
            for variant in variants:
                variant_lower = variant.lower()
                if len(variant_lower) < 3:
                    continue  # Skip very short names to avoid false positives
                # Use word boundary matching for short names
                if len(variant_lower) <= 5:
                    pattern = r'\b' + re.escape(variant_lower) + r'\b'
                    mention_count += len(re.findall(pattern, content_lower))
                else:
                    mention_count += content_lower.count(variant_lower)

            if is_speaker:
                session.add(TranscriptMention(
                    transcript_id=transcript.id,
                    stakeholder_id=sh.id,
                    mention_type="speaker",
                    mention_count=mention_count if mention_count > 0 else 1,
                ))
                stats["speaker"] += 1
            elif mention_count > 0:
                session.add(TranscriptMention(
                    transcript_id=transcript.id,
                    stakeholder_id=sh.id,
                    mention_type="mentioned",
                    mention_count=mention_count,
                ))
                stats["mentioned"] += 1

    await session.commit()
    return stats


async def import_sentiments(
    session: AsyncSession, root: Path, verbose: bool = False,
) -> dict:
    """Import sentiment signals from analysis/trackers/sentiment_tracker.md."""
    stats = {"inserted": 0, "skipped": 0, "errors": 0}
    filepath = root / "analysis" / "trackers" / "sentiment_tracker.md"
    if not filepath.exists():
        _log("No sentiment tracker file found, skipping", verbose)
        return stats

    content = filepath.read_text(encoding="utf-8")
    parsed = parse_sentiments(content)
    _log(f"Parsed {len(parsed)} sentiment entries", verbose)

    # Build stakeholder name->id map
    result = await session.execute(select(Stakeholder.id, Stakeholder.name))
    name_map = {row.name.lower(): row.id for row in result.all()}

    for entry in parsed:
        try:
            person = entry["person"]
            stakeholder_id = name_map.get(person.lower())
            if not stakeholder_id:
                # Try first name match
                first_name = person.split()[0].lower() if person else ""
                for name, sid in name_map.items():
                    if name.startswith(first_name):
                        stakeholder_id = sid
                        break
            if not stakeholder_id:
                _log(f"  Stakeholder not found: {person}", verbose)
                stats["errors"] += 1
                continue

            signal = SentimentSignal(
                stakeholder_id=stakeholder_id,
                date=entry.get("date"),
                sentiment=entry["sentiment"],
                shift=entry.get("shift"),
                topic=entry.get("topic"),
                quote=entry.get("quote"),
                is_manual=False,
            )
            session.add(signal)
            stats["inserted"] += 1
        except Exception as e:
            _log(f"  Error importing sentiment: {e}", verbose)
            stats["errors"] += 1

    await session.commit()
    return stats


async def import_commitments(
    session: AsyncSession, root: Path, verbose: bool = False,
) -> dict:
    """Import commitments from analysis/trackers/commitments.md."""
    stats = {"inserted": 0, "skipped": 0, "errors": 0}
    filepath = root / "analysis" / "trackers" / "commitments.md"
    if not filepath.exists():
        _log("No commitments tracker file found, skipping", verbose)
        return stats

    content = filepath.read_text(encoding="utf-8")
    parsed = parse_commitments(content)
    _log(f"Parsed {len(parsed)} commitment entries", verbose)

    for entry in parsed:
        try:
            commitment = Commitment(
                person=entry["person"],
                commitment=entry["commitment"],
                date_made=entry.get("date_made"),
                deadline_text=entry.get("deadline_text"),
                deadline_resolved=entry.get("deadline_resolved"),
                deadline_type=entry.get("deadline_type", "none"),
                condition=entry.get("condition"),
                status=entry.get("status", "pending"),
                is_manual=False,
            )
            session.add(commitment)
            stats["inserted"] += 1
        except Exception as e:
            _log(f"  Error importing commitment: {e}", verbose)
            stats["errors"] += 1

    await session.commit()
    return stats


async def import_topic_signals(
    session: AsyncSession, root: Path, verbose: bool = False,
) -> dict:
    """Import topic signals from analysis/trackers/topic_evolution.md."""
    stats = {"inserted": 0, "updated": 0, "skipped": 0, "errors": 0}
    filepath = root / "analysis" / "trackers" / "topic_evolution.md"
    if not filepath.exists():
        _log("No topic evolution tracker file found, skipping", verbose)
        return stats

    content = filepath.read_text(encoding="utf-8")
    parsed = parse_topic_signals(content)
    _log(f"Parsed {len(parsed)} topic signal entries", verbose)

    for entry in parsed:
        try:
            topic = entry.get("topic")
            entry_date = entry.get("date")

            # Match by topic + date composite unique
            query = select(TopicSignal).where(
                TopicSignal.topic == topic,
            )
            if entry_date:
                query = query.where(TopicSignal.date == entry_date)
            else:
                query = query.where(TopicSignal.date.is_(None))

            result = await session.execute(query)
            existing = result.scalar_one_or_none()

            if existing:
                if existing.is_manual:
                    stats["skipped"] += 1
                    continue
                # Update existing record
                for key, val in entry.items():
                    if hasattr(existing, key):
                        setattr(existing, key, val)
                stats["updated"] += 1
                _log(f"  Updated: {topic} ({entry_date})", verbose)
            else:
                signal = TopicSignal(**entry, is_manual=False)
                session.add(signal)
                stats["inserted"] += 1
                _log(f"  Inserted: {topic} ({entry_date})", verbose)

        except Exception as e:
            _log(f"  Error importing topic signal: {e}", verbose)
            stats["errors"] += 1

    await session.commit()
    return stats


async def import_influence_signals(
    session: AsyncSession, root: Path, verbose: bool = False,
) -> dict:
    """Import influence signals from analysis/trackers/influence_graph.md."""
    stats = {"inserted": 0, "deleted": 0, "errors": 0}
    filepath = root / "analysis" / "trackers" / "influence_graph.md"
    if not filepath.exists():
        _log("No influence graph tracker file found, skipping", verbose)
        return stats

    content = filepath.read_text(encoding="utf-8")
    parsed = parse_influence_signals(content)
    _log(f"Parsed {len(parsed)} influence signal entries", verbose)

    # Delete all non-manual records and re-insert from parsed data
    del_result = await session.execute(
        delete(InfluenceSignal).where(InfluenceSignal.is_manual == False)  # noqa: E712
    )
    stats["deleted"] = del_result.rowcount
    _log(f"  Cleared {stats['deleted']} non-manual influence signals", verbose)
    await session.flush()

    for entry in parsed:
        try:
            # Remove entry_kind from dict before creating model (not a column)
            entry_data = {k: v for k, v in entry.items() if k != "entry_kind"}
            signal = InfluenceSignal(**entry_data, is_manual=False)
            session.add(signal)
            stats["inserted"] += 1
        except Exception as e:
            _log(f"  Error importing influence signal: {e}", verbose)
            stats["errors"] += 1

    await session.commit()
    return stats


async def import_contradictions(
    session: AsyncSession, root: Path, verbose: bool = False,
) -> dict:
    """Import contradictions from analysis/trackers/contradictions.md."""
    stats = {"inserted": 0, "deleted": 0, "errors": 0}
    filepath = root / "analysis" / "trackers" / "contradictions.md"
    if not filepath.exists():
        _log("No contradictions tracker file found, skipping", verbose)
        return stats

    content = filepath.read_text(encoding="utf-8")
    parsed = parse_contradictions(content)
    _log(f"Parsed {len(parsed)} contradiction entries", verbose)

    # Delete all non-manual records and re-insert from parsed data
    del_result = await session.execute(
        delete(Contradiction).where(Contradiction.is_manual == False)  # noqa: E712
    )
    stats["deleted"] = del_result.rowcount
    _log(f"  Cleared {stats['deleted']} non-manual contradictions", verbose)
    await session.flush()

    for entry in parsed:
        try:
            contradiction = Contradiction(**entry, is_manual=False)
            session.add(contradiction)
            stats["inserted"] += 1
        except Exception as e:
            _log(f"  Error importing contradiction: {e}", verbose)
            stats["errors"] += 1

    await session.commit()
    return stats


async def import_meeting_scores(
    session: AsyncSession, root: Path, verbose: bool = False,
) -> dict:
    """Import meeting scores from analysis/trackers/meeting_scores.md."""
    stats = {"inserted": 0, "updated": 0, "skipped": 0, "errors": 0}
    filepath = root / "analysis" / "trackers" / "meeting_scores.md"
    if not filepath.exists():
        _log("No meeting scores tracker file found, skipping", verbose)
        return stats

    content = filepath.read_text(encoding="utf-8")
    parsed = parse_meeting_scores(content)
    _log(f"Parsed {len(parsed)} meeting score entries", verbose)

    # Build a transcript lookup: title -> id (case-insensitive)
    t_result = await session.execute(select(Transcript.id, Transcript.title))
    title_to_id: dict[str, int] = {}
    for row in t_result.all():
        if row.title:
            title_to_id[row.title.lower().strip()] = row.id

    for entry in parsed:
        try:
            meeting_title = entry.get("meeting_title")
            entry_date = entry.get("date")

            # Resolve transcript_id by matching meeting_title to transcript title
            transcript_id = None
            if meeting_title:
                transcript_id = title_to_id.get(meeting_title.lower().strip())
                # Fallback: fuzzy match by checking if transcript title contains
                # the meeting title or vice versa
                if not transcript_id:
                    mt_lower = meeting_title.lower().strip()
                    for t_title, t_id in title_to_id.items():
                        if mt_lower in t_title or t_title in mt_lower:
                            transcript_id = t_id
                            break

            if not transcript_id:
                _log(f"  No transcript match for: {meeting_title}, skipping", verbose)
                stats["skipped"] += 1
                continue

            # Match by transcript_id (unique constraint on transcript_id)
            result = await session.execute(
                select(MeetingScore).where(
                    MeetingScore.transcript_id == transcript_id,
                )
            )
            existing = result.scalar_one_or_none()

            if existing:
                if existing.is_manual:
                    stats["skipped"] += 1
                    continue
                # Update existing record
                for key, val in entry.items():
                    if hasattr(existing, key):
                        setattr(existing, key, val)
                existing.transcript_id = transcript_id
                stats["updated"] += 1
                _log(f"  Updated: {meeting_title} ({entry_date})", verbose)
            else:
                entry["transcript_id"] = transcript_id
                score = MeetingScore(**entry, is_manual=False)
                session.add(score)
                stats["inserted"] += 1
                _log(f"  Inserted: {meeting_title} ({entry_date})", verbose)

        except Exception as e:
            _log(f"  Error importing meeting score: {e}", verbose)
            stats["errors"] += 1

    await session.commit()
    return stats


async def import_risk_entries(
    session: AsyncSession, root: Path, verbose: bool = False,
) -> dict:
    """Import risk entries from analysis/trackers/risk_register.md."""
    stats = {"inserted": 0, "updated": 0, "skipped": 0, "errors": 0}
    filepath = root / "analysis" / "trackers" / "risk_register.md"
    if not filepath.exists():
        _log("No risk register file found, skipping", verbose)
        return stats

    content = filepath.read_text(encoding="utf-8")
    parsed = parse_risk_entries(content)
    _log(f"Parsed {len(parsed)} risk entries", verbose)

    for entry in parsed:
        try:
            risk_id = entry.get("risk_id")
            if not risk_id:
                stats["errors"] += 1
                continue

            # Match by risk_id (unique)
            result = await session.execute(
                select(RiskEntry).where(RiskEntry.risk_id == risk_id)
            )
            existing = result.scalar_one_or_none()

            if existing:
                if existing.is_manual:
                    stats["skipped"] += 1
                    continue
                # Update existing record
                for key, val in entry.items():
                    if hasattr(existing, key):
                        setattr(existing, key, val)
                stats["updated"] += 1
                _log(f"  Updated: {risk_id} - {entry.get('title', '')}", verbose)
            else:
                risk = RiskEntry(**entry, is_manual=False)
                session.add(risk)
                stats["inserted"] += 1
                _log(f"  Inserted: {risk_id} - {entry.get('title', '')}", verbose)

        except Exception as e:
            _log(f"  Error importing risk entry: {e}", verbose)
            stats["errors"] += 1

    await session.commit()
    return stats


async def import_project_summaries(
    session: AsyncSession, root: Path, verbose: bool = False,
) -> dict:
    """Import project summaries from analysis/projects/*/."""
    stats = {"inserted": 0, "updated": 0, "skipped": 0, "errors": 0}

    parsed = parse_project_summaries(str(root))
    if not parsed:
        _log("No project summaries found, skipping", verbose)
        return stats

    _log(f"Parsed {len(parsed)} project summary entries", verbose)

    # Build project slug -> id mapping
    p_result = await session.execute(select(Project.id, Project.slug, Project.name))
    slug_to_id: dict[str, int] = {}
    name_to_id: dict[str, int] = {}
    for row in p_result.all():
        if row.slug:
            slug_to_id[row.slug.lower()] = row.id
        if row.name:
            name_to_id[row.name.lower()] = row.id
            # Also index by generated slug from name
            slug_to_id[_slugify(row.name)] = row.id

    # Build transcript title -> id mapping for resolving transcript_id
    t_result = await session.execute(select(Transcript.id, Transcript.title, Transcript.filename))
    transcript_lookup: dict[str, int] = {}
    for row in t_result.all():
        if row.title:
            transcript_lookup[row.title.lower().strip()] = row.id
        if row.filename:
            transcript_lookup[row.filename.lower().strip()] = row.id

    for entry in parsed:
        try:
            project_slug = entry.get("project_slug", "")
            source_file = entry.get("source_file", "")
            file_hash = entry.get("file_hash")

            # Resolve project_slug -> project_id
            project_id = slug_to_id.get(project_slug.lower())
            if not project_id:
                # Try matching by generated slug from name
                project_id = slug_to_id.get(project_slug.lower().replace("_", "-"))
            if not project_id:
                _log(f"  No project match for slug: {project_slug}, skipping", verbose)
                stats["skipped"] += 1
                continue

            # Try to resolve transcript_id from the source file stem
            transcript_id = None
            stem = Path(source_file).stem if source_file else ""
            if stem:
                # Try direct match
                transcript_id = transcript_lookup.get(stem.lower())
                # Try fuzzy: strip date prefix and match
                if not transcript_id:
                    for t_key, t_id in transcript_lookup.items():
                        if stem.lower() in t_key or t_key in stem.lower():
                            transcript_id = t_id
                            break

            # Match by project_id + source_file
            result = await session.execute(
                select(ProjectSummary).where(
                    ProjectSummary.project_id == project_id,
                    ProjectSummary.source_file == source_file,
                )
            )
            existing = result.scalar_one_or_none()

            if existing:
                if existing.file_hash == file_hash:
                    stats["skipped"] += 1
                    continue
                existing.content = entry.get("content", "")
                existing.date = entry.get("date")
                existing.relevance = entry.get("relevance")
                existing.file_hash = file_hash
                if transcript_id:
                    existing.transcript_id = transcript_id
                stats["updated"] += 1
                _log(f"  Updated: {source_file}", verbose)
            else:
                # transcript_id is required (non-nullable) — skip if not found
                if not transcript_id:
                    _log(f"  No transcript match for project summary: {source_file}, skipping", verbose)
                    stats["skipped"] += 1
                    continue

                summary = ProjectSummary(
                    project_id=project_id,
                    transcript_id=transcript_id,
                    date=entry.get("date"),
                    relevance=entry.get("relevance"),
                    content=entry.get("content", ""),
                    source_file=source_file,
                    file_hash=file_hash,
                )
                session.add(summary)
                stats["inserted"] += 1
                _log(f"  Inserted: {source_file}", verbose)

        except Exception as e:
            _log(f"  Error importing project summary: {e}", verbose)
            stats["errors"] += 1

    await session.commit()
    return stats


# ---------------------------------------------------------------------------
# Main orchestrator
# ---------------------------------------------------------------------------


async def import_all(data_root: str, db_url: str, verbose: bool = False):
    """Run the full import pipeline."""
    root = Path(data_root)
    if not root.exists():
        print(f"ERROR: Data root directory not found: {data_root}")
        sys.exit(1)

    print(f"Icarus Data Import")
    print(f"  Data root: {root.resolve()}")
    print(f"  Database:  {db_url.split('@')[-1] if '@' in db_url else db_url}")
    print()

    engine = create_async_engine(db_url, echo=False)
    Session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    all_stats = {}

    total_steps = 19

    async with Session() as session:
        # 1. Transcripts
        print(f"[1/{total_steps}] Importing transcripts...")
        all_stats["transcripts"] = await import_transcripts(session, root, verbose)

        # 2. Stakeholders
        print(f"[2/{total_steps}] Importing stakeholders...")
        all_stats["stakeholders"] = await import_stakeholders(session, root, verbose)

        # 3. Decisions
        print(f"[3/{total_steps}] Importing decisions...")
        all_stats["decisions"] = await import_decisions(session, root, verbose)

        # 4. Workstreams + milestones
        print(f"[4/{total_steps}] Importing workstreams...")
        all_stats["workstreams"] = await import_workstreams(session, root, verbose)

        # 5. Open threads
        print(f"[5/{total_steps}] Importing open threads...")
        all_stats["open_threads"] = await import_open_threads(session, root, verbose)

        # 6. Action items
        print(f"[6/{total_steps}] Importing action items...")
        all_stats["action_items"] = await import_action_items(session, root, verbose)

        # 7. Glossary
        print(f"[7/{total_steps}] Importing glossary...")
        all_stats["glossary"] = await import_glossary(session, root, verbose)

        # 8. Summaries
        print(f"[8/{total_steps}] Importing summaries...")
        all_stats["summaries"] = await import_summaries(session, root, verbose)

        # 9. Weekly reports
        print(f"[9/{total_steps}] Importing weekly reports...")
        all_stats["weekly_reports"] = await import_weekly_reports(session, root, verbose)

        # 10. Programme debrief (as Document)
        print(f"[10/{total_steps}] Importing programme debrief...")
        all_stats["programme_debrief"] = await import_programme_debrief(session, root, verbose)

        # 11. Project pages (as Documents)
        print(f"[11/{total_steps}] Importing project pages...")
        all_stats["project_pages"] = await import_project_pages(session, root, verbose)

        # 12. Sentiments
        print(f"[12/{total_steps}] Importing sentiments...")
        all_stats["sentiments"] = await import_sentiments(session, root, verbose)

        # 13. Commitments
        print(f"[13/{total_steps}] Importing commitments...")
        all_stats["commitments"] = await import_commitments(session, root, verbose)

        # 14. Topic signals
        print(f"[14/{total_steps}] Importing topic signals...")
        all_stats["topic_signals"] = await import_topic_signals(session, root, verbose)

        # 15. Influence signals
        print(f"[15/{total_steps}] Importing influence signals...")
        all_stats["influence_signals"] = await import_influence_signals(session, root, verbose)

        # 16. Contradictions
        print(f"[16/{total_steps}] Importing contradictions...")
        all_stats["contradictions"] = await import_contradictions(session, root, verbose)

        # 17. Meeting scores
        print(f"[17/{total_steps}] Importing meeting scores...")
        all_stats["meeting_scores"] = await import_meeting_scores(session, root, verbose)

        # 18. Risk entries
        print(f"[18/{total_steps}] Importing risk entries...")
        all_stats["risk_entries"] = await import_risk_entries(session, root, verbose)

        # 19. Project summaries
        print(f"[19/{total_steps}] Importing project summaries...")
        all_stats["project_summaries"] = await import_project_summaries(session, root, verbose)

        # Generate slugs for projects that are missing them
        print("\nGenerating project slugs...")
        p_result = await session.execute(
            select(Project).where(Project.slug.is_(None))
        )
        projects_without_slugs = p_result.scalars().all()
        slug_count = 0
        for project in projects_without_slugs:
            project.slug = _slugify(project.name)
            slug_count += 1
        if slug_count:
            await session.commit()
            _log(f"Generated slugs for {slug_count} projects", verbose)

        # Build transcript mentions
        print("\nBuilding transcript mentions...")
        all_stats["mentions"] = await build_transcript_mentions(session, verbose)

    await engine.dispose()

    # Print summary
    print("\n" + "=" * 60)
    print("IMPORT SUMMARY")
    print("=" * 60)

    for entity, stats in all_stats.items():
        if entity == "mentions":
            print(f"  Transcript mentions: {stats['speaker']} speakers, "
                  f"{stats['mentioned']} mentioned, {stats['cleared']} cleared")
        elif entity == "workstreams":
            ws = stats["workstreams"]
            ms = stats["milestones"]
            print(f"  Workstreams: {ws['inserted']} inserted, {ws['updated']} updated, "
                  f"{ws['skipped']} skipped, {ws['errors']} errors")
            print(f"  Milestones:  {ms['inserted']} inserted, {ms['errors']} errors")
        elif "deleted" in stats:
            # Bulk-replace style: influence_signals, contradictions
            label = entity.replace("_", " ").title()
            deleted = stats.get("deleted", 0)
            inserted = stats.get("inserted", 0)
            errors = stats.get("errors", 0)
            print(f"  {label}: {deleted} cleared, {inserted} inserted, "
                  f"{errors} errors")
        else:
            label = entity.replace("_", " ").title()
            inserted = stats.get("inserted", 0)
            updated = stats.get("updated", 0)
            skipped = stats.get("skipped", 0)
            errors = stats.get("errors", 0)
            print(f"  {label}: {inserted} inserted, {updated} updated, "
                  f"{skipped} skipped, {errors} errors")

    print("=" * 60)

    # Check for any errors
    total_errors = 0
    for entity, entity_stats in all_stats.items():
        if entity == "workstreams":
            total_errors += entity_stats["workstreams"].get("errors", 0)
            total_errors += entity_stats["milestones"].get("errors", 0)
        elif entity != "mentions":
            total_errors += entity_stats.get("errors", 0)

    if total_errors > 0:
        print(f"\nWARNING: {total_errors} error(s) occurred during import.")
    else:
        print("\nImport completed successfully.")


def main():
    parser = argparse.ArgumentParser(
        description="Import Icarus data files into PostgreSQL"
    )
    parser.add_argument(
        "--data-root",
        required=True,
        help="Path to the Icarus data root directory",
    )
    parser.add_argument(
        "--db-url",
        default=None,
        help="Database URL (default: from DATABASE_URL env or local fallback)",
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Print detailed progress for each record",
    )
    args = parser.parse_args()

    db_url = (
        args.db_url
        or os.environ.get("DATABASE_URL")
        or "postgresql+asyncpg://icarus:icarus_local@localhost:5432/icarus"
    )

    asyncio.run(import_all(args.data_root, db_url, args.verbose))


if __name__ == "__main__":
    main()
