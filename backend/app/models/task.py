from sqlalchemy import Boolean, Column, Date, DateTime, ForeignKey, Index, Integer, String, Text
from sqlalchemy.dialects.postgresql import ARRAY, TSVECTOR
from sqlalchemy.orm import relationship

from app.database import Base, utcnow

TASK_STATUSES = ["TODO", "IN_PROGRESS", "IN_REVIEW", "DONE", "CANCELLED"]
TASK_PRIORITIES = ["URGENT", "HIGH", "MEDIUM", "LOW", "NONE"]


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)
    identifier = Column(String, unique=True, nullable=False)
    number = Column(String, nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text)
    status = Column(String, nullable=False, default="TODO")
    priority = Column(String, nullable=False, default="NONE")
    assignee = Column(String)
    labels = Column(ARRAY(String), default=list)
    due_date = Column(Date, nullable=True)
    start_date = Column(Date, nullable=True)
    estimate = Column(Integer, nullable=True)
    position = Column(Integer, nullable=False, default=0)
    project_id = Column(Integer, ForeignKey("projects.id", ondelete="SET NULL"), nullable=True)
    parent_id = Column(Integer, ForeignKey("tasks.id", ondelete="SET NULL"), nullable=True)
    created_date = Column(Date, nullable=True)
    completed_date = Column(Date, nullable=True)

    # Backward-compat fields from ActionItem
    owner = Column(String)
    context = Column(Text)
    deadline = Column(String)
    action_date = Column(Date, nullable=True)

    is_manual = Column(Boolean, nullable=False, default=False)
    search_vector = Column(TSVECTOR)
    source_file = Column(String, nullable=False, default="manual")
    file_hash = Column(String, nullable=False, default="")
    imported_at = Column(DateTime, default=utcnow)
    updated_at = Column(DateTime, default=utcnow, onupdate=utcnow)

    project = relationship("Project", foreign_keys=[project_id])
    parent = relationship("Task", remote_side=[id], foreign_keys=[parent_id], back_populates="children")
    children = relationship("Task", foreign_keys=[parent_id], back_populates="parent")

    __table_args__ = (
        Index("idx_tasks_status", "status"),
        Index("idx_tasks_assignee", "assignee"),
        Index("idx_tasks_priority", "priority"),
        Index("idx_tasks_project", "project_id"),
        Index("idx_tasks_parent", "parent_id"),
        Index("idx_tasks_identifier", "identifier", unique=True),
        Index("idx_tasks_search", "search_vector", postgresql_using="gin"),
    )
