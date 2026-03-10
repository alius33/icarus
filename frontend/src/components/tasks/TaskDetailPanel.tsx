"use client";

import { useState, useEffect } from "react";
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

  return (
    <div className="fixed inset-0 z-40">
      {/* Backdrop — click to close */}
      <div className="absolute inset-0 bg-black/20" onClick={onClose} />
      <div className="absolute inset-y-0 right-0 w-full max-w-md bg-white dark:bg-gray-900 shadow-2xl border-l border-gray-200 dark:border-gray-700 flex flex-col">
      {/* Header */}
      <div className="flex items-center justify-between px-4 py-3 border-b border-gray-200 dark:border-gray-700">
        <div className="flex items-center gap-2">
          <span className="text-xs font-mono text-gray-400">{task.identifier}</span>
          {task.project_name && (
            <Link href={`/projects/${task.project_id}`} className="text-xs text-blue-500 hover:underline flex items-center gap-0.5">
              {task.project_name} <ExternalLink className="h-3 w-3" />
            </Link>
          )}
        </div>
        <button onClick={onClose} className="text-gray-400 hover:text-gray-600 dark:hover:text-gray-300">
          <X className="h-5 w-5" />
        </button>
      </div>

      {/* Body — scrollable */}
      <div className="flex-1 overflow-y-auto px-4 py-4 space-y-4">
        {error && (
          <div className="rounded-md bg-red-50 dark:bg-red-900/30 border border-red-200 dark:border-red-800 px-3 py-2">
            <p className="text-sm text-red-700 dark:text-red-400">{error}</p>
          </div>
        )}

        {/* Title */}
        <input
          value={title}
          onChange={(e) => { setTitle(e.target.value); markDirty(); }}
          className="w-full text-lg font-semibold text-gray-900 dark:text-gray-100 bg-transparent border-0 focus:outline-none focus:ring-0 p-0"
          placeholder="Task title"
        />

        {/* Description */}
        <textarea
          value={description}
          onChange={(e) => { setDescription(e.target.value); markDirty(); }}
          rows={4}
          className="w-full text-sm text-gray-700 dark:text-gray-300 bg-gray-50 dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-md px-3 py-2 focus:outline-none focus:ring-1 focus:ring-blue-500"
          placeholder="Add a description..."
        />

        {/* Status + Priority */}
        <div className="grid grid-cols-2 gap-3">
          <div>
            <label className="block text-xs font-medium text-gray-500 dark:text-gray-400 mb-1">Status</label>
            <select
              value={status}
              onChange={(e) => { setStatus(e.target.value as TaskStatus); markDirty(); }}
              className="w-full text-sm border border-gray-300 dark:border-gray-600 rounded-md px-2 py-1.5 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100"
            >
              {TASK_STATUSES.map((s) => (
                <option key={s} value={s}>{STATUS_CONFIG[s].label}</option>
              ))}
            </select>
          </div>
          <div>
            <label className="block text-xs font-medium text-gray-500 dark:text-gray-400 mb-1">Priority</label>
            <select
              value={priority}
              onChange={(e) => { setPriority(e.target.value as TaskPriority); markDirty(); }}
              className="w-full text-sm border border-gray-300 dark:border-gray-600 rounded-md px-2 py-1.5 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100"
            >
              {TASK_PRIORITIES.map((p) => (
                <option key={p} value={p}>{PRIORITY_CONFIG[p].label}</option>
              ))}
            </select>
          </div>
        </div>

        {/* Assignee */}
        <div>
          <label className="block text-xs font-medium text-gray-500 dark:text-gray-400 mb-1">Assignee</label>
          <input
            value={assignee}
            onChange={(e) => { setAssignee(e.target.value); markDirty(); }}
            className="w-full text-sm border border-gray-300 dark:border-gray-600 rounded-md px-2 py-1.5 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100"
            placeholder="Who's responsible?"
          />
        </div>

        {/* Dates */}
        <div className="grid grid-cols-2 gap-3">
          <div>
            <label className="block text-xs font-medium text-gray-500 dark:text-gray-400 mb-1">Start Date</label>
            <input
              type="date"
              value={startDate}
              onChange={(e) => { setStartDate(e.target.value); markDirty(); }}
              className="w-full text-sm border border-gray-300 dark:border-gray-600 rounded-md px-2 py-1.5 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100"
            />
          </div>
          <div>
            <label className="block text-xs font-medium text-gray-500 dark:text-gray-400 mb-1">Due Date</label>
            <input
              type="date"
              value={dueDate}
              onChange={(e) => { setDueDate(e.target.value); markDirty(); }}
              className="w-full text-sm border border-gray-300 dark:border-gray-600 rounded-md px-2 py-1.5 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100"
            />
          </div>
        </div>

        {/* Estimate */}
        <div>
          <label className="block text-xs font-medium text-gray-500 dark:text-gray-400 mb-1">Estimate (hours)</label>
          <input
            type="number"
            value={estimate}
            onChange={(e) => { setEstimate(e.target.value); markDirty(); }}
            className="w-full text-sm border border-gray-300 dark:border-gray-600 rounded-md px-2 py-1.5 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100"
            placeholder="0"
          />
        </div>

        {/* Project */}
        {projects.length > 0 && (
          <div>
            <label className="block text-xs font-medium text-gray-500 dark:text-gray-400 mb-1">Project</label>
            <select
              value={projectId}
              onChange={(e) => { setProjectId(e.target.value); markDirty(); }}
              className="w-full text-sm border border-gray-300 dark:border-gray-600 rounded-md px-2 py-1.5 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100"
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
          <label className="block text-xs font-medium text-gray-500 dark:text-gray-400 mb-1">Labels</label>
          <LabelTagInput labels={labels} onChange={(l) => { setLabels(l); markDirty(); }} suggestions={existingLabels} />
        </div>

        {/* Metadata */}
        <div className="pt-2 border-t border-gray-200 dark:border-gray-700 text-xs text-gray-400 space-y-1">
          {task.created_date && <p>Created: {new Date(task.created_date).toLocaleDateString("en-GB", { day: "numeric", month: "short", year: "numeric" })}</p>}
          {task.completed_date && <p>Completed: {new Date(task.completed_date).toLocaleDateString("en-GB", { day: "numeric", month: "short", year: "numeric" })}</p>}
          {task.sub_task_count > 0 && <p>Sub-tasks: {task.sub_task_count}</p>}
        </div>
      </div>

      {/* Footer actions */}
      <div className="flex items-center justify-between px-4 py-3 border-t border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-800/50">
        <div className="flex gap-2">
          <button
            onClick={handleDelete}
            disabled={deleting}
            className="flex items-center gap-1 px-3 py-1.5 text-xs text-red-600 hover:bg-red-50 dark:hover:bg-red-900/20 rounded-md transition-colors disabled:opacity-50"
          >
            <Trash2 className="h-3.5 w-3.5" />
            {deleting ? "Deleting..." : "Delete"}
          </button>
          {task.status !== "DONE" && (
            <button
              onClick={handleComplete}
              disabled={saving}
              className="flex items-center gap-1 px-3 py-1.5 text-xs text-green-600 hover:bg-green-50 dark:hover:bg-green-900/20 rounded-md transition-colors disabled:opacity-50"
            >
              <Check className="h-3.5 w-3.5" />
              Complete
            </button>
          )}
        </div>
        <button
          onClick={handleSave}
          disabled={saving || !dirty}
          className="px-4 py-1.5 text-sm font-medium text-white bg-blue-600 rounded-md hover:bg-blue-700 transition-colors disabled:opacity-50"
        >
          {saving ? "Saving..." : "Save"}
        </button>
      </div>
    </div>
    </div>
  );
}
