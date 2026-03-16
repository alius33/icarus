import asyncio
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.gzip import GZipMiddleware

from app.auth.router import router as auth_router
from app.auto_import import auto_import_loop
from app.config import settings
from app.middleware.logging_middleware import LoggingMiddleware
from app.middleware.rate_limiter import RateLimiterMiddleware

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(name)s %(levelname)s %(message)s")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage background tasks that run for the lifetime of the app."""
    # Start the auto-import watcher
    watcher_task = asyncio.create_task(auto_import_loop(check_interval=30))
    yield
    # Shutdown: cancel the watcher
    watcher_task.cancel()
    try:
        await watcher_task
    except asyncio.CancelledError:
        pass


from app.routers import (
    action_items,
    adoption,
    tasks,
    transcript_extras,
    commitments,
    contradictions,
    cross_project_links,
    dashboard,
    decisions,
    dependencies,
    divisions,
    glossary,
    import_trigger,
    influence_signals,
    meeting_scores,
    open_threads,
    outreach,
    programme_deliverables,
    project_summaries,
    projects,
    resources,
    risk_entries,
    scope,
    search,
    sentiments,
    speaker_review,
    stakeholders,
    summaries,
    timeline,
    topic_signals,
    transcripts,
    weekly_plans,
    weekly_reports,
    wins,
    project_updates,
)

app = FastAPI(title="Icarus Dashboard API", version="0.1.0", lifespan=lifespan)

# Rate limiter runs first (outermost middleware)
app.add_middleware(RateLimiterMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type"],
)

app.add_middleware(LoggingMiddleware)
app.add_middleware(GZipMiddleware, minimum_size=1000)

# Auth router
app.include_router(auth_router, prefix="/api")

app.include_router(transcripts.router, prefix="/api")
app.include_router(summaries.router, prefix="/api")
app.include_router(weekly_reports.router, prefix="/api")
app.include_router(stakeholders.router, prefix="/api")
app.include_router(decisions.router, prefix="/api")
app.include_router(open_threads.router, prefix="/api")
app.include_router(action_items.router, prefix="/api")
app.include_router(tasks.router, prefix="/api")
app.include_router(glossary.router, prefix="/api")
app.include_router(search.router, prefix="/api")
app.include_router(dashboard.router, prefix="/api")
app.include_router(timeline.router, prefix="/api")
app.include_router(import_trigger.router, prefix="/api")
app.include_router(projects.router, prefix="/api")
app.include_router(dependencies.router, prefix="/api")
app.include_router(resources.router, prefix="/api")
app.include_router(scope.router, prefix="/api")
app.include_router(wins.router, prefix="/api")
app.include_router(adoption.router, prefix="/api")
app.include_router(outreach.router, prefix="/api")
app.include_router(divisions.router, prefix="/api")
app.include_router(sentiments.router, prefix="/api")
app.include_router(commitments.router, prefix="/api")
app.include_router(cross_project_links.router, prefix="/api")
app.include_router(speaker_review.router, prefix="/api")
app.include_router(topic_signals.router, prefix="/api")
app.include_router(influence_signals.router, prefix="/api")
app.include_router(contradictions.router, prefix="/api")
app.include_router(meeting_scores.router, prefix="/api")
app.include_router(risk_entries.router, prefix="/api")
app.include_router(project_summaries.router, prefix="/api")
app.include_router(transcript_extras.router, prefix="/api")
app.include_router(programme_deliverables.router, prefix="/api")
app.include_router(weekly_plans.router, prefix="/api")
app.include_router(project_updates.router, prefix="/api")


@app.get("/")
async def root():
    return {"status": "ok"}


@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": "0.1.0"}
