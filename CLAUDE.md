# Icarus — Customer Success Gen AI Programme Analysis

## What This Project Is

This is an analytical workspace **with a full web application** for tracking and analysing the Customer Success Gen AI Programme at Moody's Analytics (Insurance division). The programme runs six workstreams and has been active since January 2026. The primary tool being built is **CLARA** — an IRP adoption tracker.

There are TWO distinct types of work in this project:
1. **Transcript analysis** — processing meeting transcripts into summaries, weekly reports, and tracker updates (markdown files)
2. **App development** — building and maintaining the Icarus web app that displays all this analysis

---

## Quick Start

### Context ramp-up (read in order):
1. `context/glossary.md` — names, acronyms, systems, jargon
2. `context/stakeholders.md` — who matters and current dynamics
3. `context/workstreams.md` — current state of the six workstreams
4. The **most recent weekly summary** in `analysis/weekly/` — current programme state
5. `programme_debrief.md` — full chronological history (read sections as needed, not cover-to-cover)

### Running locally (development):
```bash
# 1. Start backend + DB in Docker (Python 3.12 required, local is 3.14)
docker compose up -d db backend

# 2. Start frontend directly (hot reload, instant changes)
cd frontend && npm run dev
```
- Frontend: http://localhost:3000 (Next.js dev server, hot reload)
- Backend API: http://localhost:8000/api (Docker container)
- PostgreSQL: localhost:5432 (Docker container)

**IMPORTANT:** Do NOT run the frontend in Docker for local dev. The Docker frontend requires a full rebuild on every code change. Run `npm run dev` directly for instant hot reload. Backend stays in Docker because local Python is 3.14 (pydantic-core requires <=3.13).

---

## Project Structure

```
icarus/
├── CLAUDE.md                        # You are here — project instructions
├── programme_debrief.md             # Master debrief (Jan 6 – Feb 27, 2026)
├── docker-compose.yml               # Dev compose (backend + frontend + postgres)
├── docker-compose.prod.yml          # Production overrides
├── .pre-commit-config.yaml          # Ruff formatting hooks
│
├── Transcripts/                     # Raw meeting transcripts (.txt)
│
├── analysis/
│   ├── summaries/                   # Per-transcript structured summaries (104+ files)
│   ├── weekly/                      # Weekly rollup reports (11+ files)
│   └── trackers/                    # Running trackers (9 files — see §Analytical Trackers)
│       ├── action_items.md
│       ├── commitments.md
│       ├── contradictions.md
│       ├── influence_graph.md
│       ├── meeting_scores.md
│       ├── risk_register.md
│       ├── sentiment_tracker.md
│       ├── task_audit_report.md
│       └── topic_evolution.md
│
├── context/                         # Reference files — read for background
│   ├── stakeholders.md              # 40+ people, roles, dynamics, tiers
│   ├── workstreams.md               # Six workstreams — status & history
│   ├── glossary.md                  # Names, acronyms, systems, jargon
│   ├── decisions.md                 # Decision log with rationale
│   ├── open_threads.md              # Unresolved questions & threads
│   └── projects/                    # Per-workstream context docs
│       ├── ws1_training_enablement.md
│       ├── ws2_clara.md
│       ├── ws3_customer_success_agent.md
│       ├── ws4_friday.md
│       ├── ws5_navigator_l1_automation.md
│       └── ws6_build_in_five.md
│
├── frontend/                        # Next.js 14 web app
│   ├── Dockerfile
│   ├── src/app/                     # 31+ page routes (see §Frontend Pages)
│   ├── src/components/              # 75+ components (see §Frontend Components)
│   └── src/lib/                     # API client, types, utils, SWR hooks
│
├── backend/                         # FastAPI + PostgreSQL
│   ├── Dockerfile
│   ├── app/
│   │   ├── main.py                  # FastAPI app, middleware, router registration
│   │   ├── config.py                # Settings (DB, CORS, auth, data root)
│   │   ├── database.py              # Async SQLAlchemy engine/session
│   │   ├── auth/                    # JWT authentication system
│   │   ├── middleware/              # Logging + rate limiting
│   │   ├── models/                  # 33 SQLAlchemy ORM models
│   │   ├── routers/                 # 36 API route files
│   │   ├── schemas/                 # 35+ Pydantic schemas
│   │   └── services/               # Upload + action writeback
│   ├── alembic/                     # 15 database migrations
│   ├── scripts/
│   │   ├── import_data.py           # Bulk markdown → DB import orchestrator
│   │   ├── parsers/                 # 18 file parsers
│   │   ├── speaker_id/             # 13-module speaker identification engine
│   │   ├── rebuild_tasks.py         # ActionItem → Task migration
│   │   ├── audit_task_statuses.py   # Task status validation
│   │   ├── backfill_project_summaries.py
│   │   └── setup_new_projects.py
│   └── tests/
│
├── cowork/                          # Multi-agent task definitions
│   ├── README.md
│   └── analyse-transcripts.md
│
├── .github/workflows/ci.yml        # GitHub Actions (lint, test, build)
│
└── .claude/
    └── commands/                    # 45+ slash commands by category
        ├── analysis/                # weekly-report, import-data, insights, etc.
        ├── backend/                 # fastapi-patterns, api-docs
        ├── db/                      # migrate, optimize, seed
        ├── deploy/                  # checklist, docker
        ├── dev/                     # feature, component, api-endpoint, refactor
        ├── frontend/                # nextjs-patterns, a11y, responsive, dark-mode
        ├── quality/                 # review, security-scan, performance, tech-debt
        ├── starter/                 # clean, commit, deps, pr-create, verify
        ├── test/                    # tdd, harness, e2e
        └── utility/                 # onboard, standup, debug, context, deps
```

