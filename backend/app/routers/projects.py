import re
from datetime import timedelta

from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.exceptions import ForbiddenError, NotFoundError
from app.models.task import Task
from app.models.decision import Decision
from app.models.open_thread import OpenThread
from app.models.project import Project
from app.models.project_link import ProjectLink
from app.models.project_summary import ProjectSummary
from app.models.project_update import ProjectUpdate as ProjectUpdateModel
from app.models.stakeholder import Stakeholder
from app.models.summary import Summary
from app.models.transcript import Transcript
from app.models.transcript_mention import TranscriptMention
from app.models.weekly_report import WeeklyReport
from app.schemas.action_item import ActionItemSchema
from app.schemas.task import TaskSchema
from app.schemas.decision import DecisionSchema
from app.schemas.open_thread import OpenThreadSchema
from app.schemas.project_summary import ProjectSummaryBase
from app.schemas.project_update import ProjectUpdateBase as ProjectUpdateBaseSchema
from app.schemas.project import (
    ProjectBase,
    ProjectCreate,
    ProjectHub,
    ProjectLinkBulkCreate,
    ProjectLinkSchema,
    ProjectUpdate,
    ProjectWeek,
    ProjectWeeklyTimeline,
    WeekActionItem,
    WeekDecisionItem,
    WeekTranscriptItem,
)
from app.schemas.stakeholder import StakeholderBase
from app.schemas.summary import SummaryBase
from app.schemas.transcript import TranscriptBase

router = APIRouter(tags=["projects"])


# ── Helpers ──────────────────────────────────────────────────────────────────

async def _get_project_or_404(project_id: int, db: AsyncSession) -> Project:
    result = await db.execute(select(Project).where(Project.id == project_id))
    project = result.scalar_one_or_none()
    if not project:
        raise NotFoundError("Project", project_id)
    return project


async def _build_project_base(project: Project, db: AsyncSession) -> ProjectBase:
    # Count links by entity type
    count_result = await db.execute(
        select(ProjectLink.entity_type, func.count(ProjectLink.id))
        .where(ProjectLink.project_id == project.id)
        .group_by(ProjectLink.entity_type)
    )
    counts = dict(count_result.all())

    # Count project summaries from the dedicated table (not ProjectLink)
    ps_count_result = await db.execute(
        select(func.count(ProjectSummary.id))
        .where(ProjectSummary.project_id == project.id)
    )
    ps_count = ps_count_result.scalar() or 0

    return ProjectBase(
        id=project.id,
        name=project.name,
        description=project.description,
        is_custom=project.is_custom,
        status=project.status,
        color=project.color,
        icon=project.icon,
        code=project.code,
        transcript_count=counts.get("transcript", 0),
        summary_count=ps_count,
        decision_count=counts.get("decision", 0),
        action_count=counts.get("task", 0) or counts.get("action_item", 0),
        open_thread_count=counts.get("open_thread", 0),
        stakeholder_count=counts.get("stakeholder", 0),
    )


def _transcript_base(
    t: Transcript, has_summary: bool, project_name: str | None = None,
) -> TranscriptBase:
    return TranscriptBase(
        id=t.id,
        file_name=t.filename,
        title=t.title,
        date=str(t.meeting_date) if t.meeting_date else None,
        participant_count=len(t.participants) if t.participants else 0,
        word_count=t.word_count or 0,
        has_summary=has_summary,
        primary_project_id=t.primary_project_id,
        primary_project_name=project_name,
    )


def _summary_base(s: Summary, transcript_title: str | None) -> SummaryBase:
    return SummaryBase(
        id=s.id,
        transcript_id=s.transcript_id or 0,
        transcript_title=transcript_title,
        date=None,
        tldr=None,
    )


def _decision_schema(d: Decision) -> DecisionSchema:
    return DecisionSchema(
        id=d.id,
        title=f"Decision #{d.number}",
        description=d.decision,
        date=str(d.decision_date) if d.decision_date else None,
        status="recorded",
        owner=", ".join(d.key_people) if d.key_people else None,
        project_id=None,
        project_name=None,
        transcript_id=None,
        transcript_title=None,
    )


def _action_schema(a: Task) -> ActionItemSchema:
    return ActionItemSchema(
        id=a.id,
        title=a.title or f"Action {a.number}",
        description=a.description,
        status=a.status,
        owner=a.assignee or a.owner,
        due_date=str(a.due_date) if a.due_date else a.deadline,
        source_transcript_id=None,
        source_transcript_title=None,
        project=None,
    )


