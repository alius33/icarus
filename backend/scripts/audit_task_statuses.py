"""
Audit and reclassify task statuses.

Reads all OPEN tasks from analysis/trackers/action_items.md, applies rule-based
heuristics and evidence search against summaries/weekly reports, then outputs a
categorized report. In --apply mode, regenerates the tracker with correct statuses
and updates the database.

Usage:
    python -m scripts.audit_task_statuses --data-root /path/to/icarus --dry-run
    python -m scripts.audit_task_statuses --data-root /path/to/icarus --apply
"""

import argparse
import asyncio
import calendar
import hashlib
import os
import re
import sys
from datetime import date, timedelta
from pathlib import Path

# ---------------------------------------------------------------------------
# Path setup -- only import lightweight parsers, NOT app models
# ---------------------------------------------------------------------------
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from scripts.parsers.action_item_parser import parse_action_items, _parse_action_date


# ---------------------------------------------------------------------------
# Inlined utilities from rebuild_tasks.py (avoids importing app.models)
# ---------------------------------------------------------------------------

MONTH_NAMES = {
    "january": 1, "february": 2, "march": 3, "april": 4,
    "may": 5, "june": 6, "july": 7, "august": 8,
    "september": 9, "october": 10, "november": 11, "december": 12,
    "jan": 1, "feb": 2, "mar": 3, "apr": 4,
    "jun": 6, "jul": 7, "aug": 8,
    "sep": 9, "oct": 10, "nov": 11, "dec": 12,
}

DAY_NAMES = {
    "monday": 0, "tuesday": 1, "wednesday": 2, "thursday": 3,
    "friday": 4, "saturday": 5, "sunday": 6,
}


def try_parse_deadline(deadline: str, reference_date: date) -> date | None:
    if not deadline:
        return None
    cleaned = deadline.strip()
    lower = cleaned.lower()
    if lower in ("tbd", "n/a", "none", "unclear", "ongoing", ""):
        return None
    if lower in ("today", "immediately", "asap"):
        return reference_date
    if lower == "tomorrow":
        return reference_date + timedelta(days=1)
    if lower in ("this week", "end of week"):
        days_until_friday = (4 - reference_date.weekday()) % 7
        return reference_date + timedelta(days=max(days_until_friday, 0))
    if lower == "next week":
        days_until_monday = (7 - reference_date.weekday()) % 7
        if days_until_monday == 0:
            days_until_monday = 7
        return reference_date + timedelta(days=days_until_monday)
    for day_name, day_num in DAY_NAMES.items():
        if lower == day_name or lower == f"by {day_name}":
            days_ahead = (day_num - reference_date.weekday()) % 7
            if days_ahead == 0:
                days_ahead = 7
            return reference_date + timedelta(days=days_ahead)
    m = re.match(r"end\s+of\s+(\w+)", lower)
    if m:
        month_num = MONTH_NAMES.get(m.group(1).lower())
        if month_num:
            year = reference_date.year
            if month_num < reference_date.month:
                year += 1
            last_day = calendar.monthrange(year, month_num)[1]
            return date(year, month_num, last_day)
    m = re.match(r"(\d{4}-\d{2}-\d{2})", cleaned)
    if m:
        try:
            return date.fromisoformat(m.group(1))
        except ValueError:
            pass
    return None


def format_date_short(d: date | None) -> str:
    if not d:
        return ""
    return f"{d.day} {d.strftime('%b')}"


def source_display(source_file: str) -> str:
    if not source_file:
        return ""
    parts = [Path(s.strip()).name for s in source_file.split(",")]
    seen: set[str] = set()
    unique: list[str] = []
    for p in parts:
        if p not in seen:
            unique.append(p)
            seen.add(p)
    return ", ".join(unique[:3])

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

TODAY = date.today()
STALE_THRESHOLD_DAYS = 28   # 4 weeks -- tasks older than this with past deadlines -> DONE
RECENT_THRESHOLD_DAYS = 14  # 2 weeks -- tasks newer than this are left alone
VERY_STALE_DAYS = 42        # 6 weeks -- catch-all stale threshold

# Deadline terms that indicate a one-shot action
ONE_SHOT_DEADLINES = {
    "today", "tomorrow", "tonight", "this week", "end of week",
    "this morning", "this afternoon", "asap", "immediately",
    "done during call", "done",
}

