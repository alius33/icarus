from pydantic import BaseModel


class TranscriptAttachmentBase(BaseModel):
    id: int
    transcript_id: int
    original_filename: str
    file_type: str
    size_bytes: int
    has_extracted_text: bool
    created_at: str


class TranscriptAttachmentDetail(TranscriptAttachmentBase):
    extracted_text: str | None = None


class TranscriptContextResponse(BaseModel):
    notes: str | None = None
    attachments: list[dict]  # [{filename, extracted_text}]