def _thread_schema(t: OpenThread) -> OpenThreadSchema:
    return OpenThreadSchema(
        id=t.id,
        title=t.title,
        description=t.context,
        status=t.status,
        priority=None,
        owner=None,
        opened_date=t.first_raised,
        last_discussed=None,
        project=None,
    )


async def _stakeholder_base(s: Stakeholder, db: AsyncSession) -> StakeholderBase:
    mention_result = await db.execute(
        select(func.coalesce(func.sum(TranscriptMention.mention_count), 0))
        .where(TranscriptMention.stakeholder_id == s.id)
    )
    mention_count = mention_result.scalar_one()
    return StakeholderBase(
        id=s.id,
        name=s.name,
        role=s.role,
        organisation=None,
        tier=s.tier,
        mention_count=mention_count,
    )


# ── Endpoints ────────────────────────────────────────────────────────────────

@router.get("/projects", response_model=list[ProjectBase])
async def list_projects(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Project).order_by(Project.is_custom, Project.name)
    )
    projects = result.scalars().all()
    return [await _build_project_base(p, db) for p in projects]


@router.get("/projects/{project_id}", response_model=ProjectBase)
async def get_project(project_id: int, db: AsyncSession = Depends(get_db)):
    project = await _get_project_or_404(project_id, db)
    return await _build_project_base(project, db)


@router.get("/projects/{project_id}/hub", response_model=ProjectHub)
async def get_project_hub(project_id: int, db: AsyncSession = Depends(get_db)):
    project = await _get_project_or_404(project_id, db)
    project_base = await _build_project_base(project, db)

    # Gather all linked entity IDs grouped by type
    link_result = await db.execute(
        select(ProjectLink.entity_type, ProjectLink.entity_id)
        .where(ProjectLink.project_id == project_id)
    )
    links_by_type: dict[str, list[int]] = {}
    for entity_type, entity_id in link_result.all():
        links_by_type.setdefault(entity_type, []).append(entity_id)

    # Fetch transcripts
    transcript_ids = links_by_type.get("transcript", [])
    transcripts: list[TranscriptBase] = []
    if transcript_ids:
        t_result = await db.execute(
            select(Transcript).where(Transcript.id.in_(transcript_ids))
            .order_by(Transcript.meeting_date.desc())
        )
        t_rows = t_result.scalars().all()
        # Check which have summaries
        sum_result = await db.execute(
            select(Summary.transcript_id).where(Summary.transcript_id.in_(transcript_ids))
        )
        summary_tids = {row[0] for row in sum_result.all()}
        transcripts = [_transcript_base(t, t.id in summary_tids) for t in t_rows]

    # Fetch summaries
    summary_ids = links_by_type.get("summary", [])
    summaries: list[SummaryBase] = []
    if summary_ids:
        s_result = await db.execute(
            select(Summary, Transcript.title)
            .outerjoin(Transcript, Summary.transcript_id == Transcript.id)
            .where(Summary.id.in_(summary_ids))
            .order_by(Summary.id)
        )
        summaries = [_summary_base(s, title) for s, title in s_result.all()]

    # Fetch decisions
    decision_ids = links_by_type.get("decision", [])
    decisions: list[DecisionSchema] = []
    if decision_ids:
        d_result = await db.execute(
            select(Decision).where(Decision.id.in_(decision_ids))
            .order_by(Decision.decision_date.asc(), Decision.number.asc())
        )
        decisions = [_decision_schema(d) for d in d_result.scalars().all()]

    # Fetch tasks (linked via project_links or direct project_id)
    action_ids = links_by_type.get("task", links_by_type.get("action_item", []))
    action_items: list[ActionItemSchema] = []
    # Also include tasks with direct project_id FK
    direct_task_result = await db.execute(
        select(Task).where(Task.project_id == project_id)
        .order_by(Task.created_date, Task.number)
    )
    direct_tasks = direct_task_result.scalars().all()
    seen_ids = {t.id for t in direct_tasks}
    action_items = [_action_schema(a) for a in direct_tasks]
    if action_ids:
        a_result = await db.execute(
            select(Task).where(Task.id.in_(action_ids))
            .order_by(Task.created_date, Task.number)
        )
        for a in a_result.scalars().all():
            if a.id not in seen_ids:
                action_items.append(_action_schema(a))

    # Fetch open threads
    thread_ids = links_by_type.get("open_thread", [])
    open_threads: list[OpenThreadSchema] = []
    if thread_ids:
        ot_result = await db.execute(
            select(OpenThread).where(OpenThread.id.in_(thread_ids))
            .order_by(OpenThread.number)
        )
        open_threads = [_thread_schema(t) for t in ot_result.scalars().all()]

    # Fetch stakeholders (batch mention counts to avoid N+1)
    stakeholder_ids = links_by_type.get("stakeholder", [])
    stakeholders: list[StakeholderBase] = []
    if stakeholder_ids:
        sh_result = await db.execute(
            select(Stakeholder).where(Stakeholder.id.in_(stakeholder_ids))
            .order_by(Stakeholder.tier, Stakeholder.name)
        )
        sh_list = sh_result.scalars().all()
        mc_result = await db.execute(
            select(
                TranscriptMention.stakeholder_id,
                func.coalesce(func.sum(TranscriptMention.mention_count), 0),
            )
            .where(TranscriptMention.stakeholder_id.in_(stakeholder_ids))
            .group_by(TranscriptMention.stakeholder_id)
        )
        mc_map = dict(mc_result.all())
        stakeholders = [
            StakeholderBase(
                id=s.id, name=s.name, role=s.role, organisation=None,
                tier=s.tier, mention_count=mc_map.get(s.id, 0),
            )
            for s in sh_list
        ]

    # Fetch project summaries linked to this project
    ps_result = await db.execute(
        select(ProjectSummary)
        .where(ProjectSummary.project_id == project_id)
        .order_by(ProjectSummary.date.desc().nullslast())
    )
    project_summaries_list: list[ProjectSummaryBase] = [
        ProjectSummaryBase(
            id=ps.id,
            project_id=ps.project_id,
            transcript_id=ps.transcript_id,
            project_update_id=ps.project_update_id,
            date=str(ps.date) if ps.date else None,
            relevance=ps.relevance,
            content=ps.content,
            source_file=ps.source_file,
        )
        for ps in ps_result.scalars().all()
    ]

    # Fetch project updates
    update_ids = links_by_type.get("project_update", [])
    project_updates_list: list[ProjectUpdateBaseSchema] = []
    if update_ids:
        pu_result = await db.execute(
            select(ProjectUpdateModel).where(ProjectUpdateModel.id.in_(update_ids))
            .order_by(ProjectUpdateModel.created_at.desc())
        )
        project_updates_list = [
            ProjectUpdateBaseSchema(
                id=pu.id,
                title=pu.title,
                content=pu.content,
                content_type=pu.content_type,
                is_processed=pu.is_processed,
                created_at=pu.created_at.isoformat() if pu.created_at else "",
                updated_at=pu.updated_at.isoformat() if pu.updated_at else "",
                project_ids=[project_id],
                project_names=[project_base.name],
            )
            for pu in pu_result.scalars().all()
        ]

    return ProjectHub(
        project=project_base,
        transcripts=transcripts,
        summaries=summaries,
        decisions=decisions,
        action_items=action_items,
        open_threads=open_threads,
        stakeholders=stakeholders,
        project_summaries=project_summaries_list,
        project_updates=project_updates_list,
    )


