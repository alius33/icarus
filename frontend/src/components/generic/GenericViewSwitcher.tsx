"use client";

import { LucideIcon, KanbanSquare, List, Calendar, Filter } from "lucide-react";
import { cn } from "@/lib/utils";

// ── Types ────────────────────────────────────────────────────────────

export interface ViewOption {
  key: string;
  icon: LucideIcon;
  label: string;
}

export interface FilterDef {
  key: string;
  label: string;
  type: "select" | "text";
  options?: { value: string; label: string }[];
  placeholder?: string;
}

export interface GenericViewSwitcherProps {
  view: string;
  onViewChange: (v: string) => void;
  views: ViewOption[];
  filters: Record<string, string>;
  onFilterChange: (key: string, value: string) => void;
  filterDefs: FilterDef[];
  showFilters: boolean;
  onToggleFilters: () => void;
}

// ── Preset view configs ──────────────────────────────────────────────

export const BOARD_LIST_TIMELINE_VIEWS: ViewOption[] = [
  { key: "board", icon: KanbanSquare, label: "Board" },
  { key: "list", icon: List, label: "List" },
  { key: "timeline", icon: Calendar, label: "Timeline" },
];

export const BOARD_LIST_VIEWS: ViewOption[] = [
  { key: "board", icon: KanbanSquare, label: "Board" },
  { key: "list", icon: List, label: "List" },
];

// ── Component ────────────────────────────────────────────────────────

export default function GenericViewSwitcher({
  view,
  onViewChange,
  views,
  filters,
  onFilterChange,
  filterDefs,
  showFilters,
  onToggleFilters,
}: GenericViewSwitcherProps) {
  const activeFilterCount = Object.values(filters).filter(Boolean).length;

  return (
    <div className="space-y-3">
      <div className="flex items-center justify-between">
        <div className="flex items-center bg-gray-100 dark:bg-gray-800 rounded-lg p-0.5">
          {views.map(({ key, icon: Icon, label }) => (
            <button
              key={key}
              onClick={() => onViewChange(key)}
              className={cn(
                "flex items-center gap-1.5 px-3 py-1.5 text-sm font-medium rounded-md transition-colors",
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
            "flex items-center gap-1.5 px-3 py-1.5 text-sm rounded-md border transition-colors",
            showFilters
              ? "border-blue-300 bg-blue-50 dark:bg-blue-900/30 text-blue-700 dark:text-blue-300"
              : "border-gray-300 dark:border-gray-600 text-gray-600 dark:text-gray-400 hover:bg-gray-50 dark:hover:bg-gray-800"
          )}
        >
          <Filter className="h-4 w-4" />
          Filters
          {activeFilterCount > 0 && (
            <span className="ml-1 px-1.5 py-0.5 text-xs bg-blue-500 text-white rounded-full">
              {activeFilterCount}
            </span>
          )}
        </button>
      </div>

      {showFilters && (
        <div className="flex flex-wrap gap-3 p-3 bg-gray-50 dark:bg-gray-800/50 rounded-lg border border-gray-200 dark:border-gray-700">
          {filterDefs.map((def) =>
            def.type === "select" && def.options ? (
              <div key={def.key} className="flex flex-col gap-1">
                <span className="text-xs font-medium text-gray-500 dark:text-gray-400">
                  {def.label}
                </span>
                <select
                  value={filters[def.key] || ""}
                  onChange={(e) => onFilterChange(def.key, e.target.value)}
                  className="text-sm border border-gray-300 dark:border-gray-600 rounded-md px-2 py-1 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:outline-none focus:ring-1 focus:ring-blue-500"
                >
                  <option value="">All</option>
                  {def.options.map((o) => (
                    <option key={o.value} value={o.value}>
                      {o.label}
                    </option>
                  ))}
                </select>
              </div>
            ) : (
              <div key={def.key} className="flex flex-col gap-1">
                <span className="text-xs font-medium text-gray-500 dark:text-gray-400">
                  {def.label}
                </span>
                <input
                  type="text"
                  value={filters[def.key] || ""}
                  onChange={(e) => onFilterChange(def.key, e.target.value)}
                  placeholder={def.placeholder}
                  className="text-sm border border-gray-300 dark:border-gray-600 rounded-md px-2 py-1 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:outline-none focus:ring-1 focus:ring-blue-500"
                />
              </div>
            )
          )}
          {activeFilterCount > 0 && (
            <button
              onClick={() => {
                filterDefs.forEach((def) => onFilterChange(def.key, ""));
              }}
              className="text-xs text-gray-500 hover:text-gray-700 dark:hover:text-gray-300 underline self-end mb-1"
            >
              Clear all
            </button>
          )}
        </div>
      )}
    </div>
  );
}
