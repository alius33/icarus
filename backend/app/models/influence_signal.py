from sqlalchemy import Boolean, Column, Date, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.sql import func

from app.database import Base


class InfluenceSignal(Base):
    __tablename__ = "influence_signals"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=True, index=True)
    person = Column(String, nullable=False, index=True)
    influence_type = Column(String, nullable=False)  # proposal_adopted | deferred_to | interrupted | final_say | bridging | blocked
    direction = Column(String, nullable=True)  # outbound | inbound
    target_person = Column(String, nullable=True)
    topic = Column(String, nullable=True)
    evidence = Column(Text, nullable=True)
    strength = Column(String, nullable=True)  # HIGH | MEDIUM | LOW
    confidence = Column(String, nullable=True)  # HIGH | MEDIUM | LOW
    coalition_name = Column(String, nullable=True)
    coalition_members = Column(String, nullable=True)  # comma-separated
    alignment = Column(String, nullable=True)
    transcript_id = Column(
        Integer,
        ForeignKey("transcripts.id", ondelete="SET NULL"),
        nullable=True,
    )
    is_manual = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