# ── Weekly Timeline ──────────────────────────────────────────────────────

def _strip_markdown(text: str) -> str:
    """Strip markdown syntax for TLDR extraction."""
    text = re.sub(r"^#+\s+.*$", "", text, flags=re.MULTILINE)  # headings
    text = re.sub(r"\*\*([^*]+)\*\*", r"\1", text)  # bold
    text = re.sub(r"\*([^*]+)\*", r"\1", text)  # italic
    text = re.sub(r"^\|.*\|$", "", text, flags=re.MULTILINE)  # tables
    text = re.sub(r"^[-*]\s+", "", text, flags=re.MULTILINE)  # list markers
    text = re.sub(r"\n{2,}", "\n", text)  # multiple newlines
    return text.strip()


def _week_start(d) -> str:
    """Return the Monday of the ISO week as a string."""
    monday = d - timedelta(days=d.weekday())
    return str(monday)


def _week_label(start_date, end_date) -> str:
    """Format a week label like '3–9 Mar 2026'."""
    from datetime import date as date_type
    if isinstance(start_date, str):
        start_date = date_type.fromisoformat(start_date)
    if isinstance(end_date, str):
        end_date = date_type.fromisoformat(end_date)
    s_month = start_date.strftime("%b")
    e_month = end_date.strftime("%b")
    if s_month == e_month:
        return f"{start_date.day}–{end_date.day} {s_month} {end_date.year}"
    return f"{start_date.day} {s_month} – {end_date.day} {e_month} {end_date.year}"


