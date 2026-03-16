from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Index, Integer, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class WeeklyPlanAction(Base):
    __tablename__ = "weekly_plan_actions"

    id = Column(Integer, primary_key=True, index=True)
    weekly_plan_id = Column(
        Integer,
        ForeignKey("weekly_plans.id", ondelete="CASCADE"),
        nullable=False,
    )
    category = Column(String, nullable=False)  # deliverable_strategic | deliverable_tactical | programme_strategic | programme_tactical
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    priority = Column(String, nullable=False, default="MEDIUM")  # HIGH | MEDIUM | LOW
    owner = Column(String, nullable=True)
    status = Column(String, nullable=False, default="PENDING")  # PENDING | IN_PROGRESS | DONE | SKIPPED
    deliverable_id = Column(
        Integer,
        ForeignKey("programme_deliverables.id", ondelete="SET NULL"),
        nullable=True,
    )
    position = Column(Integer, nullable=False, default=0)
    is_ai_generated = Column(Boolean, nullable=False, default=True)
    carried_from_week = Column(Integer, nullable=True)
    source_transcript_id = Column(
        Integer,
        ForeignKey("transcripts.id", ondelete="SET NULL"),
        nullable=True,
    )
    source_update_id = Column(
        Integer,
        ForeignKey("project_updates.id", ondelete="SET NULL"),
        nullable=True,
    )
    context = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    plan = relationship("WeeklyPlan", back_populates="actions")
    deliverable = relationship("ProgrammeDeliverable")
    source_transcript = relationship("Transcript")
    source_update = relationship("ProjectUpdate")

    __table_args__ = (
        Index("idx_weekly_plan_actions_plan", "weekly_plan_id"),
        Index("idx_weekly_plan_actions_deliverable", "deliverable_id"),
    )
