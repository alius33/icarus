from pydantic import BaseModel


class TranscriptNoteBase(BaseModel):
    id: int
    transcript_id: int
    content: str
    version: int
    created_at: str


class TranscriptNoteCurrent(BaseModel):
    content: str
    version: int
    created_at: str
    version_count: int


class TranscriptNoteHistory(BaseModel):
    versions: list[TranscriptNoteBase]


class TranscriptNoteUpdate(BaseModel):
    content: str
