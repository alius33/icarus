from pydantic import BaseModel


class DivisionProfileSchema(BaseModel):
    id: int
    name: str
    status: str = "not_engaged"
    current_tools: str | None = None
    pain_points: str | None = None
    key_contact: str | None = None
    notes: str | None = None


class DivisionProfileCreate(BaseModel):
    name: str
    status: str = "not_engaged"
    current_tools: str | None = None
    pain_points: str | None = None
    key_contact: str | None = None
    notes: str | None = None


class DivisionProfileUpdate(BaseModel):
    name: str | None = None
    status: str | None = None
    current_tools: str | None = None
    pain_points: str | None = None
    key_contact: str | None = None
    notes: str | None = None
