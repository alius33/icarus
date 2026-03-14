"use client";

import { DecisionSchema, DECISION_STATUS_CONFIG, DecisionStatus } from "@/lib/types";
import { useSortable } from "@dnd-kit/sortable";
import { CSS } from "@dnd-kit/utilities";
import { Calendar, Users } from "lucide-react";

interface DecisionCardProps {
  decision: DecisionSchema;
  onClick: (decision: DecisionSchema) => void;
  isDragging?: boolean;
}

export default function DecisionCard({ decision, onClick, isDragging }: DecisionCardProps) {
  const {
    attributes,
    listeners,
    setNodeRef,
    transform,
    transition,
    isDragging: isSortableDragging,
  } = useSortable({ id: decision.id });

  const style = {
    transform: CSS.Transform.toString(transform),
    transition,
    opacity: isSortableDragging ? 0.5 : 1,
  };

  const statusCfg = DECISION_STATUS_CONFIG[decision.execution_status as DecisionStatus] ?? DECISION_STATUS_CONFIG.made;

  return (
    <div
      ref={setNodeRef}
      style={style}
      {...attributes}
      {...listeners}
      onClick={() => onClick(decision)}
      className={`
        bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700
        rounded-lg p-3 cursor-pointer hover:shadow-md transition-shadow
        ${isDragging ? "shadow-lg ring-2 ring-blue-400" : ""}
      `}
    >
      {/* Top row: identifier + status badge */}
      <div className="flex items-center justify-between mb-1">
        <span className="text-sm font-mono text-gray-400">Decision #{decision.number}</span>
        <span className={`text-sm font-medium px-1.5 py-0.5 rounded ${statusCfg.bgColor} ${statusCfg.color}`}>
          {statusCfg.label}
        </span>
      </div>

      {/* Title */}
      <p className="text-base font-medium text-gray-900 dark:text-gray-100 line-clamp-2 mb-2">
        {decision.title}
      </p>

      {/* Key people tags */}
      {decision.key_people.length > 0 && (
        <div className="flex flex-wrap gap-1 mb-2">
          {decision.key_people.slice(0, 3).map((person) => (
            <span
              key={person}
              className="px-1.5 py-0.5 text-sm rounded bg-blue-50 dark:bg-blue-900/30 text-blue-700 dark:text-blue-300"
            >
              {person}
            </span>
          ))}
          {decision.key_people.length > 3 && (
            <span className="px-1.5 py-0.5 text-sm text-gray-400">
              +{decision.key_people.length - 3}
            </span>
          )}
        </div>
      )}

      {/* Bottom row: date, workstream */}
      <div className="flex items-center gap-3 text-sm text-gray-500 dark:text-gray-400">
        {decision.date && (
          <span className="flex items-center gap-1">
            <Calendar className="h-3 w-3" />
            {new Date(decision.date).toLocaleDateString("en-GB", { day: "numeric", month: "short" })}
          </span>
        )}
        {decision.key_people.length > 0 && (
          <span className="flex items-center gap-1">
            <Users className="h-3 w-3" />
            {decision.key_people.length}
          </span>
        )}
      </div>

      {/* Workstream badge */}
      {decision.workstream && (
        <div className="mt-2 text-sm text-gray-400 truncate">
          {decision.workstream}
        </div>
      )}
    </div>
  );
}
