from pydantic import BaseModel


class WeeklyReportBase(BaseModel):
    id: int
    title: str
    week_start: str
    week_end: str
    period_label: str | None = None


class WeeklyReportDetail(WeeklyReportBase):
    content: str
    workstream_updates: list[str]
    highlights: list[str]
    risks: list[str]