---

## The Icarus Web App — Backend

### Architecture

- **Framework:** FastAPI with async SQLAlchemy 2.0, PostgreSQL, Alembic migrations (15 versions)
- **Port:** 8000 | **API prefix:** `/api`
- **Middleware stack** (outermost → innermost): RateLimiterMiddleware → CORSMiddleware → LoggingMiddleware
- **Auth:** JWT tokens (HS256). `AUTH_ENABLED=false` in dev, `true` in production. Default dev creds: `admin:admin`
- **Rate limiting:** 100 reads/min, 30 writes/min per IP. Returns `429` with `Retry-After` header when exceeded.

### Data Models (33 models in `backend/app/models/`)

#### Core Content (7)
| Model | File | Purpose |
|-------|------|---------|
| `Transcript` | `transcript.py` | Meeting transcripts with raw_text, word_count, file_hash dedup |
| `Summary` | `summary.py` | Per-transcript structured summaries (TSVECTOR search) |
| `WeeklyReport` | `weekly_report.py` | Weekly executive summaries (TSVECTOR search) |
| `Document` | `document.py` | Generic document storage (doc_type field, TSVECTOR search) |
| `TranscriptMention` | `transcript_mention.py` | Join: transcript → stakeholder (speaker/mentioned, count) |
| `Project` | `project.py` | Projects (workstream + custom), status, health, milestones |
| `ProjectLink` | `project_link.py` | Join: project → any entity (transcript, decision, etc.) |

#### Programme Entities (7)
| Model | File | Purpose |
|-------|------|---------|
| `Decision` | `decision.py` | Decisions with status (made/in_progress/implemented/reversed/superseded), position field for board ordering |
| `OpenThread` | `open_thread.py` | Unresolved questions, severity (CRITICAL/HIGH/MEDIUM/LOW), position for board |
| `Task` | `task.py` | Tasks (evolved from ActionItem): status (TODO/IN_PROGRESS/IN_REVIEW/DONE/CANCELLED), priority, assignee, labels, project hierarchy |
| `ActionItem` | `action_item.py` | Legacy — superseded by Task, still exists for backward compat |
| `Stakeholder` | `stakeholder.py` | People, roles, tier, engagement level |
| `Workstream` | `workstream.py` | Six programme workstreams with status, RAG, milestones |
| `Glossary` | `glossary.py` | Terms, acronyms, definitions |

#### Analysis Engine (7)
| Model | File | Purpose |
|-------|------|---------|
| `Contradiction` | `contradiction.py` | Tracks reversals, quiet drops, scope shifts, reframing. `entry_kind`: contradiction or gap |
| `RiskEntry` | `risk_entry.py` | Risk register. Severity: CRITICAL/HIGH/MEDIUM/LOW. Trajectory: escalating/stable/de-escalating/new/resolved |
| `MeetingScore` | `meeting_score.py` | Meeting quality: decision_velocity, action_clarity, engagement_balance, topic_completion, follow_through. Overall 0-100 |
| `InfluenceSignal` | `influence_signal.py` | Stakeholder influence: proposal_adopted, deferred_to, interrupted, final_say, bridging, blocked |
| `TopicSignal` | `topic_signal.py` | Topic tracking: intensity, trend (rising/stable/declining/new) |
| `SentimentSignal` | `sentiment_signal.py` | Stakeholder sentiment (champion→disengaged), shift (UP/DOWN/STABLE/NEW) |
| `Commitment` | `commitment.py` | Stakeholder commitments: deadline_type, status (pending/fulfilled/broken/formalised/conditional) |

#### Programme Intelligence (5)
| Model | File | Purpose |
|-------|------|---------|
| `ProgrammeWin` | `programme_win.py` | Wins/successes. Category: time_saved, adoption, quality, reach, process_improvement |
| `AdoptionMetric` | `adoption_metric.py` | CLARA adoption: active_users, data_entries, reviews_completed, queries_run |
| `Outreach` | `outreach.py` | Division engagement: status (initial_contact→committed/cold) |
| `OutreachLink` | `outreach_link.py` | Join: outreach → transcript |
| `DivisionProfile` | `division_profile.py` | Division-level partnership status |

#### Project & Dependency (5)
| Model | File | Purpose |
|-------|------|---------|
| `ProjectSummary` | `project_summary.py` | Per-project transcript summaries with relevance (HIGH/MEDIUM/LOW) |
| `CrossProjectLink` | `cross_project_link.py` | Project dependencies/conflicts (dependency/conflict/synergy/resource_shared/blocked_by/supersedes) |
| `Dependency` | `dependency.py` | Integration/external dependencies with status |
| `ScopeItem` | `scope_item.py` | Scope additions tracking (original vs addition, status) |
| `ResourceAllocation` | `resource_allocation.py` | Person → role → allocation % per workstream |

