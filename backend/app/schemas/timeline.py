from pydantic import BaseModel


class TimelineEvent(BaseModel):
    date: str
    type: str
    title: str
    description: str | None = None
    reference_id: int | None = None
    reference_url: str | None = None


class TimelineResponse(BaseModel):
    from_date: str
    to_date: str
    events: list[TimelineEvent]
    total: int
