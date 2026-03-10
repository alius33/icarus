"""
Parser for context/glossary.md

Handles:
  - ## Category Name  sections
  - Entries: - **Term** -- Definition  (using em dash or double dash)
  - Skips the "People -- Quick Reference" section (handled by stakeholder_parser)
"""

import hashlib
import re
from pathlib import Path

# Sections to skip (people tables handled elsewhere)
SKIP_SECTIONS = {"people — quick reference", "people -- quick reference"}


def _compute_file_hash(filepath: Path) -> str:
    """Compute SHA256 hash of file contents."""
    sha256 = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            sha256.update(chunk)
    return sha256.hexdigest()


def parse_glossary(filepath: Path) -> list[dict]:
    """Parse glossary.md into a list of glossary entry dicts.

    Args:
        filepath: Path to glossary.md

    Returns:
        List of dicts with: term, category, definition, source_file, file_hash.
    """
    content = filepath.read_text(encoding="utf-8", errors="replace")
    file_hash = _compute_file_hash(filepath)
    source_file = str(filepath.relative_to(filepath.parent.parent))
    lines = content.splitlines()

    entries = []
    current_category = None
    skip_section = False

    for line in lines:
        stripped = line.strip()

        # Detect category headings
        cat_match = re.match(r'^##\s+(.+)$', stripped)
        if cat_match:
            category_name = cat_match.group(1).strip()
            if category_name.lower().replace('\u2014', '--') in SKIP_SECTIONS:
                skip_section = True
                current_category = None
            elif "quick reference" in category_name.lower():
                skip_section = True
                current_category = None
            else:
                skip_section = False
                current_category = category_name
            continue

        if skip_section or current_category is None:
            continue

        # Match glossary entries: - **Term** — Definition
        # Supports em dash (—), en dash (–), or double-dash (--)
        entry_match = re.match(
            r'^-\s+\*\*(.+?)\*\*\s*(?:—|–|--|---)\s*(.+)$',
            stripped
        )
        if entry_match:
            term = entry_match.group(1).strip()
            definition = entry_match.group(2).strip()
            entries.append({
                "term": term,
                "category": current_category,
                "definition": definition,
                "source_file": source_file,
                "file_hash": file_hash,
            })

    return entries
