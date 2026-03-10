from pydantic import BaseModel


class ProjectSummaryBase(BaseModel):
    id: int
    project_id: int
    transcript_id: int
    date: str | None = None
    relevance: str | None = None
    content: str
    source_file: str | None = None


class ProjectSummaryCreate(BaseModel):
    project_id: int
    transcript_id: int
    date: str | None = None
    relevance: str | None = None
    content: str
    source_file: str | None = None
