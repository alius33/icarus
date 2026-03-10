"""
Rebuild all tasks from enhanced summary files.

Orchestrates a full pipeline:
  1. Extract actionable items from all summary .md files (via summary_extractor)
  2. Deduplicate cross-summary items
  3. Clear the database tasks table completely
  4. Import all consolidated tasks with proper project linking
  5. Regenerate the analysis/trackers/action_items.md tracker file

Usage:
    python -m scripts.rebuild_tasks --data-root /path/to/icarus
    python -m scripts.rebuild_tasks --data-root /path/to/icarus --dry-run --verbose
"""

import argparse
import asyncio
import calendar
import hashlib
import os
import re
import sys
from datetime import date, datetime, timedelta
from pathlib import Path

from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

# ---------------------------------------------------------------------------
# Path setup — must come before app imports
# ---------------------------------------------------------------------------
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.models import ActionItem, DeletedImport, Project, Workstream
from scripts.parsers.summary_extractor import extract_all_summaries

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

WS_PREFIX: dict[str, str] = {
    "WS1": "TRAIN",
    "WS2": "CLARA",
    "WS3": "AGENT",
    "WS4": "FRIDY",
    "WS5": "NAVIG",
    "WS6": "BUILD",
}
DEFAULT_PREFIX = "PROG"

PRIORITY_MAP: dict[str, str] = {
    "HIGH": "MEDIUM",
    "MEDIUM": "LOW",
    "LOW": "NONE",
}

STATUS_MAP: dict[str, str] = {
    "open": "TODO",
    "in progress": "IN_PROGRESS",
    "in_progress": "IN_PROGRESS",
    "complete": "DONE",
    "completed": "DONE",
    "done": "DONE",
    "cancelled": "CANCELLED",
}

DAY_NAMES = {
    "monday": 0,
    "tuesday": 1,
    "wednesday": 2,
    "thursday": 3,
    "friday": 4,
    "saturday": 5,
    "sunday": 6,
}

MONTH_NAMES = {
    "january": 1, "february": 2, "march": 3, "april": 4,
    "may": 5, "june": 6, "july": 7, "august": 8,
    "september": 9, "october": 10, "november": 11, "december": 12,
    "jan": 1, "feb": 2, "mar": 3, "apr": 4,
    "jun": 6, "jul": 7, "aug": 8,
    "sep": 9, "oct": 10, "nov": 11, "dec": 12,
}


# ---------------------------------------------------------------------------
# Date parsing
# ---------------------------------------------------------------------------

def try_parse_deadline(deadline: str, reference_date: date) -> date | None:
    """Try to parse a deadline string into a concrete date.

    Handles: ISO dates, relative terms (Today, Tomorrow, This week, Next week),
    day names (Monday, Tuesday...), "End of <month>", ASAP, TBD, etc.
    """
    if not deadline:
        return None

    cleaned = deadline.strip()
    lower = cleaned.lower()

    # Skip unknowns
    if lower in ("tbd", "n/a", "none", "unclear", "ongoing", ""):
        return None

    # "Today" / "Immediately" / "ASAP"
    if lower in ("today", "immediately", "asap"):
        return reference_date

    # "Tomorrow"
    if lower == "tomorrow":
        return reference_date + timedelta(days=1)

    # "This week" -> Friday of that week
    if lower in ("this week", "end of week"):
        days_until_friday = (4 - reference_date.weekday()) % 7
        if days_until_friday == 0 and reference_date.weekday() > 4:
            days_until_friday = 7
        return reference_date + timedelta(days=max(days_until_friday, 0))

    # "Next week" -> next Monday
    if lower in ("next week",):
        days_until_monday = (7 - reference_date.weekday()) % 7
        if days_until_monday == 0:
            days_until_monday = 7
        return reference_date + timedelta(days=days_until_monday)

    # "Next 2 weeks" / "Next two weeks"
    m = re.match(r"next\s+(\d+)\s+weeks?", lower)
    if m:
        weeks = int(m.group(1))
        return reference_date + timedelta(weeks=weeks)

    # Day names: "Monday", "Friday", etc. -> next occurrence
    for day_name, day_num in DAY_NAMES.items():
        if lower == day_name or lower == f"by {day_name}":
            days_ahead = (day_num - reference_date.weekday()) % 7
            if days_ahead == 0:
                days_ahead = 7
            return reference_date + timedelta(days=days_ahead)

    # "End of <month>" -> last day of that month
    m = re.match(r"end\s+of\s+(\w+)", lower)
    if m:
        month_str = m.group(1).lower()
        month_num = MONTH_NAMES.get(month_str)
        if month_num:
            year = reference_date.year
            if month_num < reference_date.month:
                year += 1
            last_day = calendar.monthrange(year, month_num)[1]
            return date(year, month_num, last_day)

    # ISO date: "2026-03-04"
    m = re.match(r"(\d{4})-(\d{2})-(\d{2})", cleaned)
    if m:
        try:
            return date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
        except ValueError:
            pass

    # Dates like "2026-01-23 EOD" or "2026-01-24 (weekend)"
    m = re.match(r"(\d{4}-\d{2}-\d{2})", cleaned)
    if m:
        try:
            return date.fromisoformat(m.group(1))
        except ValueError:
            pass

    return None


