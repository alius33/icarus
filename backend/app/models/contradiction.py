from sqlalchemy import Boolean, Column, Date, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.sql import func

from app.database import Base


class Contradiction(Base):
    __tablename__ = "contradictions"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=True, index=True)
    contradiction_type = Column(String, nullable=False)  # reversal | contradiction | quiet_drop | scope_shift | reframing
    person = Column(String, nullable=True, index=True)
    statement_a = Column(Text, nullable=True)
    date_a = Column(Date, nullable=True)
    statement_b = Column(Text, nullable=True)
    date_b = Column(Date, nullable=True)
    severity = Column(String, nullable=True)  # CRITICAL | HIGH | MEDIUM | LOW
    resolution = Column(String, default="unresolved")  # unresolved | acknowledged | explained | superseded
    confidence = Column(String, nullable=True)  # HIGH | MEDIUM | LOW
    # For gap entries
    gap_description = Column(Text, nullable=True)
    expected_source = Column(String, nullable=True)
    last_mentioned = Column(Date, nullable=True)
    meetings_absent = Column(Integer, nullable=True)
    entry_kind = Column(String, nullable=False, default="contradiction")  # contradiction | gap
    transcript_id = Column(
        Integer,
        ForeignKey("transcripts.id", ondelete="SET NULL"),
        nullable=True,
    )
    is_manual = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
