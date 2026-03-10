from pydantic import BaseModel


class SentimentSignalBase(BaseModel):
    id: int
    stakeholder_id: int
    transcript_id: int | None = None
    date: str | None = None
    sentiment: str
    shift: str | None = None
    topic: str | None = None
    quote: str | None = None
    notes: str | None = None
    is_manual: bool = False


class SentimentSignalCreate(BaseModel):
    stakeholder_id: int
    transcript_id: int | None = None
    date: str | None = None
    sentiment: str
    shift: str | None = None
    topic: str | None = None
    quote: str | None = None
    notes: str | None = None


class SentimentSignalUpdate(BaseModel):
    stakeholder_id: int | None = None
    transcript_id: int | None = None
    date: str | None = None
    sentiment: str | None = None
    shift: str | None = None
    topic: str | None = None
    quote: str | None = None
    notes: str | None = None
