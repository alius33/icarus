"""Speaker identification review API — serves mapping data and handles confirmations."""

from __future__ import annotations

import json
import logging
import re
from pathlib import Path

from fastapi import APIRouter, HTTPException, Query

from app.config import settings
from app.schemas.speaker_review import (
    ConfirmRequest,
    ConfirmResponse,
    SpeakerReviewItem,
    SpeakerReviewResponse,
    ReviewSummary,
    TranscriptContext,
)

logger = logging.getLogger(__name__)

router = APIRouter(tags=["speaker-review"])

# Paths — use DATA_ROOT for transcripts (project root), backend dir for scripts
_BACKEND_DIR = Path(__file__).resolve().parent.parent.parent
_MAPPING_PATH = _BACKEND_DIR / "scripts" / "speaker_id" / "output" / "mapping.json"
_DATA_ROOT = Path(settings.DATA_ROOT).resolve()
_TRANSCRIPTS_DIR = _DATA_ROOT / "Transcripts"

# Applied threshold used during the batch apply
_APPLIED_THRESHOLD = 0.65


def _load_mapping() -> dict:
    """Load the mapping JSON file."""
    if not _MAPPING_PATH.exists():
        raise HTTPException(status_code=404, detail="Mapping file not found. Run the speaker ID pipeline first.")
    with open(_MAPPING_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def _save_mapping(data: dict) -> None:
    """Save mapping JSON back to disk."""
    with open(_MAPPING_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def _check_name_in_transcript(filename: str, name: str) -> bool:
    """Check if the identified name actually appears in the transcript file."""
    if not name:
        return False
    filepath = _TRANSCRIPTS_DIR / filename
    if not filepath.exists():
        return False
    try:
        content = filepath.read_text(encoding="utf-8")
        return name in content
    except Exception:
        return False


def _build_items(data: dict) -> list[SpeakerReviewItem]:
    """Convert mapping JSON into flat list of review items.

    Status logic: check the actual transcript file to see if the speaker name
    is already present.  This gives an accurate picture regardless of whether
    the batch apply or a manual confirm put it there.
    """
    items: list[SpeakerReviewItem] = []

    # Cache file reads per transcript (one read per file, not per item)
    _file_cache: dict[str, str] = {}

    def _name_in_file(filename: str, name: str) -> bool:
        if not name:
            return False
        if filename not in _file_cache:
            filepath = _TRANSCRIPTS_DIR / filename
            try:
                _file_cache[filename] = filepath.read_text(encoding="utf-8")
            except Exception:
                _file_cache[filename] = ""
        return name in _file_cache[filename]

    for filename, tdata in data.get("transcripts", {}).items():
        meeting_type = tdata.get("meeting_type", "unknown")
        known = tdata.get("known_speakers", [])
        unresolved = set(tdata.get("unresolved", []))
        mappings = tdata.get("mappings", {})

        for label, label_data in mappings.items():
            # Handle instance-specific mappings (Unknown Speaker with instances dict)
            instances = label_data.get("instances")
            if instances:
                for ts, inst in instances.items():
                    item_id = f"{filename}::{label}::{ts}"
                    confidence = inst.get("confidence", 0.0)
                    identified_as = inst.get("identified_as", "")

                    # Determine status by checking the actual file
                    if label in unresolved and not identified_as:
                        status = "unresolved"
                    elif _name_in_file(filename, identified_as):
                        status = "applied"
                    else:
                        status = "flagged"

                    items.append(SpeakerReviewItem(
                        id=item_id,
                        transcript_filename=filename,
                        meeting_type=meeting_type,
                        known_speakers=known,
                        speaker_label=label,
                        timestamp=ts,
                        identified_as=identified_as,
                        confidence=confidence,
                        method=inst.get("method", ""),
                        evidence=inst.get("evidence", ""),
                        status=status,
                    ))
            else:
                # Simple mapping (Speaker N → name)
                item_id = f"{filename}::{label}::0"
                confidence = label_data.get("confidence", 0.0)
                identified_as = label_data.get("identified_as", "")

                if _name_in_file(filename, identified_as):
                    status = "applied"
                else:
                    status = "flagged"

                items.append(SpeakerReviewItem(
                    id=item_id,
                    transcript_filename=filename,
                    meeting_type=meeting_type,
                    known_speakers=known,
                    speaker_label=label,
                    timestamp="",
                    identified_as=identified_as,
                    confidence=confidence,
                    method=label_data.get("method", ""),
                    evidence=label_data.get("evidence", ""),
                    status=status,
                ))

    # Sort: flagged first, then by confidence ascending
    status_order = {"unresolved": 0, "flagged": 1, "applied": 2}
    items.sort(key=lambda x: (status_order.get(x.status, 3), x.confidence))
    return items


def _get_stakeholder_names() -> list[str]:
    """Get list of all known stakeholder canonical names."""
    try:
        import sys
        sys.path.insert(0, str(_BACKEND_DIR))
        from scripts.speaker_id.config import STAKEHOLDER_ALIASES
        return sorted(STAKEHOLDER_ALIASES.keys())
    except ImportError:
        return []


@router.get("/speaker-review", response_model=SpeakerReviewResponse)
async def get_speaker_review():
    """Return all speaker identifications for review."""
    data = _load_mapping()
    items = _build_items(data)

    applied_count = sum(1 for i in items if i.status == "applied")
    flagged_count = sum(1 for i in items if i.status == "flagged")
    unresolved_count = sum(1 for i in items if i.status == "unresolved")

    # Count methods
    methods: dict[str, int] = {}
    for item in items:
        m = item.method
        methods[m] = methods.get(m, 0) + 1

    summary = ReviewSummary(
        total_transcripts=len(data.get("transcripts", {})),
        total_identifications=len(items),
        applied_count=applied_count,
        flagged_count=flagged_count,
        unresolved_count=unresolved_count,
        methods=methods,
    )

    return SpeakerReviewResponse(
        summary=summary,
        items=items,
        stakeholder_names=_get_stakeholder_names(),
    )


@router.post("/speaker-review/confirm", response_model=ConfirmResponse)
async def confirm_speaker_identifications(req: ConfirmRequest):
    """Apply user-confirmed identifications to transcript files."""
    data = _load_mapping()
    applied = 0
    rejected = 0
    errors: list[str] = []

    for action in req.actions:
        try:
            # Parse the item ID: "filename::label::timestamp"
            parts = action.id.split("::")
            if len(parts) != 3:
                errors.append(f"Invalid ID format: {action.id}")
                continue

            filename, label, ts = parts
            tdata = data.get("transcripts", {}).get(filename)
            if not tdata:
                errors.append(f"Transcript not found: {filename}")
                continue

            mappings = tdata.get("mappings", {})

            if action.action == "reject":
                # Remove from mappings
                if label in mappings:
                    instances = mappings[label].get("instances")
                    if instances and ts in instances:
                        del instances[ts]
                        if not instances:
                            del mappings[label]
                    elif not instances:
                        del mappings[label]
                rejected += 1

            elif action.action in ("accept", "manual"):
                name = action.manual_name if action.action == "manual" else None

                if label in mappings:
                    instances = mappings[label].get("instances")
                    if instances and ts in instances:
                        inst = instances[ts]
                        if name:
                            inst["identified_as"] = name
                            inst["method"] = "manual"
                            inst["evidence"] = f"Manually set to {name}"
                        inst["confidence"] = max(inst.get("confidence", 0), 0.95)

                        # Remove from flagged_for_review
                        flag_key = f"{label}@{ts}"
                        flagged = tdata.get("flagged_for_review", [])
                        if flag_key in flagged:
                            flagged.remove(flag_key)

                # Apply to transcript file
                filepath = _TRANSCRIPTS_DIR / filename
                if filepath.exists():
                    final_name = name
                    if not final_name and label in mappings:
                        instances = mappings[label].get("instances")
                        if instances and ts in instances:
                            final_name = instances[ts].get("identified_as")

                    if final_name:
                        _apply_single_replacement(filepath, label, ts, final_name)
                        applied += 1
                else:
                    errors.append(f"Transcript file not found: {filename}")

        except Exception as e:
            errors.append(f"Error processing {action.id}: {str(e)}")

    # Save updated mapping
    _save_mapping(data)

    # Trigger re-import if any changes were applied
    if applied > 0:
        try:
            import subprocess
            subprocess.Popen(
                ["python", "-m", "scripts.import_data", "--data-root", "..", "--db-url",
                 "postgresql://icarus:icarus_local@db:5432/icarus"],
                cwd=str(_BACKEND_DIR),
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
        except Exception:
            pass  # Non-critical: import can be triggered manually

    return ConfirmResponse(applied=applied, rejected=rejected, errors=errors)


def _apply_single_replacement(filepath: Path, label: str, timestamp: str, name: str) -> None:
    """Apply a single speaker label replacement in a transcript file."""
    text = filepath.read_text(encoding="utf-8")

    # Build regex pattern for the specific speaker line
    if label == "Unknown Speaker":
        # For Unknown Speaker, match by timestamp to replace the correct instance
        pattern = re.compile(
            rf"^(Unknown Speaker)(\s{{2,}}{re.escape(timestamp)}.*)$",
            re.MULTILINE,
        )
    else:
        # For Speaker N, replace all instances (consistent label)
        pattern = re.compile(
            rf"^({re.escape(label)})(\s{{2,}}\d+:\d+.*)$",
            re.MULTILINE,
        )

    new_text, count = pattern.subn(rf"{name}\2", text)
    if count > 0:
        # Create backup if not already exists
        bak = filepath.with_suffix(filepath.suffix + ".bak")
        if not bak.exists():
            filepath.rename(bak)
            bak.rename(filepath.with_suffix(filepath.suffix + ".bak"))
            # Actually: copy first
            import shutil
            if not filepath.with_suffix(filepath.suffix + ".bak").exists():
                shutil.copy2(filepath, filepath.with_suffix(filepath.suffix + ".bak"))

        filepath.write_text(new_text, encoding="utf-8")


@router.get("/speaker-review/context/{filename}", response_model=TranscriptContext)
async def get_transcript_context(
    filename: str,
    timestamp: str = Query("0:00"),
    label: str = Query("Unknown Speaker"),
    window: int = Query(5, ge=1, le=20),
):
    """Return lines from the transcript around a speaker occurrence."""
    filepath = _TRANSCRIPTS_DIR / filename
    if not filepath.exists():
        raise HTTPException(status_code=404, detail=f"Transcript not found: {filename}")

    lines = filepath.read_text(encoding="utf-8").splitlines()

    # Find the line with the matching label + timestamp
    target_line = -1
    speaker_re = re.compile(rf"^{re.escape(label)}\s{{2,}}{re.escape(timestamp)}")
    for i, line in enumerate(lines):
        if speaker_re.match(line):
            target_line = i
            break

    if target_line == -1:
        # Fallback: find first occurrence of the label
        for i, line in enumerate(lines):
            if line.startswith(label):
                target_line = i
                break

    if target_line == -1:
        target_line = 0

    start = max(0, target_line - window)
    end = min(len(lines), target_line + window + 1)

    return TranscriptContext(
        filename=filename,
        lines=lines[start:end],
        highlight_line=target_line - start,
    )
