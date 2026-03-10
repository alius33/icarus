from sqlalchemy import Column, ForeignKey, Index, Integer, String, UniqueConstraint
from sqlalchemy.orm import relationship

from app.database import Base


class TranscriptMention(Base):
    __tablename__ = "transcript_mentions"

    id = Column(Integer, primary_key=True)
    transcript_id = Column(Integer, ForeignKey("transcripts.id", ondelete="CASCADE"), nullable=False)
    stakeholder_id = Column(Integer, ForeignKey("stakeholders.id", ondelete="CASCADE"), nullable=False)
    mention_type = Column(String, nullable=False)
    mention_count = Column(Integer, default=1)

    transcript = relationship("Transcript", back_populates="mentions")
    stakeholder = relationship("Stakeholder", back_populates="mentions")

    __table_args__ = (
        UniqueConstraint("transcript_id", "stakeholder_id", "mention_type"),
        Index("idx_mentions_stakeholder", "stakeholder_id"),
        Index("idx_mentions_transcript", "transcript_id"),
    )
