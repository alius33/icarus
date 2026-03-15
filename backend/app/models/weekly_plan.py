from sqlalchemy import Column, Date, DateTime, Index, Integer, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class WeeklyPlan(Base):
    __tablename__ = "weekly_plans"

    id = Column(Integer, primary_key=True, index=True)
    week_number = Column(Integer, nullable=False, unique=True)
    week_start_date = Column(Date, nullable=False)  # Monday
    week_end_date = Column(Date, nullable=False)  # Friday
    deliverable_progress_summary = Column(Text, nullable=True)
    programme_actions_summary = Column(Text, nullable=True)
    status = Column(String, nullable=False, default="DRAFT")  # DRAFT | FINAL
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    actions = relationship(
        "WeeklyPlanAction",
        back_populates="plan",
        cascade="all, delete-orphan",
        order_by="WeeklyPlanAction.position",
    )
    snapshots = relationship(
        "DeliverableProgressSnapshot",
        back_populates="plan",
        cascade="all, delete-orphan",
    )

    __table_args__ = (
        Index("idx_weekly_plans_week_number", "week_number"),
    )
