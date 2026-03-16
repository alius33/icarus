from sqlalchemy import Boolean, Column, DateTime, Index, Integer, String, Text
from sqlalchemy.dialects.postgresql import TSVECTOR

from app.database import Base, utcnow


class OpenThread(Base):
    __tablename__ = "open_threads"

    id = Column(Integer, primary_key=True)
    number = Column(Integer, nullable=False)
    title = Column(String, nullable=False)
    status = Column(String, nullable=False)
    first_raised = Column(String)
    context = Column(Text)
    question = Column(Text)
    why_it_matters = Column(Text)
    resolution = Column(Text)
    severity = Column(String)  # CRITICAL, HIGH, MEDIUM, LOW
    trend = Column(String)  # escalating, stable, de-escalating
    position = Column(Integer, nullable=False, default=0)
    is_manual = Column(Boolean, nullable=False, default=False)
    search_vector = Column(TSVECTOR)
    source_file = Column(String, nullable=False, default="context/open_threads.md")
    file_hash = Column(String, nullable=False, default="")
    imported_at = Column(DateTime, default=utcnow)
    updated_at = Column(DateTime, default=utcnow, onupdate=utcnow)

    __table_args__ = (
        Index("idx_threads_status", "status"),
        Index("idx_threads_position", "position"),
        Index("idx_threads_search", "search_vector", postgresql_using="gin"),
    )
