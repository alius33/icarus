from typing import Literal

from pydantic import BaseModel

from app.schemas.transcript import TranscriptBase
from app.schemas.summary import SummaryBase
from app.schemas.decision import DecisionSchema
from app.schemas.action_item import ActionItemSchema
from app.schemas.open_thread import OpenThreadSchema
from app.schemas.stakeholder import StakeholderBase


EntityType = Literal[
    "transcript", "summary", "decision",
    "action_item", "open_thread", "stakeholder",
]


class ProjectLinkSchema(BaseModel):
    id: int
    project_id: int
    entity_type: EntityType
    entity_id: int


class ProjectBase(BaseModel):
    id: int
    name: str
    description: str | None = None
    is_custom: bool
    status: str
    color: str | None = None
    icon: str | None = None
    workstream_id: int | None = None
    workstream_code: str | None = None
    transcript_count: int = 0
    summary_count: int = 0
    decision_count: int = 0
    action_count: int = 0
    open_thread_count: int = 0
    stakeholder_count: int = 0


class ProjectCreate(BaseModel):
    name: str
    description: str | None = None
    status: str = "active"
    color: str | None = None
    icon: str | None = None


class ProjectUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    status: str | None = None
    color: str | None = None
    icon: str | None = None


class ProjectHub(BaseModel):
    project: ProjectBase
    transcripts: list[TranscriptBase]
    summaries: list[SummaryBase]
    decisions: list[DecisionSchema]
    action_items: list[ActionItemSchema]
    open_threads: list[OpenThreadSchema]
    stakeholders: list[StakeholderBase]


class ProjectLinkCreate(BaseModel):
    entity_type: EntityType
    entity_id: int


class ProjectLinkBulkCreate(BaseModel):
    links: list[ProjectLinkCreate]


# ── Weekly Timeline ──────────────────────────────────────────────────────

class WeekTranscriptItem(BaseModel):
    id: int
    title: str | None = None
    file_name: str
    date: str | None = None
    participant_count: int = 0
    word_count: int = 0
    has_summary: bool = False
    summary_id: int | None = None
    summary_tldr: str | None = None
    summary_content: str | None = None


class WeekDecisionItem(BaseModel):
    id: int
    number: int
    decision: str
    rationale: str | None = None
    key_people: list[str] = []


class WeekActionItem(BaseModel):
    id: int
    number: str
    description: str
    owner: str | None = None
    status: str
    deadline: str | None = None


class ProjectWeek(BaseModel):
    week_start: str
    week_end: str
    week_label: str
    weekly_report_id: int | None = None
    weekly_report_content: str | None = None
    transcripts: list[WeekTranscriptItem] = []
    decisions: list[WeekDecisionItem] = []
    action_items: list[WeekActionItem] = []
    transcript_count: int = 0
    decision_count: int = 0
    action_count: int = 0


class ProjectWeeklyTimeline(BaseModel):
    project: ProjectBase
    weeks: list[ProjectWeek]
    total_weeks: int
