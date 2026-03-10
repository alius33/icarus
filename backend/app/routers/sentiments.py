from datetime import date, datetime

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.sentiment_signal import SentimentSignal
from app.schemas.sentiment_signal import (
    SentimentSignalBase,
    SentimentSignalCreate,
    SentimentSignalUpdate,
)

router = APIRouter(tags=["sentiments"])


def _schema(s: SentimentSignal) -> SentimentSignalBase:
    return SentimentSignalBase(
        id=s.id,
        stakeholder_id=s.stakeholder_id,
        transcript_id=s.transcript_id,
        date=str(s.date) if s.date else None,
        sentiment=s.sentiment,
        shift=s.shift,
        topic=s.topic,
        quote=s.quote,
        notes=s.notes,
        is_manual=s.is_manual,
    )


@router.get("/sentiments", response_model=list[SentimentSignalBase])
async def list_sentiments(
    stakeholder_id: int | None = Query(None),
    db: AsyncSession = Depends(get_db),
):
    query = select(SentimentSignal)
    if stakeholder_id is not None:
        query = query.where(SentimentSignal.stakeholder_id == stakeholder_id)
    query = query.order_by(SentimentSignal.date.desc().nullslast(), SentimentSignal.id.desc())
    result = await db.execute(query)
    return [_schema(s) for s in result.scalars().all()]


@router.get("/sentiments/{signal_id}", response_model=SentimentSignalBase)
async def get_sentiment(signal_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(SentimentSignal).where(SentimentSignal.id == signal_id)
    )
    signal = result.scalar_one_or_none()
    if not signal:
        raise HTTPException(status_code=404, detail="Sentiment signal not found")
    return _schema(signal)


@router.post("/sentiments", response_model=SentimentSignalBase, status_code=201)
async def create_sentiment(body: SentimentSignalCreate, db: AsyncSession = Depends(get_db)):
    signal = SentimentSignal(
        stakeholder_id=body.stakeholder_id,
        transcript_id=body.transcript_id,
        date=date.fromisoformat(body.date) if body.date else None,
        sentiment=body.sentiment,
        shift=body.shift,
        topic=body.topic,
        quote=body.quote,
        notes=body.notes,
        is_manual=True,
    )
    db.add(signal)
    await db.commit()
    await db.refresh(signal)
    return _schema(signal)


@router.patch("/sentiments/{signal_id}", response_model=SentimentSignalBase)
async def update_sentiment(
    signal_id: int,
    body: SentimentSignalUpdate,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(SentimentSignal).where(SentimentSignal.id == signal_id)
    )
    signal = result.scalar_one_or_none()
    if not signal:
        raise HTTPException(status_code=404, detail="Sentiment signal not found")

    if body.stakeholder_id is not None:
        signal.stakeholder_id = body.stakeholder_id
    if body.transcript_id is not None:
        signal.transcript_id = body.transcript_id
    if body.date is not None:
        signal.date = date.fromisoformat(body.date)
    if body.sentiment is not None:
        signal.sentiment = body.sentiment
    if body.shift is not None:
        signal.shift = body.shift
    if body.topic is not None:
        signal.topic = body.topic
    if body.quote is not None:
        signal.quote = body.quote
    if body.notes is not None:
        signal.notes = body.notes

    await db.commit()
    await db.refresh(signal)
    return _schema(signal)


@router.delete("/sentiments/{signal_id}")
async def delete_sentiment(signal_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(SentimentSignal).where(SentimentSignal.id == signal_id)
    )
    signal = result.scalar_one_or_none()
    if not signal:
        raise HTTPException(status_code=404, detail="Sentiment signal not found")
    await db.delete(signal)
    await db.commit()
    return {"ok": True}


@router.get(
    "/sentiments/timeline/{stakeholder_id}",
    response_model=list[SentimentSignalBase],
)
async def sentiment_timeline(
    stakeholder_id: int, db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(SentimentSignal)
        .where(SentimentSignal.stakeholder_id == stakeholder_id)
        .order_by(SentimentSignal.date.asc().nullslast(), SentimentSignal.id.asc())
    )
    return [_schema(s) for s in result.scalars().all()]
