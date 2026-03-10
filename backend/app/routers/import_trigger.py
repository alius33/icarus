from fastapi import APIRouter

router = APIRouter(tags=["import"])


@router.post("/import/trigger")
async def trigger_import():
    """Placeholder endpoint that will eventually call the import script."""
    return {"status": "triggered"}
