from datetime import date

from app.models.commitment import Commitment
from app.routers.crud_factory import CRUDConfig, WritebackHooks, create_crud_router
from app.schemas.commitment import CommitmentBase, CommitmentCreate, CommitmentUpdate
from app.services.commitment_writeback import (
    append_commitment,
    remove_commitment,
    update_commitment_status,
)


def _to_schema(c: Commitment) -> CommitmentBase:
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


def _create_to_orm(body: CommitmentCreate, db) -> dict:
    return {
        "person": body.person,
        "commitment": body.commitment,
        "transcript_id": body.transcript_id,
        "date_made": date.fromisoformat(body.date_made) if body.date_made else None,
        "deadline_text": body.deadline_text,
        "deadline_resolved": date.fromisoformat(body.deadline_resolved) if body.deadline_resolved else None,
        "deadline_type": body.deadline_type,
        "condition": body.condition,
        "linked_action_id": body.linked_action_id,
        "status": body.status,
        "notes": body.notes,
        "is_manual": True,
    }


def _on_create(item: Commitment, body: CommitmentCreate):
    append_commitment(
        date_made=item.date_made,
        person=body.person or "",
        commitment=body.commitment or "",
        deadline_text=body.deadline_text,
        condition=body.condition,
        status=body.status or "pending",
    )


def _on_update(item: Commitment, body: CommitmentUpdate):
    if body.status is not None:
        update_commitment_status(item.person, item.commitment, body.status)


def _on_delete(item: Commitment):
    remove_commitment(item.person, item.commitment)


config = CRUDConfig(
    model=Commitment,
    schema=CommitmentBase,
    schema_create=CommitmentCreate,
    schema_update=CommitmentUpdate,
    prefix="/commitments",
    entity_name="Commitment",
    tags=["commitments"],
    to_schema=_to_schema,
    create_to_orm=_create_to_orm,
    ordering=[("date_made", "desc_nullslast"), ("id", "desc")],
    date_fields=["date_made", "deadline_resolved", "verified_date"],
    writeback=WritebackHooks(
        on_create=_on_create,
        on_update=_on_update,
        on_delete=_on_delete,
    ),
)

router = create_crud_router(config)
