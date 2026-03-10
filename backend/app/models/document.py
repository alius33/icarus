from datetime import datetime

from sqlalchemy import Column, Integer, String, Text, DateTime, Index
from sqlalchemy.dialects.postgresql import TSVECTOR

from app.database import Base


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True)
    filename = Column(String, unique=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    doc_type = Column(String, nullable=False)
    search_vector = Column(TSVECTOR)
    source_file = Column(String, nullable=False)
    file_hash = Column(String, nullable=False)
    imported_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        Index("idx_documents_search", "search_vector", postgresql_using="gin"),
    )