# Patterns for scheduling tasks
SCHEDULING_PATTERNS = [
    r"\bset up\b.*\b(call|meeting|session|standup|check-in|catch-?up|sync)\b",
    r"\bschedule\b",
    r"\breschedule\b",
    r"\bbook\b.*\b(meeting|call|room|session)\b",
    r"\barrange\b.*\b(call|meeting)\b",
]

# Patterns for send/email tasks
SEND_PATTERNS = [
    r"\bsend\b.*\bto\b",
    r"\bemail\b",
    r"\bcc\b.*\bon\b",
    r"\bforward\b",
    r"\bshare\b.*\b(with|to)\b",
    r"\bcirculate\b",
]

# Patterns for code/deploy tasks
CODE_PATTERNS = [
    r"\bpush\b.*\b(code|branch|to github|to repo|latest)\b",
    r"\bdeploy\b",
    r"\bcreate\s+(new\s+)?branch\b",
    r"\bmerge\b.*\bbranch\b",
    r"\bcommit\b",
    r"\bclone\b.*\brepo\b",
    r"\bgit\b",
]

# Completion language for evidence search
COMPLETION_WORDS = {
    "done", "completed", "finished", "delivered", "deployed",
    "resolved", "closed", "sorted", "fixed", "shipped",
    "launched", "released", "implemented", "built", "created",
    "sent", "emailed", "shared", "published", "submitted",
    "approved", "confirmed", "agreed", "signed off",
    "went live", "live", "in production", "working",
}

# Stop words for keyword extraction
STOP_WORDS = {
    "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for",
    "of", "with", "by", "from", "up", "about", "into", "through", "during",
    "before", "after", "above", "below", "between", "out", "off", "over",
    "under", "again", "further", "then", "once", "is", "are", "was", "were",
    "be", "been", "being", "have", "has", "had", "having", "do", "does",
    "did", "doing", "will", "would", "shall", "should", "may", "might",
    "must", "can", "could", "need", "this", "that", "these", "those",
    "it", "its", "he", "she", "they", "them", "his", "her", "their",
    "we", "our", "you", "your", "all", "each", "every", "both", "few",
    "more", "most", "other", "some", "such", "no", "not", "only", "same",
    "so", "than", "too", "very", "just", "also", "now", "new", "get",
    "make", "use", "set", "call", "work", "also", "any", "if", "next",
    "end", "week", "today", "tomorrow", "check", "update", "add",
}


# ---------------------------------------------------------------------------
# Categories
# ---------------------------------------------------------------------------

class Category:
    DELETE_DECISION = "DELETE_DECISION"
    DONE_ONESHOT = "DONE_ONESHOT"
    DONE_SCHEDULING = "DONE_SCHEDULING"
    DONE_SEND = "DONE_SEND"
    DONE_CODE = "DONE_CODE"
    DONE_COMMITMENT = "DONE_COMMITMENT"
    DONE_EVIDENCE = "DONE_EVIDENCE"
    IN_PROGRESS = "IN_PROGRESS"
    STALE = "STALE"
    KEEP_OPEN = "KEEP_OPEN"
    KEEP_RECENT = "KEEP_RECENT"
    ALREADY_DONE = "ALREADY_DONE"


CATEGORY_LABELS = {
    Category.DELETE_DECISION: "Decisions (removed)",
    Category.DONE_ONESHOT: "Done -- one-shot past action",
    Category.DONE_SCHEDULING: "Done -- scheduling task",
    Category.DONE_SEND: "Done -- send/email task",
    Category.DONE_CODE: "Done -- code/deploy task",
    Category.DONE_COMMITMENT: "Done -- past commitment",
    Category.DONE_EVIDENCE: "Done -- evidence found in later meetings",
    Category.IN_PROGRESS: "In Progress -- ongoing/recurring",
    Category.STALE: "Stale -- no evidence, needs review",
    Category.KEEP_OPEN: "Still Open -- valid task",
    Category.KEEP_RECENT: "Still Open -- recent (< 14 days)",
    Category.ALREADY_DONE: "Already Done/Completed",
}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def task_age_days(task: dict) -> int:
    """Days since this task was created."""
    action_date = task.get("action_date")
    if not action_date:
        return 999  # Unknown age -> treat as old
    return (TODAY - action_date).days


