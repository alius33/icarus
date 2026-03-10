"""
Parser for context/decisions.md

Parses a markdown table with columns:
  # | Date | Decision | Rationale | Key People

Dates are in formats like "7 Jan", "13 Jan", "5 Feb" — all in 2026.
Key People is a comma-separated list.
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

DECISION_YEAR = 2026


def _compute_file_hash(filepath: Path) -> str:
    """Compute SHA256 hash of file contents."""
    sha256 = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            sha256.update(chunk)
    return sha256.hexdigest()


def _parse_short_date(date_str: str) -> datetime | None:
    """Parse dates like '7 Jan', '13 Jan', '5 Feb' into date objects.

    Assumes all dates are in DECISION_YEAR (2026).
    """
    date_str = date_str.strip()
    match = re.match(r'^(\d{1,2})\s+([A-Za-z]+)$', date_str)
    if match:
        day = int(match.group(1))
        month_str = match.group(2).lower()[:3]
        month = MONTH_MAP.get(month_str)
        if month:
            try:
                return datetime(DECISION_YEAR, month, day).date()
            except ValueError:
                return None
    return None


def _parse_key_people(people_str: str) -> list[str]:
    """Parse comma-separated list of people names."""
    if not people_str or not people_str.strip():
        return []
    return [p.strip() for p in people_str.split(",") if p.strip()]


def parse_decisions(filepath: Path) -> list[dict]:
    """Parse decisions.md into a list of decision dicts.

    Args:
        filepath: Path to decisions.md

    Returns:
        List of dicts with: number, decision_date, decision, rationale,
        key_people (list), source_file, file_hash.
    """
    content = filepath.read_text(encoding="utf-8", errors="replace")
    file_hash = _compute_file_hash(filepath)
    source_file = str(filepath.relative_to(filepath.parent.parent))
    lines = content.splitlines()

    decisions = []
    in_table = False

    for line in lines:
        stripped = line.strip()

        # Detect table header row
        if stripped.startswith("| #") or stripped.startswith("|#"):
            in_table = True
            continue

        # Skip separator rows
        if stripped.startswith("|---") or stripped.startswith("| ---"):
            continue

        # Parse table data rows
        if in_table and stripped.startswith("|"):
            cols = [c.strip() for c in stripped.split("|")]
            # Remove empty strings from leading/trailing pipes
            cols = [c for c in cols if c != ""]
            if len(cols) < 4:
                continue

            try:
                number = int(cols[0].strip())
            except (ValueError, IndexError):
                continue

            date_str = cols[1].strip() if len(cols) > 1 else ""
            decision_text = cols[2].strip() if len(cols) > 2 else ""
            rationale = cols[3].strip() if len(cols) > 3 else ""
            people_str = cols[4].strip() if len(cols) > 4 else ""

            decision_date = _parse_short_date(date_str)
            key_people = _parse_key_people(people_str)

            decisions.append({
                "number": number,
                "decision_date": decision_date,
                "decision": decision_text,
                "rationale": rationale if rationale else None,
                "key_people": key_people,
                "source_file": source_file,
                "file_hash": file_hash,
            })

        # Stop if we hit a non-table line after the table started
        elif in_table and stripped and not stripped.startswith("|"):
            in_table = False

    return decisions
