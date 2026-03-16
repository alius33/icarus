"use client";

import React, { useState } from "react";
import { DecisionSchema, DECISION_STATUS_CONFIG, DecisionStatus } from "@/lib/types";
import { ArrowUpDown, ChevronDown, ChevronRight } from "lucide-react";

interface DecisionListProps {
  decisions: DecisionSchema[];
  onDecisionClick: (decision: DecisionSchema) => void;
  onStatusChange?: (decisionId: number, executionStatus: string) => void;
}

type SortKey = "number" | "date" | "title" | "execution_status" | "project_name";
type GroupKey = "none" | "execution_status" | "project_name";

function sortValue(decision: DecisionSchema, key: SortKey): string | number {
  if (key === "number") return decision.number;
  if (key === "execution_status") return DECISION_STATUS_CONFIG[decision.execution_status as DecisionStatus]?.order ?? 99;
  if (key === "date") return decision.date ?? "zzz";
  const v = decision[key];
  return v ? String(v).toLowerCase() : "zzz";
}

function groupLabel(decision: DecisionSchema, key: GroupKey): string {
  if (key === "execution_status") return DECISION_STATUS_CONFIG[decision.execution_status as DecisionStatus]?.label ?? decision.execution_status;
  if (key === "project_name") return decision.project_name || "No Project";
  return "";
}

