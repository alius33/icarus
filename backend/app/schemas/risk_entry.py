from pydantic import BaseModel


class RiskEntryBase(BaseModel):
    id: int
    risk_id: str
    date: str | None = None
    title: str
    description: str | None = None
    category: str | None = None
    severity: str
    trajectory: str | None = None
    source_type: str | None = None
    owner: str | None = None
    mitigation: str | None = None
    last_reviewed: str | None = None
    meetings_mentioned: int = 1
    confidence: str | None = None
    transcript_id: int | None = None
    is_manual: bool = False


class RiskEntryCreate(BaseModel):
    risk_id: str
    date: str | None = None
    title: str
    description: str | None = None
    category: str | None = None
    severity: str
    trajectory: str | None = None
    source_type: str | None = None
    owner: str | None = None
    mitigation: str | None = None
    last_reviewed: str | None = None
    meetings_mentioned: int = 1
    confidence: str | None = None
    transcript_id: int | None = None


class RiskEntryUpdate(BaseModel):
    risk_id: str | None = None
    date: str | None = None
    title: str | None = None
    description: str | None = None
    category: str | None = None
    severity: str | None = None
    trajectory: str | None = None
    source_type: str | None = None
    owner: str | None = None
    mitigation: str | None = None
    last_reviewed: str | None = None
    meetings_mentioned: int | None = None
    confidence: str | None = None
    transcript_id: int | None = None
