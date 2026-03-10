"""
Parser for analysis/summaries/*.md files.

Reads all summary markdown files and extracts three types of actionable items:
  - Action Items (from ## Action Items table)
  - Commitments  (from ## Commitments Made table — four format variants)
  - Decision follow-ups (from ## Decisions Made — bullet or table format)

Each extracted item is returned as a plain dict for easy JSON serialisation.
"""

import re
import sys
from datetime import date
from pathlib import Path


# ---------------------------------------------------------------------------
# Data shape — returned as plain dicts, documented here for reference
# ---------------------------------------------------------------------------
#
# {
#     "item_type":    "action_item" | "commitment" | "decision_followup",
#     "description":  str,
#     "assignee":     str | None,
#     "deadline":     str | None,
#     "status":       str,           # Open, In progress, Complete, Done
#     "confidence":   str | None,    # HIGH, MEDIUM, LOW
#     "source_file":  str,           # relative path
#     "source_date":  date | None,
#     "workstreams":  list[str],     # ["WS2", "WS6"]
#     "attendees":    list[str],
#     "context":      str | None,
# }


# ---------------------------------------------------------------------------
# Header parsing
# ---------------------------------------------------------------------------

_DATE_RE = re.compile(r"\*\*Date:\*\*\s*(\d{4}-\d{2}-\d{2})")
_ATTENDEES_RE = re.compile(r"\*\*Attendees:\*\*\s*(.+)", re.IGNORECASE)
_WORKSTREAMS_RE = re.compile(r"\*\*Workstreams\s+touched:\*\*\s*(.+)", re.IGNORECASE)
_WS_CODE_RE = re.compile(r"WS\d+")


def parse_summary_header(content: str) -> dict:
    """Parse the header block: Date, Attendees, Workstreams touched.

    Returns a dict with keys: source_date, attendees, workstreams.
    """
    source_date: date | None = None
    attendees: list[str] = []
    workstreams: list[str] = []

    for line in content.splitlines()[:20]:  # header is always near the top
        m = _DATE_RE.search(line)
        if m:
            try:
                source_date = date.fromisoformat(m.group(1))
            except ValueError:
                pass

        m = _ATTENDEES_RE.search(line)
        if m:
            raw = m.group(1)
            # Split on commas, strip parenthetical notes
            parts = re.split(r",(?![^(]*\))", raw)
            for part in parts:
                name = re.sub(r"\s*\(.*?\)\s*", "", part).strip()
                if name:
                    attendees.append(name)

        m = _WORKSTREAMS_RE.search(line)
        if m:
            workstreams = _WS_CODE_RE.findall(m.group(1))

    return {
        "source_date": source_date,
        "attendees": attendees,
        "workstreams": workstreams,
    }


# ---------------------------------------------------------------------------
# Section extraction helpers
# ---------------------------------------------------------------------------

def _extract_section(content: str, heading: str) -> str:
    """Return all text between ``## <heading>`` and the next ``## `` heading."""
    pattern = re.compile(
        rf"^##\s+{re.escape(heading)}\s*$",
        re.MULTILINE,
    )
    m = pattern.search(content)
    if not m:
        return ""
    start = m.end()
    # Find next heading at same or higher level
    next_heading = re.search(r"^## ", content[start:], re.MULTILINE)
    if next_heading:
        return content[start:start + next_heading.start()]
    return content[start:]


def _parse_table_rows(section: str) -> tuple[list[str], list[list[str]]]:
    """Parse a markdown table from a section into headers + data rows.

    Returns (headers, rows) where each row is a list of cell strings.
    Skips separator rows.  Tolerates missing trailing pipe.
    """
    headers: list[str] = []
    rows: list[list[str]] = []
    found_header = False

    for line in section.splitlines():
        stripped = line.strip()
        if not stripped.startswith("|"):
            if found_header and stripped:
                # Non-table line after table started — table ended
                break
            continue

        cells = [c.strip() for c in stripped.split("|")]
        # Remove empty strings from leading/trailing pipes
        if cells and cells[0] == "":
            cells = cells[1:]
        if cells and cells[-1] == "":
            cells = cells[:-1]

        if not cells:
            continue

        # Separator row (e.g. |---|---|)
        if all(re.match(r"^-+:?$|^:?-+:?$|^:?-+$", c) for c in cells):
            continue

        if not found_header:
            headers = [h.strip() for h in cells]
            found_header = True
        else:
            rows.append([c.strip() for c in cells])

    return headers, rows


