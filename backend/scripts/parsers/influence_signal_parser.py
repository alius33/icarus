"""
Parser for influence signals from analysis/trackers/influence_tracker.md

Expected format:
## Influence Signals

| Date | Person | Influence_Type | Direction | Target_Person | Topic | Evidence | Strength | Confidence |
|------|--------|----------------|-----------|---------------|-------|----------|----------|------------|
| 2026-02-10 | Richard | proposal_adopted | outbound | Josh | CLARA scope | "Let's keep it simple" | HIGH | HIGH |

## Coalitions

| Date | Coalition_Name | Members | Issue | Alignment |
|------|----------------|---------|-------|-----------|
| 2026-02-10 | Platform advocates | Richard, Ben | CLARA direction | aligned |
"""

import re
from datetime import date


def parse_influence_signals(content: str) -> list[dict]:
    """Parse influence tracker markdown into a list of dicts.

    Handles two table sections: Influence Signals and Coalitions.
    Returns a combined list with entry_kind='influence' or entry_kind='coalition'.
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
            if "coalition" in lower:
                current_section = "coalition"
            elif "influence" in lower:
                current_section = "influence"
            in_table = False
            continue

        # Detect table header for influence signals
        if ("|" in stripped and "Date" in stripped
                and "Person" in stripped and "Influence_Type" in stripped):
            in_table = True
            current_section = "influence"
            continue

        # Detect table header for coalitions
        if ("|" in stripped and "Date" in stripped
                and "Coalition_Name" in stripped):
            in_table = True
            current_section = "coalition"
            continue

        # Skip separator line
        if in_table and re.match(r"^\|[\s\-|]+\|$", stripped):
            continue

        # Parse table rows
        if in_table and stripped.startswith("|"):
            cells = [c.strip() for c in stripped.split("|")[1:-1]]

            if current_section == "influence" and len(cells) >= 3:
                entry = _parse_influence_row(cells)
                if entry:
                    results.append(entry)
            elif current_section == "coalition" and len(cells) >= 3:
                entry = _parse_coalition_row(cells)
                if entry:
                    results.append(entry)
        elif in_table and not stripped.startswith("|"):
            in_table = False

    return results


def _parse_influence_row(cells: list[str]) -> dict | None:
    """Parse a single influence signal table row."""
    date_str = cells[0].strip()
    person = cells[1].strip()
    influence_type = cells[2].strip().lower()
    direction = cells[3].strip().lower() if len(cells) > 3 else None
    target_person = cells[4].strip() if len(cells) > 4 else None
    topic = cells[5].strip() if len(cells) > 5 else None
    evidence = cells[6].strip().strip('"') if len(cells) > 6 else None
    strength = cells[7].strip().upper() if len(cells) > 7 else None
    confidence = cells[8].strip().upper() if len(cells) > 8 else None

    parsed_date = None
    if date_str:
        try:
            parsed_date = date.fromisoformat(date_str)
        except ValueError:
            pass

    valid_types = {
        "proposal_adopted", "deferred_to", "interrupted",
        "final_say", "bridging", "blocked",
    }
    if influence_type not in valid_types:
        influence_type = "bridging"

    valid_directions = {"outbound", "inbound"}
    if direction and direction not in valid_directions:
        direction = None

    valid_strengths = {"HIGH", "MEDIUM", "LOW"}
    if strength and strength not in valid_strengths:
        strength = None

    valid_confidences = {"HIGH", "MEDIUM", "LOW"}
    if confidence and confidence not in valid_confidences:
        confidence = None

    return {
        "date": parsed_date,
        "person": person,
        "influence_type": influence_type,
        "direction": direction,
        "target_person": target_person if target_person else None,
        "topic": topic if topic else None,
        "evidence": evidence if evidence else None,
        "strength": strength,
        "confidence": confidence,
        "entry_kind": "influence",
    }


def _parse_coalition_row(cells: list[str]) -> dict | None:
    """Parse a single coalition table row."""
    date_str = cells[0].strip()
    coalition_name = cells[1].strip()
    members = cells[2].strip() if len(cells) > 2 else None
    issue = cells[3].strip() if len(cells) > 3 else None
    alignment = cells[4].strip().lower() if len(cells) > 4 else None

    parsed_date = None
    if date_str:
        try:
            parsed_date = date.fromisoformat(date_str)
        except ValueError:
            pass

    return {
        "date": parsed_date,
        "person": coalition_name,
        "influence_type": "coalition",
        "direction": None,
        "target_person": None,
        "topic": issue if issue else None,
        "evidence": None,
        "strength": None,
        "confidence": None,
        "coalition_name": coalition_name,
        "coalition_members": members if members else None,
        "alignment": alignment if alignment else None,
        "entry_kind": "coalition",
    }