# ---------------------------------------------------------------------------
# Deduplication
# ---------------------------------------------------------------------------

def _normalise_key(text: str) -> str:
    """Normalise text for deduplication: lowercase, strip, first 80 chars."""
    return text.strip().lower()[:80]


def _normalise_assignee(assignee: str | None) -> str:
    """Normalise assignee for grouping: lowercase, strip, handle separators."""
    if not assignee:
        return ""
    # Handle "Richard / Martin" or "Richard/Martin" -> consistent form
    cleaned = assignee.strip().lower()
    cleaned = re.sub(r"\s*/\s*", "/", cleaned)
    return cleaned


def deduplicate_items(items: list[dict]) -> list[dict]:
    """Deduplicate items that appear across multiple summaries.

    Strategy:
      - Group by (normalised_assignee, normalised_description_prefix)
      - For each group, use EARLIEST source_date as created_date
      - Use LATEST source_date's status and deadline
      - Keep the longest description
      - Merge all source_files and workstreams
    """
    groups: dict[tuple[str, str], list[dict]] = {}

    for item in items:
        key = (
            _normalise_assignee(item.get("assignee")),
            _normalise_key(item.get("description", "")),
        )
        if key not in groups:
            groups[key] = []
        groups[key].append(item)

    deduped: list[dict] = []

    for _key, group in groups.items():
        # Sort by source_date so we know earliest and latest
        group.sort(key=lambda x: x.get("source_date") or date(9999, 12, 31))

        earliest = group[0]
        latest = group[-1]

        # Use the longest description
        best_description = max(
            (g.get("description", "") for g in group),
            key=len,
        )

        # Merge source files
        all_sources = []
        seen_sources: set[str] = set()
        for g in group:
            sf = g.get("source_file", "")
            if sf and sf not in seen_sources:
                all_sources.append(sf)
                seen_sources.add(sf)

        # Merge workstreams
        all_ws: list[str] = []
        seen_ws: set[str] = set()
        for g in group:
            for ws in g.get("workstreams", []):
                if ws not in seen_ws:
                    all_ws.append(ws)
                    seen_ws.add(ws)

        # Merge context
        contexts = [g.get("context") for g in group if g.get("context")]
        merged_context = "; ".join(contexts) if contexts else None

        deduped.append({
            "item_type": earliest.get("item_type", "action_item"),
            "description": best_description,
            "assignee": earliest.get("assignee"),
            "deadline": latest.get("deadline"),
            "status": latest.get("status", "Open"),
            "confidence": latest.get("confidence", "MEDIUM"),
            "context": merged_context,
            "source_file": ", ".join(all_sources),
            "source_date": earliest.get("source_date"),
            "workstreams": all_ws,
            "occurrence_count": len(group),
        })

    # Sort by source_date
    deduped.sort(key=lambda x: x.get("source_date") or date(9999, 12, 31))

    return deduped


# ---------------------------------------------------------------------------
# Priority and status mapping
# ---------------------------------------------------------------------------

