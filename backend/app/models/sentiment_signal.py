from sqlalchemy import Boolean, Column, Date, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.sql import func

from app.database import Base


class SentimentSignal(Base):
    __tablename__ = "sentiment_signals"

    id = Column(Integer, primary_key=True, index=True)
    stakeholder_id = Column(
        Integer,
        ForeignKey("stakeholders.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    transcript_id = Column(
        Integer,
        ForeignKey("transcripts.id", ondelete="SET NULL"),
        nullable=True,
    )
    date = Column(Date, nullable=True, index=True)
    sentiment = Column(String, nullable=False)  # champion | supportive | neutral | cautious | frustrated | resistant | disengaged
    shift = Column(String, nullable=True)  # UP | DOWN | STABLE | NEW
    topic = Column(String, nullable=True)
    quote = Column(Text, nullable=True)
    notes = Column(Text, nullable=True)
    is_manual = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