def is_decision(task: dict) -> bool:
    """Check if the raw description (before stripping) starts with [D]."""
    raw = task.get("raw_description", task.get("description", ""))
    return raw.strip().startswith("[D]")


def is_commitment(task: dict) -> bool:
    """Check if the raw description starts with [C]."""
    raw = task.get("raw_description", task.get("description", ""))
    return raw.strip().startswith("[C]")


def has_one_shot_deadline(task: dict) -> bool:
    """Check if the deadline indicates a one-time action."""
    deadline = (task.get("deadline") or "").strip().lower()
    if not deadline:
        return False
    # Direct match
    if deadline in ONE_SHOT_DEADLINES:
        return True
    # Partial match for compound deadlines like "Today (before 2pm)"
    for term in ONE_SHOT_DEADLINES:
        if deadline.startswith(term):
            return True
    # Dates like "10-12 Jan", "Jan 20", "Week of 12 Jan"
    if re.match(r"^\d{1,2}[-–]\d{1,2}\s+[a-z]", deadline):
        return True
    if re.match(r"^[a-z]+\s+\d{1,2}$", deadline):
        return True
    if re.match(r"^week\s+of\b", deadline):
        return True
    # "End of <month>" for past months
    m = re.match(r"^end\s+of\s+(\w+)", deadline)
    if m:
        return True
    # "By <day name>"
    if re.match(r"^by\s+(monday|tuesday|wednesday|thursday|friday|saturday|sunday)", deadline):
        return True
    # Specific date "2026-01-XX"
    if re.match(r"^\d{4}-\d{2}-\d{2}", deadline):
        return True
    # "Next week" from 4+ weeks ago
    if "next week" in deadline:
        return True
    # "Done" / "Done during call"
    if "done" in deadline:
        return True
    return False


def matches_patterns(description: str, patterns: list[str]) -> bool:
    """Check if description matches any of the regex patterns."""
    lower = description.lower()
    for pattern in patterns:
        if re.search(pattern, lower):
            return True
    return False


def extract_keywords(description: str) -> set[str]:
    """Extract significant keywords from a description for evidence search."""
    # Remove [C] / [D] prefixes
    cleaned = re.sub(r"^\[(?:C|D)\]\s*", "", description)
    # Split into words, lowercase, remove short/stop words
    words = re.findall(r"[a-zA-Z]{3,}", cleaned.lower())
    keywords = {w for w in words if w not in STOP_WORDS and len(w) > 2}
    # Also extract proper names (capitalized words in original)
    names = re.findall(r"\b[A-Z][a-z]{2,}\b", cleaned)
    keywords.update(n.lower() for n in names)
    return keywords


# ---------------------------------------------------------------------------
# Evidence search
# ---------------------------------------------------------------------------

def load_summaries_text(summaries_dir: Path) -> list[tuple[date | None, str, str]]:
    """Load all summary files as (date, filename, full_text) tuples."""
    results = []
    for f in sorted(summaries_dir.glob("*.md")):
        content = f.read_text(encoding="utf-8", errors="replace")
        # Extract date from header
        m = re.search(r"\*\*Date:\*\*\s*(\d{4}-\d{2}-\d{2})", content)
        file_date = None
        if m:
            try:
                file_date = date.fromisoformat(m.group(1))
            except ValueError:
                pass
        results.append((file_date, f.name, content))
    return results


def load_weekly_text(weekly_dir: Path) -> list[tuple[str, str]]:
    """Load all weekly report files as (filename, full_text) tuples."""
    results = []
    for f in sorted(weekly_dir.glob("*.md")):
        content = f.read_text(encoding="utf-8", errors="replace")
        results.append((f.name, content))
    return results


