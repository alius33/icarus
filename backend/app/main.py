import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.auth.router import router as auth_router
from app.config import settings
from app.middleware.logging_middleware import LoggingMiddleware
from app.middleware.rate_limiter import RateLimiterMiddleware

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(name)s %(levelname)s %(message)s")
from app.routers import (
    action_items,
    adoption,
    commitments,
    cross_project_links,
    dashboard,
    decisions,
    dependencies,
    divisions,
    glossary,
    import_trigger,
    open_threads,
    outreach,
    projects,
    resources,
    scope,
    search,
    sentiments,
    stakeholders,
    summaries,
    timeline,
    transcripts,
    weekly_reports,
    wins,
    workstreams,
)

app = FastAPI(title="Icarus Dashboard API", version="0.1.0")

# Rate limiter runs first (outermost middleware)
app.add_middleware(RateLimiterMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type"],
)

app.add_middleware(LoggingMiddleware)

# Auth router
app.include_router(auth_router, prefix="/api")

app.include_router(transcripts.router, prefix="/api")
app.include_router(summaries.router, prefix="/api")
app.include_router(weekly_reports.router, prefix="/api")
app.include_router(workstreams.router, prefix="/api")
app.include_router(stakeholders.router, prefix="/api")
app.include_router(decisions.router, prefix="/api")
app.include_router(open_threads.router, prefix="/api")
app.include_router(action_items.router, prefix="/api")
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


@app.get("/")
async def root():
    return {"status": "ok"}


@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": "0.1.0"}
