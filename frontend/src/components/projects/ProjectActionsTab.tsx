"use client";

import { useState } from "react";
import { api } from "@/lib/api";
import { formatDate, getStatusColor } from "@/lib/utils";
import type { ActionItemSchema } from "@/lib/types";
import EntityModal, { FormInput, FormTextarea, FormSelect } from "@/components/EntityModal";

export default function ProjectActionsTab({
  actions: initialActions,
}: {
  actions: ActionItemSchema[];
}) {
  const [actions, setActions] = useState(initialActions);
  const [modalOpen, setModalOpen] = useState(false);
  const [editingItem, setEditingItem] = useState<ActionItemSchema | null>(null);
  const [formDesc, setFormDesc] = useState("");
  const [formOwner, setFormOwner] = useState("");
  const [formDeadline, setFormDeadline] = useState("");
  const [formContext, setFormContext] = useState("");
  const [formStatus, setFormStatus] = useState("OPEN");
  const [saving, setSaving] = useState(false);
  const [deleting, setDeleting] = useState(false);
  const [modalError, setModalError] = useState<string | null>(null);


  const openCreate = () => {
    setEditingItem(null); setFormDesc(""); setFormOwner(""); setFormDeadline(""); setFormContext(""); setFormStatus("OPEN");
    setModalError(null); setModalOpen(true);
  };
  const openEdit = (item: ActionItemSchema) => {
    setEditingItem(item); setFormDesc(item.description || ""); setFormOwner(item.owner || "");
    setFormDeadline(item.due_date || ""); setFormContext(""); setFormStatus(item.status);
    setModalError(null); setModalOpen(true);
  };
  const handleSave = async () => {
    setSaving(true); setModalError(null);
    try {
      if (editingItem) {
        const updated = await api.updateActionItem(editingItem.id, { description: formDesc, owner: formOwner || undefined, deadline: formDeadline || undefined, status: formStatus });
        setActions((prev) => prev.map((a) => a.id === updated.id ? updated : a));
      } else {
        const created = await api.createActionItem({ description: formDesc, owner: formOwner || undefined, deadline: formDeadline || undefined, context: formContext || undefined, status: formStatus });
        setActions((prev) => [...prev, created]);
      }
      setModalOpen(false);
    } catch (e) { setModalError(e instanceof Error ? e.message : "Save failed"); }
    finally { setSaving(false); }
  };
  const handleDelete = async () => {
    if (!editingItem) return; setDeleting(true);
    try { await api.deleteActionItem(editingItem.id); setActions((prev) => prev.filter((a) => a.id !== editingItem.id)); setModalOpen(false); }
    catch (e) { setModalError(e instanceof Error ? e.message : "Delete failed"); }
    finally { setDeleting(false); }
  };
  const handleComplete = async (id: number) => {
    try {
      const updated = await api.completeActionItem(id);
      setActions((prev) => prev.map((a) => a.id === id ? updated : a));
    } catch { /* ignore */ }
  };

  return (
    <div className="space-y-4">
      <div className="flex justify-end">
        <button onClick={openCreate} className="px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-md hover:bg-blue-700 transition-colors">+ New Action</button>
      </div>

      {actions.length === 0 ? (
        <div className="rounded-lg border border-gray-200 bg-white p-8 text-center">
          <p className="text-sm text-gray-500">No action items linked to this project yet.</p>
        </div>
      ) : (
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden">
          <table className="w-full">
            <thead>
              <tr className="border-b border-gray-200 bg-gray-50">
                <th className="px-3 py-3 w-10"></th>
                <th className="px-4 py-3 text-left text-xs font-medium uppercase tracking-wider text-gray-500 w-12">#</th>
                <th className="px-4 py-3 text-left text-xs font-medium uppercase tracking-wider text-gray-500">Action</th>
                <th className="px-4 py-3 text-left text-xs font-medium uppercase tracking-wider text-gray-500 w-36">Owner</th>
                <th className="px-4 py-3 text-left text-xs font-medium uppercase tracking-wider text-gray-500 w-28">Deadline</th>
                <th className="px-4 py-3 text-left text-xs font-medium uppercase tracking-wider text-gray-500 w-36">Status</th>
                <th className="px-3 py-3 w-10"></th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-200">
              {actions.map((a) => (
                <tr key={a.id} className="hover:bg-gray-50 transition-colors cursor-pointer" onClick={() => openEdit(a)}>
                  <td className="px-3 py-4 text-center">
                    {a.status !== "COMPLETED" && (
                      <button onClick={(e) => { e.stopPropagation(); handleComplete(a.id); }} title="Mark complete" className="text-gray-400 hover:text-green-600">
                        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" /></svg>
                      </button>
                    )}
                  </td>
                  <td className="px-4 py-4 text-sm text-gray-400 tabular-nums">{a.id}</td>
                  <td className="px-4 py-4">
                    <p className="text-sm text-gray-900">{a.title}</p>
                    {a.description && <p className="mt-1 text-xs text-gray-500">{a.description}</p>}
                  </td>
                  <td className="px-4 py-4 text-sm text-gray-600">{a.owner || "\u2014"}</td>
                  <td className="px-4 py-4 text-sm text-gray-500 whitespace-nowrap">{a.due_date ? formatDate(a.due_date) : "\u2014"}</td>
                  <td className="px-4 py-4">
                    <span className={`px-2 py-1 rounded-full text-xs font-medium border ${getStatusColor(a.status)}`}>{a.status.replace(/_/g, " ")}</span>
                  </td>
                  <td className="px-3 py-4 text-center">
                    <button onClick={(e) => { e.stopPropagation(); openEdit(a); }} className="text-gray-400 hover:text-blue-600" title="Edit">
                      <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" /></svg>
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      <EntityModal open={modalOpen} onClose={() => setModalOpen(false)} title={editingItem ? "Edit Action Item" : "New Action Item"}
        onSave={handleSave} onDelete={editingItem ? handleDelete : undefined} saving={saving} deleting={deleting} error={modalError}>
        <FormTextarea label="Description" value={formDesc} onChange={setFormDesc} placeholder="What needs to be done?" />
        <FormInput label="Owner" value={formOwner} onChange={setFormOwner} placeholder="Who is responsible?" />
        <FormInput label="Deadline" value={formDeadline} onChange={setFormDeadline} placeholder="e.g. 2026-03-15" />
        {!editingItem && <FormTextarea label="Context" value={formContext} onChange={setFormContext} placeholder="Additional context..." rows={2} />}
        <FormSelect label="Status" value={formStatus} onChange={setFormStatus} options={[{ value: "OPEN", label: "Open" }, { value: "COMPLETED", label: "Completed" }, { value: "LIKELY_COMPLETED", label: "Likely Completed" }]} />
      </EntityModal>
    </div>
  );
}
