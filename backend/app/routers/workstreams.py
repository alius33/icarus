import re
from datetime import date, timedelta
from datetime import datetime as dt_datetime

from fastapi import APIRouter, Depends
from sqlalchemy import and_, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.database import get_db
from app.exceptions import NotFoundError
from app.models.action_item import ActionItem
from app.models.open_thread import OpenThread
from app.models.project import Project
from app.models.project_link import ProjectLink
from app.models.transcript import Transcript
from app.models.transcript_mention import TranscriptMention
from app.models.workstream import Workstream, WorkstreamMilestone
from app.schemas.workstream import (
    MilestoneSchema,
    WorkstreamBase,
    WorkstreamDetail,
    WorkstreamHealthScore,
)

router = APIRouter(tags=["workstreams"])


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _parse_date_string(s: str | None) -> date | None:
    """Try to parse a date string in common formats."""
    if not s:
        return None
    for fmt in ("%Y-%m-%d", "%d-%m-%Y", "%d %b %Y", "%d %B %Y"):
        try:
            if fmt == "%Y-%m-%d":
                return date.fromisoformat(s)
            return dt_datetime.strptime(s, fmt).date()
        except (ValueError, TypeError):
            continue
    match = re.search(r"(\d{4}-\d{2}-\d{2})", s)
    if match:
        try:
            return date.fromisoformat(match.group(1))
        except ValueError:
            pass
    return None


def _rag_from_score(score: float) -> str:
    if score > 70:
        return "green"
    if score >= 40:
        return "amber"
    return "red"


def _workstream_base(w: Workstream) -> WorkstreamBase:
    return WorkstreamBase(
        id=w.id,
        code=w.code,
        name=w.name,
        owner=w.lead,
        status=w.status,
        progress_pct=None,
        blocker_reason=w.blocker_reason,
        assigned_fte=w.assigned_fte,
    )


def _milestone_schema(m: WorkstreamMilestone) -> MilestoneSchema:
    return MilestoneSchema(
        id=m.id,
        workstream_id=m.workstream_id,
        title=m.description,
        status="open",
        target_date=str(m.milestone_date) if m.milestone_date else None,
        notes=None,
    )


# ---------------------------------------------------------------------------
# GET /api/workstreams
# ---------------------------------------------------------------------------

@router.get("/workstreams", response_model=list[WorkstreamBase])
async def list_workstreams(
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Workstream).order_by(Workstream.code)
    )
    workstreams = result.scalars().all()

    return [_workstream_base(w) for w in workstreams]


# ---------------------------------------------------------------------------
# GET /api/workstreams/{workstream_id}
# ---------------------------------------------------------------------------

@router.get("/workstreams/{workstream_id}", response_model=WorkstreamDetail)
async def get_workstream(
    workstream_id: int,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Workstream)
        .options(selectinload(Workstream.milestones))
        .where(Workstream.id == workstream_id)
    )
    workstream = result.scalar_one_or_none()
    if not workstream:
        raise NotFoundError("Workstream", workstream_id)

    return WorkstreamDetail(
        id=workstream.id,
        code=workstream.code,
        name=workstream.name,
        owner=workstream.lead,
        status=workstream.status,
        progress_pct=None,
        description=workstream.description,
        milestones=[_milestone_schema(m) for m in workstream.milestones],
        recent_mentions=[],
    )


# ---------------------------------------------------------------------------
# GET /api/workstreams/{workstream_id}/health
# ---------------------------------------------------------------------------

