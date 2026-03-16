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
import json
import os
import re
import sys
import traceback
from datetime import date, datetime, timezone


def _utcnow() -> datetime:
    """Naive UTC now — compatible with TIMESTAMP WITHOUT TIME ZONE columns."""
    return _utcnow().replace(tzinfo=None)
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
    DeliverableProgressSnapshot,
    DivisionProfile,
    Document,
    Document,
    GlossaryEntry,
    InfluenceSignal,
    MeetingScore,
    OpenThread,
    Outreach,
    ProgrammeWin,
    Project,
    ProjectLink,
    ProjectSummary,
    RiskEntry,
    SentimentSignal,
    Stakeholder,
    Summary,
    Task,
    TopicSignal,
    Transcript,
    TranscriptMention,
    WeeklyPlan,
    WeeklyPlanAction,
    WeeklyReport,
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
# Project seeding — ensures all expected projects exist in the DB
# ---------------------------------------------------------------------------

# All projects in a single flat list.  Each entry carries enough data to
# create a new project *or* update an existing one.  The ``code`` is set to
# ``PR{id}`` after the row is flushed (so the DB-assigned id is known).
ALL_PROJECTS = [
    {
        "name": "CLARA (IRP Adoption Tracker)",
        "slug": "clara",
        "description": "IRP adoption tracking tool",
        "is_custom": False,
        "status": "active",
        "color": None,
        "keywords": "clara,irp,adoption,tracker,csm",
    },
    {
        "name": "Friday (CS AI Agent)",
        "alt_names": ["Friday (Project Management App)"],
        "slug": "friday",
        "description": "CS AI agent / project management",
        "is_custom": False,
        "status": "active",
        "color": None,
        "keywords": "friday,ai agent,project management",
    },
    {
        "name": "Build in Five",
        "alt_names": ["Build in Five (Cursor for Pipeline Sales)"],
        "slug": "build-in-five",
        "description": "Rapid prototyping for pipeline sales",
        "is_custom": False,
        "status": "active",
        "color": None,
        "keywords": "build in five,cursor,pipeline,martin",
    },
    {
        "name": "Training & Enablement",
        "slug": "training-enablement",
        "description": "Training and enablement programme",
        "is_custom": False,
        "status": "active",
        "color": None,
        "keywords": "training,enablement,onboarding",
    },
    {
        "name": "Navigator L1 Automation",
        "alt_names": ["IRP Navigator L1 Automation"],
        "slug": "navigator-l1",
        "description": "Navigator L1 automation",
        "is_custom": False,
        "status": "active",
        "color": None,
        "keywords": "navigator,l1,automation",
    },
    {
        "name": "Customer Success Agent",
        "slug": "cs-agent",
        "description": "Customer success agent project",
        "is_custom": False,
        "status": "active",
        "color": None,
        "keywords": "customer success agent,cs agent",
    },
    {
        "name": "Cross OU Collaboration",
        "slug": "cross-ou",
        "description": "Cross-OU banking, AM, life insurance",
        "is_custom": True,
        "status": "active",
        "color": "#10B981",
        "keywords": "cross ou,banking,asset management,life insurance,idrees",
    },
    {
        "name": "Program Management",
        "slug": "programme-mgmt",
        "description": "Governance, steering, portfolio reviews",
        "is_custom": True,
        "status": "active",
        "color": "#6366F1",
        "keywords": "governance,steering,portfolio review,programme",
    },
    {
        "name": "TSR Enhancements",
        "slug": "tsr-enhancements",
        "description": "TSR automation track",
        "is_custom": True,
        "status": "active",
        "color": "#F59E0B",
        "keywords": "tsr,technical service request,cat bond",
    },
    {
        "name": "App Factory",
        "slug": "app-factory",
        "description": "Automated deployment platform for AI apps",
        "is_custom": True,
        "status": "active",
        "color": "#8B5CF6",
        "keywords": "app factory,phantom agent,advisoryappfactory,moplit",
    },
    {
        "name": "Slidey (AI Presentations)",
        "slug": "slidey",
        "description": "AI-powered collaborative presentation platform with markdown content layer, RBAC, and agentic extensions",
        "is_custom": True,
        "status": "active",
        "color": "#EC4899",
        "keywords": "slidey,presentations,slides,ai presentations,deck,storyboard,content layer,narrative",
    },
]


