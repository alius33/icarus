# Icarus — Customer Success Gen AI Programme Analysis

## What This Project Is

This is an analytical workspace **with a full web application** for tracking and analysing the Customer Success Gen AI Programme at Moody's Analytics (Insurance division). The programme runs six workstreams and has been active since January 2026. The primary tool being built is **CLARA** — an IRP adoption tracker.

There are TWO distinct types of work in this project:
1. **Transcript analysis** — processing meeting transcripts into summaries, weekly reports, and tracker updates (markdown files)
2. **App development** — building and maintaining the Icarus web app that displays all this analysis

## The Icarus Web App

The app is a **Next.js frontend + FastAPI backend** that reads the markdown analysis files and serves them through a web interface.

### Frontend (`frontend/`)
- **Framework:** Next.js 14 (App Router) with TypeScript, Tailwind CSS
- **Port:** 3000
- **Key routes:**
  - `/` — Dashboard (programme pulse, needs attention, activity feed)
  - `/transcripts` — Transcript list and detail views
  - `/upload` — Drag-and-drop transcript upload
  - `/analysis/summaries` — Per-call summary list and detail
  - `/analysis/weekly` — Weekly report list and detail
  - `/projects` — Project hub (workstream + custom projects)
  - `/projects/[id]` — Project detail with tabbed view (overview shows weekly summaries first, then drill into calls)
  - `/workstreams`, `/stakeholders`, `/decisions`, `/action-items`, `/open-threads`, `/glossary`, `/timeline`, `/search`
- **Key files:**
  - `frontend/src/app/layout.tsx` — Root layout with sidebar
  - `frontend/src/app/page.tsx` — Dashboard
  - `frontend/src/app/projects/[id]/page.tsx` — Project detail (tabs: overview, transcripts, summaries, decisions, actions, threads, stakeholders)
  - `frontend/src/components/` — Shared components (Sidebar, Header, MarkdownContent, ProjectTabBar, CopyBriefButton)
  - `frontend/src/components/projects/` — Tab components (ProjectOverviewTab, ProjectTranscriptsTab, etc.)
  - `frontend/src/lib/api.ts` — API client (`fetchApi<T>()` wrapper, all endpoints)
  - `frontend/src/lib/types.ts` — TypeScript interfaces (30+ types)
  - `frontend/src/lib/utils.ts` — Helpers (cn, statusColor, formatDate, ragDotColor)
- **Data:** All data comes from the backend API, NOT the filesystem. Server components use `INTERNAL_API_URL` (default: `http://backend:8000`), client components use `NEXT_PUBLIC_API_URL` (default: `http://localhost:8000`).

### Backend (`backend/`)
- **Framework:** FastAPI with async SQLAlchemy 2.0, PostgreSQL, Alembic migrations
- **Port:** 8000
- **API prefix:** `/api`
- **Key routes:**
  - `GET /api/dashboard` — Programme dashboard metrics
  - `GET /api/dashboard/brief` — Text-based leadership brief
  - `GET|POST /api/transcripts` — List, detail, upload
  - `GET /api/summaries` — List and detail
  - `GET /api/weekly-reports` — List and detail
  - `GET /api/projects` — CRUD + hub + weekly timeline
  - `GET /api/projects/{id}/hub` — All linked entities for a project
  - `GET /api/projects/{id}/weekly` — Weekly timeline (buckets by ISO week)
  - `POST /api/import/trigger` — Trigger re-import of markdown files into DB
  - `GET /api/search` — Full-text search across all entities
  - Plus: `/api/workstreams`, `/api/stakeholders`, `/api/decisions`, `/api/action-items`, `/api/open-threads`, `/api/glossary`, `/api/timeline`
- **Key files:**
  - `backend/app/main.py` — FastAPI app setup
  - `backend/app/config.py` — Settings (DATABASE_URL, CORS_ORIGINS, DATA_ROOT)
  - `backend/app/routers/` — One router per entity type
  - `backend/app/models/` — SQLAlchemy ORM models
  - `backend/app/schemas/` — Pydantic request/response schemas
  - `backend/app/services/upload_service.py` — Transcript upload processing + mention rebuilding
  - `backend/scripts/import_data.py` — Bulk import orchestrator (reads all markdown → DB)
  - `backend/scripts/parsers/` — File parsers (transcript, decision, action_item, stakeholder, workstream, glossary, open_thread)
