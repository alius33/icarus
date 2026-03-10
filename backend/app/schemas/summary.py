from pydantic import BaseModel


class SummaryBase(BaseModel):
    id: int
    transcript_id: int
    transcript_title: str | None = None
    date: str | None = None
    tldr: str | None = None


class SummaryDetail(SummaryBase):
    full_summary: str
    key_decisions: list[str]
    action_items: list[str]
    risks_and_concerns: list[str]
    follow_ups: list[str]
