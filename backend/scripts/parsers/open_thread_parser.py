"""
Parser for context/open_threads.md

Handles:
  - ## OPEN, ## WATCHING, ## CLOSED top-level sections
  - ### N. Title  numbered entries within each section
  - Bullet points: **First raised:**, **Context:**, **Question:**,
    **Why it matters:**, **Status:**
"""

import hashlib
import re
from pathlib import Path


def _compute_file_hash(filepath: Path) -> str:
    """Compute SHA256 hash of file contents."""
    sha256 = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            sha256.update(chunk)
    return sha256.hexdigest()


def _extract_bullet_value(lines: list[str], key: str) -> str | None:
    """Extract a value from bullet points matching **Key:** pattern.

    Handles multi-line values by collecting lines until the next bullet
    or heading.
    """
    collecting = False
    collected: list[str] = []
    pattern_lower = f"**{key.lower()}:**"

    for line in lines:
        stripped = line.strip()
        # Check if this line starts a new bullet with a different key
        if stripped.startswith("- **") and collecting:
            break
        if pattern_lower in stripped.lower():
            # Extract the value after the key
            lower_stripped = stripped.lower()
            idx = lower_stripped.index(pattern_lower)
            real_idx = idx + len(pattern_lower)
            after = stripped[real_idx:].strip()
            if after:
                collected.append(after)
            collecting = True
            continue
        if collecting and stripped:
            collected.append(stripped)

    result = " ".join(collected).strip()
    return result if result else None


def parse_open_threads(filepath: Path) -> list[dict]:
    """Parse open_threads.md into a list of thread dicts.

    Args:
        filepath: Path to open_threads.md

    Returns:
        List of dicts with: number, title, status, first_raised, context,
        question, why_it_matters, source_file, file_hash.
    """
    content = filepath.read_text(encoding="utf-8", errors="replace")
    file_hash = _compute_file_hash(filepath)
    source_file = str(filepath.relative_to(filepath.parent.parent))
    lines = content.splitlines()

    threads = []
    current_status = None
    current_number = None
    current_title = None
    current_entry_lines: list[str] = []

    def _flush_entry():
        nonlocal current_number, current_title, current_entry_lines
        if current_number is not None and current_title and current_status:
            first_raised = _extract_bullet_value(current_entry_lines, "First raised")
            ctx = _extract_bullet_value(current_entry_lines, "Context")
            question = _extract_bullet_value(current_entry_lines, "Question")
            why_it_matters = _extract_bullet_value(current_entry_lines, "Why it matters")

            threads.append({
                "number": current_number,
                "title": current_title,
                "status": current_status,
                "first_raised": first_raised,
                "context": ctx,
                "question": question,
                "why_it_matters": why_it_matters,
                "source_file": source_file,
                "file_hash": file_hash,
            })
        current_number = None
        current_title = None
        current_entry_lines = []

    for line in lines:
        stripped = line.strip()

        # Detect status section headings
        if stripped == "## OPEN":
            _flush_entry()
            current_status = "OPEN"
            continue
        elif stripped == "## WATCHING":
            _flush_entry()
            current_status = "WATCHING"
            continue
        elif stripped == "## CLOSED":
            _flush_entry()
            current_status = "CLOSED"
            continue
        elif stripped.startswith("## ") and current_status is not None:
            # Another ## heading that's not a status section ends parsing
            _flush_entry()
            current_status = None
            continue

        if current_status is None:
            continue

        # Detect entry headings: ### N. Title or ### Title
        entry_match = re.match(r'^###\s+(\d+)\.\s+(.+)$', stripped)
        if entry_match:
            _flush_entry()
            current_number = int(entry_match.group(1))
            current_title = entry_match.group(2).strip()
            continue

        # Also match ### Title without a number (for WATCHING/CLOSED)
        entry_match_no_num = re.match(r'^###\s+(.+)$', stripped)
        if entry_match_no_num and current_number is None and not entry_match:
            _flush_entry()
            # Assign a sequential number based on threads already parsed in this section
            section_count = sum(1 for t in threads if t["status"] == current_status)
            current_number = section_count + 1
            current_title = entry_match_no_num.group(1).strip()
            continue

        # Accumulate content lines for the current entry
        if current_number is not None:
            current_entry_lines.append(line)

    # Flush the last entry
    _flush_entry()

    return threads
