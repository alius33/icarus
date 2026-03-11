"use client";

import { useEffect, useState, useCallback } from "react";
import { useSearchParams, useRouter, usePathname } from "next/navigation";
import {
  OpenThreadSchema,
  ThreadBoardResponse,
  THREAD_STATUS_CONFIG,
  THREAD_STATUSES,
  SEVERITY_CONFIG,
  THREAD_SEVERITIES,
  ThreadStatus,
  ThreadSeverity,
} from "@/lib/types";
import { api } from "@/lib/api";
import GenericBoard from "@/components/generic/GenericBoard";
import GenericList, { ColumnDef, GroupOption } from "@/components/generic/GenericList";
import GenericViewSwitcher, {
  BOARD_LIST_VIEWS,
  FilterDef,
} from "@/components/generic/GenericViewSwitcher";
import { threadBoardConfig } from "@/config/board-configs";
import ThreadCard from "@/components/threads/ThreadCard";
import ThreadDetailPanel from "@/components/threads/ThreadDetailPanel";
import ThreadCreateModal from "@/components/threads/ThreadCreateModal";
import { Plus } from "lucide-react";

function trendLabel(trend: string | null): string {
  if (!trend) return "Unknown";
  if (trend === "escalating") return "\u2191 Escalating";
  if (trend === "stable") return "\u2192 Stable";
  if (trend === "de-escalating") return "\u2193 De-escalating";
  return trend;
}

const listColumns: ColumnDef<OpenThreadSchema>[] = [
  { key: "title", label: "Thread", sortable: true, sortValue: (t) => t.title.toLowerCase() },
  { key: "status", label: "Status", width: "w-28", sortable: true, sortValue: (t) => THREAD_STATUS_CONFIG[t.status as ThreadStatus]?.order ?? 99 },
  { key: "severity", label: "Severity", width: "w-24", sortable: true, sortValue: (t) => { const o: Record<string, number> = { CRITICAL: 0, HIGH: 1, MEDIUM: 2, LOW: 3 }; return o[t.severity ?? ""] ?? 4; } },
  { key: "trend", label: "Trend", width: "w-32", sortable: true, sortValue: (t) => { const o: Record<string, number> = { escalating: 0, stable: 1, "de-escalating": 2 }; return o[t.trend ?? ""] ?? 3; } },
  { key: "opened_date", label: "First Raised", width: "w-28", sortable: true, sortValue: (t) => t.opened_date ?? "zzz" },
];

const listGroupOptions: GroupOption[] = [
  { key: "status", label: "Status", groupFn: (item) => { const t = item as OpenThreadSchema; return THREAD_STATUS_CONFIG[t.status as ThreadStatus]?.label ?? t.status; } },
  { key: "severity", label: "Severity", groupFn: (item) => { const t = item as OpenThreadSchema; return SEVERITY_CONFIG[t.severity as ThreadSeverity]?.label ?? (t.severity || "Unknown"); } },
  { key: "trend", label: "Trend", groupFn: (item) => trendLabel((item as OpenThreadSchema).trend) },
];

const filterDefs: FilterDef[] = [
  { key: "status", label: "Status", type: "select", options: THREAD_STATUSES.map((s) => ({ value: s, label: THREAD_STATUS_CONFIG[s].label })) },
  { key: "severity", label: "Severity", type: "select", options: THREAD_SEVERITIES.map((s) => ({ value: s, label: SEVERITY_CONFIG[s].label })) },
  { key: "trend", label: "Trend", type: "select", options: [{ value: "escalating", label: "\u2191 Escalating" }, { value: "stable", label: "\u2192 Stable" }, { value: "de-escalating", label: "\u2193 De-escalating" }] },
  { key: "search", label: "Search", type: "text", placeholder: "Search threads..." },
];

interface Props { projectId: number; }

