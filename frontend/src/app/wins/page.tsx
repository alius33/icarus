"use client";

import { useEffect, useState, useCallback } from "react";
import { api } from "@/lib/api";
import { formatDate } from "@/lib/utils";
import type { ProgrammeWinSchema, ProgrammeWinCreate } from "@/lib/types";
import EntityModal, {
  FormInput,
  FormTextarea,
  FormSelect,
} from "@/components/EntityModal";

/* ── helpers ─────────────────────────────────────────────────────────── */

const CATEGORIES = [
  { value: "time_saved", label: "Time Saved" },
  { value: "adoption", label: "Adoption" },
  { value: "quality", label: "Quality" },
  { value: "reach", label: "Reach" },
  { value: "process_improvement", label: "Process Improvement" },
];

const CONFIDENCE_OPTIONS = [
  { value: "measured", label: "Measured" },
  { value: "estimated", label: "Estimated" },
  { value: "anecdotal", label: "Anecdotal" },
];

function categoryLabel(cat: string): string {
  return (
    CATEGORIES.find((c) => c.value === cat)?.label ?? cat.replace(/_/g, " ")
  );
}

function categoryIcon(cat: string): string {
  switch (cat) {
    case "time_saved":
      return "clock";
    case "adoption":
      return "users";
    case "quality":
      return "check-circle";
    case "reach":
      return "globe";
    case "process_improvement":
      return "cog";
    default:
      return "star";
  }
}

function categoryColor(cat: string): string {
  switch (cat) {
    case "time_saved":
      return "bg-purple-50 border-purple-200 text-purple-700";
    case "adoption":
      return "bg-blue-50 border-blue-200 text-blue-700";
    case "quality":
      return "bg-green-50 border-green-200 text-green-700";
    case "reach":
      return "bg-orange-50 border-orange-200 text-orange-700";
    case "process_improvement":
      return "bg-indigo-50 border-indigo-200 text-indigo-700";
    default:
      return "bg-gray-50 border-gray-200 text-gray-700";
  }
}

function confidenceBadge(confidence: string) {
  switch (confidence) {
    case "measured":
      return (
        <span className="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800 border border-green-200">
          Measured
        </span>
      );
    case "estimated":
      return (
        <span className="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-amber-100 text-amber-800 border border-amber-200">
          Estimated
        </span>
      );
    case "anecdotal":
    default:
      return (
        <span className="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-gray-100 text-gray-600 border border-gray-200">
          Anecdotal
        </span>
      );
  }
}

function CategoryIconSvg({ category }: { category: string }) {
  const base = "w-5 h-5 flex-shrink-0";
  switch (categoryIcon(category)) {
    case "clock":
      return (
        <svg
          className={base}
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <circle cx="12" cy="12" r="10" strokeWidth={2} />
          <path strokeLinecap="round" strokeWidth={2} d="M12 6v6l4 2" />
        </svg>
      );
    case "users":
      return (
        <svg
          className={base}
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0z"
          />
        </svg>
      );
    case "check-circle":
      return (
        <svg
          className={base}
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
          />
        </svg>
      );
    case "globe":
      return (
        <svg
          className={base}
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M3.055 11H5a2 2 0 012 2v1a2 2 0 002 2 2 2 0 012 2v2.945M8 3.935V5.5A2.5 2.5 0 0010.5 8h.5a2 2 0 012 2 2 2 0 104 0 2 2 0 012-2h1.064M15 20.488V18a2 2 0 012-2h3.064M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
          />
        </svg>
      );
    case "cog":
      return (
        <svg
          className={base}
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.066 2.573c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.573 1.066c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.066-2.573c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"
          />
          <circle cx="12" cy="12" r="3" strokeWidth={2} />
        </svg>
      );
    default:
      return (
        <svg
          className={base}
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M11.049 2.927c.3-.921 1.603-.921 1.902 0l1.519 4.674a1 1 0 00.95.69h4.915c.969 0 1.371 1.24.588 1.81l-3.976 2.888a1 1 0 00-.363 1.118l1.518 4.674c.3.922-.755 1.688-1.538 1.118l-3.976-2.888a1 1 0 00-1.176 0l-3.976 2.888c-.783.57-1.838-.197-1.538-1.118l1.518-4.674a1 1 0 00-.363-1.118l-3.976-2.888c-.784-.57-.38-1.81.588-1.81h4.914a1 1 0 00.951-.69l1.519-4.674z"
          />
        </svg>
      );
  }
}

