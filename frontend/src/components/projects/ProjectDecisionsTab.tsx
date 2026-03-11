"use client";

import { useEffect, useState, useCallback } from "react";
import { useSearchParams, useRouter, usePathname } from "next/navigation";
import {
  DecisionSchema,
  DecisionBoardResponse,
  DecisionTimelineResponse,
  DecisionTimelineItem,
  DECISION_STATUS_CONFIG,
  DecisionStatus,
} from "@/lib/types";
import { api } from "@/lib/api";
import GenericBoard from "@/components/generic/GenericBoard";
import GenericList, { ColumnDef, GroupOption } from "@/components/generic/GenericList";
import GenericTimeline from "@/components/generic/GenericTimeline";
import GenericViewSwitcher, {
  BOARD_LIST_TIMELINE_VIEWS,
  FilterDef,
} from "@/components/generic/GenericViewSwitcher";
import { decisionBoardConfig } from "@/config/board-configs";
import DecisionCard from "@/components/decisions/DecisionCard";
import DecisionDetailPanel from "@/components/decisions/DecisionDetailPanel";
import DecisionCreateModal from "@/components/decisions/DecisionCreateModal";
import { Plus } from "lucide-react";

// Reuse column/group/filter configs from the decisions page pattern
const listColumns: ColumnDef<DecisionSchema>[] = [
  { key: "number", label: "#", width: "w-16", sortable: true, sortValue: (d) => d.number },
  { key: "date", label: "Date", width: "w-28", sortable: true, sortValue: (d) => d.date ?? "zzz" },
  { key: "title", label: "Decision", sortable: true, sortValue: (d) => d.title.toLowerCase() },
  { key: "execution_status", label: "Status", width: "w-32", sortable: true, sortValue: (d) => DECISION_STATUS_CONFIG[d.execution_status as DecisionStatus]?.order ?? 99 },
  { key: "workstream", label: "Workstream", width: "w-36", sortable: true, sortValue: (d) => d.workstream?.toLowerCase() ?? "zzz" },
  { key: "key_people", label: "Key People", width: "w-40", sortable: false },
];

const listGroupOptions: GroupOption[] = [
  { key: "execution_status", label: "Status", groupFn: (item) => { const d = item as DecisionSchema; return DECISION_STATUS_CONFIG[d.execution_status as DecisionStatus]?.label ?? d.execution_status; } },
  { key: "workstream", label: "Workstream", groupFn: (item) => (item as DecisionSchema).workstream || "No Workstream" },
];

const filterDefs: FilterDef[] = [
  { key: "execution_status", label: "Status", type: "select", options: Object.entries(DECISION_STATUS_CONFIG).map(([k, v]) => ({ value: k, label: v.label })) },
  { key: "search", label: "Search", type: "text", placeholder: "Search decisions..." },
];

interface Props {
  projectId: number;
}

