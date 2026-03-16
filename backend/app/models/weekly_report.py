from sqlalchemy import Column, Date, DateTime, Index, Integer, String, Text
from sqlalchemy.dialects.postgresql import TSVECTOR

from app.database import Base, utcnow


class WeeklyReport(Base):
    __tablename__ = "weekly_reports"

    id = Column(Integer, primary_key=True)
    filename = Column(String, unique=True, nullable=False)
    title = Column(String, nullable=False)
    week_start = Column(Date, nullable=True)
    week_end = Column(Date, nullable=True)
    content = Column(Text, nullable=False)
    search_vector = Column(TSVECTOR)
    source_file = Column(String, nullable=False)
    file_hash = Column(String, nullable=False)
    imported_at = Column(DateTime, default=utcnow)
    updated_at = Column(DateTime, default=utcnow, onupdate=utcnow)

    __table_args__ = (
        Index("idx_weekly_reports_search", "search_vector", postgresql_using="gin"),
    )
