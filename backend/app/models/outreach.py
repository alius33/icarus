from datetime import datetime

from sqlalchemy import Column, Integer, String, Text, Date, DateTime, Index

from app.database import Base


class Outreach(Base):
    __tablename__ = "outreach"

    id = Column(Integer, primary_key=True)
    contact_name = Column(String, nullable=False)
    contact_role = Column(String)
    division = Column(String)  # Banking | Asset Management | Life | etc.
    status = Column(String, nullable=False, default="initial_contact")  # initial_contact | interested | engaged | committed | cold
    interest_level = Column(Integer, default=1)  # 1-5
    first_contact_date = Column(Date)
    last_contact_date = Column(Date)
    meeting_count = Column(Integer, default=0)
    notes = Column(Text)
    next_step = Column(String)
    next_step_date = Column(Date)
    external_id = Column(String)
    external_source = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        Index("idx_outreach_status", "status"),
        Index("idx_outreach_division", "division"),
    )
