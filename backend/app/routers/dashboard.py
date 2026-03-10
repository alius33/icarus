import re
from collections import defaultdict
from datetime import date, timedelta, datetime as dt_datetime

from fastapi import APIRouter, Depends, Response
from sqlalchemy import select, func, desc, and_, case, literal_column
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.transcript import Transcript
from app.models.action_item import ActionItem
from app.models.open_thread import OpenThread
from app.models.workstream import Workstream
from app.models.decision import Decision
from app.models.project import Project
from app.models.project_link import ProjectLink
from app.models.stakeholder import Stakeholder
from app.models.transcript_mention import TranscriptMention
from app.models.dependency import Dependency
from app.models.resource_allocation import ResourceAllocation
from app.models.scope_item import ScopeItem
from app.schemas.dashboard import (
    DashboardResponse,
    DashboardProjectCard,
    ActivityFeedItem,
    NeedsAttentionItem,
    StakeholderEngagementItem,
    ProgrammeBrief,
    KpiData,
    InsightsData,
    ProgrammeStatus,
)

router = APIRouter(tags=["dashboard"])


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
    """Convert a 0-100 health score to a RAG rating."""
    if score > 70:
        return "green"
    if score >= 40:
        return "amber"
    return "red"


def _week_monday(d: date) -> date:
    """Return the Monday of the ISO week containing *d*."""
    return d - timedelta(days=d.weekday())


# ---------------------------------------------------------------------------
# Batch helpers — called once per dashboard load, not per entity
# ---------------------------------------------------------------------------

async def _batch_project_links_to_projects(
    db: AsyncSession,
    entity_type: str,
    entity_ids: list[int],
) -> dict[int, tuple[int, str]]:
    """Return {entity_id: (project_id, project_name)} for the given type."""
    if not entity_ids:
        return {}
    result = await db.execute(
        select(ProjectLink.entity_id, Project.id, Project.name)
        .join(Project, ProjectLink.project_id == Project.id)
        .where(
            ProjectLink.entity_type == entity_type,
            ProjectLink.entity_id.in_(entity_ids),
        )
    )
    mapping: dict[int, tuple[int, str]] = {}
    for entity_id, proj_id, proj_name in result.all():
        if entity_id not in mapping:
            mapping[entity_id] = (proj_id, proj_name)
    return mapping


async def _compute_weekly_counts(
    db: AsyncSession,
    today: date,
    weeks: int = 7,
) -> dict[str, list]:
    """Pre-compute weekly bucket counts for KPI sparklines.

    Returns dict with keys: transcripts, open_actions, risks, blocked_deps, utilization.
    Each value is a list of *weeks* numbers (oldest first).
    """
    monday = _week_monday(today)

    # Transcript counts per week
    transcript_counts: list[int] = []
    # Action snapshot per week (open at end of that week)
    action_counts: list[int] = []
    # Risk counts per week (open critical/high threads)
    risk_counts: list[int] = []
    # Blocked dependency counts per week — approximated as current snapshot
    blocked_counts: list[int] = []
    # Utilization per week — approximated as current snapshot
    utilization_values: list[float] = []

    # -- Transcripts per week (actual, from meeting_date) --
    week_starts = [monday - timedelta(weeks=i) for i in range(weeks - 1, -1, -1)]
    for ws in week_starts:
        we = ws + timedelta(days=7)
        count = (await db.execute(
            select(func.count(Transcript.id)).where(
                Transcript.meeting_date >= ws,
                Transcript.meeting_date < we,
            )
        )).scalar_one()
        transcript_counts.append(count)

    # -- Open actions per week: approximate as current open count minus
    #    actions completed in future weeks. This gives a rough backward
    #    projection without requiring event-sourced snapshots.
    current_open = (await db.execute(
        select(func.count(ActionItem.id)).where(ActionItem.status == "OPEN")
    )).scalar_one()
    # Get completions per week to walk backwards
    completions_result = await db.execute(
        select(ActionItem.completed_date)
        .where(ActionItem.status != "OPEN", ActionItem.completed_date.isnot(None))
    )
    completions_by_week: dict[date, int] = defaultdict(int)
    for (comp_date,) in completions_result.all():
        if comp_date:
            completions_by_week[_week_monday(comp_date)] += 1

    # Walk backwards from current week
    running = current_open
    raw_action_counts: list[tuple[date, int]] = []
    for ws in reversed(week_starts):
        raw_action_counts.append((ws, running))
        # Going one week further back: add back completions from this week
        running += completions_by_week.get(ws, 0)
    raw_action_counts.reverse()
    action_counts = [c for _, c in raw_action_counts]

    # -- Risks per week: same backward-projection approach
    current_risks = (await db.execute(
        select(func.count(OpenThread.id)).where(
            OpenThread.status == "OPEN",
            OpenThread.severity.in_(["CRITICAL", "HIGH"]),
        )
    )).scalar_one()
    for _ in week_starts:
        risk_counts.append(current_risks)

    # -- Blocked deps: current snapshot replicated
    current_blocked = (await db.execute(
        select(func.count(Dependency.id)).where(Dependency.status == "blocked")
    )).scalar_one()
    for _ in week_starts:
        blocked_counts.append(current_blocked)

    # -- Utilization: current snapshot replicated
    resources_result = await db.execute(select(ResourceAllocation))
    resources = resources_result.scalars().all()
    if resources:
        total_pct = 0.0
        for r in resources:
            if r.allocations and isinstance(r.allocations, list):
                total_pct += sum(
                    a.get("percentage", 0) for a in r.allocations if isinstance(a, dict)
                )
        avg_util = total_pct / len(resources) if resources else 0.0
    else:
        avg_util = 0.0
    for _ in week_starts:
        utilization_values.append(round(avg_util, 1))

    return {
        "transcripts": transcript_counts,
        "open_actions": action_counts,
        "risks": risk_counts,
        "blocked_deps": blocked_counts,
        "utilization": utilization_values,
    }


