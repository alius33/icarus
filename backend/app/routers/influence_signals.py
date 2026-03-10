from datetime import date

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select, func as sa_func
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.exceptions import NotFoundError
from app.models.influence_signal import InfluenceSignal
from app.schemas.influence_signal import (
    InfluenceSignalBase,
    InfluenceSignalCreate,
    InfluenceSignalUpdate,
)

router = APIRouter(tags=["influence-signals"])


def _schema(s: InfluenceSignal) -> InfluenceSignalBase:
    return InfluenceSignalBase(
        id=s.id,
        date=str(s.date) if s.date else None,
        person=s.person,
        influence_type=s.influence_type,
        direction=s.direction,
        target_person=s.target_person,
        topic=s.topic,
        evidence=s.evidence,
        strength=s.strength,
        confidence=s.confidence,
        coalition_name=s.coalition_name,
        coalition_members=s.coalition_members,
        alignment=s.alignment,
        transcript_id=s.transcript_id,
        is_manual=s.is_manual,
    )


@router.get("/influence-signals", response_model=list[InfluenceSignalBase])
async def list_influence_signals(
    person: str | None = Query(None),
    target_person: str | None = Query(None),
    db: AsyncSession = Depends(get_db),
):
    query = select(InfluenceSignal)
    if person is not None:
        query = query.where(InfluenceSignal.person == person)
    if target_person is not None:
        query = query.where(InfluenceSignal.target_person == target_person)
    query = query.order_by(InfluenceSignal.date.desc().nullslast(), InfluenceSignal.id.desc())
    result = await db.execute(query)
    return [_schema(s) for s in result.scalars().all()]


@router.get("/influence-signals/graph")
async def influence_graph(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(InfluenceSignal).order_by(InfluenceSignal.date.desc().nullslast())
    )
    signals = result.scalars().all()

    node_counts: dict[str, int] = {}
    edge_map: dict[tuple[str, str, str], int] = {}

    for s in signals:
        node_counts[s.person] = node_counts.get(s.person, 0) + 1
        if s.target_person:
            node_counts[s.target_person] = node_counts.get(s.target_person, 0)
            edge_key = (s.person, s.target_person, s.influence_type)
            edge_map[edge_key] = edge_map.get(edge_key, 0) + 1

    nodes = [
        {"id": name, "name": name, "signal_count": count}
        for name, count in node_counts.items()
    ]
    edges = [
        {"source": src, "target": tgt, "type": itype, "weight": weight}
        for (src, tgt, itype), weight in edge_map.items()
    ]

    return {"nodes": nodes, "edges": edges}


@router.get("/influence-signals/arcs/{person}", response_model=list[InfluenceSignalBase])
async def influence_arcs(person: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(InfluenceSignal)
        .where(InfluenceSignal.person == person)
        .order_by(InfluenceSignal.date.asc().nullslast(), InfluenceSignal.id.asc())
    )
    return [_schema(s) for s in result.scalars().all()]


@router.get("/influence-signals/{signal_id}", response_model=InfluenceSignalBase)
async def get_influence_signal(signal_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(InfluenceSignal).where(InfluenceSignal.id == signal_id)
    )
    signal = result.scalar_one_or_none()
    if not signal:
        raise NotFoundError("Influence signal", signal_id)
    return _schema(signal)


@router.post("/influence-signals", response_model=InfluenceSignalBase, status_code=201)
async def create_influence_signal(body: InfluenceSignalCreate, db: AsyncSession = Depends(get_db)):
    signal = InfluenceSignal(
        date=date.fromisoformat(body.date) if body.date else None,
        person=body.person,
        influence_type=body.influence_type,
        direction=body.direction,
        target_person=body.target_person,
        topic=body.topic,
        evidence=body.evidence,
        strength=body.strength,
        confidence=body.confidence,
        coalition_name=body.coalition_name,
        coalition_members=body.coalition_members,
        alignment=body.alignment,
        transcript_id=body.transcript_id,
        is_manual=True,
    )
    db.add(signal)
    await db.commit()
    await db.refresh(signal)
    return _schema(signal)


@router.patch("/influence-signals/{signal_id}", response_model=InfluenceSignalBase)
async def update_influence_signal(
    signal_id: int,
    body: InfluenceSignalUpdate,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(InfluenceSignal).where(InfluenceSignal.id == signal_id)
    )
    signal = result.scalar_one_or_none()
    if not signal:
        raise NotFoundError("Influence signal", signal_id)

    if body.date is not None:
        signal.date = date.fromisoformat(body.date)
    if body.person is not None:
        signal.person = body.person
    if body.influence_type is not None:
        signal.influence_type = body.influence_type
    if body.direction is not None:
        signal.direction = body.direction
    if body.target_person is not None:
        signal.target_person = body.target_person
    if body.topic is not None:
        signal.topic = body.topic
    if body.evidence is not None:
        signal.evidence = body.evidence
    if body.strength is not None:
        signal.strength = body.strength
    if body.confidence is not None:
        signal.confidence = body.confidence
    if body.coalition_name is not None:
        signal.coalition_name = body.coalition_name
    if body.coalition_members is not None:
        signal.coalition_members = body.coalition_members
    if body.alignment is not None:
        signal.alignment = body.alignment
    if body.transcript_id is not None:
        signal.transcript_id = body.transcript_id

    await db.commit()
    await db.refresh(signal)
    return _schema(signal)


@router.delete("/influence-signals/{signal_id}")
async def delete_influence_signal(signal_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(InfluenceSignal).where(InfluenceSignal.id == signal_id)
    )
    signal = result.scalar_one_or_none()
    if not signal:
        raise NotFoundError("Influence signal", signal_id)
    await db.delete(signal)
    await db.commit()
    return {"ok": True}