async def seed_projects(session: AsyncSession, verbose: bool) -> dict:
    """Ensure all projects exist in the database.

    Iterates over ALL_PROJECTS and matches by name.  If the project already
    exists its code and slug are backfilled when empty.  New projects are
    created with all fields.  The code is always ``PR{id}``.
    """
    stats = {"created": 0, "existing": 0, "updated": 0}

    for proj_data in ALL_PROJECTS:
        result = await session.execute(
            select(Project).where(Project.name == proj_data["name"])
        )
        existing = result.scalar_one_or_none()

        # Check alternative names if not found by primary name
        if not existing:
            for alt in proj_data.get("alt_names", []):
                result = await session.execute(
                    select(Project).where(Project.name == alt)
                )
                existing = result.scalar_one_or_none()
                if existing:
                    existing.name = proj_data["name"]
                    _log(f"  Renamed project '{alt}' -> '{proj_data['name']}'", verbose)
                    break

        if existing:
            stats["existing"] += 1
            changed = False

            # Backfill code if missing or empty
            expected_code = f"PR{existing.id}"
            if not existing.code or existing.code != expected_code:
                existing.code = expected_code
                changed = True

            # Backfill slug if missing
            if not existing.slug and proj_data.get("slug"):
                existing.slug = proj_data["slug"]
                changed = True

            # Backfill keywords if missing
            if not existing.keywords and proj_data.get("keywords"):
                existing.keywords = proj_data["keywords"]
                changed = True

            # Backfill description if missing
            if not existing.description and proj_data.get("description"):
                existing.description = proj_data["description"]
                changed = True

            if changed:
                stats["updated"] += 1
                _log(f"  Updated project '{existing.name}' (id={existing.id}, code={existing.code})", verbose)
            else:
                _log(f"  Project '{existing.name}' already exists (id={existing.id})", verbose)
        else:
            project = Project(
                name=proj_data["name"],
                slug=proj_data.get("slug"),
                description=proj_data.get("description"),
                is_custom=proj_data.get("is_custom", False),
                status=proj_data.get("status", "active"),
                color=proj_data.get("color"),
                keywords=proj_data.get("keywords"),
            )
            session.add(project)
            await session.flush()
            # Set code based on DB-assigned id
            project.code = f"PR{project.id}"
            stats["created"] += 1
            _log(f"  Created project '{project.name}' (id={project.id}, code={project.code})", verbose)

    await session.commit()
    return stats


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
                existing.updated_at = _utcnow()
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


async def _merge_stakeholder_duplicates(session: AsyncSession, verbose: bool):
    """One-time cleanup: merge stakeholder records that are duplicates due to name corrections.

    When a name is corrected in the markdown (e.g. 'Ben Brooks' -> 'Ben Brookes'),
    the import creates a new record instead of updating the old one. This function
    merges the old record's transcript_mentions into the new one and deletes the old.
    """
    # Map of old_name -> correct_name (the correct one should exist in the DB)
    NAME_CORRECTIONS = {
        "Ben Brooks": "Ben Brookes",
        "Natalia (Plant)": "Natalia Plant",
    }

    for old_name, correct_name in NAME_CORRECTIONS.items():
        old_result = await session.execute(
            select(Stakeholder).where(Stakeholder.name == old_name)
        )
        old_sh = old_result.scalar_one_or_none()
        if not old_sh:
            continue  # Already cleaned up

        new_result = await session.execute(
            select(Stakeholder).where(Stakeholder.name == correct_name)
        )
        new_sh = new_result.scalar_one_or_none()
        if not new_sh:
            # Correct name doesn't exist yet — just rename the old record
            old_sh.name = correct_name
            _log(f"  Renamed stakeholder '{old_name}' -> '{correct_name}'", verbose)
            continue

        # Both exist — merge mentions from old into new, then delete old.
        # First delete mentions that would conflict (same transcript+mention_type
        # already exists on the new stakeholder), then move the rest.
        await session.execute(
            text("""
                DELETE FROM transcript_mentions old_m
                WHERE old_m.stakeholder_id = :old_id
                  AND EXISTS (
                    SELECT 1 FROM transcript_mentions new_m
                    WHERE new_m.stakeholder_id = :new_id
                      AND new_m.transcript_id = old_m.transcript_id
                      AND new_m.mention_type = old_m.mention_type
                  )
            """),
            {"new_id": new_sh.id, "old_id": old_sh.id},
        )
        await session.execute(
            text("UPDATE transcript_mentions SET stakeholder_id = :new_id WHERE stakeholder_id = :old_id"),
            {"new_id": new_sh.id, "old_id": old_sh.id},
        )
        await session.execute(
            text("DELETE FROM stakeholders WHERE id = :old_id"),
            {"old_id": old_sh.id},
        )
        _log(f"  Merged stakeholder '{old_name}' (id={old_sh.id}) into '{correct_name}' (id={new_sh.id})", verbose)

    await session.commit()


async def import_stakeholders(
    session: AsyncSession, data_root: Path, verbose: bool
) -> dict:
    """Import stakeholders from context/stakeholders.md."""
    stats = {"inserted": 0, "updated": 0, "skipped": 0, "errors": 0}
    filepath = data_root / "context" / "stakeholders.md"

    if not filepath.exists():
        _log("stakeholders.md not found, skipping.", verbose)
        return stats

    # Clean up any duplicate stakeholders from prior name corrections
    await _merge_stakeholder_duplicates(session, verbose)

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
                    existing.updated_at = _utcnow()
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
                    existing.updated_at = _utcnow()
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
                    existing.updated_at = _utcnow()
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
                    existing.updated_at = _utcnow()
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
                    existing.updated_at = _utcnow()
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


