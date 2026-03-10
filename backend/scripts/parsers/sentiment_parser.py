"""
Parser for sentiment signals from analysis/trackers/sentiment_tracker.md

Expected format:
## Sentiment Tracker

| Date | Person | Sentiment | Shift | Topic | Quote |
|------|--------|-----------|-------|-------|-------|
| 2026-02-10 | Richard Purcell | cautious | STABLE | CLARA rollout | "Let's see how it goes" |
"""

import re
from datetime import date


def parse_sentiments(content: str) -> list[dict]:
    """Parse sentiment tracker markdown into a list of dicts."""
    results = []

    lines = content.strip().split("\n")
    in_table = False

    for line in lines:
        stripped = line.strip()

        # Skip empty lines and headers
        if not stripped or stripped.startswith("#"):
            continue

        # Detect table header
        if "|" in stripped and "Date" in stripped and "Person" in stripped:
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
                person = cells[1].strip()
                sentiment = cells[2].strip().lower()
                shift = cells[3].strip().upper() if len(cells) > 3 else None
                topic = cells[4].strip() if len(cells) > 4 else None
                quote = cells[5].strip().strip('"') if len(cells) > 5 else None

                parsed_date = None
                if date_str:
                    try:
                        parsed_date = date.fromisoformat(date_str)
                    except ValueError:
                        pass

                valid_sentiments = {
                    "champion", "supportive", "neutral", "cautious",
                    "frustrated", "resistant", "disengaged",
                }
                if sentiment not in valid_sentiments:
                    sentiment = "neutral"

                valid_shifts = {"UP", "DOWN", "STABLE", "NEW"}
                if shift and shift not in valid_shifts:
                    shift = "STABLE"

                results.append({
                    "person": person,
                    "date": parsed_date,
                    "sentiment": sentiment,
                    "shift": shift,
                    "topic": topic,
                    "quote": quote,
                })
        elif in_table and not stripped.startswith("|"):
            in_table = False

    return results
