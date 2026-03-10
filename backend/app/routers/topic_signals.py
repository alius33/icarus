from datetime import date, timedelta

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select, func as sa_func
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.exceptions import NotFoundError
from app.models.topic_signal import TopicSignal
from app.schemas.topic_signal import (
    TopicSignalBase,
    TopicSignalCreate,
    TopicSignalUpdate,
)

router = APIRouter(tags=["topic-signals"])


def _schema(s: TopicSignal) -> TopicSignalBase:
    return TopicSignalBase(
        id=s.id,
        date=str(s.date) if s.date else None,
        topic=s.topic,
        category=s.category,
        intensity=s.intensity,
        first_raised=str(s.first_raised) if s.first_raised else None,
        meetings_count=s.meetings_count or 1,
        trend=s.trend,
        key_quote=s.key_quote,
        confidence=s.confidence,
        transcript_id=s.transcript_id,
        is_manual=s.is_manual,
    )


@router.get("/topic-signals", response_model=list[TopicSignalBase])
async def list_topic_signals(
    category: str | None = Query(None),
    transcript_id: int | None = Query(None),
    db: AsyncSession = Depends(get_db),
):
    query = select(TopicSignal)
    if category is not None:
        query = query.where(TopicSignal.category == category)
    if transcript_id is not None:
        query = query.where(TopicSignal.transcript_id == transcript_id)
    query = query.order_by(TopicSignal.date.desc().nullslast(), TopicSignal.id.desc())
    result = await db.execute(query)
    return [_schema(s) for s in result.scalars().all()]


@router.get("/topic-signals/evolution")
async def topic_evolution(db: AsyncSession = Depends(get_db)):
    query = (
        select(
            TopicSignal.topic,
            TopicSignal.category,
            TopicSignal.date,
            TopicSignal.intensity,
            sa_func.sum(TopicSignal.meetings_count).label("meetings_count"),
        )
        .group_by(TopicSignal.topic, TopicSignal.category, TopicSignal.date, TopicSignal.intensity)
        .order_by(TopicSignal.date.desc().nullslast())
    )
    result = await db.execute(query)
    rows = result.all()

    topics: dict[str, dict] = {}
    for row in rows:
        key = row.topic
        if key not in topics:
            topics[key] = {
                "topic": row.topic,
                "category": row.category,
                "data_points": [],
            }
        topics[key]["data_points"].append({
            "date": str(row.date) if row.date else None,
            "intensity": row.intensity,
            "meetings_count": row.meetings_count or 0,
        })

    return list(topics.values())


@router.get("/topic-signals/momentum")
async def topic_momentum(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(TopicSignal).order_by(TopicSignal.date.desc().nullslast(), TopicSignal.id.desc())
    )
    signals = result.scalars().all()

    cutoff = date.today() - timedelta(days=14)
    rising = []
    declining = []
    going_cold = []
    seen_topics: set[str] = set()

    for s in signals:
        if s.topic in seen_topics:
            continue
        seen_topics.add(s.topic)
        item = _schema(s)
        if s.trend == "rising":
            rising.append(item)
        elif s.trend == "declining":
            declining.append(item)
        elif s.date is not None and s.date < cutoff:
            going_cold.append(item)
        elif s.date is None:
            going_cold.append(item)

    return {"rising": rising, "declining": declining, "going_cold": going_cold}


@router.get("/topic-signals/{signal_id}", response_model=TopicSignalBase)
async def get_topic_signal(signal_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(TopicSignal).where(TopicSignal.id == signal_id)
    )
    signal = result.scalar_one_or_none()
    if not signal:
        raise NotFoundError("Topic signal", signal_id)
    return _schema(signal)


@router.post("/topic-signals", response_model=TopicSignalBase, status_code=201)
async def create_topic_signal(body: TopicSignalCreate, db: AsyncSession = Depends(get_db)):
    signal = TopicSignal(
        date=date.fromisoformat(body.date) if body.date else None,
        topic=body.topic,
        category=body.category,
        intensity=body.intensity,
        first_raised=date.fromisoformat(body.first_raised) if body.first_raised else None,
        meetings_count=body.meetings_count,
        trend=body.trend,
        key_quote=body.key_quote,
        confidence=body.confidence,
        transcript_id=body.transcript_id,
        is_manual=True,
    )
    db.add(signal)
    await db.commit()
    await db.refresh(signal)
    return _schema(signal)


@router.patch("/topic-signals/{signal_id}", response_model=TopicSignalBase)
async def update_topic_signal(
    signal_id: int,
    body: TopicSignalUpdate,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(TopicSignal).where(TopicSignal.id == signal_id)
    )
    signal = result.scalar_one_or_none()
    if not signal:
        raise NotFoundError("Topic signal", signal_id)

    if body.date is not None:
        signal.date = date.fromisoformat(body.date)
    if body.topic is not None:
        signal.topic = body.topic
    if body.category is not None:
        signal.category = body.category
    if body.intensity is not None:
        signal.intensity = body.intensity
    if body.first_raised is not None:
        signal.first_raised = date.fromisoformat(body.first_raised)
    if body.meetings_count is not None:
        signal.meetings_count = body.meetings_count
    if body.trend is not None:
        signal.trend = body.trend
    if body.key_quote is not None:
        signal.key_quote = body.key_quote
    if body.confidence is not None:
        signal.confidence = body.confidence
    if body.transcript_id is not None:
        signal.transcript_id = body.transcript_id

    await db.commit()
    await db.refresh(signal)
    return _schema(signal)


@router.delete("/topic-signals/{signal_id}")
async def delete_topic_signal(signal_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(TopicSignal).where(TopicSignal.id == signal_id)
    )
    signal = result.scalar_one_or_none()
    if not signal:
        raise NotFoundError("Topic signal", signal_id)
    await db.delete(signal)
    await db.commit()
    return {"ok": True}
