"""Shared markdown table manipulation utilities.

All functions follow the writeback contract:
  - Return appropriate values on success, None on failure
  - Never raise exceptions
  - Use settings.DATA_ROOT for file paths
"""

import re
from pathlib import Path

from app.config import settings


def get_data_root() -> Path:
    return Path(settings.DATA_ROOT) if hasattr(settings, "DATA_ROOT") else Path(".")


def read_file(filepath: Path) -> list[str] | None:
    """Read a markdown file, returning lines or None if not found."""
    try:
        if not filepath.exists():
            return None
        content = filepath.read_text(encoding="utf-8")
        return content.splitlines()
    except Exception:
        return None


def write_file(filepath: Path, lines: list[str]) -> bool:
    """Write lines back to file with trailing newline. Returns True on success."""
    try:
        filepath.write_text("\n".join(lines) + "\n", encoding="utf-8")
        return True
    except Exception:
        return False


def find_table_boundaries(
    lines: list[str], header_markers: list[str]
) -> tuple[int, int, int] | None:
    """Find the header row, separator row, and last data row of a table.

    Args:
        lines: All lines of the file.
        header_markers: Strings that must appear in the header row.

    Returns:
        (header_idx, separator_idx, last_data_idx) or None if not found.
    """
    try:
        for i, line in enumerate(lines):
            if "|" not in line:
                continue
            # Check if all markers appear in this line
            if all(m in line for m in header_markers):
                # Next line should be the separator (|---|...)
                if i + 1 < len(lines) and re.match(r"^\|[\s\-|]+\|$", lines[i + 1].strip()):
                    separator_idx = i + 1
                    # Find last data row
                    last_data = separator_idx
                    for j in range(separator_idx + 1, len(lines)):
                        stripped = lines[j].strip()
                        if stripped.startswith("|") and not re.match(r"^\|[\s\-|]+\|$", stripped):
                            last_data = j
                        else:
                            break
                    return (i, separator_idx, last_data)
        return None
    except Exception:
        return None


def parse_table_row(line: str) -> list[str]:
    """Split a pipe-delimited table row into cell values (stripped)."""
    parts = line.split("|")
    # Remove empty first and last elements from leading/trailing pipes
    if parts and parts[0].strip() == "":
        parts = parts[1:]
    if parts and parts[-1].strip() == "":
        parts = parts[:-1]
    return [p.strip() for p in parts]


def build_table_row(cells: list[str]) -> str:
    """Construct a pipe-delimited table row from cell values."""
    inner = " | ".join(cells)
    return f"| {inner} |"


def update_cell_in_row(line: str, column_index: int, new_value: str) -> str | None:
    """Replace a specific column's value in a table row, preserving pipe formatting."""
    try:
        parts = line.split("|")
        # Account for leading empty element from leading pipe
        actual_idx = column_index + 1  # +1 for leading empty element
        if actual_idx >= len(parts) - 1:  # -1 for trailing empty element
            return None
        parts[actual_idx] = f" {new_value} "
        return "|".join(parts)
    except Exception:
        return None


def find_row_by_cell_value(
    lines: list[str],
    start_line: int,
    end_line: int,
    column_index: int,
    value: str,
    exact: bool = True,
) -> int | None:
    """Find the line index of a row where column_index matches value."""
    try:
        for i in range(start_line, end_line + 1):
            line = lines[i]
            if "|" not in line:
                continue
            cells = parse_table_row(line)
            if column_index >= len(cells):
                continue
            cell_val = cells[column_index].strip()
            if exact:
                if cell_val == value:
                    return i
            else:
                if value.lower() in cell_val.lower():
                    return i
        return None
    except Exception:
        return None


def append_row_to_table(lines: list[str], after_line: int, cells: list[str]) -> list[str]:
    """Insert a new row after the given line index. Returns modified lines."""
    new_row = build_table_row(cells)
    lines.insert(after_line + 1, new_row)
    return lines


def remove_row_from_table(lines: list[str], row_line: int) -> list[str]:
    """Remove a table row at the given line index. Returns modified lines."""
    if 0 <= row_line < len(lines):
        lines.pop(row_line)
    return lines


def add_column_to_table(
    lines: list[str],
    header_idx: int,
    separator_idx: int,
    last_data_idx: int,
    column_name: str,
    default_value: str = "",
) -> list[str]:
    """Add a new column to an existing table (header + separator + all data rows)."""
    try:
        # Add to header
        lines[header_idx] = lines[header_idx].rstrip()
        if lines[header_idx].endswith("|"):
            lines[header_idx] = lines[header_idx][:-1] + f" {column_name} |"
        else:
            lines[header_idx] += f" | {column_name} |"

        # Add to separator
        lines[separator_idx] = lines[separator_idx].rstrip()
        if lines[separator_idx].endswith("|"):
            lines[separator_idx] = lines[separator_idx][:-1] + "------|"
        else:
            lines[separator_idx] += "------|"

        # Add to all data rows
        for i in range(separator_idx + 1, last_data_idx + 1):
            if "|" in lines[i]:
                lines[i] = lines[i].rstrip()
                if lines[i].endswith("|"):
                    lines[i] = lines[i][:-1] + f" {default_value} |"
                else:
                    lines[i] += f" | {default_value} |"

        return lines
    except Exception:
        return lines


def escape_pipe(text: str) -> str:
    """Escape pipe characters in cell values."""
    if text is None:
        return ""
    return str(text).replace("|", "\\|")
