# Analyse New Transcripts (Cowork Task)

Process all unprocessed transcripts through the full analysis pipeline with parallel agents.

## Task Definition

This task detects new transcripts, creates individual call summaries, updates weekly summaries, and refreshes all context trackers.

## Agents

### Agent 1: Detector & Context Loader
**Role:** Identify new transcripts and prepare shared context.

1. List all `.txt` files in `Transcripts/` and all `.md` files in `analysis/summaries/`
2. Identify which transcripts have no matching summary (normalise filenames: convert `DD-MM-YYYY` → `YYYY-MM-DD`, match stems)
3. Read `context/glossary.md`, `context/stakeholders.md`, `context/workstreams.md`
4. Read the most recent weekly summary from `analysis/weekly/`
5. Write the list of new transcripts and affected weeks to a shared note for other agents

If no new transcripts found, report this and all agents should stop.

### Agent 1b: Load Transcript Context (Notes & Attachments)
**Role:** Gather any analyst notes and attachment text for each new transcript.
**Depends on:** Agent 1 completing detection.

For each new transcript, check for supporting context:

**If backend is running** (local dev with Docker):
  `GET /api/transcripts/{id}/context`
  Returns notes text + extracted attachment text.

**If offline** (filesystem only):
  Check `analysis/context_notes/{YYYY-MM-DD_-_Title}.md`
  Contains analyst notes + extracted text from all attachments.

If context exists, include it in the analysis prompt for that transcript:
- Prepend analyst notes as "## Analyst Notes" section
- Include each attachment's extracted text as "## Supporting Document: {filename}"
- Reference these in the summary under "## Supporting Context Available"

### Agent 2: Summariser (Batch A)
**Role:** Summarise the first half of new transcripts.
**Depends on:** Agent 1 and 1b completing.

For each assigned transcript:
1. Read the full `.txt` file from `Transcripts/`
2. If context notes exist (from Agent 1b), include them as additional analysis context
3. Create `analysis/summaries/YYYY-MM-DD_-_Title.md` following the summary template in CLAUDE.md
4. Be specific, track sentiment, note contradictions, distinguish decisions from discussions
5. If analyst notes or attachments were used, add a "## Supporting Context Available" section at the end

### Agent 3: Summariser (Batch B)
**Role:** Summarise the second half of new transcripts.
**Depends on:** Agent 1 completing detection.

Same as Agent 2 (including context notes from Agent 1b), for the remaining transcripts.

### Agent 4: Weekly Summary & Context Updater
**Role:** Generate/update weekly summaries and context files.
**Depends on:** Agents 2 and 3 completing all summaries.

1. Read ALL summaries for each affected week (both old and newly created)
2. Read the previous week's weekly summary for continuity
3. Create or regenerate `analysis/weekly/week-of-YYYY-MM-DD.md` for each affected week
   - **Each weekly summary MUST follow on from the previous week** — this is a continuous executive briefing
   - Reference last week's state, carry forward unresolved items, note trajectory changes
   - Follow the weekly summary template in CLAUDE.md exactly
4. Update context files:
   - `context/decisions.md` — append new decisions
   - `context/open_threads.md` — add/close threads
   - `context/stakeholders.md` — update if dynamics shifted
   - `context/workstreams.md` — update if meaningful progress
   - `analysis/trackers/action_items.md` — add/update actions

### Agent 5: Import & Report
**Role:** Trigger backend import and report results.
**Depends on:** Agent 4 completing.

1. Run: `cd backend && python -m scripts.import_data --data-root .. --db-url "$DATABASE_URL"`
2. If backend not available, note it for the user
3. Compile final report: transcripts processed, weekly summaries updated, context changes, notable findings

## File Locking

- Agents 2 and 3 write to **different summary files** (no overlap)
- Only Agent 4 writes to context files and weekly summaries (no conflicts)
- Only Agent 5 runs the import

## Context Files for All Agents

Every agent should read `CLAUDE.md` at session start for the analysis guidelines and templates.
