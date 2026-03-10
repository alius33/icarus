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
    Decision,
    DeletedImport,
    Document,
    GlossaryEntry,
    OpenThread,
    Stakeholder,
    Summary,
    Transcript,
    TranscriptMention,
    WeeklyReport,
    Workstream,
    WorkstreamMilestone,
)
from scripts.parsers.action_item_parser import parse_action_items
from scripts.parsers.decision_parser import parse_decisions
from scripts.parsers.glossary_parser import parse_glossary
from scripts.parsers.open_thread_parser import parse_open_threads
from scripts.parsers.stakeholder_parser import parse_stakeholders
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
                # Use number + status as unique key
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
                            DeletedImport.entity_type == "action_item",
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

    async with Session() as session:
        # 1. Transcripts
        print("[1/11] Importing transcripts...")
        all_stats["transcripts"] = await import_transcripts(session, root, verbose)

        # 2. Stakeholders
        print("[2/11] Importing stakeholders...")
        all_stats["stakeholders"] = await import_stakeholders(session, root, verbose)

        # 3. Decisions
        print("[3/11] Importing decisions...")
        all_stats["decisions"] = await import_decisions(session, root, verbose)

        # 4. Workstreams + milestones
        print("[4/11] Importing workstreams...")
        all_stats["workstreams"] = await import_workstreams(session, root, verbose)

        # 5. Open threads
        print("[5/11] Importing open threads...")
        all_stats["open_threads"] = await import_open_threads(session, root, verbose)

        # 6. Action items
        print("[6/11] Importing action items...")
        all_stats["action_items"] = await import_action_items(session, root, verbose)

        # 7. Glossary
        print("[7/11] Importing glossary...")
        all_stats["glossary"] = await import_glossary(session, root, verbose)

        # 8. Summaries
        print("[8/11] Importing summaries...")
        all_stats["summaries"] = await import_summaries(session, root, verbose)

        # 9. Weekly reports
        print("[9/11] Importing weekly reports...")
        all_stats["weekly_reports"] = await import_weekly_reports(session, root, verbose)

        # 10. Programme debrief (as Document)
        print("[10/11] Importing programme debrief...")
        all_stats["programme_debrief"] = await import_programme_debrief(session, root, verbose)

        # 11. Project pages (as Documents)
        print("[11/11] Importing project pages...")
        all_stats["project_pages"] = await import_project_pages(session, root, verbose)

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
    for entity, stats in all_stats.items():
        if entity == "workstreams":
            total_errors += stats["workstreams"].get("errors", 0)
            total_errors += stats["milestones"].get("errors", 0)
        elif entity != "mentions":
            total_errors += stats.get("errors", 0)

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
