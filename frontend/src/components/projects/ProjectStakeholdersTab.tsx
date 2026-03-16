"use client";

import { useState } from "react";
import Link from "next/link";
import { api } from "@/lib/api";
import { tierLabels } from "@/lib/utils";
import type { StakeholderBase } from "@/lib/types";
import EntityModal, { FormInput, FormTextarea, FormSelect } from "@/components/EntityModal";

export default function ProjectStakeholdersTab({
  stakeholders: initialStakeholders,
}: {
  stakeholders: StakeholderBase[];
}) {
  const [stakeholders, setStakeholders] = useState(initialStakeholders);
  const [modalOpen, setModalOpen] = useState(false);
  const [editingItem, setEditingItem] = useState<StakeholderBase | null>(null);
  const [formName, setFormName] = useState("");
  const [formTier, setFormTier] = useState("3");
  const [formRole, setFormRole] = useState("");
  const [formNotes, setFormNotes] = useState("");
  const [saving, setSaving] = useState(false);
  const [deleting, setDeleting] = useState(false);
  const [modalError, setModalError] = useState<string | null>(null);

  const openCreate = () => {
    setEditingItem(null); setFormName(""); setFormTier("3"); setFormRole(""); setFormNotes("");
    setModalError(null); setModalOpen(true);
  };
  const openEdit = (s: StakeholderBase) => {
    setEditingItem(s); setFormName(s.name); setFormTier(String(s.tier)); setFormRole(s.role || ""); setFormNotes("");
    setModalError(null); setModalOpen(true);
  };
  const handleSave = async () => {
    setSaving(true); setModalError(null);
    try {
      if (editingItem) {
        const updated = await api.updateStakeholder(editingItem.id, { tier: Number(formTier), role: formRole || undefined, notes: formNotes || undefined });
        setStakeholders((prev) => prev.map((s) => s.id === updated.id ? updated : s));
      } else {
        const created = await api.createStakeholder({ name: formName, tier: Number(formTier), role: formRole || undefined, notes: formNotes || undefined });
        setStakeholders((prev) => [...prev, created]);
      }
      setModalOpen(false);
    } catch (e) { setModalError(e instanceof Error ? e.message : "Save failed"); }
    finally { setSaving(false); }
  };
  const handleDelete = async () => {
    if (!editingItem) return; setDeleting(true);
    try { await api.deleteStakeholder(editingItem.id); setStakeholders((prev) => prev.filter((s) => s.id !== editingItem.id)); setModalOpen(false); }
    catch (e) { setModalError(e instanceof Error ? e.message : "Delete failed"); }
    finally { setDeleting(false); }
  };

  return (
    <div className="space-y-4">
      <div className="flex justify-end">
        <button onClick={openCreate} className="px-4 py-2 text-base font-medium text-white bg-forest-500 rounded-md hover:bg-forest-600 transition-colors">+ New Stakeholder</button>
      </div>

      {stakeholders.length === 0 ? (
        <div className="rounded-lg border border-forest-200 bg-white dark:bg-forest-800 p-8 text-center">
          <p className="text-base text-forest-400">No stakeholders linked to this project yet.</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {stakeholders.map((s) => (
            <div key={s.id} className="relative group rounded-lg border border-forest-200 bg-white dark:bg-forest-800 p-4 transition-shadow hover:shadow-md">
              <button onClick={(e) => { e.preventDefault(); openEdit(s); }}
                className="absolute top-4 right-4 text-forest-300 hover:text-forest-500 opacity-0 group-hover:opacity-100 transition-opacity" title="Edit">
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" /></svg>
              </button>
              <Link href={`/stakeholders/${s.id}`} className="block">
                <div className="flex items-start justify-between">
                  <div>
                    <h4 className="text-base font-semibold text-forest-950">{s.name}</h4>
                    {s.role && <p className="mt-0.5 text-sm text-forest-400">{s.role}</p>}
                  </div>
                  <span className="inline-flex items-center rounded-full bg-blue-50 px-2 py-0.5 text-sm font-medium text-forest-600">
                    Tier {s.tier}
                  </span>
                </div>
                <div className="mt-3 flex items-center justify-between text-sm text-forest-300">
                  <span>{tierLabels[s.tier] || `Tier ${s.tier}`}</span>
                  <span>{s.mention_count} mentions</span>
                </div>
              </Link>
            </div>
          ))}
        </div>
      )}

      <EntityModal open={modalOpen} onClose={() => setModalOpen(false)} title={editingItem ? "Edit Stakeholder" : "New Stakeholder"}
        onSave={handleSave} onDelete={editingItem ? handleDelete : undefined} saving={saving} deleting={deleting} error={modalError}>
        <FormInput label="Name" value={formName} onChange={setFormName} placeholder="Full name" disabled={!!editingItem} />
        <FormSelect label="Tier" value={formTier} onChange={setFormTier} options={[{ value: "1", label: "Tier 1 - Key Decision Makers" }, { value: "2", label: "Tier 2 - Active Participants" }, { value: "3", label: "Tier 3 - Peripheral" }]} />
        <FormInput label="Role" value={formRole} onChange={setFormRole} placeholder="Role / title" />
        <FormTextarea label="Notes" value={formNotes} onChange={setFormNotes} placeholder="Additional notes..." rows={2} />
      </EntityModal>
    </div>
  );
}
