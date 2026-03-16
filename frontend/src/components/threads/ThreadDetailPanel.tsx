"use client";

import { useState, useEffect, useCallback } from "react";
import {
  OpenThreadSchema,
  OpenThreadUpdate,
  THREAD_STATUSES,
  THREAD_SEVERITIES,
  TREND_OPTIONS,
  THREAD_STATUS_CONFIG,
  SEVERITY_CONFIG,
} from "@/lib/types";
import { api } from "@/lib/api";
import { X, Trash2 } from "lucide-react";

interface ThreadDetailPanelProps {
  thread: OpenThreadSchema;
  onClose: () => void;
  onUpdated: () => void;
}

export default function ThreadDetailPanel({ thread, onClose, onUpdated }: ThreadDetailPanelProps) {
  const [title, setTitle] = useState(thread.title);
  const [description, setDescription] = useState(thread.description || "");
  const [question, setQuestion] = useState(thread.question || "");
  const [whyItMatters, setWhyItMatters] = useState(thread.why_it_matters || "");
  const [status, setStatus] = useState(thread.status);
  const [severity, setSeverity] = useState(thread.severity || "");
  const [trend, setTrend] = useState(thread.trend || "");
  const [firstRaised, setFirstRaised] = useState(thread.opened_date || "");
  const [resolution, setResolution] = useState(thread.resolution || "");
  const [saving, setSaving] = useState(false);
  const [deleting, setDeleting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [dirty, setDirty] = useState(false);

  useEffect(() => {
    setTitle(thread.title);
    setDescription(thread.description || "");
    setQuestion(thread.question || "");
    setWhyItMatters(thread.why_it_matters || "");
    setStatus(thread.status);
    setSeverity(thread.severity || "");
    setTrend(thread.trend || "");
    setFirstRaised(thread.opened_date || "");
    setResolution(thread.resolution || "");
    setDirty(false);
    setError(null);
  }, [thread]);

  function markDirty() { setDirty(true); }

  async function handleSave() {
    if (!title.trim()) { setError("Title is required"); return; }
    setSaving(true);
    setError(null);
    try {
      const body: OpenThreadUpdate = {
        title: title.trim(),
        context: description || undefined,
        question: question || undefined,
        why_it_matters: whyItMatters || undefined,
        status,
        severity: severity || undefined,
        trend: trend || undefined,
        first_raised: firstRaised || undefined,
        resolution: resolution || undefined,
      };
      await api.updateOpenThread(thread.id, body);
      setDirty(false);
      onUpdated();
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : "Failed to save");
    } finally {
      setSaving(false);
    }
  }

  async function handleDelete() {
    if (!confirm("Delete this thread? This cannot be undone.")) return;
    setDeleting(true);
    try {
      await api.deleteOpenThread(thread.id);
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
        <span className="text-base font-medium text-forest-400 dark:text-forest-300">Thread Detail</span>
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

        {/* Title */}
        <input
          value={title}
          onChange={(e) => { setTitle(e.target.value); markDirty(); }}
          className="w-full text-lg font-semibold text-forest-950 dark:text-forest-50 bg-transparent border-0 focus:outline-none focus:ring-0 p-0"
          placeholder="Thread title"
        />

        {/* Context / Description */}
        <div>
          <label className="block text-sm font-medium text-forest-400 dark:text-forest-300 mb-1">Context</label>
          <textarea
            value={description}
            onChange={(e) => { setDescription(e.target.value); markDirty(); }}
            rows={3}
            className="w-full text-base text-forest-600 dark:text-forest-200 bg-forest-50 dark:bg-forest-800 border border-forest-200 dark:border-forest-700 rounded-md px-3 py-2 focus:outline-none focus:ring-1 focus:ring-forest-500"
            placeholder="What is the context for this thread?"
          />
        </div>

        {/* Question */}
        <div>
          <label className="block text-sm font-medium text-forest-400 dark:text-forest-300 mb-1">Question</label>
          <textarea
            value={question}
            onChange={(e) => { setQuestion(e.target.value); markDirty(); }}
            rows={2}
            className="w-full text-base text-forest-600 dark:text-forest-200 bg-forest-50 dark:bg-forest-800 border border-forest-200 dark:border-forest-700 rounded-md px-3 py-2 focus:outline-none focus:ring-1 focus:ring-forest-500"
            placeholder="What is the open question?"
          />
        </div>

        {/* Why It Matters */}
        <div>
          <label className="block text-sm font-medium text-forest-400 dark:text-forest-300 mb-1">Why It Matters</label>
          <textarea
            value={whyItMatters}
            onChange={(e) => { setWhyItMatters(e.target.value); markDirty(); }}
            rows={2}
            className="w-full text-base text-forest-600 dark:text-forest-200 bg-forest-50 dark:bg-forest-800 border border-forest-200 dark:border-forest-700 rounded-md px-3 py-2 focus:outline-none focus:ring-1 focus:ring-forest-500"
            placeholder="Why does this matter to the programme?"
          />
        </div>

        {/* Status + Severity */}
        <div className="grid grid-cols-2 gap-3">
          <div>
            <label className="block text-sm font-medium text-forest-400 dark:text-forest-300 mb-1">Status</label>
            <select
              value={status}
              onChange={(e) => { setStatus(e.target.value); markDirty(); }}
              className="w-full text-base border border-forest-200 dark:border-forest-700 rounded-md px-2 py-1.5 bg-white dark:bg-forest-800 text-forest-950 dark:text-forest-50"
            >
              {THREAD_STATUSES.map((s) => (
                <option key={s} value={s}>{THREAD_STATUS_CONFIG[s].label}</option>
              ))}
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium text-forest-400 dark:text-forest-300 mb-1">Severity</label>
            <select
              value={severity}
              onChange={(e) => { setSeverity(e.target.value); markDirty(); }}
              className="w-full text-base border border-forest-200 dark:border-forest-700 rounded-md px-2 py-1.5 bg-white dark:bg-forest-800 text-forest-950 dark:text-forest-50"
            >
              <option value="">None</option>
              {THREAD_SEVERITIES.map((s) => (
                <option key={s} value={s}>{SEVERITY_CONFIG[s].label}</option>
              ))}
            </select>
          </div>
        </div>

        {/* Trend */}
        <div>
          <label className="block text-sm font-medium text-forest-400 dark:text-forest-300 mb-1">Trend</label>
          <select
            value={trend}
            onChange={(e) => { setTrend(e.target.value); markDirty(); }}
            className="w-full text-base border border-forest-200 dark:border-forest-700 rounded-md px-2 py-1.5 bg-white dark:bg-forest-800 text-forest-950 dark:text-forest-50"
          >
            <option value="">None</option>
            {TREND_OPTIONS.map((t) => (
              <option key={t} value={t}>
                {t === "escalating" ? "\u2191 Escalating" : t === "stable" ? "\u2192 Stable" : "\u2193 De-escalating"}
              </option>
            ))}
          </select>
        </div>

        {/* First Raised */}
        <div>
          <label className="block text-sm font-medium text-forest-400 dark:text-forest-300 mb-1">First Raised</label>
          <input
            type="date"
            value={firstRaised}
            onChange={(e) => { setFirstRaised(e.target.value); markDirty(); }}
            className="w-full text-base border border-forest-200 dark:border-forest-700 rounded-md px-2 py-1.5 bg-white dark:bg-forest-800 text-forest-950 dark:text-forest-50"
          />
        </div>

        {/* Resolution */}
        <div>
          <label className="block text-sm font-medium text-forest-400 dark:text-forest-300 mb-1">Resolution</label>
          <textarea
            value={resolution}
            onChange={(e) => { setResolution(e.target.value); markDirty(); }}
            rows={3}
            className="w-full text-base text-forest-600 dark:text-forest-200 bg-forest-50 dark:bg-forest-800 border border-forest-200 dark:border-forest-700 rounded-md px-3 py-2 focus:outline-none focus:ring-1 focus:ring-forest-500"
            placeholder="How was this resolved?"
          />
        </div>

        {/* Metadata */}
        <div className="pt-2 border-t border-forest-200 dark:border-forest-700 text-sm text-forest-300 space-y-1">
          {thread.last_discussed && <p>Last discussed: {new Date(thread.last_discussed).toLocaleDateString("en-GB", { day: "numeric", month: "short", year: "numeric" })}</p>}
          {thread.owner && <p>Owner: {thread.owner}</p>}
          {thread.project && <p>Project: {thread.project}</p>}
        </div>
      </div>

      {/* Footer actions */}
      <div className="flex items-center justify-between px-4 py-3 border-t border-forest-200 dark:border-forest-700 bg-forest-50 dark:bg-forest-800/50">
        <div className="flex gap-2">
          <button
            onClick={handleDelete}
            disabled={deleting}
            className="flex items-center gap-1 px-3 py-1.5 text-sm text-red-600 hover:bg-red-50 dark:hover:bg-red-900/20 rounded-md transition-colors disabled:opacity-50"
          >
            <Trash2 className="h-3.5 w-3.5" />
            {deleting ? "Deleting..." : "Delete"}
          </button>
        </div>
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
