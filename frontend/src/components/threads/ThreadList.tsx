"use client";

import React, { useState } from "react";
import {
  OpenThreadSchema,
  THREAD_STATUS_CONFIG,
  SEVERITY_CONFIG,
  ThreadStatus,
  ThreadSeverity,
  THREAD_STATUSES,
  THREAD_SEVERITIES,
} from "@/lib/types";
import { ArrowUpDown, ChevronDown, ChevronRight } from "lucide-react";

interface ThreadListProps {
  threads: OpenThreadSchema[];
  onThreadClick: (thread: OpenThreadSchema) => void;
  onStatusChange?: (threadId: number, status: string) => void;
  onSeverityChange?: (threadId: number, severity: string) => void;
}

type SortKey = "title" | "status" | "severity" | "trend" | "opened_date";
type GroupKey = "none" | "status" | "severity" | "trend";

function trendLabel(trend: string | null): string {
  if (!trend) return "Unknown";
  if (trend === "escalating") return "\u2191 Escalating";
  if (trend === "stable") return "\u2192 Stable";
  if (trend === "de-escalating") return "\u2193 De-escalating";
  return trend;
}

function sortValue(thread: OpenThreadSchema, key: SortKey): string | number {
  if (key === "status") return THREAD_STATUS_CONFIG[thread.status as ThreadStatus]?.order ?? 99;
  if (key === "severity") {
    const order: Record<string, number> = { CRITICAL: 0, HIGH: 1, MEDIUM: 2, LOW: 3 };
    return order[thread.severity ?? ""] ?? 4;
  }
  if (key === "trend") {
    const order: Record<string, number> = { escalating: 0, stable: 1, "de-escalating": 2 };
    return order[thread.trend ?? ""] ?? 3;
  }
  const v = thread[key];
  return v ? String(v).toLowerCase() : "zzz";
}

function groupLabel(thread: OpenThreadSchema, key: GroupKey): string {
  if (key === "status") return THREAD_STATUS_CONFIG[thread.status as ThreadStatus]?.label ?? thread.status;
  if (key === "severity") return SEVERITY_CONFIG[thread.severity as ThreadSeverity]?.label ?? (thread.severity || "Unknown");
  if (key === "trend") return trendLabel(thread.trend);
  return "";
}

