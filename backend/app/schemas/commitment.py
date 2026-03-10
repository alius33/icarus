from pydantic import BaseModel


class CommitmentBase(BaseModel):
    id: int
    person: str
    commitment: str
    transcript_id: int | None = None
    date_made: str | None = None
    deadline_text: str | None = None
    deadline_resolved: str | None = None
    deadline_type: str | None = None
    condition: str | None = None
    linked_action_id: int | None = None
    status: str = "pending"
    verified_date: str | None = None
    notes: str | None = None
    is_manual: bool = False


class CommitmentCreate(BaseModel):
    person: str
    commitment: str
    transcript_id: int | None = None
    date_made: str | None = None
    deadline_text: str | None = None
    deadline_resolved: str | None = None
    deadline_type: str | None = None
    condition: str | None = None
    linked_action_id: int | None = None
    status: str = "pending"
    notes: str | None = None


class CommitmentUpdate(BaseModel):
    person: str | None = None
    commitment: str | None = None
    transcript_id: int | None = None
    date_made: str | None = None
    deadline_text: str | None = None
    deadline_resolved: str | None = None
    deadline_type: str | None = None
    condition: str | None = None
    linked_action_id: int | None = None
    status: str | None = None
    verified_date: str | None = None
    notes: str | None = None
