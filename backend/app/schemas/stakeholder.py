from pydantic import BaseModel


class MentionItem(BaseModel):
    transcript_id: int
    transcript_title: str | None = None
    date: str | None = None
    snippet: str


class StakeholderBase(BaseModel):
    id: int
    name: str
    role: str | None = None
    organisation: str | None = None
    tier: int
    mention_count: int
    risk_level: str | None = None
    morale_notes: str | None = None
    is_manual: bool = False


class StakeholderDetail(StakeholderBase):
    notes: str | None = None
    aliases: list[str]
    recent_mentions: list[MentionItem]


class StakeholderCreate(BaseModel):
    name: str
    tier: int = 3
    role: str | None = None
    notes: str | None = None


class StakeholderUpdate(BaseModel):
    tier: int | None = None
    role: str | None = None
    notes: str | None = None
    risk_level: str | None = None
    morale_notes: str | None = None
