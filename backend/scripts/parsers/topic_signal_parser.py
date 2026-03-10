"""
Parser for topic signals from analysis/trackers/topic_tracker.md

Expected format:
## Topic Tracker

| Date | Topic | Category | Intensity | First_Raised | Meetings_Count | Trend | Key_Quote | Confidence |
|------|-------|----------|-----------|--------------|----------------|-------|-----------|------------|
| 2026-02-10 | CLARA rollout | strategic | HIGH | 2026-01-15 | 5 | rising | "We need to move fast" | HIGH |
"""

import re
from datetime import date


def parse_topic_signals(content: str) -> list[dict]:
    """Parse topic tracker markdown into a list of dicts."""
    results = []

    lines = content.strip().split("\n")
    in_table = False

    for line in lines:
        stripped = line.strip()

        # Skip empty lines and headers
        if not stripped or stripped.startswith("#"):
            continue

        # Detect table header
        if "|" in stripped and "Date" in stripped and "Topic" in stripped:
            in_table = True
            continue

        # Skip separator line
        if in_table and re.match(r"^\|[\s\-|]+\|$", stripped):
            continue

        # Parse table rows
        if in_table and stripped.startswith("|"):
            cells = [c.strip() for c in stripped.split("|")[1:-1]]
            if len(cells) >= 2:
                date_str = cells[0].strip()
                topic = cells[1].strip()
                category = cells[2].strip().lower() if len(cells) > 2 else None
                intensity = cells[3].strip().upper() if len(cells) > 3 else None
                first_raised = cells[4].strip() if len(cells) > 4 else None
                meetings_count_str = cells[5].strip() if len(cells) > 5 else None
                trend = cells[6].strip().lower() if len(cells) > 6 else None
                key_quote = cells[7].strip().strip('"') if len(cells) > 7 else None
                confidence = cells[8].strip().upper() if len(cells) > 8 else None

                parsed_date = None
                if date_str:
                    try:
                        parsed_date = date.fromisoformat(date_str)
                    except ValueError:
                        pass

                parsed_first_raised = None
                if first_raised:
                    try:
                        parsed_first_raised = date.fromisoformat(first_raised)
                    except ValueError:
                        parsed_first_raised = None

                meetings_count = 1
                if meetings_count_str:
                    try:
                        meetings_count = int(meetings_count_str)
                    except ValueError:
                        pass

                valid_categories = {
                    "technical", "strategic", "interpersonal",
                    "operational", "governance",
                }
                if category and category not in valid_categories:
                    category = None

                valid_intensities = {"CRITICAL", "HIGH", "MEDIUM", "LOW"}
                if intensity and intensity not in valid_intensities:
                    intensity = None

                valid_trends = {"rising", "stable", "declining", "new"}
                if trend and trend not in valid_trends:
                    trend = None

                valid_confidences = {"HIGH", "MEDIUM", "LOW"}
                if confidence and confidence not in valid_confidences:
                    confidence = None

                results.append({
                    "date": parsed_date,
                    "topic": topic,
                    "category": category,
                    "intensity": intensity,
                    "first_raised": parsed_first_raised,
                    "meetings_count": meetings_count,
                    "trend": trend,
                    "key_quote": key_quote if key_quote else None,
                    "confidence": confidence,
                })
        elif in_table and not stripped.startswith("|"):
            in_table = False

    return results
