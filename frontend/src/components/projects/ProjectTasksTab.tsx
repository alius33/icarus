"use client";

import { useEffect, useState, useCallback } from "react";
import { useSearchParams, useRouter, usePathname } from "next/navigation";
import {
  TaskSchema,
  TaskBoardResponse,
  TaskTimelineResponse,
  TaskTimelineItem,
  STATUS_CONFIG,
  PRIORITY_CONFIG,
  TaskStatus,
  TaskPriority,
} from "@/lib/types";
import { api } from "@/lib/api";
import { isOverdue } from "@/lib/utils";
import GenericBoard from "@/components/generic/GenericBoard";
import GenericList, { ColumnDef, GroupOption } from "@/components/generic/GenericList";
import GenericTimeline from "@/components/generic/GenericTimeline";
import GenericViewSwitcher, {
  BOARD_LIST_TIMELINE_VIEWS,
  FilterDef,
} from "@/components/generic/GenericViewSwitcher";
import { taskBoardConfig } from "@/config/board-configs";
import TaskCard from "@/components/tasks/TaskCard";
import TaskDetailPanel from "@/components/tasks/TaskDetailPanel";
import TaskCreateModal from "@/components/tasks/TaskCreateModal";
import { Plus } from "lucide-react";

const listColumns: ColumnDef<TaskSchema>[] = [
  { key: "title", label: "Task", sortable: true, sortValue: (t) => t.title.toLowerCase() },
  { key: "status", label: "Status", width: "w-28", sortable: true, sortValue: (t) => STATUS_CONFIG[t.status as TaskStatus]?.order ?? 99 },
  { key: "priority", label: "Priority", width: "w-24", sortable: true, sortValue: (t) => { const o: Record<string, number> = { URGENT: 0, HIGH: 1, MEDIUM: 2, LOW: 3, NONE: 4 }; return o[t.priority] ?? 4; } },
  { key: "assignee", label: "Assignee", width: "w-32", sortable: true, sortValue: (t) => t.assignee?.toLowerCase() ?? "zzz" },
  { key: "due_date", label: "Due", width: "w-28", sortable: true, sortValue: (t) => t.due_date ?? "zzz" },
  { key: "project_name", label: "Project", width: "w-36", sortable: true, sortValue: (t) => t.project_name?.toLowerCase() ?? "zzz" },
];

const listGroupOptions: GroupOption[] = [
  { key: "status", label: "Status", groupFn: (item) => { const t = item as TaskSchema; return STATUS_CONFIG[t.status as TaskStatus]?.label ?? t.status; } },
  { key: "priority", label: "Priority", groupFn: (item) => { const t = item as TaskSchema; return PRIORITY_CONFIG[t.priority as TaskPriority]?.label ?? t.priority; } },
  { key: "assignee", label: "Assignee", groupFn: (item) => (item as TaskSchema).assignee || "Unassigned" },
  { key: "project_name", label: "Project", groupFn: (item) => (item as TaskSchema).project_name || "No Project" },
];

interface Props {
  projectId: number;
  projects?: { id: number; name: string }[];
}

