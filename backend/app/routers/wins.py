from collections import defaultdict
from datetime import datetime

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db, utcnow
from app.exceptions import NotFoundError
from app.models.programme_win import ProgrammeWin
from app.schemas.programme_win import (
    ProgrammeWinCreate,
    ProgrammeWinGrouped,
    ProgrammeWinSchema,
    ProgrammeWinSummary,
    ProgrammeWinUpdate,
)

router = APIRouter(tags=["wins"])


def _schema(w: ProgrammeWin) -> ProgrammeWinSchema:
    return ProgrammeWinSchema(
        id=w.id,
        category=w.category,
        title=w.title,
        description=w.description,
        before_state=w.before_state,
        after_state=w.after_state,
        project=w.project,
        confidence=w.confidence or "estimated",
        date_recorded=str(w.date_recorded) if w.date_recorded else None,
        notes=w.notes,
        is_manual=w.is_manual if w.is_manual is not None else True,
    )


@router.get("/wins/summary", response_model=ProgrammeWinSummary)
async def wins_summary(db: AsyncSession = Depends(get_db)):
    """Summary stats: total count, count by category, count by confidence."""
    result = await db.execute(select(ProgrammeWin))
    wins = result.scalars().all()

    by_category: dict[str, int] = defaultdict(int)
    by_confidence: dict[str, int] = defaultdict(int)
    for w in wins:
        by_category[w.category] += 1
        by_confidence[w.confidence or "estimated"] += 1

    return ProgrammeWinSummary(
        total=len(wins),
        by_category=dict(by_category),
        by_confidence=dict(by_confidence),
    )


@router.get("/wins", response_model=list[ProgrammeWinSchema] | list[ProgrammeWinGrouped])
async def list_wins(
    grouped: bool = Query(False, description="Group results by category"),
    category: str | None = Query(None),
    project: str | None = Query(None),
    db: AsyncSession = Depends(get_db),
):
    query = select(ProgrammeWin)
    if category:
        query = query.where(ProgrammeWin.category == category)
    if project:
        query = query.where(ProgrammeWin.project == project)

    result = await db.execute(query.order_by(ProgrammeWin.date_recorded.desc().nullslast(), ProgrammeWin.created_at.desc()))
    wins = [_schema(w) for w in result.scalars().all()]

    if grouped:
        groups: dict[str, list[ProgrammeWinSchema]] = defaultdict(list)
        for w in wins:
            groups[w.category].append(w)
        return [
            ProgrammeWinGrouped(category=cat, count=len(items), wins=items)
            for cat, items in groups.items()
        ]

    return wins


@router.get("/wins/{win_id}", response_model=ProgrammeWinSchema)
async def get_win(win_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(ProgrammeWin).where(ProgrammeWin.id == win_id))
    win = result.scalar_one_or_none()
    if not win:
        raise NotFoundError("Programme win", win_id)
    return _schema(win)


@router.post("/wins", response_model=ProgrammeWinSchema, status_code=201)
async def create_win(body: ProgrammeWinCreate, db: AsyncSession = Depends(get_db)):
    date_recorded = None
    if body.date_recorded:
        try:
            date_recorded = datetime.strptime(body.date_recorded, "%Y-%m-%d").date()
        except ValueError:
            date_recorded = utcnow().date()
    else:
        date_recorded = utcnow().date()

    win = ProgrammeWin(
        category=body.category,
        title=body.title,
        description=body.description,
        before_state=body.before_state,
        after_state=body.after_state,
        project=body.project,
        confidence=body.confidence,
        date_recorded=date_recorded,
        notes=body.notes,
        is_manual=True,
    )
    db.add(win)
    await db.commit()
    await db.refresh(win)
    return _schema(win)


@router.patch("/wins/{win_id}", response_model=ProgrammeWinSchema)
async def update_win(win_id: int, body: ProgrammeWinUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(ProgrammeWin).where(ProgrammeWin.id == win_id))
    win = result.scalar_one_or_none()
    if not win:
        raise NotFoundError("Programme win", win_id)

    for field in ["category", "title", "description", "before_state", "after_state",
                  "project", "confidence", "notes"]:
        val = getattr(body, field)
        if val is not None:
            setattr(win, field, val)

    if body.date_recorded is not None:
        try:
            win.date_recorded = datetime.strptime(body.date_recorded, "%Y-%m-%d").date()
        except ValueError:
            pass

    win.updated_at = utcnow()
    await db.commit()
    await db.refresh(win)
    return _schema(win)


@router.delete("/wins/{win_id}")
async def delete_win(win_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(ProgrammeWin).where(ProgrammeWin.id == win_id))
    win = result.scalar_one_or_none()
    if not win:
        raise NotFoundError("Programme win", win_id)
    await db.delete(win)
    await db.commit()
    return {"ok": True}
