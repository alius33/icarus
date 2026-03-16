from sqlalchemy import Column, DateTime, ForeignKey, Index, Integer, LargeBinary, String, Text
from sqlalchemy.orm import relationship

from app.database import Base, utcnow


class TranscriptAttachment(Base):
    __tablename__ = "transcript_attachments"

    id = Column(Integer, primary_key=True)
    transcript_id = Column(
        Integer,
        ForeignKey("transcripts.id", ondelete="CASCADE"),
        nullable=False,
    )
    original_filename = Column(String, nullable=False)
    stored_filename = Column(String, nullable=False)
    file_type = Column(String, nullable=False)  # "pdf", "pptx", "docx"
    mime_type = Column(String, nullable=False)
    size_bytes = Column(Integer, nullable=False)
    file_data = Column(LargeBinary, nullable=False)  # Binary for Railway persistence
    extracted_text = Column(Text, nullable=True)
    storage_path = Column(String, nullable=True)  # Local filesystem path (best-effort)
    created_at = Column(DateTime, default=utcnow)

    transcript = relationship("Transcript", back_populates="attachments")

    __table_args__ = (
        Index("idx_transcript_attachments_tid", "transcript_id"),
    )
