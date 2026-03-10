from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, UniqueConstraint

from app.database import Base


class DeletedImport(Base):
    __tablename__ = "deleted_imports"

    id = Column(Integer, primary_key=True)
    entity_type = Column(String, nullable=False)
    unique_key = Column(String, nullable=False)
    deleted_at = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        UniqueConstraint("entity_type", "unique_key", name="uq_deleted_imports_entity"),
    )