def map_priority(confidence: str | None, deadline: str | None) -> str:
    """Map extraction confidence to task priority, with deadline overrides."""
    # Start with confidence-based mapping
    base = PRIORITY_MAP.get((confidence or "").upper(), "NONE")

    if not deadline:
        return base

    dl = deadline.lower()

    # Override rules based on deadline urgency
    if any(term in dl for term in ("urgent",)):
        return "URGENT"
    if any(term in dl for term in ("asap", "immediately", "today")):
        return "HIGH"
    if any(term in dl for term in ("this week", "end of week")):
        return max_priority(base, "MEDIUM")

    return base


def max_priority(a: str, b: str) -> str:
    """Return the higher priority of two values."""
    order = ["URGENT", "HIGH", "MEDIUM", "LOW", "NONE"]
    idx_a = order.index(a) if a in order else len(order)
    idx_b = order.index(b) if b in order else len(order)
    return order[min(idx_a, idx_b)]


def map_status(raw: str | None) -> str:
    """Map raw status string to Task model status constant."""
    if not raw:
        return "TODO"
    cleaned = raw.strip().lower()
    # Strip trailing qualifications
    cleaned = re.split(r"\s*[-–—]", cleaned)[0].strip()
    return STATUS_MAP.get(cleaned, "TODO")


# ---------------------------------------------------------------------------
# Status inference heuristics (prevent stale tasks staying OPEN forever)
# ---------------------------------------------------------------------------

# One-shot deadline terms that indicate a task should be done if old enough
_ONE_SHOT_TERMS = {
    "today", "tomorrow", "tonight", "this week", "end of week",
    "this morning", "this afternoon", "asap", "immediately",
    "done during call", "done",
}

# Patterns for tasks that are inherently time-bound
_SCHEDULING_RE = [
    re.compile(r"\bset up\b.*\b(call|meeting|session|standup|check-in|catch-?up|sync)\b", re.I),
    re.compile(r"\bschedule\b", re.I),
    re.compile(r"\breschedule\b", re.I),
]
_SEND_RE = [
    re.compile(r"\bsend\b.*\bto\b", re.I),
    re.compile(r"\bemail\b", re.I),
    re.compile(r"\bcc\b.*\bon\b", re.I),
    re.compile(r"\bforward\b", re.I),
]

_STALE_DAYS = 28  # 4 weeks


def infer_status(item: dict, today: date | None = None) -> str:
    """Infer a smarter status for an item based on age and heuristics.

    Called after basic map_status(). Returns the inferred status or the
    original mapped status if no inference applies.
    """
    if today is None:
        today = date.today()

    mapped = map_status(item.get("status"))

    # Only upgrade TODO items (don't downgrade anything)
    if mapped != "TODO":
        return mapped

    source_date = item.get("source_date")
    if not source_date:
        return mapped

    age = (today - source_date).days
    if age < _STALE_DAYS:
        return mapped  # Too recent to infer

    description = item.get("description", "")

    # Rule: [D] decisions are records, not tasks -> DONE
    if description.strip().startswith("[D]"):
        return "DONE"

    # Rule: One-shot deadlines from 4+ weeks ago -> DONE
    deadline = (item.get("deadline") or "").strip().lower()
    if deadline:
        for term in _ONE_SHOT_TERMS:
            if deadline.startswith(term):
                return "DONE"
        # Date-like deadlines (e.g., "10-12 Jan", "Jan 20", "Week of 12 Jan")
        if re.match(r"^\d{1,2}[-\u2013]\d{1,2}\s+[a-z]", deadline):
            return "DONE"
        if re.match(r"^[a-z]+\s+\d{1,2}$", deadline):
            return "DONE"
        if re.match(r"^week\s+of\b", deadline):
            return "DONE"
        if re.match(r"^by\s+(monday|tuesday|wednesday|thursday|friday|saturday|sunday)", deadline):
            return "DONE"
        if re.match(r"^\d{4}-\d{2}-\d{2}", deadline):
            parsed = try_parse_deadline(deadline, source_date)
            if parsed and (today - parsed).days >= _STALE_DAYS:
                return "DONE"
        if "next week" in deadline:
            return "DONE"

    # Rule: Scheduling tasks from 4+ weeks ago -> DONE
    for pattern in _SCHEDULING_RE:
        if pattern.search(description):
            return "DONE"

    # Rule: Send/email tasks from 4+ weeks ago -> DONE
    for pattern in _SEND_RE:
        if pattern.search(description):
            return "DONE"

    # Rule: [C] commitments from 6+ weeks ago -> DONE
    if description.strip().startswith("[C]") and age >= 42:
        return "DONE"

    # Rule: Ongoing/In progress -> IN_PROGRESS
    if "ongoing" in deadline or "in progress" in deadline:
        return "IN_PROGRESS"

    return mapped


