from datetime import datetime

from sqlalchemy import Column, Date, DateTime, ForeignKey, Index, Integer, String, Text
from sqlalchemy.dialects.postgresql import ARRAY, TSVECTOR
from sqlalchemy.orm import relationship

from app.database import Base


class Transcript(Base):
    __tablename__ = "transcripts"

    id = Column(Integer, primary_key=True)
    filename = Column(String, unique=True, nullable=False)
    title = Column(String, nullable=False)
    meeting_date = Column(Date, nullable=False)
    content = Column(Text, nullable=False)
    word_count = Column(Integer)
    participants = Column(ARRAY(String), default=[])
    search_vector = Column(TSVECTOR)
    primary_project_id = Column(
        Integer,
        ForeignKey("projects.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    source_file = Column(String, nullable=False)
    file_hash = Column(String, nullable=False)
    imported_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    primary_project = relationship("Project", foreign_keys=[primary_project_id])
    summary = relationship("Summary", back_populates="transcript", uselist=False)
    mentions = relationship("TranscriptMention", back_populates="transcript")

    __table_args__ = (
        Index("idx_transcripts_date", "meeting_date"),
        Index("idx_transcripts_search", "search_vector", postgresql_using="gin"),
    )
