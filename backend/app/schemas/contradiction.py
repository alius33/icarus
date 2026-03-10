from pydantic import BaseModel


class ContradictionBase(BaseModel):
    id: int
    date: str | None = None
    contradiction_type: str
    person: str | None = None
    statement_a: str | None = None
    date_a: str | None = None
    statement_b: str | None = None
    date_b: str | None = None
    severity: str | None = None
    resolution: str = "unresolved"
    confidence: str | None = None
    gap_description: str | None = None
    expected_source: str | None = None
    last_mentioned: str | None = None
    meetings_absent: int | None = None
    entry_kind: str = "contradiction"
    transcript_id: int | None = None
    is_manual: bool = False


class ContradictionCreate(BaseModel):
    date: str | None = None
    contradiction_type: str
    person: str | None = None
    statement_a: str | None = None
    date_a: str | None = None
    statement_b: str | None = None
    date_b: str | None = None
    severity: str | None = None
    resolution: str = "unresolved"
    confidence: str | None = None
    gap_description: str | None = None
    expected_source: str | None = None
    last_mentioned: str | None = None
    meetings_absent: int | None = None
    entry_kind: str = "contradiction"
    transcript_id: int | None = None


class ContradictionUpdate(BaseModel):
    date: str | None = None
    contradiction_type: str | None = None
    person: str | None = None
    statement_a: str | None = None
    date_a: str | None = None
    statement_b: str | None = None
    date_b: str | None = None
    severity: str | None = None
    resolution: str | None = None
    confidence: str | None = None
    gap_description: str | None = None
    expected_source: str | None = None
    last_mentioned: str | None = None
    meetings_absent: int | None = None
    entry_kind: str | None = None
    transcript_id: int | None = None
