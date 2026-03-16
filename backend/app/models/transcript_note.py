from sqlalchemy import Column, DateTime, ForeignKey, Index, Integer, Text
from sqlalchemy.orm import relationship

from app.database import Base, utcnow


class TranscriptNote(Base):
    __tablename__ = "transcript_notes"

    id = Column(Integer, primary_key=True)
    transcript_id = Column(
        Integer,
        ForeignKey("transcripts.id", ondelete="CASCADE"),
        nullable=False,
    )
    content = Column(Text, nullable=False)
    version = Column(Integer, nullable=False, default=1)
    created_at = Column(DateTime, default=utcnow)

    transcript = relationship("Transcript", back_populates="notes")

    __table_args__ = (
        Index("idx_transcript_notes_tid_version", "transcript_id", "version"),
    )
