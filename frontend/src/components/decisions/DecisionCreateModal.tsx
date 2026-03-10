"use client";

import { useState } from "react";
import EntityModal, { FormInput, FormTextarea, FormSelect } from "@/components/EntityModal";
import { DecisionCreate, DECISION_STATUSES, DECISION_STATUS_CONFIG, DecisionStatus } from "@/lib/types";
import { api } from "@/lib/api";

interface DecisionCreateModalProps {
  open: boolean;
  onClose: () => void;
  onCreated: () => void;
}

export default function DecisionCreateModal({
  open,
  onClose,
  onCreated,
}: DecisionCreateModalProps) {
  const [decision, setDecision] = useState("");
  const [rationale, setRationale] = useState("");
  const [date, setDate] = useState(new Date().toISOString().split("T")[0]);
  const [executionStatus, setExecutionStatus] = useState("made");
  const [keyPeople, setKeyPeople] = useState("");
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);

  function reset() {
    setDecision(""); setRationale("");
    setDate(new Date().toISOString().split("T")[0]);
    setExecutionStatus("made"); setKeyPeople(""); setError(null);
  }

  async function handleSave() {
    if (!decision.trim()) {
      setError("Decision text is required");
      return;
    }
    setSaving(true);
    setError(null);
    try {
      const people = keyPeople
        .split(",")
        .map((p) => p.trim())
        .filter(Boolean);

      const body: DecisionCreate = {
        decision: decision.trim(),
        rationale: rationale || undefined,
        date: date || undefined,
        execution_status: executionStatus,
        key_people: people.length > 0 ? people : undefined,
      };
      await api.createDecision(body);
      reset();
      onCreated();
      onClose();
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : "Failed to create decision");
    } finally {
      setSaving(false);
    }
  }

  return (
    <EntityModal
      open={open}
      onClose={() => { reset(); onClose(); }}
      title="New Decision"
      onSave={handleSave}
      saving={saving}
      error={error}
    >
      <FormTextarea label="Decision" value={decision} onChange={setDecision} placeholder="What was decided?" rows={3} />
      <FormTextarea label="Rationale" value={rationale} onChange={setRationale} placeholder="Why was this decided?" rows={3} />

      <div className="grid grid-cols-2 gap-4">
        <FormInput label="Date" value={date} onChange={setDate} type="date" />
        <FormSelect
          label="Status"
          value={executionStatus}
          onChange={setExecutionStatus}
          options={DECISION_STATUSES.map((s) => ({ value: s, label: DECISION_STATUS_CONFIG[s as DecisionStatus].label }))}
        />
      </div>

      <FormInput label="Key People (comma-separated)" value={keyPeople} onChange={setKeyPeople} placeholder="Alice, Bob, Charlie" />
    </EntityModal>
  );
}
