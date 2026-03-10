from typing import Literal

from pydantic import BaseModel


class WorkstreamHealthScore(BaseModel):
    workstream_id: int
    workstream_code: str
    workstream_name: str
    score: float
    rag: Literal["green", "amber", "red"]
    breakdown: dict  # signal name -> individual score (0-100)


class MilestoneSchema(BaseModel):
    id: int
    workstream_id: int
    title: str
    status: str
    target_date: str | None = None
    notes: str | None = None


class WorkstreamBase(BaseModel):
    id: int
    code: str
    name: str
    owner: str | None = None
    status: str
    progress_pct: int | None = None
    blocker_reason: str | None = None
    assigned_fte: str | None = None


class WorkstreamDetail(WorkstreamBase):
    description: str | None = None
    milestones: list[MilestoneSchema]
    recent_mentions: list[str]
