"""
Generic CRUD router factory.

Eliminates boilerplate across 15+ routers by generating standard
list / get / create / update / delete endpoints from a configuration object.

Usage:
    from app.routers.crud_factory import CRUDConfig, create_crud_router

    config = CRUDConfig(
        model=MyModel,
        schema=MySchema,
        schema_create=MyCreate,
        schema_update=MyUpdate,
        prefix="/my-models",
        entity_name="My Model",
        tags=["my_models"],
        to_schema=lambda m: MySchema(...),
    )
    router = create_crud_router(config)
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Any, Callable, Awaitable

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel
from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.exceptions import NotFoundError
from app.models.deleted_import import DeletedImport


# ── Writeback hooks ──────────────────────────────────────────────────

@dataclass
class WritebackHooks:
    """Optional markdown writeback functions called on mutations."""

    on_create: Callable[..., None] | None = None
    on_update: Callable[..., None] | None = None
    on_delete: Callable[..., None] | None = None


# ── Main config ──────────────────────────────────────────────────────

@dataclass
class CRUDConfig:
    # ORM model class
    model: Any
    # Pydantic response schema
    schema: type[BaseModel]
    # Pydantic create body schema
    schema_create: type[BaseModel]
    # Pydantic update body schema
    schema_update: type[BaseModel]
    # URL prefix (e.g. "/commitments")
    prefix: str
    # Human-readable name for error messages (e.g. "Commitment")
    entity_name: str
    # Router tags
    tags: list[str]

    # Function: ORM instance -> schema. May be sync or async.
    to_schema: Callable[..., Any]
    # Function: (CreateBody, db) -> dict of ORM kwargs. If None, uses body.model_dump().
    create_to_orm: Callable[..., dict | Awaitable[dict]] | None = None

    # Search fields (ILIKE across these columns)
    search_fields: list[str] = field(default_factory=list)

    # Default ordering: list of (column_name, direction) tuples
    # direction is "asc" or "desc" or "desc_nullslast"
    ordering: list[tuple[str, str]] = field(default_factory=lambda: [("id", "desc")])

    # If True, track deletions of non-manual items in DeletedImport
    track_deletions: bool = False
    # entity_type string for DeletedImport
    deletion_entity_type: str = ""
    # Function: ORM instance -> unique_key string for DeletedImport
    deletion_key: Callable[..., str] | None = None

    # Markdown writeback hooks
    writeback: WritebackHooks | None = None

    # Date fields that need str -> date conversion on create/update
    date_fields: list[str] = field(default_factory=list)


# ── Helpers ──────────────────────────────────────────────────────────

def _parse_date(value: str | None) -> date | None:
    if not value:
        return None
    try:
        return date.fromisoformat(value)
    except ValueError:
        try:
            return datetime.strptime(value, "%Y-%m-%d").date()
        except ValueError:
            return None


def _apply_ordering(query, model, ordering: list[tuple[str, str]]):
    for col_name, direction in ordering:
        col = getattr(model, col_name, None)
        if col is None:
            continue
        if direction == "desc_nullslast":
            query = query.order_by(col.desc().nullslast())
        elif direction == "desc":
            query = query.order_by(col.desc())
        else:
            query = query.order_by(col.asc())
    return query


async def _maybe_await(result):
    """Await the result if it's a coroutine."""
    if hasattr(result, "__await__"):
        return await result
    return result


# ── Factory ──────────────────────────────────────────────────────────

