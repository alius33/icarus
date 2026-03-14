"use client";

import { useEffect, useState } from "react";
import { api } from "@/lib/api";
import type { ScopeItemSchema, ScopeItemCreate } from "@/lib/types";
import { useEntityModal } from "./hooks/useEntityModal";
import EntityModal, { FormInput, FormSelect, FormTextarea } from "@/components/EntityModal";
import { Target, Plus, Edit2 } from "lucide-react";

export default function ScopeTracker() {
  const [items, setItems] = useState<ScopeItemSchema[]>([]);
  const [loading, setLoading] = useState(true);

  // Form state
  const [fName, setFName] = useState("");
  const [fType, setFType] = useState("original");
  const [fWorkstream, setFWorkstream] = useState("");
  const [fStatus, setFStatus] = useState("planned");
  const [fDescription, setFDescription] = useState("");

  const loadData = async () => {
    try {
      const data = await api.getScopeItems();
      setItems(data);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { loadData(); }, []);

  const modal = useEntityModal<ScopeItemCreate>({
    onSave: async (data) => {
      if (modal.editId) {
        await api.updateScopeItem(modal.editId, data);
      } else {
        await api.createScopeItem(data);
      }
    },
    onDelete: async (id) => { await api.deleteScopeItem(id); },
    onSuccess: loadData,
  });

  const handleEdit = (item: ScopeItemSchema) => {
    setFName(item.name);
    setFType(item.scope_type || "original");
    setFWorkstream(item.workstream || "");
    setFStatus(item.status || "planned");
    setFDescription(item.description || "");
    modal.openEdit(item.id);
  };

  const handleCreate = () => {
    setFName(""); setFType("original"); setFWorkstream(""); setFStatus("planned"); setFDescription("");
    modal.openCreate();
  };

  if (loading) {
    return <div className="p-4 text-base text-gray-500">Loading scope items...</div>;
  }

  const original = items.filter((i) => i.scope_type === "original");
  const additions = items.filter((i) => i.scope_type === "addition");
  const creepPct =
    original.length > 0
      ? Math.round((additions.length / original.length) * 100)
      : 0;

  return (
    <div>
      <div className="flex items-center justify-between mb-3">
        <h4 className="text-sm font-semibold text-gray-500 uppercase tracking-wider flex items-center gap-1.5">
          <Target className="h-3.5 w-3.5" />
          Scope ({items.length})
        </h4>
        <button
          onClick={handleCreate}
          className="flex items-center gap-1 text-sm text-blue-600 hover:text-blue-800"
        >
          <Plus className="h-3 w-3" /> Add
        </button>
      </div>

      {/* Scope creep indicator */}
      <div className="flex items-center gap-3 mb-3 rounded-md bg-gray-50 px-3 py-2">
        <div className="flex-1">
          <div className="flex items-center justify-between text-sm mb-1">
            <span className="text-gray-600">
              Original: <span className="font-semibold">{original.length}</span>
            </span>
            <span className="text-gray-600">
              Additions: <span className="font-semibold">{additions.length}</span>
            </span>
          </div>
          <div className="relative h-2 w-full rounded-full bg-gray-200">
            <div
              className="absolute inset-y-0 left-0 rounded-full bg-blue-500"
              style={{
                width: `${
                  items.length > 0
                    ? Math.round((original.length / items.length) * 100)
                    : 100
                }%`,
              }}
            />
          </div>
        </div>
        <span
          className={`text-base font-bold ${
            creepPct > 30 ? "text-red-600" : creepPct > 15 ? "text-amber-600" : "text-green-600"
          }`}
        >
          {creepPct}% creep
        </span>
      </div>

      {items.length === 0 ? (
        <p className="text-base text-gray-500">No scope items tracked.</p>
      ) : (
        <div className="space-y-1.5 max-h-64 overflow-y-auto">
          {items.map((item) => (
            <button
              key={item.id}
              onClick={() => handleEdit(item)}
              className="flex items-start gap-2 w-full text-left rounded-md border border-gray-100 bg-white px-3 py-2 hover:bg-gray-50 transition-colors"
            >
              <span
                className={`mt-0.5 inline-flex rounded-full px-1.5 py-0.5 text-[10px] font-medium ${
                  item.scope_type === "original"
                    ? "bg-blue-100 text-blue-700"
                    : "bg-amber-100 text-amber-700"
                }`}
              >
                {item.scope_type}
              </span>
              <div className="flex-1 min-w-0">
                <p className="text-base font-medium text-gray-900 truncate">
                  {item.name}
                </p>
                {item.workstream && (
                  <span className="text-[10px] text-gray-500">
                    {item.workstream}
                  </span>
                )}
              </div>
              <span
                className={`text-[10px] font-medium ${
                  item.status === "completed"
                    ? "text-green-600"
                    : item.status === "in-progress"
                      ? "text-blue-600"
                      : "text-gray-500"
                }`}
              >
                {item.status}
              </span>
              <Edit2 className="h-3 w-3 text-gray-400 flex-shrink-0 mt-1" />
            </button>
          ))}
        </div>
      )}

      {/* Scope Modal */}
      <EntityModal
        open={modal.open}
        onClose={modal.close}
        title={modal.editId ? "Edit Scope Item" : "New Scope Item"}
        onSave={() => modal.save({ name: fName, scope_type: fType, workstream: fWorkstream || undefined, status: fStatus, description: fDescription || undefined })}
        onDelete={modal.editId ? modal.handleDelete : undefined}
        saving={modal.saving}
        deleting={modal.deleting}
        error={modal.error}
      >
        <FormInput label="Name" value={fName} onChange={setFName} placeholder="Scope item name" />
        <FormSelect label="Type" value={fType} onChange={setFType} options={[
          { value: "original", label: "Original" },
          { value: "addition", label: "Addition" },
        ]} />
        <FormInput label="Workstream" value={fWorkstream} onChange={setFWorkstream} placeholder="Which workstream?" />
        <FormSelect label="Status" value={fStatus} onChange={setFStatus} options={[
          { value: "planned", label: "Planned" },
          { value: "in-progress", label: "In Progress" },
          { value: "completed", label: "Completed" },
          { value: "deferred", label: "Deferred" },
        ]} />
        <FormTextarea label="Description" value={fDescription} onChange={setFDescription} placeholder="Description" rows={2} />
      </EntityModal>
    </div>
  );
}
