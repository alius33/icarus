# Icarus — Customer Success Gen AI Programme Analysis

## What This Is

An analytical workspace **with a full web application** for tracking the Customer Success Gen AI Programme at Moody's Analytics (Insurance division). The programme runs ten projects, active since January 2026. Primary tool: **CLARA** (IRP adoption tracker).

Two types of work happen here:
1. **Transcript analysis** — processing meeting transcripts into summaries, weekly reports, and tracker updates (all markdown files, no database needed)
2. **App development** — building the Icarus web app (Next.js + FastAPI + PostgreSQL) that displays the analysis

See `frontend/CLAUDE.md` and `backend/CLAUDE.md` for app-specific technical details.

---

## Quick Start

**Context ramp-up** (read in order):
1. `context/glossary.md` — names, acronyms, jargon
2. `context/stakeholders.md` — 40+ people, roles, dynamics
3. `context/projects/` — per-project context docs (6 files)
4. Most recent file in `analysis/weekly/` — current programme state

**Local development:**
```bash
docker compose up -d db backend    # Backend + DB in Docker (port 8000)
cd frontend && npm run dev          # Frontend direct (port 3000, hot reload)
```
Do NOT run frontend in Docker — no hot reload. Backend MUST be in Docker (local Python 3.14, pydantic-core needs <=3.13).

---

## Railway Deployment

App deployed on Railway, auto-deploys from GitHub. Analysis runs locally (no database needed).

```
LOCAL:  git pull → drop .txt in Transcripts/ → /analyse-deep → git add → commit → push
RAILWAY: auto-deploy → alembic upgrade head → import_data.py → uvicorn serves API
```

- Import is idempotent (SHA256 hash dedup) — safe to re-run
- Commit `Transcripts/`, `analysis/`, AND `context/` — all needed for Railway import
- `/analyse-deep` detects new transcripts by comparing filenames (no API/database needed)

---

## Analysis Pipeline

Use `/analyse` (lightweight) or `/analyse-deep` (full 11-agent swarm) to process new transcripts. High-level flow:

1. Detect new transcripts — compare `Transcripts/*.txt` vs `analysis/summaries/*.md`
2. Also check API for `has_summary: false` (transcripts uploaded via web UI are DB-only)
3. Load context — glossary, stakeholders, project files, latest weekly summary
4. Run speaker identification before analysis
5. Generate per-transcript summaries → `analysis/summaries/`
6. Update trackers in `analysis/trackers/` and context files
7. Create/update weekly summaries → `analysis/weekly/`
8. Import auto-creates ProjectSummary + ProjectLink entries from `**Primary project:**` headers

Full pipeline details are in the `/analyse` and `/analyse-deep` slash commands.

---

## Projects (March 2026)

| Code | Name | Context file |
|------|------|-------------|
| PR1 | CLARA (IRP Adoption Tracker) | `context/projects/clara.md` |
| PR2 | Friday (CS AI Agent) | `context/projects/friday.md` |
| PR3 | Build in Five | `context/projects/build_in_five.md` |
| PR4 | Training & Enablement | `context/projects/training_enablement.md` |
| PR5 | Navigator L1 Automation | `context/projects/navigator_l1_automation.md` |
| PR7 | Customer Success Agent | `context/projects/customer_success_agent.md` |
| PR8 | Cross OU Collaboration | _(no context file yet)_ |
| PR9 | Program Management | _(no context file yet)_ |
| PR10 | App Factory | _(no context file yet)_ |
| PR11 | TSR Enhancements | _(no context file yet)_ |

Note: "Sales Recon" is NOT a project — it's another team's product that gets mentioned in discussions.

---

## Key People — Disambiguation

Two pairs of names that are easily confused:
- **Natalia Orzechowska** — Senior Director, CS lead, runs Portfolio Reviews
- **Natalia Plant** — leads Gainsight team AND CLARA governance (fortnightly releases). DIFFERENT person.
- **Idrees Deen** — Banking CS, cross-OU coalition builder, strategic ally
- **Idris Abram** — works on TSR Enhancements / cat bond automation. DIFFERENT person.

Full stakeholder details: `context/stakeholders.md`

---

## Analytical Trackers

Nine markdown files in `analysis/trackers/` provide running intelligence. The import script parses these into the database:

`action_items.md`, `commitments.md`, `contradictions.md`, `risk_register.md`, `sentiment_tracker.md`, `influence_graph.md`, `meeting_scores.md`, `topic_evolution.md`, `task_audit_report.md`

---

## Behavioral Rules

Rules are in `.claude/rules/` (7 files, path-scoped — load automatically when working with matching files):
- `analysis-guidelines.md` — how to analyze transcripts
- `transcript-handling.md` — file naming, line endings, large file handling
- `project-conventions.md` — planning meta-rule, file organization, commit rules (global)
- `data-integrity.md` — import safety, tracker updates, deduplication
- `migration-safety.md` — database migration conventions
- `deleted-features.md` — features intentionally removed, do NOT recreate
- `docker-constraints.md` — Python version, Docker requirements

Cowork tasks: `cowork/README.md` | Slash commands: `.claude/commands/` (organized by category)
