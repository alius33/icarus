"""
Parser for analysis/trackers/action_items.md

Handles three sections:
  - ## OPEN  — table with # | Date | Action | Owner | Deadline | Context
  - ## LIKELY COMPLETED — table with # | Date | Action | Likely Status
  - ## COMPLETED — table with # | Date | Action | Completion Date

Number column can be numeric ("1", "10") or alphabetic ("A", "B").
Date column can be "23 Feb", "9 Feb", "Ongoing", etc.
"""

import hashlib
import re
from datetime import datetime
from pathlib import Path

# Month abbreviation to number
MONTH_MAP = {
    "jan": 1, "feb": 2, "mar": 3, "apr": 4,
    "may": 5, "jun": 6, "jul": 7, "aug": 8,
    "sep": 9, "oct": 10, "nov": 11, "dec": 12,
}

ACTION_YEAR = 2026


def _compute_file_hash(filepath: Path) -> str:
    """Compute SHA256 hash of file contents."""
    sha256 = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            sha256.update(chunk)
    return sha256.hexdigest()


def _parse_action_date(date_str: str) -> datetime | None:
    """Parse dates like '23 Feb', '9 Feb', 'Ongoing' into date objects."""
    date_str = date_str.strip()
    if not date_str or date_str.lower() == "ongoing":
        return None

    match = re.match(r'^(\d{1,2})\s+([A-Za-z]+)$', date_str)
    if match:
        day = int(match.group(1))
        month_str = match.group(2).lower()[:3]
        month = MONTH_MAP.get(month_str)
        if month:
            try:
                return datetime(ACTION_YEAR, month, day).date()
            except ValueError:
                return None
    return None


def parse_action_items(filepath: Path) -> list[dict]:
    """Parse action_items.md into a list of action item dicts.

    Args:
        filepath: Path to action_items.md

    Returns:
        List of dicts with: number (str), action_date, description, owner,
        deadline, context, status, source_file, file_hash.
    """
    content = filepath.read_text(encoding="utf-8", errors="replace")
    file_hash = _compute_file_hash(filepath)
    source_file = str(filepath.relative_to(filepath.parent.parent))
    lines = content.splitlines()

    items = []
    current_section = None
    in_table = False

    for line in lines:
        stripped = line.strip()

        # Detect section headings
        if stripped.startswith("## OPEN"):
            current_section = "OPEN"
            in_table = False
            continue
        elif stripped.startswith("## LIKELY COMPLETED"):
            current_section = "LIKELY COMPLETED"
            in_table = False
            continue
        elif stripped.startswith("## COMPLETED"):
            current_section = "COMPLETED"
            in_table = False
            continue
        elif stripped.startswith("## "):
            current_section = None
            in_table = False
            continue

        if current_section is None:
            continue

        # Detect table header
        if stripped.startswith("| #"):
            in_table = True
            continue
        # Skip separator rows
        if stripped.startswith("|---") or stripped.startswith("| ---"):
            continue

        # Parse table data rows
        if in_table and stripped.startswith("|"):
            cols = [c.strip() for c in stripped.split("|")]
            cols = [c for c in cols if c != ""]

            if len(cols) < 3:
                continue

            number = cols[0].strip()
            date_str = cols[1].strip()
            action_date = _parse_action_date(date_str)

            if current_section == "OPEN":
                description = cols[2].strip() if len(cols) > 2 else ""
                owner = cols[3].strip() if len(cols) > 3 else None
                deadline = cols[4].strip() if len(cols) > 4 else None
                context = cols[5].strip() if len(cols) > 5 else None
                status = "OPEN"
            elif current_section == "LIKELY COMPLETED":
                description = cols[2].strip() if len(cols) > 2 else ""
                owner = None
                deadline = None
                likely_status = cols[3].strip() if len(cols) > 3 else None
                context = likely_status  # Store likely status in context field
                status = "LIKELY COMPLETED"
            elif current_section == "COMPLETED":
                description = cols[2].strip() if len(cols) > 2 else ""
                owner = None
                deadline = None
                completion_info = cols[3].strip() if len(cols) > 3 else None
                notes = cols[4].strip() if len(cols) > 4 else None
                # Combine completion info and notes into context
                if completion_info and notes:
                    context = f"{completion_info} | {notes}"
                else:
                    context = completion_info or notes
                status = "COMPLETED"
            else:
                continue

            items.append({
                "number": number,
                "action_date": action_date,
                "description": description,
                "owner": owner,
                "deadline": deadline,
                "context": context,
                "status": status,
                "source_file": source_file,
                "file_hash": file_hash,
            })

        # Non-table line while in_table means table ended
        elif in_table and stripped and not stripped.startswith("|") and not stripped.startswith("("):
            in_table = False

    return items
