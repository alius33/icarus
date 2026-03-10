from datetime import datetime

from sqlalchemy import Column, Integer, String, Text, Date, DateTime, Index

from app.database import Base


class AdoptionMetric(Base):
    __tablename__ = "adoption_metrics"

    id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False, index=True)
    metric_type = Column(String, nullable=False)  # active_users | data_entries | reviews_completed | queries_run
    value = Column(Integer, nullable=False)
    workstream = Column(String)
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        Index("idx_adoption_date", "date"),
        Index("idx_adoption_metric_type", "metric_type"),
    )
