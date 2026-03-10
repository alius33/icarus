"use client";

import { useState, useEffect } from "react";
import EntityModal, { FormInput, FormTextarea, FormSelect } from "@/components/EntityModal";
import type { OpenThreadSchema, OpenThreadCreate } from "@/lib/types";

interface Props {
  open: boolean;
  onClose: () => void;
  onSave: (data: OpenThreadCreate) => Promise<void>;
  onDelete?: () => void;
  saving?: boolean;
  deleting?: boolean;
  error?: string | null;
  initial?: OpenThreadSchema | null;
}

export default function ThreadModal({
  open,
  onClose,
  onSave,
  onDelete,
  saving,
  deleting,
  error: externalError,
  initial,
}: Props) {
  const [title, setTitle] = useState("");
  const [context, setContext] = useState("");
  const [question, setQuestion] = useState("");
  const [whyItMatters, setWhyItMatters] = useState("");
  const [status, setStatus] = useState("OPEN");
  const [severity, setSeverity] = useState("MEDIUM");
  const [trend, setTrend] = useState("stable");
  const [validationError, setValidationError] = useState<string | null>(null);

  useEffect(() => {
    if (initial) {
      setTitle(initial.title || "");
      setContext(initial.description || "");
      setQuestion("");
      setWhyItMatters("");
      setStatus(initial.status || "OPEN");
      setSeverity(initial.severity || "MEDIUM");
      setTrend(initial.trend || "stable");
    } else {
      setTitle("");
      setContext("");
      setQuestion("");
      setWhyItMatters("");
      setStatus("OPEN");
      setSeverity("MEDIUM");
      setTrend("stable");
    }
    setValidationError(null);
  }, [initial, open]);

  const handleSave = () => {
    if (!title.trim()) {
      setValidationError("Title is required.");
      return;
    }
    setValidationError(null);
    onSave({
      title: title.trim(),
      context: context.trim() || undefined,
      question: question.trim() || undefined,
      why_it_matters: whyItMatters.trim() || undefined,
      status,
      severity,
      trend,
    });
  };

  return (
    <EntityModal
      open={open}
      onClose={onClose}
      title={initial ? "Edit Open Thread" : "New Open Thread"}
      onSave={handleSave}
      onDelete={onDelete}
      saving={saving}
      deleting={deleting}
      error={validationError || externalError}
    >
      <FormInput
        label="Title"
        value={title}
        onChange={setTitle}
        placeholder="Thread title"
      />
      <FormTextarea
        label="Context"
        value={context}
        onChange={setContext}
        placeholder="Background context..."
      />
      <FormTextarea
        label="Question"
        value={question}
        onChange={setQuestion}
        placeholder="What needs to be resolved?"
        rows={2}
      />
      <FormTextarea
        label="Why it Matters"
        value={whyItMatters}
        onChange={setWhyItMatters}
        placeholder="Impact if unresolved..."
        rows={2}
      />
      <div className="grid grid-cols-3 gap-3">
        <FormSelect
          label="Status"
          value={status}
          onChange={setStatus}
          options={[
            { value: "OPEN", label: "Open" },
            { value: "CLOSED", label: "Closed" },
            { value: "LIKELY RESOLVED", label: "Likely Resolved" },
          ]}
        />
        <FormSelect
          label="Severity"
          value={severity}
          onChange={setSeverity}
          options={[
            { value: "CRITICAL", label: "Critical" },
            { value: "HIGH", label: "High" },
            { value: "MEDIUM", label: "Medium" },
            { value: "LOW", label: "Low" },
          ]}
        />
        <FormSelect
          label="Trend"
          value={trend}
          onChange={setTrend}
          options={[
            { value: "escalating", label: "Escalating" },
            { value: "stable", label: "Stable" },
            { value: "de-escalating", label: "De-escalating" },
          ]}
        />
      </div>
    </EntityModal>
  );
}
