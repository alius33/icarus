"use client";

import { Suspense, useEffect, useState, useCallback } from "react";
import { useSearchParams, useRouter } from "next/navigation";
import { TaskSchema, TaskBoardResponse, TaskTimelineResponse, TaskViewMode } from "@/lib/types";
import { api } from "@/lib/api";
import TaskBoard from "@/components/tasks/TaskBoard";
import TaskList from "@/components/tasks/TaskList";
import TaskTimeline from "@/components/tasks/TaskTimeline";
import TaskDetailPanel from "@/components/tasks/TaskDetailPanel";
import TaskCreateModal from "@/components/tasks/TaskCreateModal";
import TaskViewSwitcher from "@/components/tasks/TaskViewSwitcher";
import { Plus } from "lucide-react";

export default function TasksPage() {
  return (
    <Suspense fallback={<div className="flex items-center justify-center py-12"><div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600" /></div>}>
      <TasksContent />
    </Suspense>
  );
}

function TasksContent() {
  const searchParams = useSearchParams();
  const router = useRouter();

  const view = (searchParams.get("view") as TaskViewMode) || "board";

  const [filters, setFilters] = useState({
    status: searchParams.get("status") || "",
    priority: searchParams.get("priority") || "",
    assignee: searchParams.get("assignee") || "",
    project_id: searchParams.get("project_id") || "",
    label: searchParams.get("label") || "",
  });
  const [showFilters, setShowFilters] = useState(
    Object.values(filters).some(Boolean)
  );

  // Data states
  const [boardData, setBoardData] = useState<TaskBoardResponse | null>(null);
  const [listData, setListData] = useState<TaskSchema[]>([]);
  const [timelineData, setTimelineData] = useState<TaskTimelineResponse | null>(null);
  const [loading, setLoading] = useState(true);

  // UI states
  const [selectedTask, setSelectedTask] = useState<TaskSchema | null>(null);
  const [showCreate, setShowCreate] = useState(false);
  const [projects, setProjects] = useState<{ id: number; name: string }[]>([]);
  const [allLabels, setAllLabels] = useState<string[]>([]);
  const [assignees, setAssignees] = useState<string[]>([]);

  function updateUrlParams(newView?: TaskViewMode, newFilters?: Record<string, string>) {
    const params = new URLSearchParams();
    const v = newView ?? view;
    if (v !== "board") params.set("view", v);
    const f = newFilters ?? filters;
    Object.entries(f).forEach(([k, val]) => { if (val) params.set(k, val); });
    const qs = params.toString();
    router.replace(`/tasks${qs ? `?${qs}` : ""}`, { scroll: false });
  }

  function handleViewChange(v: TaskViewMode) {
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
      const params: Record<string, string> = {};
      if (filters.status) params.status = filters.status;
      if (filters.priority) params.priority = filters.priority;
      if (filters.assignee) params.assignee = filters.assignee;
      if (filters.project_id) params.project_id = filters.project_id;
      if (filters.label) params.label = filters.label;

      if (view === "board") {
        const data = await api.getTaskBoard(filters.project_id ? parseInt(filters.project_id) : undefined);
        setBoardData(data);
      } else if (view === "list") {
        const data = await api.getTasks(params);
        setListData(data);
      } else {
        const data = await api.getTaskTimeline(filters.project_id ? parseInt(filters.project_id) : undefined);
        setTimelineData(data);
      }
    } catch (e) {
      console.error("Failed to fetch tasks:", e);
    } finally {
      setLoading(false);
    }
  }, [view, filters]);

  // Load metadata (projects, labels)
  useEffect(() => {
    async function loadMeta() {
      try {
        const [projectsData, labelsData] = await Promise.all([
          api.getProjects() as Promise<{ id: number; name: string }[]>,
          api.getTaskLabels(),
        ]);
        setProjects(projectsData);
        setAllLabels(labelsData);
      } catch {
        // metadata is optional
      }
    }
    loadMeta();
  }, []);

  // Extract unique assignees from list data
  useEffect(() => {
    if (listData.length > 0) {
      const unique = Array.from(new Set(listData.map((t) => t.assignee).filter(Boolean) as string[]));
      setAssignees(unique);
    }
  }, [listData]);

  // Fetch data on view/filter change
  useEffect(() => {
    fetchData();
  }, [fetchData]);

  async function handleStatusChange(taskId: number, status: string) {
    try {
      await api.updateTask(taskId, { status });
      fetchData();
    } catch (e) {
      console.error("Failed to update status:", e);
    }
  }

  async function handlePriorityChange(taskId: number, priority: string) {
    try {
      await api.updateTask(taskId, { priority });
      fetchData();
    } catch (e) {
      console.error("Failed to update priority:", e);
    }
  }

  function handleTaskClick(task: TaskSchema) {
    setSelectedTask(task);
  }

  function handleTimelineTaskClick(taskId: number) {
    // Find from board or list data, or fetch individually
    const found = listData.find((t) => t.id === taskId);
    if (found) {
      setSelectedTask(found);
    } else {
      // Fetch the task individually
      api.getTask(taskId).then(setSelectedTask).catch(console.error);
    }
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900 dark:text-gray-100">Tasks</h1>
          <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">
            Manage and track project tasks across all workstreams
          </p>
        </div>
        <button
          onClick={() => setShowCreate(true)}
          className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white text-sm font-medium rounded-lg hover:bg-blue-700 transition-colors"
        >
          <Plus className="h-4 w-4" />
          New Task
        </button>
      </div>

      {/* View switcher + filters */}
      <TaskViewSwitcher
        view={view}
        onViewChange={handleViewChange}
        filters={filters}
        onFilterChange={handleFilterChange}
        projects={projects}
        assignees={assignees}
        labels={allLabels}
        showFilters={showFilters}
        onToggleFilters={() => setShowFilters(!showFilters)}
      />

      {/* Loading state */}
      {loading && (
        <div className="flex items-center justify-center py-12">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600" />
        </div>
      )}

      {/* Views */}
      {!loading && view === "board" && boardData && (
        <TaskBoard data={boardData} onTaskClick={handleTaskClick} onRefresh={fetchData} />
      )}

      {!loading && view === "list" && (
        <TaskList
          tasks={listData}
          onTaskClick={handleTaskClick}
          onStatusChange={handleStatusChange}
          onPriorityChange={handlePriorityChange}
        />
      )}

      {!loading && view === "timeline" && timelineData && (
        <TaskTimeline tasks={timelineData.tasks} onTaskClick={handleTimelineTaskClick} />
      )}

      {/* Detail panel */}
      {selectedTask && (
        <TaskDetailPanel
          task={selectedTask}
          onClose={() => setSelectedTask(null)}
          onUpdated={() => {
            setSelectedTask(null);
            fetchData();
          }}
          projects={projects}
          existingLabels={allLabels}
        />
      )}

      {/* Create modal */}
      <TaskCreateModal
        open={showCreate}
        onClose={() => setShowCreate(false)}
        onCreated={fetchData}
        projects={projects}
        existingLabels={allLabels}
      />
    </div>
  );
}
