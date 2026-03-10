from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Index, UniqueConstraint
from sqlalchemy.orm import relationship

from app.database import Base


class ProjectLink(Base):
    __tablename__ = "project_links"

    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    entity_type = Column(String, nullable=False)
    entity_id = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    project = relationship("Project", back_populates="links")

    __table_args__ = (
        UniqueConstraint("project_id", "entity_type", "entity_id", name="uq_project_entity"),
        Index("idx_project_links_project", "project_id"),
        Index("idx_project_links_entity", "entity_type", "entity_id"),
    )
