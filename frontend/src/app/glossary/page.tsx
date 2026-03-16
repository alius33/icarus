"use client";

import { useEffect, useState, useMemo, useCallback } from "react";
import { api } from "@/lib/api";
import type { GlossaryGrouped, GlossaryEntrySchema } from "@/lib/types";
import EntityModal, { FormInput, FormTextarea } from "@/components/EntityModal";

export default function GlossaryPage() {
  const [glossary, setGlossary] = useState<GlossaryGrouped | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState("");
  const [modalOpen, setModalOpen] = useState(false);
  const [editingItem, setEditingItem] = useState<GlossaryEntrySchema | null>(null);
  const [formTerm, setFormTerm] = useState("");
  const [formDefinition, setFormDefinition] = useState("");
  const [formCategory, setFormCategory] = useState("");
  const [saving, setSaving] = useState(false);
  const [deleting, setDeleting] = useState(false);
  const [modalError, setModalError] = useState<string | null>(null);

  const reload = useCallback(() => { api.getGlossary().then(setGlossary).catch(() => {}); }, []);

  useEffect(() => {
    api.getGlossary().then(setGlossary)
      .catch((e) => setError(e instanceof Error ? e.message : "Failed to load glossary"))
      .finally(() => setLoading(false));
  }, []);

  const filteredGlossary = useMemo(() => {
    if (!glossary) return null;
    const search = filter.trim().toLowerCase();
    if (!search) return glossary;
    const result: GlossaryGrouped = {};
    for (const [category, entries] of Object.entries(glossary)) {
      const filtered = entries.filter((e: GlossaryEntrySchema) =>
        e.term.toLowerCase().includes(search) || e.definition.toLowerCase().includes(search) || e.aliases.some((a: string) => a.toLowerCase().includes(search)));
      if (filtered.length > 0) result[category] = filtered;
    }
    return result;
  }, [glossary, filter]);

  const totalEntries = useMemo(() => {
    if (!filteredGlossary) return 0;
    return Object.values(filteredGlossary).reduce((sum, entries) => sum + entries.length, 0);
  }, [filteredGlossary]);

  const openCreate = () => {
    setEditingItem(null); setFormTerm(""); setFormDefinition(""); setFormCategory("");
    setModalError(null); setModalOpen(true);
  };
  const openEdit = (entry: GlossaryEntrySchema) => {
    setEditingItem(entry); setFormTerm(entry.term); setFormDefinition(entry.definition); setFormCategory(entry.category);
    setModalError(null); setModalOpen(true);
  };
  const handleSave = async () => {
    setSaving(true); setModalError(null);
    try {
      if (editingItem) {
        await api.updateGlossaryEntry(editingItem.id, { definition: formDefinition, category: formCategory || undefined });
      } else {
        await api.createGlossaryEntry({ term: formTerm, definition: formDefinition, category: formCategory || "Uncategorized" });
      }
      setModalOpen(false); reload();
    } catch (e) { setModalError(e instanceof Error ? e.message : "Save failed"); }
    finally { setSaving(false); }
  };
  const handleDelete = async () => {
    if (!editingItem) return; setDeleting(true);
    try { await api.deleteGlossaryEntry(editingItem.id); setModalOpen(false); reload(); }
    catch (e) { setModalError(e instanceof Error ? e.message : "Delete failed"); }
    finally { setDeleting(false); }
  };

  if (loading) return (<div className="space-y-6"><h2 className="text-2xl font-bold text-forest-950">Glossary</h2><p className="text-base text-forest-400">Loading glossary...</p></div>);
  if (error) return (<div className="space-y-6"><h2 className="text-2xl font-bold text-forest-950">Glossary</h2><div className="rounded-lg border border-red-200 bg-red-50 p-6"><p className="text-base text-red-700">{error}</p></div></div>);
  if (!glossary || Object.keys(glossary).length === 0) return (
    <div className="space-y-6">
      <div className="flex flex-wrap items-center justify-between gap-3">
        <h2 className="text-xl md:text-2xl font-bold text-forest-950">Glossary</h2>
        <button onClick={openCreate} className="px-4 py-2 text-base font-medium text-white bg-forest-500 rounded-md hover:bg-forest-600 transition-colors">+ New Term</button>
      </div>
      <div className="text-center py-12"><p className="text-base text-forest-400">No glossary entries yet.</p></div>
    </div>
  );

  const categories = Object.keys(filteredGlossary || {});

  return (
    <div className="space-y-6">
      <div className="flex flex-wrap items-center justify-between gap-3">
        <h2 className="text-xl md:text-2xl font-bold text-forest-950">Glossary</h2>
        <button onClick={openCreate} className="px-4 py-2 text-base font-medium text-white bg-forest-500 rounded-md hover:bg-forest-600 transition-colors">+ New Term</button>
      </div>

      <div className="flex gap-4 items-center">
        <input type="text" placeholder="Filter terms..." value={filter} onChange={(e) => setFilter(e.target.value)}
          className="border rounded px-3 py-2 text-base text-forest-600 bg-white dark:bg-forest-800 w-full max-w-xs md:w-72 focus:outline-none focus:ring-1 focus:ring-forest-500 focus:border-forest-500" />
        <span className="text-base text-forest-400">{totalEntries} term{totalEntries !== 1 ? "s" : ""}{filter.trim() ? " matching" : ""}</span>
      </div>

      {categories.length === 0 ? (
        <div className="text-center py-12"><p className="text-base text-forest-400">No terms match &ldquo;{filter.trim()}&rdquo;</p></div>
      ) : categories.map((category, idx) => (
        <div key={category} className={idx > 0 ? "border-t border-forest-200 mt-8 pt-8" : ""}>
          <h3 className="text-lg font-semibold text-forest-950 mb-4">{category}</h3>
          <div className="bg-white dark:bg-forest-800 rounded-lg shadow-sm border border-forest-200 divide-y divide-gray-100">
            {(filteredGlossary?.[category] || []).map((entry: GlossaryEntrySchema) => (
              <div key={entry.id} className="px-6 py-4 group relative">
                <button onClick={() => openEdit(entry)}
                  className="absolute top-4 right-4 text-forest-300 hover:text-forest-500 opacity-0 group-hover:opacity-100 transition-opacity" title="Edit">
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" /></svg>
                </button>
                <div className="flex items-start gap-2">
                  <span className="text-base font-bold text-forest-950">{entry.term}</span>
                  {entry.aliases.length > 0 && <span className="text-sm text-forest-300 mt-0.5">({entry.aliases.join(", ")})</span>}
                </div>
                <p className="text-base text-forest-600 mt-1">{entry.definition}</p>
              </div>
            ))}
          </div>
        </div>
      ))}

      <EntityModal open={modalOpen} onClose={() => setModalOpen(false)} title={editingItem ? "Edit Term" : "New Term"}
        onSave={handleSave} onDelete={editingItem ? handleDelete : undefined} saving={saving} deleting={deleting} error={modalError}>
        <FormInput label="Term" value={formTerm} onChange={setFormTerm} placeholder="Term or acronym" disabled={!!editingItem} />
        <FormTextarea label="Definition" value={formDefinition} onChange={setFormDefinition} placeholder="What does it mean?" />
        <FormInput label="Category" value={formCategory} onChange={setFormCategory} placeholder="e.g. Systems, People, Processes" />
      </EntityModal>
    </div>
  );
}