def _parse_project_fields(content: str) -> tuple[str | None, list[str]]:
    """Extract Primary project and Secondary projects from summary markdown header.

    Returns (primary_project_name, [secondary_project_names]).
    """
    primary = None
    secondary: list[str] = []

    for line in content.splitlines()[:20]:
        m = re.match(r"\*\*Primary project:\*\*\s*(.+)", line)
        if m:
            val = m.group(1).strip()
            if val and val.lower() not in ("none", "n/a", "—", "-"):
                primary = val

        m = re.match(r"\*\*Secondary projects?:\*\*\s*(.+)", line)
        if m:
            raw = m.group(1).strip()
            if raw and raw.lower() not in ("none", "n/a", "—", "-"):
                parts = re.split(r",\s*", raw)
                secondary = [p.strip() for p in parts if p.strip()]

    return primary, secondary


def _extract_key_points(content: str) -> str:
    """Extract the Key Points section from a summary as markdown bullets for ProjectSummary."""
    m = re.search(r"^## Key Points\s*$", content, re.MULTILINE)
    if not m:
        return ""
    start = m.end()
    next_heading = re.search(r"^## ", content[start:], re.MULTILINE)
    section = content[start:start + next_heading.start()] if next_heading else content[start:]
    # Preserve original markdown bullet format
    bullets = [line for line in section.strip().splitlines() if line.strip().startswith("- ")]
    return "\n".join(bullets[:5])


async def import_summaries(
    session: AsyncSession, data_root: Path, verbose: bool
) -> dict:
    """Import summary files from analysis/summaries/*.md.

    Also parses **Primary project:** and **Secondary projects:** fields from
    each summary to:
      1. Set primary_project_id on the linked transcript
      2. Create ProjectLink entries (transcript ↔ project)
      3. Create ProjectSummary entries (project-specific content from Key Points)
    """
    stats = {"inserted": 0, "updated": 0, "skipped": 0, "errors": 0,
             "project_links": 0, "project_summaries": 0, "project_ids_set": 0}
    summaries_dir = data_root / "analysis" / "summaries"

    if not summaries_dir.exists():
        _log("analysis/summaries directory not found, skipping.", verbose)
        return stats

    md_files = sorted(summaries_dir.glob("*.md"))
    if not md_files:
        _log("No summary files found.", verbose)
        return stats

    _log(f"Found {len(md_files)} summary files.", verbose)

    # Build project name -> id mapping with fuzzy matching support
    p_result = await session.execute(select(Project.id, Project.name))
    _project_rows = p_result.all()
    project_name_to_id: dict[str, int] = {}
    _project_full_names: list[tuple[str, int]] = []  # (lowercase name, id)
    for row in _project_rows:
        if row.name:
            lowered = row.name.lower().strip()
            project_name_to_id[lowered] = row.id
            _project_full_names.append((lowered, row.id))
            # Also index by short name (before parenthetical)
            short = re.sub(r'\s*\(.*?\)\s*$', '', lowered).strip()
            if short and short != lowered:
                project_name_to_id[short] = row.id

    def _resolve_project_name(name: str) -> int | None:
        """Resolve a project name to an ID with fuzzy matching."""
        norm = name.lower().strip()
        # Remove parenthetical qualifiers from summary names
        norm_clean = re.sub(r'\s*\(.*?\)\s*$', '', norm).strip()
        # Remove common noise like "tangential —" qualifiers
        norm_clean = re.split(r'\s*[-–—]\s*', norm_clean)[0].strip()
        # Exact match
        if norm_clean in project_name_to_id:
            return project_name_to_id[norm_clean]
        # Check if summary name is a prefix of any DB project name
        for full_name, pid in _project_full_names:
            if full_name.startswith(norm_clean):
                return pid
        return None

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
            summary_date = None
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
                    # Even if summary unchanged, still ensure project attribution
                    # is set (handles cases where summary existed before this feature)
                    if transcript_id:
                        await _ensure_project_attribution(
                            session, content, transcript_id, summary_date,
                            source_file, _resolve_project_name, stats, verbose,
                        )
                    continue
                existing.content = content
                existing.file_hash = file_hash
                existing.source_file = source_file
                existing.transcript_id = transcript_id
                existing.updated_at = _utcnow()
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

            # Set project attribution from summary content
            if transcript_id:
                await _ensure_project_attribution(
                    session, content, transcript_id, summary_date,
                    source_file, _resolve_project_name, stats, verbose,
                )

        except Exception as e:
            stats["errors"] += 1
            _log(f"  ERROR importing summary {filepath.name}: {e}", verbose)

    await session.commit()
    return stats


