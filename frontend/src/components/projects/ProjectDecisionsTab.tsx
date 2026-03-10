"use client";

import { useEffect, useState, useCallback } from "react";
import { useSearchParams, useRouter, usePathname } from "next/navigation";
import { DecisionSchema, DecisionBoardResponse, DecisionTimelineResponse, DecisionViewMode } from "@/lib/types";
import { api } from "@/lib/api";
import DecisionBoard from "@/components/decisions/DecisionBoard";
import DecisionList from "@/components/decisions/DecisionList";
import DecisionTimeline from "@/components/decisions/DecisionTimeline";
import DecisionDetailPanel from "@/components/decisions/DecisionDetailPanel";
import DecisionCreateModal from "@/components/decisions/DecisionCreateModal";
import DecisionViewSwitcher from "@/components/decisions/DecisionViewSwitcher";
import { Plus } from "lucide-react";

interface Props {
  projectId: number;
}

export default function ProjectDecisionsTab({ projectId }: Props) {
  const searchParams = useSearchParams();
  const router = useRouter();
  const pathname = usePathname();

  const view = (searchParams.get("view") as DecisionViewMode) || "board";

  const [filters, setFilters] = useState({
    execution_status: searchParams.get("execution_status") || "",
    workstream: "",
    search: searchParams.get("search") || "",
  });
  const [showFilters, setShowFilters] = useState(Object.values(filters).some(Boolean));

  const [boardData, setBoardData] = useState<DecisionBoardResponse | null>(null);
  const [listData, setListData] = useState<DecisionSchema[]>([]);
  const [timelineData, setTimelineData] = useState<DecisionTimelineResponse | null>(null);
  const [loading, setLoading] = useState(true);

  const [selectedDecision, setSelectedDecision] = useState<DecisionSchema | null>(null);
  const [showCreate, setShowCreate] = useState(false);

  function updateUrlParams(newView?: DecisionViewMode, newFilters?: Record<string, string>) {
    const params = new URLSearchParams();
    params.set("tab", "decisions");
    const v = newView ?? view;
    if (v !== "board") params.set("view", v);
    const f = newFilters ?? filters;
    Object.entries(f).forEach(([k, val]) => { if (val) params.set(k, val); });
    const qs = params.toString();
    router.replace(`${pathname}?${qs}`, { scroll: false });
  }

  function handleViewChange(v: DecisionViewMode) {
    updateUrlParams(v);
  }

  function handleFilterChange(key: string, value: string) {
    const next = { ...filters, [key]: value };
    setFilters(next);
    updateUrlParams(undefined, next);
  }

  const fetchData = useCallback(async () => {
    setLoading(true);
    try {
      if (view === "board") {
        const data = await api.getDecisionBoard(undefined, projectId);
        setBoardData(data);
      } else if (view === "list") {
        const params: Record<string, string> = { project_id: String(projectId) };
        if (filters.execution_status) params.execution_status = filters.execution_status;
        if (filters.search) params.search = filters.search;
        const data = await api.getDecisions(params);
        setListData(data);
      } else {
        const data = await api.getDecisionTimeline(undefined, projectId);
        setTimelineData(data);
      }
    } catch (e) {
      console.error("Failed to fetch decisions:", e);
    } finally {
      setLoading(false);
    }
  }, [view, filters, projectId]);

  useEffect(() => {
    fetchData();
  }, [fetchData]);

  async function handleStatusChange(decisionId: number, executionStatus: string) {
    try {
      await api.updateDecision(decisionId, { execution_status: executionStatus });
      fetchData();
    } catch (e) {
      console.error("Failed to update status:", e);
    }
  }

  function handleDecisionClick(decision: DecisionSchema) {
    setSelectedDecision(decision);
  }

  function handleTimelineDecisionClick(decisionId: number) {
    const found = listData.find((d) => d.id === decisionId);
    if (found) {
      setSelectedDecision(found);
    } else {
      api.getDecision(decisionId).then(setSelectedDecision).catch(console.error);
    }
  }

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <DecisionViewSwitcher
          view={view}
          onViewChange={handleViewChange}
          filters={filters}
          onFilterChange={handleFilterChange}
          showFilters={showFilters}
          onToggleFilters={() => setShowFilters(!showFilters)}
        />
        <button
          onClick={() => setShowCreate(true)}
          className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white text-sm font-medium rounded-lg hover:bg-blue-700 transition-colors"
        >
          <Plus className="h-4 w-4" />
          New Decision
        </button>
      </div>

      {loading && (
        <div className="flex items-center justify-center py-12">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600" />
        </div>
      )}

      {!loading && view === "board" && boardData && (
        <DecisionBoard data={boardData} onDecisionClick={handleDecisionClick} onRefresh={fetchData} />
      )}

      {!loading && view === "list" && (
        <DecisionList
          decisions={listData}
          onDecisionClick={handleDecisionClick}
          onStatusChange={handleStatusChange}
        />
      )}

      {!loading && view === "timeline" && timelineData && (
        <DecisionTimeline
          decisions={timelineData.decisions}
          onDecisionClick={handleTimelineDecisionClick}
        />
      )}

      {selectedDecision && (
        <DecisionDetailPanel
          decision={selectedDecision}
          onClose={() => setSelectedDecision(null)}
          onUpdated={() => {
            setSelectedDecision(null);
            fetchData();
          }}
        />
      )}

      <DecisionCreateModal
        open={showCreate}
        onClose={() => setShowCreate(false)}
        onCreated={fetchData}
      />
    </div>
  );
}
