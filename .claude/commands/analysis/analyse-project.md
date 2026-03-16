---
description: Retroactively analyse existing transcripts for a specific project and generate per-project summaries
allowed-tools: Bash, Read, Write, Edit, Glob, Grep, Agent
argument-hint: [project-name|project-slug]
---

# Analyse Project (Retroactive)

Scan existing transcripts and summaries for content related to a specific project and generate per-project summaries. Use when a new project is created and you want to backfill its history from existing meeting records.

## Arguments
$ARGUMENTS -- Project name or slug (optional; will prompt if not provided)

---

## Step 1: Identify Project

If $ARGUMENTS is provided, use it as the project name or slug. Otherwise, ask:
"Which project should I analyse? (name or ID)"

Fetch project details:
1. Try `GET /api/projects` if backend is running
2. Otherwise, check `analysis/projects/` for existing project directories
3. If neither works, ask the user for project details

Required project info:
- **name**: full project name
- **slug**: lowercase-hyphenated identifier (generate if missing: lowercase, replace spaces with hyphens, strip special characters)
- **description**: what the project is about
- **keywords**: terms likely to appear in transcripts when this project is discussed
- **key_stakeholders**: people most closely associated with this project

If the project does not exist in the system yet, ask the user to provide description, keywords, and key stakeholders. Create the directory: `mkdir -p "analysis/projects/{slug}/"`

---

## Step 2: Determine Date Range

If not specified in arguments, ask:
"What date range should I analyse? (e.g., 'last 2 weeks', '2026-02-15 to now', 'all')"

Parse the response:
- `last N weeks` -> start_date = today minus N weeks, end_date = today
- `YYYY-MM-DD to YYYY-MM-DD` -> explicit range
- `YYYY-MM-DD to now` -> start_date to today
- `all` -> scan every transcript available
- Default if ambiguous: last 2 weeks

**Important:** There is no value in scanning months-old transcripts for a project conceived last week. Guide the user toward a sensible range based on the project's creation date if known.

---

## Step 3: Load Context

Read these files in parallel:
1. `context/glossary.md` -- names and acronyms the transcript might use
2. `context/stakeholders.md` -- who is involved, roles, dynamics
3. All files in `context/projects/` -- per-project context
4. Project details from Step 1 (description, keywords, stakeholders)
5. `analysis/trackers/action_items.md` -- existing actions that may relate to this project
6. `analysis/trackers/risk_register.md` -- existing risks for cross-referencing

---

## Step 4: Scan Transcripts for Relevance

List all transcripts in the date range (files in `Transcripts/` whose normalised date falls within start_date to end_date).

For each transcript in the range:

1. **Check for existing summary first.** Look in `analysis/summaries/` for a matching summary file.
   - If a summary exists: read the summary (faster and more structured than raw transcript)
   - If no summary exists: read the raw transcript from `Transcripts/`