#### Internal (1)
| Model | File | Purpose |
|-------|------|---------|
| `DeletedImport` | `deleted_import.py` | Tracks deleted entities during re-imports |

### API Routes (36 routers in `backend/app/routers/`)

#### Content & Core
| Endpoint prefix | Router | Key operations |
|-----------------|--------|----------------|
| `/api/dashboard` | `dashboard.py` | GET metrics, GET /brief (leadership text brief) |
| `/api/transcripts` | `transcripts.py` | GET list (search, limit), GET detail, POST upload, PATCH update |
| `/api/summaries` | `summaries.py` | GET list, GET detail |
| `/api/weekly-reports` | `weekly_reports.py` | GET list, GET detail |
| `/api/search` | `search.py` | GET full-text search across all entities |
| `/api/timeline` | `timeline.py` | GET with date range |
| `/api/import/trigger` | `import_trigger.py` | POST re-import markdown → DB |

#### Programme Management
| Endpoint prefix | Router | Key operations |
|-----------------|--------|----------------|
| `/api/projects` | `projects.py` | CRUD + GET /{id}/hub + GET /{id}/weekly + POST /{id}/links |
| `/api/workstreams` | `workstreams.py` | GET list, GET detail |
| `/api/stakeholders` | `stakeholders.py` | CRUD + GET /{id}/mentions |
| `/api/decisions` | `decisions.py` | CRUD + GET /board + GET /timeline + PATCH position |
| `/api/open-threads` | `open_threads.py` | CRUD + GET /board + PATCH position |
| `/api/tasks` | `tasks.py` | CRUD + GET /board + GET /timeline + POST complete + labels |
| `/api/action-items` | `action_items.py` | CRUD (legacy, mostly redirects to tasks) |
| `/api/glossary` | `glossary.py` | CRUD |
| `/api/commitments` | `commitments.py` | CRUD |

#### Analysis Engine
| Endpoint prefix | Router | Key operations |
|-----------------|--------|----------------|
| `/api/contradictions` | `contradictions.py` | CRUD + GET /gaps |
| `/api/risk-entries` | `risk_entries.py` | CRUD + GET /heatmap |
| `/api/meeting-scores` | `meeting_scores.py` | CRUD + GET /trend |
| `/api/influence-signals` | `influence_signals.py` | CRUD + GET /graph |
| `/api/topic-signals` | `topic_signals.py` | CRUD + GET /evolution + GET /momentum |
| `/api/sentiments` | `sentiments.py` | CRUD + GET /timeline |
| `/api/speaker-review` | `speaker_review.py` | GET review, POST confirm, GET context |

#### Programme Intelligence
| Endpoint prefix | Router | Key operations |
|-----------------|--------|----------------|
| `/api/wins` | `wins.py` | CRUD |
| `/api/adoption` | `adoption.py` | CRUD + GET /timeline |
| `/api/outreach` | `outreach.py` | CRUD with status filtering |
| `/api/divisions` | `divisions.py` | CRUD |

#### Dependencies & Scope
| Endpoint prefix | Router | Key operations |
|-----------------|--------|----------------|
| `/api/project-summaries` | `project_summaries.py` | CRUD |
| `/api/cross-project-links` | `cross_project_links.py` | CRUD |
| `/api/dependencies` | `dependencies.py` | CRUD |
| `/api/resources` | `resources.py` | CRUD |
| `/api/scope` | `scope.py` | CRUD |

#### Auth
| Endpoint prefix | Router | Key operations |
|-----------------|--------|----------------|
| `/api/auth` | `auth/router.py` | POST /login (returns JWT token) |

### Services

| Service | File | Purpose |
|---------|------|---------|
| Upload | `services/upload_service.py` | Ingests transcript files: parses filename for date/title, extracts participants, computes word count, upserts with file hash dedup, rebuilds transcript_mentions |
| Action Writeback | `services/action_writeback.py` | Writes task status changes back to `analysis/trackers/action_items.md` so the `/analyse` pipeline sees UI-driven updates |

### Import Scripts (`backend/scripts/`)

| Script | Purpose |
|--------|---------|
| `import_data.py` | **Main orchestrator** — reads all markdown from `Transcripts/`, `analysis/`, `context/` → parses → stores in DB |
| `rebuild_tasks.py` | Converts ActionItem records → Task records |
| `audit_task_statuses.py` | Validates task status consistency |
| `backfill_project_summaries.py` | Auto-creates ProjectSummary entries from existing transcripts |
| `setup_new_projects.py` | Creates new project records in DB |

### Parsers (18 files in `backend/scripts/parsers/`)

**Original:** transcript, decision, action_item, stakeholder, workstream, glossary, open_thread

**Added:** commitment, contradiction, risk_entry, meeting_score, influence_signal, topic_signal, sentiment, project_summary, summary_extractor (578 lines — the largest parser)

