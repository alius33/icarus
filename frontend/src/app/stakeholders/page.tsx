"use client";

import { useEffect, useState, useCallback } from "react";
import Link from "next/link";
import { api } from "@/lib/api";
import { tierLabels } from "@/lib/utils";
import type { StakeholderBase } from "@/lib/types";
import EntityModal, { FormInput, FormTextarea, FormSelect } from "@/components/EntityModal";

export default function StakeholdersPage() {
  const [stakeholders, setStakeholders] = useState<StakeholderBase[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [modalOpen, setModalOpen] = useState(false);
  const [editingItem, setEditingItem] = useState<StakeholderBase | null>(null);
  const [formName, setFormName] = useState("");
  const [formTier, setFormTier] = useState("3");
  const [formRole, setFormRole] = useState("");
  const [formNotes, setFormNotes] = useState("");
  const [formRiskLevel, setFormRiskLevel] = useState("none");
  const [formMoraleNotes, setFormMoraleNotes] = useState("");
  const [saving, setSaving] = useState(false);
  const [deleting, setDeleting] = useState(false);
  const [modalError, setModalError] = useState<string | null>(null);

  const reload = useCallback(() => { api.getStakeholders().then(setStakeholders).catch(() => {}); }, []);

  useEffect(() => {
    api.getStakeholders().then(setStakeholders)
      .catch((e) => setError(e instanceof Error ? e.message : "Failed to load stakeholders"))
      .finally(() => setLoading(false));
  }, []);

  const openCreate = () => {
    setEditingItem(null); setFormName(""); setFormTier("3"); setFormRole(""); setFormNotes(""); setFormRiskLevel("none"); setFormMoraleNotes("");
    setModalError(null); setModalOpen(true);
  };
  const openEdit = (s: StakeholderBase) => {
    setEditingItem(s); setFormName(s.name); setFormTier(String(s.tier)); setFormRole(s.role || ""); setFormNotes(""); setFormRiskLevel(s.risk_level || "none"); setFormMoraleNotes(s.morale_notes || "");
    setModalError(null); setModalOpen(true);
  };
  const handleSave = async () => {
    setSaving(true); setModalError(null);
    try {
      if (editingItem) {
        await api.updateStakeholder(editingItem.id, { tier: Number(formTier), role: formRole || undefined, notes: formNotes || undefined, risk_level: formRiskLevel, morale_notes: formMoraleNotes || undefined });
      } else {
        await api.createStakeholder({ name: formName, tier: Number(formTier), role: formRole || undefined, notes: formNotes || undefined });
      }
      setModalOpen(false); reload();
    } catch (e) { setModalError(e instanceof Error ? e.message : "Save failed"); }
    finally { setSaving(false); }
  };
  const handleDelete = async () => {
    if (!editingItem) return; setDeleting(true);
    try { await api.deleteStakeholder(editingItem.id); setModalOpen(false); reload(); }
    catch (e) { setModalError(e instanceof Error ? e.message : "Delete failed"); }
    finally { setDeleting(false); }
  };

  if (loading) return (<div className="space-y-6"><h2 className="text-2xl font-bold text-gray-900">Stakeholders</h2><p className="text-base text-gray-500">Loading stakeholders...</p></div>);
  if (error) return (<div className="space-y-6"><h2 className="text-2xl font-bold text-gray-900">Stakeholders</h2><div className="rounded-lg border border-red-200 bg-red-50 p-6"><p className="text-base text-red-700">{error}</p></div></div>);

  const grouped = stakeholders.reduce<Record<number, StakeholderBase[]>>((acc, s) => {
    const tier = s.tier || 4;
    if (!acc[tier]) acc[tier] = [];
    acc[tier].push(s);
    return acc;
  }, {});
  const tiers = Object.keys(grouped).map(Number).sort((a, b) => a - b);

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold text-gray-900">Stakeholders</h2>
          <p className="mt-1 text-base text-gray-500">{stakeholders.length} stakeholders across {tiers.length} tiers</p>
        </div>
        <button onClick={openCreate} className="px-4 py-2 text-base font-medium text-white bg-blue-600 rounded-md hover:bg-blue-700 transition-colors">+ New Stakeholder</button>
      </div>

      {tiers.map((tier) => (
        <section key={tier}>
          <h3 className="text-xl font-bold text-gray-800 mb-4 mt-8">Tier {tier} &mdash; {tierLabels[tier] || "Other"}</h3>
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
            {grouped[tier].map((s) => (
              <div key={s.id} className="relative group rounded-lg border border-gray-200 bg-white p-6 shadow-sm transition-shadow hover:shadow-md">
                <button onClick={(e) => { e.preventDefault(); openEdit(s); }}
                  className="absolute top-4 right-4 text-gray-400 hover:text-blue-600 opacity-0 group-hover:opacity-100 transition-opacity" title="Edit">
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" /></svg>
                </button>
                <Link href={`/stakeholders/${s.id}`} className="block">
                  <div className="flex items-start justify-between">
                    <div>
                      <p className="font-semibold text-gray-900">{s.name}</p>
                      {s.role && <p className="mt-1 text-base text-gray-500">{s.role}</p>}
                      {s.organisation && <p className="mt-0.5 text-sm text-gray-400">{s.organisation}</p>}
                    </div>
                    {s.risk_level && s.risk_level !== "none" && (
                      <span className={`inline-flex items-center rounded-full px-2 py-0.5 text-[10px] font-semibold ${
                        s.risk_level === "critical" ? "bg-red-100 text-red-800 border border-red-300" :
                        s.risk_level === "high" ? "bg-orange-100 text-orange-800 border border-orange-300" :
                        s.risk_level === "medium" ? "bg-yellow-100 text-yellow-800 border border-yellow-300" :
                        "bg-gray-100 text-gray-600 border border-gray-300"
                      }`}>
                        {s.risk_level.toUpperCase()} RISK
                      </span>
                    )}
                  </div>
                  {s.morale_notes && (
                    <p className="mt-2 text-sm text-amber-700 bg-amber-50 rounded px-2 py-1 border border-amber-200">
                      {s.morale_notes}
                    </p>
                  )}
                  <div className="mt-3 flex flex-wrap items-center gap-2">
                    <span className="inline-flex items-center rounded-full bg-blue-50 px-2 py-0.5 text-sm font-medium text-blue-700 border border-blue-200">Tier {s.tier}</span>
                    {s.mention_count > 0 && <span className="text-sm text-gray-500">Mentioned in {s.mention_count} transcript{s.mention_count !== 1 ? "s" : ""}</span>}
                  </div>
                </Link>
              </div>
            ))}
          </div>
        </section>
      ))}

      {stakeholders.length === 0 && (
        <div className="rounded-lg border border-gray-200 bg-white p-12 text-center shadow-sm"><p className="text-gray-500">No stakeholders found.</p></div>
      )}

      <EntityModal open={modalOpen} onClose={() => setModalOpen(false)} title={editingItem ? "Edit Stakeholder" : "New Stakeholder"}
        onSave={handleSave} onDelete={editingItem ? handleDelete : undefined} saving={saving} deleting={deleting} error={modalError}>
        <FormInput label="Name" value={formName} onChange={setFormName} placeholder="Full name" disabled={!!editingItem} />
        <FormSelect label="Tier" value={formTier} onChange={setFormTier} options={[{ value: "1", label: "Tier 1 - Key Decision Makers" }, { value: "2", label: "Tier 2 - Active Participants" }, { value: "3", label: "Tier 3 - Peripheral" }]} />
        <FormInput label="Role" value={formRole} onChange={setFormRole} placeholder="Role / title" />
        <FormTextarea label="Notes" value={formNotes} onChange={setFormNotes} placeholder="Additional notes..." rows={2} />
        {editingItem && (
          <>
            <FormSelect label="Flight Risk Level" value={formRiskLevel} onChange={setFormRiskLevel} options={[{ value: "none", label: "None" }, { value: "low", label: "Low" }, { value: "medium", label: "Medium" }, { value: "high", label: "High" }, { value: "critical", label: "Critical" }]} />
            <FormTextarea label="Morale / Burnout Notes" value={formMoraleNotes} onChange={setFormMoraleNotes} placeholder="e.g. showing fatigue, interviewing elsewhere, interpersonal tensions..." rows={2} />
          </>
        )}
      </EntityModal>
    </div>
  );
}
