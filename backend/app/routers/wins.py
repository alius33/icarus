from collections import defaultdict
from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.programme_win import ProgrammeWin
from app.routers.crud_factory import CRUDConfig, create_crud_router
from app.schemas.programme_win import (
    ProgrammeWinCreate,
    ProgrammeWinSchema,
    ProgrammeWinSummary,
    ProgrammeWinUpdate,
)


def _to_schema(w: ProgrammeWin) -> ProgrammeWinSchema:
    return ProgrammeWinSchema(
        id=w.id,
        category=w.category,
        title=w.title,
        description=w.description,
        before_state=w.before_state,
        after_state=w.after_state,
        workstream=w.workstream,
        confidence=w.confidence or "estimated",
        date_recorded=str(w.date_recorded) if w.date_recorded else None,
        notes=w.notes,
        is_manual=w.is_manual if w.is_manual is not None else True,
    )


def _create_to_orm(body: ProgrammeWinCreate, db) -> dict:
    date_recorded = None
    if body.date_recorded:
        try:
            date_recorded = datetime.strptime(body.date_recorded, "%Y-%m-%d").date()
        except ValueError:
            date_recorded = datetime.utcnow().date()
    else:
        date_recorded = datetime.utcnow().date()

    return {
        "category": body.category,
        "title": body.title,
        "description": body.description,
        "before_state": body.before_state,
        "after_state": body.after_state,
        "workstream": body.workstream,
        "confidence": body.confidence,
        "date_recorded": date_recorded,
        "notes": body.notes,
        "is_manual": True,
    }


# Register custom endpoints FIRST (before /{item_id})
router = APIRouter(tags=["wins"])


@router.get("/wins/summary", response_model=ProgrammeWinSummary)
async def wins_summary(db: AsyncSession = Depends(get_db)):
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


# Add CRUD routes to the same router (detail routes come after /summary)
config = CRUDConfig(
    model=ProgrammeWin,
    schema=ProgrammeWinSchema,
    schema_create=ProgrammeWinCreate,
    schema_update=ProgrammeWinUpdate,
    prefix="/wins",
    entity_name="Programme win",
    tags=["wins"],
    to_schema=_to_schema,
    create_to_orm=_create_to_orm,
    ordering=[("date_recorded", "desc_nullslast"), ("created_at", "desc")],
    date_fields=["date_recorded"],
)

create_crud_router(config, router=router)
