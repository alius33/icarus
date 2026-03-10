"use client";

import { useState, useEffect } from "react";
import EntityModal, { FormInput, FormTextarea, FormSelect } from "@/components/EntityModal";
import type { ResourceAllocationSchema, ResourceAllocationCreate } from "@/lib/types";

interface Props {
  open: boolean;
  onClose: () => void;
  onSave: (data: ResourceAllocationCreate) => Promise<void>;
  onDelete?: () => void;
  saving?: boolean;
  deleting?: boolean;
  error?: string | null;
  initial?: ResourceAllocationSchema | null;
}

export default function ResourceModal({
  open,
  onClose,
  onSave,
  onDelete,
  saving,
  deleting,
  error: externalError,
  initial,
}: Props) {
  const [personName, setPersonName] = useState("");
  const [role, setRole] = useState("");
  const [capacityStatus, setCapacityStatus] = useState("available");
  const [notes, setNotes] = useState("");
  const [validationError, setValidationError] = useState<string | null>(null);

  useEffect(() => {
    if (initial) {
      setPersonName(initial.person_name || "");
      setRole(initial.role || "");
      setCapacityStatus(initial.capacity_status || "available");
      setNotes(initial.notes || "");
    } else {
      setPersonName("");
      setRole("");
      setCapacityStatus("available");
      setNotes("");
    }
    setValidationError(null);
  }, [initial, open]);

  const handleSave = () => {
    if (!personName.trim()) {
      setValidationError("Person name is required.");
      return;
    }
    setValidationError(null);
    onSave({
      person_name: personName.trim(),
      role: role.trim() || undefined,
      capacity_status: capacityStatus,
      notes: notes.trim() || undefined,
    });
  };

  return (
    <EntityModal
      open={open}
      onClose={onClose}
      title={initial ? "Edit Resource" : "New Resource"}
      onSave={handleSave}
      onDelete={onDelete}
      saving={saving}
      deleting={deleting}
      error={validationError || externalError}
    >
      <FormInput
        label="Person Name"
        value={personName}
        onChange={setPersonName}
        placeholder="Full name"
      />
      <FormInput
        label="Role"
        value={role}
        onChange={setRole}
        placeholder="e.g. Senior Developer"
      />
      <FormSelect
        label="Capacity Status"
        value={capacityStatus}
        onChange={setCapacityStatus}
        options={[
          { value: "available", label: "Available" },
          { value: "stretched", label: "Stretched" },
          { value: "overloaded", label: "Overloaded" },
        ]}
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
