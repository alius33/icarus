"use client";

import { useState, useEffect } from "react";
import EntityModal, { FormInput, FormTextarea, FormSelect } from "@/components/EntityModal";
import type { ActionItemSchema, ActionItemCreate } from "@/lib/types";

interface Props {
  open: boolean;
  onClose: () => void;
  onSave: (data: ActionItemCreate) => Promise<void>;
  onDelete?: () => void;
  saving?: boolean;
  deleting?: boolean;
  error?: string | null;
  initial?: ActionItemSchema | null;
}

export default function ActionModal({
  open,
  onClose,
  onSave,
  onDelete,
  saving,
  deleting,
  error: externalError,
  initial,
}: Props) {
  const [description, setDescription] = useState("");
  const [owner, setOwner] = useState("");
  const [deadline, setDeadline] = useState("");
  const [context, setContext] = useState("");
  const [status, setStatus] = useState("OPEN");
  const [validationError, setValidationError] = useState<string | null>(null);

  useEffect(() => {
    if (initial) {
      setDescription(initial.description || initial.title || "");
      setOwner(initial.owner || "");
      setDeadline(initial.due_date || "");
      setContext("");
      setStatus(initial.status || "OPEN");
    } else {
      setDescription("");
      setOwner("");
      setDeadline("");
      setContext("");
      setStatus("OPEN");
    }
    setValidationError(null);
  }, [initial, open]);

  const handleSave = () => {
    if (!description.trim()) {
      setValidationError("Description is required.");
      return;
    }
    setValidationError(null);
    onSave({
      description: description.trim(),
      owner: owner.trim() || undefined,
      deadline: deadline.trim() || undefined,
      context: context.trim() || undefined,
      status,
    });
  };

  return (
    <EntityModal
      open={open}
      onClose={onClose}
      title={initial ? "Edit Action Item" : "New Action Item"}
      onSave={handleSave}
      onDelete={onDelete}
      saving={saving}
      deleting={deleting}
      error={validationError || externalError}
    >
      <FormTextarea
        label="Description"
        value={description}
        onChange={setDescription}
        placeholder="What needs to be done?"
      />
      <FormInput
        label="Owner"
        value={owner}
        onChange={setOwner}
        placeholder="Who is responsible?"
      />
      <FormInput
        label="Deadline"
        value={deadline}
        onChange={setDeadline}
        placeholder="e.g. 2026-03-15 or 'by Friday'"
      />
      <FormTextarea
        label="Context"
        value={context}
        onChange={setContext}
        placeholder="Additional context..."
        rows={2}
      />
      <FormSelect
        label="Status"
        value={status}
        onChange={setStatus}
        options={[
          { value: "OPEN", label: "Open" },
          { value: "LIKELY COMPLETED", label: "Likely Completed" },
          { value: "COMPLETED", label: "Completed" },
        ]}
      />
    </EntityModal>
  );
}
