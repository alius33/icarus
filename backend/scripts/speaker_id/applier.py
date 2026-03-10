"""Apply speaker identification mappings to transcript files in-place."""

from __future__ import annotations

import re
import shutil
from pathlib import Path

from .models import SpeakerMapping


SPEAKER_LINE_RE = re.compile(
    r'^(Speaker \d+|Unknown Speaker)(\s{2,}\d+:\d+.*)$'
)

TIMESTAMP_RE = re.compile(r'(\d+:\d+)')


def apply_mapping(filepath: Path,
                  mapping: SpeakerMapping,
                  threshold: float = 0.0,
                  backup: bool = True,
                  dry_run: bool = False) -> dict:
    """Replace speaker labels in-place, preserving timestamp format.

    Args:
        filepath: Path to the .txt transcript
        mapping: SpeakerMapping with label → name mappings
        threshold: Only apply identifications above this confidence
        backup: Create .txt.bak backup before modifying
        dry_run: If True, don't modify files, just return what would change

    Returns:
        dict with counts and details of replacements
    """
    try:
        content = filepath.read_text(encoding="utf-8", errors="replace")
    except (OSError, UnicodeDecodeError) as e:
        return {"error": str(e), "file": str(filepath), "replacements": 0}

    lines = content.splitlines(keepends=True)
    replacements = []
    modified_lines = list(lines)

    for i, line in enumerate(lines):
        stripped = line.strip()
        match = SPEAKER_LINE_RE.match(stripped)
        if not match:
            continue

        label = match.group(1)
        rest = match.group(2)  # "  0:52" etc.

        if label not in mapping.mappings:
            continue

        entry = mapping.mappings[label]

        if label == "Unknown Speaker" and isinstance(entry, dict) and "instances" in entry:
            # Instance-specific replacement (keyed by timestamp)
            ts_match = TIMESTAMP_RE.search(rest)
            if not ts_match:
                continue
            ts = ts_match.group(1)

            instances = entry.get("instances", {})
            if ts not in instances:
                continue

            instance = instances[ts]
            confidence = instance.get("confidence", 0)
            if confidence < threshold:
                continue

            new_name = instance["identified_as"]
            new_line = line.replace(label, new_name, 1)
            modified_lines[i] = new_line
            replacements.append({
                "line": i + 1,
                "old": label,
                "new": new_name,
                "timestamp": ts,
                "confidence": confidence,
            })

        elif isinstance(entry, dict) and "identified_as" in entry:
            # Simple replacement (Speaker N → Name)
            confidence = entry.get("confidence", 0)
            if confidence < threshold:
                continue

            new_name = entry["identified_as"]
            new_line = line.replace(label, new_name, 1)
            modified_lines[i] = new_line
            replacements.append({
                "line": i + 1,
                "old": label,
                "new": new_name,
                "confidence": confidence,
            })

    result = {
        "file": str(filepath),
        "replacements": len(replacements),
        "details": replacements,
    }

    if not dry_run and replacements:
        # Create backup
        if backup:
            backup_path = filepath.with_suffix('.txt.bak')
            if not backup_path.exists():  # Don't overwrite existing backups
                shutil.copy2(filepath, backup_path)

        # Write modified content
        filepath.write_text("".join(modified_lines), encoding="utf-8")
        result["backed_up"] = backup and not filepath.with_suffix('.txt.bak').exists()

    return result


def apply_all_mappings(transcripts_dir: Path,
                       all_mappings: dict[str, SpeakerMapping],
                       threshold: float = 0.0,
                       backup: bool = True,
                       dry_run: bool = False) -> list[dict]:
    """Apply mappings to all transcripts.

    Args:
        transcripts_dir: Directory containing transcript .txt files
        all_mappings: filename → SpeakerMapping
        threshold: Minimum confidence to apply
        backup: Create backups
        dry_run: Preview mode

    Returns:
        List of result dicts per file
    """
    results = []

    for filename, mapping in all_mappings.items():
        filepath = transcripts_dir / filename
        if not filepath.exists():
            results.append({
                "file": str(filepath),
                "error": "File not found",
                "replacements": 0,
            })
            continue

        if not mapping.mappings:
            continue  # Nothing to apply

        result = apply_mapping(filepath, mapping, threshold, backup, dry_run)
        if result["replacements"] > 0 or result.get("error"):
            results.append(result)

    return results


def restore_from_backup(filepath: Path) -> bool:
    """Restore a transcript from its .txt.bak backup."""
    backup_path = filepath.with_suffix('.txt.bak')
    if not backup_path.exists():
        return False
    shutil.copy2(backup_path, filepath)
    return True


def clean_backups(transcripts_dir: Path) -> int:
    """Remove all .txt.bak backup files."""
    count = 0
    for bak in transcripts_dir.glob("*.txt.bak"):
        bak.unlink()
        count += 1
    return count
