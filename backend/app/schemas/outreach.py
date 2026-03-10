from pydantic import BaseModel


class OutreachSchema(BaseModel):
    id: int
    contact_name: str
    contact_role: str | None = None
    division: str | None = None
    status: str = "initial_contact"
    interest_level: int = 1
    first_contact_date: str | None = None
    last_contact_date: str | None = None
    meeting_count: int = 0
    notes: str | None = None
    next_step: str | None = None
    next_step_date: str | None = None
    external_id: str | None = None
    external_source: str | None = None


class OutreachCreate(BaseModel):
    contact_name: str
    contact_role: str | None = None
    division: str | None = None
    status: str = "initial_contact"
    interest_level: int = 1
    first_contact_date: str | None = None
    last_contact_date: str | None = None
    meeting_count: int = 0
    notes: str | None = None
    next_step: str | None = None
    next_step_date: str | None = None
    external_id: str | None = None
    external_source: str | None = None


class OutreachUpdate(BaseModel):
    contact_name: str | None = None
    contact_role: str | None = None
    division: str | None = None
    status: str | None = None
    interest_level: int | None = None
    first_contact_date: str | None = None
    last_contact_date: str | None = None
    meeting_count: int | None = None
    notes: str | None = None
    next_step: str | None = None
    next_step_date: str | None = None
    external_id: str | None = None
    external_source: str | None = None
