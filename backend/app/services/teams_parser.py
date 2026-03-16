"""Parse Microsoft Teams chat format into speaker-attributed text."""

import re

# Pattern: [3/14/2026 10:23 AM] John Smith
_BRACKET_PATTERN = re.compile(
    r"^\[(\d{1,2}/\d{1,2}/\d{4}\s+\d{1,2}:\d{2}(?::\d{2})?\s*(?:AM|PM)?)\]\s+(.+)$",
    re.IGNORECASE,
)

# Pattern: John Smith 10:23 AM  or  John Smith, 3/14/2026 10:23 AM
_INLINE_PATTERN = re.compile(
    r"^(.+?)\s*,?\s+(\d{1,2}(?:/\d{1,2}/\d{4})?\s+\d{1,2}:\d{2}(?::\d{2})?\s*(?:AM|PM)?)$",
    re.IGNORECASE,
)

# Minimum number of detected speaker lines to consider it a Teams chat
_MIN_SPEAKER_LINES = 2


def detect_teams_chat(text: str) -> bool:
    """Return True if the text looks like a pasted Teams chat."""
    count = 0
    for line in text.splitlines():
        stripped = line.strip()
        if _BRACKET_PATTERN.match(stripped) or _INLINE_PATTERN.match(stripped):
            count += 1
            if count >= _MIN_SPEAKER_LINES:
                return True
    return False


def parse_teams_chat(text: str) -> str:
    """Convert Teams chat format to speaker-attributed transcript format.

    Input:
        [3/14/2026 10:23 AM] John Smith
        Hey team, quick update...

    Output:
        John Smith: Hey team, quick update...
    """
    lines = text.splitlines()
    result: list[str] = []
    current_speaker: str | None = None
    current_message: list[str] = []

    def flush():
        if current_speaker and current_message:
            msg = "\n".join(current_message).strip()
            if msg:
                result.append(f"{current_speaker}: {msg}")

    for line in lines:
        stripped = line.strip()

        # Try bracket pattern first
        m = _BRACKET_PATTERN.match(stripped)
        if m:
            flush()
            current_speaker = m.group(2).strip()
            current_message = []
            continue

        # Try inline pattern
        m = _INLINE_PATTERN.match(stripped)
        if m:
            name = m.group(1).strip()
            # Avoid false positives: name should not be too long or contain common words
            if len(name.split()) <= 4 and not any(c.isdigit() for c in name):
                flush()
                current_speaker = name
                current_message = []
                continue

        # Regular line — append to current message
        if current_speaker is not None:
            current_message.append(line)
        else:
            # Lines before any speaker detected — keep as-is
            result.append(line)

    flush()
    return "\n\n".join(result)
