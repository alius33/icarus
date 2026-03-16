from sqlalchemy import Column, DateTime, Index, Integer, String, Text

from app.database import Base, utcnow


class Dependency(Base):
    __tablename__ = "dependencies"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    dependency_type = Column(String, nullable=False, default="integration")  # integration, external, internal
    status = Column(String, nullable=False, default="pending")  # pending, in-progress, blocked, completed
    blocking_reason = Column(Text)
    estimated_effort = Column(String)  # e.g. "2 weeks", "3 sprints"
    assigned_to = Column(String)
    affected_projects = Column(Text)  # comma-separated
    priority = Column(String, default="MEDIUM")  # CRITICAL, HIGH, MEDIUM, LOW
    notes = Column(Text)
    created_at = Column(DateTime, default=utcnow)
    updated_at = Column(DateTime, default=utcnow, onupdate=utcnow)

    __table_args__ = (
        Index("idx_dependencies_status", "status"),
        Index("idx_dependencies_priority", "priority"),
    )
