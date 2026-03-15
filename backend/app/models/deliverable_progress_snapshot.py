from sqlalchemy import Column, DateTime, ForeignKey, Index, Integer, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class DeliverableProgressSnapshot(Base):
    __tablename__ = "deliverable_progress_snapshots"

    id = Column(Integer, primary_key=True, index=True)
    deliverable_id = Column(
        Integer,
        ForeignKey("programme_deliverables.id", ondelete="CASCADE"),
        nullable=False,
    )
    weekly_plan_id = Column(
        Integer,
        ForeignKey("weekly_plans.id", ondelete="CASCADE"),
        nullable=False,
    )
    week_number = Column(Integer, nullable=False)
    rag_status = Column(String, nullable=False, default="GREEN")
    progress_percent = Column(Integer, nullable=False, default=0)
    milestones_completed = Column(Integer, nullable=False, default=0)
    milestones_total = Column(Integer, nullable=False, default=0)
    narrative = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    deliverable = relationship("ProgrammeDeliverable")
    plan = relationship("WeeklyPlan", back_populates="snapshots")

    __table_args__ = (
        Index("idx_progress_snapshots_deliverable", "deliverable_id"),
        Index("idx_progress_snapshots_plan", "weekly_plan_id"),
    )
