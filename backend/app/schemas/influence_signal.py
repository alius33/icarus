from pydantic import BaseModel


class InfluenceSignalBase(BaseModel):
    id: int
    date: str | None = None
    person: str
    influence_type: str
    direction: str | None = None
    target_person: str | None = None
    topic: str | None = None
    evidence: str | None = None
    strength: str | None = None
    confidence: str | None = None
    coalition_name: str | None = None
    coalition_members: str | None = None
    alignment: str | None = None
    transcript_id: int | None = None
    is_manual: bool = False


class InfluenceSignalCreate(BaseModel):
    date: str | None = None
    person: str
    influence_type: str
    direction: str | None = None
    target_person: str | None = None
    topic: str | None = None
    evidence: str | None = None
    strength: str | None = None
    confidence: str | None = None
    coalition_name: str | None = None
    coalition_members: str | None = None
    alignment: str | None = None
    transcript_id: int | None = None


class InfluenceSignalUpdate(BaseModel):
    date: str | None = None
    person: str | None = None
    influence_type: str | None = None
    direction: str | None = None
    target_person: str | None = None
    topic: str | None = None
    evidence: str | None = None
    strength: str | None = None
    confidence: str | None = None
    coalition_name: str | None = None
    coalition_members: str | None = None
    alignment: str | None = None
    transcript_id: int | None = None