### Speaker Identification System (`backend/scripts/speaker_id/`)

A sophisticated 13-module engine for identifying speakers in transcripts:

| Module | Purpose |
|--------|---------|
| `runner.py` | Main orchestrator |
| `heuristics.py` | Rule-based matching (word choice, speaking style, timing) |
| `config.py` | Known speakers, speech patterns |
| `profiler.py` | Builds speaker profiles from transcript history |
| `stylometric_matcher.py` | Linguistic fingerprinting |
| `confidence_engine.py` | Confidence scoring for matches |
| `models.py` | Data models (Speaker, SpeakerSegment, ConfidenceScore) |
| `conversation_graph.py` | Tracks conversation flow and turn-taking |
| `applier.py` | Applies speaker IDs to transcript segments |
| `report.py` | Generates speaker ID reports |
| `segment_parser.py` | Parses transcript segments |

**Usage:**
```bash
# Preview speaker identification
cd backend && python -m scripts.speaker_id --file Transcripts/<filename>.txt

# Apply identified speakers
cd backend && python -m scripts.speaker_id --file Transcripts/<filename>.txt --apply
```

### Database Migrations (15 versions in `backend/alembic/versions/`)

| # | Migration | What it adds |
|---|-----------|-------------|
| 001 | Initial schema | Base tables (transcript, summary, weekly_report, stakeholder, etc.) |
| 002 | Projects | Project model + project_links |
| 003 | Manual flag | is_manual flag, deleted_imports tracking |
| 004 | Programme intelligence | programme_win, adoption_metric, dependency, resource_allocation, scope_item |
| 005 | Wins & adoption | Extended adoption fields |
| 006 | Outreach | Outreach, outreach_link, division_profile |
| 007 | Enhanced projects | Extended project fields (health, milestones) |
| 008 | Sentiment & commitments | sentiment_signal, commitment |
| 009 | Cross-project links | cross_project_link |
| 010 | Decision execution | Decision status tracking |
| 011 | Milestone status | Milestone status fields |
| 012 | Tasks | Evolved action_items → tasks (priority, labels, project hierarchy) |
| 013 | Positions | Position field on threads and decisions (for board ordering) |
| 014 | Analysis engine | contradiction, influence_signal, topic_signal, meeting_score, risk_entry |
| 015 | Primary project | primary_project_id on transcript |

**Creating a new migration:**
```bash
cd backend && alembic revision --autogenerate -m "description_of_change"
cd backend && alembic upgrade head
```

---

## The Icarus Web App — Frontend

### Tech Stack

- **Next.js 14.2** (App Router) with TypeScript
- **Tailwind CSS 3.4** with `@tailwindcss/typography`
- **SWR 2.4** for data fetching/caching
- **Recharts 3.8** for charts and visualisations
- **@dnd-kit** for drag-and-drop (kanban boards)
- **lucide-react** for icons
- **react-markdown** + remark-gfm for markdown rendering
- **vitest** + Testing Library for tests

### Pages & Navigation (31+ routes)

The sidebar has 8 sections:

#### Overview
| Route | Page | Description |
|-------|------|-------------|
| `/` | Dashboard | Programme pulse, KPI strip, insights, needs attention, activity feed, stakeholder panel, resource capacity, scope tracker, risk/dependency board |
| `/timeline` | Timeline | Chronological view of all events |

#### Content
| Route | Page | Description |
|-------|------|-------------|
| `/transcripts` | Transcript List | All transcripts with search |
| `/transcripts/[id]` | Transcript Detail | Full transcript view |
| `/upload` | Upload | Drag-and-drop transcript upload with project dropdown |
| `/speaker-review` | Speaker Review | Speaker identification review interface |
| `/analysis/summaries` | Summaries | Per-call summary list |
| `/analysis/summaries/[id]` | Summary Detail | Full summary with markdown rendering |
| `/analysis/weekly` | Weekly Reports | Weekly executive summaries |
| `/analysis/weekly/[id]` | Weekly Detail | Full weekly report |

#### Programme
| Route | Page | Description |
|-------|------|-------------|
| `/projects` | Project Hub | All projects (workstream + custom) |
| `/projects/new` | New Project | Create project form |
| `/projects/[id]` | Project Detail | Tabbed view: overview, weekly, summaries, transcripts, decisions, tasks, threads, stakeholders, cross-links |
| `/workstreams` | Workstreams | Workstream list with milestone burndown |
| `/workstreams/[id]` | Workstream Detail | Individual workstream |
| `/stakeholders` | Stakeholders | 40+ people with tier, engagement |
| `/stakeholders/[id]` | Stakeholder Detail | Individual stakeholder |

#### Tracking
| Route | Page | Description |
|-------|------|-------------|
| `/decisions` | Decisions | Board (kanban), list, and timeline views with drag-drop |
| `/tasks` | Tasks | Board (TODO/IN_PROGRESS/IN_REVIEW/DONE), list, timeline views |
| `/open-threads` | Open Threads | Board (OPEN/WATCHING/CLOSED), list views with drag-drop |
| `/commitments` | Commitments | Stakeholder commitment tracker |
| `/action-items` | Action Items | Legacy action items |
| `/my-items` | My Items | Personalised view of assigned items |

