"use client";

import { useState, ReactNode } from "react";
import {
  DndContext,
  DragOverlay,
  closestCorners,
  PointerSensor,
  useSensor,
  useSensors,
  DragStartEvent,
  DragEndEvent,
  DragOverEvent,
} from "@dnd-kit/core";
import {
  SortableContext,
  verticalListSortingStrategy,
} from "@dnd-kit/sortable";
import { useDroppable } from "@dnd-kit/core";
import { ChevronDown, ChevronRight } from "lucide-react";

// ── Types ────────────────────────────────────────────────────────────

export interface BoardColumn<T> {
  status: string;
  label: string;
  color: string;
  order: number;
  items: T[];
  count: number;
}

export interface StatusConfig {
  label: string;
  color: string;
  bgColor: string;
}

export interface GenericBoardProps<T extends { id: number }> {
  /** Board columns with items */
  columns: BoardColumn<T>[];
  /** Status config for column header styling */
  statusConfig: Record<string, StatusConfig>;
  /** Entity name for empty state text (e.g. "decisions") */
  entityName: string;
  /** Render a card for each item */
  renderCard: (item: T, onClick: (item: T) => void) => ReactNode;
  /** Render the drag overlay card */
  renderDragOverlay: (item: T) => ReactNode;
  /** Called when an item is clicked */
  onItemClick: (item: T) => void;
  /** Update position API call */
  updatePosition: (id: number, status: string, position: number) => Promise<void>;
  /** Refresh data on error */
  onRefresh: () => void;
}

// ── Droppable Column ─────────────────────────────────────────────────

function DroppableColumn<T extends { id: number }>({
  column,
  statusConfig,
  entityName,
  renderCard,
  onItemClick,
  collapsedColumns,
  toggleCollapse,
}: {
  column: BoardColumn<T>;
  statusConfig: Record<string, StatusConfig>;
  entityName: string;
  renderCard: (item: T, onClick: (item: T) => void) => ReactNode;
  onItemClick: (item: T) => void;
  collapsedColumns: Set<string>;
  toggleCollapse: (status: string) => void;
}) {
  const { setNodeRef, isOver } = useDroppable({ id: column.status });
  const collapsed = collapsedColumns.has(column.status);
  const cfg = statusConfig[column.status] ?? {
    label: column.label,
    color: "text-gray-600",
    bgColor: "bg-gray-100",
  };

  return (
    <div
      ref={setNodeRef}
      className={`
        flex flex-col min-w-[280px] max-w-[320px] bg-gray-50 dark:bg-gray-800/50
        rounded-lg border border-gray-200 dark:border-gray-700
        ${isOver ? "ring-2 ring-blue-400" : ""}
      `}
    >
      <button
        onClick={() => toggleCollapse(column.status)}
        className="flex items-center gap-2 px-3 py-2.5 border-b border-gray-200 dark:border-gray-700"
      >
        {collapsed ? (
          <ChevronRight className="h-4 w-4 text-gray-400" />
        ) : (
          <ChevronDown className="h-4 w-4 text-gray-400" />
        )}
        <span className={`text-sm font-semibold ${cfg.color}`}>{cfg.label}</span>
        <span className="ml-auto text-xs text-gray-400 bg-gray-200 dark:bg-gray-700 px-1.5 py-0.5 rounded-full">
          {column.count}
        </span>
      </button>

      {!collapsed && (
        <div className="flex-1 p-2 space-y-2 overflow-y-auto max-h-[calc(100vh-240px)]">
          <SortableContext
            items={column.items.map((item) => item.id)}
            strategy={verticalListSortingStrategy}
          >
            {column.items.map((item) => renderCard(item, onItemClick))}
          </SortableContext>
          {column.items.length === 0 && (
            <p className="text-xs text-gray-400 text-center py-4">
              No {entityName}
            </p>
          )}
        </div>
      )}
    </div>
  );
}

// ── Generic Board ────────────────────────────────────────────────────

export default function GenericBoard<T extends { id: number }>({
  columns: initialColumns,
  statusConfig,
  entityName,
  renderCard,
  renderDragOverlay,
  onItemClick,
  updatePosition,
  onRefresh,
}: GenericBoardProps<T>) {
  const [columns, setColumns] = useState(initialColumns);
  const [activeItem, setActiveItem] = useState<T | null>(null);
  const [collapsedColumns, setCollapsedColumns] = useState<Set<string>>(new Set());

  // Sync with new data when not dragging
  if (initialColumns !== columns && !activeItem) {
    setColumns(initialColumns);
  }

  const sensors = useSensors(
    useSensor(PointerSensor, { activationConstraint: { distance: 5 } })
  );

  function toggleCollapse(status: string) {
    setCollapsedColumns((prev) => {
      const next = new Set(prev);
      if (next.has(status)) next.delete(status);
      else next.add(status);
      return next;
    });
  }

  function findItem(id: number): T | undefined {
    for (const col of columns) {
      const item = col.items.find((item) => item.id === id);
      if (item) return item;
    }
    return undefined;
  }

  function findColumnByItemId(itemId: number): string | undefined {
    for (const col of columns) {
      if (col.items.some((item) => item.id === itemId)) return col.status;
    }
    return undefined;
  }

  function handleDragStart(event: DragStartEvent) {
    setActiveItem(findItem(event.active.id as number) || null);
  }

  function handleDragOver(event: DragOverEvent) {
    const { active, over } = event;
    if (!over) return;

    const activeColStatus = findColumnByItemId(active.id as number);
    let overColStatus = columns.find((c) => c.status === over.id)?.status;
    if (!overColStatus) {
      overColStatus = findColumnByItemId(over.id as number);
    }

    if (!activeColStatus || !overColStatus || activeColStatus === overColStatus) return;

    setColumns((prev) => {
      const next = prev.map((col) => ({ ...col, items: [...col.items] }));
      const srcCol = next.find((c) => c.status === activeColStatus)!;
      const destCol = next.find((c) => c.status === overColStatus)!;
      const itemIdx = srcCol.items.findIndex((item) => item.id === active.id);
      if (itemIdx === -1) return prev;
      const [item] = srcCol.items.splice(itemIdx, 1);
      srcCol.count = srcCol.items.length;
      destCol.items.push(item);
      destCol.count = destCol.items.length;
      return next;
    });
  }

  async function handleDragEnd(event: DragEndEvent) {
    const { active, over } = event;
    setActiveItem(null);

    if (!over) return;

    const colStatus = findColumnByItemId(active.id as number);
    if (!colStatus) return;

    const col = columns.find((c) => c.status === colStatus);
    if (!col) return;

    const position = col.items.findIndex((item) => item.id === active.id);

    try {
      await updatePosition(active.id as number, colStatus, position);
    } catch {
      onRefresh();
    }
  }

  return (
    <DndContext
      sensors={sensors}
      collisionDetection={closestCorners}
      onDragStart={handleDragStart}
      onDragOver={handleDragOver}
      onDragEnd={handleDragEnd}
    >
      <div className="flex gap-4 overflow-x-auto pb-4">
        {columns.map((column) => (
          <DroppableColumn
            key={column.status}
            column={column}
            statusConfig={statusConfig}
            entityName={entityName}
            renderCard={renderCard}
            onItemClick={onItemClick}
            collapsedColumns={collapsedColumns}
            toggleCollapse={toggleCollapse}
          />
        ))}
      </div>

      <DragOverlay>
        {activeItem && <div className="w-[300px]">{renderDragOverlay(activeItem)}</div>}
      </DragOverlay>
    </DndContext>
  );
}
