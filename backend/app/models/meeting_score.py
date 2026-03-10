from sqlalchemy import Boolean, Column, Date, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.sql import func

from app.database import Base


class MeetingScore(Base):
    __tablename__ = "meeting_scores"

    id = Column(Integer, primary_key=True, index=True)
    transcript_id = Column(
        Integer,
        ForeignKey("transcripts.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
    )
    date = Column(Date, nullable=True, index=True)
    meeting_title = Column(String, nullable=True)
    meeting_type = Column(String, nullable=True)  # decision_making | status_update | brainstorming | escalation | planning | review | onboarding
    overall_score = Column(Integer, nullable=False)  # 0-100
    decision_velocity = Column(Float, nullable=True)  # 0.0-1.0
    action_clarity = Column(Float, nullable=True)  # 0.0-1.0
    engagement_balance = Column(Float, nullable=True)  # 0.0-1.0
    topic_completion = Column(Float, nullable=True)  # 0.0-1.0
    follow_through = Column(Float, nullable=True)  # 0.0-1.0
    participant_count = Column(Integer, nullable=True)
    duration_category = Column(String, nullable=True)  # short | medium | long
    recommendations = Column(Text, nullable=True)
    is_manual = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
