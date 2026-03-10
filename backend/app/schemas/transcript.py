
from pydantic import BaseModel


class TranscriptBase(BaseModel):
    id: int
    file_name: str
    title: str | None = None
    date: str | None = None
    participant_count: int
    word_count: int
    has_summary: bool
    primary_project_id: int | None = None
    primary_project_name: str | None = None


class TranscriptDetail(TranscriptBase):
    raw_text: str
    participants: list[str]
    summary: "SummaryBase | None" = None


class TranscriptList(BaseModel):
    items: list[TranscriptBase]
    total: int
    page: int
    limit: int
    pages: int


# Avoid circular import — import at module level for forward ref resolution
from app.schemas.summary import SummaryBase  # noqa: E402

TranscriptDetail.model_rebuild()
