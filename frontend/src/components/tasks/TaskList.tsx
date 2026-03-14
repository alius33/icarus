"use client";

import { useState } from "react";
import { TaskSchema, STATUS_CONFIG, PRIORITY_CONFIG, TaskStatus, TaskPriority } from "@/lib/types";
import { isOverdue } from "@/lib/utils";
import { ArrowUpDown, ChevronDown, ChevronRight } from "lucide-react";

interface TaskListProps {
  tasks: TaskSchema[];
  onTaskClick: (task: TaskSchema) => void;
  onStatusChange?: (taskId: number, status: string) => void;
  onPriorityChange?: (taskId: number, priority: string) => void;
}

type SortKey = "title" | "status" | "priority" | "assignee" | "due_date" | "project_name" | "created_date";
type GroupKey = "none" | "status" | "priority" | "assignee" | "project_name";

function sortValue(task: TaskSchema, key: SortKey): string | number {
  if (key === "status") return STATUS_CONFIG[task.status]?.order ?? 99;
  if (key === "priority") {
    const order: Record<string, number> = { URGENT: 0, HIGH: 1, MEDIUM: 2, LOW: 3, NONE: 4 };
    return order[task.priority] ?? 4;
  }
  const v = task[key];
  return v ? String(v).toLowerCase() : "zzz";
}

function groupLabel(task: TaskSchema, key: GroupKey): string {
  if (key === "status") return STATUS_CONFIG[task.status as TaskStatus]?.label ?? task.status;
  if (key === "priority") return PRIORITY_CONFIG[task.priority as TaskPriority]?.label ?? task.priority;
  if (key === "assignee") return task.assignee || "Unassigned";
  if (key === "project_name") return task.project_name || "No Project";
  return "";
}

