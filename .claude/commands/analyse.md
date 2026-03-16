# Analyse New Transcripts

You are an executive assistant processing new meeting transcripts for the Icarus programme. Follow the pipeline below exactly.

## Step 0: Detect New Transcripts

List all `.txt` files in `Transcripts/` and all `.md` files in `analysis/summaries/`. A transcript is "new" if there is no matching summary file. To match:
- Normalise the transcript filename: convert `DD-MM-YYYY` dates to `YYYY-MM-DD`, replace `___` with `_-_`, strip special characters to match the summary naming convention
- If no summary exists with a matching date and title stem, the transcript is new

If there are no new transcripts, tell the user and stop.

Report what you found: "Found X new transcript(s) to process: [list filenames]"

## Step 1: Load Context

Read these files (in parallel) to understand the current programme state:
1. `context/glossary.md`
2. `context/stakeholders.md`
3. All files in `context/projects/` — per-project context
4. The most recent file in `analysis/weekly/` (sort by filename, take the last one)
5. (If backend running) Current wins via `GET /api/wins` and outreach via `GET /api/outreach` — to avoid duplicates when extracting new ones

## Step 2: Summarise Each Transcript

For each new transcript, read the full `.txt` file and create a summary at `analysis/summaries/YYYY-MM-DD_-_Title.md` following the enhanced summary template in `/analyse-deep` (Step 3). At minimum include: title, date, attendees, duration context, primary/secondary projects, key points, decisions, action items, stakeholder signals, open questions, and raw quotes.

The summary must include these additional sections (appended after the standard sections):

### Sentiment Signals
| Person | Sentiment | Shift | Topic | Quote |
|--------|-----------|-------|-------|-------|
| ... | ... | ... | ... | ... |

### Commitments Made
| Person | Commitment | Implied Deadline | Condition |
|--------|------------|------------------|-----------|
| ... | ... | ... | ... |

### Cross-Project Impacts
- **[Source] → [Target]** ([link_type]): [description]

### Suggested Actions (Unassigned)
- [Description of thing discussed but not committed to]

### Programme Wins Detected
| Category | Title | Description | Project | Confidence |
|----------|-------|-------------|---------|------------|
(Only include if concrete achievements were discussed — shipped features, adoption numbers, time savings, process improvements. Leave empty if none.)

### Outreach Signals
| Contact | Division | Signal Type | Detail |
|---------|----------|-------------|--------|
(Only include if cross-divisional engagement signals detected — new contacts, status changes, meetings, next steps. Leave empty if none.)

Process transcripts in parallel where possible (use agents for batches of 3+).

## Step 3: Update Context Files

After all summaries are written, review them collectively and update:
- `context/decisions.md` — append any new decisions (with date)
- `context/open_threads.md` — add new threads, mark resolved ones as CLOSED (with date)
- `context/stakeholders.md` — update if roles, attitudes, or dynamics shifted
- `context/projects/*.md` — update project context if there's meaningful progress
- `analysis/trackers/action_items.md` — add new actions, update existing ones
- `analysis/trackers/sentiment_tracker.md` — add sentiment signals extracted from transcripts
- `analysis/trackers/commitments.md` — add commitments made, update status of existing ones
- Programme Wins (via API if backend running): `POST /api/wins` for each new win detected in transcripts. Check loaded wins to avoid duplicates. Set `date_recorded` to transcript date, add `notes: "Auto-extracted from: [filename]"`. Categories: time_saved, adoption, quality, reach, process_improvement.
- Outreach (via API if backend running): `POST /api/outreach` for new cross-divisional contacts, `PATCH /api/outreach/{id}` for status/meeting updates on existing contacts. Set `last_contact_date` to transcript date.

Only update files where there are actual changes. Don't touch files for no reason.

## Step 4: Update Weekly Summaries

Determine which ISO weeks the new transcripts fall into. For each affected week:

1. Read the **previous week's** weekly summary (the one before the affected week)
2. Read **all** summaries for that week (both existing and newly created)
3. Either create or update `analysis/weekly/week-of-YYYY-MM-DD.md` (Monday date)

**CRITICAL:** Each weekly summary must follow on from the previous week. This is a continuous executive briefing. Reference last week's state, carry forward unresolved items, note trajectory changes. Follow the enhanced weekly summary template in `/analyse-deep` (Step 10).

If updating an existing weekly summary (because new transcripts were added to a week that already had some), regenerate the full summary incorporating all transcripts for that week — don't just append.

## Step 5: Trigger Backend Import

After all files are written, run the backend import to refresh the database:
```bash
cd backend && python -m scripts.import_data --data-root .. --db-url "$DATABASE_URL"
```

If `$DATABASE_URL` is not set or the backend is not available, skip this step and tell the user: "Markdown files updated. Run the backend import to refresh the web app."

## Step 6: Report

Summarise what was done:
- How many transcripts were processed
- Which weekly summaries were created/updated
- Which context files were updated
- Any notable findings (key decisions, risks, stakeholder shifts)
- Programme wins logged (new/skipped)
- Outreach contacts created/updated
- Whether the backend import succeeded