#### Intelligence
| Route | Page | Description |
|-------|------|-------------|
| `/risks` | Risk Register | Severity heatmap, trajectory tracking |
| `/dependencies` | Dependencies | Integration/external dependency tracker |
| `/resources` | Resources | Resource allocation and capacity planning |
| `/scope` | Scope Tracker | Scope creep tracking (original vs additions) |
| `/topic-evolution` | Topic Evolution | Topic trend analysis over time |
| `/influence-graph` | Influence Map | Stakeholder influence network visualisation |
| `/contradictions` | Contradictions | Contradictions and data gaps tracker |
| `/meeting-scores` | Meeting Scores | Meeting effectiveness scoring with radar charts |

#### Strategy
| Route | Page | Description |
|-------|------|-------------|
| `/wins` | Programme Wins | Wins tracker (time_saved, adoption, quality, reach) |
| `/outreach` | Outreach Tracker | Division engagement status |

#### Reference
| Route | Page | Description |
|-------|------|-------------|
| `/glossary` | Glossary | Terms and acronyms |
| `/search` | Search | Full-text search across all entities |

### Key Frontend Files

| File | Purpose |
|------|---------|
| `src/app/layout.tsx` | Root layout: dark theme (bg-gray-900), fixed sidebar, header, breadcrumb bar, Geist font |
| `src/lib/api.ts` | `fetchApi<T>()` wrapper, ALL API endpoints (32 endpoint groups) |
| `src/lib/types.ts` | 50+ TypeScript interfaces for all entities |
| `src/lib/swr.ts` | 30+ SWR hooks (useDashboard, useTranscripts, useDecisions, useTasks, useRiskEntries, etc.) |
| `src/lib/utils.ts` | Helpers: cn, getStatusColor, formatDate, ragDotColor, severityColor, capacityColor, trendArrow, isOverdue, taskStatusColor, priorityDotColor |

### Component Architecture

**Major component directories:**
- `components/dashboard/` — DashboardClient, ProgrammePulse, KpiStrip, InsightsStrip, NeedsAttention, ActivityFeed, StakeholderPanel, ResourceCapacity, ScopeTracker, RiskDependencyBoard + 7 modals (Action, Decision, Thread, Resource, Dependency, ScopeItem, Stakeholder) + hooks (useDashboardData, useDashboardFilters, useDashboardModals, useKeyboardShortcuts)
- `components/decisions/` — DecisionBoard, DecisionCard, DecisionList, DecisionTimeline, DecisionDetailPanel, DecisionViewSwitcher, DecisionCreateModal
- `components/tasks/` — TaskBoard, TaskCard, TaskList, TaskTimeline, TaskDetailPanel, TaskViewSwitcher, TaskCreateModal, LabelTagInput
- `components/threads/` — ThreadBoard, ThreadCard, ThreadList, ThreadDetailPanel, ThreadViewSwitcher, ThreadCreateModal
- `components/projects/` — ProjectTabBar, ProjectOverviewTab, ProjectWeeklyOverviewTab, ProjectSummariesTab, ProjectTranscriptsTab, ProjectDecisionsTab, ProjectTasksTab, ProjectActionsTab, ProjectThreadsTab, ProjectStakeholdersTab, ProjectCrossLinksTab, ProjectBriefButton
- `components/contradictions/` — ContradictionCard, GapCard
- `components/influence/` — InfluenceNetwork, PersonInfluenceCard
- `components/meeting-scores/` — ScoreTrendChart, MeetingRadar
- `components/speaker-review/` — SpeakerReviewTable, ContextModal
- `components/workstreams/` — MilestoneBurndown
- `components/layout/` — Sidebar, Header, BreadcrumbBar
- `components/skeletons/` — DetailSkeleton, TableSkeleton, CardSkeleton

**Reusable patterns:**
- `ViewSwitcher` — toggles between board/list/timeline views (decisions, tasks, threads)
- `DetailPanel` — side-sheet detail view
- `CreateModal` — entity creation form modal
- `EntityModal` — generic wrapper for inline edit modals

### Data Flow

- **Server components** use `INTERNAL_API_URL` (default: `http://backend:8000` for Docker)
- **Client components** use `NEXT_PUBLIC_API_URL` (default: `http://localhost:8000` for dev)
- **SWR hooks** handle client-side caching with automatic revalidation
- All data comes from the backend API, NOT the filesystem

---

## Infrastructure

### Docker

| File | Purpose |
|------|---------|
| `docker-compose.yml` | Dev: PostgreSQL 16 + backend (reload) + frontend |
| `docker-compose.prod.yml` | Production overrides: no bind mounts, 4 workers, memory limits (backend 512M, frontend 256M), AUTH_ENABLED=true |
| `backend/Dockerfile` | Multi-stage Python 3.12-slim with healthcheck |
| `frontend/Dockerfile` | Multi-stage Node 20-alpine with healthcheck |

### Environment Variables

