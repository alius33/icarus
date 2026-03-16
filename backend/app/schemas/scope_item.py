from pydantic import BaseModel


class ScopeItemSchema(BaseModel):
    id: int
    name: str
    scope_type: str
    project: str | None = None
    added_date: str | None = None
    estimated_effort: str | None = None
    budgeted: bool = False
    status: str = "planned"
    description: str | None = None
    impact_notes: str | None = None


class ScopeItemCreate(BaseModel):
    name: str
    scope_type: str = "addition"
    project: str | None = None
    added_date: str | None = None
    estimated_effort: str | None = None
    budgeted: bool = False
    status: str = "planned"
    description: str | None = None
    impact_notes: str | None = None


class ScopeItemUpdate(BaseModel):
    name: str | None = None
    scope_type: str | None = None
    project: str | None = None
    added_date: str | None = None
    estimated_effort: str | None = None
    budgeted: bool | None = None
    status: str | None = None
    description: str | None = None
    impact_notes: str | None = None
