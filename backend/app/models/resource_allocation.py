from sqlalchemy import Column, DateTime, Index, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSON

from app.database import Base, utcnow


class ResourceAllocation(Base):
    __tablename__ = "resource_allocations"

    id = Column(Integer, primary_key=True)
    person_name = Column(String, nullable=False)
    role = Column(String)
    allocations = Column(JSON, default=list)  # [{project: str, percentage: int}]
    capacity_status = Column(String, default="available")  # available, stretched, overloaded
    notes = Column(Text)
    start_date = Column(String)
    end_date = Column(String)
    created_at = Column(DateTime, default=utcnow)
    updated_at = Column(DateTime, default=utcnow, onupdate=utcnow)

    __table_args__ = (
        Index("idx_resources_capacity", "capacity_status"),
    )