- **Data flow:** Backend reads markdown files from the Icarus project root (`Transcripts/`, `analysis/`, `context/`), parses them, and stores structured data in PostgreSQL. Frontend queries the API.

### How the Pipeline Works
```
User uploads .txt transcripts (via web UI or drops into Transcripts/)
    ↓
Claude analyses transcripts → creates markdown summaries + weekly reports
    ↓
Backend import script reads markdown → parses → stores in PostgreSQL
    ↓
Frontend displays everything via API
```

## Project Structure

```
icarus/
├── CLAUDE.md                    # You are here — project instructions
├── programme_debrief.md         # Master debrief (Jan 6 – Feb 27, 2026)
├── Transcripts/                 # Raw meeting transcripts (.txt)
├── analysis/
│   ├── summaries/               # Per-transcript structured summaries
│   ├── weekly/                  # Weekly rollup reports
│   └── trackers/                # Running trackers (actions, risks, etc.)
├── context/                     # Reference files — read these for background
│   ├── stakeholders.md          # People, roles, dynamics
│   ├── workstreams.md           # Six workstreams — status & history
│   ├── glossary.md              # Names, acronyms, systems, jargon
│   ├── decisions.md             # Decision log with rationale
│   └── open_threads.md          # Unresolved questions & threads
├── frontend/                    # Next.js 14 web app (see above)
├── backend/                     # FastAPI + PostgreSQL (see above)
├── cowork/                      # Cowork task definitions
│   └── README.md                # How to use cowork with this project
└── .claude/
    └── commands/                # Slash commands (e.g. /analyse)
        └── analyse.md           # Process new transcripts end-to-end
```

## Context Files — Read Order

When starting a new session, read these in order for fastest ramp-up:
1. `context/glossary.md` — so you recognise names and acronyms
2. `context/stakeholders.md` — so you understand who matters and why
3. `context/workstreams.md` — current state of the six workstreams
4. `programme_debrief.md` — full chronological history (read sections as needed, not always cover-to-cover)

## Transcript Naming Convention

Transcripts use two date formats (both are valid):
- `DD-MM-YYYY_-_Title.txt` (earlier transcripts)
- `YYYY-MM-DD_-_Title.txt` (later transcripts)

When adding new transcripts, use: `YYYY-MM-DD_-_Short_Descriptive_Title.txt`

## Core Workflow: Processing New Transcripts

Use `/analyse` in Claude Code or run the cowork task `analyse-transcripts`. Both follow the same pipeline:

### Step 0. Detect new transcripts

Compare `Transcripts/*.txt` filenames against `analysis/summaries/*.md`. Any transcript without a matching summary is "new" and needs processing. The matching logic: normalise the transcript filename to `YYYY-MM-DD_-_Title` format and check if a summary with that stem exists.

### Step 1. Load context

Read these files to understand the current programme state before analysing:
1. `context/glossary.md` — names and acronyms
2. `context/stakeholders.md` — who matters and current dynamics
3. `context/workstreams.md` — current workstream status
4. The **most recent weekly summary** in `analysis/weekly/` — this is critical for continuity

### Step 2. Summarise each transcript → `analysis/summaries/`

Create `analysis/summaries/YYYY-MM-DD_-_Title.md` with this structure:

```markdown
# [Meeting Title]
**Date:** YYYY-MM-DD
**Attendees:** [names mentioned]
**Duration context:** [short/medium/long based on transcript length]
**Workstreams touched:** [list which of the 6 workstreams are relevant]

## Key Points
- [Bullet points — what was discussed, decided, revealed]

## Decisions Made
- [Decision]: [rationale if given] → [owner if identified]

## Action Items
| Action | Owner | Deadline | Status |
|--------|-------|----------|--------|
| ... | ... | ... | Open |

## Stakeholder Signals
- [Notable positions, concerns, shifts in attitude from key people]

## Open Questions Raised
- [Questions that came up but weren't resolved]

## Raw Quotes of Note
- "[Exact quote]" — [Speaker], on [topic]
```

### Step 3. Update running trackers

