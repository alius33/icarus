"""Tests for the transcript filename parser.

These are pure unit tests that do not require a database or HTTP client.
They exercise the date/title extraction logic in the transcript parser.
"""

import sys
from pathlib import Path

import pytest

# Add the backend directory to the path so we can import the parser directly
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from scripts.parsers.transcript_parser import _parse_date_and_title, _clean_title, _extract_participants


class TestParseDateAndTitle:
    """Test _parse_date_and_title with various filename formats."""

    def test_dd_mm_yyyy_separator(self):
        """DD-MM-YYYY_-_Title.txt format."""
        date, title = _parse_date_and_title("06-01-2026_-_Weekly_Standup.txt")
        assert date is not None
        assert date.year == 2026
        assert date.month == 1
        assert date.day == 6
        assert title == "Weekly Standup"

    def test_yyyy_mm_dd_separator(self):
        """YYYY-MM-DD_-_Title.txt format."""
        date, title = _parse_date_and_title("2026-03-07_-_CLARA_Sprint_Review.txt")
        assert date is not None
        assert date.year == 2026
        assert date.month == 3
        assert date.day == 7
        assert title == "CLARA Sprint Review"

    def test_yyyy_mm_dd_no_separator(self):
        """YYYY-MM-DD_Title.txt format (no _-_ separator)."""
        date, title = _parse_date_and_title("2026-02-14_Stakeholder_Alignment.txt")
        assert date is not None
        assert date.year == 2026
        assert date.month == 2
        assert date.day == 14
        assert title == "Stakeholder Alignment"

    def test_yyyy_mm_dd_timestamp_only(self):
        """YYYY-MM-DD_HH-MM-SS.txt format (no title)."""
        date, title = _parse_date_and_title("2026-01-15_14-30-00.txt")
        assert date is not None
        assert date.year == 2026
        assert date.month == 1
        assert date.day == 15
        assert "14:30:00" in title

    def test_yyyy_mm_dd_space_dash_separator(self):
        """YYYY-MM-DD - Title.txt format."""
        date, title = _parse_date_and_title("2026-03-01 - Programme Review.txt")
        assert date is not None
        assert date.year == 2026
        assert date.month == 3
        assert date.day == 1
        assert title == "Programme Review"

    def test_dd_mm_yyyy_space_dash_separator(self):
        """DD-MM-YYYY - Title.txt format."""
        date, title = _parse_date_and_title("01-03-2026 - Programme Review.txt")
        assert date is not None
        assert date.year == 2026
        assert date.month == 3
        assert date.day == 1
        assert title == "Programme Review"

    def test_yyyy_mm_dd_space_separator(self):
        """YYYY-MM-DD Title.txt format."""
        date, title = _parse_date_and_title("2026-02-20 Quick Sync.txt")
        assert date is not None
        assert date.year == 2026
        assert date.month == 2
        assert date.day == 20
        assert title == "Quick Sync"

    def test_unrecognised_format_returns_none_date(self):
        """Filenames without a recognisable date pattern return None date."""
        date, title = _parse_date_and_title("random_meeting_notes.txt")
        assert date is None
        assert title == "random meeting notes"

    def test_suffix_removal(self):
        """Trailing __1_ suffixes are stripped from titles."""
        date, title = _parse_date_and_title("2026-03-01_-_Sprint_Demo__1_.txt")
        assert title == "Sprint Demo"

    def test_parenthetical_suffix_removal(self):
        """Trailing (1) suffixes are stripped from titles."""
        date, title = _parse_date_and_title("2026-03-01_-_Sprint_Demo(2).txt")
        assert title == "Sprint Demo"


class TestCleanTitle:
    """Test the _clean_title helper."""

    def test_underscores_to_spaces(self):
        assert _clean_title("Hello_World") == "Hello World"

    def test_trailing_number_suffix(self):
        assert _clean_title("Meeting_Notes__2_") == "Meeting Notes"

    def test_multiple_spaces_collapsed(self):
        assert _clean_title("Too   Many    Spaces") == "Too Many Spaces"


class TestExtractParticipants:
    """Test participant extraction from transcript content."""

    def test_extracts_speakers(self):
        content = (
            "Alice Smith  0:01\n"
            "Hello everyone, let's get started.\n"
            "\n"
            "Bob Jones  0:15\n"
            "Sounds good.\n"
            "\n"
            "Alice Smith  0:30\n"
            "Great, moving on.\n"
        )
        participants = _extract_participants(content)
        assert "Alice Smith" in participants
        assert "Bob Jones" in participants
        assert len(participants) == 2

    def test_empty_content_returns_empty(self):
        assert _extract_participants("") == []

    def test_no_speakers_returns_empty(self):
        content = "Just some plain text without speaker lines."
        assert _extract_participants(content) == []
