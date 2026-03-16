"use client";

import { DecisionViewMode, DECISION_STATUSES, DECISION_STATUS_CONFIG, DecisionStatus } from "@/lib/types";
import { KanbanSquare, List, Calendar, Filter } from "lucide-react";
import { cn } from "@/lib/utils";

interface DecisionViewSwitcherProps {
  view: DecisionViewMode;
  onViewChange: (v: DecisionViewMode) => void;
  filters: {
    execution_status: string;
    project: string;
    search: string;
  };
  onFilterChange: (key: string, value: string) => void;
  projects?: string[];
  showFilters: boolean;
  onToggleFilters: () => void;
}

const views: { key: DecisionViewMode; icon: typeof KanbanSquare; label: string }[] = [
  { key: "board", icon: KanbanSquare, label: "Board" },
  { key: "list", icon: List, label: "List" },
  { key: "timeline", icon: Calendar, label: "Timeline" },
];

export default function DecisionViewSwitcher({
  view,
  onViewChange,
  filters,
  onFilterChange,
  projects = [],
  showFilters,
  onToggleFilters,
}: DecisionViewSwitcherProps) {
  return (
    <div className="space-y-3">
      {/* View toggle + filter button */}
      <div className="flex items-center justify-between">
        <div className="flex items-center bg-forest-100 dark:bg-forest-800 rounded-lg p-0.5">
          {views.map(({ key, icon: Icon, label }) => (
            <button
              key={key}
              onClick={() => onViewChange(key)}
              className={cn(
                "flex items-center gap-1.5 px-3 py-1.5 text-base font-medium rounded-md transition-colors",
                view === key
                  ? "bg-white dark:bg-forest-800 text-forest-950 dark:text-forest-50 shadow-sm"
                  : "text-forest-400 dark:text-forest-300 hover:text-forest-600 dark:hover:text-gray-300"
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
              ? "border-blue-300 bg-forest-100 dark:bg-forest-900/30 text-forest-600 dark:text-forest-200"
              : "border-forest-200 dark:border-forest-700 text-forest-500 dark:text-forest-300 hover:bg-forest-50 dark:hover:bg-forest-700"
          )}
        >
          <Filter className="h-4 w-4" />
          Filters
          {Object.values(filters).filter(Boolean).length > 0 && (
            <span className="ml-1 px-1.5 py-0.5 text-sm bg-forest-500 text-white rounded-full">
              {Object.values(filters).filter(Boolean).length}
            </span>
          )}
        </button>
      </div>

      {/* Filters bar */}
      {showFilters && (
        <div className="flex flex-wrap gap-3 p-3 bg-forest-50 dark:bg-forest-800/50 rounded-lg border border-forest-200 dark:border-forest-700">
          <FilterSelect
            label="Status"
            value={filters.execution_status}
            onChange={(v) => onFilterChange("execution_status", v)}
            options={DECISION_STATUSES.map((s) => ({ value: s, label: DECISION_STATUS_CONFIG[s as DecisionStatus].label }))}
          />
          {projects.length > 0 && (
            <FilterSelect
              label="Project"
              value={filters.project}
              onChange={(v) => onFilterChange("project", v)}
              options={projects.map((p) => ({ value: p, label: p }))}
            />
          )}
          <div className="flex flex-col gap-1">
            <span className="text-sm font-medium text-forest-400 dark:text-forest-300">Search</span>
            <input
              type="text"
              value={filters.search}
              onChange={(e) => onFilterChange("search", e.target.value)}
              placeholder="Search decisions..."
              className="text-base border border-forest-200 dark:border-forest-700 rounded-md px-2 py-1 bg-white dark:bg-forest-800 text-forest-950 dark:text-forest-50 focus:outline-none focus:ring-1 focus:ring-forest-500"
            />
          </div>
          {Object.values(filters).some(Boolean) && (
            <button
              onClick={() => {
                onFilterChange("execution_status", "");
                onFilterChange("project", "");
                onFilterChange("search", "");
              }}
              className="text-sm text-forest-400 hover:text-forest-600 dark:hover:text-gray-300 underline self-end mb-1"
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
      <span className="text-sm font-medium text-forest-400 dark:text-forest-300">{label}</span>
      <select
        value={value}
        onChange={(e) => onChange(e.target.value)}
        className="text-base border border-forest-200 dark:border-forest-700 rounded-md px-2 py-1 bg-white dark:bg-forest-800 text-forest-950 dark:text-forest-50 focus:outline-none focus:ring-1 focus:ring-forest-500"
      >
        <option value="">All</option>
        {options.map((o) => (
          <option key={o.value} value={o.value}>{o.label}</option>
        ))}
      </select>
    </div>
  );
}