def _normalise_confidence(raw: str | None) -> str | None:
    """Normalise confidence to uppercase (HIGH, MEDIUM, LOW) or None."""
    if not raw:
        return None
    cleaned = raw.strip().upper()
    # Handle cases like "High -- BenVH committed" → "HIGH"
    cleaned = re.split(r"\s*[-–—]", cleaned)[0].strip()
    if cleaned in ("HIGH", "MEDIUM", "LOW"):
        return cleaned
    return raw.strip() if raw.strip() else None


def _normalise_status(raw: str | None) -> str:
    """Normalise status to a canonical value."""
    if not raw:
        return "Open"
    cleaned = raw.strip().lower()
    # Strip trailing qualifications like "-- fix already written"
    cleaned = re.split(r"\s*[-–—]", cleaned)[0].strip()
    # Strip parenthetical qualifiers like "(in session)"
    cleaned = re.sub(r"\s*\(.*?\)\s*", "", cleaned).strip()
    mapping = {
        "open": "Open",
        "in progress": "In progress",
        "in-progress": "In progress",
        "complete": "Complete",
        "completed": "Complete",
        "done": "Done",
        "closed": "Complete",
    }
    return mapping.get(cleaned, raw.strip())


# ---------------------------------------------------------------------------
# Action Items
# ---------------------------------------------------------------------------

def extract_action_items(content: str) -> list[dict]:
    """Extract from ## Action Items section.

    Handles three header layouts:
      A: Action | Owner | Deadline | Status | Confidence
      B: Action | Owner | Deadline | Confidence           (no Status col)
      C: Action | Owner | Deadline | Confidence | Status  (swapped)
    """
    section = _extract_section(content, "Action Items")
    if not section:
        return []

    headers, rows = _parse_table_rows(section)
    if not headers:
        return []

    # Build a column index by normalised header name
    col = {h.lower(): i for i, h in enumerate(headers)}

    action_idx = col.get("action", 0)
    owner_idx = col.get("owner", 1)
    deadline_idx = col.get("deadline", 2)
    status_idx = col.get("status")
    confidence_idx = col.get("confidence")

    items: list[dict] = []
    for cells in rows:
        if len(cells) <= action_idx:
            continue

        description = cells[action_idx] if action_idx < len(cells) else ""
        if not description:
            continue

        owner = cells[owner_idx] if owner_idx < len(cells) else None
        deadline = cells[deadline_idx] if deadline_idx < len(cells) else None

        raw_status = cells[status_idx] if status_idx is not None and status_idx < len(cells) else None
        raw_confidence = cells[confidence_idx] if confidence_idx is not None and confidence_idx < len(cells) else None

        items.append({
            "item_type": "action_item",
            "description": description,
            "assignee": owner if owner else None,
            "deadline": deadline if deadline else None,
            "status": _normalise_status(raw_status),
            "confidence": _normalise_confidence(raw_confidence),
            "context": None,
        })

    return items


# ---------------------------------------------------------------------------
# Commitments
# ---------------------------------------------------------------------------

# Keywords used to identify semantic columns
_WHO_KEYWORDS = {"person", "who"}
_WHAT_KEYWORDS = {"commitment"}
_DEADLINE_KEYWORDS = {"deadline", "implied deadline"}
_CONTEXT_KEYWORDS = {"condition", "context", "to whom", "specificity", "strength"}


def _find_column(headers: list[str], keywords: set[str]) -> int | None:
    """Find the first column index whose lowered header matches any keyword."""
    for i, h in enumerate(headers):
        if h.lower().strip() in keywords:
            return i
    return None


