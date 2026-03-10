from datetime import datetime

from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, Index

from app.database import Base


class ScopeItem(Base):
    __tablename__ = "scope_items"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    scope_type = Column(String, nullable=False, default="addition")  # original, addition
    workstream = Column(String)
    added_date = Column(String)
    estimated_effort = Column(String)
    budgeted = Column(Boolean, default=False)
    status = Column(String, default="planned")  # planned, in-progress, completed, cancelled
    description = Column(Text)
    impact_notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        Index("idx_scope_type", "scope_type"),
        Index("idx_scope_status", "status"),
    )
