from sqlalchemy import Column, DateTime, ForeignKey, Index, Integer, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class ProgrammeDeliverable(Base):
    __tablename__ = "programme_deliverables"

    id = Column(Integer, primary_key=True, index=True)
    pillar = Column(Integer, nullable=False)  # 1, 2, or 3
    pillar_name = Column(String, nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    position = Column(Integer, nullable=False, default=0)
    project_id = Column(
        Integer,
        ForeignKey("projects.id", ondelete="SET NULL"),
        nullable=True,
    )
    rag_status = Column(String, nullable=False, default="GREEN")  # GREEN | AMBER | RED
    progress_percent = Column(Integer, nullable=False, default=0)  # 0-100, auto-calculated from milestones
    notes = Column(Text, nullable=True)  # AI-generated current-state summary
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    milestones = relationship(
        "DeliverableMilestone",
        back_populates="deliverable",
        cascade="all, delete-orphan",
        order_by="DeliverableMilestone.position",
    )
    project = relationship("Project")

    __table_args__ = (
        Index("idx_programme_deliverables_pillar", "pillar"),
    )