async def _ensure_project_attribution(
    session: AsyncSession,
    summary_content: str,
    transcript_id: int,
    summary_date,
    source_file: str,
    resolve_project,
    stats: dict,
    verbose: bool,
) -> None:
    """Parse project fields from summary and create project attribution records.

    Sets primary_project_id on transcript, creates ProjectLink and ProjectSummary entries.
    resolve_project is a callable(name: str) -> int | None for fuzzy project name matching.
    """
    primary_name, secondary_names = _parse_project_fields(summary_content)
    if not primary_name and not secondary_names:
        return

    # Resolve primary project
    primary_project_id = None
    if primary_name:
        primary_project_id = resolve_project(primary_name)
        if not primary_project_id:
            _log(f"    No project match for primary: '{primary_name}'", verbose)

    # Resolve secondary project IDs
    secondary_project_ids: list[int] = []
    for sec_name in secondary_names:
        sec_id = resolve_project(sec_name)
        if sec_id:
            secondary_project_ids.append(sec_id)
        else:
            _log(f"    No project match for secondary: '{sec_name}'", verbose)

    # Set project IDs on transcript (only if not already set)
    t_result = await session.execute(
        select(Transcript).where(Transcript.id == transcript_id)
    )
    transcript = t_result.scalar_one_or_none()
    if transcript:
        if primary_project_id and not transcript.primary_project_id:
            transcript.primary_project_id = primary_project_id
            stats["project_ids_set"] += 1
            _log(f"    Set primary_project_id={primary_project_id} on transcript {transcript_id}", verbose)
        if len(secondary_project_ids) >= 1 and not transcript.secondary_project_id:
            transcript.secondary_project_id = secondary_project_ids[0]
            _log(f"    Set secondary_project_id={secondary_project_ids[0]} on transcript {transcript_id}", verbose)
        if len(secondary_project_ids) >= 2 and not transcript.tertiary_project_id:
            transcript.tertiary_project_id = secondary_project_ids[1]
            _log(f"    Set tertiary_project_id={secondary_project_ids[1]} on transcript {transcript_id}", verbose)

    # Collect all project IDs (primary + secondary)
    all_project_ids: list[int] = []
    if primary_project_id:
        all_project_ids.append(primary_project_id)
    all_project_ids.extend(secondary_project_ids)

    key_points = _extract_key_points(summary_content)

    for project_id in all_project_ids:
        # Create ProjectLink if not exists
        existing_link = await session.execute(
            select(ProjectLink).where(
                ProjectLink.project_id == project_id,
                ProjectLink.entity_type == "transcript",
                ProjectLink.entity_id == transcript_id,
            )
        )
        if not existing_link.scalar_one_or_none():
            session.add(ProjectLink(
                project_id=project_id,
                entity_type="transcript",
                entity_id=transcript_id,
            ))
            stats["project_links"] += 1
            _log(f"    Created ProjectLink: project {project_id} ↔ transcript {transcript_id}", verbose)

        # Create ProjectSummary if not exists (only if we have key points)
        if key_points:
            existing_ps = await session.execute(
                select(ProjectSummary).where(
                    ProjectSummary.project_id == project_id,
                    ProjectSummary.transcript_id == transcript_id,
                )
            )
            if not existing_ps.scalar_one_or_none():
                relevance = "HIGH" if project_id == primary_project_id else "MEDIUM"
                session.add(ProjectSummary(
                    project_id=project_id,
                    transcript_id=transcript_id,
                    date=summary_date,
                    relevance=relevance,
                    content=key_points,
                    source_file=source_file,
                ))
                stats["project_summaries"] += 1
                _log(f"    Created ProjectSummary: project {project_id} ← transcript {transcript_id}", verbose)


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
                existing.updated_at = _utcnow()
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
                existing.updated_at = _utcnow()
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
                existing.updated_at = _utcnow()
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
# Project link builder — connects entities to projects
# ---------------------------------------------------------------------------

# Keywords that map entity text to projects.  Each tuple is
# (keyword_or_phrase, project_name_prefix) where the prefix is matched
# against the lowercased project name stored in the DB.
_PROJECT_KEYWORDS: list[tuple[str, str]] = [
    ("clara", "clara"),
    ("irp", "clara"),
    ("adoption tracker", "clara"),
    ("dashboard", "clara"),
    ("friday", "friday"),
    ("build in five", "build in five"),
    ("cursor for pipeline", "build in five"),
    ("martin", "build in five"),
    ("training", "training"),
    ("enablement", "training"),
    ("navigator", "navigator"),
    ("l1 automation", "navigator"),
    ("customer success agent", "customer success agent"),
    ("cs agent", "customer success agent"),
    ("cross ou", "cross ou"),
    ("banking", "cross ou"),
    ("asset management", "cross ou"),
    ("life insurance", "cross ou"),
    ("programme management", "program management"),
    ("program management", "program management"),
    ("governance", "program management"),
    ("steering", "program management"),
    ("tsr", "tsr"),
    ("app factory", "app factory"),
    ("phantom agent", "app factory"),
    ("advisoryappfactory", "app factory"),
    ("moplit", "app factory"),
]


