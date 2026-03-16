from sqlalchemy import Boolean, Column, DateTime, Index, Integer, String, Text

from app.database import Base, utcnow


class ProjectUpdate(Base):
    __tablename__ = "project_updates"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    raw_content = Column(Text, nullable=True)
    content_type = Column(String, nullable=False, default="note")  # "note" | "teams_chat"
    summary = Column(Text, nullable=True)
    is_processed = Column(Boolean, nullable=False, default=False)
    processed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=utcnow)
    updated_at = Column(DateTime, default=utcnow, onupdate=utcnow)

    __table_args__ = (
        Index("idx_project_updates_created", "created_at"),
        Index("idx_project_updates_processed", "is_processed"),
    )