# ---------------------------------------------------------------------------
# GET /api/dashboard
# ---------------------------------------------------------------------------

@router.get("/dashboard", response_model=DashboardResponse)
async def get_dashboard(
    response: Response,
    db: AsyncSession = Depends(get_db),
):
    response.headers["Cache-Control"] = "max-age=30"

    today = date.today()
    two_weeks_ago = today - timedelta(days=14)
    four_weeks_ago = today - timedelta(days=28)
    week_start = _week_monday(today)

    # ==================================================================
    # 1. Headline metrics — 4 scalar queries (unavoidable, very fast)
    # ==================================================================

    total_transcripts = (await db.execute(
        select(func.count(Transcript.id))
    )).scalar_one()

    total_decisions = (await db.execute(
        select(func.count(Decision.id))
    )).scalar_one()

    open_actions_count = (await db.execute(
        select(func.count(ActionItem.id)).where(ActionItem.status == "OPEN")
    )).scalar_one()

    critical_threads_count = (await db.execute(
        select(func.count(OpenThread.id)).where(OpenThread.status == "OPEN")
    )).scalar_one()

    # ==================================================================
    # 2. Programme Pulse — Project cards via batch GROUP BY queries
    # ==================================================================

    # 2a. All projects with workstream codes in one LEFT JOIN query
    proj_ws_result = await db.execute(
        select(
            Project.id,
            Project.name,
            Project.status,
            Project.color,
            Project.is_custom,
            Workstream.code.label("ws_code"),
        )
        .outerjoin(Workstream, Project.workstream_id == Workstream.id)
        .order_by(Project.is_custom, Project.name)
    )
    project_rows = proj_ws_result.all()
    project_ids = [r[0] for r in project_rows]

    # 2b. Entity counts grouped by (project_id, entity_type) — one query
    link_counts_result = await db.execute(
        select(
            ProjectLink.project_id,
            ProjectLink.entity_type,
            func.count(ProjectLink.id),
        )
        .where(ProjectLink.project_id.in_(project_ids))
        .group_by(ProjectLink.project_id, ProjectLink.entity_type)
    )
    link_counts: dict[int, dict[str, int]] = defaultdict(dict)
    for pid, etype, cnt in link_counts_result.all():
        link_counts[pid][etype] = cnt

    # 2c. Last activity date per project (max transcript meeting_date) — one query
    last_activity_result = await db.execute(
        select(
            ProjectLink.project_id,
            func.max(Transcript.meeting_date),
        )
        .join(Transcript, and_(
            ProjectLink.entity_id == Transcript.id,
            ProjectLink.entity_type == "transcript",
        ))
        .where(ProjectLink.project_id.in_(project_ids))
        .group_by(ProjectLink.project_id)
    )
    last_activity_map: dict[int, date | None] = {}
    for pid, max_date in last_activity_result.all():
        last_activity_map[pid] = max_date

    # 2d. Transcript trend: recent (last 2 weeks) vs previous (2-4 weeks) — two queries
    recent_trend_result = await db.execute(
        select(
            ProjectLink.project_id,
            func.count(Transcript.id),
        )
        .join(Transcript, and_(
            ProjectLink.entity_id == Transcript.id,
            ProjectLink.entity_type == "transcript",
        ))
        .where(
            ProjectLink.project_id.in_(project_ids),
            Transcript.meeting_date >= two_weeks_ago,
        )
        .group_by(ProjectLink.project_id)
    )
    recent_map: dict[int, int] = dict(recent_trend_result.all())

    prev_trend_result = await db.execute(
        select(
            ProjectLink.project_id,
            func.count(Transcript.id),
        )
        .join(Transcript, and_(
            ProjectLink.entity_id == Transcript.id,
            ProjectLink.entity_type == "transcript",
        ))
        .where(
            ProjectLink.project_id.in_(project_ids),
            Transcript.meeting_date >= four_weeks_ago,
            Transcript.meeting_date < two_weeks_ago,
        )
        .group_by(ProjectLink.project_id)
    )
    prev_map: dict[int, int] = dict(prev_trend_result.all())

    # Assemble project cards — pure Python, no DB calls
    project_cards: list[DashboardProjectCard] = []
    for pid, pname, pstatus, pcolor, pis_custom, ws_code in project_rows:
        counts = link_counts.get(pid, {})
        recent = recent_map.get(pid, 0)
        prev = prev_map.get(pid, 0)
        trend = "up" if recent > prev else ("down" if recent < prev else "flat")
        la = last_activity_map.get(pid)

        project_cards.append(DashboardProjectCard(
            id=pid,
            name=pname,
            status=pstatus,
            color=pcolor,
            workstream_code=ws_code,
            is_custom=pis_custom,
            transcript_count=counts.get("transcript", 0),
            action_count=counts.get("action_item", 0),
            open_thread_count=counts.get("open_thread", 0),
            decision_count=counts.get("decision", 0),
            last_activity_date=str(la) if la else None,
            trend=trend,
        ))

    # ==================================================================
    # 3. Activity Feed — batch project lookups
    # ==================================================================

    recent_transcripts_result = await db.execute(
        select(Transcript).order_by(desc(Transcript.meeting_date)).limit(10)
    )
    recent_transcripts = recent_transcripts_result.scalars().all()

    recent_decisions_result = await db.execute(
        select(Decision).order_by(desc(Decision.decision_date)).limit(10)
    )
    recent_decisions = recent_decisions_result.scalars().all()

    # Batch-fetch project mappings for all activity entities
    transcript_proj_map = await _batch_project_links_to_projects(
        db, "transcript", [t.id for t in recent_transcripts]
    )
    decision_proj_map = await _batch_project_links_to_projects(
        db, "decision", [d.id for d in recent_decisions]
    )

    activity_items: list[ActivityFeedItem] = []
    for t in recent_transcripts:
        proj = transcript_proj_map.get(t.id)
        activity_items.append(ActivityFeedItem(
            id=t.id,
            entity_type="transcript",
            title=t.title or t.filename,
            date=str(t.meeting_date) if t.meeting_date else None,
            project_id=proj[0] if proj else None,
            project_name=proj[1] if proj else None,
        ))

    for d in recent_decisions:
        proj = decision_proj_map.get(d.id)
        text = d.decision[:80] + "..." if len(d.decision) > 80 else d.decision
        activity_items.append(ActivityFeedItem(
            id=d.id,
            entity_type="decision",
            title=f"Decision #{d.number}: {text}",
            date=str(d.decision_date) if d.decision_date else None,
            project_id=proj[0] if proj else None,
            project_name=proj[1] if proj else None,
        ))

    activity_items.sort(key=lambda x: x.date or "", reverse=True)
    activity_items = activity_items[:10]

    # ==================================================================
    # 4. Needs Attention — batch project lookups
    # ==================================================================

    open_actions_result = await db.execute(
        select(ActionItem).where(ActionItem.status == "OPEN")
    )
    all_open_actions = open_actions_result.scalars().all()

    # Determine which actions need attention and collect their IDs
    attention_action_ids: list[int] = []
    action_attention_data: list[tuple] = []  # (action, reason, days)
    for a in all_open_actions:
        parsed_deadline = _parse_date_string(a.deadline)
        reason = None
        days = None
        if parsed_deadline and parsed_deadline < today:
            reason = "overdue"
            days = (today - parsed_deadline).days
        elif a.action_date and (today - a.action_date).days > 14:
            reason = "stale"
            days = (today - a.action_date).days
        if reason:
            attention_action_ids.append(a.id)
            action_attention_data.append((a, reason, days))

    open_threads_result = await db.execute(
        select(OpenThread).where(OpenThread.status == "OPEN").order_by(OpenThread.number)
    )
    all_open_threads = open_threads_result.scalars().all()

    # Batch-fetch project mappings for attention items
    action_proj_map = await _batch_project_links_to_projects(
        db, "action_item", attention_action_ids
    )
    thread_proj_map = await _batch_project_links_to_projects(
        db, "open_thread", [t.id for t in all_open_threads]
    )

    attention_items: list[NeedsAttentionItem] = []
    for a, reason, days in action_attention_data:
        proj = action_proj_map.get(a.id)
        desc_text = a.description[:80] + "..." if len(a.description) > 80 else a.description
        attention_items.append(NeedsAttentionItem(
            id=a.id,
            entity_type="action_item",
            title=f"Action {a.number}: {desc_text}",
            description=a.description,
            status=a.status,
            owner=a.owner,
            reason=reason,
            days_overdue=days,
            project_id=proj[0] if proj else None,
            project_name=proj[1] if proj else None,
        ))

    for t in all_open_threads:
        parsed_raised = _parse_date_string(t.first_raised)
        days = (today - parsed_raised).days if parsed_raised else None
        proj = thread_proj_map.get(t.id)
        attention_items.append(NeedsAttentionItem(
            id=t.id,
            entity_type="open_thread",
            title=t.title,
            description=t.context[:120] + "..." if t.context and len(t.context) > 120 else t.context,
            status=t.status,
            owner=None,
            reason="unresolved",
            days_overdue=days,
            project_id=proj[0] if proj else None,
            project_name=proj[1] if proj else None,
        ))

    reason_order = {"overdue": 0, "stale": 1, "unresolved": 2}
    attention_items.sort(key=lambda x: (reason_order.get(x.reason, 9), -(x.days_overdue or 0)))
    attention_items = attention_items[:10]

    # ==================================================================
    # 5. Stakeholder Engagement — batch mention queries
    # ==================================================================

    stakeholders_result = await db.execute(
        select(Stakeholder)
        .where(Stakeholder.tier.in_([1, 2]))
        .order_by(Stakeholder.tier, Stakeholder.name)
    )
    stakeholders = stakeholders_result.scalars().all()
    stakeholder_ids = [s.id for s in stakeholders]

    # Recent mentions (last 2 weeks) grouped by stakeholder — one query
    recent_mentions_result = await db.execute(
        select(
            TranscriptMention.stakeholder_id,
            func.coalesce(func.sum(TranscriptMention.mention_count), 0),
        )
        .join(Transcript, TranscriptMention.transcript_id == Transcript.id)
        .where(
            TranscriptMention.stakeholder_id.in_(stakeholder_ids),
            Transcript.meeting_date >= two_weeks_ago,
        )
        .group_by(TranscriptMention.stakeholder_id)
    )
    recent_mentions_map: dict[int, int] = dict(recent_mentions_result.all())

    # Previous mentions (2-4 weeks ago) grouped by stakeholder — one query
    prev_mentions_result = await db.execute(
        select(
            TranscriptMention.stakeholder_id,
            func.coalesce(func.sum(TranscriptMention.mention_count), 0),
        )
        .join(Transcript, TranscriptMention.transcript_id == Transcript.id)
        .where(
            TranscriptMention.stakeholder_id.in_(stakeholder_ids),
            Transcript.meeting_date >= four_weeks_ago,
            Transcript.meeting_date < two_weeks_ago,
        )
        .group_by(TranscriptMention.stakeholder_id)
    )
    prev_mentions_map: dict[int, int] = dict(prev_mentions_result.all())

    # Last mentioned date per stakeholder — one query
    last_mention_result = await db.execute(
        select(
            TranscriptMention.stakeholder_id,
            func.max(Transcript.meeting_date),
        )
        .join(Transcript, TranscriptMention.transcript_id == Transcript.id)
        .where(TranscriptMention.stakeholder_id.in_(stakeholder_ids))
        .group_by(TranscriptMention.stakeholder_id)
    )
    last_mention_map: dict[int, date] = dict(last_mention_result.all())

    engagement_items: list[StakeholderEngagementItem] = []
    for s in stakeholders:
        recent_m = recent_mentions_map.get(s.id, 0)
        prev_m = prev_mentions_map.get(s.id, 0)

        if recent_m == 0 and prev_m == 0:
            trend = "silent"
        elif recent_m > prev_m:
            trend = "rising"
        elif recent_m < prev_m:
            trend = "declining"
        else:
            trend = "stable"

        last_d = last_mention_map.get(s.id)
        engagement_items.append(StakeholderEngagementItem(
            id=s.id,
            name=s.name,
            tier=s.tier,
            role=s.role,
            recent_mentions=recent_m,
            previous_mentions=prev_m,
            trend=trend,
            last_mentioned_date=str(last_d) if last_d else None,
        ))

    # ==================================================================
    # 6. KPI sparkline data
    # ==================================================================

    weekly = await _compute_weekly_counts(db, today, weeks=7)

    transcripts_this_week = (await db.execute(
        select(func.count(Transcript.id)).where(Transcript.meeting_date >= week_start)
    )).scalar_one()

    overdue_actions_count = 0
    for a in all_open_actions:
        parsed = _parse_date_string(a.deadline)
        if parsed and parsed < today:
            overdue_actions_count += 1

    critical_high_risks = (await db.execute(
        select(func.count(OpenThread.id)).where(
            OpenThread.status == "OPEN",
            OpenThread.severity.in_(["CRITICAL", "HIGH"]),
        )
    )).scalar_one()

    escalating_risks = (await db.execute(
        select(func.count(OpenThread.id)).where(
            OpenThread.status == "OPEN",
            OpenThread.trend == "escalating",
        )
    )).scalar_one()

    blocked_deps = (await db.execute(
        select(func.count(Dependency.id)).where(Dependency.status == "blocked")
    )).scalar_one()

    in_progress_deps = (await db.execute(
        select(func.count(Dependency.id)).where(Dependency.status == "in-progress")
    )).scalar_one()

    resources_result = await db.execute(select(ResourceAllocation))
    all_resources = resources_result.scalars().all()
    if all_resources:
        total_util = 0.0
        for r in all_resources:
            if r.allocations and isinstance(r.allocations, list):
                total_util += sum(
                    a.get("percentage", 0) for a in r.allocations if isinstance(a, dict)
                )
        avg_utilization = round(total_util / len(all_resources), 1)
        overloaded_count = sum(1 for r in all_resources if r.capacity_status == "overloaded")
    else:
        avg_utilization = 0.0
        overloaded_count = 0

    active_projects = sum(1 for c in project_cards if c.status == "active")

    kpi = KpiData(
        total_transcripts=total_transcripts,
        transcripts_this_week=transcripts_this_week,
        weekly_transcript_counts=weekly["transcripts"],
        open_actions=open_actions_count,
        overdue_actions=overdue_actions_count,
        weekly_open_action_counts=weekly["open_actions"],
        critical_high_risks=critical_high_risks,
        escalating_risks=escalating_risks,
        weekly_risk_counts=weekly["risks"],
        blocked_dependencies=blocked_deps,
        in_progress_dependencies=in_progress_deps,
        weekly_blocked_counts=weekly["blocked_deps"],
        avg_utilization=avg_utilization,
        overloaded_count=overloaded_count,
        weekly_utilization=weekly["utilization"],
        total_projects=len(project_cards),
        active_projects=active_projects,
    )

    # ==================================================================
    # 7. Insights
    # ==================================================================

    total_actions = (await db.execute(
        select(func.count(ActionItem.id))
    )).scalar_one()
    completed_actions = (await db.execute(
        select(func.count(ActionItem.id)).where(ActionItem.status != "OPEN")
    )).scalar_one()
    action_completion_rate = round(
        (completed_actions / total_actions * 100) if total_actions > 0 else 0.0, 1
    )

    # Decision velocity: decisions this week vs previous week
    prev_week_start = week_start - timedelta(days=7)
    decisions_this_week = (await db.execute(
        select(func.count(Decision.id)).where(Decision.decision_date >= week_start)
    )).scalar_one()
    decisions_prev_week = (await db.execute(
        select(func.count(Decision.id)).where(
            Decision.decision_date >= prev_week_start,
            Decision.decision_date < week_start,
        )
    )).scalar_one()
    decision_velocity = decisions_this_week - decisions_prev_week

    # Scope creep: additions vs originals
    scope_additions = (await db.execute(
        select(func.count(ScopeItem.id)).where(ScopeItem.scope_type == "addition")
    )).scalar_one()
    scope_total = (await db.execute(
        select(func.count(ScopeItem.id))
    )).scalar_one()
    scope_creep_pct = round(
        (scope_additions / scope_total * 100) if scope_total > 0 else 0.0, 1
    )

    # Risk velocity: new risks this week vs previous
    risk_velocity = escalating_risks

    # Overdue SLA %: overdue actions as % of all open
    overdue_sla_pct = round(
        (overdue_actions_count / open_actions_count * 100) if open_actions_count > 0 else 0.0, 1
    )

    insights = InsightsData(
        action_completion_rate=action_completion_rate,
        decision_velocity=decision_velocity,
        scope_creep_pct=scope_creep_pct,
        risk_velocity=risk_velocity,
        overdue_sla_pct=overdue_sla_pct,
    )

    # ==================================================================
    # 8. Programme Status — health computation
    # ==================================================================

    programme_status = await _compute_programme_status(
        db, today, open_actions_count, overdue_actions_count,
        critical_high_risks, escalating_risks, all_open_actions, all_open_threads,
    )

    # ==================================================================
    # Assemble response
    # ==================================================================

    return DashboardResponse(
        total_transcripts=total_transcripts,
        total_decisions=total_decisions,
        open_actions=open_actions_count,
        critical_threads=critical_threads_count,
        projects=project_cards,
        recent_activity=activity_items,
        needs_attention=attention_items,
        stakeholder_engagement=engagement_items,
        programme_status=programme_status,
        kpi=kpi,
        insights=insights,
    )


