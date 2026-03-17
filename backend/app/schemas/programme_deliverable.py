from pydantic import BaseModel


class DeliverableMilestoneBase(BaseModel):
    id: int
    deliverable_id: int
    title: str
    description: str | None = None
    status: str = "NOT_STARTED"
    target_week: int | None = None
    completed_week: int | None = None
    evidence: str | None = None
    position: int = 0


class DeliverableMilestoneCreate(BaseModel):
    title: str
    description: str | None = None
    status: str = "NOT_STARTED"
    target_week: int | None = None
    completed_week: int | None = None
    evidence: str | None = None
    position: int = 0


class DeliverableMilestoneUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    status: str | None = None
    target_week: int | None = None
    completed_week: int | None = None
    evidence: str | None = None
    position: int | None = None


class ProgressSnapshotBase(BaseModel):
    id: int
    deliverable_id: int
    weekly_plan_id: int
    week_number: int
    rag_status: str = "GREEN"
    progress_percent: int = 0
    milestones_completed: int = 0
    milestones_total: int = 0
    narrative: str | None = None


class ProgressSnapshotCreate(BaseModel):
    deliverable_id: int
    week_number: int
    rag_status: str = "GREEN"
    progress_percent: int = 0
    milestones_completed: int = 0
    milestones_total: int = 0
    narrative: str | None = None


class ProgrammeDeliverableBase(BaseModel):
    id: int
    pillar: int
    pillar_name: str
    title: str
    description: str | None = None
    position: int = 0
    project_id: int | None = None
    rag_status: str = "GREEN"
    progress_percent: int = 0
    notes: str | None = None


class ProgrammeDeliverableUpdate(BaseModel):
    project_id: int | None = None
    rag_status: str | None = None
    progress_percent: int | None = None
    notes: str | None = None


class DeliverableWithMilestones(ProgrammeDeliverableBase):
    milestones: list[DeliverableMilestoneBase] = []
    latest_snapshot: ProgressSnapshotBase | None = None


class DeliverableWithHistory(ProgrammeDeliverableBase):
    milestones: list[DeliverableMilestoneBase] = []
    snapshots: list[ProgressSnapshotBase] = []


class PillarSummary(BaseModel):
    pillar: int
    pillar_name: str
    deliverables: list[DeliverableWithMilestones]
    aggregate_progress: int = 0
    aggregate_rag: str = "GREEN"


class DeliverableOverview(BaseModel):
    pillars: list[PillarSummary]
