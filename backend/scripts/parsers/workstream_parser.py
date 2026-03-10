"""
Parser for context/workstreams.md

Handles:
  - ## WS1: Name  sections (6 total)
  - **Lead:** and **Status:** fields
  - Markdown tables for milestones (Date | Milestone)
  - Sections: Current State, Feature Backlog, Key Risks, Next Steps
"""

import hashlib
import re
from datetime import datetime
from pathlib import Path

# Month abbreviation to number
MONTH_MAP = {
    "jan": 1, "january": 1,
    "feb": 2, "february": 2,
    "mar": 3, "march": 3,
    "apr": 4, "april": 4,
    "may": 5,
    "jun": 6, "june": 6,
    "jul": 7, "july": 7,
    "aug": 8, "august": 8,
    "sep": 9, "september": 9,
    "oct": 10, "october": 10,
    "nov": 11, "november": 11,
    "dec": 12, "december": 12,
}


def _compute_file_hash(filepath: Path) -> str:
    """Compute SHA256 hash of file contents."""
    sha256 = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            sha256.update(chunk)
    return sha256.hexdigest()


def _parse_milestone_date(date_str: str) -> datetime | None:
    """Parse milestone dates.

    Formats:
      - "7 Jan" / "14 Jan" => 2026
      - "Christmas 2025" => 25 Dec 2025
      - "2 Feb" => 2026
    """
    date_str = date_str.strip()

    # Handle "Christmas YYYY"
    christmas_match = re.match(r'Christmas\s+(\d{4})', date_str, re.IGNORECASE)
    if christmas_match:
        year = int(christmas_match.group(1))
        return datetime(year, 12, 25).date()

    # Handle "D Mon" or "DD Mon" format
    match = re.match(r'^(\d{1,2})\s+([A-Za-z]+)$', date_str)
    if match:
        day = int(match.group(1))
        month_str = match.group(2).lower()
        month = MONTH_MAP.get(month_str) or MONTH_MAP.get(month_str[:3])
        if month:
            # Assume 2026 for Jan+, 2025 for Dec (Christmas already handled)
            year = 2025 if month == 12 else 2026
            try:
                return datetime(year, month, day).date()
            except ValueError:
                return None

    # Handle "D Mon YYYY" format
    match = re.match(r'^(\d{1,2})\s+([A-Za-z]+)\s+(\d{4})$', date_str)
    if match:
        day = int(match.group(1))
        month_str = match.group(2).lower()
        year = int(match.group(3))
        month = MONTH_MAP.get(month_str) or MONTH_MAP.get(month_str[:3])
        if month:
            try:
                return datetime(year, month, day).date()
            except ValueError:
                return None

    return None


def _extract_field(lines: list[str], field_name: str) -> str | None:
    """Extract a **Field:** value from a list of lines."""
    for line in lines:
        stripped = line.strip()
        pattern = f"**{field_name}:**"
        if pattern in stripped:
            idx = stripped.index(pattern)
            after = stripped[idx + len(pattern):].strip()
            return after if after else None
    return None


def _extract_section_content(lines: list[str], section_name: str) -> str | None:
    """Extract all content under a ### Section heading until the next heading."""
    in_section = False
    section_lines = []

    for line in lines:
        stripped = line.strip()
        if stripped.startswith("### ") and section_name.lower() in stripped.lower():
            in_section = True
            continue
        if in_section:
            if stripped.startswith("### ") or stripped.startswith("## "):
                break
            section_lines.append(line)

    content = "\n".join(section_lines).strip()
    return content if content else None


def _extract_bullet_section(lines: list[str], section_name: str) -> str | None:
    """Extract bullet-point content under a ### section heading."""
    return _extract_section_content(lines, section_name)


def parse_workstreams(filepath: Path) -> tuple[list[dict], list[dict]]:
    """Parse workstreams.md into workstreams and milestones.

    Args:
        filepath: Path to workstreams.md

    Returns:
        Tuple of (workstreams, milestones) where:
        - workstreams: list of dicts with code, name, lead, status,
          description, current_state, next_steps, risks, source_file, file_hash
        - milestones: list of dicts with workstream_code, milestone_date,
          description, source_file
    """
    content = filepath.read_text(encoding="utf-8", errors="replace")
    file_hash = _compute_file_hash(filepath)
    source_file = str(filepath.relative_to(filepath.parent.parent))
    lines = content.splitlines()

    workstreams = []
    milestones = []

    # Split content into workstream blocks at ## WS headings
    ws_blocks: list[tuple[str, str, list[str]]] = []
    current_code = None
    current_name = None
    current_lines: list[str] = []

    for line in lines:
        stripped = line.strip()
        ws_match = re.match(r'^##\s+(WS\d+):\s+(.+)$', stripped)
        if ws_match:
            if current_code:
                ws_blocks.append((current_code, current_name, current_lines))
            current_code = ws_match.group(1)
            current_name = ws_match.group(2).strip()
            current_lines = []
            continue
        if current_code:
            current_lines.append(line)

    # Don't forget the last block
    if current_code:
        ws_blocks.append((current_code, current_name, current_lines))

    for code, name, block_lines in ws_blocks:
        lead = _extract_field(block_lines, "Lead")
        status = _extract_field(block_lines, "Status") or "UNKNOWN"

        # Build description from all content between **Status:** and ### sections
        description_parts = []
        past_status = False
        for bl in block_lines:
            stripped_bl = bl.strip()
            if "**Status:**" in stripped_bl:
                past_status = True
                continue
            if past_status:
                if stripped_bl.startswith("### "):
                    break
                if stripped_bl and not stripped_bl.startswith("---"):
                    description_parts.append(stripped_bl)
        description = "\n".join(description_parts).strip() if description_parts else None

        current_state = _extract_section_content(block_lines, "Current State")
        next_steps = _extract_section_content(block_lines, "Next Steps")
        # Also check for "Next step needed" in bullet points
        if not next_steps:
            for bl in block_lines:
                if "**Next step needed:**" in bl:
                    idx = bl.index("**Next step needed:**")
                    next_steps = bl[idx + len("**Next step needed:**"):].strip()
                    break

        risks = _extract_section_content(block_lines, "Key Risks")

        workstreams.append({
            "code": code,
            "name": name,
            "lead": lead,
            "status": status,
            "description": description,
            "current_state": current_state,
            "next_steps": next_steps,
            "risks": risks,
            "source_file": source_file,
            "file_hash": file_hash,
        })

        # Parse milestone tables (### Timeline sections with Date | Milestone)
        in_milestone_table = False
        for bl in block_lines:
            stripped_bl = bl.strip()
            if stripped_bl.startswith("### Timeline"):
                in_milestone_table = True
                continue
            if in_milestone_table:
                # Stop at next heading
                if stripped_bl.startswith("### ") or stripped_bl.startswith("## "):
                    in_milestone_table = False
                    continue
                # Skip header row and separator
                if stripped_bl.startswith("| Date") or stripped_bl.startswith("|---"):
                    continue
                # Parse data rows
                if stripped_bl.startswith("|"):
                    cols = [c.strip() for c in stripped_bl.split("|")]
                    cols = [c for c in cols if c != ""]
                    if len(cols) >= 2:
                        date_str = cols[0]
                        milestone_desc = cols[1]
                        milestone_date = _parse_milestone_date(date_str)
                        milestones.append({
                            "workstream_code": code,
                            "milestone_date": milestone_date,
                            "description": milestone_desc,
                            "source_file": source_file,
                        })

    return workstreams, milestones