async def build_project_links(session: AsyncSession, verbose: bool) -> dict:
    """Create ProjectLink entries for transcripts, summaries, decisions, tasks,
    and open threads.

    Strategies:
      1. Transcripts: keyword match on title → set primary_project_id + ProjectLink
         + create ProjectSummary entries from linked Summary content.
      2. Tasks: match context field (transcript filename) → transcript →
         primary_project_id.  Also sets task.project_id directly.
      3. Decisions & threads: keyword match on title/description text.
    """
    stats = {
        "transcript_links": 0, "transcript_project_ids": 0,
        "project_summaries": 0,
        "task_links": 0, "decision_links": 0, "thread_links": 0,
        "task_project_ids": 0,
    }

    # Load project name → id mapping
    p_result = await session.execute(select(Project.id, Project.name))
    project_rows = p_result.all()
    name_to_id: dict[str, int] = {}
    for row in project_rows:
        if row.name:
            name_to_id[row.name.lower().strip()] = row.id
            short = re.sub(r'\s*\(.*?\)\s*$', '', row.name.lower().strip()).strip()
            if short:
                name_to_id[short] = row.id

    def _match_projects_by_keywords(text: str) -> set[int]:
        """Return project IDs that match keywords in the given text."""
        lowered = text.lower()
        matched: set[int] = set()
        for keyword, proj_prefix in _PROJECT_KEYWORDS:
            if keyword in lowered:
                for name, pid in name_to_id.items():
                    if name.startswith(proj_prefix):
                        matched.add(pid)
                        break
        return matched

    async def _ensure_link(project_id: int, entity_type: str, entity_id: int) -> bool:
        """Create a ProjectLink if it doesn't exist. Returns True if created."""
        existing = await session.execute(
            select(ProjectLink.id).where(
                ProjectLink.project_id == project_id,
                ProjectLink.entity_type == entity_type,
                ProjectLink.entity_id == entity_id,
            )
        )
        if existing.scalar_one_or_none():
            return False
        session.add(ProjectLink(
            project_id=project_id,
            entity_type=entity_type,
            entity_id=entity_id,
        ))
        return True

    # --- Transcripts: keyword match on title + summary content ---
    all_transcripts_result = await session.execute(
        select(Transcript.id, Transcript.title, Transcript.filename,
               Transcript.meeting_date, Transcript.primary_project_id)
    )
    all_transcripts = all_transcripts_result.all()

    # Pre-load summaries keyed by transcript_id
    summary_result = await session.execute(
        select(Summary.transcript_id, Summary.content, Summary.source_file, Summary.file_hash)
        .where(Summary.transcript_id.isnot(None))
    )
    summary_by_transcript: dict[int, tuple] = {}
    for row in summary_result.all():
        summary_by_transcript[row.transcript_id] = (row.content, row.source_file, row.file_hash)

    # Track transcript → project mappings for task linking later
    transcript_to_projects: dict[int, set[int]] = {}

    for t in all_transcripts:
        # Build search text from title + summary content
        search_text = t.title or ""
        summary_data = summary_by_transcript.get(t.id)
        if summary_data:
            # Also search first ~500 chars of summary for keywords
            search_text += " " + (summary_data[0] or "")[:500]

        project_ids = _match_projects_by_keywords(search_text)
        if not project_ids:
            # Fallback: try matching on filename
            fname = Path(t.filename).stem if t.filename else ""
            project_ids = _match_projects_by_keywords(fname.replace("_", " ").replace("-", " "))

        if not project_ids:
            continue

        transcript_to_projects[t.id] = project_ids

        # Set primary_project_id if not already set
        if not t.primary_project_id:
            primary_pid = next(iter(project_ids))
            await session.execute(
                Transcript.__table__.update()
                .where(Transcript.id == t.id)
                .values(primary_project_id=primary_pid)
            )
            stats["transcript_project_ids"] += 1

        # Create ProjectLinks for transcripts
        for pid in project_ids:
            if await _ensure_link(pid, "transcript", t.id):
                stats["transcript_links"] += 1

            # Create ProjectSummary entry if a summary exists
            if summary_data:
                content, source_file, file_hash = summary_data
                ps_check = await session.execute(
                    select(ProjectSummary.id).where(
                        ProjectSummary.project_id == pid,
                        ProjectSummary.transcript_id == t.id,
                    )
                )
                if not ps_check.scalar_one_or_none():
                    # Extract key points as summary content
                    key_points = _extract_key_points(content) if content else ""
                    if not key_points:
                        key_points = (content or "")[:300]
                    session.add(ProjectSummary(
                        project_id=pid,
                        transcript_id=t.id,
                        date=t.meeting_date,
                        relevance="MEDIUM",
                        content=key_points,
                        source_file=source_file,
                        file_hash=file_hash or "",
                    ))
                    stats["project_summaries"] += 1

    await session.flush()

    # --- Build stem → project lookup (now includes newly linked transcripts) ---
    stem_to_project: dict[str, int] = {}
    for t in all_transcripts:
        stem = Path(t.filename).stem.lower() if t.filename else ""
        if not stem:
            continue
        # Use primary_project_id or first matched project
        pid = t.primary_project_id
        if not pid and t.id in transcript_to_projects:
            pid = next(iter(transcript_to_projects[t.id]))
        if pid:
            stem_to_project[stem] = pid

    # --- Tasks: link via context (transcript filename) + keywords ---
    task_result = await session.execute(select(Task))
    tasks = task_result.scalars().all()
    for task in tasks:
        project_ids: set[int] = set()

        # Strategy 1: match context to transcript
        if task.context:
            ctx_stem = task.context.strip().lower()
            pid = stem_to_project.get(ctx_stem)
            if pid:
                project_ids.add(pid)

        # Strategy 2: keyword match on title/description
        search_text = f"{task.title or ''} {task.description or ''}"
        project_ids |= _match_projects_by_keywords(search_text)

        # Set project_id on the task itself (use first match)
        if project_ids and not task.project_id:
            task.project_id = next(iter(project_ids))
            stats["task_project_ids"] += 1

        for pid in project_ids:
            if await _ensure_link(pid, "task", task.id):
                stats["task_links"] += 1

    # --- Decisions: keyword match ---
    dec_result = await session.execute(select(Decision))
    decisions = dec_result.scalars().all()
    for dec in decisions:
        search_text = f"{dec.decision or ''} {dec.rationale or ''}"
        project_ids = _match_projects_by_keywords(search_text)
        for pid in project_ids:
            if await _ensure_link(pid, "decision", dec.id):
                stats["decision_links"] += 1

    # --- Open threads: keyword match ---
    thread_result = await session.execute(select(OpenThread))
    threads = thread_result.scalars().all()
    for thread in threads:
        search_text = f"{thread.title or ''} {thread.context or ''} {thread.question or ''}"
        project_ids = _match_projects_by_keywords(search_text)
        for pid in project_ids:
            if await _ensure_link(pid, "open_thread", thread.id):
                stats["thread_links"] += 1

    await session.commit()
    return stats


