"use client";

import {
  ThreadViewMode,
  THREAD_STATUSES,
  THREAD_SEVERITIES,
  TREND_OPTIONS,
  THREAD_STATUS_CONFIG,
  SEVERITY_CONFIG,
  ThreadStatus,
  ThreadSeverity,
} from "@/lib/types";
import { KanbanSquare, List, Filter } from "lucide-react";
import { cn } from "@/lib/utils";

interface ThreadViewSwitcherProps {
  view: ThreadViewMode;
  onViewChange: (v: ThreadViewMode) => void;
  filters: {
    status: string;
    severity: string;
    trend: string;
  };
  onFilterChange: (key: string, value: string) => void;
  showFilters: boolean;
  onToggleFilters: () => void;
}

const views: { key: ThreadViewMode; icon: typeof KanbanSquare; label: string }[] = [
  { key: "board", icon: KanbanSquare, label: "Board" },
  { key: "list", icon: List, label: "List" },
];

export default function ThreadViewSwitcher({
  view,
  onViewChange,
  filters,
  onFilterChange,
  showFilters,
  onToggleFilters,
}: ThreadViewSwitcherProps) {
  return (
    <div className="space-y-3">
      {/* View toggle + filter button */}
      <div className="flex items-center justify-between">
        <div className="flex items-center bg-gray-100 dark:bg-gray-800 rounded-lg p-0.5">
          {views.map(({ key, icon: Icon, label }) => (
            <button
              key={key}
              onClick={() => onViewChange(key)}
              className={cn(
                "flex items-center gap-1.5 px-3 py-1.5 text-base font-medium rounded-md transition-colors",
                view === key
                  ? "bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 shadow-sm"
                  : "text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-300"
              )}
            >
              <Icon className="h-4 w-4" />
              {label}
            </button>
          ))}
        </div>

        <button
          onClick={onToggleFilters}
          className={cn(
            "flex items-center gap-1.5 px-3 py-1.5 text-base rounded-md border transition-colors",
            showFilters
              ? "border-blue-300 bg-blue-50 dark:bg-blue-900/30 text-blue-700 dark:text-blue-300"
              : "border-gray-300 dark:border-gray-600 text-gray-600 dark:text-gray-400 hover:bg-gray-50 dark:hover:bg-gray-800"
          )}
        >
          <Filter className="h-4 w-4" />
          Filters
          {Object.values(filters).filter(Boolean).length > 0 && (
            <span className="ml-1 px-1.5 py-0.5 text-sm bg-blue-500 text-white rounded-full">
              {Object.values(filters).filter(Boolean).length}
            </span>
          )}
        </button>
      </div>

      {/* Filters bar */}
      {showFilters && (
        <div className="flex flex-wrap gap-3 p-3 bg-gray-50 dark:bg-gray-800/50 rounded-lg border border-gray-200 dark:border-gray-700">
          <FilterSelect
            label="Status"
            value={filters.status}
            onChange={(v) => onFilterChange("status", v)}
            options={THREAD_STATUSES.map((s) => ({ value: s, label: THREAD_STATUS_CONFIG[s as ThreadStatus].label }))}
          />
          <FilterSelect
            label="Severity"
            value={filters.severity}
            onChange={(v) => onFilterChange("severity", v)}
            options={THREAD_SEVERITIES.map((s) => ({ value: s, label: SEVERITY_CONFIG[s as ThreadSeverity].label }))}
          />
          <FilterSelect
            label="Trend"
            value={filters.trend}
            onChange={(v) => onFilterChange("trend", v)}
            options={TREND_OPTIONS.map((t) => ({
              value: t,
              label: t === "escalating" ? "\u2191 Escalating" : t === "stable" ? "\u2192 Stable" : "\u2193 De-escalating",
            }))}
          />
          {Object.values(filters).some(Boolean) && (
            <button
              onClick={() => {
                onFilterChange("status", "");
                onFilterChange("severity", "");
                onFilterChange("trend", "");
              }}
              className="text-sm text-gray-500 hover:text-gray-700 dark:hover:text-gray-300 underline self-end mb-1"
            >
              Clear all
            </button>
          )}
        </div>
      )}
    </div>
  );
}

function FilterSelect({
  label,
  value,
  onChange,
  options,
}: {
  label: string;
  value: string;
  onChange: (v: string) => void;
  options: { value: string; label: string }[];
}) {
  return (
    <div className="flex flex-col gap-1">
      <span className="text-sm font-medium text-gray-500 dark:text-gray-400">{label}</span>
      <select
        value={value}
        onChange={(e) => onChange(e.target.value)}
        className="text-base border border-gray-300 dark:border-gray-600 rounded-md px-2 py-1 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:outline-none focus:ring-1 focus:ring-blue-500"
      >
        <option value="">All</option>
        {options.map((o) => (
          <option key={o.value} value={o.value}>{o.label}</option>
        ))}
      </select>
    </div>
  );
}