# ---------------------------------------------------------------------------
# Programme status helper
# ---------------------------------------------------------------------------

async def _compute_programme_status(
    db: AsyncSession,
    today: date,
    open_actions: int,
    overdue_count: int,
    critical_risks: int,
    escalating_risks: int,
    all_open_actions: list,
    all_open_threads: list,
) -> ProgrammeStatus:
    """Compute the programme health narrative, RAG, biggest win, biggest risk."""

    # Health score: weighted combination
    # Action completion contributes positively
    total_actions = (await db.execute(
        select(func.count(ActionItem.id))
    )).scalar_one()
    completed_actions = (await db.execute(
        select(func.count(ActionItem.id)).where(ActionItem.status != "OPEN")
    )).scalar_one()
    completion_rate = (completed_actions / total_actions * 100) if total_actions > 0 else 50.0

    # Overdue ratio penalises
    overdue_ratio = (overdue_count / open_actions * 100) if open_actions > 0 else 0.0
    overdue_score = max(0, 100 - overdue_ratio * 2)  # 50% overdue -> score 0

    # Risk escalation penalises
    risk_score = 100.0
    if critical_risks > 0:
        risk_score -= min(40, critical_risks * 15)
    if escalating_risks > 0:
        risk_score -= min(30, escalating_risks * 10)
    risk_score = max(0, risk_score)

    # Resource strain
    resources_result = await db.execute(select(ResourceAllocation))
    all_resources = resources_result.scalars().all()
    overloaded = sum(1 for r in all_resources if r.capacity_status == "overloaded")
    resource_score = 100.0
    if all_resources:
        overloaded_pct = overloaded / len(all_resources) * 100
        resource_score = max(0, 100 - overloaded_pct * 2)

    # Weighted average
    health_score = (
        completion_rate * 0.30
        + overdue_score * 0.25
        + risk_score * 0.25
        + resource_score * 0.20
    )
    health_rag = _rag_from_score(health_score)

    # Biggest win: most recently completed action
    recent_completed = (await db.execute(
        select(ActionItem)
        .where(ActionItem.status != "OPEN", ActionItem.completed_date.isnot(None))
        .order_by(desc(ActionItem.completed_date))
        .limit(1)
    )).scalar_one_or_none()

    biggest_win = None
    if recent_completed:
        desc_text = recent_completed.description
        if len(desc_text) > 100:
            desc_text = desc_text[:100] + "..."
        biggest_win = f"Action {recent_completed.number} completed: {desc_text}"
    else:
        # Fall back to most recent decision
        recent_decision = (await db.execute(
            select(Decision).order_by(desc(Decision.decision_date)).limit(1)
        )).scalar_one_or_none()
        if recent_decision:
            d_text = recent_decision.decision
            if len(d_text) > 100:
                d_text = d_text[:100] + "..."
            biggest_win = f"Decision #{recent_decision.number}: {d_text}"

    # Biggest risk: top critical/escalating thread
    biggest_risk = None
    critical_thread = (await db.execute(
        select(OpenThread)
        .where(
            OpenThread.status == "OPEN",
            OpenThread.severity.in_(["CRITICAL", "HIGH"]),
        )
        .order_by(
            case(
                (OpenThread.severity == "CRITICAL", 0),
                (OpenThread.severity == "HIGH", 1),
                else_=2,
            ),
            case(
                (OpenThread.trend == "escalating", 0),
                (OpenThread.trend == "stable", 1),
                else_=2,
            ),
        )
        .limit(1)
    )).scalar_one_or_none()

    if critical_thread:
        biggest_risk = f"[{critical_thread.severity}] {critical_thread.title}"
        if critical_thread.trend == "escalating":
            biggest_risk += " (escalating)"
    elif overdue_count > 0:
        biggest_risk = f"{overdue_count} overdue action(s) requiring attention"

    # Narrative
    narrative_parts = []
    if health_rag == "green":
        narrative_parts.append("Programme is progressing well.")
    elif health_rag == "amber":
        narrative_parts.append("Programme has areas requiring attention.")
    else:
        narrative_parts.append("Programme health is concerning and needs intervention.")

    if overdue_count > 0:
        narrative_parts.append(
            f"{overdue_count} action{'s are' if overdue_count != 1 else ' is'} overdue."
        )
    if critical_risks > 0:
        narrative_parts.append(
            f"{critical_risks} critical/high risk thread{'s' if critical_risks != 1 else ''} open."
        )
    if overloaded > 0:
        narrative_parts.append(
            f"{overloaded} team member{'s' if overloaded != 1 else ''} at capacity."
        )

    narrative = " ".join(narrative_parts)

    return ProgrammeStatus(
        narrative=narrative,
        health_rag=health_rag,
        biggest_win=biggest_win,
        biggest_risk=biggest_risk,
        open_actions=open_actions,
        overdue_count=overdue_count,
        critical_risks=critical_risks,
    )


