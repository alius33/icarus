"use client";

import { useState, useEffect, useCallback } from "react";
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

  // Escape key to close
  const handleKeyDown = useCallback((e: KeyboardEvent) => {
    if (e.key === "Escape") onClose();
  }, [onClose]);
  useEffect(() => {
    document.addEventListener("keydown", handleKeyDown);
    return () => document.removeEventListener("keydown", handleKeyDown);
  }, [handleKeyDown]);

  return (
    <div className="fixed inset-0 z-40">
      {/* Backdrop — click to close */}
      <div className="absolute inset-0 bg-black/20" onClick={onClose} />
      <div className="absolute bg-white dark:bg-forest-800 dark:bg-forest-900 shadow-2xl flex flex-col md:inset-y-0 md:right-0 md:w-full md:max-w-md md:border-l md:border-forest-200 dark:md:border-gray-700 max-md:inset-x-0 max-md:bottom-0 max-md:top-[10vh] max-md:rounded-t-2xl max-md:border-t max-md:border-forest-200 dark:max-md:border-gray-700">
      {/* Mobile drag handle */}
      <div className="md:hidden flex justify-center pt-2 pb-1">
        <div className="w-10 h-1 bg-gray-300 dark:bg-forest-700 rounded-full" />
      </div>
      {/* Header */}
      <div className="flex items-center justify-between px-4 py-3 border-b border-forest-200 dark:border-forest-700">
        <span className="text-sm font-mono text-forest-300">Decision #{decision.number}</span>
        <button onClick={onClose} className="text-forest-300 hover:text-forest-500 dark:hover:text-gray-300">
          <X className="h-5 w-5" />
        </button>
      </div>

      {/* Body -- scrollable */}
      <div className="flex-1 overflow-y-auto px-4 py-4 space-y-4">
        {error && (
          <div className="rounded-md bg-red-50 dark:bg-red-900/30 border border-red-200 dark:border-red-800 px-3 py-2">
            <p className="text-base text-red-700 dark:text-red-400">{error}</p>
          </div>
        )}

        {/* Decision text */}
        <div>
          <label className="block text-sm font-medium text-forest-400 dark:text-forest-300 mb-1">Decision</label>
          <textarea
            value={decisionText}
            onChange={(e) => { setDecisionText(e.target.value); markDirty(); }}
            rows={3}
            className="w-full text-base text-forest-600 dark:text-forest-200 bg-forest-50 dark:bg-forest-800 border border-forest-200 dark:border-forest-700 rounded-md px-3 py-2 focus:outline-none focus:ring-1 focus:ring-forest-500"
            placeholder="What was decided?"
          />
        </div>

        {/* Rationale */}
        <div>
          <label className="block text-sm font-medium text-forest-400 dark:text-forest-300 mb-1">Rationale</label>
          <textarea
            value={rationale}
            onChange={(e) => { setRationale(e.target.value); markDirty(); }}
            rows={3}
            className="w-full text-base text-forest-600 dark:text-forest-200 bg-forest-50 dark:bg-forest-800 border border-forest-200 dark:border-forest-700 rounded-md px-3 py-2 focus:outline-none focus:ring-1 focus:ring-forest-500"
            placeholder="Why was this decided?"
          />
        </div>

        {/* Status + Date */}
        <div className="grid grid-cols-2 gap-3">
          <div>
            <label className="block text-sm font-medium text-forest-400 dark:text-forest-300 mb-1">Status</label>
            <select
              value={executionStatus}
              onChange={(e) => { setExecutionStatus(e.target.value); markDirty(); }}
              className="w-full text-base border border-forest-200 dark:border-forest-700 rounded-md px-2 py-1.5 bg-white dark:bg-forest-800 text-forest-950 dark:text-forest-50"
            >
              {DECISION_STATUSES.map((s) => (
                <option key={s} value={s}>{DECISION_STATUS_CONFIG[s as DecisionStatus].label}</option>
              ))}
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium text-forest-400 dark:text-forest-300 mb-1">Date</label>
            <input
              type="date"
              value={date}
              onChange={(e) => { setDate(e.target.value); markDirty(); }}
              className="w-full text-base border border-forest-200 dark:border-forest-700 rounded-md px-2 py-1.5 bg-white dark:bg-forest-800 text-forest-950 dark:text-forest-50"
            />
          </div>
        </div>

        {/* Key People */}
        <div>
          <label className="block text-sm font-medium text-forest-400 dark:text-forest-300 mb-1">Key People (comma-separated)</label>
          <input
            value={keyPeople}
            onChange={(e) => { setKeyPeople(e.target.value); markDirty(); }}
            className="w-full text-base border border-forest-200 dark:border-forest-700 rounded-md px-2 py-1.5 bg-white dark:bg-forest-800 text-forest-950 dark:text-forest-50"
            placeholder="Alice, Bob, Charlie"
          />
        </div>

        {/* Metadata */}
        <div className="pt-2 border-t border-forest-200 dark:border-forest-700 text-sm text-forest-300 space-y-1">
          {decision.transcript_title && <p>Source: {decision.transcript_title}</p>}
          {decision.owner && <p>Owner: {decision.owner}</p>}
        </div>
      </div>

      {/* Footer actions */}
      <div className="flex items-center justify-between px-4 py-3 border-t border-forest-200 dark:border-forest-700 bg-forest-50 dark:bg-forest-800/50">
        <button
          onClick={handleDelete}
          disabled={deleting}
          className="flex items-center gap-1 px-3 py-1.5 text-sm text-red-600 hover:bg-red-50 dark:hover:bg-red-900/20 rounded-md transition-colors disabled:opacity-50"
        >
          <Trash2 className="h-3.5 w-3.5" />
          {deleting ? "Deleting..." : "Delete"}
        </button>
        <button
          onClick={handleSave}
          disabled={saving || !dirty}
          className="px-4 py-1.5 text-base font-medium text-white bg-forest-500 rounded-md hover:bg-forest-600 transition-colors disabled:opacity-50"
        >
          {saving ? "Saving..." : "Save"}
        </button>
      </div>
    </div>
    </div>
  );
}
