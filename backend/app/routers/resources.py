from app.models.resource_allocation import ResourceAllocation
from app.routers.crud_factory import CRUDConfig, create_crud_router
from app.schemas.resource_allocation import (
    AllocationEntry,
    ResourceAllocationCreate,
    ResourceAllocationSchema,
    ResourceAllocationUpdate,
)


def _to_schema(r: ResourceAllocation) -> ResourceAllocationSchema:
    allocs = []
    if r.allocations:
        for a in r.allocations:
            allocs.append(AllocationEntry(
                workstream=a.get("workstream", ""),
                percentage=a.get("percentage", 0),
            ))
    return ResourceAllocationSchema(
        id=r.id,
        person_name=r.person_name,
        role=r.role,
        allocations=allocs,
        capacity_status=r.capacity_status or "available",
        notes=r.notes,
        start_date=r.start_date,
        end_date=r.end_date,
    )


def _create_to_orm(body: ResourceAllocationCreate, db) -> dict:
    return {
        "person_name": body.person_name,
        "role": body.role,
        "allocations": [a.model_dump() for a in body.allocations],
        "capacity_status": body.capacity_status,
        "notes": body.notes,
        "start_date": body.start_date,
        "end_date": body.end_date,
    }


config = CRUDConfig(
    model=ResourceAllocation,
    schema=ResourceAllocationSchema,
    schema_create=ResourceAllocationCreate,
    schema_update=ResourceAllocationUpdate,
    prefix="/resources",
    entity_name="Resource allocation",
    tags=["resources"],
    to_schema=_to_schema,
    create_to_orm=_create_to_orm,
    ordering=[("person_name", "asc")],
)

router = create_crud_router(config)
