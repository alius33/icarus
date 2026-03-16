"use client";

import { useEffect, useState, useCallback } from "react";
import { useSearchParams, useRouter, usePathname } from "next/navigation";
import { OpenThreadSchema, ThreadBoardResponse, ThreadViewMode } from "@/lib/types";
import { api } from "@/lib/api";
import ThreadBoard from "@/components/threads/ThreadBoard";
import ThreadList from "@/components/threads/ThreadList";
import ThreadDetailPanel from "@/components/threads/ThreadDetailPanel";
import ThreadCreateModal from "@/components/threads/ThreadCreateModal";
import ThreadViewSwitcher from "@/components/threads/ThreadViewSwitcher";
import { Plus } from "lucide-react";

interface Props {
  projectId: number;
}

export default function ProjectThreadsTab({ projectId }: Props) {
  const searchParams = useSearchParams();
  const router = useRouter();
  const pathname = usePathname();

  const view = (searchParams.get("view") as ThreadViewMode) || "board";

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

  function updateUrlParams(newView?: ThreadViewMode, newFilters?: Record<string, string>) {
    const params = new URLSearchParams();
    params.set("tab", "threads");
    const v = newView ?? view;
    if (v !== "board") params.set("view", v);
    const f = newFilters ?? filters;
    Object.entries(f).forEach(([k, val]) => { if (val) params.set(k, val); });
    const qs = params.toString();
    router.replace(`${pathname}?${qs}`, { scroll: false });
  }

  function handleViewChange(v: ThreadViewMode) {
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
        const data = await api.getThreadBoard(projectId);
        setBoardData(data);
      } else {
        const params: Record<string, string> = { project_id: String(projectId) };
        if (filters.status) params.status = filters.status;
        if (filters.severity) params.severity = filters.severity;
        if (filters.trend) params.trend = filters.trend;
        if (filters.search) params.search = filters.search;
        const data = await api.getOpenThreads(params);
        setListData(data);
      }
    } catch (e) {
      console.error("Failed to fetch threads:", e);
    } finally {
      setLoading(false);
    }
  }, [view, filters, projectId]);

  useEffect(() => {
    fetchData();
  }, [fetchData]);

  async function handleStatusChange(threadId: number, status: string) {
    try {
      await api.updateOpenThread(threadId, { status });
      fetchData();
    } catch (e) {
      console.error("Failed to update status:", e);
    }
  }

  function handleThreadClick(thread: OpenThreadSchema) {
    setSelectedThread(thread);
  }

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <ThreadViewSwitcher
          view={view}
          onViewChange={handleViewChange}
          filters={filters}
          onFilterChange={handleFilterChange}
          showFilters={showFilters}
          onToggleFilters={() => setShowFilters(!showFilters)}
        />
        <button
          onClick={() => setShowCreate(true)}
          className="flex items-center gap-2 px-4 py-2 bg-forest-500 text-white text-base font-medium rounded-lg hover:bg-forest-600 transition-colors"
        >
          <Plus className="h-4 w-4" />
          New Thread
        </button>
      </div>

      {loading && (
        <div className="flex items-center justify-center py-12">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-forest-500" />
        </div>
      )}

      {!loading && view === "board" && boardData && (
        <ThreadBoard data={boardData} onThreadClick={handleThreadClick} onRefresh={fetchData} />
      )}

      {!loading && view === "list" && (
        <ThreadList
          threads={listData}
          onThreadClick={handleThreadClick}
          onStatusChange={handleStatusChange}
        />
      )}

      {selectedThread && (
        <ThreadDetailPanel
          thread={selectedThread}
          onClose={() => setSelectedThread(null)}
          onUpdated={() => {
            setSelectedThread(null);
            fetchData();
          }}
        />
      )}

      <ThreadCreateModal
        open={showCreate}
        onClose={() => setShowCreate(false)}
        onCreated={fetchData}
      />
    </div>
  );
}