**Backend** (`backend/.env.example`):
| Variable | Purpose | Default |
|----------|---------|---------|
| `DATABASE_URL` | Async PostgreSQL URL | `postgresql+asyncpg://...` |
| `SYNC_DATABASE_URL` | Sync URL (for Alembic) | `postgresql://...` |
| `CORS_ORIGINS` | Allowed origins | `["http://localhost:3000"]` |
| `DATA_ROOT` | Path to markdown files | `.` |
| `SECRET_KEY` | JWT signing key | `change-me-in-production` |
| `AUTH_ENABLED` | Enable JWT auth | `false` |
| `AUTH_USERS` | JSON dict `{username: password_hash}` | — |

**Frontend** (`frontend/.env.local`):
| Variable | Purpose | Default |
|----------|---------|---------|
| `NEXT_PUBLIC_API_URL` | Client-side API URL | `http://localhost:8000` |
| `INTERNAL_API_URL` | Server-side API URL | `http://backend:8000` |

### Authentication System (`backend/app/auth/`)

- JWT tokens (HS256 algorithm, 480-minute expiry)
- `POST /api/auth/login` returns `{access_token, token_type}`
- `AUTH_ENABLED=false` in dev (all routes open), `true` in production
- Protected routes use `get_current_user` dependency
- Default dev credentials: `admin:admin` (plain-text fallback when no AUTH_USERS set)
- Production: set `AUTH_USERS` env var with bcrypt-hashed passwords

### CI/CD (`.github/workflows/ci.yml`)

5 jobs triggered on push to main/develop, PRs to main:
1. **backend-lint** — Ruff check on `app/`, `scripts/`
2. **backend-test** — pytest (SQLite in-memory for CI)
3. **frontend-lint** — Next.js lint
4. **frontend-test** — vitest
5. **frontend-build** — npm build (depends on lint + test)

### Pre-commit Hooks

`.pre-commit-config.yaml` runs Ruff formatting and checking on `backend/` files with `--fix`.

---

## How the Pipeline Works

```
User uploads .txt transcripts (via web UI or drops into Transcripts/)
    ↓
Claude analyses transcripts → creates markdown summaries + weekly reports + tracker updates
    ↓
Backend import script reads markdown → parses → stores in PostgreSQL
    ↓
Frontend displays everything via API
```

---

## Railway Deployment Workflow

The app is deployed on Railway (auto-deploys from GitHub). Analysis runs locally without a database — Railway handles the DB import automatically on every deploy.

### How it works

```
LOCAL (no database needed):
  git pull                                    ← get latest code
  Copy .txt files into Transcripts/           ← add new transcripts
  /analyse-deep                               ← Claude Code runs full analysis
  git add Transcripts/ analysis/ context/     ← stage all changed files
  git commit -m "Analysis: [date] transcripts"
  git push                                    ← push to GitHub

RAILWAY (automatic on every deploy):
  GitHub push triggers auto-deploy
  Docker rebuilds → COPY Transcripts/, analysis/, context/ into container
  alembic upgrade head                        ← run migrations
  python -m scripts.import_data               ← import all markdown into PostgreSQL
  uvicorn starts                              ← serve updated data via API
```

### Key points
- **No local database needed** for analysis. The `/analyse-deep` command detects new transcripts by comparing filenames (`Transcripts/*.txt` vs `analysis/summaries/*.md`), loads context from markdown files, and writes output to markdown files. Purely filesystem-based.
- **Railway import is automatic.** The `Dockerfile.railway-backend` startup command runs `import_data.py` on every deploy, which reads all markdown files and upserts them into PostgreSQL (idempotent via SHA256 hash dedup).
- **Commit everything.** After analysis, stage `Transcripts/`, `analysis/`, and `context/` — these all need to be in the repo for Railway to pick them up.
- **Import covers all entities:** transcripts, summaries, weekly reports, action items, decisions, open threads, stakeholders, workstreams, commitments, risks, contradictions, meeting scores, influence signals, topic signals, sentiments, and transcript mentions.

---

## Transcript Naming Convention

Transcripts use two date formats (both are valid):
- `DD-MM-YYYY_-_Title.txt` (earlier transcripts)
- `YYYY-MM-DD_-_Title.txt` (later transcripts)

When adding new transcripts, use: `YYYY-MM-DD_-_Short_Descriptive_Title.txt`

---

## Core Workflow: Processing New Transcripts

Use `/analyse` in Claude Code or run the cowork task `analyse-transcripts`. Both follow the same pipeline:

### Step 0. Detect new transcripts

Compare `Transcripts/*.txt` filenames against `analysis/summaries/*.md`. Any transcript without a matching summary is "new" and needs processing. The matching logic: normalise the transcript filename to `YYYY-MM-DD_-_Title` format and check if a summary with that stem exists.

Also check the backend API: `GET /api/transcripts?limit=100` — transcripts uploaded via the web UI exist only in the database, not the filesystem. Look for `has_summary: false`.

### Step 1. Load context

Read these files to understand the current programme state before analysing:
1. `context/glossary.md` — names and acronyms
2. `context/stakeholders.md` — who matters and current dynamics
3. `context/workstreams.md` — current workstream status
4. The **most recent weekly summary** in `analysis/weekly/` — this is critical for continuity

### Step 2. Speaker identification