def search_completion_evidence(
    task: dict,
    summaries: list[tuple[date | None, str, str]],
    weeklies: list[tuple[str, str]],
) -> tuple[bool, str | None]:
    """Search later summaries and weekly reports for evidence the task was completed.

    Returns (found, evidence_source) tuple.
    """
    keywords = extract_keywords(task.get("description", ""))
    if len(keywords) < 2:
        return False, None

    task_date = task.get("action_date")

    # Need at least 3 keyword matches + 1 completion word
    min_keyword_matches = min(3, len(keywords))

    # Search summaries dated after the task
    for summary_date, filename, content in summaries:
        if task_date and summary_date and summary_date <= task_date:
            continue

        content_lower = content.lower()
        matched_keywords = sum(1 for kw in keywords if kw in content_lower)
        if matched_keywords < min_keyword_matches:
            continue

        # Check for completion language near the keyword matches
        for completion_word in COMPLETION_WORDS:
            if completion_word in content_lower:
                return True, filename

    # Search weekly reports
    for filename, content in weeklies:
        content_lower = content.lower()
        matched_keywords = sum(1 for kw in keywords if kw in content_lower)
        if matched_keywords < min_keyword_matches:
            continue

        for completion_word in COMPLETION_WORDS:
            if completion_word in content_lower:
                return True, f"weekly/{filename}"

    return False, None


# ---------------------------------------------------------------------------
# Classification engine
# ---------------------------------------------------------------------------

def classify_task(
    task: dict,
    summaries: list[tuple[date | None, str, str]],
    weeklies: list[tuple[str, str]],
) -> tuple[str, str]:
    """Classify a single task into a category.

    Returns (category, reason) tuple.
    """
    desc = task.get("description", "")
    raw_desc = task.get("raw_description", desc)
    status = task.get("status", "OPEN")
    age = task_age_days(task)

    # Rule 1: Remove decisions
    if is_decision(task):
        return Category.DELETE_DECISION, "Decision item -- not a task"

    # Rule 2: Already completed
    if status in ("COMPLETED", "LIKELY COMPLETED"):
        return Category.ALREADY_DONE, f"Already {status}"

    # Rule 3: Recent tasks (< 14 days) -- don't touch
    if age < RECENT_THRESHOLD_DAYS:
        return Category.KEEP_RECENT, f"Recent ({age} days old)"

    # Rule 4: One-shot past actions with old deadlines
    if has_one_shot_deadline(task) and age >= STALE_THRESHOLD_DAYS:
        return Category.DONE_ONESHOT, f"One-shot deadline '{task.get('deadline')}', {age}d old"

    # Rule 5: Scheduling tasks
    if matches_patterns(desc, SCHEDULING_PATTERNS) and age >= STALE_THRESHOLD_DAYS:
        return Category.DONE_SCHEDULING, f"Scheduling task, {age}d old"

    # Rule 6: Send/email tasks
    if matches_patterns(desc, SEND_PATTERNS) and age >= STALE_THRESHOLD_DAYS:
        return Category.DONE_SEND, f"Send/email task, {age}d old"

    # Rule 7: Code/deploy tasks
    if matches_patterns(desc, CODE_PATTERNS) and age >= STALE_THRESHOLD_DAYS:
        return Category.DONE_CODE, f"Code/deploy task, {age}d old"

    # Rule 8: Past commitments
    if is_commitment(task) and age >= STALE_THRESHOLD_DAYS:
        deadline = task.get("deadline", "")
        if deadline:
            parsed = try_parse_deadline(deadline, task.get("action_date") or TODAY)
            if parsed and (TODAY - parsed).days >= STALE_THRESHOLD_DAYS:
                return Category.DONE_COMMITMENT, f"Commitment, deadline was '{deadline}'"
        # Commitments without deadlines but very old
        if age >= VERY_STALE_DAYS:
            return Category.DONE_COMMITMENT, f"Old commitment, {age}d old, no recent activity"

    # Rule 9: Ongoing/recurring
    deadline_lower = (task.get("deadline") or "").lower()
    if "ongoing" in deadline_lower or "in progress" in deadline_lower:
        return Category.IN_PROGRESS, f"Deadline says '{task.get('deadline')}'"

    # Rule 10: Evidence search for remaining tasks
    if age >= STALE_THRESHOLD_DAYS:
        found, source = search_completion_evidence(task, summaries, weeklies)
        if found:
            return Category.DONE_EVIDENCE, f"Completion evidence in {source}"

    # Rule 11: Stale fallback
    if age >= VERY_STALE_DAYS:
        return Category.STALE, f"No evidence, {age}d old"

    # Default: keep open
    return Category.KEEP_OPEN, f"Valid open task, {age}d old"


# ---------------------------------------------------------------------------
# Parse OPEN tasks with raw descriptions preserved
# ---------------------------------------------------------------------------

