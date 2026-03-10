from pydantic import BaseModel


class DecisionSchema(BaseModel):
    id: int
    number: int = 0
    title: str
    description: str | None = None
    date: str | None = None
    status: str
    execution_status: str = "made"
    rationale: str | None = None
    key_people: list[str] = []
    owner: str | None = None
    workstream: str | None = None
    position: int = 0
    transcript_id: int | None = None
    transcript_title: str | None = None
    is_manual: bool = False


class DecisionCreate(BaseModel):
    decision: str
    date: str | None = None
    rationale: str | None = None
    key_people: list[str] = []
    execution_status: str = "made"
    workstream: str | None = None


class DecisionUpdate(BaseModel):
    decision: str | None = None
    date: str | None = None
    rationale: str | None = None
    key_people: list[str] | None = None
    execution_status: str | None = None
    workstream: str | None = None


class DecisionPositionUpdate(BaseModel):
    execution_status: str
    position: int


class DecisionBoardColumn(BaseModel):
    status: str
    label: str
    color: str
    order: int
    decisions: list[DecisionSchema]
    count: int


class DecisionBoardResponse(BaseModel):
    columns: list[DecisionBoardColumn]
    total: int


class DecisionTimelineItem(BaseModel):
    id: int
    number: int
    title: str
    execution_status: str
    key_people: list[str] = []
    decision_date: str | None = None
    workstream: str | None = None


class DecisionTimelineResponse(BaseModel):
    decisions: list[DecisionTimelineItem]
    total: int