Run speaker identification on each new transcript before detailed analysis:
```bash
cd backend && python -m scripts.speaker_id --file Transcripts/<filename>.txt
```
Review the output and apply fixes if needed:
```bash
cd backend && python -m scripts.speaker_id --file Transcripts/<filename>.txt --apply
```
This ensures speaker labels are correct before analysis begins.

### Step 3. Summarise each transcript → `analysis/summaries/`

Create `analysis/summaries/YYYY-MM-DD_-_Title.md` with this structure:

```markdown
# [Meeting Title]
**Date:** YYYY-MM-DD
**Attendees:** [names mentioned]
**Duration context:** [short/medium/long based on transcript length]
**Primary project:** [name of the primary project this transcript relates to]
**Secondary projects:** [list of other projects touched, if any]

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

### Step 4. Update running trackers

After summarising, update these files if relevant:
- `context/decisions.md` — add any new decisions
- `context/open_threads.md` — add new threads, close resolved ones
- `context/stakeholders.md` — update if roles, attitudes, or dynamics shift
- `context/workstreams.md` — update status if there's meaningful progress
- `analysis/trackers/action_items.md` — add new actions, update existing
- `analysis/trackers/risk_register.md` — add new risks, update trajectories
- `analysis/trackers/commitments.md` — add new commitments, track fulfilment
- `analysis/trackers/contradictions.md` — flag reversals, quiet drops, scope shifts
- `analysis/trackers/sentiment_tracker.md` — note stakeholder sentiment changes
- `analysis/trackers/influence_graph.md` — update influence signals
- `analysis/trackers/meeting_scores.md` — score meeting effectiveness
- `analysis/trackers/topic_evolution.md` — track topic intensity changes

### Step 5. Update weekly summaries → `analysis/weekly/`

Weekly summaries provide a cross-programme narrative view. For every week that had new transcripts processed, either **create** or **update** the file `analysis/weekly/week-of-YYYY-MM-DD.md` (where the date is the Monday of that week).

**CRITICAL: Each weekly summary must follow on from the previous week.** Read the previous week's summary before writing. These are a continuous executive briefing — like having an executive assistant who tracks everything. Carry forward:
- Unresolved risks from last week — did they get better, worse, or stay the same?
- Open threads — any progress or new developments?
- Stakeholder trajectories — continuing trends, not just point-in-time snapshots
- Action items — were last week's actions completed?

Use this template:

```markdown
# Week of [date range, e.g. 3–7 March 2026]
**Transcripts processed:** [count]
**Previous week:** [one-line summary of where things stood]

## Executive Summary
[2-3 paragraph narrative of the week.]

## Headlines
- [3-5 most important developments, ranked by impact. Bold the key phrase.]

## Project Progress
[One subsection per active project. Use project names (not WS codes). Write in prose.]

### CLARA
[Progress since last week...]

### Build in Five
[Progress since last week...]

### [Other active projects...]

## Key Decisions
[Decisions made this week. Include who made them, the rationale, and any dissent.]

## Emerging Risks / Concerns
[Each risk should be tagged with severity: CRITICAL / HIGH / MEDIUM / LOW.]

## Stakeholder Moves
[Notable shifts.]