def extract_commitments(content: str) -> list[dict]:
    """Extract from ## Commitments Made section.

    Handles four format variants by detecting column headers semantically:
      A: Person | Commitment | Implied Deadline | Condition | Confidence
      B: Commitment | Who | To Whom | Specificity
      C: Who | Commitment | To Whom | Context
      D: Who | Commitment | To Whom | Strength
    """
    section = _extract_section(content, "Commitments Made")
    if not section:
        return []

    headers, rows = _parse_table_rows(section)
    if not headers:
        return []

    lower_headers = [h.lower().strip() for h in headers]

    # Identify columns semantically
    who_idx = _find_column(headers, _WHO_KEYWORDS)
    what_idx = _find_column(headers, _WHAT_KEYWORDS)

    if what_idx is None:
        # No recognisable commitment column — skip
        return []
    if who_idx is None:
        # Might not have a "who" column at all; leave assignee as None
        pass

    deadline_idx = _find_column(headers, _DEADLINE_KEYWORDS)
    confidence_idx = _find_column(headers, {"confidence"})

    # Gather remaining columns as context sources
    context_indices: list[int] = []
    used = {who_idx, what_idx, deadline_idx, confidence_idx}
    for i, h in enumerate(lower_headers):
        if i not in used and h in _CONTEXT_KEYWORDS:
            context_indices.append(i)

    items: list[dict] = []
    for cells in rows:
        if len(cells) <= (what_idx or 0):
            continue

        description = cells[what_idx] if what_idx < len(cells) else ""
        if not description:
            continue

        assignee = cells[who_idx] if who_idx is not None and who_idx < len(cells) else None
        deadline = cells[deadline_idx] if deadline_idx is not None and deadline_idx < len(cells) else None
        raw_confidence = cells[confidence_idx] if confidence_idx is not None and confidence_idx < len(cells) else None

        # Collect context from remaining meaningful columns
        context_parts: list[str] = []
        for ci in context_indices:
            if ci < len(cells) and cells[ci]:
                context_parts.append(f"{headers[ci]}: {cells[ci]}")
        context = "; ".join(context_parts) if context_parts else None

        items.append({
            "item_type": "commitment",
            "description": description,
            "assignee": assignee if assignee else None,
            "deadline": deadline if deadline else None,
            "status": "Open",  # Commitments don't have explicit status in summaries
            "confidence": _normalise_confidence(raw_confidence),
            "context": context,
        })

    return items


# ---------------------------------------------------------------------------
# Decisions
# ---------------------------------------------------------------------------

_ARROW_RE = re.compile(r"\s*(?:→|->|=>|—>)\s*")


def _parse_bullet_decisions(section: str) -> list[dict]:
    """Parse decisions in bullet-list format.

    Pattern:
        - Decision text → owner
          - **Type:** explicit
          - **Confidence:** HIGH

    Also handles: ``- Decision text: rationale -> owner``
    """
    items: list[dict] = []
    current_text: str | None = None
    current_owner: str | None = None
    current_confidence: str | None = None

    for line in section.splitlines():
        stripped = line.strip()

        # Top-level bullet: starts a new decision
        if stripped.startswith("- ") and not stripped.startswith("- **"):
            # Flush previous
            if current_text and current_owner:
                items.append({
                    "item_type": "decision_followup",
                    "description": current_text,
                    "assignee": current_owner,
                    "deadline": None,
                    "status": "Open",
                    "confidence": _normalise_confidence(current_confidence),
                    "context": None,
                })
            current_text = None
            current_owner = None
            current_confidence = None

            body = stripped[2:].strip()
            parts = _ARROW_RE.split(body, maxsplit=1)
            if len(parts) == 2:
                current_text = parts[0].strip()
                current_owner = parts[1].strip()
            else:
                current_text = body
                current_owner = None

        # Sub-bullet with metadata
        elif stripped.startswith("- **") and current_text is not None:
            m = re.match(r"- \*\*Confidence:\*\*\s*(.+)", stripped, re.IGNORECASE)
            if m:
                current_confidence = m.group(1).strip()

    # Flush last item
    if current_text and current_owner:
        items.append({
            "item_type": "decision_followup",
            "description": current_text,
            "assignee": current_owner,
            "deadline": None,
            "status": "Open",
            "confidence": _normalise_confidence(current_confidence),
            "context": None,
        })

    return items


