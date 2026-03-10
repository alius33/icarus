"use client";

import { useState, useEffect } from "react";
import EntityModal, { FormInput, FormTextarea, FormSelect } from "@/components/EntityModal";
import type { StakeholderBase, StakeholderCreate } from "@/lib/types";

interface Props {
  open: boolean;
  onClose: () => void;
  onSave: (data: StakeholderCreate) => Promise<void>;
  onDelete?: () => void;
  saving?: boolean;
  deleting?: boolean;
  error?: string | null;
  initial?: StakeholderBase | null;
}

export default function StakeholderModal({
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
  const [role, setRole] = useState("");
  const [tier, setTier] = useState("3");
  const [riskLevel, setRiskLevel] = useState("none");
  const [moraleNotes, setMoraleNotes] = useState("");
  const [notes, setNotes] = useState("");
  const [validationError, setValidationError] = useState<string | null>(null);

  useEffect(() => {
    if (initial) {
      setName(initial.name || "");
      setRole(initial.role || "");
      setTier(String(initial.tier || 3));
      setRiskLevel(initial.risk_level || "none");
      setMoraleNotes(initial.morale_notes || "");
      setNotes("");
    } else {
      setName("");
      setRole("");
      setTier("3");
      setRiskLevel("none");
      setMoraleNotes("");
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
      role: role.trim() || undefined,
      tier: Number(tier),
      risk_level: riskLevel,
      morale_notes: moraleNotes.trim() || undefined,
      notes: notes.trim() || undefined,
    });
  };

  return (
    <EntityModal
      open={open}
      onClose={onClose}
      title={initial ? "Edit Stakeholder" : "New Stakeholder"}
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
        placeholder="Full name"
        disabled={!!initial}
      />
      <FormInput
        label="Role"
        value={role}
        onChange={setRole}
        placeholder="e.g. Programme Manager"
      />
      <div className="grid grid-cols-2 gap-3">
        <FormSelect
          label="Tier"
          value={tier}
          onChange={setTier}
          options={[
            { value: "1", label: "T1 - Decision Makers" },
            { value: "2", label: "T2 - Gatekeepers" },
            { value: "3", label: "T3 - Technical" },
            { value: "4", label: "T4 - Adjacent" },
          ]}
        />
        <FormSelect
          label="Risk Level"
          value={riskLevel}
          onChange={setRiskLevel}
          options={[
            { value: "none", label: "None" },
            { value: "low", label: "Low" },
            { value: "medium", label: "Medium" },
            { value: "high", label: "High" },
            { value: "critical", label: "Critical" },
          ]}
        />
      </div>
      <FormTextarea
        label="Morale Notes"
        value={moraleNotes}
        onChange={setMoraleNotes}
        placeholder="Current mood, engagement level..."
        rows={2}
      />
      <FormTextarea
        label="Notes"
        value={notes}
        onChange={setNotes}
        placeholder="Additional observations..."
        rows={2}
      />
    </EntityModal>
  );
}
