from pydantic import BaseModel


class ProjectUpdateBase(BaseModel):
    id: int
    title: str
    content: str
    content_type: str
    summary: str | None = None
    is_processed: bool
    created_at: str
    updated_at: str
    project_ids: list[int] = []
    project_names: list[str] = []


class ProjectUpdateDetail(ProjectUpdateBase):
    raw_content: str | None = None


class ProjectUpdateCreate(BaseModel):
    title: str
    content: str
    content_type: str = "note"
    project_ids: list[int] = []


class ProjectUpdateUpdate(BaseModel):
    title: str | None = None
    content: str | None = None
    content_type: str | None = None
    project_ids: list[int] | None = None
    summary: str | None = None
