"""
Board (kanban) and timeline endpoint mixins.

Adds reusable /board and /timeline and /position endpoints to any router
for entities that support drag-and-drop kanban boards.

Usage:
    from app.routers.board_mixin import BoardConfig, add_board_routes

    board_cfg = BoardConfig(
        model=Decision,
        schema=DecisionSchema,
        to_schema=_decision_schema,
        status_field="execution_status",
        status_values=["made", "in_progress", "implemented"],
        status_config={
            "made": {"label": "Made", "color": "blue", "order": 0},
            ...
        },
        entity_name="Decision",
        items_key="decisions",
    )
    add_board_routes(router, board_cfg, prefix="/decisions")
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Callable, Awaitable

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.exceptions import NotFoundError
from app.models.project_link import ProjectLink


async def _maybe_await(result):
    if hasattr(result, "__await__"):
        return await result
    return result


# ── Board configuration ──────────────────────────────────────────────

@dataclass
class BoardConfig:
    model: Any
    schema: type[BaseModel]
    to_schema: Callable[..., Any]
    # The ORM column name that holds the status
    status_field: str
    # Ordered list of status values
    status_values: list[str]
    # Config dict: status -> {label, color, order}
    status_config: dict[str, dict[str, Any]]
    entity_name: str
    # Key name for items list in board column response (e.g. "decisions", "tasks")
    items_key: str
    # Whether to use ProjectLink for project_id filtering
    uses_project_links: bool = False
    # entity_type for ProjectLink queries
    project_link_entity_type: str = ""
    # Optional callback on position/status change for writeback
    on_position_change: Callable[..., None] | None = None


class PositionUpdate(BaseModel):
    status: str
    position: int


class BoardColumn(BaseModel):
    status: str
    label: str
    color: str
    order: int
    items: list[Any]
    count: int


class BoardResponse(BaseModel):
    columns: list[dict[str, Any]]
    total: int


# ── Add board routes ─────────────────────────────────────────────────

def add_board_routes(
    router: APIRouter,
    cfg: BoardConfig,
    prefix: str,
) -> None:
    """Add GET /board and PATCH /{id}/position endpoints to router."""

    async def get_board(
        project_id: int | None = Query(None),
        db: AsyncSession = Depends(get_db),
    ):
        model = cfg.model
        status_col = getattr(model, cfg.status_field)

        query = select(model).order_by(model.position, model.id)

        if project_id is not None and cfg.uses_project_links:
            linked_ids = select(ProjectLink.entity_id).where(
                ProjectLink.project_id == project_id,
                ProjectLink.entity_type == cfg.project_link_entity_type,
            )
            query = query.where(model.id.in_(linked_ids))
        elif project_id is not None and hasattr(model, "project_id"):
            query = query.where(model.project_id == project_id)

        result = await db.execute(query)
        rows = result.scalars().all()

        columns_map: dict[str, list] = {s: [] for s in cfg.status_values}
        for item in rows:
            status = getattr(item, cfg.status_field) or cfg.status_values[0]
            bucket = status if status in columns_map else cfg.status_values[0]
            schema = await _maybe_await(cfg.to_schema(item))
            columns_map[bucket].append(schema)

        columns = []
        total = 0
        for status in cfg.status_values:
            sc = cfg.status_config.get(status, {"label": status, "color": "gray", "order": 99})
            items = columns_map[status]
            total += len(items)
            col = {
                "status": status,
                "label": sc["label"],
                "color": sc["color"],
                "order": sc["order"],
                cfg.items_key: items,
                "count": len(items),
            }
            columns.append(col)

        return {"columns": columns, "total": total}

    router.add_api_route(
        f"{prefix}/board",
        get_board,
        methods=["GET"],
    )

    async def update_position(
        item_id: int,
        body: PositionUpdate,
        db: AsyncSession = Depends(get_db),
    ):
        result = await db.execute(
            select(cfg.model).where(cfg.model.id == item_id)
        )
        item = result.scalar_one_or_none()
        if not item:
            raise NotFoundError(cfg.entity_name, item_id)

        old_status = getattr(item, cfg.status_field)
        setattr(item, cfg.status_field, body.status)
        item.position = body.position
        if hasattr(item, "is_manual"):
            item.is_manual = True
        if hasattr(item, "updated_at"):
            item.updated_at = datetime.utcnow()

        await db.commit()
        await db.refresh(item)

        if cfg.on_position_change and body.status != old_status:
            cfg.on_position_change(item, old_status, body.status)

        return await _maybe_await(cfg.to_schema(item))

    router.add_api_route(
        f"{prefix}/{{item_id}}/position",
        update_position,
        methods=["PATCH"],
        response_model=cfg.schema,
    )
