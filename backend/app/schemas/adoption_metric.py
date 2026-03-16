from pydantic import BaseModel


class AdoptionMetricSchema(BaseModel):
    id: int
    date: str
    metric_type: str
    value: int
    project: str | None = None
    notes: str | None = None


class AdoptionMetricCreate(BaseModel):
    date: str
    metric_type: str
    value: int
    project: str | None = None
    notes: str | None = None
