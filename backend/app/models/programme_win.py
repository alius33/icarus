from datetime import datetime

from sqlalchemy import Boolean, Column, Date, DateTime, Index, Integer, String, Text

from app.database import Base


class ProgrammeWin(Base):
    __tablename__ = "programme_wins"

    id = Column(Integer, primary_key=True)
    category = Column(String, nullable=False)  # time_saved | adoption | quality | reach | process_improvement
    title = Column(String, nullable=False)
    description = Column(Text)
    before_state = Column(String)
    after_state = Column(String)
    project = Column(String)
    confidence = Column(String, nullable=False, default="estimated")  # measured | estimated | anecdotal
    date_recorded = Column(Date)
    notes = Column(Text)
    is_manual = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        Index("idx_wins_category", "category"),
        Index("idx_wins_confidence", "confidence"),
    )
