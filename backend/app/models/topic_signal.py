from sqlalchemy import Boolean, Column, Date, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.sql import func

from app.database import Base


class TopicSignal(Base):
    __tablename__ = "topic_signals"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=True, index=True)
    topic = Column(String, nullable=False, index=True)
    category = Column(String, nullable=True)  # technical | strategic | interpersonal | operational | governance
    intensity = Column(String, nullable=True)  # CRITICAL | HIGH | MEDIUM | LOW
    first_raised = Column(Date, nullable=True)
    meetings_count = Column(Integer, default=1)
    trend = Column(String, nullable=True)  # rising | stable | declining | new
    key_quote = Column(Text, nullable=True)
    confidence = Column(String, nullable=True)  # HIGH | MEDIUM | LOW
    transcript_id = Column(
        Integer,
        ForeignKey("transcripts.id", ondelete="SET NULL"),
        nullable=True,
    )
    is_manual = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
