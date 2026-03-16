from sqlalchemy import Column, DateTime, Index, Integer, String, Text

from app.database import Base, utcnow


class DivisionProfile(Base):
    __tablename__ = "division_profiles"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    status = Column(String, nullable=False, default="not_engaged")  # not_engaged | early_talks | collaborating | active_partnership
    current_tools = Column(Text)
    pain_points = Column(Text)
    key_contact = Column(String)
    notes = Column(Text)
    created_at = Column(DateTime, default=utcnow)
    updated_at = Column(DateTime, default=utcnow, onupdate=utcnow)

    __table_args__ = (
        Index("idx_division_status", "status"),
    )