export default function ThreadList({ threads, onThreadClick, onStatusChange, onSeverityChange }: ThreadListProps) {
  const [sortKey, setSortKey] = useState<SortKey>("opened_date");
  const [sortAsc, setSortAsc] = useState(true);
  const [groupBy, setGroupBy] = useState<GroupKey>("none");
  const [collapsedGroups, setCollapsedGroups] = useState<Set<string>>(new Set());

  function handleSort(key: SortKey) {
    if (sortKey === key) setSortAsc(!sortAsc);
    else { setSortKey(key); setSortAsc(true); }
  }

  function toggleGroup(label: string) {
    setCollapsedGroups((prev) => {
      const next = new Set(prev);
      if (next.has(label)) next.delete(label); else next.add(label);
      return next;
    });
  }

  const sorted = [...threads].sort((a, b) => {
    const av = sortValue(a, sortKey);
    const bv = sortValue(b, sortKey);
    const cmp = av < bv ? -1 : av > bv ? 1 : 0;
    return sortAsc ? cmp : -cmp;
  });

  const groups: { label: string; threads: OpenThreadSchema[] }[] =
    groupBy === "none"
      ? [{ label: "", threads: sorted }]
      : Object.entries(
          sorted.reduce<Record<string, OpenThreadSchema[]>>((acc, t) => {
            const g = groupLabel(t, groupBy);
            if (!acc[g]) acc[g] = [];
            acc[g].push(t);
            return acc;
          }, {})
        ).map(([label, threads]) => ({ label, threads }));

  return (
    <div className="space-y-4">
      {/* Controls */}
      <div className="flex flex-wrap items-center gap-2 md:gap-3">
        <span className="text-sm font-medium text-forest-400 dark:text-forest-300">Group by:</span>
        <select
          value={groupBy}
          onChange={(e) => setGroupBy(e.target.value as GroupKey)}
          className="text-base border border-forest-200 dark:border-forest-700 rounded-md px-2 py-1 bg-white dark:bg-forest-800 text-forest-950 dark:text-forest-50"
        >
          <option value="none">None</option>
          <option value="status">Status</option>
          <option value="severity">Severity</option>
          <option value="trend">Trend</option>
        </select>
        <span className="ml-auto text-sm text-forest-300">{threads.length} threads</span>
      </div>

      {/* Mobile card view */}
      <div className="space-y-2 md:hidden">
        {groups.map((group) => (
          <React.Fragment key={group.label || "all"}>
            {group.label && (
              <button
                className="flex items-center gap-2 text-base font-medium text-forest-600 dark:text-forest-200 py-1"
                onClick={() => toggleGroup(group.label)}
              >
                {collapsedGroups.has(group.label) ? <ChevronRight className="h-4 w-4" /> : <ChevronDown className="h-4 w-4" />}
                {group.label}
                <span className="text-sm text-forest-300 font-normal">({group.threads.length})</span>
              </button>
            )}
            {!collapsedGroups.has(group.label) &&
              group.threads.map((thread) => {
                const statusCfg = THREAD_STATUS_CONFIG[thread.status as ThreadStatus];
                const severityCfg = SEVERITY_CONFIG[thread.severity as ThreadSeverity];
                return (
                  <div
                    key={thread.id}
                    className="rounded-lg border border-forest-200 dark:border-forest-700 p-3 active:bg-forest-50 dark:active:bg-gray-800 cursor-pointer"
                    onClick={() => onThreadClick(thread)}
                  >
                    <div className="flex items-center gap-2 mb-1">
                      {severityCfg && <span className={`w-2 h-2 rounded-full shrink-0 ${severityCfg.dotColor}`} />}
                      <span className="text-forest-950 dark:text-forest-50 text-base line-clamp-2">{thread.title}</span>
                    </div>
                    <div className="flex flex-wrap items-center gap-2 mb-1">
                      <span className={`text-sm font-medium px-2 py-0.5 rounded ${statusCfg?.bgColor ?? "bg-forest-100"} ${statusCfg?.color ?? "text-forest-500"}`}>
                        {statusCfg?.label ?? thread.status}
                      </span>
                      {severityCfg && (
                        <span className="text-sm text-forest-400">{severityCfg.label}</span>
                      )}
                      {thread.trend && (
                        <span className={`text-sm font-medium px-2 py-0.5 rounded-full ${
                          thread.trend === "escalating" ? "bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-400" :
                          thread.trend === "stable" ? "bg-yellow-100 text-yellow-700 dark:bg-yellow-900/30 dark:text-yellow-400" :
                          "bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400"
                        }`}>
                          {trendLabel(thread.trend)}
                        </span>
                      )}
                    </div>
                    <div className="text-sm text-forest-300">
                      {thread.opened_date ? new Date(thread.opened_date).toLocaleDateString("en-GB", { day: "numeric", month: "short" }) : ""}
                    </div>
                  </div>
                );
              })}
          </React.Fragment>
        ))}
        {threads.length === 0 && (
          <div className="rounded-lg border-2 border-dashed border-forest-200 dark:border-forest-700 p-8 text-center">
            <p className="text-base text-forest-400">No threads yet.</p>
          </div>
        )}
      </div>

      {/* Desktop table */}
      <div className="hidden md:block border border-forest-200 dark:border-forest-700 rounded-lg overflow-hidden">
        <table className="w-full text-base">
          <thead className="bg-forest-50 dark:bg-forest-800">
            <tr>
              {(
                [
                  { key: "title", label: "Thread", w: "" },
                  { key: "status", label: "Status", w: "w-28" },
                  { key: "severity", label: "Severity", w: "w-24" },
                  { key: "trend", label: "Trend", w: "w-32" },
                  { key: "opened_date", label: "First Raised", w: "w-28" },
                ] as { key: SortKey; label: string; w: string }[]
              ).map((col) => (
                <th
                  key={col.key}
                  className={`px-3 py-2 text-left font-medium text-forest-400 dark:text-forest-300 cursor-pointer hover:text-forest-600 dark:hover:text-gray-200 ${col.w}`}
                  onClick={() => handleSort(col.key)}
                >
                  <span className="flex items-center gap-1">
                    {col.label}
                    {sortKey === col.key && <ArrowUpDown className="h-3 w-3" />}
                  </span>
                </th>
              ))}
            </tr>
          </thead>
          <tbody className="divide-y divide-forest-200 dark:divide-forest-700">
            {groups.map((group) => (
              <React.Fragment key={group.label || "all"}>
                {group.label && (
                  <tr>
                    <td colSpan={5} className="px-3 py-2 bg-forest-100 dark:bg-forest-800/80">
                      <button
                        className="flex items-center gap-2 text-base font-medium text-forest-600 dark:text-forest-200"
                        onClick={() => toggleGroup(group.label)}
                      >
                        {collapsedGroups.has(group.label) ? (
                          <ChevronRight className="h-4 w-4" />
                        ) : (
                          <ChevronDown className="h-4 w-4" />
                        )}
                        {group.label}
                        <span className="text-sm text-forest-300 font-normal">({group.threads.length})</span>
                      </button>
                    </td>
                  </tr>
                )}
                {!collapsedGroups.has(group.label) &&
                  group.threads.map((thread) => {
                    const statusCfg = THREAD_STATUS_CONFIG[thread.status as ThreadStatus];
                    const severityCfg = SEVERITY_CONFIG[thread.severity as ThreadSeverity];

                    return (
                      <tr
                        key={thread.id}
                        className="hover:bg-forest-50 dark:hover:bg-forest-700/50 cursor-pointer"
                        onClick={() => onThreadClick(thread)}
                      >
                        <td className="px-3 py-2">
                          <div className="flex items-center gap-2">
                            {severityCfg && (
                              <span className={`w-2 h-2 rounded-full shrink-0 ${severityCfg.dotColor}`} />
                            )}
                            <span className="text-forest-950 dark:text-forest-50 truncate">{thread.title}</span>
                          </div>
                        </td>
                        <td className="px-3 py-2" onClick={(e) => e.stopPropagation()}>
                          {onStatusChange ? (
                            <select
                              value={thread.status}
                              onChange={(e) => onStatusChange(thread.id, e.target.value)}
                              className={`text-sm font-medium rounded px-2 py-1 border-0 ${statusCfg?.bgColor ?? "bg-forest-100"} ${statusCfg?.color ?? "text-forest-500"}`}
                            >
                              {THREAD_STATUSES.map((s) => (
                                <option key={s} value={s}>{THREAD_STATUS_CONFIG[s].label}</option>
                              ))}
                            </select>
                          ) : (
                            <span className={`text-sm font-medium px-2 py-1 rounded ${statusCfg?.bgColor ?? "bg-forest-100"} ${statusCfg?.color ?? "text-forest-500"}`}>
                              {statusCfg?.label ?? thread.status}
                            </span>
                          )}
                        </td>
                        <td className="px-3 py-2" onClick={(e) => e.stopPropagation()}>
                          {onSeverityChange ? (
                            <select
                              value={thread.severity ?? ""}
                              onChange={(e) => onSeverityChange(thread.id, e.target.value)}
                              className="text-sm rounded px-1 py-1 border-0 bg-transparent"
                            >
                              <option value="">None</option>
                              {THREAD_SEVERITIES.map((s) => (
                                <option key={s} value={s}>{SEVERITY_CONFIG[s].label}</option>
                              ))}
                            </select>
                          ) : (
                            <span className="flex items-center gap-1.5">
                              <span className={`w-2 h-2 rounded-full ${severityCfg?.dotColor ?? "bg-gray-300"}`} />
                              <span className="text-sm">{severityCfg?.label ?? (thread.severity || "None")}</span>
                            </span>
                          )}
                        </td>
                        <td className="px-3 py-2">
                          {thread.trend && (
                            <span className={`text-sm font-medium px-2 py-0.5 rounded-full ${
                              thread.trend === "escalating" ? "bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-400" :
                              thread.trend === "stable" ? "bg-yellow-100 text-yellow-700 dark:bg-yellow-900/30 dark:text-yellow-400" :
                              "bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400"
                            }`}>
                              {trendLabel(thread.trend)}
                            </span>
                          )}
                        </td>
                        <td className="px-3 py-2 text-sm text-forest-400 dark:text-forest-300">
                          {thread.opened_date ? new Date(thread.opened_date).toLocaleDateString("en-GB", { day: "numeric", month: "short" }) : "\u2014"}
                        </td>
                      </tr>
                    );
                  })}
              </React.Fragment>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