export default function ProjectTasksTab({ projectId, projects = [] }: Props) {
  const searchParams = useSearchParams();
  const router = useRouter();
  const pathname = usePathname();

  const view = searchParams.get("view") || "board";

  const [filters, setFilters] = useState({
    status: searchParams.get("status") || "",
    priority: searchParams.get("priority") || "",
    assignee: searchParams.get("assignee") || "",
    label: searchParams.get("label") || "",
  });
  const [showFilters, setShowFilters] = useState(Object.values(filters).some(Boolean));

  const [boardData, setBoardData] = useState<TaskBoardResponse | null>(null);
  const [listData, setListData] = useState<TaskSchema[]>([]);
  const [timelineData, setTimelineData] = useState<TaskTimelineResponse | null>(null);
  const [loading, setLoading] = useState(true);

  const [selectedTask, setSelectedTask] = useState<TaskSchema | null>(null);
  const [showCreate, setShowCreate] = useState(false);
  const [allLabels, setAllLabels] = useState<string[]>([]);
  const [assignees, setAssignees] = useState<string[]>([]);

  const filterDefs: FilterDef[] = [
    { key: "status", label: "Status", type: "select", options: Object.entries(STATUS_CONFIG).map(([k, v]) => ({ value: k, label: v.label })) },
    { key: "priority", label: "Priority", type: "select", options: Object.entries(PRIORITY_CONFIG).map(([k, v]) => ({ value: k, label: v.label })) },
    { key: "assignee", label: "Assignee", type: "select", options: assignees.map((a) => ({ value: a, label: a })) },
    { key: "label", label: "Label", type: "select", options: allLabels.map((l) => ({ value: l, label: l })) },
  ];

  function updateUrlParams(newView?: string, newFilters?: Record<string, string>) {
    const params = new URLSearchParams();
    params.set("tab", "tasks");
    const v = newView ?? view;
    if (v !== "board") params.set("view", v);
    const f = newFilters ?? filters;
    Object.entries(f).forEach(([k, val]) => { if (val) params.set(k, val); });
    router.replace(`${pathname}?${params.toString()}`, { scroll: false });
  }

  function handleViewChange(v: string) { updateUrlParams(v); }
  function handleFilterChange(key: string, value: string) {
    const next = { ...filters, [key]: value };
    setFilters(next);
    updateUrlParams(undefined, next);
  }

  const fetchData = useCallback(async () => {
    setLoading(true);
    try {
      if (view === "board") {
        setBoardData(await api.getTaskBoard(projectId));
      } else if (view === "list") {
        const params: Record<string, string> = { project_id: String(projectId) };
        if (filters.status) params.status = filters.status;
        if (filters.priority) params.priority = filters.priority;
        if (filters.assignee) params.assignee = filters.assignee;
        if (filters.label) params.label = filters.label;
        setListData(await api.getTasks(params));
      } else {
        setTimelineData(await api.getTaskTimeline(projectId));
      }
    } catch (e) { console.error("Failed to fetch tasks:", e); }
    finally { setLoading(false); }
  }, [view, filters, projectId]);

  useEffect(() => { api.getTaskLabels().then(setAllLabels).catch(() => {}); }, []);
  useEffect(() => {
    if (listData.length > 0) {
      setAssignees(Array.from(new Set(listData.map((t) => t.assignee).filter(Boolean) as string[])));
    }
  }, [listData]);
  useEffect(() => { fetchData(); }, [fetchData]);

  async function handleStatusChange(taskId: number, status: string) {
    try { await api.updateTask(taskId, { status }); fetchData(); }
    catch (e) { console.error("Failed to update status:", e); }
  }

  async function handlePriorityChange(taskId: number, priority: string) {
    try { await api.updateTask(taskId, { priority }); fetchData(); }
    catch (e) { console.error("Failed to update priority:", e); }
  }

  function handleTaskClick(task: TaskSchema) { setSelectedTask(task); }

  function handleTimelineClick(item: TaskTimelineItem) {
    const found = listData.find((t) => t.id === item.id);
    if (found) setSelectedTask(found);
    else api.getTask(item.id).then(setSelectedTask).catch(console.error);
  }

  function renderRow(task: TaskSchema) {
    const statusCfg = STATUS_CONFIG[task.status as TaskStatus];
    const overdue = isOverdue(task.due_date) && task.status !== "DONE" && task.status !== "CANCELLED";
    return (
      <>
        <td className="px-3 py-2">
          <div className="flex items-center gap-2">
            <span className="text-xs font-mono text-gray-400 shrink-0">{task.identifier}</span>
            <span className="text-gray-900 dark:text-gray-100 truncate">{task.title}</span>
            {task.labels.length > 0 && (
              <span className="text-xs px-1.5 py-0.5 rounded bg-blue-50 dark:bg-blue-900/30 text-blue-600 dark:text-blue-300 shrink-0">
                {task.labels[0]}{task.labels.length > 1 && `+${task.labels.length - 1}`}
              </span>
            )}
          </div>
        </td>
        <td className="px-3 py-2" onClick={(e) => e.stopPropagation()}>
          <select value={task.status} onChange={(e) => handleStatusChange(task.id, e.target.value)}
            className={`text-xs font-medium rounded px-2 py-1 border-0 ${statusCfg?.bgColor ?? "bg-gray-100"} ${statusCfg?.color ?? "text-gray-600"}`}>
            {Object.entries(STATUS_CONFIG).map(([k, v]) => (<option key={k} value={k}>{v.label}</option>))}
          </select>
        </td>
        <td className="px-3 py-2" onClick={(e) => e.stopPropagation()}>
          <select value={task.priority} onChange={(e) => handlePriorityChange(task.id, e.target.value)}
            className="text-xs rounded px-1 py-1 border-0 bg-transparent">
            {Object.entries(PRIORITY_CONFIG).map(([k, v]) => (<option key={k} value={k}>{v.label}</option>))}
          </select>
        </td>
        <td className="px-3 py-2 text-gray-500 dark:text-gray-400 truncate">{task.assignee || "\u2014"}</td>
        <td className={`px-3 py-2 text-xs ${overdue ? "text-red-500 font-medium" : "text-gray-500 dark:text-gray-400"}`}>
          {task.due_date ? new Date(task.due_date).toLocaleDateString("en-GB", { day: "numeric", month: "short" }) : "\u2014"}
        </td>
        <td className="px-3 py-2 text-xs text-gray-400 truncate">{task.project_name || "\u2014"}</td>
      </>
    );
  }

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <GenericViewSwitcher view={view} onViewChange={handleViewChange} views={BOARD_LIST_TIMELINE_VIEWS}
          filters={filters} onFilterChange={handleFilterChange} filterDefs={filterDefs}
          showFilters={showFilters} onToggleFilters={() => setShowFilters(!showFilters)} />
        <button onClick={() => setShowCreate(true)}
          className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white text-sm font-medium rounded-lg hover:bg-blue-700 transition-colors">
          <Plus className="h-4 w-4" /> New Task
        </button>
      </div>

      {loading && <div className="flex items-center justify-center py-12"><div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600" /></div>}

      {!loading && view === "board" && boardData && (
        <GenericBoard columns={taskBoardConfig.toColumns(boardData)} statusConfig={taskBoardConfig.statusConfig}
          entityName={taskBoardConfig.entityName}
          renderCard={(item, onClick) => <TaskCard task={item} onClick={() => onClick(item)} />}
          renderDragOverlay={(item) => <TaskCard task={item} onClick={() => {}} isDragging />}
          onItemClick={handleTaskClick} updatePosition={taskBoardConfig.updatePosition} onRefresh={fetchData} />
      )}

      {!loading && view === "list" && (
        <GenericList items={listData} columns={listColumns} groupOptions={listGroupOptions}
          entityName="tasks" renderRow={renderRow} onItemClick={handleTaskClick} />
      )}

      {!loading && view === "timeline" && timelineData && (
        <GenericTimeline items={timelineData.tasks} entityName="Task"
          getDates={(item) => ({ start: item.start_date ?? item.due_date, end: item.due_date ?? null })}
          renderLabel={(item) => {
            const priorityCfg = PRIORITY_CONFIG[item.priority as TaskPriority];
            return (
              <div className="flex items-center gap-2">
                {priorityCfg && <span className={`w-2 h-2 rounded-full shrink-0 ${priorityCfg.dotColor}`} />}
                <div className="min-w-0">
                  <p className="text-sm text-gray-900 dark:text-gray-100 truncate">{item.title}</p>
                  <p className="text-xs text-gray-400">{item.identifier} {item.assignee && `\u00B7 ${item.assignee}`}</p>
                </div>
              </div>
            );
          }}
          renderMarker={(item, layout) => {
            const statusCfg = STATUS_CONFIG[item.status as TaskStatus];
            const barColor = statusCfg?.bgColor ?? "bg-gray-200";
            const textColor = statusCfg?.color ?? "text-gray-600";
            if (layout.isPoint) {
              return <div className={`absolute top-1/2 -translate-y-1/2 -translate-x-1/2 w-4 h-4 rotate-45 ${barColor} border-2 ${textColor} cursor-pointer z-20`}
                style={{ left: `${layout.leftPct}%` }} onClick={() => handleTimelineClick(item)} title={item.title} />;
            }
            return (
              <div className={`absolute h-6 top-1/2 -translate-y-1/2 rounded ${barColor} border ${textColor} cursor-pointer flex items-center px-2`}
                style={{ left: `${layout.leftPct}%`, width: `${Math.max(layout.widthPct, 1)}%`, minWidth: "24px" }}
                onClick={() => handleTimelineClick(item)}
                title={`${item.title} (${item.start_date ?? "?"} \u2192 ${item.due_date ?? "?"})`}>
                <span className={`text-xs truncate ${textColor} font-medium`}>{item.identifier}</span>
              </div>
            );
          }}
          onItemClick={handleTimelineClick} />
      )}

      {selectedTask && (
        <TaskDetailPanel task={selectedTask} onClose={() => setSelectedTask(null)}
          onUpdated={() => { setSelectedTask(null); fetchData(); }}
          projects={projects} existingLabels={allLabels} />
      )}

      <TaskCreateModal open={showCreate} onClose={() => setShowCreate(false)} onCreated={fetchData}
        projects={projects} existingLabels={allLabels} />
    </div>
  );
}
