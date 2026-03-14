"use client";

import { useState } from "react";
import EntityModal, { FormInput, FormTextarea, FormSelect } from "@/components/EntityModal";
import LabelTagInput from "./LabelTagInput";
import { TaskCreate, TASK_STATUSES, TASK_PRIORITIES, STATUS_CONFIG, PRIORITY_CONFIG, TaskStatus, TaskPriority } from "@/lib/types";
import { api } from "@/lib/api";

interface TaskCreateModalProps {
  open: boolean;
  onClose: () => void;
  onCreated: () => void;
  projects?: { id: number; name: string }[];
  existingLabels?: string[];
  defaultProjectId?: number;
}

export default function TaskCreateModal({
  open,
  onClose,
  onCreated,
  projects = [],
  existingLabels = [],
  defaultProjectId,
}: TaskCreateModalProps) {
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [status, setStatus] = useState("TODO");
  const [priority, setPriority] = useState("NONE");
  const [assignee, setAssignee] = useState("");
  const [dueDate, setDueDate] = useState("");
  const [startDate, setStartDate] = useState("");
  const [estimate, setEstimate] = useState("");
  const [projectId, setProjectId] = useState(defaultProjectId ? String(defaultProjectId) : "");
  const [labels, setLabels] = useState<string[]>([]);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);

  function reset() {
    setTitle(""); setDescription(""); setStatus("TODO"); setPriority("NONE");
    setAssignee(""); setDueDate(""); setStartDate(""); setEstimate("");
    setProjectId(defaultProjectId ? String(defaultProjectId) : "");
    setLabels([]); setError(null);
  }

  async function handleSave() {
    if (!title.trim()) {
      setError("Title is required");
      return;
    }
    setSaving(true);
    setError(null);
    try {
      const body: TaskCreate = {
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
      await api.createTask(body);
      reset();
      onCreated();
      onClose();
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : "Failed to create task");
    } finally {
      setSaving(false);
    }
  }

  return (
    <EntityModal
      open={open}
      onClose={() => { reset(); onClose(); }}
      title="New Task"
      onSave={handleSave}
      saving={saving}
      error={error}
    >
      <FormInput label="Title" value={title} onChange={setTitle} placeholder="What needs to be done?" />
      <FormTextarea label="Description" value={description} onChange={setDescription} placeholder="Add details..." rows={3} />

      <div className="grid grid-cols-2 gap-4">
        <FormSelect
          label="Status"
          value={status}
          onChange={setStatus}
          options={TASK_STATUSES.map((s) => ({ value: s, label: STATUS_CONFIG[s as TaskStatus].label }))}
        />
        <FormSelect
          label="Priority"
          value={priority}
          onChange={setPriority}
          options={TASK_PRIORITIES.map((p) => ({ value: p, label: PRIORITY_CONFIG[p as TaskPriority].label }))}
        />
      </div>

      <FormInput label="Assignee" value={assignee} onChange={setAssignee} placeholder="Who's responsible?" />

      <div className="grid grid-cols-2 gap-4">
        <FormInput label="Start Date" value={startDate} onChange={setStartDate} type="date" />
        <FormInput label="Due Date" value={dueDate} onChange={setDueDate} type="date" />
      </div>

      <FormInput label="Estimate (hours)" value={estimate} onChange={setEstimate} type="number" placeholder="0" />

      {projects.length > 0 && (
        <FormSelect
          label="Project"
          value={projectId}
          onChange={setProjectId}
          options={[{ value: "", label: "No project" }, ...projects.map((p) => ({ value: String(p.id), label: p.name }))]}
        />
      )}

      <div>
        <label className="block text-base font-medium text-gray-700 dark:text-gray-300 mb-1">Labels</label>
        <LabelTagInput labels={labels} onChange={setLabels} suggestions={existingLabels} />
      </div>
    </EntityModal>
  );
}
