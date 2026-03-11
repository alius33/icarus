from datetime import date

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.exceptions import NotFoundError
from app.models.commitment import Commitment
from app.services.commitment_writeback import (
    append_commitment,
    remove_commitment,
    update_commitment_status,
)
from app.schemas.commitment import CommitmentBase, CommitmentCreate, CommitmentUpdate

router = APIRouter(tags=["commitments"])


def _schema(c: Commitment) -> CommitmentBase:
    return CommitmentBase(
        id=c.id,
        person=c.person,
        commitment=c.commitment,
        transcript_id=c.transcript_id,
        date_made=str(c.date_made) if c.date_made else None,
        deadline_text=c.deadline_text,
        deadline_resolved=str(c.deadline_resolved) if c.deadline_resolved else None,
        deadline_type=c.deadline_type,
        condition=c.condition,
        linked_action_id=c.linked_action_id,
        status=c.status,
        verified_date=str(c.verified_date) if c.verified_date else None,
        notes=c.notes,
        is_manual=c.is_manual,
    )


@router.get("/commitments", response_model=list[CommitmentBase])
async def list_commitments(
    person: str | None = Query(None),
    status: str | None = Query(None),
    db: AsyncSession = Depends(get_db),
):
    query = select(Commitment)
    if person is not None:
        query = query.where(Commitment.person == person)
    if status is not None:
        query = query.where(Commitment.status == status)
    query = query.order_by(Commitment.date_made.desc().nullslast(), Commitment.id.desc())
    result = await db.execute(query)
    return [_schema(c) for c in result.scalars().all()]


@router.get("/commitments/{commitment_id}", response_model=CommitmentBase)
async def get_commitment(commitment_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Commitment).where(Commitment.id == commitment_id)
    )
    item = result.scalar_one_or_none()
    if not item:
        raise NotFoundError("Commitment", commitment_id)
    return _schema(item)


@router.post("/commitments", response_model=CommitmentBase, status_code=201)
async def create_commitment(body: CommitmentCreate, db: AsyncSession = Depends(get_db)):
    item = Commitment(
        person=body.person,
        commitment=body.commitment,
        transcript_id=body.transcript_id,
        date_made=date.fromisoformat(body.date_made) if body.date_made else None,
        deadline_text=body.deadline_text,
        deadline_resolved=date.fromisoformat(body.deadline_resolved) if body.deadline_resolved else None,
        deadline_type=body.deadline_type,
        condition=body.condition,
        linked_action_id=body.linked_action_id,
        status=body.status,
        notes=body.notes,
        is_manual=True,
    )
    db.add(item)
    await db.commit()
    await db.refresh(item)

    # Writeback to markdown
    append_commitment(
        date_made=item.date_made,
        person=body.person or "",
        commitment=body.commitment or "",
        deadline_text=body.deadline_text,
        condition=body.condition,
        status=body.status or "pending",
    )

    return _schema(item)


@router.patch("/commitments/{commitment_id}", response_model=CommitmentBase)
async def update_commitment(
    commitment_id: int,
    body: CommitmentUpdate,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Commitment).where(Commitment.id == commitment_id)
    )
    item = result.scalar_one_or_none()
    if not item:
        raise NotFoundError("Commitment", commitment_id)

    if body.person is not None:
        item.person = body.person
    if body.commitment is not None:
        item.commitment = body.commitment
    if body.transcript_id is not None:
        item.transcript_id = body.transcript_id
    if body.date_made is not None:
        item.date_made = date.fromisoformat(body.date_made)
    if body.deadline_text is not None:
        item.deadline_text = body.deadline_text
    if body.deadline_resolved is not None:
        item.deadline_resolved = date.fromisoformat(body.deadline_resolved)
    if body.deadline_type is not None:
        item.deadline_type = body.deadline_type
    if body.condition is not None:
        item.condition = body.condition
    if body.linked_action_id is not None:
        item.linked_action_id = body.linked_action_id
    if body.status is not None:
        item.status = body.status
    if body.verified_date is not None:
        item.verified_date = date.fromisoformat(body.verified_date)
    if body.notes is not None:
        item.notes = body.notes

    await db.commit()
    await db.refresh(item)

    # Writeback to markdown on status change
    if body.status is not None:
        update_commitment_status(item.person, item.commitment, body.status)

    return _schema(item)


@router.delete("/commitments/{commitment_id}")
async def delete_commitment(commitment_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Commitment).where(Commitment.id == commitment_id)
    )
    item = result.scalar_one_or_none()
    if not item:
        raise NotFoundError("Commitment", commitment_id)

    # Writeback to markdown (before delete)
    remove_commitment(item.person, item.commitment)

    await db.delete(item)
    await db.commit()
    return {"ok": True}
