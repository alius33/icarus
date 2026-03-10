"use client";

import { useEffect, useState, useMemo, useCallback } from "react";
import { api } from "@/lib/api";
import { formatDate, getStatusColor } from "@/lib/utils";
import type { ActionItemSchema } from "@/lib/types";
import EntityModal, { FormInput, FormTextarea, FormSelect } from "@/components/EntityModal";

const STATUS_ORDER: Record<string, number> = { OPEN: 0, LIKELY_COMPLETED: 1, COMPLETED: 2 };

export default function ActionItemsPage() {
  const [items, setItems] = useState<ActionItemSchema[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const [statusFilter, setStatusFilter] = useState<string>("ALL");
  const [ownerFilter, setOwnerFilter] = useState<string>("ALL");
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

  const reload = useCallback(() => { api.getActionItems().then(setItems).catch(() => {}); }, []);

  useEffect(() => {
    api.getActionItems()
      .then(setItems)
      .catch((e) => setError(e instanceof Error ? e.message : "Failed to load action items"))
      .finally(() => setLoading(false));
  }, []);

  const uniqueOwners = useMemo(() => {
    const owners = new Set<string>();
    items.forEach((item) => { if (item.owner) owners.add(item.owner); });
    return Array.from(owners).sort();
  }, [items]);

  const filteredAndSorted = useMemo(() => {
    let filtered = items;
    if (statusFilter !== "ALL") filtered = filtered.filter((i) => i.status === statusFilter);
    if (ownerFilter !== "ALL") filtered = filtered.filter((i) => i.owner === ownerFilter);
    return [...filtered].sort((a, b) => (STATUS_ORDER[a.status] ?? 99) - (STATUS_ORDER[b.status] ?? 99));
  }, [items, statusFilter, ownerFilter]);

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
        await api.updateActionItem(editingItem.id, { description: formDesc, owner: formOwner || undefined, deadline: formDeadline || undefined, status: formStatus });
      } else {
        await api.createActionItem({ description: formDesc, owner: formOwner || undefined, deadline: formDeadline || undefined, context: formContext || undefined, status: formStatus });
      }
      setModalOpen(false); reload();
    } catch (e) { setModalError(e instanceof Error ? e.message : "Save failed"); }
    finally { setSaving(false); }
  };
  const handleDelete = async () => {
    if (!editingItem) return; setDeleting(true);
    try { await api.deleteActionItem(editingItem.id); setModalOpen(false); reload(); }
    catch (e) { setModalError(e instanceof Error ? e.message : "Delete failed"); }
    finally { setDeleting(false); }
  };
  const handleComplete = async (id: number) => {
    try { await api.completeActionItem(id); reload(); } catch { /* ignore */ }
  };

  if (loading) return (<div className="space-y-6"><h2 className="text-2xl font-bold text-gray-900">Action Items</h2><p className="text-sm text-gray-500">Loading action items...</p></div>);
  if (error) return (<div className="space-y-6"><h2 className="text-2xl font-bold text-gray-900">Action Items</h2><div className="rounded-lg border border-red-200 bg-red-50 p-6"><p className="text-sm text-red-700">{error}</p></div></div>);

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h2 className="text-2xl font-bold text-gray-900">Action Items</h2>
        <button onClick={openCreate} className="px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-md hover:bg-blue-700 transition-colors">+ New Action</button>
      </div>

      <div className="flex gap-4 mb-6">
        <select value={statusFilter} onChange={(e) => setStatusFilter(e.target.value)} className="border rounded px-3 py-2 text-sm text-gray-700 bg-white focus:outline-none focus:ring-1 focus:ring-blue-500 focus:border-blue-500">
          <option value="ALL">All Statuses</option><option value="OPEN">Open</option><option value="LIKELY_COMPLETED">Likely Completed</option><option value="COMPLETED">Completed</option>
        </select>
        <select value={ownerFilter} onChange={(e) => setOwnerFilter(e.target.value)} className="border rounded px-3 py-2 text-sm text-gray-700 bg-white focus:outline-none focus:ring-1 focus:ring-blue-500 focus:border-blue-500">
          <option value="ALL">All Owners</option>
          {uniqueOwners.map((o) => <option key={o} value={o}>{o}</option>)}
        </select>
        {(statusFilter !== "ALL" || ownerFilter !== "ALL") && <span className="self-center text-sm text-gray-500">Showing {filteredAndSorted.length} of {items.length}</span>}
      </div>

      {filteredAndSorted.length === 0 ? (
        <div className="text-center py-12"><p className="text-sm text-gray-500">{items.length === 0 ? "No action items recorded yet." : "No action items match the current filters."}</p></div>
      ) : (
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden">
          <table className="w-full">
            <thead><tr className="border-b border-gray-200 bg-gray-50">
              <th className="px-3 py-3 w-10"></th>
              <th className="px-4 py-3 text-left text-xs font-medium uppercase tracking-wider text-gray-500 w-12">#</th>
              <th className="px-4 py-3 text-left text-xs font-medium uppercase tracking-wider text-gray-500">Action</th>
              <th className="px-4 py-3 text-left text-xs font-medium uppercase tracking-wider text-gray-500 w-36">Owner</th>
              <th className="px-4 py-3 text-left text-xs font-medium uppercase tracking-wider text-gray-500 w-28">Deadline</th>
              <th className="px-4 py-3 text-left text-xs font-medium uppercase tracking-wider text-gray-500 w-36">Status</th>
              <th className="px-3 py-3 w-10"></th>
            </tr></thead>
            <tbody className="divide-y divide-gray-200">
              {filteredAndSorted.map((item) => (
                <tr key={item.id} className="hover:bg-gray-50 transition-colors cursor-pointer" onClick={() => openEdit(item)}>
                  <td className="px-3 py-4 text-center">
                    {item.status !== "COMPLETED" && (
                      <button onClick={(e) => { e.stopPropagation(); handleComplete(item.id); }} title="Mark complete" className="text-gray-400 hover:text-green-600">
                        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" /></svg>
                      </button>
                    )}
                  </td>
                  <td className="px-4 py-4 text-sm text-gray-400 tabular-nums">{item.id}</td>
                  <td className="px-4 py-4"><p className="text-sm text-gray-900">{item.title}</p>{item.description && <p className="text-xs text-gray-500 mt-1">{item.description}</p>}</td>
                  <td className="px-4 py-4 text-sm text-gray-600">{item.owner || "\u2014"}</td>
                  <td className="px-4 py-4 text-sm text-gray-500 whitespace-nowrap">{item.due_date ? formatDate(item.due_date) : "\u2014"}</td>
                  <td className="px-4 py-4"><span className={`px-2 py-1 rounded-full text-xs font-medium border ${getStatusColor(item.status)}`}>{item.status.replace(/_/g, " ")}</span></td>
                  <td className="px-3 py-4 text-center">
                    <button onClick={(e) => { e.stopPropagation(); openEdit(item); }} className="text-gray-400 hover:text-blue-600" title="Edit">
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
