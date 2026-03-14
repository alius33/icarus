"use client";

import { useState, useRef } from "react";
import { DecisionSchema, DecisionBoardColumn, DecisionBoardResponse, DECISION_STATUS_CONFIG, DecisionStatus } from "@/lib/types";
import DecisionCard from "./DecisionCard";
import { api } from "@/lib/api";
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

interface DecisionBoardProps {
  data: DecisionBoardResponse;
  onDecisionClick: (decision: DecisionSchema) => void;
  onRefresh: () => void;
}

function DroppableColumn({
  column,
  onDecisionClick,
  collapsedColumns,
  toggleCollapse,
}: {
  column: DecisionBoardColumn;
  onDecisionClick: (decision: DecisionSchema) => void;
  collapsedColumns: Set<string>;
  toggleCollapse: (status: string) => void;
}) {
  const { setNodeRef, isOver } = useDroppable({ id: column.status });
  const collapsed = collapsedColumns.has(column.status);
  const cfg = DECISION_STATUS_CONFIG[column.status as DecisionStatus] ?? { label: column.label, color: "text-gray-600", bgColor: "bg-gray-100" };

  return (
    <div
      ref={setNodeRef}
      className={`
        flex flex-col min-w-[280px] max-w-[320px] bg-gray-50 dark:bg-gray-800/50
        rounded-lg border border-gray-200 dark:border-gray-700
        ${isOver ? "ring-2 ring-blue-400" : ""}
      `}
    >
      {/* Column header */}
      <button
        onClick={() => toggleCollapse(column.status)}
        className="flex items-center gap-2 px-3 py-2.5 border-b border-gray-200 dark:border-gray-700"
      >
        {collapsed ? <ChevronRight className="h-4 w-4 text-gray-400" /> : <ChevronDown className="h-4 w-4 text-gray-400" />}
        <span className={`text-base font-semibold ${cfg.color}`}>{cfg.label}</span>
        <span className="ml-auto text-sm text-gray-400 bg-gray-200 dark:bg-gray-700 px-1.5 py-0.5 rounded-full">
          {column.count}
        </span>
      </button>

      {/* Decisions */}
      {!collapsed && (
        <div className="flex-1 p-2 space-y-2 overflow-y-auto max-h-[calc(100vh-240px)]">
          <SortableContext items={column.decisions.map((d) => d.id)} strategy={verticalListSortingStrategy}>
            {column.decisions.map((decision) => (
              <DecisionCard key={decision.id} decision={decision} onClick={onDecisionClick} />
            ))}
          </SortableContext>
          {column.decisions.length === 0 && (
            <p className="text-sm text-gray-400 text-center py-4">No decisions</p>
          )}
        </div>
      )}
    </div>
  );
}

export default function DecisionBoard({ data, onDecisionClick, onRefresh }: DecisionBoardProps) {
  const [columns, setColumns] = useState(data.columns);
  const [activeDecision, setActiveDecision] = useState<DecisionSchema | null>(null);
  const [collapsedColumns, setCollapsedColumns] = useState<Set<string>>(new Set());
  const prevDataRef = useRef(data);

  // Sync only when parent passes genuinely new data (after a fetch),
  // not when local columns diverge from the prop due to drag-and-drop.
  if (data !== prevDataRef.current && !activeDecision) {
    setColumns(data.columns);
    prevDataRef.current = data;
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

  function findDecision(id: number): DecisionSchema | undefined {
    for (const col of columns) {
      const d = col.decisions.find((d) => d.id === id);
      if (d) return d;
    }
    return undefined;
  }

  function findColumnByDecisionId(decisionId: number): string | undefined {
    for (const col of columns) {
      if (col.decisions.some((d) => d.id === decisionId)) return col.status;
    }
    return undefined;
  }

  function handleDragStart(event: DragStartEvent) {
    const decision = findDecision(event.active.id as number);
    setActiveDecision(decision || null);
  }

  function handleDragOver(event: DragOverEvent) {
    const { active, over } = event;
    if (!over) return;

    const activeColStatus = findColumnByDecisionId(active.id as number);
    // Determine target column: either a column id (status string) or another decision's column
    let overColStatus = columns.find((c) => c.status === over.id)?.status;
    if (!overColStatus) {
      overColStatus = findColumnByDecisionId(over.id as number);
    }

    if (!activeColStatus || !overColStatus || activeColStatus === overColStatus) return;

    // Move decision between columns optimistically
    setColumns((prev) => {
      const next = prev.map((col) => ({ ...col, decisions: [...col.decisions] }));
      const srcCol = next.find((c) => c.status === activeColStatus)!;
      const destCol = next.find((c) => c.status === overColStatus)!;
      const decisionIdx = srcCol.decisions.findIndex((d) => d.id === active.id);
      if (decisionIdx === -1) return prev;
      const [decision] = srcCol.decisions.splice(decisionIdx, 1);
      srcCol.count = srcCol.decisions.length;
      destCol.decisions.push({ ...decision, execution_status: destCol.status });
      destCol.count = destCol.decisions.length;
      return next;
    });
  }

  async function handleDragEnd(event: DragEndEvent) {
    const { active, over } = event;
    setActiveDecision(null);

    if (!over) return;

    const colStatus = findColumnByDecisionId(active.id as number);
    if (!colStatus) return;

    const col = columns.find((c) => c.status === colStatus);
    if (!col) return;

    const position = col.decisions.findIndex((d) => d.id === active.id);

    try {
      await api.updateDecisionPosition(active.id as number, { execution_status: colStatus, position });
      onRefresh(); // Sync parent with server state
    } catch {
      onRefresh(); // Revert on error
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
            onDecisionClick={onDecisionClick}
            collapsedColumns={collapsedColumns}
            toggleCollapse={toggleCollapse}
          />
        ))}
      </div>

      <DragOverlay>
        {activeDecision && (
          <div className="w-[300px]">
            <DecisionCard decision={activeDecision} onClick={() => {}} isDragging />
          </div>
        )}
      </DragOverlay>
    </DndContext>
  );
}
