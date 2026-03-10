from sqlalchemy import Boolean, Column, Date, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.sql import func

from app.database import Base


class Commitment(Base):
    __tablename__ = "commitments"

    id = Column(Integer, primary_key=True, index=True)
    person = Column(String, nullable=False)
    commitment = Column(Text, nullable=False)
    transcript_id = Column(
        Integer,
        ForeignKey("transcripts.id", ondelete="SET NULL"),
        nullable=True,
    )
    date_made = Column(Date, nullable=True)
    deadline_text = Column(String, nullable=True)  # Raw: "by Friday", "next week"
    deadline_resolved = Column(Date, nullable=True)
    deadline_type = Column(String, nullable=True)  # date_resolved | event_relative | conditional | none
    condition = Column(String, nullable=True)
    linked_action_id = Column(
        Integer,
        ForeignKey("tasks.id", ondelete="SET NULL"),
        nullable=True,
    )
    status = Column(String, nullable=False, default="pending")  # pending | fulfilled | broken | formalised | conditional
    verified_date = Column(Date, nullable=True)
    notes = Column(Text, nullable=True)
    is_manual = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
