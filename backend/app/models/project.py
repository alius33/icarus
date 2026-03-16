from sqlalchemy import Boolean, Column, Date, DateTime, Index, Integer, String, Text
from sqlalchemy.orm import relationship

from app.database import Base, utcnow


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    slug = Column(String, unique=True, index=True, nullable=True)
    code = Column(String, unique=True, index=True, nullable=False, default="")
    description = Column(Text)
    is_custom = Column(Boolean, nullable=False, default=False)
    status = Column(String, nullable=False, default="active")
    color = Column(String, nullable=True)
    icon = Column(String, nullable=True)
    keywords = Column(Text, nullable=True)
    division = Column(String, nullable=True)
    last_analysed_date = Column(Date, nullable=True)
    created_at = Column(DateTime, default=utcnow)
    updated_at = Column(DateTime, default=utcnow, onupdate=utcnow)

    links = relationship("ProjectLink", back_populates="project", cascade="all, delete-orphan")
