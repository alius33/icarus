"""Write-back service for open thread changes.

Syncs open threads from the UI back to context/open_threads.md.
"""

import re
from pathlib import Path

from app.services.markdown_table import get_data_root, read_file, write_file

FILEPATH = "context/open_threads.md"
VALID_STATUSES = ["OPEN", "WATCHING", "CLOSED"]


def _find_section_boundaries(lines: list[str]) -> dict[str, tuple[int, int]]:
    """Find start/end line indices for each ## STATUS section.

    Returns dict like {"OPEN": (start, end), "WATCHING": (start, end), ...}
    where start is the line of the ## heading and end is the line before the
    next ## heading (or end of file).
    """
    sections: dict[str, tuple[int, int]] = {}
    current_section = None
    current_start = 0

    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith("## "):
            # Close previous section
            if current_section:
                sections[current_section] = (current_start, i - 1)

            heading = stripped[3:].strip().upper()
            for status in VALID_STATUSES:
                if status in heading:
                    current_section = status
                    current_start = i
                    break
            else:
                current_section = None

    # Close last section
    if current_section:
        sections[current_section] = (current_start, len(lines) - 1)

    return sections


def _find_entry_in_section(
    lines: list[str], section_start: int, section_end: int, number: int
) -> tuple[int, int] | None:
    """Find the start/end line indices of a ### N. Title entry within a section.

    Returns (entry_start, entry_end) or None.
    """
    entry_start = None
    pattern = re.compile(rf"^###\s+{number}\.\s+")

    for i in range(section_start, section_end + 1):
        stripped = lines[i].strip()

        if entry_start is not None:
            # We're inside the entry — look for the next heading
            if stripped.startswith("### ") or stripped.startswith("## "):
                return (entry_start, i - 1)
        else:
            if pattern.match(stripped):
                entry_start = i

    if entry_start is not None:
        return (entry_start, section_end)

    return None


def _find_entry_any_section(
    lines: list[str], sections: dict[str, tuple[int, int]], number: int
) -> tuple[str, int, int] | None:
    """Find an entry by number across all sections.

    Returns (status, entry_start, entry_end) or None.
    """
    for status, (sec_start, sec_end) in sections.items():
        result = _find_entry_in_section(lines, sec_start, sec_end, number)
        if result:
            return (status, result[0], result[1])
    return None


def _build_entry_block(
    number: int,
    title: str,
    first_raised: str | None = None,
    context: str | None = None,
    question: str | None = None,
    why_it_matters: str | None = None,
    resolution: str | None = None,
    resolution_date: str | None = None,
) -> list[str]:
    """Construct the markdown lines for a single thread entry."""
    block = [f"### {number}. {title}"]

    if first_raised:
        block.append(f"- **First raised:** {first_raised}")
    if context:
        block.append(f"- **Context:** {context}")
    if question:
        block.append(f"- **Question:** {question}")
    if why_it_matters:
        block.append(f"- **Why it matters:** {why_it_matters}")
    if resolution_date:
        block.append(f"- **Resolution date:** {resolution_date}")
    if resolution:
        block.append(f"- **Resolution:** {resolution}")

    block.append("")  # trailing blank line
    return block


def _extract_entry_lines(lines: list[str], start: int, end: int) -> list[str]:
    """Extract lines for an entry, trimming trailing blank lines."""
    entry = lines[start:end + 1]
    while entry and entry[-1].strip() == "":
        entry.pop()
    return entry


