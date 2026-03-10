from pydantic import BaseModel


class TaskSchema(BaseModel):
    id: int
    identifier: str
    title: str
    description: str | None = None
    status: str
    priority: str = "NONE"
    assignee: str | None = None
    labels: list[str] = []
    due_date: str | None = None
    start_date: str | None = None
    estimate: int | None = None
    position: int = 0
    project_id: int | None = None
    project_name: str | None = None
    parent_id: int | None = None
    parent_identifier: str | None = None
    sub_task_count: int = 0
    created_date: str | None = None
    completed_date: str | None = None
    is_manual: bool = False


class TaskCreate(BaseModel):
    title: str
    description: str | None = None
    status: str = "TODO"
    priority: str = "NONE"
    assignee: str | None = None
    labels: list[str] = []
    due_date: str | None = None
    start_date: str | None = None
    estimate: int | None = None
    project_id: int | None = None
    parent_id: int | None = None


class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    status: str | None = None
    priority: str | None = None
    assignee: str | None = None
    labels: list[str] | None = None
    due_date: str | None = None
    start_date: str | None = None
    estimate: int | None = None
    project_id: int | None = None
    parent_id: int | None = None


class TaskPositionUpdate(BaseModel):
    status: str
    position: int


class TaskBoardColumn(BaseModel):
    status: str
    label: str
    color: str
    order: int
    tasks: list[TaskSchema]
    count: int


class TaskBoardResponse(BaseModel):
    columns: list[TaskBoardColumn]
    total: int


class TaskTimelineItem(BaseModel):
    id: int
    identifier: str
    title: str
    status: str
    priority: str
    assignee: str | None = None
    start_date: str | None = None
    due_date: str | None = None
    project_name: str | None = None


class TaskTimelineResponse(BaseModel):
    tasks: list[TaskTimelineItem]
    total: int
