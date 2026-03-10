from pydantic import BaseModel


class ActionItemSchema(BaseModel):
    id: int
    title: str
    description: str | None = None
    status: str
    owner: str | None = None
    due_date: str | None = None
    source_transcript_id: int | None = None
    source_transcript_title: str | None = None
    workstream: str | None = None
    is_manual: bool = False


class ActionItemCreate(BaseModel):
    description: str
    owner: str | None = None
    deadline: str | None = None
    context: str | None = None
    status: str = "OPEN"


class ActionItemUpdate(BaseModel):
    description: str | None = None
    owner: str | None = None
    deadline: str | None = None
    context: str | None = None
    status: str | None = None
