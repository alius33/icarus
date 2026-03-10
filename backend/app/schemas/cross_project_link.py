from pydantic import BaseModel


class CrossProjectLinkBase(BaseModel):
    id: int
    source_project_id: int
    target_project_id: int
    link_type: str
    description: str | None = None
    transcript_id: int | None = None
    date_detected: str | None = None
    severity: str = "info"
    status: str = "active"
    is_manual: bool = False


class CrossProjectLinkCreate(BaseModel):
    source_project_id: int
    target_project_id: int
    link_type: str
    description: str | None = None
    transcript_id: int | None = None
    date_detected: str | None = None
    severity: str = "info"
    status: str = "active"


class CrossProjectLinkUpdate(BaseModel):
    source_project_id: int | None = None
    target_project_id: int | None = None
    link_type: str | None = None
    description: str | None = None
    transcript_id: int | None = None
    date_detected: str | None = None
    severity: str | None = None
    status: str | None = None
