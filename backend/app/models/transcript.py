from datetime import date, datetime

from sqlalchemy import Column, Integer, String, Text, Date, DateTime, Index, text
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
    source_file = Column(String, nullable=False)
    file_hash = Column(String, nullable=False)
    imported_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    summary = relationship("Summary", back_populates="transcript", uselist=False)
    mentions = relationship("TranscriptMention", back_populates="transcript")

    __table_args__ = (
        Index("idx_transcripts_date", "meeting_date"),
        Index("idx_transcripts_search", "search_vector", postgresql_using="gin"),
    )