After summarising, update these files if relevant:
- `context/decisions.md` — add any new decisions
- `context/open_threads.md` — add new threads, close resolved ones
- `context/stakeholders.md` — update if roles, attitudes, or dynamics shift
- `context/workstreams.md` — update status if there's meaningful progress
- `analysis/trackers/action_items.md` — add new actions, update existing

### Step 4. Update weekly summaries → `analysis/weekly/`

This is the most important output. Weekly summaries are the **primary view** in the app — they are what the user sees when they open a project page, before drilling into individual call summaries.

For every week that had new transcripts processed, either **create** or **update** the file `analysis/weekly/week-of-YYYY-MM-DD.md` (where the date is the Monday of that week).

**CRITICAL: Each weekly summary must follow on from the previous week.** Read the previous week's summary before writing. These are a continuous executive briefing — like having an executive assistant who tracks everything. Carry forward:
- Unresolved risks from last week — did they get better, worse, or stay the same?
- Open threads — any progress or new developments?
- Stakeholder trajectories — continuing trends, not just point-in-time snapshots
- Action items — were last week's actions completed?

Use this template:

```markdown
# Week of [date range, e.g. 3–7 March 2026]
**Transcripts processed:** [count]
**Previous week:** [one-line summary of where things stood, e.g. "Diya's first governance session; 12-week resource plan locked; User Voice integration scoped"]

## Executive Summary
[2-3 paragraph narrative of the week. Written in a flowing style as if briefing an executive who read last week's summary. Start with what moved forward, then what emerged as new, then what's concerning. Reference last week's state where relevant — e.g. "The resource plan locked last week hit its first test when..." or "Richard's fatigue, noted in passing last week, has escalated to..."]

## Headlines
- [3-5 most important developments, ranked by impact. Bold the key phrase.]

## Workstream Progress
[One subsection per active workstream. Write in prose, not just bullets. Reference last week's state — what changed, what didn't move, what's new.]

### WS2 CLARA
[Progress since last week...]

### [Other active workstreams...]

## Key Decisions
[Decisions made this week. Include who made them, the rationale, and any dissent.]

## Emerging Risks / Concerns
[Each risk should be tagged with severity: CRITICAL / HIGH / MEDIUM / LOW. For risks carried from previous weeks, note whether they're escalating, stable, or de-escalating.]

## Stakeholder Moves
[Notable shifts. Who leaned in? Who pulled back? Any new players? Any relationship dynamics that shifted?]

## Carried Forward from Last Week
[Explicitly list 3-5 items from last week that are still live — unresolved risks, pending decisions, open threads. Note any progress or lack thereof.]
```

### Step 5. Trigger backend import

After all markdown files are written, trigger the backend to re-import:
```bash
cd backend && python -m scripts.import_data --data-root .. --db-url "$DATABASE_URL"
```
Or call `POST /api/import/trigger` if the backend is running.

## Analysis Guidelines

- **Be specific.** "Data quality issues" is useless. "CSMs entering blocker data that disappears on deployment refresh, causing trust damage" is useful.
- **Track sentiment, not just facts.** If Josh is "cautious but coming around" or Diya "appeared engaged for the first time", that matters.
- **Note contradictions.** If Richard tells Diya one origin story and the debrief records a different one, flag it.
- **Distinguish what was decided from what was discussed.** Many meetings are exploratory — don't record discussions as decisions.
- **Quote sparingly but well.** One good quote per transcript summary is better than five mediocre ones. Choose quotes that reveal character, tension, or turning points.

## Things to Track Over Time

These are the through-lines to watch across transcripts:
- **CLARA adoption** — are CSMs actually using it? What's the feedback?
- **Data quality** — is it improving? What's still broken?
- **Resource strain** — Azmain's bandwidth, token costs, dev capacity
- **Stakeholder engagement** — who's leaning in, who's drifting
- **Scope creep** — new requirements landing on CLARA (User Voice, HD models, etc.)
- **Sales Recon convergence** — is the standalone→platform migration progressing?
- **Build in Five** — Martin's progress toward March 21 demo
- **Governance maturity** — is the programme becoming more structured?

## Rules

- Never fabricate information. If a transcript is ambiguous, say so.
- Never merge transcripts from different meetings into one summary.
- Preserve the human messiness — these are real conversations with tangents, politics, and personality. Don't sanitise.
- When updating trackers, add dates so changes can be traced.
- Keep context files concise. They should be quick-reference, not exhaustive.
