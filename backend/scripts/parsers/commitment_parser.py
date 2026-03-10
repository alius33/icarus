"""
Parser for commitments from analysis/trackers/commitments.md

Expected format:
## Commitments Tracker

| Date | Person | Commitment | Deadline | Type | Condition | Status |
|------|--------|------------|----------|------|-----------|--------|
| 2026-02-10 | Azmain | Finish CLARA data quality fix | by Friday | date_resolved | | pending |
"""

import re
from datetime import date, timedelta


def parse_commitments(content: str) -> list[dict]:
    """Parse commitments tracker markdown into a list of dicts."""
    results = []

    lines = content.strip().split("\n")
    in_table = False

    for line in lines:
        stripped = line.strip()

        if not stripped or stripped.startswith("#"):
            continue

        # Detect table header
        if "|" in stripped and "Person" in stripped and "Commitment" in stripped:
            in_table = True
            continue

        # Skip separator line
        if in_table and re.match(r"^\|[\s\-|]+\|$", stripped):
            continue

        # Parse table rows
        if in_table and stripped.startswith("|"):
            cells = [c.strip() for c in stripped.split("|")[1:-1]]
            if len(cells) >= 3:
                date_str = cells[0].strip() if len(cells) > 0 else ""
                person = cells[1].strip() if len(cells) > 1 else ""
                commitment = cells[2].strip() if len(cells) > 2 else ""
                deadline_text = cells[3].strip() if len(cells) > 3 else ""
                deadline_type = cells[4].strip() if len(cells) > 4 else "none"
                condition = cells[5].strip() if len(cells) > 5 else ""
                status = cells[6].strip() if len(cells) > 6 else "pending"

                parsed_date = None
                if date_str:
                    try:
                        parsed_date = date.fromisoformat(date_str)
                    except ValueError:
                        pass

                deadline_resolved = _resolve_deadline(deadline_text, parsed_date)

                valid_statuses = {"pending", "fulfilled", "broken", "formalised", "conditional"}
                if status not in valid_statuses:
                    status = "pending"

                valid_types = {"date_resolved", "event_relative", "conditional", "none"}
                if deadline_type not in valid_types:
                    deadline_type = "none"

                results.append({
                    "person": person,
                    "commitment": commitment,
                    "date_made": parsed_date,
                    "deadline_text": deadline_text or None,
                    "deadline_resolved": deadline_resolved,
                    "deadline_type": deadline_type,
                    "condition": condition or None,
                    "status": status,
                })
        elif in_table and not stripped.startswith("|"):
            in_table = False

    return results


def _resolve_deadline(text: str, reference_date: date | None) -> date | None:
    """Attempt to resolve relative deadline text to an actual date."""
    if not text:
        return None

    # Try ISO format first
    try:
        return date.fromisoformat(text)
    except ValueError:
        pass

    if not reference_date:
        return None

    text_lower = text.lower().strip()

    # Common patterns
    if "by friday" in text_lower or "this friday" in text_lower:
        days_until_friday = (4 - reference_date.weekday()) % 7
        if days_until_friday == 0:
            days_until_friday = 7
        return reference_date + timedelta(days=days_until_friday)

    if "next week" in text_lower:
        days_until_monday = (7 - reference_date.weekday()) % 7
        if days_until_monday == 0:
            days_until_monday = 7
        return reference_date + timedelta(days=days_until_monday + 4)  # Friday of next week

    if "end of week" in text_lower or "eow" in text_lower:
        days_until_friday = (4 - reference_date.weekday()) % 7
        return reference_date + timedelta(days=days_until_friday)

    if "end of month" in text_lower or "eom" in text_lower:
        if reference_date.month == 12:
            return date(reference_date.year + 1, 1, 1) - timedelta(days=1)
        return date(reference_date.year, reference_date.month + 1, 1) - timedelta(days=1)

    return None
