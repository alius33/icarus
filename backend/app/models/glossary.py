from datetime import datetime

from sqlalchemy import Column, Integer, String, Text, DateTime, Index, Boolean
from sqlalchemy.dialects.postgresql import TSVECTOR

from app.database import Base


class GlossaryEntry(Base):
    __tablename__ = "glossary_entries"

    id = Column(Integer, primary_key=True)
    term = Column(String, unique=True, nullable=False)
    category = Column(String)
    definition = Column(Text, nullable=False)
    is_manual = Column(Boolean, nullable=False, default=False)
    search_vector = Column(TSVECTOR)
    source_file = Column(String, nullable=False, default="context/glossary.md")
    file_hash = Column(String, nullable=False, default="")
    imported_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        Index("idx_glossary_search", "search_vector", postgresql_using="gin"),
    )
