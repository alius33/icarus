"""
Parser for context/stakeholders.md

Handles:
  - Tier 1-3: ### Name -- Role  sections with bullet-point attributes
  - Tier 4: markdown table with Person | Domain | Status columns
"""

import hashlib
import re
from pathlib import Path


def _compute_file_hash(filepath: Path) -> str:
    """Compute SHA256 hash of file contents."""
    sha256 = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            sha256.update(chunk)
    return sha256.hexdigest()


def _extract_bullet_value(lines: list[str], key: str) -> str | None:
    """Extract a value from bullet points matching **Key:** pattern."""
    for line in lines:
        stripped = line.strip()
        pattern = f"**{key}:**"
        if pattern.lower() in stripped.lower():
            # Extract everything after the **Key:** marker
            idx = stripped.lower().index(pattern.lower())
            after = stripped[idx + len(pattern):].strip()
            return after if after else None
    return None


def _extract_bullet_value_flexible(lines: list[str], keys: list[str]) -> str | None:
    """Try multiple key variants and return the first match."""
    for key in keys:
        val = _extract_bullet_value(lines, key)
        if val:
            return val
    return None


def parse_stakeholders(filepath: Path) -> list[dict]:
    """Parse stakeholders.md into a list of stakeholder dicts.

    Args:
        filepath: Path to stakeholders.md

    Returns:
        List of dicts with: name, tier, role, engagement_level,
        communication_style, concerns, key_contributions, notes,
        source_file, file_hash.
    """
    content = filepath.read_text(encoding="utf-8", errors="replace")
    file_hash = _compute_file_hash(filepath)
    source_file = str(filepath.relative_to(filepath.parent.parent))
    lines = content.splitlines()

    stakeholders = []
    current_tier = None
    current_person_name = None
    current_person_role = None
    current_person_lines: list[str] = []
    in_tier4_table = False

    def _flush_person():
        """Save the current accumulated person data."""
        nonlocal current_person_name, current_person_role, current_person_lines
        if current_person_name and current_tier is not None:
            block = "\n".join(current_person_lines)
            engagement = _extract_bullet_value_flexible(
                current_person_lines,
                ["Engagement level", "Engagement"]
            )
            style = _extract_bullet_value_flexible(
                current_person_lines,
                ["Style", "Communication style"]
            )
            concerns = _extract_bullet_value_flexible(
                current_person_lines,
                ["Key concern", "Concern", "Risk", "Key tension"]
            )
            contributions = _extract_bullet_value_flexible(
                current_person_lines,
                ["Key contributions", "Key role", "Role", "Focus"]
            )
            stakeholders.append({
                "name": current_person_name,
                "tier": current_tier,
                "role": current_person_role,
                "engagement_level": engagement,
                "communication_style": style,
                "concerns": concerns,
                "key_contributions": contributions,
                "notes": block.strip() if block.strip() else None,
                "source_file": source_file,
                "file_hash": file_hash,
            })
        current_person_name = None
        current_person_role = None
        current_person_lines = []

    for line in lines:
        stripped = line.strip()

        # Detect tier headings: ## Tier N ...
        tier_match = re.match(r'^##\s+Tier\s+(\d+)', stripped)
        if tier_match:
            _flush_person()
            current_tier = int(tier_match.group(1))
            in_tier4_table = (current_tier == 4)
            continue

        # Detect other ## headings (like "## Dynamics to Watch") that end
        # the stakeholder sections
        if stripped.startswith("## ") and not tier_match:
            _flush_person()
            current_tier = None
            in_tier4_table = False
            continue

        if current_tier is None:
            continue

        # Handle Tier 4 table rows
        if in_tier4_table and current_tier == 4:
            if stripped.startswith("|") and not stripped.startswith("|---") and not stripped.startswith("| Person"):
                cols = [c.strip() for c in stripped.split("|")]
                # Filter empty strings from leading/trailing pipes
                cols = [c for c in cols if c]
                if len(cols) >= 2:
                    person_name = cols[0]
                    domain = cols[1] if len(cols) > 1 else ""
                    status = cols[2] if len(cols) > 2 else ""
                    stakeholders.append({
                        "name": person_name,
                        "tier": 4,
                        "role": domain,
                        "engagement_level": status if status else None,
                        "communication_style": None,
                        "concerns": None,
                        "key_contributions": None,
                        "notes": f"Domain: {domain}. Status: {status}" if status else f"Domain: {domain}",
                        "source_file": source_file,
                        "file_hash": file_hash,
                    })
            continue

        # For Tiers 1-3: detect ### Name -- Role headings
        person_match = re.match(r'^###\s+(.+?)\s*(?:—|--|---)\s*(.+)$', stripped)
        if person_match:
            _flush_person()
            current_person_name = person_match.group(1).strip()
            current_person_role = person_match.group(2).strip()
            continue

        # Accumulate bullet lines for current person
        if current_person_name:
            current_person_lines.append(line)

    # Flush last person
    _flush_person()

    return stakeholders
