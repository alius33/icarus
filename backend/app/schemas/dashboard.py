import datetime
from typing import Optional, Literal

from pydantic import BaseModel


# -- Dashboard Project Card (Programme Pulse) ---------------------------------

class DashboardProjectCard(BaseModel):
    id: int
    name: str
    status: str
    color: Optional[str] = None
    workstream_code: Optional[str] = None
    is_custom: bool
    transcript_count: int = 0
    action_count: int = 0
    open_thread_count: int = 0
    decision_count: int = 0
    last_activity_date: Optional[str] = None
    trend: Literal["up", "down", "flat"] = "flat"


# -- Activity Feed ------------------------------------------------------------

class ActivityFeedItem(BaseModel):
    id: int
    entity_type: str
    title: str
    date: Optional[str] = None
    project_id: Optional[int] = None
    project_name: Optional[str] = None


# -- Needs Attention ----------------------------------------------------------

class NeedsAttentionItem(BaseModel):
    id: int
    entity_type: str
    title: str
    description: Optional[str] = None
    status: str
    owner: Optional[str] = None
    reason: str  # "overdue" | "stale" | "unresolved"
    days_overdue: Optional[int] = None
    project_id: Optional[int] = None
    project_name: Optional[str] = None


# -- Stakeholder Engagement ---------------------------------------------------

class StakeholderEngagementItem(BaseModel):
    id: int
    name: str
    tier: int
    role: Optional[str] = None
    recent_mentions: int = 0
    previous_mentions: int = 0
    trend: Literal["rising", "stable", "declining", "silent"] = "stable"
    last_mentioned_date: Optional[str] = None


# -- KPI Data -----------------------------------------------------------------

class KpiData(BaseModel):
    total_transcripts: int
    transcripts_this_week: int
    weekly_transcript_counts: list[int]  # last 7 weeks
    open_actions: int
    overdue_actions: int
    weekly_open_action_counts: list[int]
    critical_high_risks: int
    escalating_risks: int
    weekly_risk_counts: list[int]
    blocked_dependencies: int
    in_progress_dependencies: int
    weekly_blocked_counts: list[int]
    avg_utilization: float
    overloaded_count: int
    weekly_utilization: list[float]
    total_projects: int
    active_projects: int


# -- Insights -----------------------------------------------------------------

class InsightsData(BaseModel):
    action_completion_rate: float
    decision_velocity: int  # decisions this period vs previous
    scope_creep_pct: float
    risk_velocity: int
    overdue_sla_pct: float


# -- Health Score -------------------------------------------------------------

class HealthScore(BaseModel):
    score: float
    rag: Literal["green", "amber", "red"]
    breakdown: dict  # signal name -> score


# -- Programme Status ---------------------------------------------------------

class ProgrammeStatus(BaseModel):
    narrative: str
    health_rag: Literal["green", "amber", "red"]
    biggest_win: Optional[str] = None
    biggest_risk: Optional[str] = None
    open_actions: int
    overdue_count: int
    critical_risks: int


# -- Dashboard Response -------------------------------------------------------

class DashboardResponse(BaseModel):
    total_transcripts: int
    total_decisions: int
    open_actions: int
    critical_threads: int
    projects: list[DashboardProjectCard]
    recent_activity: list[ActivityFeedItem]
    needs_attention: list[NeedsAttentionItem]
    stakeholder_engagement: list[StakeholderEngagementItem]
    programme_status: ProgrammeStatus
    kpi: KpiData
    insights: InsightsData


# -- Leadership Brief ---------------------------------------------------------

class ProgrammeBrief(BaseModel):
    date: str
    text: str
    narrative: Optional[str] = None
    health_rag: Optional[str] = None
    biggest_win: Optional[str] = None
    biggest_risk: Optional[str] = None
