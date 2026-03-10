from datetime import datetime

from sqlalchemy import Column, Integer, DateTime, ForeignKey, UniqueConstraint, Index

from app.database import Base


class OutreachLink(Base):
    __tablename__ = "outreach_links"

    id = Column(Integer, primary_key=True)
    outreach_id = Column(Integer, ForeignKey("outreach.id", ondelete="CASCADE"), nullable=False)
    transcript_id = Column(Integer, ForeignKey("transcripts.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        UniqueConstraint("outreach_id", "transcript_id", name="uq_outreach_transcript"),
        Index("idx_outreach_links_outreach", "outreach_id"),
        Index("idx_outreach_links_transcript", "transcript_id"),
    )