@router.get("/projects/{project_id}/weekly", response_model=ProjectWeeklyTimeline)
async def get_project_weekly(project_id: int, db: AsyncSession = Depends(get_db)):
    project = await _get_project_or_404(project_id, db)
    project_base = await _build_project_base(project, db)

    # Gather linked entity IDs
    link_result = await db.execute(
        select(ProjectLink.entity_type, ProjectLink.entity_id)
        .where(ProjectLink.project_id == project_id)
    )
    links_by_type: dict[str, list[int]] = {}
    for entity_type, entity_id in link_result.all():
        links_by_type.setdefault(entity_type, []).append(entity_id)

    # ── Fetch transcripts with summaries ─────────────────────────────
    transcript_ids = links_by_type.get("transcript", [])
    week_buckets: dict[str, dict] = {}  # key = week_start string

    if transcript_ids:
        t_result = await db.execute(
            select(Transcript, Summary.id, Summary.content)
            .outerjoin(Summary, Summary.transcript_id == Transcript.id)
            .where(Transcript.id.in_(transcript_ids))
            .order_by(Transcript.meeting_date.desc())
        )
        for t, sum_id, sum_content in t_result.all():
            if t.meeting_date:
                ws = _week_start(t.meeting_date)
            else:
                ws = "undated"

            if ws not in week_buckets:
                week_buckets[ws] = {"transcripts": [], "decisions": [], "action_items": []}

            # Build TLDR from summary content
            tldr = None
            if sum_content:
                stripped = _strip_markdown(sum_content)
                tldr = stripped[:200] + "..." if len(stripped) > 200 else stripped

            week_buckets[ws]["transcripts"].append(WeekTranscriptItem(
                id=t.id,
                title=t.title,
                file_name=t.filename,
                date=str(t.meeting_date) if t.meeting_date else None,
                participant_count=len(t.participants) if t.participants else 0,
                word_count=t.word_count or 0,
                has_summary=sum_id is not None,
                summary_id=sum_id,
                summary_tldr=tldr,
                summary_content=sum_content,
            ))

    # ── Fetch decisions ──────────────────────────────────────────────
    decision_ids = links_by_type.get("decision", [])
    if decision_ids:
        d_result = await db.execute(
            select(Decision).where(Decision.id.in_(decision_ids))
            .order_by(Decision.decision_date.asc(), Decision.number.asc())
        )
        for d in d_result.scalars().all():
            if d.decision_date:
                ws = _week_start(d.decision_date)
            else:
                ws = "undated"

            if ws not in week_buckets:
                week_buckets[ws] = {"transcripts": [], "decisions": [], "action_items": []}

            week_buckets[ws]["decisions"].append(WeekDecisionItem(
                id=d.id,
                number=d.number,
                decision=d.decision,
                rationale=d.rationale,
                key_people=d.key_people or [],
            ))

    # ── Fetch tasks ─────────────────────────────────────────────────
    action_ids = links_by_type.get("task", links_by_type.get("action_item", []))
    # Also get tasks with direct project_id FK
    all_task_result = await db.execute(
        select(Task).where(Task.project_id == project_id)
        .order_by(Task.created_date, Task.number)
    )
    all_tasks = list(all_task_result.scalars().all())
    seen_task_ids = {t.id for t in all_tasks}
    if action_ids:
        linked_result = await db.execute(
            select(Task).where(Task.id.in_(action_ids))
            .order_by(Task.created_date, Task.number)
        )
        for t in linked_result.scalars().all():
            if t.id not in seen_task_ids:
                all_tasks.append(t)
                seen_task_ids.add(t.id)

    for a in all_tasks:
        if a.created_date:
            ws = _week_start(a.created_date)
        elif a.action_date:
            ws = _week_start(a.action_date)
        else:
            ws = "undated"

        if ws not in week_buckets:
            week_buckets[ws] = {"transcripts": [], "decisions": [], "action_items": []}

        week_buckets[ws]["action_items"].append(WeekActionItem(
            id=a.id,
            number=a.number,
            description=a.description or a.title,
            owner=a.assignee or a.owner,
            status=a.status,
            deadline=str(a.due_date) if a.due_date else a.deadline,
        ))

    # ── Fetch all weekly reports, keyed by the Monday of their week ──
    wr_result = await db.execute(
        select(WeeklyReport).order_by(WeeklyReport.week_start.desc())
    )
    weekly_reports_by_start: dict[str, tuple[int, str]] = {}
    for wr in wr_result.scalars().all():
        if wr.week_start:
            # Normalise to Monday of the ISO week (handles reports dated
            # on any day of the week, e.g. Tuesday or Thursday)
            monday = wr.week_start - timedelta(days=wr.week_start.weekday())
            weekly_reports_by_start[str(monday)] = (wr.id, wr.content)

    # ── Assemble weeks sorted newest-first, filling gaps ────────────
    from datetime import date as date_type

    # Collect all dated week-start keys (exclude "undated")
    dated_keys = sorted(
        [k for k in week_buckets if k != "undated"],
        reverse=True,
    )

    weeks: list[ProjectWeek] = []

    # Add undated bucket first if it exists
    if "undated" in week_buckets:
        bucket = week_buckets["undated"]
        weeks.append(ProjectWeek(
            week_start="undated",
            week_end="undated",
            week_label="Undated Items",
            transcripts=bucket["transcripts"],
            decisions=bucket["decisions"],
            action_items=bucket["action_items"],
            transcript_count=len(bucket["transcripts"]),
            decision_count=len(bucket["decisions"]),
            action_count=len(bucket["action_items"]),
        ))

    # Fill in every week from newest to oldest, including gaps
    if dated_keys:
        newest = date_type.fromisoformat(dated_keys[0])
        oldest = date_type.fromisoformat(dated_keys[-1])

        cursor = newest
        while cursor >= oldest:
            ws_key = str(cursor)
            bucket = week_buckets.get(ws_key, {
                "transcripts": [], "decisions": [], "action_items": [],
            })
            end = cursor + timedelta(days=6)

            # Match weekly report by week_start date
            wr_data = weekly_reports_by_start.get(ws_key)
            wr_id = wr_data[0] if wr_data else None
            wr_content = wr_data[1] if wr_data else None

            weeks.append(ProjectWeek(
                week_start=str(cursor),
                week_end=str(end),
                week_label=_week_label(cursor, end),
                weekly_report_id=wr_id,
                weekly_report_content=wr_content,
                transcripts=bucket["transcripts"],
                decisions=bucket["decisions"],
                action_items=bucket["action_items"],
                transcript_count=len(bucket["transcripts"]),
                decision_count=len(bucket["decisions"]),
                action_count=len(bucket["action_items"]),
            ))
            cursor -= timedelta(days=7)

    return ProjectWeeklyTimeline(
        project=project_base,
        weeks=weeks,
        total_weeks=len(weeks),
    )