def parse_open_tasks_raw(tracker_path: Path) -> list[dict]:
    """Parse OPEN tasks keeping both raw and stripped descriptions."""
    content = tracker_path.read_text(encoding="utf-8", errors="replace")
    lines = content.splitlines()

    items = []
    in_open = False
    in_table = False

    for line in lines:
        stripped = line.strip()

        if stripped.startswith("## OPEN"):
            in_open = True
            in_table = False
            continue
        elif stripped.startswith("## "):
            if in_open:
                break  # Past the OPEN section
            continue

        if not in_open:
            continue

        if stripped.startswith("| #"):
            in_table = True
            continue
        if stripped.startswith("|---") or stripped.startswith("| ---"):
            continue

        if in_table and stripped.startswith("|"):
            cols = [c.strip() for c in stripped.split("|")]
            cols = [c for c in cols if c != ""]

            if len(cols) < 3:
                continue

            number = cols[0].strip()
            date_str = cols[1].strip()
            action_date = _parse_action_date(date_str)

            raw_description = cols[2].strip() if len(cols) > 2 else ""
            description = re.sub(r"^\[(?:C|D)\]\s*", "", raw_description)

            owner = cols[3].strip() if len(cols) > 3 else None
            deadline = cols[4].strip() if len(cols) > 4 else None
            context = cols[5].strip() if len(cols) > 5 else None
            source = cols[6].strip() if len(cols) > 6 else None

            items.append({
                "number": number,
                "action_date": action_date,
                "raw_description": raw_description,
                "description": description,
                "owner": owner,
                "deadline": deadline,
                "context": context,
                "source": source,
                "status": "OPEN",
            })

    return items


# ---------------------------------------------------------------------------
# Report generation
# ---------------------------------------------------------------------------

def generate_report(
    categorized: list[tuple[dict, str, str]],
    report_path: Path | None = None,
) -> str:
    """Generate the audit report as a markdown string."""
    lines = []
    lines.append("# Task Status Audit Report")
    lines.append(f"Generated: {TODAY.isoformat()}")
    lines.append("")

    # Count by category
    counts: dict[str, int] = {}
    by_category: dict[str, list[tuple[dict, str]]] = {}
    for task, category, reason in categorized:
        counts[category] = counts.get(category, 0) + 1
        if category not in by_category:
            by_category[category] = []
        by_category[category].append((task, reason))

    total = len(categorized)
    deleted = counts.get(Category.DELETE_DECISION, 0)
    done = sum(counts.get(c, 0) for c in [
        Category.DONE_ONESHOT, Category.DONE_SCHEDULING, Category.DONE_SEND,
        Category.DONE_CODE, Category.DONE_COMMITMENT, Category.DONE_EVIDENCE,
    ])
    in_progress = counts.get(Category.IN_PROGRESS, 0)
    stale = counts.get(Category.STALE, 0)
    keep_open = counts.get(Category.KEEP_OPEN, 0) + counts.get(Category.KEEP_RECENT, 0)
    already_done = counts.get(Category.ALREADY_DONE, 0)

    lines.append("## Summary")
    lines.append("")
    lines.append(f"- **Total tasks audited:** {total}")
    lines.append(f"- **Decisions removed:** {deleted}")
    lines.append(f"- **Auto-closed (DONE):** {done}")
    lines.append(f"- **Set to IN_PROGRESS:** {in_progress}")
    lines.append(f"- **Flagged as STALE:** {stale}")
    lines.append(f"- **Kept as OPEN:** {keep_open}")
    lines.append(f"- **Already completed:** {already_done}")
    lines.append("")
    lines.append("### After audit, the task board will show:")
    lines.append(f"- **OPEN tasks:** ~{keep_open + stale}")
    lines.append(f"- **IN_PROGRESS tasks:** ~{in_progress}")
    lines.append(f"- **DONE tasks:** ~{done + already_done}")
    lines.append(f"- **Decisions removed:** {deleted}")
    lines.append("")

    # Detail sections
    section_order = [
        Category.DELETE_DECISION,
        Category.DONE_ONESHOT,
        Category.DONE_SCHEDULING,
        Category.DONE_SEND,
        Category.DONE_CODE,
        Category.DONE_COMMITMENT,
        Category.DONE_EVIDENCE,
        Category.IN_PROGRESS,
        Category.STALE,
        Category.KEEP_OPEN,
        Category.KEEP_RECENT,
    ]

    for category in section_order:
        items = by_category.get(category, [])
        if not items:
            continue

        label = CATEGORY_LABELS[category]
        lines.append(f"## {label} ({len(items)})")
        lines.append("")

        # For large sections, show first 20 + summary
        show_items = items[:30] if len(items) > 30 else items
        is_truncated = len(items) > 30

        lines.append("| # | Date | Description | Owner | Deadline | Reason |")
        lines.append("|---|------|-------------|-------|----------|--------|")

        for task, reason in show_items:
            num = task.get("number", "?")
            d = format_date_short(task.get("action_date"))
            desc = (task.get("description") or "")[:80]
            owner = task.get("owner") or ""
            deadline = task.get("deadline") or ""
            lines.append(f"| {num} | {d} | {desc} | {owner} | {deadline} | {reason[:60]} |")

        if is_truncated:
            lines.append(f"| ... | ... | *({len(items) - 30} more items)* | ... | ... | ... |")

        lines.append("")

    report_text = "\n".join(lines) + "\n"

    if report_path:
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(report_text, encoding="utf-8")
        print(f"  Report written to: {report_path}")

    return report_text


