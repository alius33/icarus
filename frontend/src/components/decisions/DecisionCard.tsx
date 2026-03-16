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
        bg-white dark:bg-forest-800 border border-forest-200 dark:border-forest-700
        rounded-lg p-3 cursor-pointer hover:shadow-md transition-shadow
        ${isDragging ? "shadow-lg ring-2 ring-forest-400" : ""}
      `}
    >
      {/* Top row: identifier + status badge */}
      <div className="flex items-center justify-between mb-1">
        <span className="text-sm font-mono text-forest-300">Decision #{decision.number}</span>
        <span className={`text-sm font-medium px-1.5 py-0.5 rounded ${statusCfg.bgColor} ${statusCfg.color}`}>
          {statusCfg.label}
        </span>
      </div>

      {/* Title */}
      <p className="text-base font-medium text-forest-950 dark:text-forest-50 line-clamp-2 mb-2">
        {decision.title}
      </p>

      {/* Key people tags */}
      {decision.key_people.length > 0 && (
        <div className="flex flex-wrap gap-1 mb-2">
          {decision.key_people.slice(0, 3).map((person) => (
            <span
              key={person}
              className="px-1.5 py-0.5 text-sm rounded bg-forest-100 dark:bg-forest-900/30 text-forest-600 dark:text-forest-200"
            >
              {person}
            </span>
          ))}
          {decision.key_people.length > 3 && (
            <span className="px-1.5 py-0.5 text-sm text-forest-300">
              +{decision.key_people.length - 3}
            </span>
          )}
        </div>
      )}

      {/* Bottom row: date, project */}
      <div className="flex items-center gap-3 text-sm text-forest-400 dark:text-forest-300">
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

      {/* Project badge */}
      {decision.project_name && (
        <div className="mt-2 text-sm text-forest-300 truncate">
          {decision.project_name}
        </div>
      )}
    </div>
  );
}
