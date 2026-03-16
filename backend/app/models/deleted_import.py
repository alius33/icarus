from sqlalchemy import Column, DateTime, Integer, String, UniqueConstraint

from app.database import Base, utcnow


class DeletedImport(Base):
    __tablename__ = "deleted_imports"

    id = Column(Integer, primary_key=True)
    entity_type = Column(String, nullable=False)
    unique_key = Column(String, nullable=False)
    deleted_at = Column(DateTime, default=utcnow)

    __table_args__ = (
        UniqueConstraint("entity_type", "unique_key", name="uq_deleted_imports_entity"),
    )