# ---------------------------------------------------------------------------
# Identifier generation
# ---------------------------------------------------------------------------

def compute_item_hash(description: str, assignee: str | None, source_file: str) -> str:
    """Compute a stable SHA256 hash for a task from its key fields."""
    parts = [
        (description or "").strip().lower(),
        (assignee or "").strip().lower(),
        (source_file or "").strip(),
    ]
    raw = "|".join(parts)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


# ---------------------------------------------------------------------------
# Workstream -> Project mapping
# ---------------------------------------------------------------------------

async def build_project_map(session: AsyncSession) -> dict[str, int]:
    """Build a workstream code -> project_id lookup from the database.

    Returns a dict like {"WS2": 5, "WS6": 12, ...}.
    Also includes a special key "_default" for the fallback project if one exists.
    """
    result = await session.execute(
        select(Project.id, Project.name, Workstream.code)
        .join(Workstream, Project.workstream_id == Workstream.id, isouter=True)
    )
    rows = result.all()

    mapping: dict[str, int] = {}
    for project_id, project_name, ws_code in rows:
        if ws_code:
            mapping[ws_code] = project_id
        # Also try to match by name patterns
        name_lower = (project_name or "").lower()
        if "programme" in name_lower or "program" in name_lower:
            mapping["_default"] = project_id

    return mapping


def resolve_project_id(
    workstreams: list[str],
    project_map: dict[str, int],
) -> int | None:
    """Resolve the project_id for an item based on its workstreams.

    Uses the FIRST workstream for project linking. Falls back to _default.
    """
    for ws in workstreams:
        if ws in project_map:
            return project_map[ws]
    return project_map.get("_default")


def resolve_prefix(workstreams: list[str]) -> str:
    """Determine the identifier prefix from workstreams."""
    if workstreams:
        return WS_PREFIX.get(workstreams[0], DEFAULT_PREFIX)
    return DEFAULT_PREFIX


# ---------------------------------------------------------------------------
# Tracker file generation
# ---------------------------------------------------------------------------

def format_date_short(d: date | None) -> str:
    """Format date as '3 Mar' style for the tracker table."""
    if not d:
        return ""
    return f"{d.day} {d.strftime('%b')}"


def source_display(source_file: str) -> str:
    """Extract just the filename(s) from source_file paths for display."""
    if not source_file:
        return ""
    parts = [Path(s.strip()).name for s in source_file.split(",")]
    # Deduplicate while preserving order
    seen: set[str] = set()
    unique: list[str] = []
    for p in parts:
        if p not in seen:
            unique.append(p)
            seen.add(p)
    return ", ".join(unique[:3])  # Max 3 sources for readability


