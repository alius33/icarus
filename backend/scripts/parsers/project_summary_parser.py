"""
Parser for project summaries from analysis/projects/*/

Scans each project subdirectory for .md files and extracts:
- Date from **Date:** line
- Relevance from **Relevance:** line
- Full file content
- SHA256 file hash for change detection

Directory structure:
analysis/projects/
    clara/
        2026-02-10_standup.md
        2026-02-12_review.md
    sales-recon/
        2026-02-11_planning.md
"""

import hashlib
import os
import pathlib
import re


def parse_project_summaries(data_root: str) -> list[dict]:
    """Scan analysis/projects/*/ and parse all .md files into dicts.

    Args:
        data_root: Root directory of the icarus project (contains analysis/).

    Returns:
        List of dicts with: project_slug, date, relevance, content,
        source_file, file_hash.
    """
    results = []
    projects_dir = pathlib.Path(data_root) / "analysis" / "projects"

    if not projects_dir.exists():
        return results

    for project_path in sorted(projects_dir.iterdir()):
        if not project_path.is_dir():
            continue

        project_slug = project_path.name

        for md_file in sorted(project_path.glob("*.md")):
            if not md_file.is_file():
                continue

            try:
                content = md_file.read_text(encoding="utf-8")
            except (OSError, UnicodeDecodeError):
                continue

            file_hash = hashlib.sha256(content.encode("utf-8")).hexdigest()

            parsed_date = _extract_field(content, "Date")
            relevance = _extract_field(content, "Relevance")

            # Build relative source file path
            source_file = str(md_file.relative_to(pathlib.Path(data_root)))

            results.append({
                "project_slug": project_slug,
                "date": parsed_date,
                "relevance": relevance,
                "content": content,
                "source_file": source_file,
                "file_hash": file_hash,
            })

    return results


def _extract_field(content: str, field_name: str) -> str | None:
    """Extract a metadata field value from markdown content.

    Looks for patterns like:
        **Date:** 2026-02-10
        **Relevance:** HIGH
    """
    pattern = rf"\*\*{re.escape(field_name)}:\*\*\s*(.+)"
    match = re.search(pattern, content)
    if match:
        value = match.group(1).strip()
        return value if value else None
    return None
