"""
Parser for contradictions and information gaps from
analysis/trackers/contradiction_tracker.md

Expected format:
## Contradictions

| Date | Type | Person | Statement_A | Date_A | Statement_B | Date_B | Severity | Resolution | Confidence |
|------|------|--------|-------------|--------|-------------|--------|----------|------------|------------|
| 2026-02-10 | reversal | Richard | "We'll use Azure" | 2026-01-15 | "AWS is the way" | 2026-02-10 | HIGH | unresolved | HIGH |

## Information Gaps

| Date | Gap_Description | Expected_Source | Last_Mentioned | Meetings_Absent | Severity |
|------|-----------------|-----------------|----------------|-----------------|----------|
| 2026-02-10 | Token cost breakdown | Finance | 2026-01-20 | 3 | MEDIUM |
"""

import re
from datetime import date


def parse_contradictions(content: str) -> list[dict]:
    """Parse contradiction tracker markdown into a list of dicts.

    Handles two table sections: Contradictions and Information Gaps.
    Returns a combined list with entry_kind='contradiction' or entry_kind='gap'.
    """
    results = []

    lines = content.strip().split("\n")
    in_table = False
    current_section = None

    for line in lines:
        stripped = line.strip()

        # Skip empty lines
        if not stripped:
            continue

        # Detect section headers
        if stripped.startswith("#"):
            lower = stripped.lower()
            if "gap" in lower:
                current_section = "gap"
            elif "contradiction" in lower:
                current_section = "contradiction"
            in_table = False
            continue

        # Detect table header for contradictions
        if ("|" in stripped and "Date" in stripped
                and "Type" in stripped and "Person" in stripped):
            in_table = True
            current_section = "contradiction"
            continue

        # Detect table header for information gaps
        if ("|" in stripped and "Date" in stripped
                and "Gap_Description" in stripped):
            in_table = True
            current_section = "gap"
            continue

        # Skip separator line
        if in_table and re.match(r"^\|[\s\-|]+\|$", stripped):
            continue

        # Parse table rows
        if in_table and stripped.startswith("|"):
            cells = [c.strip() for c in stripped.split("|")[1:-1]]

            if current_section == "contradiction" and len(cells) >= 3:
                entry = _parse_contradiction_row(cells)
                if entry:
                    results.append(entry)
            elif current_section == "gap" and len(cells) >= 2:
                entry = _parse_gap_row(cells)
                if entry:
                    results.append(entry)
        elif in_table and not stripped.startswith("|"):
            in_table = False

    return results


def _parse_contradiction_row(cells: list[str]) -> dict | None:
    """Parse a single contradiction table row."""
    date_str = cells[0].strip()
    contradiction_type = cells[1].strip().lower()
    person = cells[2].strip() if len(cells) > 2 else None
    statement_a = cells[3].strip().strip('"') if len(cells) > 3 else None
    date_a_str = cells[4].strip() if len(cells) > 4 else None
    statement_b = cells[5].strip().strip('"') if len(cells) > 5 else None
    date_b_str = cells[6].strip() if len(cells) > 6 else None
    severity = cells[7].strip().upper() if len(cells) > 7 else None
    resolution = cells[8].strip().lower() if len(cells) > 8 else "unresolved"
    confidence = cells[9].strip().upper() if len(cells) > 9 else None

    parsed_date = None
    if date_str:
        try:
            parsed_date = date.fromisoformat(date_str)
        except ValueError:
            pass

    parsed_date_a = None
    if date_a_str:
        try:
            parsed_date_a = date.fromisoformat(date_a_str)
        except ValueError:
            parsed_date_a = None

    parsed_date_b = None
    if date_b_str:
        try:
            parsed_date_b = date.fromisoformat(date_b_str)
        except ValueError:
            parsed_date_b = None

    valid_types = {
        "reversal", "contradiction", "quiet_drop",
        "scope_shift", "reframing",
    }
    if contradiction_type not in valid_types:
        contradiction_type = "contradiction"

    valid_severities = {"CRITICAL", "HIGH", "MEDIUM", "LOW"}
    if severity and severity not in valid_severities:
        severity = None

    valid_resolutions = {"unresolved", "acknowledged", "explained", "superseded"}
    if resolution and resolution not in valid_resolutions:
        resolution = "unresolved"

    valid_confidences = {"HIGH", "MEDIUM", "LOW"}
    if confidence and confidence not in valid_confidences:
        confidence = None

    return {
        "date": parsed_date,
        "contradiction_type": contradiction_type,
        "person": person if person else None,
        "statement_a": statement_a if statement_a else None,
        "date_a": parsed_date_a,
        "statement_b": statement_b if statement_b else None,
        "date_b": parsed_date_b,
        "severity": severity,
        "resolution": resolution,
        "confidence": confidence,
        "entry_kind": "contradiction",
    }


def _parse_gap_row(cells: list[str]) -> dict | None:
    """Parse a single information gap table row."""
    date_str = cells[0].strip()
    gap_description = cells[1].strip() if len(cells) > 1 else None
    expected_source = cells[2].strip() if len(cells) > 2 else None
    last_mentioned_str = cells[3].strip() if len(cells) > 3 else None
    meetings_absent_str = cells[4].strip() if len(cells) > 4 else None
    severity = cells[5].strip().upper() if len(cells) > 5 else None

    parsed_date = None
    if date_str:
        try:
            parsed_date = date.fromisoformat(date_str)
        except ValueError:
            pass

    parsed_last_mentioned = None
    if last_mentioned_str:
        try:
            parsed_last_mentioned = date.fromisoformat(last_mentioned_str)
        except ValueError:
            parsed_last_mentioned = None

    meetings_absent = None
    if meetings_absent_str:
        try:
            meetings_absent = int(meetings_absent_str)
        except ValueError:
            pass

    valid_severities = {"CRITICAL", "HIGH", "MEDIUM", "LOW"}
    if severity and severity not in valid_severities:
        severity = None

    return {
        "date": parsed_date,
        "contradiction_type": "information_gap",
        "person": None,
        "statement_a": None,
        "date_a": None,
        "statement_b": None,
        "date_b": None,
        "severity": severity,
        "resolution": "unresolved",
        "confidence": None,
        "gap_description": gap_description if gap_description else None,
        "expected_source": expected_source if expected_source else None,
        "last_mentioned": parsed_last_mentioned,
        "meetings_absent": meetings_absent,
        "entry_kind": "gap",
    }
