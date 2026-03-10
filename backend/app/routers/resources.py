from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.exceptions import NotFoundError
from app.models.resource_allocation import ResourceAllocation
from app.schemas.resource_allocation import (
    AllocationEntry,
    ResourceAllocationCreate,
    ResourceAllocationSchema,
    ResourceAllocationUpdate,
)

router = APIRouter(tags=["resources"])


def _schema(r: ResourceAllocation) -> ResourceAllocationSchema:
    allocs = []
    if r.allocations:
        for a in r.allocations:
            allocs.append(AllocationEntry(workstream=a.get("workstream", ""), percentage=a.get("percentage", 0)))
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


@router.get("/resources", response_model=list[ResourceAllocationSchema])
async def list_resources(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(ResourceAllocation).order_by(ResourceAllocation.person_name))
    return [_schema(r) for r in result.scalars().all()]


@router.get("/resources/{res_id}", response_model=ResourceAllocationSchema)
async def get_resource(res_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(ResourceAllocation).where(ResourceAllocation.id == res_id))
    res = result.scalar_one_or_none()
    if not res:
        raise NotFoundError("Resource allocation", res_id)
    return _schema(res)


@router.post("/resources", response_model=ResourceAllocationSchema, status_code=201)
async def create_resource(body: ResourceAllocationCreate, db: AsyncSession = Depends(get_db)):
    res = ResourceAllocation(
        person_name=body.person_name,
        role=body.role,
        allocations=[a.model_dump() for a in body.allocations],
        capacity_status=body.capacity_status,
        notes=body.notes,
        start_date=body.start_date,
        end_date=body.end_date,
    )
    db.add(res)
    await db.commit()
    await db.refresh(res)
    return _schema(res)


@router.patch("/resources/{res_id}", response_model=ResourceAllocationSchema)
async def update_resource(res_id: int, body: ResourceAllocationUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(ResourceAllocation).where(ResourceAllocation.id == res_id))
    res = result.scalar_one_or_none()
    if not res:
        raise NotFoundError("Resource allocation", res_id)

    if body.person_name is not None:
        res.person_name = body.person_name
    if body.role is not None:
        res.role = body.role
    if body.allocations is not None:
        res.allocations = [a.model_dump() for a in body.allocations]
    if body.capacity_status is not None:
        res.capacity_status = body.capacity_status
    if body.notes is not None:
        res.notes = body.notes
    if body.start_date is not None:
        res.start_date = body.start_date
    if body.end_date is not None:
        res.end_date = body.end_date

    res.updated_at = datetime.utcnow()
    await db.commit()
    await db.refresh(res)
    return _schema(res)


@router.delete("/resources/{res_id}")
async def delete_resource(res_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(ResourceAllocation).where(ResourceAllocation.id == res_id))
    res = result.scalar_one_or_none()
    if not res:
        raise NotFoundError("Resource allocation", res_id)
    await db.delete(res)
    await db.commit()
    return {"ok": True}
