# Icarus Backend

## Architecture

- **FastAPI** with async SQLAlchemy 2.0 + PostgreSQL + Alembic migrations
- **Port:** 8000 | **API prefix:** `/api`
- **Middleware** (outer → inner): RateLimiterMiddleware → CORSMiddleware → LoggingMiddleware
- **Auth:** JWT (HS256). `AUTH_ENABLED=false` in dev, `true` in prod. Dev creds: `admin:admin`
- **Rate limiting:** 100 reads/min, 30 writes/min per IP → 429 with Retry-After

## Models (39 total in `app/models/`)

**Core Content (7):** Transcript, Summary, WeeklyReport, Document, TranscriptMention, Project, ProjectLink

**Programme Entities (6):** Decision, OpenThread, Task, ActionItem (legacy), Stakeholder, Glossary

**Analysis Engine (7):** Contradiction, RiskEntry, MeetingScore, InfluenceSignal, TopicSignal, SentimentSignal, Commitment

**Programme Intelligence (5):** ProgrammeWin, AdoptionMetric, Outreach, OutreachLink, DivisionProfile

**Project & Dependency (5):** ProjectSummary, CrossProjectLink, Dependency, ScopeItem, ResourceAllocation

**Weekly Plan (5):** ProgrammeDeliverable, DeliverableMilestone, WeeklyPlan, WeeklyPlanAction, DeliverableProgressSnapshot

**Transcript Extras (2):** TranscriptAttachment, TranscriptNote

**Internal (1):** DeletedImport

## Routers (35 in `app/routers/`)

Content: dashboard, transcripts, transcript_extras, summaries, weekly_reports, search, timeline, import_trigger
Programme: projects, project_summaries, cross_project_links, stakeholders, decisions, open_threads, tasks, action_items, glossary, commitments
Analysis: contradictions, risk_entries, meeting_scores, influence_signals, topic_signals, sentiments, speaker_review
Intelligence: wins, adoption, outreach, divisions
Dependencies: dependencies, resources, scope
Weekly Plan: weekly_plans, programme_deliverables

## Services (12 in `app/services/`)

- **upload_service** — transcript ingestion with file hash dedup
- **Writebacks** (6): action, decision, thread, commitment, contradiction, risk — sync UI changes back to markdown trackers
- **weekly_plan_export** — export weekly plans to seed JSON
- **attachment_service**, **text_extraction**, **markdown_table** — utilities

## Import Pipeline

- **Orchestrator:** `scripts/import_data.py` — reads all markdown from `Transcripts/`, `analysis/`, `context/` → parses → upserts to DB
- **Parsers (15):** in `scripts/parsers/` — one per entity type (transcript, summary, decision, action_item, stakeholder, glossary, open_thread, commitment, contradiction, risk_entry, meeting_score, influence_signal, topic_signal, sentiment, project_summary)
- **Summary extractor** (`summary_extractor.py`, 578 lines) — largest parser, handles structured summary parsing
- Auto-creates ProjectSummary + ProjectLink entries from `**Primary project:**` / `**Secondary projects:**` headers

## Speaker Identification (`scripts/speaker_id/`)

13-module engine: runner, heuristics, config, profiler, stylometric_matcher, confidence_engine, models, conversation_graph, applier, report, segment_parser

```bash
# Preview
cd backend && python -m scripts.speaker_id --file "Transcripts/<file>.txt"
# Apply
cd backend && python -m scripts.speaker_id --file "Transcripts/<file>.txt" --apply
```

## Migrations (20 versions in `alembic/versions/`)

Latest: `020_action_source_context.py`

```bash
# Create new migration
cd backend && alembic revision --autogenerate -m "description"
# Apply
cd backend && alembic upgrade head
```

## Testing

- pytest with SQLite in-memory for CI
- Tests in `tests/` directory

## Commands

```bash
docker compose up -d db backend   # Start backend + DB
cd backend && pytest              # Run tests (in Docker or CI)
cd backend && alembic upgrade head # Run migrations
cd backend && python -m scripts.import_data --data-root .. # Import markdown → DB
```
