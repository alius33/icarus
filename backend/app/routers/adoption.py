from datetime import datetime

from app.models.adoption_metric import AdoptionMetric
from app.routers.crud_factory import CRUDConfig, create_crud_router
from app.schemas.adoption_metric import AdoptionMetricCreate, AdoptionMetricSchema


# Adoption doesn't have an update schema — create a minimal one
from pydantic import BaseModel


class AdoptionMetricUpdate(BaseModel):
    date: str | None = None
    metric_type: str | None = None
    value: int | None = None
    workstream: str | None = None
    notes: str | None = None


def _to_schema(m: AdoptionMetric) -> AdoptionMetricSchema:
    return AdoptionMetricSchema(
        id=m.id,
        date=str(m.date) if m.date else "",
        metric_type=m.metric_type,
        value=m.value,
        workstream=m.workstream,
        notes=m.notes,
    )


def _create_to_orm(body: AdoptionMetricCreate, db) -> dict:
    metric_date = None
    try:
        metric_date = datetime.strptime(body.date, "%Y-%m-%d").date()
    except ValueError:
        metric_date = datetime.utcnow().date()
    return {
        "date": metric_date,
        "metric_type": body.metric_type,
        "value": body.value,
        "workstream": body.workstream,
        "notes": body.notes,
    }


config = CRUDConfig(
    model=AdoptionMetric,
    schema=AdoptionMetricSchema,
    schema_create=AdoptionMetricCreate,
    schema_update=AdoptionMetricUpdate,
    prefix="/adoption",
    entity_name="Adoption metric",
    tags=["adoption"],
    to_schema=_to_schema,
    create_to_orm=_create_to_orm,
    ordering=[("date", "desc"), ("id", "desc")],
)

router = create_crud_router(config)