@router.post("/projects", response_model=ProjectBase, status_code=201)
async def create_project(body: ProjectCreate, db: AsyncSession = Depends(get_db)):
    project = Project(
        name=body.name,
        description=body.description,
        is_custom=True,
        status=body.status,
        color=body.color,
        icon=body.icon,
    )
    db.add(project)
    await db.commit()
    await db.refresh(project)
    return await _build_project_base(project, db)


@router.patch("/projects/{project_id}", response_model=ProjectBase)
async def update_project(
    project_id: int,
    body: ProjectUpdate,
    db: AsyncSession = Depends(get_db),
):
    project = await _get_project_or_404(project_id, db)

    update_data = body.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(project, key, value)

    await db.commit()
    await db.refresh(project)
    return await _build_project_base(project, db)


@router.delete("/projects/{project_id}")
async def delete_project(project_id: int, db: AsyncSession = Depends(get_db)):
    project = await _get_project_or_404(project_id, db)

    if not project.is_custom:
        raise ForbiddenError("Cannot delete seed projects. Only custom projects can be deleted.")

    await db.delete(project)
    await db.commit()
    return {"ok": True}


@router.post("/projects/{project_id}/links", response_model=list[ProjectLinkSchema])
async def add_project_links(
    project_id: int,
    body: ProjectLinkBulkCreate,
    db: AsyncSession = Depends(get_db),
):
    await _get_project_or_404(project_id, db)

    created = []
    for link_data in body.links:
        # Check if link already exists
        existing = await db.execute(
            select(ProjectLink).where(
                ProjectLink.project_id == project_id,
                ProjectLink.entity_type == link_data.entity_type,
                ProjectLink.entity_id == link_data.entity_id,
            )
        )
        if existing.scalar_one_or_none():
            continue

        link = ProjectLink(
            project_id=project_id,
            entity_type=link_data.entity_type,
            entity_id=link_data.entity_id,
        )
        db.add(link)
        await db.flush()
        created.append(ProjectLinkSchema(
            id=link.id,
            project_id=link.project_id,
            entity_type=link.entity_type,
            entity_id=link.entity_id,
        ))

    await db.commit()
    return created


@router.delete("/projects/{project_id}/links/{link_id}")
async def remove_project_link(
    project_id: int,
    link_id: int,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(ProjectLink).where(
            ProjectLink.id == link_id,
            ProjectLink.project_id == project_id,
        )
    )
    link = result.scalar_one_or_none()
    if not link:
        raise NotFoundError("Link", link_id)

    await db.delete(link)
    await db.commit()
    return {"ok": True}
