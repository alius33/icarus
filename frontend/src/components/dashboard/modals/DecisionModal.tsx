"use client";

import { useState, useEffect } from "react";
import EntityModal, { FormInput, FormTextarea } from "@/components/EntityModal";
import type { DecisionSchema, DecisionCreate } from "@/lib/types";

interface Props {
  open: boolean;
  onClose: () => void;
  onSave: (data: DecisionCreate) => Promise<void>;
  onDelete?: () => void;
  saving?: boolean;
  deleting?: boolean;
  error?: string | null;
  initial?: DecisionSchema | null;
}

export default function DecisionModal({
  open,
  onClose,
  onSave,
  onDelete,
  saving,
  deleting,
  error: externalError,
  initial,
}: Props) {
  const [decision, setDecision] = useState("");
  const [date, setDate] = useState("");
  const [rationale, setRationale] = useState("");
  const [keyPeople, setKeyPeople] = useState("");
  const [validationError, setValidationError] = useState<string | null>(null);

  useEffect(() => {
    if (initial) {
      setDecision(initial.description || initial.title || "");
      setDate(initial.date || "");
      setRationale("");
      setKeyPeople(initial.owner || "");
    } else {
      setDecision("");
      setDate("");
      setRationale("");
      setKeyPeople("");
    }
    setValidationError(null);
  }, [initial, open]);

  const handleSave = () => {
    if (!decision.trim()) {
      setValidationError("Decision text is required.");
      return;
    }
    setValidationError(null);
    onSave({
      decision: decision.trim(),
      date: date.trim() || undefined,
      rationale: rationale.trim() || undefined,
      key_people: keyPeople
        .split(",")
        .map((s) => s.trim())
        .filter(Boolean),
    });
  };

  return (
    <EntityModal
      open={open}
      onClose={onClose}
      title={initial ? "Edit Decision" : "New Decision"}
      onSave={handleSave}
      onDelete={onDelete}
      saving={saving}
      deleting={deleting}
      error={validationError || externalError}
    >
      <FormTextarea
        label="Decision"
        value={decision}
        onChange={setDecision}
        placeholder="What was decided?"
      />
      <FormInput
        label="Date"
        value={date}
        onChange={setDate}
        placeholder="YYYY-MM-DD"
        type="date"
      />
      <FormTextarea
        label="Rationale"
        value={rationale}
        onChange={setRationale}
        placeholder="Why was this decision made?"
        rows={2}
      />
      <FormInput
        label="Key People"
        value={keyPeople}
        onChange={setKeyPeople}
        placeholder="Comma-separated names"
      />
    </EntityModal>
  );
}
