from app.models.dependency import Dependency
from app.routers.crud_factory import CRUDConfig, create_crud_router
from app.schemas.dependency import DependencyCreate, DependencySchema, DependencyUpdate

config = CRUDConfig(
    model=Dependency,
    schema=DependencySchema,
    schema_create=DependencyCreate,
    schema_update=DependencyUpdate,
    prefix="/dependencies",
    entity_name="Dependency",
    tags=["dependencies"],
    to_schema=lambda d: DependencySchema(
        id=d.id,
        name=d.name,
        dependency_type=d.dependency_type,
        status=d.status,
        blocking_reason=d.blocking_reason,
        estimated_effort=d.estimated_effort,
        assigned_to=d.assigned_to,
        affected_workstreams=d.affected_workstreams,
        priority=d.priority or "MEDIUM",
        notes=d.notes,
    ),
    ordering=[("created_at", "desc")],
)

router = create_crud_router(config)
