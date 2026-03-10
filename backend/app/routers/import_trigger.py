import asyncio
import logging

from fastapi import APIRouter, BackgroundTasks

from app.config import settings

logger = logging.getLogger("icarus.import")

router = APIRouter(tags=["import"])


async def _run_import():
    """Run the import script as a subprocess."""
    logger.info("Starting background import from %s", settings.DATA_ROOT)
    try:
        proc = await asyncio.create_subprocess_exec(
            "python", "-m", "scripts.import_data",
            "--data-root", settings.DATA_ROOT,
            "--db-url", settings.SYNC_DATABASE_URL,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await proc.communicate()
        if proc.returncode == 0:
            logger.info("Import completed successfully")
        else:
            logger.error("Import failed (exit %d): %s", proc.returncode, stderr.decode()[:500])
    except Exception as e:
        logger.error("Import process error: %s", e)


@router.post("/import/trigger")
async def trigger_import(background_tasks: BackgroundTasks):
    """Trigger a background re-import of markdown files into the database."""
    background_tasks.add_task(_run_import)
    return {"status": "triggered", "message": "Import started in background"}
