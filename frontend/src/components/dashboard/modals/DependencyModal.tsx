"use client";

import { useState, useEffect } from "react";
import EntityModal, { FormInput, FormTextarea, FormSelect } from "@/components/EntityModal";
import type { DependencySchema, DependencyCreate } from "@/lib/types";

interface Props {
  open: boolean;
  onClose: () => void;
  onSave: (data: DependencyCreate) => Promise<void>;
  onDelete?: () => void;
  saving?: boolean;
  deleting?: boolean;
  error?: string | null;
  initial?: DependencySchema | null;
}

export default function DependencyModal({
  open,
  onClose,
  onSave,
  onDelete,
  saving,
  deleting,
  error: externalError,
  initial,
}: Props) {
  const [name, setName] = useState("");
  const [depType, setDepType] = useState("external");
  const [status, setStatus] = useState("pending");
  const [blockingReason, setBlockingReason] = useState("");
  const [estimatedEffort, setEstimatedEffort] = useState("");
  const [assignedTo, setAssignedTo] = useState("");
  const [affectedWorkstreams, setAffectedWorkstreams] = useState("");
  const [priority, setPriority] = useState("medium");
  const [notes, setNotes] = useState("");
  const [validationError, setValidationError] = useState<string | null>(null);

  useEffect(() => {
    if (initial) {
      setName(initial.name || "");
      setDepType(initial.dependency_type || "external");
      setStatus(initial.status || "pending");
      setBlockingReason(initial.blocking_reason || "");
      setEstimatedEffort(initial.estimated_effort || "");
      setAssignedTo(initial.assigned_to || "");
      setAffectedWorkstreams(initial.affected_workstreams || "");
      setPriority(initial.priority || "medium");
      setNotes(initial.notes || "");
    } else {
      setName("");
      setDepType("external");
      setStatus("pending");
      setBlockingReason("");
      setEstimatedEffort("");
      setAssignedTo("");
      setAffectedWorkstreams("");
      setPriority("medium");
      setNotes("");
    }
    setValidationError(null);
  }, [initial, open]);

  const handleSave = () => {
    if (!name.trim()) {
      setValidationError("Name is required.");
      return;
    }
    setValidationError(null);
    onSave({
      name: name.trim(),
      dependency_type: depType,
      status,
      blocking_reason: blockingReason.trim() || undefined,
      estimated_effort: estimatedEffort.trim() || undefined,
      assigned_to: assignedTo.trim() || undefined,
      affected_workstreams: affectedWorkstreams.trim() || undefined,
      priority,
      notes: notes.trim() || undefined,
    });
  };

  return (
    <EntityModal
      open={open}
      onClose={onClose}
      title={initial ? "Edit Dependency" : "New Dependency"}
      onSave={handleSave}
      onDelete={onDelete}
      saving={saving}
      deleting={deleting}
      error={validationError || externalError}
    >
      <FormInput
        label="Name"
        value={name}
        onChange={setName}
        placeholder="Dependency name"
      />
      <div className="grid grid-cols-1 fold:grid-cols-3 gap-3">
        <FormSelect
          label="Type"
          value={depType}
          onChange={setDepType}
          options={[
            { value: "external", label: "External" },
            { value: "internal", label: "Internal" },
            { value: "integration", label: "Integration" },
          ]}
        />
        <FormSelect
          label="Status"
          value={status}
          onChange={setStatus}
          options={[
            { value: "pending", label: "Pending" },
            { value: "in-progress", label: "In Progress" },
            { value: "blocked", label: "Blocked" },
            { value: "completed", label: "Completed" },
          ]}
        />
        <FormSelect
          label="Priority"
          value={priority}
          onChange={setPriority}
          options={[
            { value: "critical", label: "Critical" },
            { value: "high", label: "High" },
            { value: "medium", label: "Medium" },
            { value: "low", label: "Low" },
          ]}
        />
      </div>
      {status === "blocked" && (
        <FormTextarea
          label="Blocking Reason"
          value={blockingReason}
          onChange={setBlockingReason}
          placeholder="Why is it blocked?"
          rows={2}
        />
      )}
      <FormInput
        label="Assigned To"
        value={assignedTo}
        onChange={setAssignedTo}
        placeholder="Who owns this?"
      />
      <FormInput
        label="Affected Workstreams"
        value={affectedWorkstreams}
        onChange={setAffectedWorkstreams}
        placeholder="e.g. WS2, WS4"
      />
      <FormTextarea
        label="Notes"
        value={notes}
        onChange={setNotes}
        placeholder="Additional notes..."
        rows={2}
      />
    </EntityModal>
  );
}
