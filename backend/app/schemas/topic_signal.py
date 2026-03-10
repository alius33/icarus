from pydantic import BaseModel


class TopicSignalBase(BaseModel):
    id: int
    date: str | None = None
    topic: str
    category: str | None = None
    intensity: str | None = None
    first_raised: str | None = None
    meetings_count: int = 1
    trend: str | None = None
    key_quote: str | None = None
    confidence: str | None = None
    transcript_id: int | None = None
    is_manual: bool = False


class TopicSignalCreate(BaseModel):
    date: str | None = None
    topic: str
    category: str | None = None
    intensity: str | None = None
    first_raised: str | None = None
    meetings_count: int = 1
    trend: str | None = None
    key_quote: str | None = None
    confidence: str | None = None
    transcript_id: int | None = None


class TopicSignalUpdate(BaseModel):
    date: str | None = None
    topic: str | None = None
    category: str | None = None
    intensity: str | None = None
    first_raised: str | None = None
    meetings_count: int | None = None
    trend: str | None = None
    key_quote: str | None = None
    confidence: str | None = None
    transcript_id: int | None = None