def generate_tracker_file(tasks: list[dict], data_root: Path) -> None:
    """Write the analysis/trackers/action_items.md file.

    Groups items by status:
      - TODO / IN_PROGRESS -> OPEN
      - IN_REVIEW -> LIKELY COMPLETED
      - DONE / CANCELLED -> COMPLETED
    """
    today = date.today().isoformat()

    # Filter out [D] decision items -- they belong in decisions tracker, not tasks
    filtered = [t for t in tasks if not (t.get("description", "").strip().startswith("[D]"))]
    total = len(filtered)

    open_items: list[dict] = []
    likely_items: list[dict] = []
    completed_items: list[dict] = []

    for task in filtered:
        status = task.get("_mapped_status", "TODO")
        if status in ("TODO", "IN_PROGRESS"):
            open_items.append(task)
        elif status == "IN_REVIEW":
            likely_items.append(task)
        else:
            completed_items.append(task)

    lines: list[str] = []
    lines.append("# Action Items Tracker")
    lines.append("")
    lines.append(f"Last updated: {today} (rebuilt from {total} consolidated tasks, decisions excluded)")
    lines.append("")
    lines.append("Items are grouped by status. [C] = commitment.")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## OPEN")
    lines.append("")
    lines.append("| # | Date | Action | Owner | Deadline | Context | Source |")
    lines.append("|---|------|--------|-------|----------|---------|--------|")

    for i, task in enumerate(open_items, 1):
        d = format_date_short(task.get("source_date"))
        desc = (task.get("description") or "")[:120]
        owner = task.get("assignee") or ""
        deadline = task.get("deadline") or ""
        ctx = (task.get("context") or "")[:60]
        src = source_display(task.get("source_file", ""))
        lines.append(f"| {i} | {d} | {desc} | {owner} | {deadline} | {ctx} | {src} |")

    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## LIKELY COMPLETED (need confirmation)")
    lines.append("")
    lines.append("| # | Date | Action | Likely Status | Source |")
    lines.append("|---|------|--------|---------------|--------|")

    for i, task in enumerate(likely_items, 1):
        d = format_date_short(task.get("source_date"))
        desc = (task.get("description") or "")[:120]
        status = task.get("status") or "In review"
        src = source_display(task.get("source_file", ""))
        lines.append(f"| {i} | {d} | {desc} | {status} | {src} |")

    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## COMPLETED")
    lines.append("")
    lines.append("| # | Date | Action | Completed | Notes | Source |")
    lines.append("|---|------|--------|-----------|-------|--------|")

    for i, task in enumerate(completed_items, 1):
        d = format_date_short(task.get("source_date"))
        desc = (task.get("description") or "")[:120]
        completed_date = ""
        notes = task.get("context") or ""
        src = source_display(task.get("source_file", ""))
        lines.append(f"| {i} | {d} | {desc} | {completed_date} | {notes[:60]} | {src} |")

    # Write the file
    tracker_path = data_root / "analysis" / "trackers" / "action_items.md"
    tracker_path.parent.mkdir(parents=True, exist_ok=True)
    tracker_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"  Wrote tracker: {tracker_path}")


# ---------------------------------------------------------------------------
# Database operations
# ---------------------------------------------------------------------------

async def clear_tasks_table(session: AsyncSession, verbose: bool = False) -> None:
    """Clear all task-related records from the database."""
    if verbose:
        print("  Clearing project_links for tasks...")
    await session.execute(text("DELETE FROM project_links WHERE entity_type = 'task'"))

    if verbose:
        print("  Clearing deleted_imports for tasks/action_items...")
    await session.execute(
        text("DELETE FROM deleted_imports WHERE entity_type IN ('task', 'action_item')")
    )

    if verbose:
        print("  Clearing tasks table...")
    await session.execute(text("DELETE FROM tasks"))

    await session.commit()
    print("  Database cleared: project_links (task), deleted_imports, tasks.")


async def insert_tasks(
    session: AsyncSession,
    tasks: list[dict],
    project_map: dict[str, int],
    verbose: bool = False,
) -> int:
    """Insert deduplicated tasks into the database.

    Returns the number of tasks inserted.
    """
    # Group tasks by status for position assignment
    status_groups: dict[str, list[dict]] = {}
    for task in tasks:
        status = task.get("_mapped_status", "TODO")
        if status not in status_groups:
            status_groups[status] = []
        status_groups[status].append(task)

    # Track identifier sequences per prefix
    prefix_seq: dict[str, int] = {}
    inserted = 0

    for task in tasks:
        workstreams = task.get("workstreams", [])
        prefix = resolve_prefix(workstreams)
        seq = prefix_seq.get(prefix, 0) + 1
        prefix_seq[prefix] = seq

        identifier = f"{prefix}-{seq}"
        number = f"M-{seq:03d}"

        description = task.get("description", "")
        title = description[:200]
        assignee = task.get("assignee")
        mapped_status = task.get("_mapped_status", "TODO")
        mapped_priority = task.get("_mapped_priority", "NONE")
        source_date = task.get("source_date")
        deadline_str = task.get("deadline")
        context = task.get("context")
        item_type = task.get("item_type", "action_item")
        source_file = task.get("source_file", "")
        file_hash = compute_item_hash(description, assignee, source_file)

        # Parse due_date from deadline string
        due_date = None
        if deadline_str and source_date:
            due_date = try_parse_deadline(deadline_str, source_date)

        # Resolve project_id
        project_id = resolve_project_id(workstreams, project_map)

        # Compute position within status group
        status_list = status_groups.get(mapped_status, [])
        try:
            pos_index = status_list.index(task)
        except ValueError:
            pos_index = 0
        position = pos_index * 1000

        try:
            record = ActionItem(
                identifier=identifier,
                number=number,
                title=title,
                description=description,
                status=mapped_status,
                priority=mapped_priority,
                assignee=assignee,
                owner=assignee,
                labels=[item_type],
                due_date=due_date,
                created_date=source_date,
                action_date=source_date,
                deadline=deadline_str,
                context=context,
                project_id=project_id,
                position=position,
                is_manual=False,
                source_file=source_file,
                file_hash=file_hash,
            )
            session.add(record)
            inserted += 1

            if verbose and inserted % 50 == 0:
                print(f"    ... inserted {inserted} tasks")

        except Exception as e:
            print(f"  [WARN] Failed to create task '{identifier}': {e}")
            continue

    await session.commit()

    # Create project_links entries so project pages show correct counts
    if verbose:
        print("  Creating project_links for tasks with project_id...")
    await session.execute(
        text(
            "INSERT INTO project_links (project_id, entity_type, entity_id) "
            "SELECT project_id, 'task', id FROM tasks "
            "WHERE project_id IS NOT NULL "
            "ON CONFLICT (project_id, entity_type, entity_id) DO NOTHING"
        )
    )
    await session.commit()

    link_count = (await session.execute(
        text("SELECT count(*) FROM project_links WHERE entity_type = 'task'")
    )).scalar()
    print(f"  Created {link_count} project_links for tasks.")

    return inserted