# ---------------------------------------------------------------------------
# Apply changes
# ---------------------------------------------------------------------------

def build_updated_tasks(
    categorized: list[tuple[dict, str, str]],
    completed_tasks: list[dict],
) -> list[dict]:
    """Build the final task list for tracker regeneration.

    Returns items formatted for generate_tracker_file().
    """
    result = []

    for task, category, reason in categorized:
        # Skip decisions -- they're removed
        if category == Category.DELETE_DECISION:
            continue

        # Map category to status
        if category in (
            Category.DONE_ONESHOT, Category.DONE_SCHEDULING,
            Category.DONE_SEND, Category.DONE_CODE,
            Category.DONE_COMMITMENT, Category.DONE_EVIDENCE,
            Category.ALREADY_DONE,
        ):
            mapped_status = "DONE"
        elif category == Category.IN_PROGRESS:
            mapped_status = "IN_PROGRESS"
        elif category == Category.STALE:
            mapped_status = "TODO"  # Keep as open but flagged
        else:
            mapped_status = "TODO"

        result.append({
            "description": task.get("raw_description") or task.get("description", ""),
            "assignee": task.get("owner"),
            "deadline": task.get("deadline"),
            "status": task.get("status"),
            "confidence": None,
            "context": task.get("context"),
            "source_file": task.get("source") or "",
            "source_date": task.get("action_date"),
            "workstreams": [],
            "item_type": "action_item",
            "_mapped_status": mapped_status,
            "_mapped_priority": "NONE",
            "_audit_category": category,
            "_audit_reason": reason,
        })

    # Add existing completed tasks
    for task in completed_tasks:
        result.append({
            "description": task.get("description", ""),
            "assignee": task.get("owner"),
            "deadline": task.get("deadline"),
            "status": "COMPLETED",
            "confidence": None,
            "context": task.get("context"),
            "source_file": task.get("source_file") or "",
            "source_date": task.get("action_date"),
            "workstreams": [],
            "item_type": "action_item",
            "_mapped_status": "DONE",
            "_mapped_priority": "NONE",
        })

    return result


