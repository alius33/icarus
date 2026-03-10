from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.adoption_metric import AdoptionMetric
from app.schemas.adoption_metric import AdoptionMetricSchema, AdoptionMetricCreate

router = APIRouter(tags=["adoption"])


def _schema(m: AdoptionMetric) -> AdoptionMetricSchema:
    return AdoptionMetricSchema(
        id=m.id,
        date=str(m.date) if m.date else "",
        metric_type=m.metric_type,
        value=m.value,
        workstream=m.workstream,
        notes=m.notes,
    )


@router.get("/adoption", response_model=list[AdoptionMetricSchema])
async def list_adoption_metrics(
    workstream: str | None = Query(None),
    metric_type: str | None = Query(None),
    db: AsyncSession = Depends(get_db),
):
    query = select(AdoptionMetric)
    if workstream:
        query = query.where(AdoptionMetric.workstream == workstream)
    if metric_type:
        query = query.where(AdoptionMetric.metric_type == metric_type)

    result = await db.execute(query.order_by(AdoptionMetric.date.desc(), AdoptionMetric.id.desc()))
    return [_schema(m) for m in result.scalars().all()]


@router.post("/adoption", response_model=AdoptionMetricSchema, status_code=201)
async def create_adoption_metric(body: AdoptionMetricCreate, db: AsyncSession = Depends(get_db)):
    metric_date = None
    try:
        metric_date = datetime.strptime(body.date, "%Y-%m-%d").date()
    except ValueError:
        metric_date = datetime.utcnow().date()

    metric = AdoptionMetric(
        date=metric_date,
        metric_type=body.metric_type,
        value=body.value,
        workstream=body.workstream,
        notes=body.notes,
    )
    db.add(metric)
    await db.commit()
    await db.refresh(metric)
    return _schema(metric)


@router.delete("/adoption/{metric_id}")
async def delete_adoption_metric(metric_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(AdoptionMetric).where(AdoptionMetric.id == metric_id))
    metric = result.scalar_one_or_none()
    if not metric:
        raise HTTPException(status_code=404, detail="Adoption metric not found")
    await db.delete(metric)
    await db.commit()
    return {"ok": True}
