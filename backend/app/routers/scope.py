from app.models.scope_item import ScopeItem
from app.routers.crud_factory import CRUDConfig, create_crud_router
from app.schemas.scope_item import ScopeItemCreate, ScopeItemSchema, ScopeItemUpdate

config = CRUDConfig(
    model=ScopeItem,
    schema=ScopeItemSchema,
    schema_create=ScopeItemCreate,
    schema_update=ScopeItemUpdate,
    prefix="/scope",
    entity_name="Scope item",
    tags=["scope"],
    to_schema=lambda s: ScopeItemSchema(
        id=s.id,
        name=s.name,
        scope_type=s.scope_type,
        workstream=s.workstream,
        added_date=s.added_date,
        estimated_effort=s.estimated_effort,
        budgeted=s.budgeted or False,
        status=s.status or "planned",
        description=s.description,
        impact_notes=s.impact_notes,
    ),
    ordering=[("scope_type", "asc"), ("created_at", "desc")],
)

router = create_crud_router(config)
