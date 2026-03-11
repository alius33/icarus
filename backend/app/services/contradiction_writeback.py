"""Write-back service for contradiction and information gap changes.

Syncs contradictions from the UI back to analysis/trackers/contradictions.md.
"""

from datetime import date

from app.services.markdown_table import (
    append_row_to_table,
    escape_pipe,
    find_table_boundaries,
    get_data_root,
    parse_table_row,
    read_file,
    remove_row_from_table,
    update_cell_in_row,
    write_file,
)

FILEPATH = "analysis/trackers/contradictions.md"

# Contradictions table markers and columns
CONTRADICTION_MARKERS = ["Date", "Type", "Person", "Statement_A"]
C_COL_DATE = 0
C_COL_TYPE = 1
C_COL_PERSON = 2
C_COL_STATEMENT_A = 3
C_COL_DATE_A = 4
C_COL_STATEMENT_B = 5
C_COL_DATE_B = 6
C_COL_SEVERITY = 7
C_COL_RESOLUTION = 8
C_COL_CONFIDENCE = 9

# Gaps table markers and columns
GAP_MARKERS = ["Date", "Gap_Description", "Expected_Source"]
G_COL_DATE = 0
G_COL_DESCRIPTION = 1
G_COL_SOURCE = 2
G_COL_LAST_MENTIONED = 3
G_COL_MEETINGS_ABSENT = 4
G_COL_SEVERITY = 5


def _find_contradiction_row(
    lines: list[str], start: int, end: int,
    person: str, statement_fragment: str,
) -> int | None:
    """Find a contradiction row by matching person + statement_a substring."""
    try:
        person_lower = person.lower().strip()
        frag_lower = statement_fragment.lower().strip()[:30]

        for i in range(start, end + 1):
            if "|" not in lines[i]:
                continue
            cells = parse_table_row(lines[i])
            if len(cells) < 4:
                continue
            if (person_lower in cells[C_COL_PERSON].lower()
                    and frag_lower in cells[C_COL_STATEMENT_A].lower()):
                return i
        return None
    except Exception:
        return None


def _find_gap_row(
    lines: list[str], start: int, end: int,
    description_fragment: str,
) -> int | None:
    """Find a gap row by matching gap description substring."""
    try:
        frag_lower = description_fragment.lower().strip()[:30]

        for i in range(start, end + 1):
            if "|" not in lines[i]:
                continue
            cells = parse_table_row(lines[i])
            if len(cells) < 2:
                continue
            if frag_lower in cells[G_COL_DESCRIPTION].lower():
                return i
        return None
    except Exception:
        return None


def update_contradiction_resolution(
    person: str, statement_fragment: str, new_resolution: str,
) -> bool:
    """Update the Resolution column for a matching contradiction."""
    try:
        filepath = get_data_root() / FILEPATH
        lines = read_file(filepath)
        if lines is None:
            return False

        boundaries = find_table_boundaries(lines, CONTRADICTION_MARKERS)
        if boundaries is None:
            return False

        _, separator_idx, last_data_idx = boundaries

        row_idx = _find_contradiction_row(
            lines, separator_idx + 1, last_data_idx, person, statement_fragment
        )
        if row_idx is None:
            return False

        updated = update_cell_in_row(
            lines[row_idx], C_COL_RESOLUTION, escape_pipe(new_resolution)
        )
        if updated is None:
            return False

        lines[row_idx] = updated
        return write_file(filepath, lines)

    except Exception:
        return False


def append_contradiction(
    entry_date: date | None,
    contradiction_type: str | None = None,
    person: str | None = None,
    statement_a: str | None = None,
    date_a: date | None = None,
    statement_b: str | None = None,
    date_b: date | None = None,
    severity: str | None = None,
    resolution: str | None = None,
    confidence: str | None = None,
) -> bool:
    """Append a new contradiction row to the Contradictions table."""
    try:
        filepath = get_data_root() / FILEPATH
        lines = read_file(filepath)
        if lines is None:
            return False

        boundaries = find_table_boundaries(lines, CONTRADICTION_MARKERS)
        if boundaries is None:
            return False

        _, _, last_data_idx = boundaries

        cells = [
            str(entry_date) if entry_date else str(date.today()),
            escape_pipe(contradiction_type or ""),
            escape_pipe(person or ""),
            escape_pipe(statement_a or ""),
            str(date_a) if date_a else "",
            escape_pipe(statement_b or ""),
            str(date_b) if date_b else "",
            severity or "MEDIUM",
            escape_pipe(resolution or ""),
            confidence or "Medium",
        ]

        lines = append_row_to_table(lines, last_data_idx, cells)
        return write_file(filepath, lines)

    except Exception:
        return False


def append_gap(
    entry_date: date | None,
    gap_description: str | None = None,
    expected_source: str | None = None,
    last_mentioned: date | None = None,
    meetings_absent: int | None = None,
    severity: str | None = None,
) -> bool:
    """Append a new gap row to the Information Gaps table."""
    try:
        filepath = get_data_root() / FILEPATH
        lines = read_file(filepath)
        if lines is None:
            return False

        boundaries = find_table_boundaries(lines, GAP_MARKERS)
        if boundaries is None:
            return False

        _, _, last_data_idx = boundaries

        cells = [
            str(entry_date) if entry_date else str(date.today()),
            escape_pipe(gap_description or ""),
            escape_pipe(expected_source or ""),
            str(last_mentioned) if last_mentioned else str(date.today()),
            str(meetings_absent) if meetings_absent else "1",
            severity or "MEDIUM",
        ]

        lines = append_row_to_table(lines, last_data_idx, cells)
        return write_file(filepath, lines)

    except Exception:
        return False


def remove_contradiction(person: str, statement_fragment: str) -> bool:
    """Remove a contradiction row by matching person + statement_a."""
    try:
        filepath = get_data_root() / FILEPATH
        lines = read_file(filepath)
        if lines is None:
            return False

        boundaries = find_table_boundaries(lines, CONTRADICTION_MARKERS)
        if boundaries is None:
            return False

        _, separator_idx, last_data_idx = boundaries

        row_idx = _find_contradiction_row(
            lines, separator_idx + 1, last_data_idx, person, statement_fragment
        )
        if row_idx is None:
            return False

        lines = remove_row_from_table(lines, row_idx)
        return write_file(filepath, lines)

    except Exception:
        return False


def remove_gap(description_fragment: str) -> bool:
    """Remove a gap row by matching gap_description."""
    try:
        filepath = get_data_root() / FILEPATH
        lines = read_file(filepath)
        if lines is None:
            return False

        boundaries = find_table_boundaries(lines, GAP_MARKERS)
        if boundaries is None:
            return False

        _, separator_idx, last_data_idx = boundaries

        row_idx = _find_gap_row(
            lines, separator_idx + 1, last_data_idx, description_fragment
        )
        if row_idx is None:
            return False

        lines = remove_row_from_table(lines, row_idx)
        return write_file(filepath, lines)

    except Exception:
        return False