/* ── component ───────────────────────────────────────────────────────── */

export default function WinsPage() {
  const [wins, setWins] = useState<ProgrammeWinSchema[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  /* modal state */
  const [modalOpen, setModalOpen] = useState(false);
  const [editingItem, setEditingItem] = useState<ProgrammeWinSchema | null>(
    null,
  );
  const [saving, setSaving] = useState(false);
  const [deleting, setDeleting] = useState(false);
  const [modalError, setModalError] = useState<string | null>(null);

  /* form state */
  const [formCategory, setFormCategory] = useState("time_saved");
  const [formTitle, setFormTitle] = useState("");
  const [formDescription, setFormDescription] = useState("");
  const [formBefore, setFormBefore] = useState("");
  const [formAfter, setFormAfter] = useState("");
  const [formWorkstream, setFormWorkstream] = useState("");
  const [formConfidence, setFormConfidence] = useState("estimated");
  const [formDate, setFormDate] = useState("");
  const [formNotes, setFormNotes] = useState("");

  /* filter state */
  const [filterCategory, setFilterCategory] = useState<string>("all");

  const reload = useCallback(() => {
    api
      .getWins()
      .then(setWins)
      .catch(() => {});
  }, []);

  useEffect(() => {
    api
      .getWins()
      .then(setWins)
      .catch((e) =>
        setError(e instanceof Error ? e.message : "Failed to load wins"),
      )
      .finally(() => setLoading(false));
  }, []);

  const resetForm = () => {
    setFormCategory("time_saved");
    setFormTitle("");
    setFormDescription("");
    setFormBefore("");
    setFormAfter("");
    setFormWorkstream("");
    setFormConfidence("estimated");
    setFormDate("");
    setFormNotes("");
  };

  const openCreate = () => {
    setEditingItem(null);
    resetForm();
    setModalError(null);
    setModalOpen(true);
  };

  const openEdit = (win: ProgrammeWinSchema) => {
    setEditingItem(win);
    setFormCategory(win.category);
    setFormTitle(win.title);
    setFormDescription(win.description || "");
    setFormBefore(win.before_state || "");
    setFormAfter(win.after_state || "");
    setFormWorkstream(win.workstream || "");
    setFormConfidence(win.confidence);
    setFormDate(win.date_recorded || "");
    setFormNotes(win.notes || "");
    setModalError(null);
    setModalOpen(true);
  };

  const handleSave = async () => {
    if (!formTitle.trim()) {
      setModalError("Title is required.");
      return;
    }
    setSaving(true);
    setModalError(null);
    try {
      const data: ProgrammeWinCreate = {
        category: formCategory,
        title: formTitle.trim(),
        description: formDescription.trim() || undefined,
        before_state: formBefore.trim() || undefined,
        after_state: formAfter.trim() || undefined,
        workstream: formWorkstream.trim() || undefined,
        confidence: formConfidence,
        date_recorded: formDate || undefined,
        notes: formNotes.trim() || undefined,
      };
      if (editingItem) {
        await api.updateWin(editingItem.id, data);
      } else {
        await api.createWin(data);
      }
      setModalOpen(false);
      reload();
    } catch (e) {
      setModalError(e instanceof Error ? e.message : "Save failed");
    } finally {
      setSaving(false);
    }
  };

  const handleDelete = async () => {
    if (!editingItem) return;
    setDeleting(true);
    try {
      await api.deleteWin(editingItem.id);
      setModalOpen(false);
      reload();
    } catch (e) {
      setModalError(e instanceof Error ? e.message : "Delete failed");
    } finally {
      setDeleting(false);
    }
  };

  /* derived data */
  const filteredWins =
    filterCategory === "all"
      ? wins
      : wins.filter((w) => w.category === filterCategory);

  const grouped = filteredWins.reduce(
    (acc, w) => {
      const cat = w.category;
      if (!acc[cat]) acc[cat] = [];
      acc[cat].push(w);
      return acc;
    },
    {} as Record<string, ProgrammeWinSchema[]>,
  );

  const measuredCount = wins.filter((w) => w.confidence === "measured").length;
  const uniqueWorkstreams = new Set(
    wins.map((w) => w.workstream).filter(Boolean),
  );

  /* render */
  if (loading) {
    return (
      <div className="space-y-6">
        <h2 className="text-2xl font-bold text-gray-900">Programme Wins</h2>
        <p className="text-sm text-gray-500">Loading wins...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="space-y-6">
        <h2 className="text-2xl font-bold text-gray-900">Programme Wins</h2>
        <div className="rounded-lg border border-red-200 bg-red-50 p-6">
          <p className="text-sm text-red-700">{error}</p>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* header */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold text-gray-900">Programme Wins</h2>
          <p className="mt-1 text-sm text-gray-500">
            Track and celebrate measurable programme achievements
          </p>
        </div>
        <button
          onClick={openCreate}
          className="px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-md hover:bg-blue-700 transition-colors"
        >
          + New Win
        </button>
      </div>

      {/* summary stats bar */}
      <div className="grid grid-cols-1 sm:grid-cols-4 gap-4">
        <div className="bg-white rounded-lg border border-gray-200 p-4">
          <p className="text-xs font-medium uppercase tracking-wider text-gray-500">
            Total Wins
          </p>
          <p className="mt-1 text-2xl font-bold text-gray-900">{wins.length}</p>
        </div>
        <div className="bg-white rounded-lg border border-gray-200 p-4">
          <p className="text-xs font-medium uppercase tracking-wider text-gray-500">
            Measured
          </p>
          <p className="mt-1 text-2xl font-bold text-green-600">
            {measuredCount}
          </p>
        </div>
        <div className="bg-white rounded-lg border border-gray-200 p-4">
          <p className="text-xs font-medium uppercase tracking-wider text-gray-500">
            Workstreams
          </p>
          <p className="mt-1 text-2xl font-bold text-blue-600">
            {uniqueWorkstreams.size}
          </p>
        </div>
        <div className="bg-white rounded-lg border border-gray-200 p-4">
          <p className="text-xs font-medium uppercase tracking-wider text-gray-500">
            Categories
          </p>
          <p className="mt-1 text-2xl font-bold text-purple-600">
            {Object.keys(grouped).length}
          </p>
        </div>
      </div>

      {/* category filter */}
      <div className="flex items-center gap-2 flex-wrap">
        <span className="text-sm font-medium text-gray-700">Filter:</span>
        <button
          onClick={() => setFilterCategory("all")}
          className={`px-3 py-1 text-xs font-medium rounded-full border transition-colors ${
            filterCategory === "all"
              ? "bg-gray-900 text-white border-gray-900"
              : "bg-white text-gray-600 border-gray-300 hover:border-gray-400"
          }`}
        >
          All
        </button>
        {CATEGORIES.map((cat) => (
          <button
            key={cat.value}
            onClick={() => setFilterCategory(cat.value)}
            className={`px-3 py-1 text-xs font-medium rounded-full border transition-colors ${
              filterCategory === cat.value
                ? "bg-gray-900 text-white border-gray-900"
                : "bg-white text-gray-600 border-gray-300 hover:border-gray-400"
            }`}
          >
            {cat.label}
          </button>
        ))}
      </div>

      {/* wins by category */}
      {filteredWins.length === 0 ? (
        <div className="text-center py-12">
          <p className="text-sm text-gray-500">
            No wins recorded yet. Click &ldquo;+ New Win&rdquo; to add your
            first programme win.
          </p>
        </div>
      ) : (
        Object.entries(grouped)
          .sort(([a], [b]) => a.localeCompare(b))
          .map(([category, catWins]) => (
            <div key={category} className="space-y-3">
              <div className="flex items-center gap-2">
                <div className={`p-1.5 rounded-md border ${categoryColor(category)}`}>
                  <CategoryIconSvg category={category} />
                </div>
                <h3 className="text-lg font-semibold text-gray-900">
                  {categoryLabel(category)}
                </h3>
                <span className="text-sm text-gray-400">
                  ({catWins.length})
                </span>
              </div>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {catWins.map((win) => (
                  <div
                    key={win.id}
                    className="bg-white rounded-lg border border-gray-200 shadow-sm hover:shadow-md transition-shadow cursor-pointer"
                    onClick={() => openEdit(win)}
                  >
                    <div className="p-5">
                      {/* top row: title + confidence */}
                      <div className="flex items-start justify-between gap-3 mb-3">
                        <h4 className="text-sm font-semibold text-gray-900 leading-tight">
                          {win.title}
                        </h4>
                        {confidenceBadge(win.confidence)}
                      </div>

                      {/* description */}
                      {win.description && (
                        <p className="text-sm text-gray-600 mb-3">
                          {win.description}
                        </p>
                      )}

                      {/* before / after */}
                      {(win.before_state || win.after_state) && (
                        <div className="flex gap-3 mb-3">
                          {win.before_state && (
                            <div className="flex-1 bg-red-50 border border-red-100 rounded-md p-3">
                              <p className="text-xs font-medium text-red-500 mb-1">
                                Before
                              </p>
                              <p className="text-sm text-red-800">
                                {win.before_state}
                              </p>
                            </div>
                          )}
                          {win.before_state && win.after_state && (
                            <div className="flex items-center">
                              <svg
                                className="w-5 h-5 text-gray-400"
                                fill="none"
                                stroke="currentColor"
                                viewBox="0 0 24 24"
                              >
                                <path
                                  strokeLinecap="round"
                                  strokeLinejoin="round"
                                  strokeWidth={2}
                                  d="M13 7l5 5m0 0l-5 5m5-5H6"
                                />
                              </svg>
                            </div>
                          )}
                          {win.after_state && (
                            <div className="flex-1 bg-green-50 border border-green-100 rounded-md p-3">
                              <p className="text-xs font-medium text-green-500 mb-1">
                                After
                              </p>
                              <p className="text-sm text-green-800">
                                {win.after_state}
                              </p>
                            </div>
                          )}
                        </div>
                      )}

                      {/* meta row */}
                      <div className="flex items-center gap-3 text-xs text-gray-400">
                        {win.workstream && (
                          <span className="inline-flex items-center px-2 py-0.5 rounded-full bg-blue-50 text-blue-700 border border-blue-200 font-medium">
                            {win.workstream}
                          </span>
                        )}
                        {win.date_recorded && (
                          <span>{formatDate(win.date_recorded)}</span>
                        )}
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          ))
      )}

      {/* modal */}
      <EntityModal
        open={modalOpen}
        onClose={() => setModalOpen(false)}
        title={editingItem ? "Edit Win" : "New Programme Win"}
        onSave={handleSave}
        onDelete={editingItem ? handleDelete : undefined}
        saving={saving}
        deleting={deleting}
        error={modalError}
      >
        <FormSelect
          label="Category"
          value={formCategory}
          onChange={setFormCategory}
          options={CATEGORIES}
        />
        <FormInput
          label="Title"
          value={formTitle}
          onChange={setFormTitle}
          placeholder="What was achieved?"
        />
        <FormTextarea
          label="Description"
          value={formDescription}
          onChange={setFormDescription}
          placeholder="Details about this win"
          rows={2}
        />
        <div className="grid grid-cols-2 gap-4">
          <FormTextarea
            label="Before"
            value={formBefore}
            onChange={setFormBefore}
            placeholder="State before the win"
            rows={2}
          />
          <FormTextarea
            label="After"
            value={formAfter}
            onChange={setFormAfter}
            placeholder="State after the win"
            rows={2}
          />
        </div>
        <div className="grid grid-cols-2 gap-4">
          <FormInput
            label="Workstream"
            value={formWorkstream}
            onChange={setFormWorkstream}
            placeholder="e.g. WS2"
          />
          <FormSelect
            label="Confidence"
            value={formConfidence}
            onChange={setFormConfidence}
            options={CONFIDENCE_OPTIONS}
          />
        </div>
        <FormInput
          label="Date Recorded"
          value={formDate}
          onChange={setFormDate}
          placeholder="YYYY-MM-DD"
          type="date"
        />
        <FormTextarea
          label="Notes"
          value={formNotes}
          onChange={setFormNotes}
          placeholder="Additional notes"
          rows={2}
        />
      </EntityModal>
    </div>
  );
}
