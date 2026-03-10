from datetime import datetime

from sqlalchemy import Boolean, Column, Date, DateTime, Index, Integer, String, Text
from sqlalchemy.dialects.postgresql import TSVECTOR

from app.database import Base


class ActionItem(Base):
    __tablename__ = "action_items"

    id = Column(Integer, primary_key=True)
    number = Column(String, nullable=False)
    action_date = Column(Date, nullable=True)
    description = Column(Text, nullable=False)
    owner = Column(String)
    deadline = Column(String)
    context = Column(Text)
    status = Column(String, nullable=False, default="OPEN")
    completed_date = Column(Date, nullable=True)
    is_manual = Column(Boolean, nullable=False, default=False)
    search_vector = Column(TSVECTOR)
    source_file = Column(String, nullable=False, default="analysis/trackers/action_items.md")
    file_hash = Column(String, nullable=False, default="")
    imported_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        Index("idx_actions_status", "status"),
        Index("idx_actions_owner", "owner"),
        Index("idx_actions_search", "search_vector", postgresql_using="gin"),
    )
