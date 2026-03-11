from app.models.division_profile import DivisionProfile
from app.routers.crud_factory import CRUDConfig, create_crud_router
from app.schemas.division_profile import (
    DivisionProfileCreate,
    DivisionProfileSchema,
    DivisionProfileUpdate,
)

config = CRUDConfig(
    model=DivisionProfile,
    schema=DivisionProfileSchema,
    schema_create=DivisionProfileCreate,
    schema_update=DivisionProfileUpdate,
    prefix="/divisions",
    entity_name="Division profile",
    tags=["divisions"],
    to_schema=lambda d: DivisionProfileSchema(
        id=d.id,
        name=d.name,
        status=d.status or "not_engaged",
        current_tools=d.current_tools,
        pain_points=d.pain_points,
        key_contact=d.key_contact,
        notes=d.notes,
    ),
    ordering=[("name", "asc")],
)

router = create_crud_router(config)
