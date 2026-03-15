from sqlalchemy import Column, DateTime, ForeignKey, Index, Integer, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class DeliverableMilestone(Base):
    __tablename__ = "deliverable_milestones"

    id = Column(Integer, primary_key=True, index=True)
    deliverable_id = Column(
        Integer,
        ForeignKey("programme_deliverables.id", ondelete="CASCADE"),
        nullable=False,
    )
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    status = Column(String, nullable=False, default="NOT_STARTED")  # NOT_STARTED | IN_PROGRESS | COMPLETED | BLOCKED
    target_week = Column(Integer, nullable=True)  # 1-12+
    completed_week = Column(Integer, nullable=True)
    evidence = Column(Text, nullable=True)
    position = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    deliverable = relationship("ProgrammeDeliverable", back_populates="milestones")

    __table_args__ = (
        Index("idx_deliverable_milestones_deliverable", "deliverable_id"),
    )