# ---------------------------------------------------------------------------
# Weekly plan seeding from JSON
# ---------------------------------------------------------------------------


async def seed_weekly_plans(session: AsyncSession, verbose: bool) -> dict:
    """Seed weekly plans from JSON files in scripts/seed_data/.

    Reads weekly_plans.json (single plan or list of plans) and creates
    any plans that don't already exist (matched by week_number).
    Idempotent: skips plans that already exist for a given week.
    """
    stats = {"inserted": 0, "updated": 0, "skipped": 0, "errors": 0}
    seed_file = Path(__file__).resolve().parent / "seed_data" / "weekly_plans.json"

    if not seed_file.exists():
        _log("No weekly_plans.json seed file found, skipping.", verbose)
        return stats

    try:
        with open(seed_file, "r") as f:
            data = json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        _log(f"Error reading weekly_plans.json: {e}", verbose)
        stats["errors"] += 1
        return stats

    # Support both single plan object and list of plans
    plans = data if isinstance(data, list) else [data]

    for plan_data in plans:
        week_num = plan_data.get("week_number")
        if not week_num:
            _log("Skipping plan with no week_number", verbose)
            stats["errors"] += 1
            continue

        # Check if plan for this week already exists
        existing = await session.execute(
            select(WeeklyPlan).where(WeeklyPlan.week_number == week_num)
        )
        existing_plan = existing.scalar_one_or_none()
        if existing_plan:
            # Update summary fields and actions if they differ
            try:
                updated = False
                for field in ("deliverable_progress_summary", "programme_actions_summary", "status"):
                    new_val = plan_data.get(field)
                    if new_val and getattr(existing_plan, field, None) != new_val:
                        setattr(existing_plan, field, new_val)
                        updated = True

                # Update existing actions (match by title within plan)
                actions_data = plan_data.get("actions", [])
                if actions_data:
                    existing_actions_result = await session.execute(
                        select(WeeklyPlanAction).where(
                            WeeklyPlanAction.weekly_plan_id == existing_plan.id
                        )
                    )
                    existing_actions = {
                        a.title: a for a in existing_actions_result.scalars().all()
                    }
                    action_fields = (
                        "description", "priority", "owner", "status",
                        "deliverable_id", "position", "is_ai_generated",
                        "carried_from_week", "source_transcript_id",
                        "source_update_id", "context",
                    )
                    for i, action_data in enumerate(actions_data):
                        title = action_data["title"]
                        if title in existing_actions:
                            # Update existing action fields
                            action = existing_actions[title]
                            for field in action_fields:
                                new_val = action_data.get(field)
                                if field == "position" and new_val is None:
                                    new_val = i
                                if new_val is not None and getattr(action, field) != new_val:
                                    setattr(action, field, new_val)
                                    updated = True
                        else:
                            # New action — insert it
                            action = WeeklyPlanAction(
                                weekly_plan_id=existing_plan.id,
                                category=action_data["category"],
                                title=title,
                                description=action_data.get("description"),
                                priority=action_data.get("priority", "MEDIUM"),
                                owner=action_data.get("owner"),
                                status=action_data.get("status", "PENDING"),
                                deliverable_id=action_data.get("deliverable_id"),
                                position=action_data.get("position", i),
                                is_ai_generated=action_data.get("is_ai_generated", True),
                                carried_from_week=action_data.get("carried_from_week"),
                                source_transcript_id=action_data.get("source_transcript_id"),
                                source_update_id=action_data.get("source_update_id"),
                                context=action_data.get("context"),
                            )
                            session.add(action)
                            updated = True

                if updated:
                    await session.commit()
                    _log(f"Weekly plan for week {week_num} updated (summary + actions).", verbose)
                    stats["updated"] += 1
                else:
                    _log(f"Weekly plan for week {week_num} already exists, skipping.", verbose)
                    stats["skipped"] += 1
            except Exception as e:
                await session.rollback()
                _log(f"Error updating weekly plan for week {week_num}: {e}", verbose)
                stats["skipped"] += 1
            continue

        try:
            # Create the plan
            plan = WeeklyPlan(
                week_number=week_num,
                week_start_date=date.fromisoformat(plan_data["week_start_date"]),
                week_end_date=date.fromisoformat(plan_data["week_end_date"]),
                deliverable_progress_summary=plan_data.get("deliverable_progress_summary"),
                programme_actions_summary=plan_data.get("programme_actions_summary"),
                status=plan_data.get("status", "DRAFT"),
            )
            session.add(plan)
            await session.flush()  # Get plan.id

            # Create actions
            actions_data = plan_data.get("actions", [])
            for i, action_data in enumerate(actions_data):
                action = WeeklyPlanAction(
                    weekly_plan_id=plan.id,
                    category=action_data["category"],
                    title=action_data["title"],
                    description=action_data.get("description"),
                    priority=action_data.get("priority", "MEDIUM"),
                    owner=action_data.get("owner"),
                    status=action_data.get("status", "PENDING"),
                    deliverable_id=action_data.get("deliverable_id"),
                    position=action_data.get("position", i),
                    is_ai_generated=action_data.get("is_ai_generated", True),
                    carried_from_week=action_data.get("carried_from_week"),
                    source_transcript_id=action_data.get("source_transcript_id"),
                    source_update_id=action_data.get("source_update_id"),
                    context=action_data.get("context"),
                )
                session.add(action)

            # Create progress snapshots
            snapshots_data = plan_data.get("snapshots", [])
            for snap_data in snapshots_data:
                snap = DeliverableProgressSnapshot(
                    deliverable_id=snap_data["deliverable_id"],
                    weekly_plan_id=plan.id,
                    week_number=snap_data.get("week_number", week_num),
                    rag_status=snap_data.get("rag_status", "GREEN"),
                    progress_percent=snap_data.get("progress_percent", 0),
                    milestones_completed=snap_data.get("milestones_completed", 0),
                    milestones_total=snap_data.get("milestones_total", 0),
                    narrative=snap_data.get("narrative"),
                )
                session.add(snap)

            await session.commit()
            _log(f"Created weekly plan for week {week_num} with "
                 f"{len(actions_data)} actions, {len(snapshots_data)} snapshots.", verbose)
            stats["inserted"] += 1

        except Exception as e:
            await session.rollback()
            _log(f"Error creating weekly plan for week {week_num}: {e}", verbose)
            traceback.print_exc()
            stats["errors"] += 1

    return stats


