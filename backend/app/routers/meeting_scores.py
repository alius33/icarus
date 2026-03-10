from datetime import date

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.exceptions import NotFoundError
from app.models.meeting_score import MeetingScore
from app.schemas.meeting_score import (
    MeetingScoreBase,
    MeetingScoreCreate,
    MeetingScoreTrend,
    MeetingScoreUpdate,
)

router = APIRouter(tags=["meeting-scores"])


def _schema(s: MeetingScore) -> MeetingScoreBase:
    return MeetingScoreBase(
        id=s.id,
        transcript_id=s.transcript_id,
        date=str(s.date) if s.date else None,
        meeting_title=s.meeting_title,
        meeting_type=s.meeting_type,
        overall_score=s.overall_score,
        decision_velocity=s.decision_velocity,
        action_clarity=s.action_clarity,
        engagement_balance=s.engagement_balance,
        topic_completion=s.topic_completion,
        follow_through=s.follow_through,
        participant_count=s.participant_count,
        duration_category=s.duration_category,
        recommendations=s.recommendations,
        is_manual=s.is_manual,
    )


@router.get("/meeting-scores", response_model=list[MeetingScoreBase])
async def list_meeting_scores(
    meeting_type: str | None = Query(None),
    db: AsyncSession = Depends(get_db),
):
    query = select(MeetingScore)
    if meeting_type is not None:
        query = query.where(MeetingScore.meeting_type == meeting_type)
    query = query.order_by(MeetingScore.date.desc().nullslast(), MeetingScore.id.desc())
    result = await db.execute(query)
    return [_schema(s) for s in result.scalars().all()]


@router.get("/meeting-scores/trend", response_model=list[MeetingScoreTrend])
async def meeting_score_trend(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(MeetingScore)
        .where(MeetingScore.date.isnot(None))
        .order_by(MeetingScore.date.asc(), MeetingScore.id.asc())
    )
    return [
        MeetingScoreTrend(
            date=str(s.date),
            score=s.overall_score,
            meeting_type=s.meeting_type,
        )
        for s in result.scalars().all()
    ]


@router.get("/meeting-scores/recommendations")
async def meeting_recommendations(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(MeetingScore.recommendations)
        .where(MeetingScore.recommendations.isnot(None))
        .where(MeetingScore.recommendations != "")
    )
    raw = result.scalars().all()
    unique: list[str] = []
    seen: set[str] = set()
    for rec in raw:
        if rec and rec.strip() not in seen:
            seen.add(rec.strip())
            unique.append(rec.strip())
    return unique


@router.get("/meeting-scores/{score_id}", response_model=MeetingScoreBase)
async def get_meeting_score(score_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(MeetingScore).where(MeetingScore.id == score_id)
    )
    score = result.scalar_one_or_none()
    if not score:
        raise NotFoundError("Meeting score", score_id)
    return _schema(score)


@router.post("/meeting-scores", response_model=MeetingScoreBase, status_code=201)
async def create_meeting_score(body: MeetingScoreCreate, db: AsyncSession = Depends(get_db)):
    record = MeetingScore(
        transcript_id=body.transcript_id,
        date=date.fromisoformat(body.date) if body.date else None,
        meeting_title=body.meeting_title,
        meeting_type=body.meeting_type,
        overall_score=body.overall_score,
        decision_velocity=body.decision_velocity,
        action_clarity=body.action_clarity,
        engagement_balance=body.engagement_balance,
        topic_completion=body.topic_completion,
        follow_through=body.follow_through,
        participant_count=body.participant_count,
        duration_category=body.duration_category,
        recommendations=body.recommendations,
        is_manual=True,
    )
    db.add(record)
    await db.commit()
    await db.refresh(record)
    return _schema(record)


@router.patch("/meeting-scores/{score_id}", response_model=MeetingScoreBase)
async def update_meeting_score(
    score_id: int,
    body: MeetingScoreUpdate,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(MeetingScore).where(MeetingScore.id == score_id)
    )
    record = result.scalar_one_or_none()
    if not record:
        raise NotFoundError("Meeting score", score_id)

    if body.transcript_id is not None:
        record.transcript_id = body.transcript_id
    if body.date is not None:
        record.date = date.fromisoformat(body.date)
    if body.meeting_title is not None:
        record.meeting_title = body.meeting_title
    if body.meeting_type is not None:
        record.meeting_type = body.meeting_type
    if body.overall_score is not None:
        record.overall_score = body.overall_score
    if body.decision_velocity is not None:
        record.decision_velocity = body.decision_velocity
    if body.action_clarity is not None:
        record.action_clarity = body.action_clarity
    if body.engagement_balance is not None:
        record.engagement_balance = body.engagement_balance
    if body.topic_completion is not None:
        record.topic_completion = body.topic_completion
    if body.follow_through is not None:
        record.follow_through = body.follow_through
    if body.participant_count is not None:
        record.participant_count = body.participant_count
    if body.duration_category is not None:
        record.duration_category = body.duration_category
    if body.recommendations is not None:
        record.recommendations = body.recommendations

    await db.commit()
    await db.refresh(record)
    return _schema(record)


@router.delete("/meeting-scores/{score_id}")
async def delete_meeting_score(score_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(MeetingScore).where(MeetingScore.id == score_id)
    )
    record = result.scalar_one_or_none()
    if not record:
        raise NotFoundError("Meeting score", score_id)
    await db.delete(record)
    await db.commit()
    return {"ok": True}