export default function TaskList({ tasks, onTaskClick, onStatusChange, onPriorityChange }: TaskListProps) {
  const [sortKey, setSortKey] = useState<SortKey>("created_date");
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

  const sorted = [...tasks].sort((a, b) => {
    const av = sortValue(a, sortKey);
    const bv = sortValue(b, sortKey);
    const cmp = av < bv ? -1 : av > bv ? 1 : 0;
    return sortAsc ? cmp : -cmp;
  });

  const groups: { label: string; tasks: TaskSchema[] }[] =
    groupBy === "none"
      ? [{ label: "", tasks: sorted }]
      : Object.entries(
          sorted.reduce<Record<string, TaskSchema[]>>((acc, t) => {
            const g = groupLabel(t, groupBy);
            (acc[g] ??= []).push(t);
            return acc;
          }, {})
        ).map(([label, tasks]) => ({ label, tasks }));

  return (
    <div className="space-y-4">
      {/* Controls */}
      <div className="flex items-center gap-3">
        <span className="text-sm font-medium text-gray-500 dark:text-gray-400">Group by:</span>
        <select
          value={groupBy}
          onChange={(e) => setGroupBy(e.target.value as GroupKey)}
          className="text-base border border-gray-300 dark:border-gray-600 rounded-md px-2 py-1 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100"
        >
          <option value="none">None</option>
          <option value="status">Status</option>
          <option value="priority">Priority</option>
          <option value="assignee">Assignee</option>
          <option value="project_name">Project</option>
        </select>
        <span className="ml-auto text-sm text-gray-400">{tasks.length} tasks</span>
      </div>

      {/* Table */}
      <div className="border border-gray-200 dark:border-gray-700 rounded-lg overflow-hidden">
        <table className="w-full text-base">
          <thead className="bg-gray-50 dark:bg-gray-800">
            <tr>
              {(
                [
                  { key: "title", label: "Task", w: "" },
                  { key: "status", label: "Status", w: "w-28" },
                  { key: "priority", label: "Priority", w: "w-24" },
                  { key: "assignee", label: "Assignee", w: "w-32" },
                  { key: "due_date", label: "Due", w: "w-28" },
                  { key: "project_name", label: "Project", w: "w-36" },
                ] as { key: SortKey; label: string; w: string }[]
              ).map((col) => (
                <th
                  key={col.key}
                  className={`px-3 py-2 text-left font-medium text-gray-500 dark:text-gray-400 cursor-pointer hover:text-gray-700 dark:hover:text-gray-200 ${col.w}`}
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
          <tbody className="divide-y divide-gray-200 dark:divide-gray-700">
            {groups.map((group) => (
              <>
                {group.label && (
                  <tr key={`group-${group.label}`}>
                    <td colSpan={6} className="px-3 py-2 bg-gray-100 dark:bg-gray-800/80">
                      <button
                        className="flex items-center gap-2 text-base font-medium text-gray-700 dark:text-gray-300"
                        onClick={() => toggleGroup(group.label)}
                      >
                        {collapsedGroups.has(group.label) ? (
                          <ChevronRight className="h-4 w-4" />
                        ) : (
                          <ChevronDown className="h-4 w-4" />
                        )}
                        {group.label}
                        <span className="text-sm text-gray-400 font-normal">({group.tasks.length})</span>
                      </button>
                    </td>
                  </tr>
                )}
                {!collapsedGroups.has(group.label) &&
                  group.tasks.map((task) => {
                    const statusCfg = STATUS_CONFIG[task.status as TaskStatus];
                    const priorityCfg = PRIORITY_CONFIG[task.priority as TaskPriority];
                    const overdue = isOverdue(task.due_date) && task.status !== "DONE" && task.status !== "CANCELLED";

                    return (
                      <tr
                        key={task.id}
                        className="hover:bg-gray-50 dark:hover:bg-gray-800/50 cursor-pointer"
                        onClick={() => onTaskClick(task)}
                      >
                        <td className="px-3 py-2">
                          <div className="flex items-center gap-2">
                            <span className="text-sm font-mono text-gray-400 shrink-0">{task.identifier}</span>
                            <span className="text-gray-900 dark:text-gray-100 truncate">{task.title}</span>
                            {task.labels.length > 0 && (
                              <span className="text-sm px-1.5 py-0.5 rounded bg-blue-50 dark:bg-blue-900/30 text-blue-600 dark:text-blue-300 shrink-0">
                                {task.labels[0]}
                                {task.labels.length > 1 && `+${task.labels.length - 1}`}
                              </span>
                            )}
                          </div>
                        </td>
                        <td className="px-3 py-2" onClick={(e) => e.stopPropagation()}>
                          {onStatusChange ? (
                            <select
                              value={task.status}
                              onChange={(e) => onStatusChange(task.id, e.target.value)}
                              className={`text-sm font-medium rounded px-2 py-1 border-0 ${statusCfg?.bgColor ?? "bg-gray-100"} ${statusCfg?.color ?? "text-gray-600"}`}
                            >
                              {Object.entries(STATUS_CONFIG).map(([k, v]) => (
                                <option key={k} value={k}>{v.label}</option>
                              ))}
                            </select>
                          ) : (
                            <span className={`text-sm font-medium px-2 py-1 rounded ${statusCfg?.bgColor ?? "bg-gray-100"} ${statusCfg?.color ?? "text-gray-600"}`}>
                              {statusCfg?.label ?? task.status}
                            </span>
                          )}
                        </td>
                        <td className="px-3 py-2" onClick={(e) => e.stopPropagation()}>
                          {onPriorityChange ? (
                            <select
                              value={task.priority}
                              onChange={(e) => onPriorityChange(task.id, e.target.value)}
                              className="text-sm rounded px-1 py-1 border-0 bg-transparent"
                            >
                              {Object.entries(PRIORITY_CONFIG).map(([k, v]) => (
                                <option key={k} value={k}>{v.label}</option>
                              ))}
                            </select>
                          ) : (
                            <span className="flex items-center gap-1.5">
                              <span className={`w-2 h-2 rounded-full ${priorityCfg?.dotColor ?? "bg-gray-300"}`} />
                              <span className="text-sm">{priorityCfg?.label ?? task.priority}</span>
                            </span>
                          )}
                        </td>
                        <td className="px-3 py-2 text-gray-500 dark:text-gray-400 truncate">
                          {task.assignee || "—"}
                        </td>
                        <td className={`px-3 py-2 text-sm ${overdue ? "text-red-500 font-medium" : "text-gray-500 dark:text-gray-400"}`}>
                          {task.due_date ? new Date(task.due_date).toLocaleDateString("en-GB", { day: "numeric", month: "short" }) : "—"}
                        </td>
                        <td className="px-3 py-2 text-sm text-gray-400 truncate">
                          {task.project_name || "—"}
                        </td>
                      </tr>
                    );
                  })}
              </>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
