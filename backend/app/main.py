from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routers import (
    transcripts,
    summaries,
    weekly_reports,
    workstreams,
    stakeholders,
    decisions,
    open_threads,
    action_items,
    glossary,
    search,
    dashboard,
    timeline,
    import_trigger,
    projects,
    dependencies,
    resources,
    scope,
    wins,
    adoption,
    outreach,
    divisions,
    sentiments,
    commitments,
    cross_project_links,
)

app = FastAPI(title="Icarus Dashboard API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