export default function ProjectDecisionsTab({ projectId }: Props) {
  const searchParams = useSearchParams();
  const router = useRouter();
  const pathname = usePathname();

  const view = searchParams.get("view") || "board";

  const [filters, setFilters] = useState({
    execution_status: searchParams.get("execution_status") || "",
    search: searchParams.get("search") || "",
  });
  const [showFilters, setShowFilters] = useState(Object.values(filters).some(Boolean));

  const [boardData, setBoardData] = useState<DecisionBoardResponse | null>(null);
  const [listData, setListData] = useState<DecisionSchema[]>([]);
  const [timelineData, setTimelineData] = useState<DecisionTimelineResponse | null>(null);
  const [loading, setLoading] = useState(true);

  const [selectedDecision, setSelectedDecision] = useState<DecisionSchema | null>(null);
  const [showCreate, setShowCreate] = useState(false);

  function updateUrlParams(newView?: string, newFilters?: Record<string, string>) {
    const params = new URLSearchParams();
    params.set("tab", "decisions");
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
        setBoardData(await api.getDecisionBoard(undefined, projectId));
      } else if (view === "list") {
        const params: Record<string, string> = { project_id: String(projectId) };
        if (filters.execution_status) params.execution_status = filters.execution_status;
        if (filters.search) params.search = filters.search;
        setListData(await api.getDecisions(params));
      } else {
        setTimelineData(await api.getDecisionTimeline(undefined, projectId));
      }
    } catch (e) { console.error("Failed to fetch decisions:", e); }
    finally { setLoading(false); }
  }, [view, filters, projectId]);

  useEffect(() => { fetchData(); }, [fetchData]);

  async function handleStatusChange(decisionId: number, executionStatus: string) {
    try { await api.updateDecision(decisionId, { execution_status: executionStatus }); fetchData(); }
    catch (e) { console.error("Failed to update status:", e); }
  }

  function handleDecisionClick(decision: DecisionSchema) { setSelectedDecision(decision); }

  function handleTimelineClick(item: DecisionTimelineItem) {
    const found = listData.find((d) => d.id === item.id);
    if (found) setSelectedDecision(found);
    else api.getDecision(item.id).then(setSelectedDecision).catch(console.error);
  }

  function renderRow(decision: DecisionSchema) {
    const statusCfg = DECISION_STATUS_CONFIG[decision.execution_status as DecisionStatus];
    return (
      <>
        <td className="px-3 py-2"><span className="text-xs font-mono text-gray-400">#{decision.number}</span></td>
        <td className="px-3 py-2 text-xs text-gray-500 dark:text-gray-400">
          {decision.date ? new Date(decision.date).toLocaleDateString("en-GB", { day: "numeric", month: "short" }) : "\u2014"}
        </td>
        <td className="px-3 py-2"><span className="text-gray-900 dark:text-gray-100 truncate">{decision.title}</span></td>
        <td className="px-3 py-2" onClick={(e) => e.stopPropagation()}>
          <select value={decision.execution_status} onChange={(e) => handleStatusChange(decision.id, e.target.value)}
            className={`text-xs font-medium rounded px-2 py-1 border-0 ${statusCfg?.bgColor ?? "bg-gray-100"} ${statusCfg?.color ?? "text-gray-600"}`}>
            {Object.entries(DECISION_STATUS_CONFIG).map(([k, v]) => (<option key={k} value={k}>{v.label}</option>))}
          </select>
        </td>
        <td className="px-3 py-2 text-xs text-gray-400 truncate">{decision.workstream || "\u2014"}</td>
        <td className="px-3 py-2">
          <div className="flex flex-wrap gap-1">
            {decision.key_people.slice(0, 2).map((p) => (
              <span key={p} className="px-1.5 py-0.5 text-xs rounded bg-blue-50 dark:bg-blue-900/30 text-blue-600 dark:text-blue-300">{p}</span>
            ))}
            {decision.key_people.length > 2 && <span className="text-xs text-gray-400">+{decision.key_people.length - 2}</span>}
          </div>
        </td>
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
          <Plus className="h-4 w-4" /> New Decision
        </button>
      </div>

      {loading && <div className="flex items-center justify-center py-12"><div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600" /></div>}

      {!loading && view === "board" && boardData && (
        <GenericBoard columns={decisionBoardConfig.toColumns(boardData)} statusConfig={decisionBoardConfig.statusConfig}
          entityName={decisionBoardConfig.entityName}
          renderCard={(item, onClick) => <DecisionCard decision={item} onClick={() => onClick(item)} />}
          renderDragOverlay={(item) => <DecisionCard decision={item} onClick={() => {}} isDragging />}
          onItemClick={handleDecisionClick} updatePosition={decisionBoardConfig.updatePosition} onRefresh={fetchData} />
      )}

      {!loading && view === "list" && (
        <GenericList items={listData} columns={listColumns} groupOptions={listGroupOptions}
          entityName="decisions" renderRow={renderRow} onItemClick={handleDecisionClick} />
      )}

      {!loading && view === "timeline" && timelineData && (
        <GenericTimeline items={timelineData.decisions} entityName="Decision"
          getDates={(item) => ({ start: item.decision_date, end: item.decision_date })}
          renderLabel={(item) => {
            const cfg = DECISION_STATUS_CONFIG[item.execution_status as DecisionStatus];
            return (
              <div className="min-w-0">
                <p className="text-sm text-gray-900 dark:text-gray-100 truncate">{item.title}</p>
                <div className="flex items-center gap-2 mt-0.5">
                  <span className="text-xs font-mono text-gray-400">#{item.number}</span>
                  {cfg && <span className={`text-xs font-medium px-1 py-0.5 rounded ${cfg.bgColor} ${cfg.color}`}>{cfg.label}</span>}
                </div>
              </div>
            );
          }}
          renderMarker={(item, layout) => {
            const cfg = DECISION_STATUS_CONFIG[item.execution_status as DecisionStatus];
            return (
              <div className={`absolute top-1/2 -translate-y-1/2 -translate-x-1/2 w-4 h-4 rotate-45 ${cfg?.bgColor ?? "bg-gray-200"} border-2 ${cfg?.color ?? "text-gray-600"} cursor-pointer z-20`}
                style={{ left: `${layout.leftPct}%` }} onClick={() => handleTimelineClick(item)}
                title={`${item.title} (${item.decision_date})`} />
            );
          }}
          onItemClick={handleTimelineClick} />
      )}

      {selectedDecision && (
        <DecisionDetailPanel decision={selectedDecision} onClose={() => setSelectedDecision(null)}
          onUpdated={() => { setSelectedDecision(null); fetchData(); }} />
      )}

      <DecisionCreateModal open={showCreate} onClose={() => setShowCreate(false)} onCreated={fetchData} />
    </div>
  );
}
