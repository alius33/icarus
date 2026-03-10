from datetime import datetime

from fastapi import APIRouter, Depends, Query
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.exceptions import NotFoundError
from app.models.decision import Decision
from app.models.deleted_import import DeletedImport
from app.schemas.decision import DecisionCreate, DecisionSchema, DecisionUpdate

router = APIRouter(tags=["decisions"])


def _decision_schema(d: Decision) -> DecisionSchema:
    return DecisionSchema(
        id=d.id,
        title=f"Decision #{d.number}",
        description=d.decision,
        date=str(d.decision_date) if d.decision_date else None,
        status="recorded",
        owner=", ".join(d.key_people) if d.key_people else None,
        workstream=None,
        transcript_id=None,
        transcript_title=None,
        is_manual=d.is_manual,
    )


@router.get("/decisions", response_model=list[DecisionSchema])
async def list_decisions(
    workstream_id: int | None = Query(None),
    db: AsyncSession = Depends(get_db),
):
    query = select(Decision)
    if workstream_id is not None:
        query = query.where(Decision.workstream_id == workstream_id)
    result = await db.execute(
        query.order_by(Decision.decision_date.asc(), Decision.number.asc())
    )
    return [_decision_schema(d) for d in result.scalars().all()]


@router.get("/decisions/{decision_id}", response_model=DecisionSchema)
async def get_decision(decision_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Decision).where(Decision.id == decision_id))
    d = result.scalar_one_or_none()
    if not d:
        raise NotFoundError("Decision", decision_id)
    return _decision_schema(d)


@router.post("/decisions", response_model=DecisionSchema)
async def create_decision(body: DecisionCreate, db: AsyncSession = Depends(get_db)):
    max_num = await db.execute(select(func.coalesce(func.max(Decision.number), 0)))
    next_number = max_num.scalar_one() + 1

    decision_date = None
    if body.date:
        try:
            decision_date = datetime.strptime(body.date, "%Y-%m-%d").date()
        except ValueError:
            decision_date = datetime.utcnow().date()
    else:
        decision_date = datetime.utcnow().date()

    d = Decision(
        number=next_number,
        decision_date=decision_date,
        decision=body.decision,
        rationale=body.rationale,
        key_people=body.key_people or [],
        is_manual=True,
        source_file="manual",
        file_hash="",
    )
    db.add(d)
    await db.commit()
    await db.refresh(d)
    return _decision_schema(d)


@router.patch("/decisions/{decision_id}", response_model=DecisionSchema)
async def update_decision(decision_id: int, body: DecisionUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Decision).where(Decision.id == decision_id))
    d = result.scalar_one_or_none()
    if not d:
        raise NotFoundError("Decision", decision_id)

    if body.decision is not None:
        d.decision = body.decision
    if body.rationale is not None:
        d.rationale = body.rationale
    if body.key_people is not None:
        d.key_people = body.key_people
    if body.date is not None:
        try:
            d.decision_date = datetime.strptime(body.date, "%Y-%m-%d").date()
        except ValueError:
            pass

    d.is_manual = True
    d.updated_at = datetime.utcnow()
    await db.commit()
    await db.refresh(d)
    return _decision_schema(d)


@router.delete("/decisions/{decision_id}")
async def delete_decision(decision_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Decision).where(Decision.id == decision_id))
    d = result.scalar_one_or_none()
    if not d:
        raise NotFoundError("Decision", decision_id)

    if not d.is_manual:
        db.add(DeletedImport(entity_type="decision", unique_key=str(d.number)))

    await db.delete(d)
    await db.commit()
    return {"ok": True}
