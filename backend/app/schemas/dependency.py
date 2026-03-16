from pydantic import BaseModel


class DependencySchema(BaseModel):
    id: int
    name: str
    dependency_type: str
    status: str
    blocking_reason: str | None = None
    estimated_effort: str | None = None
    assigned_to: str | None = None
    affected_projects: str | None = None
    priority: str = "MEDIUM"
    notes: str | None = None


class DependencyCreate(BaseModel):
    name: str
    dependency_type: str = "integration"
    status: str = "pending"
    blocking_reason: str | None = None
    estimated_effort: str | None = None
    assigned_to: str | None = None
    affected_projects: str | None = None
    priority: str = "MEDIUM"
    notes: str | None = None


class DependencyUpdate(BaseModel):
    name: str | None = None
    dependency_type: str | None = None
    status: str | None = None
    blocking_reason: str | None = None
    estimated_effort: str | None = None
    assigned_to: str | None = None
    affected_projects: str | None = None
    priority: str | None = None
    notes: str | None = None
