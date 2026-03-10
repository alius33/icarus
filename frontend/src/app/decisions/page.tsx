"use client";

import { useEffect, useState, useCallback } from "react";
import { api } from "@/lib/api";
import { formatDate } from "@/lib/utils";
import type { DecisionSchema } from "@/lib/types";
import EntityModal, { FormInput, FormTextarea } from "@/components/EntityModal";

export default function DecisionsPage() {
  const [decisions, setDecisions] = useState<DecisionSchema[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const [modalOpen, setModalOpen] = useState(false);
  const [editingItem, setEditingItem] = useState<DecisionSchema | null>(null);
  const [formDecision, setFormDecision] = useState("");
  const [formDate, setFormDate] = useState("");
  const [formRationale, setFormRationale] = useState("");
  const [formPeople, setFormPeople] = useState("");
  const [saving, setSaving] = useState(false);
  const [deleting, setDeleting] = useState(false);
  const [modalError, setModalError] = useState<string | null>(null);

  const reload = useCallback(() => { api.getDecisions().then(setDecisions).catch(() => {}); }, []);

  useEffect(() => {
    api.getDecisions().then(setDecisions)
      .catch((e) => setError(e instanceof Error ? e.message : "Failed to load decisions"))
      .finally(() => setLoading(false));
  }, []);

  const openCreate = () => {
    setEditingItem(null); setFormDecision(""); setFormDate(""); setFormRationale(""); setFormPeople("");
    setModalError(null); setModalOpen(true);
  };
  const openEdit = (d: DecisionSchema) => {
    setEditingItem(d); setFormDecision(d.description || d.title); setFormDate(d.date || "");
    setFormRationale(""); setFormPeople(d.owner || "");
    setModalError(null); setModalOpen(true);
  };
  const handleSave = async () => {
    setSaving(true); setModalError(null);
    try {
      const people = formPeople ? formPeople.split(",").map(s => s.trim()).filter(Boolean) : [];
      if (editingItem) {
        await api.updateDecision(editingItem.id, { decision: formDecision, date: formDate || undefined, rationale: formRationale || undefined, key_people: people });
      } else {
        await api.createDecision({ decision: formDecision, date: formDate || undefined, rationale: formRationale || undefined, key_people: people });
      }
      setModalOpen(false); reload();
    } catch (e) { setModalError(e instanceof Error ? e.message : "Save failed"); }
    finally { setSaving(false); }
  };
  const handleDelete = async () => {
    if (!editingItem) return; setDeleting(true);
    try { await api.deleteDecision(editingItem.id); setModalOpen(false); reload(); }
    catch (e) { setModalError(e instanceof Error ? e.message : "Delete failed"); }
    finally { setDeleting(false); }
  };

  if (loading) return (<div className="space-y-6"><h2 className="text-2xl font-bold text-gray-900">Decision Log</h2><p className="text-sm text-gray-500">Loading decisions...</p></div>);
  if (error) return (<div className="space-y-6"><h2 className="text-2xl font-bold text-gray-900">Decision Log</h2><div className="rounded-lg border border-red-200 bg-red-50 p-6"><p className="text-sm text-red-700">{error}</p></div></div>);

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h2 className="text-2xl font-bold text-gray-900">Decision Log</h2>
        <div className="flex items-center gap-4">
          <span className="text-sm text-gray-500">{decisions.length} decision{decisions.length !== 1 ? "s" : ""}</span>
          <button onClick={openCreate} className="px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-md hover:bg-blue-700 transition-colors">+ New Decision</button>
        </div>
      </div>

      {decisions.length === 0 ? (
        <div className="text-center py-12"><p className="text-sm text-gray-500">No decisions recorded yet.</p></div>
      ) : (
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden">
          <table className="w-full">
            <thead><tr className="border-b border-gray-200 bg-gray-50">
              <th className="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider text-gray-500 w-12">#</th>
              <th className="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider text-gray-500 w-28">Date</th>
              <th className="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider text-gray-500">Decision</th>
              <th className="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider text-gray-500 w-48">Key People</th>
              <th className="px-3 py-3 w-10"></th>
            </tr></thead>
            <tbody className="divide-y divide-gray-200">
              {decisions.map((d) => {
                return (
                  <tr key={d.id} className="hover:bg-gray-50 transition-colors cursor-pointer"
                    onClick={() => openEdit(d)}>
                    <td className="px-6 py-4 text-sm text-gray-400 tabular-nums align-top">{d.id}</td>
                    <td className="px-6 py-4 text-sm text-gray-500 whitespace-nowrap align-top">{d.date ? formatDate(d.date) : "\u2014"}</td>
                    <td className="px-6 py-4 align-top">
                      <p className="text-sm text-gray-900">{d.title}</p>
                      {d.description && <p className="mt-1 text-xs text-gray-500 line-clamp-2">{d.description}</p>}
                    </td>
                    <td className="px-6 py-4 align-top">
                      <div className="flex flex-wrap gap-1">
                        {d.owner && <span className="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-blue-50 text-blue-700 border border-blue-200">{d.owner}</span>}
                      </div>
                    </td>
                    <td className="px-3 py-4 align-top">
                      <button onClick={(e) => { e.stopPropagation(); openEdit(d); }} className="text-gray-400 hover:text-blue-600" title="Edit">
                        <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" /></svg>
                      </button>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      )}

      <EntityModal open={modalOpen} onClose={() => setModalOpen(false)} title={editingItem ? "Edit Decision" : "New Decision"}
        onSave={handleSave} onDelete={editingItem ? handleDelete : undefined} saving={saving} deleting={deleting} error={modalError}>
        <FormTextarea label="Decision" value={formDecision} onChange={setFormDecision} placeholder="What was decided?" />
        <FormInput label="Date" value={formDate} onChange={setFormDate} placeholder="YYYY-MM-DD" />
        <FormTextarea label="Rationale" value={formRationale} onChange={setFormRationale} placeholder="Why was this decided?" rows={2} />
        <FormInput label="Key People" value={formPeople} onChange={setFormPeople} placeholder="Comma-separated names" />
      </EntityModal>
    </div>
  );
}