# ---------------------------------------------------------------------------
# Main orchestrator
# ---------------------------------------------------------------------------

async def rebuild_all(
    data_root_str: str,
    db_url: str,
    verbose: bool = False,
    dry_run: bool = False,
) -> None:
    """Run the full rebuild pipeline."""
    data_root = Path(data_root_str).resolve()
    summaries_dir = data_root / "analysis" / "summaries"

    print("=" * 60)
    print("REBUILD TASKS FROM ENHANCED SUMMARIES")
    print("=" * 60)
    print(f"  Data root:    {data_root}")
    print(f"  Summaries:    {summaries_dir}")
    print(f"  DB URL:       {db_url[:40]}...")
    print(f"  Dry run:      {dry_run}")
    print(f"  Verbose:      {verbose}")
    print()

    # -----------------------------------------------------------------
    # Step 1: Extract items from all summary files
    # -----------------------------------------------------------------
    print("[1/5] Extracting items from summary files...")

    if not summaries_dir.is_dir():
        print(f"  ERROR: Summaries directory not found: {summaries_dir}")
        sys.exit(1)

    raw_items = extract_all_summaries(summaries_dir)
    file_count = len(list(summaries_dir.glob("*.md")))
    print(f"  Scanned {file_count} summary files.")
    print(f"  Extracted {len(raw_items)} raw items.")

    if verbose:
        by_type: dict[str, int] = {}
        for item in raw_items:
            t = item.get("item_type", "unknown")
            by_type[t] = by_type.get(t, 0) + 1
        for t in sorted(by_type):
            print(f"    {t}: {by_type[t]}")
    print()

    # -----------------------------------------------------------------
    # Step 2: Deduplicate
    # -----------------------------------------------------------------
    print("[2/5] Deduplicating cross-summary items...")

    deduped = deduplicate_items(raw_items)
    print(f"  {len(raw_items)} raw -> {len(deduped)} unique items.")
    print(f"  Removed {len(raw_items) - len(deduped)} duplicates.")

    if verbose:
        multi_occurrence = [d for d in deduped if d.get("occurrence_count", 1) > 1]
        print(f"  Items appearing in multiple summaries: {len(multi_occurrence)}")
    print()

    # -----------------------------------------------------------------
    # Step 3: Map status and priority
    # -----------------------------------------------------------------
    print("[3/5] Mapping status and priority...")

    status_counts: dict[str, int] = {}
    priority_counts: dict[str, int] = {}

    for item in deduped:
        mapped_status = infer_status(item)  # Uses map_status() + heuristics
        mapped_priority = map_priority(item.get("confidence"), item.get("deadline"))
        item["_mapped_status"] = mapped_status
        item["_mapped_priority"] = mapped_priority

        status_counts[mapped_status] = status_counts.get(mapped_status, 0) + 1
        priority_counts[mapped_priority] = priority_counts.get(mapped_priority, 0) + 1

    print("  Status distribution:")
    for s in ["TODO", "IN_PROGRESS", "IN_REVIEW", "DONE", "CANCELLED"]:
        if s in status_counts:
            print(f"    {s:15s} {status_counts[s]:>4d}")

    print("  Priority distribution:")
    for p in ["URGENT", "HIGH", "MEDIUM", "LOW", "NONE"]:
        if p in priority_counts:
            print(f"    {p:15s} {priority_counts[p]:>4d}")
    print()

    # -----------------------------------------------------------------
    # Dry run stops here
    # -----------------------------------------------------------------
    if dry_run:
        print("[DRY RUN] Skipping database operations and tracker generation.")
        print()
        _print_sample(deduped)
        return

    # -----------------------------------------------------------------
    # Step 4: Clear database and insert tasks
    # -----------------------------------------------------------------
    print("[4/5] Clearing database and inserting tasks...")

    engine = create_async_engine(db_url, echo=False)
    session_factory = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with session_factory() as session:
        # Build project mapping before clearing
        project_map = await build_project_map(session)
        if verbose:
            print(f"  Project map: {project_map}")

        # Clear existing tasks
        await clear_tasks_table(session, verbose=verbose)

        # Insert new tasks
        inserted = await insert_tasks(session, deduped, project_map, verbose=verbose)
        print(f"  Inserted {inserted} tasks into database.")
    print()

    await engine.dispose()

    # -----------------------------------------------------------------
    # Step 5: Regenerate tracker file
    # -----------------------------------------------------------------
    print("[5/5] Regenerating tracker file...")
    generate_tracker_file(deduped, data_root)
    print()

    # -----------------------------------------------------------------
    # Summary
    # -----------------------------------------------------------------
    print("=" * 60)
    print("REBUILD COMPLETE")
    print("=" * 60)
    print(f"  Summary files processed: {file_count}")
    print(f"  Raw items extracted:     {len(raw_items)}")
    print(f"  After deduplication:     {len(deduped)}")
    print(f"  Tasks inserted:          {inserted}")
    print(f"  Tracker written:         {data_root / 'analysis' / 'trackers' / 'action_items.md'}")


