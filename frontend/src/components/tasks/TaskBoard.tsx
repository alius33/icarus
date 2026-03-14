"use client";

import { useState, useRef } from "react";
import { TaskSchema, TaskBoardColumn, TaskBoardResponse, STATUS_CONFIG, TaskStatus } from "@/lib/types";
import TaskCard from "./TaskCard";
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

interface TaskBoardProps {
  data: TaskBoardResponse;
  onTaskClick: (task: TaskSchema) => void;
  onRefresh: () => void;
}

function DroppableColumn({
  column,
  onTaskClick,
  collapsedColumns,
  toggleCollapse,
}: {
  column: TaskBoardColumn;
  onTaskClick: (task: TaskSchema) => void;
  collapsedColumns: Set<string>;
  toggleCollapse: (status: string) => void;
}) {
  const { setNodeRef, isOver } = useDroppable({ id: column.status });
  const collapsed = collapsedColumns.has(column.status);
  const cfg = STATUS_CONFIG[column.status as TaskStatus] ?? { label: column.label, color: "text-gray-600", bgColor: "bg-gray-100" };

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

      {/* Tasks */}
      {!collapsed && (
        <div className="flex-1 p-2 space-y-2 overflow-y-auto max-h-[calc(100vh-240px)]">
          <SortableContext items={column.tasks.map((t) => t.id)} strategy={verticalListSortingStrategy}>
            {column.tasks.map((task) => (
              <TaskCard key={task.id} task={task} onClick={onTaskClick} />
            ))}
          </SortableContext>
          {column.tasks.length === 0 && (
            <p className="text-sm text-gray-400 text-center py-4">No tasks</p>
          )}
        </div>
      )}
    </div>
  );
}

export default function TaskBoard({ data, onTaskClick, onRefresh }: TaskBoardProps) {
  const [columns, setColumns] = useState(data.columns);
  const [activeTask, setActiveTask] = useState<TaskSchema | null>(null);
  const [collapsedColumns, setCollapsedColumns] = useState<Set<string>>(new Set());
  const prevDataRef = useRef(data);

  // Sync only when parent passes genuinely new data (after a fetch),
  // not when local columns diverge from the prop due to drag-and-drop.
  if (data !== prevDataRef.current && !activeTask) {
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

  function findTask(id: number): TaskSchema | undefined {
    for (const col of columns) {
      const t = col.tasks.find((t) => t.id === id);
      if (t) return t;
    }
    return undefined;
  }

  function findColumnByTaskId(taskId: number): string | undefined {
    for (const col of columns) {
      if (col.tasks.some((t) => t.id === taskId)) return col.status;
    }
    return undefined;
  }

  function handleDragStart(event: DragStartEvent) {
    const task = findTask(event.active.id as number);
    setActiveTask(task || null);
  }

  function handleDragOver(event: DragOverEvent) {
    const { active, over } = event;
    if (!over) return;

    const activeColStatus = findColumnByTaskId(active.id as number);
    // Determine target column: either a column id (status string) or another task's column
    let overColStatus = columns.find((c) => c.status === over.id)?.status;
    if (!overColStatus) {
      overColStatus = findColumnByTaskId(over.id as number);
    }

    if (!activeColStatus || !overColStatus || activeColStatus === overColStatus) return;

    // Move task between columns optimistically
    setColumns((prev) => {
      const next = prev.map((col) => ({ ...col, tasks: [...col.tasks] }));
      const srcCol = next.find((c) => c.status === activeColStatus)!;
      const destCol = next.find((c) => c.status === overColStatus)!;
      const taskIdx = srcCol.tasks.findIndex((t) => t.id === active.id);
      if (taskIdx === -1) return prev;
      const [task] = srcCol.tasks.splice(taskIdx, 1);
      srcCol.count = srcCol.tasks.length;
      destCol.tasks.push({ ...task, status: destCol.status as TaskSchema["status"] });
      destCol.count = destCol.tasks.length;
      return next;
    });
  }

  async function handleDragEnd(event: DragEndEvent) {
    const { active, over } = event;
    setActiveTask(null);

    if (!over) return;

    const colStatus = findColumnByTaskId(active.id as number);
    if (!colStatus) return;

    const col = columns.find((c) => c.status === colStatus);
    if (!col) return;

    const position = col.tasks.findIndex((t) => t.id === active.id);

    try {
      await api.updateTaskPosition(active.id as number, { status: colStatus, position });
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
            onTaskClick={onTaskClick}
            collapsedColumns={collapsedColumns}
            toggleCollapse={toggleCollapse}
          />
        ))}
      </div>

      <DragOverlay>
        {activeTask && (
          <div className="w-[300px]">
            <TaskCard task={activeTask} onClick={() => {}} isDragging />
          </div>
        )}
      </DragOverlay>
    </DndContext>
  );
}
