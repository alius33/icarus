from datetime import datetime

from sqlalchemy import Column, Integer, String, Text, DateTime, Index, Boolean
from sqlalchemy.dialects.postgresql import TSVECTOR
from sqlalchemy.orm import relationship

from app.database import Base


class Stakeholder(Base):
    __tablename__ = "stakeholders"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    tier = Column(Integer, nullable=False)
    role = Column(String)
    engagement_level = Column(String)
    communication_style = Column(Text)
    concerns = Column(Text)
    key_contributions = Column(Text)
    notes = Column(Text)
    risk_level = Column(String)  # none, low, medium, high, critical
    morale_notes = Column(Text)
    is_manual = Column(Boolean, nullable=False, default=False)
    search_vector = Column(TSVECTOR)
    source_file = Column(String, nullable=False, default="context/stakeholders.md")
    file_hash = Column(String, nullable=False, default="")
    imported_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    mentions = relationship("TranscriptMention", back_populates="stakeholder")

    __table_args__ = (
        Index("idx_stakeholders_tier", "tier"),
        Index("idx_stakeholders_search", "search_vector", postgresql_using="gin"),
    )