export default function ProjectThreadsTab({ projectId }: Props) {
  const searchParams = useSearchParams();
  const router = useRouter();
  const pathname = usePathname();

  const view = searchParams.get("view") || "board";

  const [filters, setFilters] = useState({
    status: searchParams.get("status") || "",
    severity: searchParams.get("severity") || "",
    trend: searchParams.get("trend") || "",
    search: searchParams.get("search") || "",
  });
  const [showFilters, setShowFilters] = useState(Object.values(filters).some(Boolean));

  const [boardData, setBoardData] = useState<ThreadBoardResponse | null>(null);
  const [listData, setListData] = useState<OpenThreadSchema[]>([]);
  const [loading, setLoading] = useState(true);

  const [selectedThread, setSelectedThread] = useState<OpenThreadSchema | null>(null);
  const [showCreate, setShowCreate] = useState(false);

  function updateUrlParams(newView?: string, newFilters?: Record<string, string>) {
    const params = new URLSearchParams();
    params.set("tab", "threads");
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
        setBoardData(await api.getThreadBoard(projectId));
      } else {
        const params: Record<string, string> = { project_id: String(projectId) };
        if (filters.status) params.status = filters.status;
        if (filters.severity) params.severity = filters.severity;
        if (filters.trend) params.trend = filters.trend;
        if (filters.search) params.search = filters.search;
        setListData(await api.getOpenThreads(params));
      }
    } catch (e) { console.error("Failed to fetch threads:", e); }
    finally { setLoading(false); }
  }, [view, filters, projectId]);

  useEffect(() => { fetchData(); }, [fetchData]);

  async function handleStatusChange(threadId: number, status: string) {
    try { await api.updateOpenThread(threadId, { status }); fetchData(); }
    catch (e) { console.error("Failed to update status:", e); }
  }

  function handleThreadClick(thread: OpenThreadSchema) { setSelectedThread(thread); }

  function renderRow(thread: OpenThreadSchema) {
    const statusCfg = THREAD_STATUS_CONFIG[thread.status as ThreadStatus];
    const severityCfg = SEVERITY_CONFIG[thread.severity as ThreadSeverity];
    return (
      <>
        <td className="px-3 py-2">
          <div className="flex items-center gap-2">
            {severityCfg && <span className={`w-2 h-2 rounded-full shrink-0 ${severityCfg.dotColor}`} />}
            <span className="text-gray-900 dark:text-gray-100 truncate">{thread.title}</span>
          </div>
        </td>
        <td className="px-3 py-2" onClick={(e) => e.stopPropagation()}>
          <select value={thread.status} onChange={(e) => handleStatusChange(thread.id, e.target.value)}
            className={`text-xs font-medium rounded px-2 py-1 border-0 ${statusCfg?.bgColor ?? "bg-gray-100"} ${statusCfg?.color ?? "text-gray-600"}`}>
            {THREAD_STATUSES.map((s) => (<option key={s} value={s}>{THREAD_STATUS_CONFIG[s].label}</option>))}
          </select>
        </td>
        <td className="px-3 py-2">
          <span className="flex items-center gap-1.5">
            <span className={`w-2 h-2 rounded-full ${severityCfg?.dotColor ?? "bg-gray-300"}`} />
            <span className="text-xs">{severityCfg?.label ?? (thread.severity || "None")}</span>
          </span>
        </td>
        <td className="px-3 py-2">
          {thread.trend && (
            <span className={`text-xs font-medium px-2 py-0.5 rounded-full ${
              thread.trend === "escalating" ? "bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-400" :
              thread.trend === "stable" ? "bg-yellow-100 text-yellow-700 dark:bg-yellow-900/30 dark:text-yellow-400" :
              "bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400"
            }`}>{trendLabel(thread.trend)}</span>
          )}
        </td>
        <td className="px-3 py-2 text-xs text-gray-500 dark:text-gray-400">
          {thread.opened_date ? new Date(thread.opened_date).toLocaleDateString("en-GB", { day: "numeric", month: "short" }) : "\u2014"}
        </td>
      </>
    );
  }

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <GenericViewSwitcher view={view} onViewChange={handleViewChange} views={BOARD_LIST_VIEWS}
          filters={filters} onFilterChange={handleFilterChange} filterDefs={filterDefs}
          showFilters={showFilters} onToggleFilters={() => setShowFilters(!showFilters)} />
        <button onClick={() => setShowCreate(true)}
          className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white text-sm font-medium rounded-lg hover:bg-blue-700 transition-colors">
          <Plus className="h-4 w-4" /> New Thread
        </button>
      </div>

      {loading && <div className="flex items-center justify-center py-12"><div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600" /></div>}

      {!loading && view === "board" && boardData && (
        <GenericBoard columns={threadBoardConfig.toColumns(boardData)} statusConfig={threadBoardConfig.statusConfig}
          entityName={threadBoardConfig.entityName}
          renderCard={(item, onClick) => <ThreadCard thread={item} onClick={() => onClick(item)} />}
          renderDragOverlay={(item) => <ThreadCard thread={item} onClick={() => {}} isDragging />}
          onItemClick={handleThreadClick} updatePosition={threadBoardConfig.updatePosition} onRefresh={fetchData} />
      )}

      {!loading && view === "list" && (
        <GenericList items={listData} columns={listColumns} groupOptions={listGroupOptions}
          entityName="threads" renderRow={renderRow} onItemClick={handleThreadClick} />
      )}

      {selectedThread && (
        <ThreadDetailPanel thread={selectedThread} onClose={() => setSelectedThread(null)}
          onUpdated={() => { setSelectedThread(null); fetchData(); }} />
      )}

      <ThreadCreateModal open={showCreate} onClose={() => setShowCreate(false)} onCreated={fetchData} />
    </div>
  );
}
