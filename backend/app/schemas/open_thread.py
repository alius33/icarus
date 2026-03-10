from pydantic import BaseModel


class OpenThreadSchema(BaseModel):
    id: int
    title: str
    description: str | None = None
    status: str
    priority: str | None = None
    owner: str | None = None
    opened_date: str | None = None
    last_discussed: str | None = None
    workstream: str | None = None
    severity: str | None = None
    trend: str | None = None
    is_manual: bool = False


class OpenThreadCreate(BaseModel):
    title: str
    context: str | None = None
    question: str | None = None
    why_it_matters: str | None = None
    status: str = "OPEN"
    first_raised: str | None = None
    severity: str | None = None
    trend: str | None = None


class OpenThreadUpdate(BaseModel):
    title: str | None = None
    context: str | None = None
    question: str | None = None
    why_it_matters: str | None = None
    status: str | None = None
    resolution: str | None = None
    first_raised: str | None = None
    severity: str | None = None
    trend: str | None = None