def create_crud_router(cfg: CRUDConfig, router: APIRouter | None = None) -> APIRouter:
    """Generate a full CRUD router from a CRUDConfig.

    If `router` is provided, routes are added to it (useful when you need
    to register custom endpoints like /summary before the /{item_id} route).
    """

    if router is None:
        router = APIRouter(tags=cfg.tags)

    # ── LIST ──────────────────────────────────────────────────────

    async def list_items(
        search: str | None = Query(None),
        db: AsyncSession = Depends(get_db),
    ):
        query = select(cfg.model)

        if search and cfg.search_fields:
            pattern = f"%{search}%"
            clauses = [
                getattr(cfg.model, f).ilike(pattern)
                for f in cfg.search_fields
                if hasattr(cfg.model, f)
            ]
            if clauses:
                query = query.where(or_(*clauses))

        query = _apply_ordering(query, cfg.model, cfg.ordering)
        result = await db.execute(query)
        return [await _maybe_await(cfg.to_schema(item)) for item in result.scalars().all()]

    router.add_api_route(
        cfg.prefix,
        list_items,
        methods=["GET"],
        response_model=list[cfg.schema],
    )

    # ── GET DETAIL ────────────────────────────────────────────────

    async def get_item(item_id: int, db: AsyncSession = Depends(get_db)):
        result = await db.execute(
            select(cfg.model).where(cfg.model.id == item_id)
        )
        item = result.scalar_one_or_none()
        if not item:
            raise NotFoundError(cfg.entity_name, item_id)
        return await _maybe_await(cfg.to_schema(item))

    router.add_api_route(
        f"{cfg.prefix}/{{item_id}}",
        get_item,
        methods=["GET"],
        response_model=cfg.schema,
    )

    # ── CREATE ────────────────────────────────────────────────────

    async def create_item(body: cfg.schema_create, db: AsyncSession = Depends(get_db)):
        if cfg.create_to_orm:
            orm_kwargs = await _maybe_await(cfg.create_to_orm(body, db))
        else:
            orm_kwargs = body.model_dump()
            for df in cfg.date_fields:
                if df in orm_kwargs and isinstance(orm_kwargs[df], str):
                    orm_kwargs[df] = _parse_date(orm_kwargs[df])
            orm_kwargs["is_manual"] = True

        item = cfg.model(**orm_kwargs)
        db.add(item)
        await db.commit()
        await db.refresh(item)

        if cfg.writeback and cfg.writeback.on_create:
            cfg.writeback.on_create(item, body)

        return await _maybe_await(cfg.to_schema(item))

    router.add_api_route(
        cfg.prefix,
        create_item,
        methods=["POST"],
        response_model=cfg.schema,
        status_code=201,
    )

    # ── UPDATE ────────────────────────────────────────────────────

    async def update_item(
        item_id: int,
        body: cfg.schema_update,
        db: AsyncSession = Depends(get_db),
    ):
        result = await db.execute(
            select(cfg.model).where(cfg.model.id == item_id)
        )
        item = result.scalar_one_or_none()
        if not item:
            raise NotFoundError(cfg.entity_name, item_id)

        update_data = body.model_dump(exclude_unset=True)
        for field_name, value in update_data.items():
            if field_name in cfg.date_fields and isinstance(value, str):
                value = _parse_date(value)
            setattr(item, field_name, value)

        if hasattr(item, "is_manual"):
            item.is_manual = True
        if hasattr(item, "updated_at"):
            item.updated_at = datetime.utcnow()

        await db.commit()
        await db.refresh(item)

        if cfg.writeback and cfg.writeback.on_update:
            cfg.writeback.on_update(item, body)

        return await _maybe_await(cfg.to_schema(item))

    router.add_api_route(
        f"{cfg.prefix}/{{item_id}}",
        update_item,
        methods=["PATCH"],
        response_model=cfg.schema,
    )

    # ── DELETE ────────────────────────────────────────────────────

    async def delete_item(item_id: int, db: AsyncSession = Depends(get_db)):
        result = await db.execute(
            select(cfg.model).where(cfg.model.id == item_id)
        )
        item = result.scalar_one_or_none()
        if not item:
            raise NotFoundError(cfg.entity_name, item_id)

        if cfg.writeback and cfg.writeback.on_delete:
            cfg.writeback.on_delete(item)

        if cfg.track_deletions and hasattr(item, "is_manual") and not item.is_manual:
            key = cfg.deletion_key(item) if cfg.deletion_key else str(item.id)
            db.add(DeletedImport(
                entity_type=cfg.deletion_entity_type,
                unique_key=key,
            ))

        await db.delete(item)
        await db.commit()
        return {"ok": True}

    router.add_api_route(
        f"{cfg.prefix}/{{item_id}}",
        delete_item,
        methods=["DELETE"],
    )

    return router
