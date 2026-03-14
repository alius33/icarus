"use client";

import { useState, useEffect } from "react";
import EntityModal, { FormInput, FormTextarea, FormSelect } from "@/components/EntityModal";
import type { ScopeItemSchema, ScopeItemCreate } from "@/lib/types";

interface Props {
  open: boolean;
  onClose: () => void;
  onSave: (data: ScopeItemCreate) => Promise<void>;
  onDelete?: () => void;
  saving?: boolean;
  deleting?: boolean;
  error?: string | null;
  initial?: ScopeItemSchema | null;
}

export default function ScopeItemModal({
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
  const [scopeType, setScopeType] = useState("original");
  const [workstream, setWorkstream] = useState("");
  const [status, setStatus] = useState("planned");
  const [description, setDescription] = useState("");
  const [impactNotes, setImpactNotes] = useState("");
  const [validationError, setValidationError] = useState<string | null>(null);

  useEffect(() => {
    if (initial) {
      setName(initial.name || "");
      setScopeType(initial.scope_type || "original");
      setWorkstream(initial.workstream || "");
      setStatus(initial.status || "planned");
      setDescription(initial.description || "");
      setImpactNotes(initial.impact_notes || "");
    } else {
      setName("");
      setScopeType("original");
      setWorkstream("");
      setStatus("planned");
      setDescription("");
      setImpactNotes("");
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
      scope_type: scopeType,
      workstream: workstream.trim() || undefined,
      status,
      description: description.trim() || undefined,
      impact_notes: impactNotes.trim() || undefined,
    });
  };

  return (
    <EntityModal
      open={open}
      onClose={onClose}
      title={initial ? "Edit Scope Item" : "New Scope Item"}
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
        placeholder="Scope item name"
      />
      <div className="grid grid-cols-1 fold:grid-cols-3 gap-3">
        <FormSelect
          label="Type"
          value={scopeType}
          onChange={setScopeType}
          options={[
            { value: "original", label: "Original" },
            { value: "addition", label: "Addition" },
          ]}
        />
        <FormSelect
          label="Status"
          value={status}
          onChange={setStatus}
          options={[
            { value: "planned", label: "Planned" },
            { value: "in-progress", label: "In Progress" },
            { value: "completed", label: "Completed" },
            { value: "cancelled", label: "Cancelled" },
          ]}
        />
        <FormInput
          label="Workstream"
          value={workstream}
          onChange={setWorkstream}
          placeholder="e.g. WS2"
        />
      </div>
      <FormTextarea
        label="Description"
        value={description}
        onChange={setDescription}
        placeholder="What is this scope item?"
      />
      <FormTextarea
        label="Impact Notes"
        value={impactNotes}
        onChange={setImpactNotes}
        placeholder="Impact on delivery..."
        rows={2}
      />
    </EntityModal>
  );
}
