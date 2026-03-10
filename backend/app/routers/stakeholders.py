from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.stakeholder import Stakeholder
from app.models.transcript_mention import TranscriptMention
from app.models.transcript import Transcript
from app.models.deleted_import import DeletedImport
from app.schemas.stakeholder import (
    StakeholderBase, StakeholderDetail, StakeholderCreate, StakeholderUpdate, MentionItem,
)

router = APIRouter(tags=["stakeholders"])


@router.get("/stakeholders", response_model=list[StakeholderBase])
async def list_stakeholders(
    tier: int | None = Query(None, ge=1, le=3),
    db: AsyncSession = Depends(get_db),
):
    query = select(Stakeholder)
    if tier is not None:
        query = query.where(Stakeholder.tier == tier)
    result = await db.execute(query.order_by(Stakeholder.tier, Stakeholder.name))
    stakeholders = result.scalars().all()

    items = []
    for s in stakeholders:
        mc = await db.execute(
            select(func.coalesce(func.sum(TranscriptMention.mention_count), 0))
            .where(TranscriptMention.stakeholder_id == s.id)
        )
        items.append(StakeholderBase(
            id=s.id, name=s.name, role=s.role, organisation=None,
            tier=s.tier, mention_count=mc.scalar_one(),
            risk_level=s.risk_level, morale_notes=s.morale_notes,
            is_manual=s.is_manual,
        ))
    return items


@router.get("/stakeholders/{stakeholder_id}", response_model=StakeholderDetail)
async def get_stakeholder(stakeholder_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Stakeholder).where(Stakeholder.id == stakeholder_id))
    s = result.scalar_one_or_none()
    if not s:
        raise HTTPException(status_code=404, detail="Stakeholder not found")

    mc = await db.execute(
        select(func.coalesce(func.sum(TranscriptMention.mention_count), 0))
        .where(TranscriptMention.stakeholder_id == stakeholder_id)
    )

    mention_result = await db.execute(
        select(TranscriptMention.transcript_id, Transcript.title, Transcript.meeting_date, TranscriptMention.mention_type)
        .join(Transcript, TranscriptMention.transcript_id == Transcript.id)
        .where(TranscriptMention.stakeholder_id == stakeholder_id)
        .order_by(Transcript.meeting_date.desc()).limit(10)
    )
    recent_mentions = [
        MentionItem(transcript_id=r.transcript_id, transcript_title=r.title,
                     date=str(r.meeting_date) if r.meeting_date else None, snippet=r.mention_type)
        for r in mention_result.all()
    ]
    return StakeholderDetail(
        id=s.id, name=s.name, role=s.role, organisation=None, tier=s.tier,
        mention_count=mc.scalar_one(), notes=s.notes, aliases=[], recent_mentions=recent_mentions,
        risk_level=s.risk_level, morale_notes=s.morale_notes,
        is_manual=s.is_manual,
    )


@router.post("/stakeholders", response_model=StakeholderBase)
async def create_stakeholder(body: StakeholderCreate, db: AsyncSession = Depends(get_db)):
    existing = await db.execute(select(Stakeholder).where(Stakeholder.name == body.name))
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=409, detail="Stakeholder with this name already exists")

    s = Stakeholder(name=body.name, tier=body.tier, role=body.role, notes=body.notes,
                    is_manual=True, source_file="manual", file_hash="")
    db.add(s)
    await db.commit()
    await db.refresh(s)
    return StakeholderBase(id=s.id, name=s.name, role=s.role, organisation=None,
                           tier=s.tier, mention_count=0, is_manual=True)


@router.patch("/stakeholders/{stakeholder_id}", response_model=StakeholderBase)
async def update_stakeholder(stakeholder_id: int, body: StakeholderUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Stakeholder).where(Stakeholder.id == stakeholder_id))
    s = result.scalar_one_or_none()
    if not s:
        raise HTTPException(status_code=404, detail="Stakeholder not found")

    if body.tier is not None:
        s.tier = body.tier
    if body.role is not None:
        s.role = body.role
    if body.notes is not None:
        s.notes = body.notes
    if body.risk_level is not None:
        s.risk_level = body.risk_level
    if body.morale_notes is not None:
        s.morale_notes = body.morale_notes
    s.is_manual = True
    s.updated_at = datetime.utcnow()
    await db.commit()
    await db.refresh(s)

    mc = await db.execute(
        select(func.coalesce(func.sum(TranscriptMention.mention_count), 0))
        .where(TranscriptMention.stakeholder_id == s.id)
    )
    return StakeholderBase(id=s.id, name=s.name, role=s.role, organisation=None,
                           tier=s.tier, mention_count=mc.scalar_one(),
                           risk_level=s.risk_level, morale_notes=s.morale_notes,
                           is_manual=s.is_manual)


@router.delete("/stakeholders/{stakeholder_id}")
async def delete_stakeholder(stakeholder_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Stakeholder).where(Stakeholder.id == stakeholder_id))
    s = result.scalar_one_or_none()
    if not s:
        raise HTTPException(status_code=404, detail="Stakeholder not found")

    if not s.is_manual:
        db.add(DeletedImport(entity_type="stakeholder", unique_key=s.name))
    await db.delete(s)
    await db.commit()
    return {"ok": True}


@router.get("/stakeholders/{stakeholder_id}/mentions", response_model=list[MentionItem])
async def get_stakeholder_mentions(stakeholder_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Stakeholder).where(Stakeholder.id == stakeholder_id))
    if not result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Stakeholder not found")

    mention_result = await db.execute(
        select(TranscriptMention.transcript_id, Transcript.title, Transcript.meeting_date, TranscriptMention.mention_type)
        .join(Transcript, TranscriptMention.transcript_id == Transcript.id)
        .where(TranscriptMention.stakeholder_id == stakeholder_id)
        .order_by(Transcript.meeting_date.desc()).limit(20)
    )
    return [
        MentionItem(transcript_id=r.transcript_id, transcript_title=r.title,
                     date=str(r.meeting_date) if r.meeting_date else None, snippet=r.mention_type)
        for r in mention_result.all()
    ]
