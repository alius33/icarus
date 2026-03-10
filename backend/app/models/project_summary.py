from sqlalchemy import Column, Date, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.sql import func

from app.database import Base


class ProjectSummary(Base):
    __tablename__ = "project_summaries"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(
        Integer,
        ForeignKey("projects.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    transcript_id = Column(
        Integer,
        ForeignKey("transcripts.id", ondelete="CASCADE"),
        nullable=False,
    )
    date = Column(Date, nullable=True, index=True)
    relevance = Column(String, nullable=True)  # HIGH | MEDIUM | LOW
    content = Column(Text, nullable=False)
    source_file = Column(String, nullable=True)
    file_hash = Column(String(64), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