def _parse_table_decisions(section: str) -> list[dict]:
    """Parse decisions in table format.

    Headers: Decision | Type | Confidence | Owner
    Only returns rows that have an explicit Owner.
    """
    headers, rows = _parse_table_rows(section)
    if not headers:
        return []

    col = {h.lower().strip(): i for i, h in enumerate(headers)}

    decision_idx = col.get("decision", 0)
    owner_idx = col.get("owner")
    confidence_idx = col.get("confidence")
    type_idx = col.get("type")

    if owner_idx is None:
        # Cannot identify owner column — skip
        return []

    items: list[dict] = []
    for cells in rows:
        if len(cells) <= decision_idx:
            continue

        description = cells[decision_idx] if decision_idx < len(cells) else ""
        if not description:
            continue

        owner = cells[owner_idx] if owner_idx < len(cells) else None
        if not owner:
            continue  # Only extract decisions that have an explicit Owner

        raw_confidence = cells[confidence_idx] if confidence_idx is not None and confidence_idx < len(cells) else None
        decision_type = cells[type_idx] if type_idx is not None and type_idx < len(cells) else None

        context = f"Type: {decision_type}" if decision_type else None

        items.append({
            "item_type": "decision_followup",
            "description": description,
            "assignee": owner,
            "deadline": None,
            "status": "Open",
            "confidence": _normalise_confidence(raw_confidence),
            "context": context,
        })

    return items


def extract_decisions(content: str) -> list[dict]:
    """Extract from ## Decisions Made section. Handle both bullet and table formats."""
    section = _extract_section(content, "Decisions Made")
    if not section:
        return []

    # Determine format: if there is a table header row, use table parser
    has_table = False
    for line in section.splitlines():
        stripped = line.strip()
        if stripped.startswith("|") and "Decision" in stripped:
            has_table = True
            break

    if has_table:
        return _parse_table_decisions(section)
    else:
        return _parse_bullet_decisions(section)


# ---------------------------------------------------------------------------
# Top-level extraction
# ---------------------------------------------------------------------------

def extract_all_from_summary(filepath: Path) -> list[dict]:
    """Read a single summary file and extract all items.

    Returns a list of dicts, each augmented with source metadata.
    """
    try:
        content = filepath.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return []

    header = parse_summary_header(content)
    source_file = str(filepath)

    all_items: list[dict] = []

    for extractor in (extract_action_items, extract_commitments, extract_decisions):
        try:
            raw_items = extractor(content)
        except Exception:
            # Lenient: skip malformed sections rather than crashing
            continue

        for item in raw_items:
            item["source_file"] = source_file
            item["source_date"] = header["source_date"]
            item["workstreams"] = header["workstreams"]
            item["attendees"] = header["attendees"]
            all_items.append(item)

    return all_items


def extract_all_summaries(summaries_dir: Path) -> list[dict]:
    """Read ALL summary .md files from the directory and return all extracted items."""
    if not summaries_dir.is_dir():
        raise FileNotFoundError(f"Directory not found: {summaries_dir}")

    all_items: list[dict] = []
    files = sorted(summaries_dir.glob("*.md"))

    for filepath in files:
        items = extract_all_from_summary(filepath)
        all_items.extend(items)

    return all_items


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def _print_stats(items: list[dict], summaries_dir: Path) -> None:
    """Print extraction statistics."""
    file_count = len(list(summaries_dir.glob("*.md")))

    by_type: dict[str, int] = {}
    by_status: dict[str, int] = {}
    by_workstream: dict[str, int] = {}
    files_with_items: set[str] = set()

    for item in items:
        t = item["item_type"]
        by_type[t] = by_type.get(t, 0) + 1

        s = item["status"]
        by_status[s] = by_status.get(s, 0) + 1

        files_with_items.add(item["source_file"])

        for ws in item.get("workstreams", []):
            by_workstream[ws] = by_workstream.get(ws, 0) + 1

    print(f"Summary files scanned:  {file_count}")
    print(f"Files with items:       {len(files_with_items)}")
    print(f"Total items extracted:  {len(items)}")
    print()
    print("By type:")
    for t in sorted(by_type):
        print(f"  {t:25s} {by_type[t]:>4d}")
    print()
    print("By status:")
    for s in sorted(by_status):
        print(f"  {s:25s} {by_status[s]:>4d}")
    print()
    print("By workstream (items mentioning):")
    for ws in sorted(by_workstream):
        print(f"  {ws:25s} {by_workstream[ws]:>4d}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python -m scripts.parsers.summary_extractor <summaries_dir>")
        print("  e.g. python -m scripts.parsers.summary_extractor ../analysis/summaries")
        sys.exit(1)

    target = Path(sys.argv[1])
    if not target.is_dir():
        print(f"Error: {target} is not a directory")
        sys.exit(1)

    results = extract_all_summaries(target)
    _print_stats(results, target)
