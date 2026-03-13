"""
Auto-import watcher: periodically checks for new or changed summary files
and triggers a re-import so the web app always shows up-to-date data.

This runs as a background task during the FastAPI lifespan, checking every
30 seconds. It compares file modification times against the last import
timestamp to detect changes efficiently — no full re-scan unless needed.
"""

import asyncio
import logging
from pathlib import Path

from app.config import settings

logger = logging.getLogger("icarus.auto_import")

# Track state across checks
_last_snapshot: dict[str, float] = {}  # filename -> mtime
_import_lock = asyncio.Lock()


def _snapshot_summaries(data_root: Path) -> dict[str, float]:
    """Build a dict of {filename: mtime} for all summary .md files."""
    summaries_dir = data_root / "analysis" / "summaries"
    if not summaries_dir.exists():
        return {}
    result = {}
    for f in summaries_dir.glob("*.md"):
        try:
            result[f.name] = f.stat().st_mtime
        except OSError:
            pass
    return result


def _snapshot_all_watched(data_root: Path) -> dict[str, float]:
    """Build snapshot of all watched directories (summaries + weekly + trackers)."""
    result = {}
    watched_dirs = [
        data_root / "analysis" / "summaries",
        data_root / "analysis" / "weekly",
        data_root / "analysis" / "trackers",
        data_root / "context",
    ]
    for d in watched_dirs:
        if not d.exists():
            continue
        for f in d.glob("*.md"):
            try:
                result[str(f.relative_to(data_root))] = f.stat().st_mtime
            except OSError:
                pass
    return result


async def _run_import_subprocess():
    """Run the import script as a subprocess."""
    async with _import_lock:
        logger.info("Auto-import: detected changes, running import...")
        try:
            proc = await asyncio.create_subprocess_exec(
                "python", "-m", "scripts.import_data",
                "--data-root", settings.DATA_ROOT,
                "--db-url", settings.DATABASE_URL,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            stdout, stderr = await proc.communicate()
            if proc.returncode == 0:
                logger.info("Auto-import: completed successfully")
            else:
                logger.error(
                    "Auto-import: failed (exit %d): %s",
                    proc.returncode,
                    stderr.decode()[:500],
                )
        except Exception as e:
            logger.error("Auto-import: process error: %s", e)


async def auto_import_loop(check_interval: int = 30):
    """Background loop that checks for file changes and triggers import.

    Args:
        check_interval: Seconds between checks (default 30).
    """
    global _last_snapshot

    data_root = Path(settings.DATA_ROOT)

    # Wait a bit for the initial startup import to finish
    await asyncio.sleep(15)

    # Take initial snapshot (after startup import has run)
    _last_snapshot = _snapshot_all_watched(data_root)
    logger.info(
        "Auto-import watcher started: monitoring %d files, checking every %ds",
        len(_last_snapshot),
        check_interval,
    )

    while True:
        try:
            await asyncio.sleep(check_interval)

            current = _snapshot_all_watched(data_root)

            # Detect new or changed files
            changes = []
            for fname, mtime in current.items():
                old_mtime = _last_snapshot.get(fname)
                if old_mtime is None:
                    changes.append(f"  NEW: {fname}")
                elif mtime > old_mtime:
                    changes.append(f"  CHANGED: {fname}")

            if changes:
                logger.info(
                    "Auto-import: detected %d file change(s):\n%s",
                    len(changes),
                    "\n".join(changes[:20]),  # Cap log output
                )
                await _run_import_subprocess()
                # Re-snapshot after import
                _last_snapshot = _snapshot_all_watched(data_root)
            else:
                _last_snapshot = current

        except asyncio.CancelledError:
            logger.info("Auto-import watcher stopped")
            break
        except Exception as e:
            logger.error("Auto-import watcher error: %s", e)
            # Don't crash the loop on transient errors
            await asyncio.sleep(check_interval)