# ---------------------------------------------------------------------------
# GET /api/dashboard/brief
# ---------------------------------------------------------------------------

@router.get("/dashboard/brief", response_model=ProgrammeBrief)
async def get_brief(db: AsyncSession = Depends(get_db)):
    today = date.today()
    week_start = _week_monday(today)

    ws_result = await db.execute(select(Workstream).order_by(Workstream.code))
    workstreams = ws_result.scalars().all()

    lines = [f"Programme Status -- {today.strftime('%d %b %Y')}", ""]
    for ws in workstreams:
        lines.append(f"{ws.code} {ws.name}: {ws.status}")

    # Overdue actions
    open_actions_result = await db.execute(
        select(ActionItem).where(ActionItem.status == "OPEN")
    )
    all_open = open_actions_result.scalars().all()

    overdue: list[tuple[int, str]] = []
    overdue_count = 0
    for a in all_open:
        parsed = _parse_date_string(a.deadline)
        if parsed and parsed < today:
            days = (today - parsed).days
            overdue.append((
                days,
                f"Action {a.number}: {a.description[:60]} -- {a.owner or 'Unassigned'} [{days}d overdue]",
            ))
            overdue_count += 1
    overdue.sort(key=lambda x: -x[0])

    open_threads_result = await db.execute(
        select(OpenThread).where(OpenThread.status == "OPEN").limit(5)
    )
    all_threads = open_threads_result.scalars().all()
    thread_lines: list[str] = []
    for t in all_threads:
        parsed = _parse_date_string(t.first_raised)
        age = f" [{(today - parsed).days}d]" if parsed else ""
        thread_lines.append(f"Thread: {t.title} -- OPEN{age}")

    if overdue or thread_lines:
        attention = [item[1] for item in overdue[:3]] + thread_lines[:3]
        lines.extend(["", f"Needs Attention ({len(attention)} items):"])
        for item in attention:
            lines.append(f"  {item}")

    transcript_count = (await db.execute(
        select(func.count(Transcript.id)).where(Transcript.meeting_date >= week_start)
    )).scalar_one()
    decision_count = (await db.execute(
        select(func.count(Decision.id)).where(Decision.decision_date >= week_start)
    )).scalar_one()

    open_count = len(all_open)
    thread_count = (await db.execute(
        select(func.count(OpenThread.id)).where(OpenThread.status == "OPEN")
    )).scalar_one()

    lines.extend([
        "",
        f"This Week: {transcript_count} transcripts, {decision_count} decisions",
        f"Open: {open_count} actions | {thread_count} threads",
    ])

    text = "\n".join(lines)

    # -- Structured fields --

    # Health RAG from action completion + risk count
    total_actions = (await db.execute(
        select(func.count(ActionItem.id))
    )).scalar_one()
    completed_actions = (await db.execute(
        select(func.count(ActionItem.id)).where(ActionItem.status != "OPEN")
    )).scalar_one()
    completion_rate = (completed_actions / total_actions * 100) if total_actions > 0 else 50.0

    critical_risks = (await db.execute(
        select(func.count(OpenThread.id)).where(
            OpenThread.status == "OPEN",
            OpenThread.severity.in_(["CRITICAL", "HIGH"]),
        )
    )).scalar_one()
    escalating_risks = (await db.execute(
        select(func.count(OpenThread.id)).where(
            OpenThread.status == "OPEN",
            OpenThread.trend == "escalating",
        )
    )).scalar_one()

    overdue_ratio = (overdue_count / open_count * 100) if open_count > 0 else 0.0
    overdue_score = max(0, 100 - overdue_ratio * 2)
    risk_score = max(0, 100 - min(40, critical_risks * 15) - min(30, escalating_risks * 10))
    health_score = completion_rate * 0.40 + overdue_score * 0.30 + risk_score * 0.30
    health_rag = _rag_from_score(health_score)

    # Narrative
    narrative_parts = []
    if health_rag == "green":
        narrative_parts.append("Programme is on track.")
    elif health_rag == "amber":
        narrative_parts.append("Programme requires monitoring.")
    else:
        narrative_parts.append("Programme health needs intervention.")

    if overdue_count > 0:
        narrative_parts.append(f"{overdue_count} overdue action{'s' if overdue_count != 1 else ''}.")
    if critical_risks > 0:
        narrative_parts.append(f"{critical_risks} critical/high risk{'s' if critical_risks != 1 else ''}.")

    narrative = " ".join(narrative_parts)

    # Biggest win
    recent_completed = (await db.execute(
        select(ActionItem)
        .where(ActionItem.status != "OPEN", ActionItem.completed_date.isnot(None))
        .order_by(desc(ActionItem.completed_date))
        .limit(1)
    )).scalar_one_or_none()

    biggest_win = None
    if recent_completed:
        win_text = recent_completed.description
        if len(win_text) > 80:
            win_text = win_text[:80] + "..."
        biggest_win = f"Action {recent_completed.number} completed: {win_text}"
    else:
        recent_decision = (await db.execute(
            select(Decision).order_by(desc(Decision.decision_date)).limit(1)
        )).scalar_one_or_none()
        if recent_decision:
            d_text = recent_decision.decision
            if len(d_text) > 80:
                d_text = d_text[:80] + "..."
            biggest_win = f"Decision #{recent_decision.number}: {d_text}"

    # Biggest risk
    biggest_risk = None
    top_thread = (await db.execute(
        select(OpenThread)
        .where(
            OpenThread.status == "OPEN",
            OpenThread.severity.in_(["CRITICAL", "HIGH"]),
        )
        .order_by(
            case(
                (OpenThread.severity == "CRITICAL", 0),
                (OpenThread.severity == "HIGH", 1),
                else_=2,
            ),
            case(
                (OpenThread.trend == "escalating", 0),
                (OpenThread.trend == "stable", 1),
                else_=2,
            ),
        )
        .limit(1)
    )).scalar_one_or_none()

    if top_thread:
        biggest_risk = f"[{top_thread.severity}] {top_thread.title}"
        if top_thread.trend == "escalating":
            biggest_risk += " (escalating)"
    elif overdue_count > 0:
        biggest_risk = f"{overdue_count} overdue action(s)"

    return ProgrammeBrief(
        date=str(today),
        text=text,
        narrative=narrative,
        health_rag=health_rag,
        biggest_win=biggest_win,
        biggest_risk=biggest_risk,
    )
