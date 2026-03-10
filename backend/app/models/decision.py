from datetime import datetime

from sqlalchemy import Boolean, Column, Date, DateTime, ForeignKey, Index, Integer, String, Text
from sqlalchemy.dialects.postgresql import ARRAY, TSVECTOR

from app.database import Base


class Decision(Base):
    __tablename__ = "decisions"

    id = Column(Integer, primary_key=True)
    number = Column(Integer, unique=True, nullable=False)
    decision_date = Column(Date, nullable=False)
    decision = Column(Text, nullable=False)
    rationale = Column(Text)
    key_people = Column(ARRAY(String), default=[])
    workstream_id = Column(Integer, ForeignKey("workstreams.id"), nullable=True)
    search_vector = Column(TSVECTOR)
    execution_status = Column(String, default="made")  # made | in_progress | implemented | reversed | superseded
    position = Column(Integer, nullable=False, default=0)
    is_manual = Column(Boolean, nullable=False, default=False)
    source_file = Column(String, nullable=False, default="context/decisions.md")
    file_hash = Column(String, nullable=False, default="")
    imported_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        Index("idx_decisions_date", "decision_date"),
        Index("idx_decisions_position", "position"),
        Index("idx_decisions_search", "search_vector", postgresql_using="gin"),
    )
