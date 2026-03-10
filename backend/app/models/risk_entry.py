from sqlalchemy import Boolean, Column, Date, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.sql import func

from app.database import Base


class RiskEntry(Base):
    __tablename__ = "risk_entries"

    id = Column(Integer, primary_key=True, index=True)
    risk_id = Column(String, nullable=False, unique=True, index=True)  # R-001
    date = Column(Date, nullable=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    category = Column(String, nullable=True)  # technical | operational | strategic | resource | stakeholder | scope
    severity = Column(String, nullable=False)  # CRITICAL | HIGH | MEDIUM | LOW
    trajectory = Column(String, nullable=True)  # escalating | stable | de-escalating | new | resolved
    source_type = Column(String, nullable=True)  # explicit | implicit | absence_inferred
    owner = Column(String, nullable=True)
    mitigation = Column(Text, nullable=True)
    last_reviewed = Column(Date, nullable=True)
    meetings_mentioned = Column(Integer, default=1)
    confidence = Column(String, nullable=True)  # HIGH | MEDIUM | LOW
    transcript_id = Column(
        Integer,
        ForeignKey("transcripts.id", ondelete="SET NULL"),
        nullable=True,
    )
    is_manual = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