@router.get(
    "/workstreams/{workstream_id}/health",
    response_model=WorkstreamHealthScore,
)
async def get_workstream_health(
    workstream_id: int,
    db: AsyncSession = Depends(get_db),
):
    """Compute health score for a workstream based on five weighted signals.

    | Signal                        | Weight | Source                                 |
    |-------------------------------|--------|----------------------------------------|
    | Action completion rate        | 25%    | ActionItem by workstream project       |
    | Overdue action ratio          | 20%    | ActionItem deadline vs today           |
    | Open thread accumulation      | 20%    | OpenThread linked to workstream project|
    | Stakeholder engagement trend  | 15%    | TranscriptMention recent vs previous   |
    | Activity recency              | 20%    | Transcript meeting_date                |

    Score -> RAG: >70 green, 40-70 amber, <40 red
    """

    # Verify workstream exists
    ws_result = await db.execute(
        select(Workstream).where(Workstream.id == workstream_id)
    )
    workstream = ws_result.scalar_one_or_none()
    if not workstream:
        raise NotFoundError("Workstream", workstream_id)

    today = date.today()
    two_weeks_ago = today - timedelta(days=14)
    four_weeks_ago = today - timedelta(days=28)

    # Find the project linked to this workstream
    proj_result = await db.execute(
        select(Project.id).where(Project.workstream_id == workstream_id)
    )
    project_id = proj_result.scalar_one_or_none()

    # ---- Signal 1: Action completion rate (25%) ----
    # Get action IDs linked to this workstream's project
    if project_id:
        action_ids_result = await db.execute(
            select(ProjectLink.entity_id).where(
                ProjectLink.project_id == project_id,
                ProjectLink.entity_type == "action_item",
            )
        )
        action_ids = [r[0] for r in action_ids_result.all()]
    else:
        action_ids = []

    if action_ids:
        total_actions = (await db.execute(
            select(func.count(ActionItem.id)).where(ActionItem.id.in_(action_ids))
        )).scalar_one()
        completed_actions = (await db.execute(
            select(func.count(ActionItem.id)).where(
                ActionItem.id.in_(action_ids),
                ActionItem.status != "OPEN",
            )
        )).scalar_one()
        action_completion_score = (completed_actions / total_actions * 100) if total_actions > 0 else 50.0
    else:
        total_actions = 0
        action_completion_score = 50.0  # neutral when no data

    # ---- Signal 2: Overdue action ratio (20%) ----
    if action_ids:
        open_actions_result = await db.execute(
            select(ActionItem).where(
                ActionItem.id.in_(action_ids),
                ActionItem.status == "OPEN",
            )
        )
        open_actions = open_actions_result.scalars().all()
        open_count = len(open_actions)
        overdue_count = 0
        for a in open_actions:
            parsed = _parse_date_string(a.deadline)
            if parsed and parsed < today:
                overdue_count += 1
        overdue_ratio = (overdue_count / open_count * 100) if open_count > 0 else 0.0
        overdue_score = max(0.0, 100.0 - overdue_ratio * 2)  # 50% overdue -> 0
    else:
        overdue_score = 50.0  # neutral

    # ---- Signal 3: Open thread accumulation (20%) ----
    if project_id:
        thread_ids_result = await db.execute(
            select(ProjectLink.entity_id).where(
                ProjectLink.project_id == project_id,
                ProjectLink.entity_type == "open_thread",
            )
        )
        thread_ids = [r[0] for r in thread_ids_result.all()]
    else:
        thread_ids = []

    if thread_ids:
        open_threads_count = (await db.execute(
            select(func.count(OpenThread.id)).where(
                OpenThread.id.in_(thread_ids),
                OpenThread.status == "OPEN",
            )
        )).scalar_one()
        total_threads = (await db.execute(
            select(func.count(OpenThread.id)).where(OpenThread.id.in_(thread_ids))
        )).scalar_one()
        open_ratio = (open_threads_count / total_threads * 100) if total_threads > 0 else 0.0
        # Fewer open threads = higher score
        thread_score = max(0.0, 100.0 - open_ratio)
    else:
        thread_score = 50.0  # neutral

    # ---- Signal 4: Stakeholder engagement trend (15%) ----
    # Get transcript IDs linked to the workstream project
    if project_id:
        transcript_ids_result = await db.execute(
            select(ProjectLink.entity_id).where(
                ProjectLink.project_id == project_id,
                ProjectLink.entity_type == "transcript",
            )
        )
        transcript_ids = [r[0] for r in transcript_ids_result.all()]
    else:
        transcript_ids = []

    if transcript_ids:
        # Recent mention count across all stakeholders in these transcripts
        recent_mentions = (await db.execute(
            select(func.coalesce(func.sum(TranscriptMention.mention_count), 0))
            .join(Transcript, TranscriptMention.transcript_id == Transcript.id)
            .where(
                TranscriptMention.transcript_id.in_(transcript_ids),
                Transcript.meeting_date >= two_weeks_ago,
            )
        )).scalar_one()

        prev_mentions = (await db.execute(
            select(func.coalesce(func.sum(TranscriptMention.mention_count), 0))
            .join(Transcript, TranscriptMention.transcript_id == Transcript.id)
            .where(
                TranscriptMention.transcript_id.in_(transcript_ids),
                Transcript.meeting_date >= four_weeks_ago,
                Transcript.meeting_date < two_weeks_ago,
            )
        )).scalar_one()

        if recent_mentions == 0 and prev_mentions == 0:
            engagement_score = 30.0  # no engagement is concerning
        elif recent_mentions >= prev_mentions:
            engagement_score = 80.0  # stable or rising
        else:
            # Declining: scale proportionally
            ratio = recent_mentions / prev_mentions if prev_mentions > 0 else 0
            engagement_score = max(20.0, ratio * 80.0)
    else:
        engagement_score = 50.0  # neutral

    # ---- Signal 5: Activity recency (20%) ----
    if project_id:
        last_transcript_date = (await db.execute(
            select(func.max(Transcript.meeting_date))
            .join(ProjectLink, and_(
                ProjectLink.entity_id == Transcript.id,
                ProjectLink.entity_type == "transcript",
            ))
            .where(ProjectLink.project_id == project_id)
        )).scalar_one_or_none()
    else:
        last_transcript_date = None

    if last_transcript_date:
        days_since = (today - last_transcript_date).days
        if days_since <= 7:
            recency_score = 100.0
        elif days_since <= 14:
            recency_score = 75.0
        elif days_since <= 21:
            recency_score = 50.0
        elif days_since <= 28:
            recency_score = 25.0
        else:
            recency_score = max(0.0, 10.0)  # stale
    else:
        recency_score = 10.0  # no activity at all

    # ---- Weighted aggregate ----
    overall_score = round(
        action_completion_score * 0.25
        + overdue_score * 0.20
        + thread_score * 0.20
        + engagement_score * 0.15
        + recency_score * 0.20,
        1,
    )
    rag = _rag_from_score(overall_score)

    breakdown = {
        "action_completion": round(action_completion_score, 1),
        "overdue_actions": round(overdue_score, 1),
        "open_threads": round(thread_score, 1),
        "stakeholder_engagement": round(engagement_score, 1),
        "activity_recency": round(recency_score, 1),
    }

    return WorkstreamHealthScore(
        workstream_id=workstream.id,
        workstream_code=workstream.code,
        workstream_name=workstream.name,
        score=overall_score,
        rag=rag,
        breakdown=breakdown,
    )