export default function DecisionList({ decisions, onDecisionClick, onStatusChange }: DecisionListProps) {
  const [sortKey, setSortKey] = useState<SortKey>("number");
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

  const sorted = [...decisions].sort((a, b) => {
    const av = sortValue(a, sortKey);
    const bv = sortValue(b, sortKey);
    const cmp = av < bv ? -1 : av > bv ? 1 : 0;
    return sortAsc ? cmp : -cmp;
  });

  const groups: { label: string; decisions: DecisionSchema[] }[] =
    groupBy === "none"
      ? [{ label: "", decisions: sorted }]
      : Object.entries(
          sorted.reduce<Record<string, DecisionSchema[]>>((acc, d) => {
            const g = groupLabel(d, groupBy);
            if (!acc[g]) acc[g] = [];
            acc[g].push(d);
            return acc;
          }, {})
        ).map(([label, decisions]) => ({ label, decisions }));

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
          <option value="execution_status">Status</option>
          <option value="project_name">Project</option>
        </select>
        <span className="ml-auto text-sm text-forest-300">{decisions.length} decisions</span>
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
                <span className="text-sm text-forest-300 font-normal">({group.decisions.length})</span>
              </button>
            )}
            {!collapsedGroups.has(group.label) &&
              group.decisions.map((decision) => {
                const statusCfg = DECISION_STATUS_CONFIG[decision.execution_status as DecisionStatus];
                return (
                  <div
                    key={decision.id}
                    className="rounded-lg border border-forest-200 dark:border-forest-700 p-3 active:bg-forest-50 dark:active:bg-gray-800 cursor-pointer"
                    onClick={() => onDecisionClick(decision)}
                  >
                    <div className="flex items-center gap-2 text-sm text-forest-300 mb-1">
                      <span className="font-mono">#{decision.number}</span>
                      <span>&middot;</span>
                      <span>{decision.date ? new Date(decision.date).toLocaleDateString("en-GB", { day: "numeric", month: "short" }) : "\u2014"}</span>
                    </div>
                    <p className="text-forest-950 dark:text-forest-50 text-base line-clamp-2 mb-2">{decision.title}</p>
                    <div className="flex flex-wrap items-center gap-2">
                      <span className={`text-sm font-medium px-2 py-0.5 rounded ${statusCfg?.bgColor ?? "bg-forest-100"} ${statusCfg?.color ?? "text-forest-500"}`}>
                        {statusCfg?.label ?? decision.execution_status}
                      </span>
                      {decision.project_name && (
                        <span className="text-sm text-forest-300">{decision.project_name}</span>
                      )}
                    </div>
                    {decision.key_people.length > 0 && (
                      <div className="flex flex-wrap gap-1 mt-2">
                        {decision.key_people.slice(0, 3).map((person) => (
                          <span key={person} className="px-1.5 py-0.5 text-sm rounded bg-blue-50 dark:bg-blue-900/30 text-forest-500 dark:text-blue-300">{person}</span>
                        ))}
                        {decision.key_people.length > 3 && <span className="text-sm text-forest-300">+{decision.key_people.length - 3}</span>}
                      </div>
                    )}
                  </div>
                );
              })}
          </React.Fragment>
        ))}
        {decisions.length === 0 && (
          <div className="rounded-lg border-2 border-dashed border-forest-200 dark:border-forest-700 p-8 text-center">
            <p className="text-base text-forest-400">No decisions yet.</p>
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
                  { key: "number", label: "#", w: "w-16" },
                  { key: "date", label: "Date", w: "w-28" },
                  { key: "title", label: "Decision", w: "" },
                  { key: "execution_status", label: "Status", w: "w-32" },
                  { key: "project_name", label: "Project", w: "w-36" },
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
              <th className="px-3 py-2 text-left font-medium text-forest-400 dark:text-forest-300 w-40">
                Key People
              </th>
            </tr>
          </thead>
          <tbody className="divide-y divide-forest-200 dark:divide-forest-700">
            {groups.map((group) => (
              <React.Fragment key={group.label || "all"}>
                {group.label && (
                  <tr>
                    <td colSpan={6} className="px-3 py-2 bg-forest-100 dark:bg-forest-800/80">
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
                        <span className="text-sm text-forest-300 font-normal">({group.decisions.length})</span>
                      </button>
                    </td>
                  </tr>
                )}
                {!collapsedGroups.has(group.label) &&
                  group.decisions.map((decision) => {
                    const statusCfg = DECISION_STATUS_CONFIG[decision.execution_status as DecisionStatus];

                    return (
                      <tr
                        key={decision.id}
                        className="hover:bg-forest-50 dark:hover:bg-forest-700/50 cursor-pointer"
                        onClick={() => onDecisionClick(decision)}
                      >
                        <td className="px-3 py-2">
                          <span className="text-sm font-mono text-forest-300">#{decision.number}</span>
                        </td>
                        <td className="px-3 py-2 text-sm text-forest-400 dark:text-forest-300">
                          {decision.date ? new Date(decision.date).toLocaleDateString("en-GB", { day: "numeric", month: "short" }) : "\u2014"}
                        </td>
                        <td className="px-3 py-2">
                          <span className="text-forest-950 dark:text-forest-50 truncate">{decision.title}</span>
                        </td>
                        <td className="px-3 py-2" onClick={(e) => e.stopPropagation()}>
                          {onStatusChange ? (
                            <select
                              value={decision.execution_status}
                              onChange={(e) => onStatusChange(decision.id, e.target.value)}
                              className={`text-sm font-medium rounded px-2 py-1 border-0 ${statusCfg?.bgColor ?? "bg-forest-100"} ${statusCfg?.color ?? "text-forest-500"}`}
                            >
                              {Object.entries(DECISION_STATUS_CONFIG).map(([k, v]) => (
                                <option key={k} value={k}>{v.label}</option>
                              ))}
                            </select>
                          ) : (
                            <span className={`text-sm font-medium px-2 py-1 rounded ${statusCfg?.bgColor ?? "bg-forest-100"} ${statusCfg?.color ?? "text-forest-500"}`}>
                              {statusCfg?.label ?? decision.execution_status}
                            </span>
                          )}
                        </td>
                        <td className="px-3 py-2 text-sm text-forest-300 truncate">
                          {decision.project_name || "\u2014"}
                        </td>
                        <td className="px-3 py-2">
                          <div className="flex flex-wrap gap-1">
                            {decision.key_people.slice(0, 2).map((person) => (
                              <span
                                key={person}
                                className="px-1.5 py-0.5 text-sm rounded bg-blue-50 dark:bg-blue-900/30 text-forest-500 dark:text-blue-300"
                              >
                                {person}
                              </span>
                            ))}
                            {decision.key_people.length > 2 && (
                              <span className="text-sm text-forest-300">+{decision.key_people.length - 2}</span>
                            )}
                          </div>
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
