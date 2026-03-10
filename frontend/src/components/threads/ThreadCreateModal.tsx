"use client";

import { useState } from "react";
import EntityModal, { FormInput, FormTextarea, FormSelect } from "@/components/EntityModal";
import {
  OpenThreadCreate,
  THREAD_STATUSES,
  THREAD_SEVERITIES,
  TREND_OPTIONS,
  THREAD_STATUS_CONFIG,
  SEVERITY_CONFIG,
  ThreadStatus,
  ThreadSeverity,
} from "@/lib/types";
import { api } from "@/lib/api";

interface ThreadCreateModalProps {
  open: boolean;
  onClose: () => void;
  onCreated: () => void;
}

export default function ThreadCreateModal({
  open,
  onClose,
  onCreated,
}: ThreadCreateModalProps) {
  const today = new Date().toISOString().split("T")[0];

  const [title, setTitle] = useState("");
  const [context, setContext] = useState("");
  const [question, setQuestion] = useState("");
  const [whyItMatters, setWhyItMatters] = useState("");
  const [status, setStatus] = useState("OPEN");
  const [severity, setSeverity] = useState("");
  const [trend, setTrend] = useState("");
  const [firstRaised, setFirstRaised] = useState(today);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);

  function reset() {
    setTitle(""); setContext(""); setQuestion(""); setWhyItMatters("");
    setStatus("OPEN"); setSeverity(""); setTrend("");
    setFirstRaised(new Date().toISOString().split("T")[0]);
    setError(null);
  }

  async function handleSave() {
    if (!title.trim()) {
      setError("Title is required");
      return;
    }
    setSaving(true);
    setError(null);
    try {
      const body: OpenThreadCreate = {
        title: title.trim(),
        context: context || undefined,
        question: question || undefined,
        why_it_matters: whyItMatters || undefined,
        status,
        severity: severity || undefined,
        trend: trend || undefined,
        first_raised: firstRaised || undefined,
      };
      await api.createOpenThread(body);
      reset();
      onCreated();
      onClose();
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : "Failed to create thread");
    } finally {
      setSaving(false);
    }
  }

  return (
    <EntityModal
      open={open}
      onClose={() => { reset(); onClose(); }}
      title="New Open Thread"
      onSave={handleSave}
      saving={saving}
      error={error}
    >
      <FormInput label="Title" value={title} onChange={setTitle} placeholder="What is this thread about?" />
      <FormTextarea label="Context" value={context} onChange={setContext} placeholder="Provide background context..." rows={3} />
      <FormTextarea label="Question" value={question} onChange={setQuestion} placeholder="What is the open question?" rows={2} />
      <FormTextarea label="Why It Matters" value={whyItMatters} onChange={setWhyItMatters} placeholder="Why does this matter to the programme?" rows={2} />

      <div className="grid grid-cols-2 gap-4">
        <FormSelect
          label="Status"
          value={status}
          onChange={setStatus}
          options={THREAD_STATUSES.map((s) => ({ value: s, label: THREAD_STATUS_CONFIG[s as ThreadStatus].label }))}
        />
        <FormSelect
          label="Severity"
          value={severity}
          onChange={setSeverity}
          options={[
            { value: "", label: "None" },
            ...THREAD_SEVERITIES.map((s) => ({ value: s, label: SEVERITY_CONFIG[s as ThreadSeverity].label })),
          ]}
        />
      </div>

      <FormSelect
        label="Trend"
        value={trend}
        onChange={setTrend}
        options={[
          { value: "", label: "None" },
          ...TREND_OPTIONS.map((t) => ({
            value: t,
            label: t === "escalating" ? "\u2191 Escalating" : t === "stable" ? "\u2192 Stable" : "\u2193 De-escalating",
          })),
        ]}
      />

      <FormInput label="First Raised" value={firstRaised} onChange={setFirstRaised} type="date" />
    </EntityModal>
  );
}