def generate_audited_tracker(
    tasks: list[dict],
    data_root: Path,
    total_audited: int,
    summary_count: int,
) -> None:
    """Write the updated analysis/trackers/action_items.md with correct statuses."""
    today_str = TODAY.isoformat()

    open_items = [t for t in tasks if t.get("_mapped_status") in ("TODO", "IN_PROGRESS")]
    likely_items = [t for t in tasks if t.get("_mapped_status") == "IN_REVIEW"]
    done_items = [t for t in tasks if t.get("_mapped_status") in ("DONE", "CANCELLED")]

    lines = []
    lines.append("# Action Items Tracker")
    lines.append("")
    lines.append(f"Last updated: {today_str} (audited from {total_audited} tasks across {summary_count} summaries)")
    lines.append("")
    lines.append("Items are grouped by status. [C] = commitment, [D] = decision follow-up.")
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
        src = source_display(task.get("source_file", ""))
        lines.append(f"| {i} | {d} | {desc} | In review | {src} |")

    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## COMPLETED")
    lines.append("")
    lines.append("| # | Date | Action | Completed | Notes | Source |")
    lines.append("|---|------|--------|-----------|-------|--------|")

    for i, task in enumerate(done_items, 1):
        d = format_date_short(task.get("source_date"))
        desc = (task.get("description") or "")[:120]
        completed_date = format_date_short(task.get("source_date"))
        notes = (task.get("_audit_reason") or task.get("context") or "")[:60]
        src = source_display(task.get("source_file", ""))
        lines.append(f"| {i} | {d} | {desc} | {completed_date} | {notes} | {src} |")

    tracker_path = data_root / "analysis" / "trackers" / "action_items.md"
    tracker_path.parent.mkdir(parents=True, exist_ok=True)
    tracker_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"  Tracker written: {tracker_path}")
    print(f"    OPEN: {len(open_items)}")
    print(f"    LIKELY COMPLETED: {len(likely_items)}")
    print(f"    COMPLETED: {len(done_items)}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

async def run_audit(
    data_root_str: str,
    db_url: str,
    dry_run: bool = True,
    verbose: bool = False,
) -> None:
    data_root = Path(data_root_str).resolve()
    tracker_path = data_root / "analysis" / "trackers" / "action_items.md"
    summaries_dir = data_root / "analysis" / "summaries"
    weekly_dir = data_root / "analysis" / "weekly"
    report_path = data_root / "analysis" / "trackers" / "task_audit_report.md"

    print("=" * 60)
    print("TASK STATUS AUDIT")
    print("=" * 60)
    print(f"  Data root:    {data_root}")
    print(f"  Mode:         {'DRY RUN' if dry_run else 'APPLY'}")
    print(f"  Date:         {TODAY}")
    print()

    # ---------------------------------------------------------------
    # Step 1: Load all data
    # ---------------------------------------------------------------
    print("[1/4] Loading data...")

    if not tracker_path.exists():
        print(f"  ERROR: Tracker not found: {tracker_path}")
        sys.exit(1)

    open_tasks = parse_open_tasks_raw(tracker_path)
    print(f"  Loaded {len(open_tasks)} OPEN tasks from tracker")

    # Also load existing completed tasks to preserve them
    all_parsed = parse_action_items(tracker_path)
    completed_tasks = [t for t in all_parsed if t.get("status") in ("COMPLETED", "LIKELY COMPLETED")]
    print(f"  Loaded {len(completed_tasks)} already-completed tasks")

    print("  Loading summaries for evidence search...")
    summaries = load_summaries_text(summaries_dir) if summaries_dir.is_dir() else []
    print(f"  Loaded {len(summaries)} summary files")

    weeklies = load_weekly_text(weekly_dir) if weekly_dir.is_dir() else []
    print(f"  Loaded {len(weeklies)} weekly report files")
    print()

    # ---------------------------------------------------------------
    # Step 2: Classify each task
    # ---------------------------------------------------------------
    print("[2/4] Classifying tasks...")

    categorized: list[tuple[dict, str, str]] = []
    for task in open_tasks:
        category, reason = classify_task(task, summaries, weeklies)
        categorized.append((task, category, reason))

    # Print summary
    counts: dict[str, int] = {}
    for _, category, _ in categorized:
        counts[category] = counts.get(category, 0) + 1

    print("  Classification results:")
    for cat in [
        Category.DELETE_DECISION, Category.DONE_ONESHOT, Category.DONE_SCHEDULING,
        Category.DONE_SEND, Category.DONE_CODE, Category.DONE_COMMITMENT,
        Category.DONE_EVIDENCE, Category.IN_PROGRESS, Category.STALE,
        Category.KEEP_OPEN, Category.KEEP_RECENT,
    ]:
        if cat in counts:
            print(f"    {CATEGORY_LABELS[cat]:45s} {counts[cat]:>5d}")

    total_done = sum(counts.get(c, 0) for c in [
        Category.DONE_ONESHOT, Category.DONE_SCHEDULING, Category.DONE_SEND,
        Category.DONE_CODE, Category.DONE_COMMITMENT, Category.DONE_EVIDENCE,
    ])
    total_deleted = counts.get(Category.DELETE_DECISION, 0)
    total_open = sum(counts.get(c, 0) for c in [Category.KEEP_OPEN, Category.KEEP_RECENT, Category.STALE])

    print()
    print(f"  TOTAL: {len(categorized)} tasks")
    print(f"    -> {total_deleted} decisions removed")
    print(f"    -> {total_done} auto-closed as DONE")
    print(f"    -> {counts.get(Category.IN_PROGRESS, 0)} set to IN_PROGRESS")
    print(f"    -> {total_open} remain OPEN")
    print()

    # ---------------------------------------------------------------
    # Step 3: Generate report
    # ---------------------------------------------------------------
    print("[3/4] Generating audit report...")
    report = generate_report(categorized, report_path)
    print()

    if dry_run:
        print("[DRY RUN] No changes applied. Review the report at:")
        print(f"  {report_path}")
        print()
        print("To apply changes, run with --apply instead of --dry-run")
        return

    # ---------------------------------------------------------------
    # Step 4: Apply changes
    # ---------------------------------------------------------------
    print("[4/4] Applying changes...")

    # Build updated task list
    updated_tasks = build_updated_tasks(categorized, completed_tasks)
    print(f"  Built {len(updated_tasks)} tasks for updated tracker")

    # Write updated tracker
    generate_audited_tracker(
        updated_tasks,
        data_root,
        total_audited=len(categorized),
        summary_count=len(summaries),
    )
    print()

    # Update database (lazy-import to avoid module-level DB dependency)
    print("  Attempting database update...")
    try:
        from sqlalchemy.ext.asyncio import AsyncSession as _AsyncSession
        from sqlalchemy.ext.asyncio import async_sessionmaker as _async_sessionmaker
        from sqlalchemy.ext.asyncio import create_async_engine as _create_async_engine
        from scripts.rebuild_tasks import (
            build_project_map as _build_project_map,
            clear_tasks_table as _clear_tasks_table,
            insert_tasks as _insert_tasks,
        )

        engine = _create_async_engine(db_url, echo=False)
        session_factory = _async_sessionmaker(engine, class_=_AsyncSession, expire_on_commit=False)

        async with session_factory() as session:
            project_map = await _build_project_map(session)
            await _clear_tasks_table(session, verbose=verbose)
            inserted = await _insert_tasks(session, updated_tasks, project_map, verbose=verbose)
            print(f"  Inserted {inserted} tasks into database")

        await engine.dispose()
    except (ImportError, Exception) as e:
        print(f"  [SKIP] Database update skipped: {e}")
        print("  The tracker file has been updated. To sync the database, run:")
        print("    python -m scripts.rebuild_tasks --data-root <path>")
        print("  or:")
        print("    python -m scripts.import_data --data-root <path>")

    print()
    print("=" * 60)
    print("AUDIT COMPLETE")
    print("=" * 60)
    print(f"  Decisions removed:   {total_deleted}")
    print(f"  Auto-closed (DONE):  {total_done}")
    print(f"  Set to IN_PROGRESS:  {counts.get(Category.IN_PROGRESS, 0)}")
    print(f"  Remaining OPEN:      {total_open}")
    print(f"  Report:              {report_path}")
    print(f"  Tracker:             {data_root / 'analysis' / 'trackers' / 'action_items.md'}")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Audit and reclassify task statuses")
    parser.add_argument(
        "--data-root", required=True,
        help="Path to the Icarus project root",
    )
    parser.add_argument(
        "--db-url", default=None,
        help="Database URL (default: $DATABASE_URL or local postgres)",
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Generate report only, don't change anything",
    )
    parser.add_argument(
        "--apply", action="store_true",
        help="Apply changes to DB and tracker",
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true",
        help="Print detailed progress",
    )
    args = parser.parse_args()

    if not args.dry_run and not args.apply:
        print("ERROR: Must specify either --dry-run or --apply")
        sys.exit(1)

    db_url = (
        args.db_url
        or os.environ.get("DATABASE_URL")
        or "postgresql+asyncpg://icarus:icarus_local@localhost:5432/icarus"
    )

    asyncio.run(run_audit(
        args.data_root,
        db_url,
        dry_run=args.dry_run,
        verbose=args.verbose,
    ))
