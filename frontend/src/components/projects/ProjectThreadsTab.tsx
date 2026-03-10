"use client";

import { useState } from "react";
import { api } from "@/lib/api";
import { formatDate, getStatusColor } from "@/lib/utils";
import type { OpenThreadSchema } from "@/lib/types";
import EntityModal, { FormInput, FormTextarea, FormSelect } from "@/components/EntityModal";

export default function ProjectThreadsTab({
  threads: initialThreads,
}: {
  threads: OpenThreadSchema[];
}) {
  const [threads, setThreads] = useState(initialThreads);
  const [modalOpen, setModalOpen] = useState(false);
  const [editingItem, setEditingItem] = useState<OpenThreadSchema | null>(null);
  const [formTitle, setFormTitle] = useState("");
  const [formContext, setFormContext] = useState("");
  const [formQuestion, setFormQuestion] = useState("");
  const [formStatus, setFormStatus] = useState("OPEN");
  const [saving, setSaving] = useState(false);
  const [deleting, setDeleting] = useState(false);
  const [modalError, setModalError] = useState<string | null>(null);

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
        const updated = await api.updateOpenThread(editingItem.id, { title: formTitle, context: formContext || undefined, status: formStatus });
        setThreads((prev) => prev.map((t) => t.id === updated.id ? updated : t));
      } else {
        const created = await api.createOpenThread({ title: formTitle, context: formContext || undefined, question: formQuestion || undefined, status: formStatus });
        setThreads((prev) => [...prev, created]);
      }
      setModalOpen(false);
    } catch (e) { setModalError(e instanceof Error ? e.message : "Save failed"); }
    finally { setSaving(false); }
  };
  const handleDelete = async () => {
    if (!editingItem) return; setDeleting(true);
    try { await api.deleteOpenThread(editingItem.id); setThreads((prev) => prev.filter((t) => t.id !== editingItem.id)); setModalOpen(false); }
    catch (e) { setModalError(e instanceof Error ? e.message : "Delete failed"); }
    finally { setDeleting(false); }
  };

  return (
    <div className="space-y-4">
      <div className="flex justify-end">
        <button onClick={openCreate} className="px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-md hover:bg-blue-700 transition-colors">+ New Thread</button>
      </div>

      {threads.length === 0 ? (
        <div className="rounded-lg border border-gray-200 bg-white p-8 text-center">
          <p className="text-sm text-gray-500">No open threads linked to this project yet.</p>
        </div>
      ) : (
        <div className="space-y-3">
          {threads.map((t) => (
            <div key={t.id} className="rounded-lg border border-gray-200 bg-white p-4 relative group">
              <button onClick={() => openEdit(t)}
                className="absolute top-4 right-4 text-gray-400 hover:text-blue-600 opacity-0 group-hover:opacity-100 transition-opacity" title="Edit">
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" /></svg>
              </button>
              <div className="flex items-start justify-between gap-3 pr-8">
                <div className="min-w-0">
                  <h4 className="text-sm font-medium text-gray-900">{t.title}</h4>
                  {t.description && (
                    <p className="mt-1 text-xs text-gray-500 line-clamp-2">{t.description}</p>
                  )}
                  <div className="mt-2 flex items-center gap-3 text-xs text-gray-400">
                    {t.owner && <span>Owner: {t.owner}</span>}
                    {t.opened_date && <span>Raised: {formatDate(t.opened_date)}</span>}
                  </div>
                </div>
                <span className={`inline-flex flex-shrink-0 rounded-full border px-2.5 py-0.5 text-xs font-medium ${getStatusColor(t.status)}`}>
                  {t.status}
                </span>
              </div>
            </div>
          ))}
        </div>
      )}

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
