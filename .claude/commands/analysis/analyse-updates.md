# Analyse Project Updates

You are an executive assistant processing project updates for the Icarus programme. These are free-text notes and Teams chat conversations that the user has added via the web app. Follow the pipeline below.

## Step 0: Fetch Unprocessed Updates

Call the API to get unprocessed project updates:

```
GET http://localhost:8000/api/project-updates/unprocessed
```

If the API is unreachable, try the Railway URL. If no unprocessed updates exist, tell the user and stop.

Report: "Found X unprocessed update(s) to analyse: [list titles with dates]"

## Step 1: Load Context

Read these files (in parallel) to understand the current programme state:
1. `context/glossary.md`
2. `context/stakeholders.md`
3. All files in `context/projects/` — per-project context
4. The most recent file in `analysis/weekly/` (sort by filename, take the last one)
5. Read the tail of `analysis/trackers/action_items.md` (use offset — file is 1000+ lines) to know the current action item count for appending

## Step 2: Analyse Each Update

For each unprocessed update, read its full content (from the API response) and extract:

### Decisions
- Look for explicit or implicit decisions. Include who decided, what was decided, and any rationale.
- Format: `| # | Date | Decision | Rationale | Key People | Status |`
- Append to `context/decisions.md`

### Action Items
- Look for tasks, to-dos, follow-ups, and commitments to act.
- Format: `| # | Date | Action | Owner | Deadline | Context | Source |`
- Source should be: `Project Update #{id} — "{title}"`
- Append to `analysis/trackers/action_items.md`

### Commitments
- Personal commitments made by named individuals.
- Append to `analysis/trackers/commitments.md`

### Risks
- New risks or updates to existing risks.
- Check existing risks in `analysis/trackers/risk_register.md` before creating duplicates.
- Append new risks or update existing risk trajectories.

### Stakeholder Signals
- Sentiment changes, new relationships, engagement shifts.
- Update `context/stakeholders.md` if warranted (preserve tier structure).
- Append sentiment signals to `analysis/trackers/sentiment_tracker.md`

### Open Threads
- New unresolved questions or topics needing follow-up.
- Append to `context/open_threads.md`

**Source attribution**: Always attribute extracted items to `Project Update #{id} — "{title}"` rather than a transcript filename.

**Before appending**: Check if the entry already exists. Never create duplicate entries.

## Step 3: Write Update Summary

For each processed update, create a summary file at:
```
analysis/updates/YYYY-MM-DD_-_Slug_Title.md
```

Use the update's `created_at` date. The file should contain:

```markdown
# Project Update: {title}

**Date:** YYYY-MM-DD
**Projects:** {comma-separated project names}
**Content type:** {note | teams_chat}
**Source:** Project Update #{id}

## Content

{The full update content, parsed if Teams chat}

## Extracted Items

### Decisions
{List any decisions found, or "None identified"}

### Action Items
{List any action items found, or "None identified"}

### Commitments
{List any commitments found, or "None identified"}

### Risks
{List any risks found, or "None identified"}

### Stakeholder Signals
{List any signals found, or "None identified"}
```

## Step 4: Update Weekly Summary

Check if a weekly summary exists for the update's week (`analysis/weekly/week-of-YYYY-MM-DD.md` where the date is the Monday of that week).

- If it exists, append a "## Project Updates" section (or update if one already exists)
- If it doesn't exist yet, note this for when a weekly summary is generated

## Step 5: Mark as Processed

For each successfully processed update, call:
```
PATCH http://localhost:8000/api/project-updates/{id}/processed
```

## Step 6: Report

Provide a summary report:
- Number of updates processed
- Items extracted per category (decisions, actions, commitments, risks, signals)
- Files created/modified
- Any issues encountered

Remind the user to commit and push: `git add analysis/ context/ && git commit -m "Analyse project updates" && git push`
