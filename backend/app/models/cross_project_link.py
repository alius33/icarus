from sqlalchemy import Boolean, Column, Date, DateTime, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.sql import func

from app.database import Base


class CrossProjectLink(Base):
    __tablename__ = "cross_project_links"

    id = Column(Integer, primary_key=True, index=True)
    source_project_id = Column(
        Integer,
        ForeignKey("projects.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    target_project_id = Column(
        Integer,
        ForeignKey("projects.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    link_type = Column(String, nullable=False)  # dependency | conflict | synergy | resource_shared | blocked_by | supersedes
    description = Column(Text, nullable=True)
    transcript_id = Column(
        Integer,
        ForeignKey("transcripts.id", ondelete="SET NULL"),
        nullable=True,
    )
    date_detected = Column(Date, nullable=True)
    severity = Column(String, nullable=False, default="info")  # info | warning | critical
    status = Column(String, nullable=False, default="active")  # active | resolved | monitoring
    is_manual = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        UniqueConstraint(
            "source_project_id",
            "target_project_id",
            "link_type",
            name="uq_cross_project_link",
        ),
    )
