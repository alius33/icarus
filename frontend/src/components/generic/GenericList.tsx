"use client";

import React, { useState, ReactNode } from "react";
import { ArrowUpDown, ChevronDown, ChevronRight } from "lucide-react";

// ── Types ────────────────────────────────────────────────────────────

export interface ColumnDef<T> {
  key: string;
  label: string;
  width?: string; // Tailwind width class (e.g. "w-16")
  sortable?: boolean;
  /** Extract sort value from item. Return string or number. */
  sortValue?: (item: T) => string | number;
}

export interface GroupOption {
  key: string;
  label: string;
  /** Extract group label from item */
  groupFn: (item: unknown) => string;
}

export interface GenericListProps<T extends { id: number }> {
  items: T[];
  columns: ColumnDef<T>[];
  groupOptions?: GroupOption[];
  entityName: string;
  /** Render a single row's cells (one <td> per column) */
  renderRow: (item: T) => ReactNode;
  onItemClick: (item: T) => void;
}

// ── Component ────────────────────────────────────────────────────────

export default function GenericList<T extends { id: number }>({
  items,
  columns,
  groupOptions = [],
  entityName,
  renderRow,
  onItemClick,
}: GenericListProps<T>) {
  const [sortKey, setSortKey] = useState(columns[0]?.key || "");
  const [sortAsc, setSortAsc] = useState(true);
  const [groupBy, setGroupBy] = useState("none");
  const [collapsedGroups, setCollapsedGroups] = useState<Set<string>>(new Set());

  function handleSort(key: string) {
    if (sortKey === key) setSortAsc(!sortAsc);
    else {
      setSortKey(key);
      setSortAsc(true);
    }
  }

  function toggleGroup(label: string) {
    setCollapsedGroups((prev) => {
      const next = new Set(prev);
      if (next.has(label)) next.delete(label);
      else next.add(label);
      return next;
    });
  }

  // Sort
  const sortCol = columns.find((c) => c.key === sortKey);
  const sorted = [...items].sort((a, b) => {
    if (!sortCol?.sortValue) return 0;
    const av = sortCol.sortValue(a);
    const bv = sortCol.sortValue(b);
    const cmp = av < bv ? -1 : av > bv ? 1 : 0;
    return sortAsc ? cmp : -cmp;
  });

  // Group
  const activeGroupOption = groupOptions.find((g) => g.key === groupBy);
  const groups: { label: string; items: T[] }[] =
    !activeGroupOption
      ? [{ label: "", items: sorted }]
      : Object.entries(
          sorted.reduce<Record<string, T[]>>((acc, item) => {
            const g = activeGroupOption.groupFn(item);
            if (!acc[g]) acc[g] = [];
            acc[g].push(item);
            return acc;
          }, {})
        ).map(([label, items]) => ({ label, items }));

  const totalCols = columns.length;

  return (
    <div className="space-y-4">
      {/* Controls */}
      <div className="flex items-center gap-3">
        {groupOptions.length > 0 && (
          <>
            <span className="text-xs font-medium text-gray-500 dark:text-gray-400">
              Group by:
            </span>
            <select
              value={groupBy}
              onChange={(e) => setGroupBy(e.target.value)}
              className="text-sm border border-gray-300 dark:border-gray-600 rounded-md px-2 py-1 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100"
            >
              <option value="none">None</option>
              {groupOptions.map((g) => (
                <option key={g.key} value={g.key}>
                  {g.label}
                </option>
              ))}
            </select>
          </>
        )}
        <span className="ml-auto text-xs text-gray-400">
          {items.length} {entityName}
        </span>
      </div>

      {/* Table */}
      <div className="border border-gray-200 dark:border-gray-700 rounded-lg overflow-hidden">
        <table className="w-full text-sm">
          <thead className="bg-gray-50 dark:bg-gray-800">
            <tr>
              {columns.map((col) => (
                <th
                  key={col.key}
                  className={`px-3 py-2 text-left font-medium text-gray-500 dark:text-gray-400 ${
                    col.sortable !== false ? "cursor-pointer hover:text-gray-700 dark:hover:text-gray-200" : ""
                  } ${col.width || ""}`}
                  onClick={() => col.sortable !== false && col.sortValue && handleSort(col.key)}
                >
                  <span className="flex items-center gap-1">
                    {col.label}
                    {sortKey === col.key && col.sortable !== false && (
                      <ArrowUpDown className="h-3 w-3" />
                    )}
                  </span>
                </th>
              ))}
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-200 dark:divide-gray-700">
            {groups.map((group) => (
              <React.Fragment key={group.label || "all"}>
                {group.label && (
                  <tr>
                    <td
                      colSpan={totalCols}
                      className="px-3 py-2 bg-gray-100 dark:bg-gray-800/80"
                    >
                      <button
                        className="flex items-center gap-2 text-sm font-medium text-gray-700 dark:text-gray-300"
                        onClick={() => toggleGroup(group.label)}
                      >
                        {collapsedGroups.has(group.label) ? (
                          <ChevronRight className="h-4 w-4" />
                        ) : (
                          <ChevronDown className="h-4 w-4" />
                        )}
                        {group.label}
                        <span className="text-xs text-gray-400 font-normal">
                          ({group.items.length})
                        </span>
                      </button>
                    </td>
                  </tr>
                )}
                {!collapsedGroups.has(group.label) &&
                  group.items.map((item) => (
                    <tr
                      key={item.id}
                      className="hover:bg-gray-50 dark:hover:bg-gray-800/50 cursor-pointer"
                      onClick={() => onItemClick(item)}
                    >
                      {renderRow(item)}
                    </tr>
                  ))}
              </React.Fragment>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
