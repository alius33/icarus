from pydantic import BaseModel

from app.schemas.programme_deliverable import ProgressSnapshotBase, ProgressSnapshotCreate


class WeeklyPlanActionBase(BaseModel):
    id: int
    weekly_plan_id: int
    category: str
    title: str
    description: str | None = None
    priority: str = "MEDIUM"
    owner: str | None = None
    status: str = "PENDING"
    deliverable_id: int | None = None
    position: int = 0
    is_ai_generated: bool = True
    carried_from_week: int | None = None
    source_transcript_id: int | None = None
    source_transcript_title: str | None = None
    context: str | None = None


class WeeklyPlanActionCreate(BaseModel):
    category: str
    title: str
    description: str | None = None
    priority: str = "MEDIUM"
    owner: str | None = None
    status: str = "PENDING"
    deliverable_id: int | None = None
    position: int = 0
    is_ai_generated: bool = True
    carried_from_week: int | None = None
    source_transcript_id: int | None = None
    context: str | None = None


class WeeklyPlanActionUpdate(BaseModel):
    category: str | None = None
    title: str | None = None
    description: str | None = None
    priority: str | None = None
    owner: str | None = None
    status: str | None = None
    deliverable_id: int | None = None
    position: int | None = None
    is_ai_generated: bool | None = None
    source_transcript_id: int | None = None
    context: str | None = None


class WeeklyPlanBase(BaseModel):
    id: int
    week_number: int
    week_start_date: str
    week_end_date: str
    deliverable_progress_summary: str | None = None
    programme_actions_summary: str | None = None
    status: str = "DRAFT"


class WeeklyPlanCreate(BaseModel):
    week_number: int
    week_start_date: str
    week_end_date: str
    deliverable_progress_summary: str | None = None
    programme_actions_summary: str | None = None
    status: str = "DRAFT"
    actions: list[WeeklyPlanActionCreate] = []
    snapshots: list[ProgressSnapshotCreate] = []


class WeeklyPlanUpdate(BaseModel):
    deliverable_progress_summary: str | None = None
    programme_actions_summary: str | None = None
    status: str | None = None


class WeeklyPlanFull(WeeklyPlanBase):
    actions: list[WeeklyPlanActionBase] = []
    snapshots: list[ProgressSnapshotBase] = []
