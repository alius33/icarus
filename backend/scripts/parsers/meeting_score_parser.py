"""
Parser for meeting scores from analysis/trackers/meeting_scores.md

Expected format:
## Meeting Scores

| Date | Meeting_Title | Type | Score | Decision_Velocity | Action_Clarity | Engagement_Balance | Topic_Completion | Follow_Through | Participants | Duration_Category |
|------|---------------|------|-------|-------------------|----------------|--------------------|--------------------|----------------|--------------|-------------------|
| 2026-02-10 | CLARA standup | status_update | 72 | 0.8 | 0.7 | 0.6 | 0.9 | 0.5 | 4 | short |
"""

import re
from datetime import date


def parse_meeting_scores(content: str) -> list[dict]:
    """Parse meeting scores markdown into a list of dicts."""
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
                and "Score" in stripped):
            in_table = True
            continue

        # Skip separator line
        if in_table and re.match(r"^\|[\s\-|]+\|$", stripped):
            continue

        # Parse table rows
        if in_table and stripped.startswith("|"):
            cells = [c.strip() for c in stripped.split("|")[1:-1]]
            if len(cells) >= 4:
                date_str = cells[0].strip()
                meeting_title = cells[1].strip() if len(cells) > 1 else None
                meeting_type = cells[2].strip().lower() if len(cells) > 2 else None
                score_str = cells[3].strip() if len(cells) > 3 else None
                decision_velocity_str = cells[4].strip() if len(cells) > 4 else None
                action_clarity_str = cells[5].strip() if len(cells) > 5 else None
                engagement_balance_str = cells[6].strip() if len(cells) > 6 else None
                topic_completion_str = cells[7].strip() if len(cells) > 7 else None
                follow_through_str = cells[8].strip() if len(cells) > 8 else None
                participants_str = cells[9].strip() if len(cells) > 9 else None
                duration_category = cells[10].strip().lower() if len(cells) > 10 else None

                parsed_date = None
                if date_str:
                    try:
                        parsed_date = date.fromisoformat(date_str)
                    except ValueError:
                        pass

                overall_score = 0
                if score_str:
                    try:
                        raw_score = float(score_str)
                        # If score is on 0-10 scale, convert to 0-100
                        if raw_score <= 10:
                            overall_score = int(round(raw_score * 10))
                        else:
                            overall_score = int(round(raw_score))
                        overall_score = max(0, min(100, overall_score))
                    except ValueError:
                        pass

                decision_velocity = _parse_subscore(decision_velocity_str)
                action_clarity = _parse_subscore(action_clarity_str)
                engagement_balance = _parse_subscore(engagement_balance_str)
                topic_completion = _parse_subscore(topic_completion_str)
                follow_through = _parse_subscore(follow_through_str)

                participant_count = None
                if participants_str:
                    try:
                        participant_count = int(participants_str)
                    except ValueError:
                        # participants_str might be names like "Richard, Azmain"
                        if "," in participants_str:
                            participant_count = len([p for p in participants_str.split(",") if p.strip()])
                        elif participants_str.strip():
                            participant_count = len([p for p in participants_str.split() if p.strip()])
                        else:
                            participant_count = None

                valid_types = {
                    "decision_making", "status_update", "brainstorming",
                    "escalation", "planning", "review", "onboarding",
                }
                if meeting_type and meeting_type not in valid_types:
                    meeting_type = None

                valid_durations = {"short", "medium", "long"}
                if duration_category and duration_category not in valid_durations:
                    duration_category = None

                results.append({
                    "date": parsed_date,
                    "meeting_title": meeting_title if meeting_title else None,
                    "meeting_type": meeting_type,
                    "overall_score": overall_score,
                    "decision_velocity": decision_velocity,
                    "action_clarity": action_clarity,
                    "engagement_balance": engagement_balance,
                    "topic_completion": topic_completion,
                    "follow_through": follow_through,
                    "participant_count": participant_count,
                    "duration_category": duration_category,
                })
        elif in_table and not stripped.startswith("|"):
            in_table = False

    return results


def _parse_subscore(value: str | None) -> float | None:
    """Parse a subscore, normalising 0-10 scale to 0.0-1.0."""
    if not value or value.upper() == "N/A":
        return None
    try:
        v = float(value)
        # If value is > 1.0, assume it's on 0-10 scale and normalise
        if v > 1.0:
            return round(v / 10.0, 2)
        return v
    except ValueError:
        return None


def _parse_float(value: str | None) -> float | None:
    """Safely parse a string to float, returning None on failure."""
    if not value:
        return None
    try:
        return float(value)
    except ValueError:
        return None
