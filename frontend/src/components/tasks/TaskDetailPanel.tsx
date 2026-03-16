"use client";

import { useState, useEffect, useCallback } from "react";
import { TaskSchema, TaskUpdate, TASK_STATUSES, TASK_PRIORITIES, STATUS_CONFIG, PRIORITY_CONFIG, TaskStatus, TaskPriority } from "@/lib/types";
import { api } from "@/lib/api";
import LabelTagInput from "./LabelTagInput";
import { X, Check, Trash2, ExternalLink } from "lucide-react";
import Link from "next/link";

interface TaskDetailPanelProps {
  task: TaskSchema;
  onClose: () => void;
  onUpdated: () => void;
  projects?: { id: number; name: string }[];
  existingLabels?: string[];
}

export default function TaskDetailPanel({ task, onClose, onUpdated, projects = [], existingLabels = [] }: TaskDetailPanelProps) {
  const [title, setTitle] = useState(task.title);
  const [description, setDescription] = useState(task.description || "");
  const [status, setStatus] = useState(task.status);
  const [priority, setPriority] = useState(task.priority);
  const [assignee, setAssignee] = useState(task.assignee || "");
  const [dueDate, setDueDate] = useState(task.due_date || "");
  const [startDate, setStartDate] = useState(task.start_date || "");
  const [estimate, setEstimate] = useState(task.estimate != null ? String(task.estimate) : "");
  const [projectId, setProjectId] = useState(task.project_id != null ? String(task.project_id) : "");
  const [labels, setLabels] = useState(task.labels);
  const [saving, setSaving] = useState(false);
  const [deleting, setDeleting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [dirty, setDirty] = useState(false);

  useEffect(() => {
    setTitle(task.title);
    setDescription(task.description || "");
    setStatus(task.status);
    setPriority(task.priority);
    setAssignee(task.assignee || "");
    setDueDate(task.due_date || "");
    setStartDate(task.start_date || "");
    setEstimate(task.estimate != null ? String(task.estimate) : "");
    setProjectId(task.project_id != null ? String(task.project_id) : "");
    setLabels(task.labels);
    setDirty(false);
    setError(null);
  }, [task]);

  function markDirty() { setDirty(true); }

  async function handleSave() {
    if (!title.trim()) { setError("Title is required"); return; }
    setSaving(true);
    setError(null);
    try {
      const body: TaskUpdate = {
        title: title.trim(),
        description: description || undefined,
        status,
        priority,
        assignee: assignee || undefined,
        due_date: dueDate || undefined,
        start_date: startDate || undefined,
        estimate: estimate ? parseInt(estimate, 10) : undefined,
        project_id: projectId ? parseInt(projectId, 10) : undefined,
        labels,
      };
      await api.updateTask(task.id, body);
      setDirty(false);
      onUpdated();
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : "Failed to save");
    } finally {
      setSaving(false);
    }
  }

  async function handleComplete() {
    setSaving(true);
    try {
      await api.completeTask(task.id);
      onUpdated();
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : "Failed to complete");
    } finally {
      setSaving(false);
    }
  }

  async function handleDelete() {
    if (!confirm("Delete this task? This cannot be undone.")) return;
    setDeleting(true);
    try {
      await api.deleteTask(task.id);
      onUpdated();
      onClose();
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : "Failed to delete");
    } finally {
      setDeleting(false);
    }
  }

  // Escape key to close
  const handleKeyDown = useCallback((e: KeyboardEvent) => {
    if (e.key === "Escape") onClose();
  }, [onClose]);
  useEffect(() => {
    document.addEventListener("keydown", handleKeyDown);
    return () => document.removeEventListener("keydown", handleKeyDown);
  }, [handleKeyDown]);

  return (
    <div className="fixed inset-0 z-40">
      {/* Backdrop — click to close */}
      <div className="absolute inset-0 bg-black/20" onClick={onClose} />
      <div className="absolute bg-white dark:bg-forest-800 dark:bg-forest-900 shadow-2xl flex flex-col md:inset-y-0 md:right-0 md:w-full md:max-w-md md:border-l md:border-forest-200 dark:md:border-gray-700 max-md:inset-x-0 max-md:bottom-0 max-md:top-[10vh] max-md:rounded-t-2xl max-md:border-t max-md:border-forest-200 dark:max-md:border-gray-700">
      {/* Mobile drag handle */}
      <div className="md:hidden flex justify-center pt-2 pb-1">
        <div className="w-10 h-1 bg-gray-300 dark:bg-forest-700 rounded-full" />
      </div>
      {/* Header */}
      <div className="flex items-center justify-between px-4 py-3 border-b border-forest-200 dark:border-forest-700">
        <div className="flex items-center gap-2">
          <span className="text-sm font-mono text-forest-300">{task.identifier}</span>
          {task.project_name && (
            <Link href={`/projects/${task.project_id}`} className="text-sm text-forest-500 hover:underline flex items-center gap-0.5">
              {task.project_name} <ExternalLink className="h-3 w-3" />
            </Link>
          )}
        </div>
        <button onClick={onClose} className="text-forest-300 hover:text-forest-500 dark:hover:text-gray-300">
          <X className="h-5 w-5" />
        </button>
      </div>

      {/* Body — scrollable */}
      <div className="flex-1 overflow-y-auto px-4 py-4 space-y-4">
        {error && (
          <div className="rounded-md bg-red-50 dark:bg-red-900/30 border border-red-200 dark:border-red-800 px-3 py-2">
            <p className="text-base text-red-700 dark:text-red-400">{error}</p>
          </div>
        )}

        {/* Title */}
        <input
          value={title}
          onChange={(e) => { setTitle(e.target.value); markDirty(); }}
          className="w-full text-lg font-semibold text-forest-950 dark:text-forest-50 bg-transparent border-0 focus:outline-none focus:ring-0 p-0"
          placeholder="Task title"
        />

        {/* Description */}
        <textarea
          value={description}
          onChange={(e) => { setDescription(e.target.value); markDirty(); }}
          rows={4}
          className="w-full text-base text-forest-600 dark:text-forest-200 bg-forest-50 dark:bg-forest-800 border border-forest-200 dark:border-forest-700 rounded-md px-3 py-2 focus:outline-none focus:ring-1 focus:ring-forest-500"
          placeholder="Add a description..."
        />

        {/* Status + Priority */}
        <div className="grid grid-cols-2 gap-3">
          <div>
            <label className="block text-sm font-medium text-forest-400 dark:text-forest-300 mb-1">Status</label>
            <select
              value={status}
              onChange={(e) => { setStatus(e.target.value as TaskStatus); markDirty(); }}
              className="w-full text-base border border-forest-200 dark:border-forest-700 rounded-md px-2 py-1.5 bg-white dark:bg-forest-800 text-forest-950 dark:text-forest-50"
            >
              {TASK_STATUSES.map((s) => (
                <option key={s} value={s}>{STATUS_CONFIG[s].label}</option>
              ))}
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium text-forest-400 dark:text-forest-300 mb-1">Priority</label>
            <select
              value={priority}
              onChange={(e) => { setPriority(e.target.value as TaskPriority); markDirty(); }}
              className="w-full text-base border border-forest-200 dark:border-forest-700 rounded-md px-2 py-1.5 bg-white dark:bg-forest-800 text-forest-950 dark:text-forest-50"
            >
              {TASK_PRIORITIES.map((p) => (
                <option key={p} value={p}>{PRIORITY_CONFIG[p].label}</option>
              ))}
            </select>
          </div>
        </div>

        {/* Assignee */}
        <div>
          <label className="block text-sm font-medium text-forest-400 dark:text-forest-300 mb-1">Assignee</label>
          <input
            value={assignee}
            onChange={(e) => { setAssignee(e.target.value); markDirty(); }}
            className="w-full text-base border border-forest-200 dark:border-forest-700 rounded-md px-2 py-1.5 bg-white dark:bg-forest-800 text-forest-950 dark:text-forest-50"
            placeholder="Who's responsible?"
          />
        </div>

        {/* Dates */}
        <div className="grid grid-cols-2 gap-3">
          <div>
            <label className="block text-sm font-medium text-forest-400 dark:text-forest-300 mb-1">Start Date</label>
            <input
              type="date"
              value={startDate}
              onChange={(e) => { setStartDate(e.target.value); markDirty(); }}
              className="w-full text-base border border-forest-200 dark:border-forest-700 rounded-md px-2 py-1.5 bg-white dark:bg-forest-800 text-forest-950 dark:text-forest-50"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-forest-400 dark:text-forest-300 mb-1">Due Date</label>
            <input
              type="date"
              value={dueDate}
              onChange={(e) => { setDueDate(e.target.value); markDirty(); }}
              className="w-full text-base border border-forest-200 dark:border-forest-700 rounded-md px-2 py-1.5 bg-white dark:bg-forest-800 text-forest-950 dark:text-forest-50"
            />
          </div>
        </div>

        {/* Estimate */}
        <div>
          <label className="block text-sm font-medium text-forest-400 dark:text-forest-300 mb-1">Estimate (hours)</label>
          <input
            type="number"
            value={estimate}
            onChange={(e) => { setEstimate(e.target.value); markDirty(); }}
            className="w-full text-base border border-forest-200 dark:border-forest-700 rounded-md px-2 py-1.5 bg-white dark:bg-forest-800 text-forest-950 dark:text-forest-50"
            placeholder="0"
          />
        </div>

        {/* Project */}
        {projects.length > 0 && (
          <div>
            <label className="block text-sm font-medium text-forest-400 dark:text-forest-300 mb-1">Project</label>
            <select
              value={projectId}
              onChange={(e) => { setProjectId(e.target.value); markDirty(); }}
              className="w-full text-base border border-forest-200 dark:border-forest-700 rounded-md px-2 py-1.5 bg-white dark:bg-forest-800 text-forest-950 dark:text-forest-50"
            >
              <option value="">No project</option>
              {projects.map((p) => (
                <option key={p.id} value={String(p.id)}>{p.name}</option>
              ))}
            </select>
          </div>
        )}

        {/* Labels */}
        <div>
          <label className="block text-sm font-medium text-forest-400 dark:text-forest-300 mb-1">Labels</label>
          <LabelTagInput labels={labels} onChange={(l) => { setLabels(l); markDirty(); }} suggestions={existingLabels} />
        </div>

        {/* Metadata */}
        <div className="pt-2 border-t border-forest-200 dark:border-forest-700 text-sm text-forest-300 space-y-1">
          {task.created_date && <p>Created: {new Date(task.created_date).toLocaleDateString("en-GB", { day: "numeric", month: "short", year: "numeric" })}</p>}
          {task.completed_date && <p>Completed: {new Date(task.completed_date).toLocaleDateString("en-GB", { day: "numeric", month: "short", year: "numeric" })}</p>}
          {task.sub_task_count > 0 && <p>Sub-tasks: {task.sub_task_count}</p>}
        </div>
      </div>

      {/* Footer actions */}
      <div className="flex items-center justify-between px-4 py-3 border-t border-forest-200 dark:border-forest-700 bg-forest-50 dark:bg-forest-800/50">
        <div className="flex gap-2">
          <button
            onClick={handleDelete}
            disabled={deleting}
            className="flex items-center gap-1 px-3 py-1.5 text-sm text-red-600 hover:bg-red-50 dark:hover:bg-red-900/20 rounded-md transition-colors disabled:opacity-50"
          >
            <Trash2 className="h-3.5 w-3.5" />
            {deleting ? "Deleting..." : "Delete"}
          </button>
          {task.status !== "DONE" && (
            <button
              onClick={handleComplete}
              disabled={saving}
              className="flex items-center gap-1 px-3 py-1.5 text-sm text-green-600 hover:bg-green-50 dark:hover:bg-green-900/20 rounded-md transition-colors disabled:opacity-50"
            >
              <Check className="h-3.5 w-3.5" />
              Complete
            </button>
          )}
        </div>
        <button
          onClick={handleSave}
          disabled={saving || !dirty}
          className="px-4 py-1.5 text-base font-medium text-white bg-forest-500 rounded-md hover:bg-forest-600 transition-colors disabled:opacity-50"
        >
          {saving ? "Saving..." : "Save"}
        </button>
      </div>
    </div>
    </div>
  );
}
