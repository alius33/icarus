from datetime import date, datetime

from sqlalchemy import Column, Integer, String, Text, Date, DateTime, ForeignKey, Index
from sqlalchemy.dialects.postgresql import TSVECTOR
from sqlalchemy.orm import relationship

from app.database import Base


class Workstream(Base):
    __tablename__ = "workstreams"

    id = Column(Integer, primary_key=True)
    code = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    lead = Column(String)
    status = Column(String, nullable=False)
    description = Column(Text)
    current_state = Column(Text)
    next_steps = Column(Text)
    risks = Column(Text)
    blocker_reason = Column(Text)
    assigned_fte = Column(String)
    search_vector = Column(TSVECTOR)
    source_file = Column(String, nullable=False, default="context/workstreams.md")
    file_hash = Column(String, nullable=False)
    imported_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    milestones = relationship("WorkstreamMilestone", back_populates="workstream", order_by="WorkstreamMilestone.milestone_date")

    __table_args__ = (
        Index("idx_workstreams_search", "search_vector", postgresql_using="gin"),
    )


class WorkstreamMilestone(Base):
    __tablename__ = "workstream_milestones"

    id = Column(Integer, primary_key=True)
    workstream_id = Column(Integer, ForeignKey("workstreams.id", ondelete="CASCADE"), nullable=False)
    milestone_date = Column(Date, nullable=True)
    description = Column(Text, nullable=False)
    source_file = Column(String, nullable=False)
    imported_at = Column(DateTime, default=datetime.utcnow)

    workstream = relationship("Workstream", back_populates="milestones")

    __table_args__ = (
        Index("idx_milestones_date", "milestone_date"),
    )
