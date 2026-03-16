import datetime

from fastapi import APIRouter, Depends, Query
from sqlalchemy import Date, String, cast, literal, select, union_all
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.decision import Decision
from app.models.transcript import Transcript
from app.schemas.timeline import TimelineEvent, TimelineResponse

router = APIRouter(tags=["timeline"])


@router.get("/timeline", response_model=TimelineResponse)
async def get_timeline(
    from_date: datetime.date | None = Query(None),
    to_date: datetime.date | None = Query(None),
    db: AsyncSession = Depends(get_db),
):
    # Build individual queries for each event type
    transcript_q = select(
        cast(Transcript.meeting_date, Date).label("date"),
        literal("transcript").label("type"),
        Transcript.title.label("title"),
        literal(None).label("description"),
        Transcript.id.label("reference_id"),
    )
    if from_date:
        transcript_q = transcript_q.where(Transcript.meeting_date >= from_date)
    if to_date:
        transcript_q = transcript_q.where(Transcript.meeting_date <= to_date)

    decision_q = select(
        cast(Decision.decision_date, Date).label("date"),
        literal("decision").label("type"),
        (literal("Decision #") + cast(Decision.number, String)).label("title"),
        Decision.decision.label("description"),
        Decision.id.label("reference_id"),
    )
    if from_date:
        decision_q = decision_q.where(Decision.decision_date >= from_date)
    if to_date:
        decision_q = decision_q.where(Decision.decision_date <= to_date)

    combined = union_all(transcript_q, decision_q).subquery()
    final_query = select(combined).order_by(combined.c.date.desc())

    result = await db.execute(final_query)
    rows = result.all()

    events = [
        TimelineEvent(
            date=str(row.date) if row.date else "",
            type=row.type,
            title=row.title or "",
            description=row.description,
            reference_id=row.reference_id,
            reference_url=None,
        )
        for row in rows
    ]

    actual_from = str(from_date) if from_date else (str(events[-1].date) if events else "")
    actual_to = str(to_date) if to_date else (str(events[0].date) if events else "")

    return TimelineResponse(
        from_date=actual_from,
        to_date=actual_to,
        events=events,
        total=len(events),
    )
