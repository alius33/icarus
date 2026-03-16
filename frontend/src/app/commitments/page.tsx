"use client";

import { useEffect, useState, useCallback, useMemo } from "react";
import { api } from "@/lib/api";
import { formatDate } from "@/lib/utils";
import type { CommitmentSchema } from "@/lib/types";
import EntityModal, {
  FormInput,
  FormTextarea,
  FormSelect,
} from "@/components/EntityModal";

const STATUS_OPTIONS = [
  { value: "pending", label: "Pending" },
  { value: "fulfilled", label: "Fulfilled" },
  { value: "broken", label: "Broken" },
  { value: "formalised", label: "Formalised" },
  { value: "conditional", label: "Conditional" },
];

const STATUS_COLORS: Record<string, string> = {
  pending: "bg-amber-50 text-amber-700 border-amber-200",
  fulfilled: "bg-green-50 text-green-700 border-green-200",
  broken: "bg-red-50 text-red-700 border-red-200",
  formalised: "bg-forest-100 text-forest-600 border-blue-200",
  conditional: "bg-forest-50 text-forest-500 border-forest-200",
};

const STATUS_ORDER = ["pending", "conditional", "formalised", "fulfilled", "broken"];

export default function CommitmentsPage() {
  const [commitments, setCommitments] = useState<CommitmentSchema[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const [personFilter, setPersonFilter] = useState("");

  // Modal state
  const [modalOpen, setModalOpen] = useState(false);
  const [editingItem, setEditingItem] = useState<CommitmentSchema | null>(null);
  const [formPerson, setFormPerson] = useState("");
  const [formCommitment, setFormCommitment] = useState("");
  const [formStatus, setFormStatus] = useState("pending");
  const [formDateMade, setFormDateMade] = useState("");
  const [formDeadlineText, setFormDeadlineText] = useState("");
  const [formCondition, setFormCondition] = useState("");
  const [formNotes, setFormNotes] = useState("");
  const [saving, setSaving] = useState(false);
  const [deleting, setDeleting] = useState(false);
  const [modalError, setModalError] = useState<string | null>(null);

  const reload = useCallback(() => {
    api
      .getCommitments()
      .then(setCommitments)
      .catch(() => {});
  }, []);

  useEffect(() => {
    api
      .getCommitments()
      .then(setCommitments)
      .catch((e) =>
        setError(e instanceof Error ? e.message : "Failed to load commitments"),
      )
      .finally(() => setLoading(false));
  }, []);

  const uniquePersons = useMemo(() => {
    const names = new Set(commitments.map((c) => c.person));
    return Array.from(names).sort();
  }, [commitments]);

  const filtered = useMemo(() => {
    if (!personFilter) return commitments;
    return commitments.filter((c) => c.person === personFilter);
  }, [commitments, personFilter]);

  const grouped = useMemo(() => {
    const groups: Record<string, CommitmentSchema[]> = {};
    for (const status of STATUS_ORDER) {
      const items = filtered.filter((c) => c.status === status);
      if (items.length > 0) groups[status] = items;
    }
    // Catch any statuses not in the predefined order
    const knownStatuses = new Set(STATUS_ORDER);
    const remaining = filtered.filter((c) => !knownStatuses.has(c.status));
    if (remaining.length > 0) groups["other"] = remaining;
    return groups;
  }, [filtered]);

  const openCreate = () => {
    setEditingItem(null);
    setFormPerson("");
    setFormCommitment("");
    setFormStatus("pending");
    setFormDateMade("");
    setFormDeadlineText("");
    setFormCondition("");
    setFormNotes("");
    setModalError(null);
    setModalOpen(true);
  };

  const openEdit = (c: CommitmentSchema) => {
    setEditingItem(c);
    setFormPerson(c.person);
    setFormCommitment(c.commitment);
    setFormStatus(c.status);
    setFormDateMade(c.date_made || "");
    setFormDeadlineText(c.deadline_text || "");
    setFormCondition(c.condition || "");
    setFormNotes(c.notes || "");
    setModalError(null);
    setModalOpen(true);
  };

  const handleSave = async () => {
    setSaving(true);
    setModalError(null);
    try {
      if (editingItem) {
        await api.updateCommitment(editingItem.id, {
          person: formPerson,
          commitment: formCommitment,
          status: formStatus,
          date_made: formDateMade || undefined,
          deadline_text: formDeadlineText || undefined,
          condition: formCondition || undefined,
          notes: formNotes || undefined,
        });
      } else {
        await api.createCommitment({
          person: formPerson,
          commitment: formCommitment,
          status: formStatus,
          date_made: formDateMade || undefined,
          deadline_text: formDeadlineText || undefined,
          condition: formCondition || undefined,
          notes: formNotes || undefined,
        });
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
      await api.deleteCommitment(editingItem.id);
      setModalOpen(false);
      reload();
    } catch (e) {
      setModalError(e instanceof Error ? e.message : "Delete failed");
    } finally {
      setDeleting(false);
    }
  };

  if (loading)
    return (
      <div className="space-y-6">
        <h2 className="text-2xl font-bold text-forest-950">Commitments</h2>
        <p className="text-base text-forest-400">Loading commitments...</p>
      </div>
    );

  if (error)
    return (
      <div className="space-y-6">
        <h2 className="text-2xl font-bold text-forest-950">Commitments</h2>
        <div className="rounded-lg border border-red-200 bg-red-50 p-6">
          <p className="text-base text-red-700">{error}</p>
        </div>
      </div>
    );

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-wrap items-center justify-between gap-3">
        <h2 className="text-xl md:text-2xl font-bold text-forest-950">Commitments</h2>
        <div className="flex flex-wrap items-center gap-2 md:gap-4">
          <select
            value={personFilter}
            onChange={(e) => setPersonFilter(e.target.value)}
            className="border border-forest-200 rounded-md px-3 py-2 text-base text-forest-600 focus:outline-none focus:ring-1 focus:ring-forest-500"
          >
            <option value="">All people</option>
            {uniquePersons.map((p) => (
              <option key={p} value={p}>
                {p}
              </option>
            ))}
          </select>
          <span className="text-base text-forest-400">
            {filtered.length} commitment{filtered.length !== 1 ? "s" : ""}
          </span>
          <button
            onClick={openCreate}
            className="px-4 py-2 text-base font-medium text-white bg-forest-500 rounded-md hover:bg-forest-600 transition-colors"
          >
            + New Commitment
          </button>
        </div>
      </div>

      {/* Grouped tables */}
      {Object.keys(grouped).length === 0 ? (
        <div className="text-center py-12">
          <p className="text-base text-forest-400">No commitments recorded yet.</p>
        </div>
      ) : (
        Object.entries(grouped).map(([status, items]) => (
          <div key={status} className="space-y-2">
            <div className="flex items-center gap-2">
              <span
                className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-sm font-semibold border capitalize ${STATUS_COLORS[status] || "bg-forest-50 text-forest-500 border-forest-200"}`}
              >
                {status}
              </span>
              <span className="text-sm text-forest-300">
                {items.length} item{items.length !== 1 ? "s" : ""}
              </span>
            </div>
            {/* Mobile cards */}
            <div className="space-y-2 md:hidden">
              {items.map((c) => (
                <div
                  key={c.id}
                  className="rounded-lg border border-forest-200 p-3 active:bg-forest-50 cursor-pointer"
                  onClick={() => openEdit(c)}
                >
                  <div className="text-base font-medium text-forest-950 mb-1">{c.person}</div>
                  <p className="text-base text-forest-600 line-clamp-2">{c.commitment}</p>
                  <div className="flex flex-wrap items-center gap-2 mt-2 text-sm text-forest-400">
                    {c.date_made && <span>{formatDate(c.date_made)}</span>}
                    {c.deadline_text && <span>&middot; {c.deadline_text}</span>}
                  </div>
                  {c.notes && <p className="mt-1 text-sm text-forest-300 line-clamp-1">{c.notes}</p>}
                </div>
              ))}
            </div>

            {/* Desktop table */}
            <div className="hidden md:block bg-white dark:bg-forest-800 rounded-lg shadow-sm border border-forest-200 overflow-hidden">
              <table className="w-full">
                <thead>
                  <tr className="border-b border-forest-200 bg-forest-50">
                    <th className="px-6 py-3 text-left text-sm font-medium uppercase tracking-wider text-forest-400 w-40">
                      Person
                    </th>
                    <th className="px-6 py-3 text-left text-sm font-medium uppercase tracking-wider text-forest-400">
                      Commitment
                    </th>
                    <th className="px-6 py-3 text-left text-sm font-medium uppercase tracking-wider text-forest-400 w-32">
                      Date Made
                    </th>
                    <th className="px-6 py-3 text-left text-sm font-medium uppercase tracking-wider text-forest-400 w-40">
                      Deadline
                    </th>
                    {status === "conditional" && (
                      <th className="px-6 py-3 text-left text-sm font-medium uppercase tracking-wider text-forest-400 w-48">
                        Condition
                      </th>
                    )}
                    <th className="px-3 py-3 w-10"></th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-forest-200">
                  {items.map((c) => (
                    <tr
                      key={c.id}
                      className="hover:bg-forest-50 transition-colors cursor-pointer"
                      onClick={() => openEdit(c)}
                    >
                      <td className="px-6 py-4 text-base font-medium text-forest-950">
                        {c.person}
                      </td>
                      <td className="px-6 py-4 text-base text-forest-600">
                        {c.commitment}
                        {c.notes && (
                          <p className="mt-1 text-sm text-forest-300">
                            {c.notes}
                          </p>
                        )}
                      </td>
                      <td className="px-6 py-4 text-base text-forest-400 whitespace-nowrap">
                        {c.date_made ? formatDate(c.date_made) : "\u2014"}
                      </td>
                      <td className="px-6 py-4 text-base text-forest-400">
                        {c.deadline_text || "\u2014"}
                      </td>
                      {status === "conditional" && (
                        <td className="px-6 py-4 text-base text-forest-400 italic">
                          {c.condition || "\u2014"}
                        </td>
                      )}
                      <td className="px-3 py-4 align-top">
                        <button
                          onClick={(e) => { e.stopPropagation(); openEdit(c); }}
                          className="text-forest-300 hover:text-forest-500"
                          title="Edit"
                        >
                          <svg
                            className="w-4 h-4"
                            fill="none"
                            stroke="currentColor"
                            viewBox="0 0 24 24"
                          >
                            <path
                              strokeLinecap="round"
                              strokeLinejoin="round"
                              strokeWidth={2}
                              d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z"
                            />
                          </svg>
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        ))
      )}

      {/* Modal */}
      <EntityModal
        open={modalOpen}
        onClose={() => setModalOpen(false)}
        title={editingItem ? "Edit Commitment" : "New Commitment"}
        onSave={handleSave}
        onDelete={editingItem ? handleDelete : undefined}
        saving={saving}
        deleting={deleting}
        error={modalError}
      >
        <FormInput
          label="Person"
          value={formPerson}
          onChange={setFormPerson}
          placeholder="Who made this commitment?"
        />
        <FormTextarea
          label="Commitment"
          value={formCommitment}
          onChange={setFormCommitment}
          placeholder="What was committed to?"
        />
        <FormSelect
          label="Status"
          value={formStatus}
          onChange={setFormStatus}
          options={STATUS_OPTIONS}
        />
        <FormInput
          label="Date Made"
          value={formDateMade}
          onChange={setFormDateMade}
          placeholder="YYYY-MM-DD"
        />
        <FormInput
          label="Deadline"
          value={formDeadlineText}
          onChange={setFormDeadlineText}
          placeholder='e.g. "by end of March" or "2026-03-21"'
        />
        <FormInput
          label="Condition"
          value={formCondition}
          onChange={setFormCondition}
          placeholder="Only applies if..."
        />
        <FormTextarea
          label="Notes"
          value={formNotes}
          onChange={setFormNotes}
          placeholder="Additional context"
          rows={2}
        />
      </EntityModal>
    </div>
  );
}
