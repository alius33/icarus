"""Parse transcripts into ordered speaker segments."""

from __future__ import annotations

import re
from pathlib import Path

from .models import SpeakerSegment


# Matches: "Name Name  0:52" or "Speaker 1  1:08" or "Unknown Speaker  14:15"
SPEAKER_LINE_RE = re.compile(
    r'^([A-Z][a-zA-Z]+(?:\s+[A-Za-z]+)*)\s{2,}(\d+:\d+)'
)

UNIDENTIFIED_RE = re.compile(r'^(Speaker \d+|Unknown Speaker)$')


def _parse_timestamp(ts: str) -> int:
    """Convert 'MM:SS' or 'H:MM:SS' to total seconds."""
    parts = ts.split(":")
    if len(parts) == 2:
        return int(parts[0]) * 60 + int(parts[1])
    elif len(parts) == 3:
        return int(parts[0]) * 3600 + int(parts[1]) * 60 + int(parts[2])
    return 0


def parse_segments(filepath: Path) -> list[SpeakerSegment]:
    """Parse a transcript file into ordered speaker segments.

    Returns a list of SpeakerSegment objects, one per speaking turn.
    """
    try:
        content = filepath.read_text(encoding="utf-8", errors="replace")
    except (OSError, UnicodeDecodeError):
        return []

    lines = content.splitlines()
    segments: list[SpeakerSegment] = []
    current: dict | None = None
    text_lines: list[str] = []
    segment_idx = 0

    for i, line in enumerate(lines):
        stripped = line.strip()
        match = SPEAKER_LINE_RE.match(stripped)

        if match:
            # Finalize previous segment
            if current is not None:
                text = "\n".join(text_lines).strip()
                word_count = len(text.split()) if text else 0
                segments.append(SpeakerSegment(
                    label=current["label"],
                    timestamp=current["timestamp"],
                    timestamp_seconds=current["timestamp_seconds"],
                    text=text,
                    line_number=current["line_number"],
                    word_count=word_count,
                    is_unidentified=current["is_unidentified"],
                    segment_index=current["segment_index"],
                ))

            label = match.group(1).strip()
            ts = match.group(2)
            is_unknown = bool(UNIDENTIFIED_RE.match(label))

            current = {
                "label": label,
                "timestamp": ts,
                "timestamp_seconds": _parse_timestamp(ts),
                "line_number": i + 1,  # 1-indexed
                "is_unidentified": is_unknown,
                "segment_index": segment_idx,
            }
            text_lines = []
            segment_idx += 1
        elif current is not None:
            # Continuation of current speaker's text
            if stripped:  # Skip blank lines at start
                text_lines.append(stripped)
            elif text_lines:  # Keep blank lines in middle
                text_lines.append("")

    # Finalize last segment
    if current is not None:
        text = "\n".join(text_lines).strip()
        word_count = len(text.split()) if text else 0
        segments.append(SpeakerSegment(
            label=current["label"],
            timestamp=current["timestamp"],
            timestamp_seconds=current["timestamp_seconds"],
            text=text,
            line_number=current["line_number"],
            word_count=word_count,
            is_unidentified=current["is_unidentified"],
            segment_index=current["segment_index"],
        ))

    return segments


def get_known_speakers(segments: list[SpeakerSegment]) -> list[str]:
    """Extract unique named (identified) speakers from segments."""
    seen = set()
    result = []
    for seg in segments:
        if not seg.is_unidentified and seg.label not in seen:
            seen.add(seg.label)
            result.append(seg.label)
    return sorted(result)


def get_unknown_labels(segments: list[SpeakerSegment]) -> list[str]:
    """Extract unique unidentified speaker labels from segments."""
    seen = set()
    result = []
    for seg in segments:
        if seg.is_unidentified and seg.label not in seen:
            seen.add(seg.label)
            result.append(seg.label)
    return result


def get_segments_by_label(segments: list[SpeakerSegment],
                          label: str) -> list[SpeakerSegment]:
    """Get all segments for a given speaker label."""
    return [s for s in segments if s.label == label]


def get_combined_text(segments: list[SpeakerSegment],
                      label: str) -> str:
    """Get all text from a speaker concatenated."""
    texts = [s.text for s in segments if s.label == label and s.text]
    return " ".join(texts)


def get_total_words(segments: list[SpeakerSegment], label: str) -> int:
    """Get total word count for a speaker."""
    return sum(s.word_count for s in segments if s.label == label)


def parse_title_from_filename(filename: str) -> str:
    """Extract a clean title from a transcript filename.

    Handles formats:
    - DD-MM-YYYY_-_Title.txt
    - YYYY-MM-DD_-_Title.txt
    - YYYY-MM-DD - Title.txt
    - YYYY-MM-DD_HH-MM-SS.txt
    """
    name = Path(filename).stem

    # Remove date prefixes
    # DD-MM-YYYY_-_ or YYYY-MM-DD_-_
    name = re.sub(r'^\d{2}-\d{2}-\d{4}_-_', '', name)
    name = re.sub(r'^\d{4}-\d{2}-\d{2}_-_', '', name)
    # YYYY-MM-DD - (with spaces)
    name = re.sub(r'^\d{4}-\d{2}-\d{2}\s*-\s*', '', name)
    # YYYY-MM-DD_ (underscore, no separator)
    name = re.sub(r'^\d{4}-\d{2}-\d{2}_', '', name)
    # Pure timestamp: YYYY-MM-DD_HH-MM-SS
    if re.match(r'^\d{4}-\d{2}-\d{2}', name) and not name.strip():
        return filename  # Return original if only timestamp

    # Clean up
    name = name.replace('_', ' ')
    name = re.sub(r'\s*\(\d+\)\s*$', '', name)  # Remove (1), (2) suffixes
    name = name.strip()

    return name if name else filename