## Carried Forward from Last Week
[Explicitly list 3-5 items from last week that are still live.]
```

### Step 6. Project attribution & ProjectSummary entries

After analysis, ensure each transcript is properly linked to projects:

1. **Primary project**: Should already be set via the upload form's project dropdown. If not, set it via API:
   ```
   PATCH /api/transcripts/{id} with {"primary_project_id": <project_id>}
   ```

2. **Secondary project links**: Auto-detect from transcript content and create links:
   ```
   POST /api/projects/{project_id}/links with {"links": [{"entity_type": "transcript", "entity_id": <id>}]}
   ```

3. **Create ProjectSummary entries**: For each project a transcript is linked to, create a summary entry that will appear in the project's "Current Status" section:
   ```
   POST /api/project-summaries with {
     "project_id": <id>,
     "transcript_id": <id>,
     "date": "YYYY-MM-DD",
     "relevance": "HIGH" or "MEDIUM",
     "content": "Brief project-specific summary of what this transcript means for the project"
   }
   ```

### Step 7. Trigger backend import

After all markdown files are written, trigger the backend to re-import:
```bash
cd backend && python -m scripts.import_data --data-root .. --db-url "$DATABASE_URL"
```
Or call `POST /api/import/trigger` if the backend is running.

---

## Analytical Trackers

Nine markdown trackers in `analysis/trackers/` provide running intelligence. Each has a corresponding backend model and API endpoint:

| Tracker file | Backend model | What it tracks |
|-------------|---------------|----------------|
| `action_items.md` | Task (evolved from ActionItem) | Tasks with owner, deadline, status, priority |
| `commitments.md` | Commitment | Promises made in meetings, deadline type, fulfilment status |
| `contradictions.md` | Contradiction | Reversals, quiet drops, scope shifts, reframing, data gaps |
| `risk_register.md` | RiskEntry | Risks with severity (CRITICAL→LOW), trajectory (escalating→resolved) |
| `sentiment_tracker.md` | SentimentSignal | Stakeholder sentiment (champion→disengaged), directional shifts |
| `influence_graph.md` | InfluenceSignal | Who defers to whom, who gets proposals adopted, who blocks |
| `meeting_scores.md` | MeetingScore | Decision velocity, action clarity, engagement, follow-through (0-100) |
| `topic_evolution.md` | TopicSignal | Topic intensity and trend (rising/stable/declining/new) |
| `task_audit_report.md` | — | Audit of task completion and status consistency |

**When to update:** After processing each transcript, check if any of these trackers need new entries or updates. The import script (`import_data.py`) reads these markdown files and parses them into the database.

---

## Analysis Guidelines

- **Be specific.** "Data quality issues" is useless. "CSMs entering blocker data that disappears on deployment refresh, causing trust damage" is useful.
- **Track sentiment, not just facts.** If Josh is "cautious but coming around" or Diya "appeared engaged for the first time", that matters.
- **Note contradictions.** If Richard tells Diya one origin story and the debrief records a different one, flag it.
- **Distinguish what was decided from what was discussed.** Many meetings are exploratory — don't record discussions as decisions.
- **Quote sparingly but well.** One good quote per transcript summary is better than five mediocre ones. Choose quotes that reveal character, tension, or turning points.

---

## Things to Track Over Time

These are the through-lines to watch across transcripts:
- **CLARA adoption** — are CSMs actually using it? What's the feedback?
- **Data quality** — is it improving? What's still broken?
- **Resource strain** — Azmain's bandwidth, token costs, dev capacity
- **Stakeholder engagement** — who's leaning in, who's drifting
- **Scope creep** — new requirements landing on CLARA (User Voice, HD models, Gainsight, Salesforce)
- **Sales Recon convergence** — is the standalone→platform migration progressing?
- **Build in Five** — Martin's progress toward demo
- **Governance maturity** — is the programme becoming more structured?
- **Cross-OU outreach** — Banking, Asset Management, Life Insurance engagement
- **Commitment fulfilment** — are stakeholders following through on promises?
- **Meeting effectiveness** — are meetings getting more productive over time?
- **Contradiction patterns** — who reverses positions, what gets quietly dropped?

---

## Projects (Current as of March 2026)

| ID | Name | Notes |
|----|------|-------|
| 1 | CLARA (IRP Adoption Tracker) | Primary tool — WS2 |
| 2 | Friday (CS AI Agent) | WS4 |
| 3 | Build in Five | WS6 — Martin's rapid prototyping |
| 4 | Training & Enablement | WS1 |
| 5 | Navigator L1 Automation | WS5 |
| 7 | Customer Success Agent | WS3 |
| 8 | Cross OU Collaboration | Banking, AM, Life outreach |
| 9 | Program Management | Governance, steering, portfolio reviews |
| 9 | TSR Enhancements | TSR automation track |
| 10 | App Factory | BenVH's automated deployment platform for AI apps |

---

## Cowork Tasks

The `cowork/` directory contains task definitions for Claude Desktop's Cowork tab. These let Claude act as a programme analyst colleague.

### Advisory (conversational — Claude responds in text)
| Task file | Purpose |
|-----------|---------|
| `meeting-prep.md` | Prepare for a meeting: talking points, risk flags, overdue commitments, stakeholder dynamics |
| `programme-advice.md` | Strategic advice: what to escalate, where to focus, evidence-based recommendations |
| `review-and-challenge.md` | Critical review: find gaps, inconsistencies, political risks, decision-execution gaps |
| `stakeholder-briefing.md` | Pre-meeting person briefing: sentiment arc, commitments, influence, approach tips |

### Operational (conversational — structured intelligence)
| Task file | Purpose |
|-----------|---------|
| `weekly-pulse.md` | Monday morning ritual: what's urgent, what to watch, what to follow up |
| `catch-up.md` | Structured debrief after absence: what changed since date X |
| `status-draft.md` | Draft audience-tailored emails, Slack messages, or speaking notes |
| `trend-analysis.md` | Compare time periods across any dimension (risk, sentiment, topics, influence) |

### Reports (generates files)
| Task file | Purpose |
|-----------|---------|
| `generate-report.md` | Unified report generator: executive debrief (PPTX), stakeholder dossier (XLSX), risk dashboard (XLSX), or custom |

All tasks read from markdown files in `analysis/` and `context/` — no database access needed. Report outputs are saved to the project root.

---

## Rules

- Never fabricate information. If a transcript is ambiguous, say so.
- Never merge transcripts from different meetings into one summary.
- Preserve the human messiness — these are real conversations with tangents, politics, and personality. Don't sanitise.
- When updating trackers, add dates so changes can be traced.
- Keep context files concise. They should be quick-reference, not exhaustive.
- Never commit `.env` files or any file containing secrets/credentials.
- Always run speaker identification before detailed analysis.
- Transcript files may have `\r\r\n` line endings — use Python for edits, not the Edit tool.
- The action items tracker is very large (960+ lines) — read tail with offset to append.
- Transcripts uploaded via the frontend go ONLY to the database, not the filesystem. Always check the API for `has_summary: false` when detecting new transcripts.
