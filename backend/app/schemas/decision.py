from pydantic import BaseModel


class DecisionSchema(BaseModel):
    id: int
    title: str
    description: str | None = None
    date: str | None = None
    status: str
    owner: str | None = None
    workstream: str | None = None
    transcript_id: int | None = None
    transcript_title: str | None = None
    is_manual: bool = False


class DecisionCreate(BaseModel):
    decision: str
    date: str | None = None
    rationale: str | None = None
    key_people: list[str] = []
    workstream: str | None = None


class DecisionUpdate(BaseModel):
    decision: str | None = None
    date: str | None = None
    rationale: str | None = None
    key_people: list[str] | None = None
    workstream: str | None = None
