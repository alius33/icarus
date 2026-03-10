"""
Parser for transcript files in Transcripts/*.txt

Handles multiple filename date formats:
  - DD-MM-YYYY_-_Title.txt
  - YYYY-MM-DD_-_Title.txt
  - YYYY-MM-DD_Title.txt  (no _-_ separator)
  - YYYY-MM-DD_HH-MM-SS.txt  (timestamp only, no title)
  - YYYY-MM-DD - Title.txt  (spaces with dash separator)
  - YYYY-MM-DD Title.txt  (space separator, no dash)
  - Suffixes like __1_, __2_ or (1), (2) on titles
"""

import hashlib
import re
from datetime import datetime
from pathlib import Path
from typing import Optional


# Speaker line pattern: "Name Name  0:01" (two+ spaces before timestamp)
SPEAKER_PATTERN = re.compile(r'^([A-Z][a-zA-Z]+(?:\s+[A-Za-z]+)*)\s{2,}\d+:\d+')

# Filename patterns ordered by specificity
# DD-MM-YYYY_-_Title.txt
PATTERN_DMY_SEP = re.compile(
    r'^(\d{2})-(\d{2})-(\d{4})_-_(.+)\.txt$'
)
# YYYY-MM-DD_-_Title.txt
PATTERN_YMD_SEP = re.compile(
    r'^(\d{4})-(\d{2})-(\d{2})_-_(.+)\.txt$'
)
# YYYY-MM-DD_HH-MM-SS.txt (timestamp only)
PATTERN_YMD_TIME = re.compile(
    r'^(\d{4})-(\d{2})-(\d{2})_(\d{2})-(\d{2})-(\d{2})\.txt$'
)
# YYYY-MM-DD_Title.txt (no separator)
PATTERN_YMD_NOSEP = re.compile(
    r'^(\d{4})-(\d{2})-(\d{2})_(.+)\.txt$'
)
# YYYY-MM-DD - Title.txt (spaces with dash separator)
PATTERN_YMD_SPACE_SEP = re.compile(
    r'^(\d{4})-(\d{2})-(\d{2})\s+-\s+(.+)\.txt$'
)
# YYYY-MM-DD Title.txt (space separator, no dash)
PATTERN_YMD_SPACE = re.compile(
    r'^(\d{4})-(\d{2})-(\d{2})\s+(.+)\.txt$'
)
# DD-MM-YYYY - Title.txt (spaces with dash separator, day-first)
PATTERN_DMY_SPACE_SEP = re.compile(
    r'^(\d{2})-(\d{2})-(\d{4})\s+-\s+(.+)\.txt$'
)


def _compute_file_hash(filepath: Path) -> str:
    """Compute SHA256 hash of file contents."""
    sha256 = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            sha256.update(chunk)
    return sha256.hexdigest()


def _clean_title(raw_title: str) -> str:
    """Clean up a title extracted from filename.

    - Remove trailing suffixes like __1_, __2_
    - Replace underscores with spaces
    - Strip extra whitespace
    """
    # Remove trailing __N_ suffixes (e.g., __1_, __2_)
    cleaned = re.sub(r'__\d+_$', '', raw_title)
    # Remove trailing parenthetical suffixes like (1), (2)
    cleaned = re.sub(r'\(\d+\)$', '', cleaned)
    # Replace underscores with spaces
    cleaned = cleaned.replace('_', ' ')
    # Collapse multiple spaces
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()
    return cleaned


def _parse_date_and_title(filename: str) -> tuple[Optional[datetime], str]:
    """Extract meeting date and title from filename.

    Returns (date, title) tuple. Title may be derived from filename if not
    explicitly present.
    """
    # Try DD-MM-YYYY_-_Title.txt
    match = PATTERN_DMY_SEP.match(filename)
    if match:
        day, month, year, raw_title = match.groups()
        try:
            meeting_date = datetime(int(year), int(month), int(day)).date()
        except ValueError:
            meeting_date = None
        return meeting_date, _clean_title(raw_title)

    # Try YYYY-MM-DD_-_Title.txt
    match = PATTERN_YMD_SEP.match(filename)
    if match:
        year, month, day, raw_title = match.groups()
        try:
            meeting_date = datetime(int(year), int(month), int(day)).date()
        except ValueError:
            meeting_date = None
        return meeting_date, _clean_title(raw_title)

    # Try YYYY-MM-DD_HH-MM-SS.txt (timestamp only, no title)
    match = PATTERN_YMD_TIME.match(filename)
    if match:
        year, month, day, hour, minute, second = match.groups()
        try:
            meeting_date = datetime(int(year), int(month), int(day)).date()
        except ValueError:
            meeting_date = None
        time_str = f"{hour}:{minute}:{second}"
        title = f"Recording {meeting_date} {time_str}" if meeting_date else f"Recording {filename}"
        return meeting_date, title

    # Try YYYY-MM-DD - Title.txt (spaces with dash separator)
    match = PATTERN_YMD_SPACE_SEP.match(filename)
    if match:
        year, month, day, raw_title = match.groups()
        try:
            meeting_date = datetime(int(year), int(month), int(day)).date()
        except ValueError:
            meeting_date = None
        return meeting_date, _clean_title(raw_title)

    # Try DD-MM-YYYY - Title.txt (spaces with dash separator, day-first)
    match = PATTERN_DMY_SPACE_SEP.match(filename)
    if match:
        day, month, year, raw_title = match.groups()
        try:
            meeting_date = datetime(int(year), int(month), int(day)).date()
        except ValueError:
            meeting_date = None
        return meeting_date, _clean_title(raw_title)

    # Try YYYY-MM-DD_Title.txt (no _-_ separator)
    match = PATTERN_YMD_NOSEP.match(filename)
    if match:
        year, month, day, raw_title = match.groups()
        try:
            meeting_date = datetime(int(year), int(month), int(day)).date()
        except ValueError:
            meeting_date = None
        return meeting_date, _clean_title(raw_title)

    # Try YYYY-MM-DD Title.txt (space separator, no dash)
    match = PATTERN_YMD_SPACE.match(filename)
    if match:
        year, month, day, raw_title = match.groups()
        try:
            meeting_date = datetime(int(year), int(month), int(day)).date()
        except ValueError:
            meeting_date = None
        return meeting_date, _clean_title(raw_title)

    # Fallback: no recognisable date pattern
    title = _clean_title(filename.replace('.txt', ''))
    return None, title


def _extract_participants(content: str) -> list[str]:
    """Extract unique speaker names from transcript content.

    Speaker lines follow the format: "Name Name  0:01" (name followed by
    two or more spaces then a timestamp).
    """
    speakers = set()
    for line in content.splitlines():
        match = SPEAKER_PATTERN.match(line.strip())
        if match:
            speakers.add(match.group(1).strip())
    return sorted(speakers)


def parse_transcript(filepath: Path) -> dict:
    """Parse a single transcript file.

    Args:
        filepath: Path to the .txt transcript file.

    Returns:
        Dict with keys: filename, title, meeting_date, content, word_count,
        participants, source_file, file_hash.
    """
    filename = filepath.name
    meeting_date, title = _parse_date_and_title(filename)

    content = filepath.read_text(encoding="utf-8", errors="replace")
    word_count = len(content.split())
    participants = _extract_participants(content)
    file_hash = _compute_file_hash(filepath)
    source_file = str(filepath.relative_to(filepath.parent.parent))

    return {
        "filename": filename,
        "title": title,
        "meeting_date": meeting_date,
        "content": content,
        "word_count": word_count,
        "participants": participants,
        "source_file": source_file,
        "file_hash": file_hash,
    }
