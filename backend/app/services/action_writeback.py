"""Write-back service for action item status changes.

When an action item's status changes via the UI, this service updates
the markdown tracker file so Claude's /analyse pipeline sees the change.
"""

import re
from pathlib import Path

from app.config import settings


def update_action_status_in_markdown(action_number: str, new_status: str) -> bool:
    """Update an action item's status in analysis/trackers/action_items.md.

    Returns True if the file was updated, False if the action wasn't found
    or the file doesn't exist. Fails gracefully — never raises.
    """
    try:
        data_root = Path(settings.DATA_ROOT) if hasattr(settings, "DATA_ROOT") else Path(".")
        filepath = data_root / "analysis" / "trackers" / "action_items.md"

        if not filepath.exists():
            return False

        content = filepath.read_text(encoding="utf-8")
        lines = content.splitlines()
        updated = False

        for i, line in enumerate(lines):
            # Match table rows like: | AI-2026-001 | description | owner | deadline | OPEN |
            # The number could appear in various columns
            if f"| {action_number}" in line or f"|{action_number}" in line:
                # Replace status in this table row
                parts = line.split("|")
                for j, part in enumerate(parts):
                    stripped = part.strip().upper()
                    if stripped in ("OPEN", "COMPLETED", "LIKELY_COMPLETED", "IN PROGRESS", "BLOCKED"):
                        parts[j] = f" {new_status} "
                        updated = True
                        break

                if updated:
                    lines[i] = "|".join(parts)
                    break

        if not updated:
            # Try a more flexible pattern: look for the action number and
            # replace any status keyword on the same line
            pattern = re.compile(
                rf"(.*{re.escape(action_number)}.*?)\b(OPEN|COMPLETED|LIKELY_COMPLETED|IN PROGRESS|BLOCKED)\b",
                re.IGNORECASE,
            )
            for i, line in enumerate(lines):
                match = pattern.match(line)
                if match:
                    lines[i] = pattern.sub(
                        lambda m: m.group(1) + new_status, line, count=1
                    )
                    updated = True
                    break

        if updated:
            filepath.write_text("\n".join(lines) + "\n", encoding="utf-8")

        return updated

    except Exception:
        # Fail gracefully — DB update should succeed even if markdown fails
        return False
