---
globs: Transcripts/**, analysis/summaries/**, analysis/weekly/**
---

# Transcript & Analysis File Handling

- Two date formats exist: `DD-MM-YYYY_-_Title.txt` (older) and `YYYY-MM-DD_-_Title.txt` (newer)
- New transcripts should use: `YYYY-MM-DD_-_Short_Descriptive_Title.txt`
- Transcript files may have `\r\r\n` line endings — use Python for edits, not the Edit tool
- The action items tracker (`analysis/trackers/action_items.md`) is very large (1040+ lines) — read tail with offset to append, never read the whole file
- Summary filenames must match transcript dates: normalise `DD-MM-YYYY` → `YYYY-MM-DD` when checking for existing summaries
- Summaries MUST include `**Primary project:**` and `**Secondary projects:**` headers — the import pipeline uses these to auto-create ProjectSummary and ProjectLink entries
