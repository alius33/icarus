from sqlalchemy import Column, DateTime, Index, Integer, String, Text
from sqlalchemy.dialects.postgresql import TSVECTOR

from app.database import Base, utcnow


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
    imported_at = Column(DateTime, default=utcnow)
    updated_at = Column(DateTime, default=utcnow, onupdate=utcnow)

    __table_args__ = (
        Index("idx_documents_search", "search_vector", postgresql_using="gin"),
    )
