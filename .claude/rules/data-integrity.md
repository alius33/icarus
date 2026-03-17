---
globs: analysis/trackers/**, context/**, backend/scripts/import*
---

# Data Integrity Rules

- Import is idempotent (SHA256 hash dedup) — safe to re-run repeatedly
- Transcripts uploaded via the frontend go ONLY to the database, not the filesystem. Always check API for `has_summary: false` when detecting new transcripts.
- "Sales Recon" is NOT a project — it's another team's product. Never create a project for it.
- Before appending to any tracker file, check if the entry already exists. Never create duplicate entries.
- ProjectSummary and ProjectLink entries are auto-created by import_data.py from `**Primary project:**` headers — no manual API calls needed.
- When updating `context/stakeholders.md`, preserve the existing tier structure and engagement levels. Only update what has observably changed.
- When closing threads in `context/open_threads.md`, add the resolution date and summary, don't just delete the entry.
- **Never overwrite update content**: When PATCHing a project update, only include the fields you are changing (e.g. `summary`). Never include `content` in the payload — the backend has a length guard but the rule is: don't send it.
