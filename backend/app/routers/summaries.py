from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.summary import Summary
from app.models.transcript import Transcript
from app.schemas.summary import SummaryBase, SummaryDetail

router = APIRouter(tags=["summaries"])


@router.get("/summaries", response_model=list[SummaryBase])
async def list_summaries(
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Summary, Transcript.title)
        .outerjoin(Transcript, Summary.transcript_id == Transcript.id)
        .order_by(Summary.id)
    )
    rows = result.all()

    return [
        SummaryBase(
            id=s.id,
            transcript_id=s.transcript_id or 0,
            transcript_title=title,
            date=None,
            tldr=None,
        )
        for s, title in rows
    ]


@router.get("/summaries/{summary_id}", response_model=SummaryDetail)
async def get_summary(
    summary_id: int,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Summary, Transcript.title)
        .outerjoin(Transcript, Summary.transcript_id == Transcript.id)
        .where(Summary.id == summary_id)
    )
    row = result.one_or_none()
    if not row:
        raise HTTPException(status_code=404, detail="Summary not found")

    summary, transcript_title = row

    return SummaryDetail(
        id=summary.id,
        transcript_id=summary.transcript_id or 0,
        transcript_title=transcript_title,
        date=None,
        tldr=None,
        full_summary=summary.content,
        key_decisions=[],
        action_items=[],
        risks_and_concerns=[],
        follow_ups=[],
    )
