"""Write-back service for risk entry changes.

Syncs risk entries from the UI back to analysis/trackers/risk_register.md.
"""

from datetime import date

from app.services.markdown_table import (
    append_row_to_table,
    escape_pipe,
    find_row_by_cell_value,
    find_table_boundaries,
    get_data_root,
    read_file,
    remove_row_from_table,
    update_cell_in_row,
    write_file,
)

FILEPATH = "analysis/trackers/risk_register.md"
TABLE_MARKERS = ["Date", "Risk_ID", "Title"]

# Column indices
COL_DATE = 0
COL_RISK_ID = 1
COL_TITLE = 2
COL_DESCRIPTION = 3
COL_CATEGORY = 4
COL_SEVERITY = 5
COL_TRAJECTORY = 6
COL_SOURCE_TYPE = 7
COL_OWNER = 8
COL_MITIGATION = 9
COL_LAST_REVIEWED = 10
COL_MEETINGS_MENTIONED = 11
COL_CONFIDENCE = 12


def update_risk_fields(
    risk_id: str,
    severity: str | None = None,
    trajectory: str | None = None,
    owner: str | None = None,
    mitigation: str | None = None,
    last_reviewed: date | None = None,
    title: str | None = None,
    description: str | None = None,
) -> bool:
    """Update field(s) for a risk entry identified by risk_id."""
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
            lines, separator_idx + 1, last_data_idx, COL_RISK_ID, risk_id
        )
        if row_idx is None:
            return False

        updates = {
            COL_TITLE: title,
            COL_DESCRIPTION: description,
            COL_SEVERITY: severity,
            COL_TRAJECTORY: trajectory,
            COL_OWNER: owner,
            COL_MITIGATION: mitigation,
            COL_LAST_REVIEWED: str(last_reviewed) if last_reviewed else None,
        }

        for col_idx, value in updates.items():
            if value is not None:
                updated = update_cell_in_row(lines[row_idx], col_idx, escape_pipe(value))
                if updated is not None:
                    lines[row_idx] = updated

        return write_file(filepath, lines)

    except Exception:
        return False


def append_risk_entry(
    risk_id: str,
    entry_date: date | None,
    title: str,
    description: str | None = None,
    category: str | None = None,
    severity: str = "MEDIUM",
    trajectory: str | None = None,
    source_type: str | None = None,
    owner: str | None = None,
    mitigation: str | None = None,
) -> bool:
    """Append a new risk entry row to the table."""
    try:
        filepath = get_data_root() / FILEPATH
        lines = read_file(filepath)
        if lines is None:
            return False

        boundaries = find_table_boundaries(lines, TABLE_MARKERS)
        if boundaries is None:
            return False

        _, _, last_data_idx = boundaries

        today = str(date.today())

        cells = [
            str(entry_date) if entry_date else today,
            risk_id,
            escape_pipe(title or ""),
            escape_pipe(description or ""),
            escape_pipe(category or ""),
            severity or "MEDIUM",
            trajectory or "New",
            source_type or "Explicit",
            escape_pipe(owner or ""),
            escape_pipe(mitigation or ""),
            today,  # Last_Reviewed
            "1",  # Meetings_Mentioned
            "Medium",  # Confidence
        ]

        lines = append_row_to_table(lines, last_data_idx, cells)
        return write_file(filepath, lines)

    except Exception:
        return False


def remove_risk_entry(risk_id: str) -> bool:
    """Remove a risk entry row from the table."""
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
            lines, separator_idx + 1, last_data_idx, COL_RISK_ID, risk_id
        )
        if row_idx is None:
            return False

        lines = remove_row_from_table(lines, row_idx)
        return write_file(filepath, lines)

    except Exception:
        return False
