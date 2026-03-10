from datetime import datetime

from sqlalchemy import Column, Integer, String, Text, Boolean, Date, DateTime, ForeignKey, Index
from sqlalchemy.orm import relationship

from app.database import Base


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    workstream_id = Column(Integer, ForeignKey("workstreams.id", ondelete="SET NULL"), nullable=True, unique=True)
    is_custom = Column(Boolean, nullable=False, default=False)
    status = Column(String, nullable=False, default="active")
    color = Column(String, nullable=True)
    icon = Column(String, nullable=True)
    keywords = Column(Text, nullable=True)
    division = Column(String, nullable=True)
    last_analysed_date = Column(Date, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    links = relationship("ProjectLink", back_populates="project", cascade="all, delete-orphan")
    workstream = relationship("Workstream")

    __table_args__ = (
        Index("idx_projects_workstream", "workstream_id"),
    )
