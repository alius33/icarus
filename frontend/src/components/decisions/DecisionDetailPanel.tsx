"use client";

import { useState, useEffect } from "react";
import { DecisionSchema, DecisionUpdate, DECISION_STATUSES, DECISION_STATUS_CONFIG, DecisionStatus } from "@/lib/types";
import { api } from "@/lib/api";
import { X, Trash2 } from "lucide-react";

interface DecisionDetailPanelProps {
  decision: DecisionSchema;
  onClose: () => void;
  onUpdated: () => void;
}

export default function DecisionDetailPanel({ decision, onClose, onUpdated }: DecisionDetailPanelProps) {
  const [decisionText, setDecisionText] = useState(decision.title);
  const [rationale, setRationale] = useState(decision.rationale || "");
  const [executionStatus, setExecutionStatus] = useState(decision.execution_status);
  const [date, setDate] = useState(decision.date || "");
  const [keyPeople, setKeyPeople] = useState(decision.key_people.join(", "));
  const [workstream, setWorkstream] = useState(decision.workstream || "");
  const [saving, setSaving] = useState(false);
  const [deleting, setDeleting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [dirty, setDirty] = useState(false);

  useEffect(() => {
    setDecisionText(decision.title);
    setRationale(decision.rationale || "");
    setExecutionStatus(decision.execution_status);
    setDate(decision.date || "");
    setKeyPeople(decision.key_people.join(", "));
    setWorkstream(decision.workstream || "");
    setDirty(false);
    setError(null);
  }, [decision]);

  function markDirty() { setDirty(true); }

  async function handleSave() {
    if (!decisionText.trim()) { setError("Decision text is required"); return; }
    setSaving(true);
    setError(null);
    try {
      const people = keyPeople
        .split(",")
        .map((p) => p.trim())
        .filter(Boolean);

      const body: DecisionUpdate = {
        decision: decisionText.trim(),
        rationale: rationale || undefined,
        execution_status: executionStatus,
        date: date || undefined,
        key_people: people,
        workstream: workstream || undefined,
      };
      await api.updateDecision(decision.id, body);
      setDirty(false);
      onUpdated();
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : "Failed to save");
    } finally {
      setSaving(false);
    }
  }

  async function handleDelete() {
    if (!confirm("Delete this decision? This cannot be undone.")) return;
    setDeleting(true);
    try {
      await api.deleteDecision(decision.id);
      onUpdated();
      onClose();
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : "Failed to delete");
    } finally {
      setDeleting(false);
    }
  }

  return (
    <div className="fixed inset-0 z-40">
      {/* Backdrop — click to close */}
      <div className="absolute inset-0 bg-black/20" onClick={onClose} />
      <div className="absolute inset-y-0 right-0 w-full max-w-md bg-white dark:bg-gray-900 shadow-2xl border-l border-gray-200 dark:border-gray-700 flex flex-col">
      {/* Header */}
      <div className="flex items-center justify-between px-4 py-3 border-b border-gray-200 dark:border-gray-700">
        <span className="text-xs font-mono text-gray-400">Decision #{decision.number}</span>
        <button onClick={onClose} className="text-gray-400 hover:text-gray-600 dark:hover:text-gray-300">
          <X className="h-5 w-5" />
        </button>
      </div>

      {/* Body -- scrollable */}
      <div className="flex-1 overflow-y-auto px-4 py-4 space-y-4">
        {error && (
          <div className="rounded-md bg-red-50 dark:bg-red-900/30 border border-red-200 dark:border-red-800 px-3 py-2">
            <p className="text-sm text-red-700 dark:text-red-400">{error}</p>
          </div>
        )}

        {/* Decision text */}
        <div>
          <label className="block text-xs font-medium text-gray-500 dark:text-gray-400 mb-1">Decision</label>
          <textarea
            value={decisionText}
            onChange={(e) => { setDecisionText(e.target.value); markDirty(); }}
            rows={3}
            className="w-full text-sm text-gray-700 dark:text-gray-300 bg-gray-50 dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-md px-3 py-2 focus:outline-none focus:ring-1 focus:ring-blue-500"
            placeholder="What was decided?"
          />
        </div>

        {/* Rationale */}
        <div>
          <label className="block text-xs font-medium text-gray-500 dark:text-gray-400 mb-1">Rationale</label>
          <textarea
            value={rationale}
            onChange={(e) => { setRationale(e.target.value); markDirty(); }}
            rows={3}
            className="w-full text-sm text-gray-700 dark:text-gray-300 bg-gray-50 dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-md px-3 py-2 focus:outline-none focus:ring-1 focus:ring-blue-500"
            placeholder="Why was this decided?"
          />
        </div>

        {/* Status + Date */}
        <div className="grid grid-cols-2 gap-3">
          <div>
            <label className="block text-xs font-medium text-gray-500 dark:text-gray-400 mb-1">Status</label>
            <select
              value={executionStatus}
              onChange={(e) => { setExecutionStatus(e.target.value); markDirty(); }}
              className="w-full text-sm border border-gray-300 dark:border-gray-600 rounded-md px-2 py-1.5 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100"
            >
              {DECISION_STATUSES.map((s) => (
                <option key={s} value={s}>{DECISION_STATUS_CONFIG[s as DecisionStatus].label}</option>
              ))}
            </select>
          </div>
          <div>
            <label className="block text-xs font-medium text-gray-500 dark:text-gray-400 mb-1">Date</label>
            <input
              type="date"
              value={date}
              onChange={(e) => { setDate(e.target.value); markDirty(); }}
              className="w-full text-sm border border-gray-300 dark:border-gray-600 rounded-md px-2 py-1.5 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100"
            />
          </div>
        </div>

        {/* Key People */}
        <div>
          <label className="block text-xs font-medium text-gray-500 dark:text-gray-400 mb-1">Key People (comma-separated)</label>
          <input
            value={keyPeople}
            onChange={(e) => { setKeyPeople(e.target.value); markDirty(); }}
            className="w-full text-sm border border-gray-300 dark:border-gray-600 rounded-md px-2 py-1.5 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100"
            placeholder="Alice, Bob, Charlie"
          />
        </div>

        {/* Workstream */}
        <div>
          <label className="block text-xs font-medium text-gray-500 dark:text-gray-400 mb-1">Workstream</label>
          <input
            value={workstream}
            onChange={(e) => { setWorkstream(e.target.value); markDirty(); }}
            className="w-full text-sm border border-gray-300 dark:border-gray-600 rounded-md px-2 py-1.5 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100"
            placeholder="e.g. WS2 CLARA"
          />
        </div>

        {/* Metadata */}
        <div className="pt-2 border-t border-gray-200 dark:border-gray-700 text-xs text-gray-400 space-y-1">
          {decision.transcript_title && <p>Source: {decision.transcript_title}</p>}
          {decision.owner && <p>Owner: {decision.owner}</p>}
        </div>
      </div>

      {/* Footer actions */}
      <div className="flex items-center justify-between px-4 py-3 border-t border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-800/50">
        <button
          onClick={handleDelete}
          disabled={deleting}
          className="flex items-center gap-1 px-3 py-1.5 text-xs text-red-600 hover:bg-red-50 dark:hover:bg-red-900/20 rounded-md transition-colors disabled:opacity-50"
        >
          <Trash2 className="h-3.5 w-3.5" />
          {deleting ? "Deleting..." : "Delete"}
        </button>
        <button
          onClick={handleSave}
          disabled={saving || !dirty}
          className="px-4 py-1.5 text-sm font-medium text-white bg-blue-600 rounded-md hover:bg-blue-700 transition-colors disabled:opacity-50"
        >
          {saving ? "Saving..." : "Save"}
        </button>
      </div>
    </div>
    </div>
  );
}
