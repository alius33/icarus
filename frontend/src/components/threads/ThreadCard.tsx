"use client";

import { OpenThreadSchema, SEVERITY_CONFIG, ThreadSeverity } from "@/lib/types";
import { useSortable } from "@dnd-kit/sortable";
import { CSS } from "@dnd-kit/utilities";
import { Calendar } from "lucide-react";

interface ThreadCardProps {
  thread: OpenThreadSchema;
  onClick: (thread: OpenThreadSchema) => void;
  isDragging?: boolean;
}

function trendIndicator(trend: string | null): string {
  if (!trend) return "";
  if (trend === "escalating") return "\u2191";
  if (trend === "stable") return "\u2192";
  if (trend === "de-escalating") return "\u2193";
  return "";
}

function trendColor(trend: string | null): string {
  if (!trend) return "text-gray-400";
  if (trend === "escalating") return "text-red-500";
  if (trend === "stable") return "text-yellow-500";
  if (trend === "de-escalating") return "text-green-500";
  return "text-gray-400";
}

export default function ThreadCard({ thread, onClick, isDragging }: ThreadCardProps) {
  const {
    attributes,
    listeners,
    setNodeRef,
    transform,
    transition,
    isDragging: isSortableDragging,
  } = useSortable({ id: thread.id });

  const style = {
    transform: CSS.Transform.toString(transform),
    transition,
    opacity: isSortableDragging ? 0.5 : 1,
  };

  const severityCfg = SEVERITY_CONFIG[thread.severity as ThreadSeverity] ?? null;
  const trend = thread.trend;

  return (
    <div
      ref={setNodeRef}
      style={style}
      {...attributes}
      {...listeners}
      onClick={() => onClick(thread)}
      className={`
        bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700
        rounded-lg p-3 cursor-pointer hover:shadow-md transition-shadow
        ${isDragging ? "shadow-lg ring-2 ring-blue-400" : ""}
      `}
    >
      {/* Top row: severity dot + trend */}
      <div className="flex items-center justify-between mb-1">
        <div className="flex items-center gap-1.5">
          {severityCfg && (
            <span className={`w-2 h-2 rounded-full ${severityCfg.dotColor}`} title={severityCfg.label} />
          )}
          {severityCfg && (
            <span className={`text-sm ${severityCfg.color}`}>{severityCfg.label}</span>
          )}
        </div>
        {trend && (
          <span className={`text-base font-medium ${trendColor(trend)}`} title={trend}>
            {trendIndicator(trend)}
          </span>
        )}
      </div>

      {/* Title */}
      <p className="text-base font-medium text-gray-900 dark:text-gray-100 line-clamp-2 mb-2">
        {thread.title}
      </p>

      {/* Description snippet */}
      {thread.description && (
        <p className="text-sm text-gray-500 dark:text-gray-400 line-clamp-2 mb-2">
          {thread.description.length > 80
            ? thread.description.slice(0, 80) + "..."
            : thread.description}
        </p>
      )}

      {/* Bottom row: opened date */}
      <div className="flex items-center gap-3 text-sm text-gray-500 dark:text-gray-400">
        {thread.opened_date && (
          <span className="flex items-center gap-1">
            <Calendar className="h-3 w-3" />
            {new Date(thread.opened_date).toLocaleDateString("en-GB", { day: "numeric", month: "short" })}
          </span>
        )}
      </div>
    </div>
  );
}