def _print_sample(tasks: list[dict], n: int = 10) -> None:
    """Print a sample of tasks for dry-run inspection."""
    print(f"  Sample of first {min(n, len(tasks))} tasks:")
    print()

    for i, task in enumerate(tasks[:n]):
        ws = ", ".join(task.get("workstreams", []))
        prefix = resolve_prefix(task.get("workstreams", []))
        print(f"  [{i+1}] {prefix}-{i+1}")
        print(f"      Type:        {task.get('item_type')}")
        print(f"      Description: {(task.get('description') or '')[:80]}")
        print(f"      Assignee:    {task.get('assignee')}")
        print(f"      Status:      {task.get('_mapped_status')} (raw: {task.get('status')})")
        print(f"      Priority:    {task.get('_mapped_priority')} (confidence: {task.get('confidence')})")
        print(f"      Deadline:    {task.get('deadline')}")
        print(f"      Workstreams: {ws}")
        print(f"      Occurrences: {task.get('occurrence_count', 1)}")
        print(f"      Source:      {source_display(task.get('source_file', ''))}")
        print()


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Rebuild tasks from enhanced summaries"
    )
    parser.add_argument(
        "--data-root",
        required=True,
        help="Path to the Icarus project root (contains analysis/ and Transcripts/)",
    )
    parser.add_argument(
        "--db-url",
        default=None,
        help="Database URL (default: $DATABASE_URL or postgresql+asyncpg://icarus:icarus_local@localhost:5432/icarus)",
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Print detailed progress",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Extract and deduplicate but don't touch DB or write tracker",
    )
    args = parser.parse_args()

    db_url = (
        args.db_url
        or os.environ.get("DATABASE_URL")
        or "postgresql+asyncpg://icarus:icarus_local@localhost:5432/icarus"
    )

    asyncio.run(rebuild_all(args.data_root, db_url, args.verbose, args.dry_run))
