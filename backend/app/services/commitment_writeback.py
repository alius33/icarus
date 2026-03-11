"""Write-back service for commitment changes.

Syncs commitments from the UI back to analysis/trackers/commitments.md.
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

FILEPATH = "analysis/trackers/commitments.md"
TABLE_MARKERS = ["Date", "Person", "Commitment"]

# Column indices
COL_DATE = 0
COL_PERSON = 1
COL_COMMITMENT = 2
COL_DEADLINE = 3
COL_CONDITION = 4
COL_STATUS = 5
COL_MEETING = 6
COL_CONFIDENCE = 7


def _find_commitment_row(
    lines: list[str], start: int, end: int,
    person: str, commitment_text: str,
) -> int | None:
    """Find a commitment row by matching person + commitment substring."""
    try:
        person_lower = person.lower().strip()
        commit_lower = commitment_text.lower().strip()[:40]  # first 40 chars

        for i in range(start, end + 1):
            if "|" not in lines[i]:
                continue
            cells = parse_table_row(lines[i])
            if len(cells) < 3:
                continue
            if (person_lower in cells[COL_PERSON].lower()
                    and commit_lower in cells[COL_COMMITMENT].lower()):
                return i
        return None
    except Exception:
        return None


def update_commitment_status(
    person: str, commitment_text: str, new_status: str,
) -> bool:
    """Update the Status column for a matching commitment."""
    try:
        filepath = get_data_root() / FILEPATH
        lines = read_file(filepath)
        if lines is None:
            return False

        boundaries = find_table_boundaries(lines, TABLE_MARKERS)
        if boundaries is None:
            return False

        _, separator_idx, last_data_idx = boundaries

        row_idx = _find_commitment_row(
            lines, separator_idx + 1, last_data_idx, person, commitment_text
        )
        if row_idx is None:
            return False

        updated = update_cell_in_row(lines[row_idx], COL_STATUS, new_status)
        if updated is None:
            return False

        lines[row_idx] = updated
        return write_file(filepath, lines)

    except Exception:
        return False


def append_commitment(
    date_made: date | None,
    person: str,
    commitment: str,
    deadline_text: str | None = None,
    condition: str | None = None,
    status: str = "pending",
    meeting: str | None = None,
    confidence: str | None = None,
) -> bool:
    """Append a new commitment row to the table."""
    try:
        filepath = get_data_root() / FILEPATH
        lines = read_file(filepath)
        if lines is None:
            return False

        boundaries = find_table_boundaries(lines, TABLE_MARKERS)
        if boundaries is None:
            return False

        _, _, last_data_idx = boundaries

        date_str = str(date_made) if date_made else ""

        cells = [
            date_str,
            escape_pipe(person or ""),
            escape_pipe(commitment or ""),
            escape_pipe(deadline_text or ""),
            escape_pipe(condition or "None"),
            status or "pending",
            escape_pipe(meeting or ""),
            confidence or "Medium",
        ]

        lines = append_row_to_table(lines, last_data_idx, cells)
        return write_file(filepath, lines)

    except Exception:
        return False


def remove_commitment(person: str, commitment_text: str) -> bool:
    """Remove a commitment row from the table."""
    try:
        filepath = get_data_root() / FILEPATH
        lines = read_file(filepath)
        if lines is None:
            return False

        boundaries = find_table_boundaries(lines, TABLE_MARKERS)
        if boundaries is None:
            return False

        _, separator_idx, last_data_idx = boundaries

        row_idx = _find_commitment_row(
            lines, separator_idx + 1, last_data_idx, person, commitment_text
        )
        if row_idx is None:
            return False

        lines = remove_row_from_table(lines, row_idx)
        return write_file(filepath, lines)

    except Exception:
        return False
