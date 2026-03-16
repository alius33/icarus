from pydantic import BaseModel


class ProgrammeWinSchema(BaseModel):
    id: int
    category: str
    title: str
    description: str | None = None
    before_state: str | None = None
    after_state: str | None = None
    project: str | None = None
    confidence: str = "estimated"
    date_recorded: str | None = None
    notes: str | None = None
    is_manual: bool = True


class ProgrammeWinCreate(BaseModel):
    category: str
    title: str
    description: str | None = None
    before_state: str | None = None
    after_state: str | None = None
    project: str | None = None
    confidence: str = "estimated"
    date_recorded: str | None = None
    notes: str | None = None


class ProgrammeWinUpdate(BaseModel):
    category: str | None = None
    title: str | None = None
    description: str | None = None
    before_state: str | None = None
    after_state: str | None = None
    project: str | None = None
    confidence: str | None = None
    date_recorded: str | None = None
    notes: str | None = None


class ProgrammeWinGrouped(BaseModel):
    category: str
    count: int
    wins: list[ProgrammeWinSchema]


class ProgrammeWinSummary(BaseModel):
    total: int
    by_category: dict[str, int]
    by_confidence: dict[str, int]
