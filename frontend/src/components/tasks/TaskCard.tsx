"use client";

import { TaskSchema, PRIORITY_CONFIG, TaskPriority } from "@/lib/types";
import { isOverdue } from "@/lib/utils";
import { useSortable } from "@dnd-kit/sortable";
import { CSS } from "@dnd-kit/utilities";
import { Calendar, User, Hash } from "lucide-react";

interface TaskCardProps {
  task: TaskSchema;
  onClick: (task: TaskSchema) => void;
  isDragging?: boolean;
}

export default function TaskCard({ task, onClick, isDragging }: TaskCardProps) {
  const {
    attributes,
    listeners,
    setNodeRef,
    transform,
    transition,
    isDragging: isSortableDragging,
  } = useSortable({ id: task.id });

  const style = {
    transform: CSS.Transform.toString(transform),
    transition,
    opacity: isSortableDragging ? 0.5 : 1,
  };

  const priorityCfg = PRIORITY_CONFIG[task.priority as TaskPriority] ?? PRIORITY_CONFIG.NONE;
  const overdue = isOverdue(task.due_date) && task.status !== "DONE" && task.status !== "CANCELLED";

  return (
    <div
      ref={setNodeRef}
      style={style}
      {...attributes}
      {...listeners}
      onClick={() => onClick(task)}
      className={`
        bg-white dark:bg-forest-800 border border-forest-200 dark:border-forest-700
        rounded-lg p-3 cursor-pointer hover:shadow-md transition-shadow
        ${isDragging ? "shadow-lg ring-2 ring-forest-400" : ""}
      `}
    >
      {/* Top row: identifier + priority */}
      <div className="flex items-center justify-between mb-1">
        <span className="text-sm font-mono text-forest-300">{task.identifier}</span>
        {task.priority !== "NONE" && (
          <span className={`w-2 h-2 rounded-full ${priorityCfg.dotColor}`} title={priorityCfg.label} />
        )}
      </div>

      {/* Title */}
      <p className="text-base font-medium text-forest-950 dark:text-forest-50 line-clamp-2 mb-2">
        {task.title}
      </p>

      {/* Labels */}
      {task.labels.length > 0 && (
        <div className="flex flex-wrap gap-1 mb-2">
          {task.labels.slice(0, 3).map((label) => (
            <span
              key={label}
              className="px-1.5 py-0.5 text-sm rounded bg-forest-100 dark:bg-forest-900/30 text-forest-600 dark:text-forest-200"
            >
              {label}
            </span>
          ))}
          {task.labels.length > 3 && (
            <span className="px-1.5 py-0.5 text-sm text-forest-300">
              +{task.labels.length - 3}
            </span>
          )}
        </div>
      )}

      {/* Bottom row: assignee, due date, sub-tasks */}
      <div className="flex items-center gap-3 text-sm text-forest-400 dark:text-forest-300">
        {task.assignee && (
          <span className="flex items-center gap-1 truncate">
            <User className="h-3 w-3" />
            {task.assignee}
          </span>
        )}
        {task.due_date && (
          <span className={`flex items-center gap-1 ${overdue ? "text-red-500 font-medium" : ""}`}>
            <Calendar className="h-3 w-3" />
            {new Date(task.due_date).toLocaleDateString("en-GB", { day: "numeric", month: "short" })}
          </span>
        )}
        {task.sub_task_count > 0 && (
          <span className="flex items-center gap-1">
            <Hash className="h-3 w-3" />
            {task.sub_task_count}
          </span>
        )}
      </div>

      {/* Project badge */}
      {task.project_name && (
        <div className="mt-2 text-sm text-forest-300 truncate">
          {task.project_name}
        </div>
      )}
    </div>
  );
}