2. **Determine relevance.** Search the text (summary or transcript) for:
   - Project name (exact match, case-insensitive)
   - Project keywords (from project config)
   - Key stakeholder names (when discussing topics related to this project's domain)
   - Related project references (when discussing projects in a related context)

3. **Classify relevance level:**
   - **HIGH**: project was a primary discussion topic. Multiple exchanges, decisions made, actions assigned. The project name or core keywords appear 3+ times in substantive context.
   - **MEDIUM**: project received dedicated discussion. A segment of the meeting addressed it, or actions/decisions were raised about it. Keywords appear 1-2 times in substantive context.
   - **LOW**: project was briefly mentioned or tangentially referenced. A passing comment, a name-drop without discussion, or a side note.

4. **Skip irrelevant transcripts.** If none of the matching criteria hit, the transcript is not relevant to this project.

Report: "Scanning N transcripts in date range [start] to [end]..."

---

## Step 5: Generate Project Summaries

For each relevant transcript (HIGH or MEDIUM relevance), create a per-project summary.

Create `analysis/projects/{slug}/YYYY-MM-DD_-_Title.md`:

```markdown
# [Project Name] -- Extract from [Meeting Title]
**Date:** YYYY-MM-DD
**Source transcript:** [transcript filename]
**Relevance:** HIGH/MEDIUM
**Source:** [summary-derived / transcript-derived]

## Discussion Summary
[2-5 paragraphs describing what was discussed about THIS project specifically. Include:
- Context of the discussion (what prompted it)
- Key points raised
- Progress reported
- Blockers or concerns identified
- Decisions being weighed
Write as a narrative, not bullet points. Be specific -- "CSMs reported that blocker fields reset after deployment" is better than "data issues discussed".]

## Decisions (project-scoped)
- [Only decisions relevant to this project]
  - Type: explicit/implicit/deferred/non-decision
  - Owner: [name if identified]
  - Rationale: [if given]

## Action Items (project-scoped)
| Action | Owner | Deadline | Status |
|--------|-------|----------|--------|
| [actions specific to this project] | [name] | [date or "unspecified"] | Open |

## Risks & Concerns (project-scoped)
| Risk | Severity | Trajectory | Notes |
|------|----------|------------|-------|
| [risk specific to this project] | CRITICAL/HIGH/MEDIUM/LOW | new/escalating/stable/de-escalating | [context] |

## Stakeholder Signals (project-scoped)
| Person | Sentiment | Topic | Quote |
|--------|-----------|-------|-------|
| [name] | [sentiment] | [aspect of the project] | "[short quote]" |

## Key Quotes
- "[quote relevant to this project]" -- [Speaker]

## Connections to Other Projects
- [If the discussion linked this project to another project, note it here]
```

For LOW relevance transcripts, do NOT create a full project summary. Instead, add a brief entry to a tracking note at `analysis/projects/{slug}/mentions.md`:

```markdown
# [Project Name] -- Mentions Log

| Date | Meeting | Context | Quote |
|------|---------|---------|-------|
| YYYY-MM-DD | [meeting title] | [1-sentence context] | "[brief quote if any]" |
```

Create or append to this file as needed.

---

## Step 6: Update Trackers

For any new findings specific to this project discovered during scanning:

1. **Action items**: Append project-tagged actions to `analysis/trackers/action_items.md`
2. **Risks**: Append project-tagged risks to `analysis/trackers/risk_register.md`
3. **Decisions**: Append project-tagged decisions to `context/decisions.md`
4. **Sentiment signals**: If notable project-specific sentiment was found, append to `analysis/trackers/sentiment_tracker.md`

Tag every entry with the project slug so it can be filtered.

Only add entries that are genuinely new (not already captured in existing tracker files). Check before appending.

---

## Step 7: Trigger Backend Import

```bash
cd backend && python -m scripts.import_data --data-root .. --db-url "$DATABASE_URL"
```

If `$DATABASE_URL` is not set or the backend is unavailable, skip and tell the user: "Markdown files updated. Run the backend import to refresh the web app."

---

## Step 8: Report

Output a summary:

```
## Project Analysis Complete: [Project Name]

**Date range scanned:** [start_date] to [end_date]
**Transcripts scanned:** N total
**Relevant transcripts found:** N
  - HIGH relevance: N
  - MEDIUM relevance: N
  - LOW relevance (mentions only): N
  - Not relevant: N

**Project summaries created:** N
**Mentions logged:** N

**Tracker entries added:**
  - Actions: N
  - Risks: N
  - Decisions: N
  - Sentiment signals: N

**Key findings:**
1. [Most significant finding about this project's history]
2. [Second finding]
3. [Third finding]

**Project narrative arc:**
[2-3 sentences summarising how this project has evolved across the meetings analysed. When was it first discussed? How has the conversation changed? What's the current trajectory?]

**Backend import:** [success/skipped/failed]
```