async def seed_programme_wins(session: AsyncSession, verbose: bool) -> dict:
    """Seed programme wins from JSON file. Idempotent by (title, date_recorded)."""
    stats = {"inserted": 0, "skipped": 0, "errors": 0}
    seed_file = Path(__file__).resolve().parent / "seed_data" / "wins.json"

    if not seed_file.exists():
        _log("No wins.json seed file found, skipping.", verbose)
        return stats

    try:
        with open(seed_file, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        _log(f"Error reading wins.json: {e}", verbose)
        stats["errors"] += 1
        return stats

    records = data if isinstance(data, list) else [data]

    for rec in records:
        title = rec.get("title", "").strip()
        if not title:
            stats["errors"] += 1
            continue

        date_str = rec.get("date_recorded")
        date_val = None
        if date_str:
            try:
                date_val = datetime.strptime(date_str, "%Y-%m-%d").date()
            except ValueError:
                date_val = None

        # Check for existing by title + date
        q = select(ProgrammeWin).where(ProgrammeWin.title == title)
        if date_val:
            q = q.where(ProgrammeWin.date_recorded == date_val)
        existing = await session.execute(q)
        if existing.scalar_one_or_none():
            stats["skipped"] += 1
            continue

        try:
            win = ProgrammeWin(
                category=rec.get("category", "process_improvement"),
                title=title,
                description=rec.get("description"),
                before_state=rec.get("before_state"),
                after_state=rec.get("after_state"),
                project=rec.get("project"),
                confidence=rec.get("confidence", "estimated"),
                date_recorded=date_val,
                notes=rec.get("notes"),
                is_manual=False,
            )
            session.add(win)
            stats["inserted"] += 1
        except Exception as e:
            _log(f"Error creating win '{title}': {e}", verbose)
            stats["errors"] += 1

    await session.commit()
    return stats


async def seed_divisions(session: AsyncSession, verbose: bool) -> dict:
    """Seed division profiles from JSON file. Idempotent by name (unique constraint)."""
    stats = {"inserted": 0, "skipped": 0, "errors": 0}
    seed_file = Path(__file__).resolve().parent / "seed_data" / "divisions.json"

    if not seed_file.exists():
        _log("No divisions.json seed file found, skipping.", verbose)
        return stats

    try:
        with open(seed_file, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        _log(f"Error reading divisions.json: {e}", verbose)
        stats["errors"] += 1
        return stats

    records = data if isinstance(data, list) else [data]

    for rec in records:
        name = rec.get("name", "").strip()
        if not name:
            stats["errors"] += 1
            continue

        existing = await session.execute(
            select(DivisionProfile).where(DivisionProfile.name == name)
        )
        if existing.scalar_one_or_none():
            stats["skipped"] += 1
            continue

        try:
            div = DivisionProfile(
                name=name,
                status=rec.get("status", "prospect"),
                current_tools=rec.get("current_tools"),
                pain_points=rec.get("pain_points"),
                key_contact=rec.get("key_contact"),
                notes=rec.get("notes"),
            )
            session.add(div)
            stats["inserted"] += 1
        except Exception as e:
            _log(f"Error creating division '{name}': {e}", verbose)
            stats["errors"] += 1

    await session.commit()
    return stats


async def seed_outreach(session: AsyncSession, verbose: bool) -> dict:
    """Seed outreach contacts from JSON file. Idempotent by (contact_name, division)."""
    stats = {"inserted": 0, "skipped": 0, "errors": 0}
    seed_file = Path(__file__).resolve().parent / "seed_data" / "outreach.json"

    if not seed_file.exists():
        _log("No outreach.json seed file found, skipping.", verbose)
        return stats

    try:
        with open(seed_file, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        _log(f"Error reading outreach.json: {e}", verbose)
        stats["errors"] += 1
        return stats

    records = data if isinstance(data, list) else [data]

    for rec in records:
        name = rec.get("contact_name", "").strip()
        if not name:
            stats["errors"] += 1
            continue

        division = rec.get("division")

        # Check for existing by name + division
        q = select(Outreach).where(Outreach.contact_name == name)
        if division:
            q = q.where(Outreach.division == division)
        existing = await session.execute(q)
        if existing.scalar_one_or_none():
            stats["skipped"] += 1
            continue

        def _parse_date_field(val):
            if not val:
                return None
            try:
                return datetime.strptime(val, "%Y-%m-%d").date()
            except ValueError:
                return None

        try:
            contact = Outreach(
                contact_name=name,
                contact_role=rec.get("contact_role"),
                division=division,
                status=rec.get("status", "initial_contact"),
                interest_level=rec.get("interest_level", 3),
                first_contact_date=_parse_date_field(rec.get("first_contact_date")),
                last_contact_date=_parse_date_field(rec.get("last_contact_date")),
                meeting_count=rec.get("meeting_count", 0),
                notes=rec.get("notes"),
                next_step=rec.get("next_step"),
                next_step_date=_parse_date_field(rec.get("next_step_date")),
            )
            session.add(contact)
            stats["inserted"] += 1
        except Exception as e:
            _log(f"Error creating outreach '{name}': {e}", verbose)
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

    total_steps = 24

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

        # 4. Seed projects (before summaries so project attribution works)
        print(f"[4/{total_steps}] Seeding projects...")
        all_stats["project_seed"] = await seed_projects(session, verbose)

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

        # 20. Seed weekly plans from JSON
        print(f"[20/{total_steps}] Seeding weekly plans...")
        all_stats["weekly_plans"] = await seed_weekly_plans(session, verbose)

        # 21. Build project links for decisions, tasks, threads
        print(f"[21/{total_steps}] Building project links...")
        all_stats["project_links_built"] = await build_project_links(session, verbose)

        # 22. Seed programme wins from JSON
        print(f"[22/{total_steps}] Seeding programme wins...")
        all_stats["programme_wins"] = await seed_programme_wins(session, verbose)

        # 23. Seed division profiles from JSON
        print(f"[23/{total_steps}] Seeding division profiles...")
        all_stats["division_profiles"] = await seed_divisions(session, verbose)

        # 24. Seed outreach contacts from JSON
        print(f"[24/{total_steps}] Seeding outreach contacts...")
        all_stats["outreach_contacts"] = await seed_outreach(session, verbose)

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
        elif entity == "project_seed":
            print(f"  Project seed: {stats['created']} created, "
                  f"{stats.get('updated', 0)} updated, {stats['existing']} existing")
        elif entity == "project_links_built":
            print(f"  Project links: {stats['transcript_links']} transcript, {stats['task_links']} task, "
                  f"{stats['decision_links']} decision, {stats['thread_links']} thread")
            print(f"  Project attribution: {stats['transcript_project_ids']} transcript IDs set, "
                  f"{stats['task_project_ids']} task IDs set, "
                  f"{stats['project_summaries']} project summaries created")
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
            extra = ""
            # Show project attribution stats for summaries
            if entity == "summaries":
                pl = stats.get("project_links", 0)
                ps = stats.get("project_summaries", 0)
                pid = stats.get("project_ids_set", 0)
                if pl or ps or pid:
                    extra = f" | project: {pid} IDs set, {pl} links, {ps} summaries"
            print(f"  {label}: {inserted} inserted, {updated} updated, "
                  f"{skipped} skipped, {errors} errors{extra}")

    print("=" * 60)

    # Check for any errors
    total_errors = 0
    for entity, entity_stats in all_stats.items():
        if entity not in ("mentions", "project_seed"):
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
