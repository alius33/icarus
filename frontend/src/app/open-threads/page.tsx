"use client";

import { useEffect, useState, useCallback } from "react";
import { api } from "@/lib/api";
import { formatDate, getStatusColor } from "@/lib/utils";
import type { OpenThreadSchema } from "@/lib/types";
import EntityModal, { FormInput, FormTextarea, FormSelect } from "@/components/EntityModal";

const STATUS_SECTIONS = ["OPEN", "WATCHING", "CLOSED"] as const;

export default function OpenThreadsPage() {
  const [threads, setThreads] = useState<OpenThreadSchema[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const [modalOpen, setModalOpen] = useState(false);
  const [editingItem, setEditingItem] = useState<OpenThreadSchema | null>(null);
  const [formTitle, setFormTitle] = useState("");
  const [formContext, setFormContext] = useState("");
  const [formQuestion, setFormQuestion] = useState("");
  const [formStatus, setFormStatus] = useState("OPEN");
  const [saving, setSaving] = useState(false);
  const [deleting, setDeleting] = useState(false);
  const [modalError, setModalError] = useState<string | null>(null);

  const reload = useCallback(() => { api.getOpenThreads().then(setThreads).catch(() => {}); }, []);

  useEffect(() => {
    api.getOpenThreads().then(setThreads)
      .catch((e) => setError(e instanceof Error ? e.message : "Failed to load open threads"))
      .finally(() => setLoading(false));
  }, []);

  const openCreate = () => {
    setEditingItem(null); setFormTitle(""); setFormContext(""); setFormQuestion(""); setFormStatus("OPEN");
    setModalError(null); setModalOpen(true);
  };
  const openEdit = (t: OpenThreadSchema) => {
    setEditingItem(t); setFormTitle(t.title); setFormContext(t.description || "");
    setFormQuestion(""); setFormStatus(t.status);
    setModalError(null); setModalOpen(true);
  };
  const handleSave = async () => {
    setSaving(true); setModalError(null);
    try {
      if (editingItem) {
        await api.updateOpenThread(editingItem.id, { title: formTitle, context: formContext || undefined, status: formStatus });
      } else {
        await api.createOpenThread({ title: formTitle, context: formContext || undefined, question: formQuestion || undefined, status: formStatus });
      }
      setModalOpen(false); reload();
    } catch (e) { setModalError(e instanceof Error ? e.message : "Save failed"); }
    finally { setSaving(false); }
  };
  const handleDelete = async () => {
    if (!editingItem) return; setDeleting(true);
    try { await api.deleteOpenThread(editingItem.id); setModalOpen(false); reload(); }
    catch (e) { setModalError(e instanceof Error ? e.message : "Delete failed"); }
    finally { setDeleting(false); }
  };

  if (loading) return (<div className="space-y-6"><h2 className="text-2xl font-bold text-gray-900">Open Threads</h2><p className="text-sm text-gray-500">Loading threads...</p></div>);
  if (error) return (<div className="space-y-6"><h2 className="text-2xl font-bold text-gray-900">Open Threads</h2><div className="rounded-lg border border-red-200 bg-red-50 p-6"><p className="text-sm text-red-700">{error}</p></div></div>);

  const grouped: Record<string, OpenThreadSchema[]> = {};
  for (const status of STATUS_SECTIONS) grouped[status] = [];
  for (const thread of threads) {
    const key = STATUS_SECTIONS.includes(thread.status as (typeof STATUS_SECTIONS)[number]) ? thread.status : "OPEN";
    grouped[key].push(thread);
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h2 className="text-2xl font-bold text-gray-900">Open Threads</h2>
        <button onClick={openCreate} className="px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-md hover:bg-blue-700 transition-colors">+ New Thread</button>
      </div>

      {threads.length === 0 ? (
        <div className="text-center py-12"><p className="text-sm text-gray-500">No open threads recorded yet.</p></div>
      ) : STATUS_SECTIONS.map((status, sectionIdx) => {
        const sectionThreads = grouped[status];
        if (sectionThreads.length === 0) return null;
        return (
          <div key={status} className={sectionIdx > 0 ? "border-t border-gray-200 mt-8 pt-8" : ""}>
            <div className="flex items-center gap-2 mb-4">
              <h3 className="text-lg font-semibold text-gray-900">{status.charAt(0) + status.slice(1).toLowerCase()}</h3>
              <span className="text-sm text-gray-500">({sectionThreads.length})</span>
            </div>
            <div className="grid grid-cols-1 gap-4 lg:grid-cols-2">
              {sectionThreads.map((thread) => (
                <div key={thread.id} className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 relative group cursor-pointer hover:border-gray-300 hover:shadow-md transition-all" onClick={() => openEdit(thread)}>
                  <button onClick={(e) => { e.stopPropagation(); openEdit(thread); }} className="absolute top-4 right-4 text-gray-400 hover:text-blue-600 opacity-0 group-hover:opacity-100 transition-opacity" title="Edit">
                    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" /></svg>
                  </button>
                  <div className="flex items-start justify-between gap-3 pr-8">
                    <h4 className="text-sm font-bold text-gray-900">{thread.title}</h4>
                    <span className={`px-2 py-1 rounded-full text-xs font-medium border flex-shrink-0 ${getStatusColor(thread.status)}`}>{thread.status}</span>
                  </div>
                  {thread.opened_date && <p className="text-xs text-gray-400 mt-1">First raised: {formatDate(thread.opened_date)}</p>}
                  {thread.priority && <p className="text-xs italic text-gray-500 mt-2">{thread.priority}</p>}
                  {thread.description && <p className="text-sm text-gray-700 mt-3">{thread.description}</p>}
                </div>
              ))}
            </div>
          </div>
        );
      })}

      <EntityModal open={modalOpen} onClose={() => setModalOpen(false)} title={editingItem ? "Edit Thread" : "New Thread"}
        onSave={handleSave} onDelete={editingItem ? handleDelete : undefined} saving={saving} deleting={deleting} error={modalError}>
        <FormInput label="Title" value={formTitle} onChange={setFormTitle} placeholder="Thread title" />
        <FormTextarea label="Context" value={formContext} onChange={setFormContext} placeholder="What is this about?" />
        {!editingItem && <FormTextarea label="Question" value={formQuestion} onChange={setFormQuestion} placeholder="What needs to be resolved?" rows={2} />}
        <FormSelect label="Status" value={formStatus} onChange={setFormStatus} options={[{ value: "OPEN", label: "Open" }, { value: "WATCHING", label: "Watching" }, { value: "CLOSED", label: "Closed" }]} />
      </EntityModal>
    </div>
  );
}
