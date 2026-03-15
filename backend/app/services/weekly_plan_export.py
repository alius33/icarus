"""Auto-export weekly plans to seed JSON file.

After any weekly plan CRUD operation, this service exports all plans
from the database to backend/scripts/seed_data/weekly_plans.json.
This ensures the seed file is always up to date when the user commits
and pushes to GitHub, so Railway's import_data.py picks up the plans.
"""

import json
import logging
from pathlib import Path

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.weekly_plan import WeeklyPlan

logger = logging.getLogger("icarus.weekly_plan_export")


def _find_seed_path() -> Path | None:
    """Find the writable seed data directory.

    Tries paths in order:
    1. /app/scripts/seed_data/ — Docker RW mount (./backend/scripts:/app/scripts)
    2. Relative to this file: ../../scripts/seed_data/ — fallback for direct runs
    """
    candidates = [
        Path("/app/scripts/seed_data"),
        Path(__file__).resolve().parents[2] / "scripts" / "seed_data",
    ]
    for candidate in candidates:
        if candidate.exists() and candidate.is_dir():
            return candidate / "weekly_plans.json"
    # Try creating the directory in the first writable candidate
    for candidate in candidates:
        try:
            candidate.mkdir(parents=True, exist_ok=True)
            return candidate / "weekly_plans.json"
        except OSError:
            continue
    return None


def _serialize_plan(plan: WeeklyPlan) -> dict:
    """Serialize a WeeklyPlan with actions and snapshots to dict."""
    actions = sorted(plan.actions, key=lambda a: (a.category, a.position)) if plan.actions else []
    snapshots = list(plan.snapshots) if plan.snapshots else []

    return {
        "week_number": plan.week_number,
        "week_start_date": str(plan.week_start_date),
        "week_end_date": str(plan.week_end_date),
        "deliverable_progress_summary": plan.deliverable_progress_summary,
        "programme_actions_summary": plan.programme_actions_summary,
        "status": plan.status,
        "actions": [
            {
                "category": a.category,
                "title": a.title,
                "description": a.description,
                "priority": a.priority,
                "owner": a.owner,
                "status": a.status,
                "deliverable_id": a.deliverable_id,
                "position": a.position,
                "is_ai_generated": a.is_ai_generated,
                "carried_from_week": a.carried_from_week,
            }
            for a in actions
        ],
        "snapshots": [
            {
                "deliverable_id": s.deliverable_id,
                "week_number": s.week_number,
                "rag_status": s.rag_status,
                "progress_percent": s.progress_percent,
                "milestones_completed": s.milestones_completed,
                "milestones_total": s.milestones_total,
                "narrative": s.narrative,
            }
            for s in snapshots
        ],
    }


async def export_plans_to_seed(session: AsyncSession) -> bool:
    """Export all weekly plans from DB to the seed JSON file.

    Returns True if the file was written, False otherwise.
    Fails gracefully — never raises.
    """
    try:
        seed_path = _find_seed_path()
        if not seed_path:
            logger.debug("No writable seed path found, skipping export")
            return False

        result = await session.execute(
            select(WeeklyPlan)
            .options(
                selectinload(WeeklyPlan.actions),
                selectinload(WeeklyPlan.snapshots),
            )
            .order_by(WeeklyPlan.week_number)
        )
        plans = result.scalars().all()

        if not plans:
            logger.debug("No weekly plans to export")
            return False

        data = [_serialize_plan(p) for p in plans]
        seed_path.write_text(json.dumps(data, indent=2), encoding="utf-8")
        logger.info(f"Exported {len(data)} weekly plan(s) to {seed_path}")
        return True

    except Exception as e:
        logger.warning(f"Failed to export weekly plans to seed: {e}")
        return False