def move_thread(
    number: int,
    old_status: str,
    new_status: str,
    resolution: str | None = None,
) -> bool:
    """Move a thread entry from one status section to another."""
    try:
        filepath = get_data_root() / FILEPATH
        lines = read_file(filepath)
        if lines is None:
            return False

        sections = _find_section_boundaries(lines)
        if old_status not in sections or new_status not in sections:
            return False

        # Find the entry in old section
        old_sec = sections[old_status]
        entry_bounds = _find_entry_in_section(lines, old_sec[0], old_sec[1], number)
        if entry_bounds is None:
            # Try finding in any section (in case status is stale)
            result = _find_entry_any_section(lines, sections, number)
            if result is None:
                return False
            _, entry_bounds_start, entry_bounds_end = result
            entry_bounds = (entry_bounds_start, entry_bounds_end)

        entry_start, entry_end = entry_bounds

        # Extract the entry content
        entry_lines = _extract_entry_lines(lines, entry_start, entry_end)

        # Add resolution if moving to CLOSED and resolution provided
        if new_status == "CLOSED" and resolution:
            # Check if resolution already exists
            has_resolution = any("**Resolution:**" in l for l in entry_lines)
            if not has_resolution:
                entry_lines.append(f"- **Resolution:** {resolution}")

        # Remove from old position
        del lines[entry_start:entry_end + 1]

        # Recalculate sections after removal
        sections = _find_section_boundaries(lines)
        if new_status not in sections:
            return False

        # Insert at the end of the new section (before the next ## or EOF)
        new_sec = sections[new_status]
        insert_at = new_sec[1] + 1

        # Ensure blank line before entry
        if insert_at > 0 and lines[insert_at - 1].strip() != "":
            lines.insert(insert_at, "")
            insert_at += 1

        for i, line in enumerate(entry_lines):
            lines.insert(insert_at + i, line)

        # Ensure blank line after entry
        after_entry = insert_at + len(entry_lines)
        if after_entry < len(lines) and lines[after_entry].strip() != "":
            lines.insert(after_entry, "")

        return write_file(filepath, lines)

    except Exception:
        return False


def append_thread(
    number: int,
    title: str,
    status: str = "OPEN",
    first_raised: str | None = None,
    context: str | None = None,
    question: str | None = None,
    why_it_matters: str | None = None,
) -> bool:
    """Append a new thread entry to the appropriate status section."""
    try:
        filepath = get_data_root() / FILEPATH
        lines = read_file(filepath)
        if lines is None:
            return False

        sections = _find_section_boundaries(lines)
        target_status = status.upper() if status else "OPEN"
        if target_status not in sections:
            return False

        sec_start, sec_end = sections[target_status]

        entry_block = _build_entry_block(
            number=number,
            title=title,
            first_raised=first_raised,
            context=context,
            question=question,
            why_it_matters=why_it_matters,
        )

        insert_at = sec_end + 1

        # Ensure blank line before entry
        if insert_at > 0 and lines[insert_at - 1].strip() != "":
            lines.insert(insert_at, "")
            insert_at += 1

        for i, line in enumerate(entry_block):
            lines.insert(insert_at + i, line)

        return write_file(filepath, lines)

    except Exception:
        return False


def update_thread_fields(
    number: int,
    current_status: str,
    title: str | None = None,
    context: str | None = None,
    question: str | None = None,
    why_it_matters: str | None = None,
    resolution: str | None = None,
    first_raised: str | None = None,
) -> bool:
    """Update fields within an existing thread entry in-place."""
    try:
        filepath = get_data_root() / FILEPATH
        lines = read_file(filepath)
        if lines is None:
            return False

        sections = _find_section_boundaries(lines)

        # Find entry
        result = _find_entry_any_section(lines, sections, number)
        if result is None:
            return False

        _, entry_start, entry_end = result

        # Update the heading if title changed
        if title is not None:
            heading_pattern = re.compile(rf"^###\s+{number}\.\s+")
            if heading_pattern.match(lines[entry_start].strip()):
                lines[entry_start] = f"### {number}. {title}"

        # Update bullet fields
        field_map = {
            "First raised": first_raised,
            "Context": context,
            "Question": question,
            "Why it matters": why_it_matters,
            "Resolution": resolution,
        }

        for field_name, new_value in field_map.items():
            if new_value is None:
                continue

            found = False
            for i in range(entry_start + 1, entry_end + 1):
                if f"**{field_name}:**" in lines[i]:
                    lines[i] = f"- **{field_name}:** {new_value}"
                    found = True
                    break

            if not found and new_value:
                # Add the field before the trailing blank line
                insert_pos = entry_end
                while insert_pos > entry_start and lines[insert_pos].strip() == "":
                    insert_pos -= 1
                lines.insert(insert_pos + 1, f"- **{field_name}:** {new_value}")

        return write_file(filepath, lines)

    except Exception:
        return False


def remove_thread(number: int, status: str | None = None) -> bool:
    """Remove a thread entry entirely."""
    try:
        filepath = get_data_root() / FILEPATH
        lines = read_file(filepath)
        if lines is None:
            return False

        sections = _find_section_boundaries(lines)

        result = _find_entry_any_section(lines, sections, number)
        if result is None:
            return False

        _, entry_start, entry_end = result

        # Also remove trailing blank line if present
        if entry_end + 1 < len(lines) and lines[entry_end + 1].strip() == "":
            entry_end += 1

        del lines[entry_start:entry_end + 1]
        return write_file(filepath, lines)

    except Exception:
        return False
