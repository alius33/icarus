"""Write-back service for decision changes.

Syncs decisions from the UI back to context/decisions.md.
"""

import re
from datetime import date

from app.services.markdown_table import (
    add_column_to_table,
    append_row_to_table,
    build_table_row,
    escape_pipe,
    find_row_by_cell_value,
    find_table_boundaries,
    get_data_root,
    read_file,
    remove_row_from_table,
    update_cell_in_row,
    write_file,
)

FILEPATH = "context/decisions.md"
TABLE_MARKERS = ["#", "Date", "Decision"]

# Column indices in the 5-column format
COL_NUMBER = 0
COL_DATE = 1
COL_DECISION = 2
COL_RATIONALE = 3
COL_KEY_PEOPLE = 4
COL_STATUS = 5  # Added by writeback if missing


MONTH_NAMES = [
    "", "Jan", "Feb", "Mar", "Apr", "May", "Jun",
    "Jul", "Aug", "Sep", "Oct", "Nov", "Dec",
]


def _format_date_short(d: date) -> str:
    """Format date as 'D Mon' (e.g., '7 Jan') to match existing decisions.md format."""
    return f"{d.day} {MONTH_NAMES[d.month]}"


def _has_status_column(lines: list[str], header_idx: int) -> bool:
    """Check if the table already has a Status column."""
    header = lines[header_idx]
    return "Status" in header


def _ensure_status_column(
    lines: list[str], boundaries: tuple[int, int, int]
) -> tuple[list[str], tuple[int, int, int]]:
    """If the table lacks a Status column, add one."""
    header_idx, separator_idx, last_data_idx = boundaries
    if _has_status_column(lines, header_idx):
        return lines, boundaries

    lines = add_column_to_table(
        lines, header_idx, separator_idx, last_data_idx,
        column_name="Status", default_value="made",
    )
    return lines, boundaries


def update_decision_status(number: int, new_status: str) -> bool:
    """Update execution_status for decision #number in decisions.md."""
    try:
        filepath = get_data_root() / FILEPATH
        lines = read_file(filepath)
        if lines is None:
            return False

        boundaries = find_table_boundaries(lines, TABLE_MARKERS)
        if boundaries is None:
            return False

        lines, boundaries = _ensure_status_column(lines, boundaries)
        header_idx, separator_idx, last_data_idx = boundaries

        row_idx = find_row_by_cell_value(
            lines, separator_idx + 1, last_data_idx, COL_NUMBER, str(number)
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


def append_decision(
    number: int,
    decision_date: date | None,
    decision: str,
    rationale: str | None,
    key_people: list[str] | None,
    execution_status: str = "made",
) -> bool:
    """Append a new decision row to the table."""
    try:
        filepath = get_data_root() / FILEPATH
        lines = read_file(filepath)
        if lines is None:
            return False

        boundaries = find_table_boundaries(lines, TABLE_MARKERS)
        if boundaries is None:
            return False

        lines, boundaries = _ensure_status_column(lines, boundaries)
        _, _, last_data_idx = boundaries

        date_str = _format_date_short(decision_date) if decision_date else ""
        people_str = ", ".join(key_people) if key_people else ""

        cells = [
            str(number),
            date_str,
            escape_pipe(decision or ""),
            escape_pipe(rationale or ""),
            escape_pipe(people_str),
            execution_status or "made",
        ]

        lines = append_row_to_table(lines, last_data_idx, cells)
        return write_file(filepath, lines)

    except Exception:
        return False


def remove_decision(number: int) -> bool:
    """Remove a decision row from the table."""
    try:
        filepath = get_data_root() / FILEPATH
        lines = read_file(filepath)
        if lines is None:
            return False

        boundaries = find_table_boundaries(lines, TABLE_MARKERS)
        if boundaries is None:
            return False

        _, separator_idx, last_data_idx = boundaries

        row_idx = find_row_by_cell_value(
            lines, separator_idx + 1, last_data_idx, COL_NUMBER, str(number)
        )
        if row_idx is None:
            return False

        lines = remove_row_from_table(lines, row_idx)
        return write_file(filepath, lines)

    except Exception:
        return False
