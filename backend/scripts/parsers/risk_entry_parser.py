"""
Parser for risk entries from analysis/trackers/risk_register.md

Expected format:
## Risk Register

| Date | Risk_ID | Title | Description | Category | Severity | Trajectory | Source_Type | Owner | Mitigation | Last_Reviewed | Meetings_Mentioned | Confidence |
|------|---------|-------|-------------|----------|----------|------------|-------------|-------|------------|---------------|--------------------|-----------|
| 2026-02-10 | R-001 | Token cost overrun | Monthly costs exceeding budget | resource | HIGH | escalating | explicit | Richard | Cap at 500k tokens | 2026-02-10 | 3 | HIGH |
"""

import re
from datetime import date


def parse_risk_entries(content: str) -> list[dict]:
    """Parse risk register markdown into a list of dicts."""
    results = []

    lines = content.strip().split("\n")
    in_table = False

    for line in lines:
        stripped = line.strip()

        # Skip empty lines and headers
        if not stripped or stripped.startswith("#"):
            continue

        # Detect table header
        if ("|" in stripped and "Date" in stripped
                and "Risk_ID" in stripped and "Title" in stripped):
            in_table = True
            continue

        # Skip separator line
        if in_table and re.match(r"^\|[\s\-|]+\|$", stripped):
            continue

        # Parse table rows
        if in_table and stripped.startswith("|"):
            cells = [c.strip() for c in stripped.split("|")[1:-1]]
            if len(cells) >= 6:
                date_str = cells[0].strip()
                risk_id = cells[1].strip()
                title = cells[2].strip()
                description = cells[3].strip() if len(cells) > 3 else None
                category = cells[4].strip().lower() if len(cells) > 4 else None
                severity = cells[5].strip().upper() if len(cells) > 5 else "MEDIUM"
                trajectory = cells[6].strip().lower() if len(cells) > 6 else None
                source_type = cells[7].strip().lower() if len(cells) > 7 else None
                owner = cells[8].strip() if len(cells) > 8 else None
                mitigation = cells[9].strip() if len(cells) > 9 else None
                last_reviewed_str = cells[10].strip() if len(cells) > 10 else None
                meetings_mentioned_str = cells[11].strip() if len(cells) > 11 else None
                confidence = cells[12].strip().upper() if len(cells) > 12 else None

                parsed_date = None
                if date_str:
                    try:
                        parsed_date = date.fromisoformat(date_str)
                    except ValueError:
                        pass

                parsed_last_reviewed = None
                if last_reviewed_str:
                    try:
                        parsed_last_reviewed = date.fromisoformat(last_reviewed_str)
                    except ValueError:
                        parsed_last_reviewed = None

                meetings_mentioned = 1
                if meetings_mentioned_str:
                    try:
                        meetings_mentioned = int(meetings_mentioned_str)
                    except ValueError:
                        pass

                valid_categories = {
                    "technical", "operational", "strategic",
                    "resource", "stakeholder", "scope",
                }
                if category and category not in valid_categories:
                    category = None

                valid_severities = {"CRITICAL", "HIGH", "MEDIUM", "LOW"}
                if severity not in valid_severities:
                    severity = "MEDIUM"

                valid_trajectories = {
                    "escalating", "stable", "de-escalating",
                    "new", "resolved",
                }
                if trajectory and trajectory not in valid_trajectories:
                    trajectory = None

                valid_source_types = {"explicit", "implicit", "absence_inferred"}
                if source_type and source_type not in valid_source_types:
                    source_type = None

                valid_confidences = {"HIGH", "MEDIUM", "LOW"}
                if confidence and confidence not in valid_confidences:
                    confidence = None

                results.append({
                    "date": parsed_date,
                    "risk_id": risk_id,
                    "title": title,
                    "description": description if description else None,
                    "category": category,
                    "severity": severity,
                    "trajectory": trajectory,
                    "source_type": source_type,
                    "owner": owner if owner else None,
                    "mitigation": mitigation if mitigation else None,
                    "last_reviewed": parsed_last_reviewed,
                    "meetings_mentioned": meetings_mentioned,
                    "confidence": confidence,
                })
        elif in_table and not stripped.startswith("|"):
            in_table = False

    return results
