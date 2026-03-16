from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.exceptions import NotFoundError
from app.models.dependency import Dependency
from app.schemas.dependency import DependencyCreate, DependencySchema, DependencyUpdate

router = APIRouter(tags=["dependencies"])


def _schema(d: Dependency) -> DependencySchema:
    return DependencySchema(
        id=d.id,
        name=d.name,
        dependency_type=d.dependency_type,
        status=d.status,
        blocking_reason=d.blocking_reason,
        estimated_effort=d.estimated_effort,
        assigned_to=d.assigned_to,
        affected_projects=d.affected_projects,
        priority=d.priority or "MEDIUM",
        notes=d.notes,
    )


@router.get("/dependencies", response_model=list[DependencySchema])
async def list_dependencies(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Dependency).order_by(Dependency.created_at.desc()))
    return [_schema(d) for d in result.scalars().all()]


@router.get("/dependencies/{dep_id}", response_model=DependencySchema)
async def get_dependency(dep_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Dependency).where(Dependency.id == dep_id))
    dep = result.scalar_one_or_none()
    if not dep:
        raise NotFoundError("Dependency", dep_id)
    return _schema(dep)


@router.post("/dependencies", response_model=DependencySchema, status_code=201)
async def create_dependency(body: DependencyCreate, db: AsyncSession = Depends(get_db)):
    dep = Dependency(
        name=body.name,
        dependency_type=body.dependency_type,
        status=body.status,
        blocking_reason=body.blocking_reason,
        estimated_effort=body.estimated_effort,
        assigned_to=body.assigned_to,
        affected_projects=body.affected_projects,
        priority=body.priority,
        notes=body.notes,
    )
    db.add(dep)
    await db.commit()
    await db.refresh(dep)
    return _schema(dep)


@router.patch("/dependencies/{dep_id}", response_model=DependencySchema)
async def update_dependency(dep_id: int, body: DependencyUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Dependency).where(Dependency.id == dep_id))
    dep = result.scalar_one_or_none()
    if not dep:
        raise NotFoundError("Dependency", dep_id)

    for field in ["name", "dependency_type", "status", "blocking_reason",
                  "estimated_effort", "assigned_to", "affected_projects",
                  "priority", "notes"]:
        val = getattr(body, field)
        if val is not None:
            setattr(dep, field, val)

    dep.updated_at = datetime.utcnow()
    await db.commit()
    await db.refresh(dep)
    return _schema(dep)


@router.delete("/dependencies/{dep_id}")
async def delete_dependency(dep_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Dependency).where(Dependency.id == dep_id))
    dep = result.scalar_one_or_none()
    if not dep:
        raise NotFoundError("Dependency", dep_id)
    await db.delete(dep)
    await db.commit()
    return {"ok": True}
