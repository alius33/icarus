"use client";

import { useEffect, useState } from "react";
import { api } from "@/lib/api";
import { capacityColor } from "@/lib/utils";
import type { ResourceAllocationSchema, ResourceAllocationCreate } from "@/lib/types";
import { useEntityModal } from "./hooks/useEntityModal";
import EntityModal, { FormInput, FormSelect, FormTextarea } from "@/components/EntityModal";
import { UserCog, Plus, Edit2 } from "lucide-react";

export default function ResourceCapacity() {
  const [resources, setResources] = useState<ResourceAllocationSchema[]>([]);
  const [loading, setLoading] = useState(true);

  // Form state
  const [fName, setFName] = useState("");
  const [fRole, setFRole] = useState("");
  const [fCapacity, setFCapacity] = useState("available");
  const [fNotes, setFNotes] = useState("");

  const loadData = async () => {
    try {
      const data = await api.getResources();
      setResources(data);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { loadData(); }, []);

  const modal = useEntityModal<ResourceAllocationCreate>({
    onSave: async (data) => {
      if (modal.editId) {
        await api.updateResource(modal.editId, data);
      } else {
        await api.createResource(data);
      }
    },
    onDelete: async (id) => { await api.deleteResource(id); },
    onSuccess: loadData,
  });

  const handleEdit = (r: ResourceAllocationSchema) => {
    setFName(r.person_name);
    setFRole(r.role || "");
    setFCapacity(r.capacity_status || "available");
    setFNotes(r.notes || "");
    modal.openEdit(r.id);
  };

  const handleCreate = () => {
    setFName(""); setFRole(""); setFCapacity("available"); setFNotes("");
    modal.openCreate();
  };

  if (loading) {
    return <div className="p-4 text-base text-forest-400">Loading resources...</div>;
  }

  return (
    <div>
      <div className="flex items-center justify-between mb-3">
        <h4 className="text-sm font-semibold text-forest-400 uppercase tracking-wider flex items-center gap-1.5">
          <UserCog className="h-3.5 w-3.5" />
          Resource Capacity ({resources.length})
        </h4>
        <button
          onClick={handleCreate}
          className="flex items-center gap-1 text-sm text-forest-500 hover:text-blue-800"
        >
          <Plus className="h-3 w-3" /> Add
        </button>
      </div>

      {resources.length === 0 ? (
        <p className="text-base text-forest-400">No resource allocations tracked.</p>
      ) : (
        <div className="space-y-2">
          {resources.map((r) => {
            const totalPct = (r.allocations || []).reduce(
              (sum, a) => sum + (a.percentage || 0),
              0,
            );
            return (
              <button
                key={r.id}
                onClick={() => handleEdit(r)}
                className="flex items-start gap-3 w-full text-left rounded-md border border-gray-100 bg-white dark:bg-forest-800 px-3 py-2.5 hover:bg-forest-50 transition-colors"
              >
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-2">
                    <span className="text-base font-medium text-forest-950">
                      {r.person_name}
                    </span>
                    <span
                      className={`text-[10px] font-semibold uppercase ${capacityColor(r.capacity_status)}`}
                    >
                      {r.capacity_status}
                    </span>
                  </div>
                  {r.role && (
                    <p className="text-[10px] text-forest-400">{r.role}</p>
                  )}

                  {/* Allocation bar */}
                  <div className="mt-1.5 w-full">
                    <div className="flex items-center gap-2">
                      <div className="relative h-2 flex-1 rounded-full bg-forest-100">
                        <div
                          className={`absolute inset-y-0 left-0 rounded-full ${
                            totalPct > 100
                              ? "bg-red-500"
                              : totalPct > 80
                                ? "bg-amber-500"
                                : "bg-forest-500"
                          }`}
                          style={{ width: `${Math.min(totalPct, 100)}%` }}
                        />
                      </div>
                      <span className="text-[10px] font-medium text-forest-400 tabular-nums w-8 text-right">
                        {totalPct}%
                      </span>
                    </div>
                    {(r.allocations || []).length > 0 && (
                      <div className="flex flex-wrap gap-1 mt-1">
                        {r.allocations.map((a, i) => (
                          <span
                            key={i}
                            className="text-[10px] text-forest-300"
                          >
                            {a.project} {a.percentage}%
                          </span>
                        ))}
                      </div>
                    )}
                  </div>
                </div>
                <Edit2 className="h-3 w-3 text-forest-300 flex-shrink-0 mt-1" />
              </button>
            );
          })}
        </div>
      )}

      {/* Resource Modal */}
      <EntityModal
        open={modal.open}
        onClose={modal.close}
        title={modal.editId ? "Edit Resource" : "New Resource"}
        onSave={() => modal.save({ person_name: fName, role: fRole || undefined, capacity_status: fCapacity, notes: fNotes || undefined })}
        onDelete={modal.editId ? modal.handleDelete : undefined}
        saving={modal.saving}
        deleting={modal.deleting}
        error={modal.error}
      >
        <FormInput label="Person Name" value={fName} onChange={setFName} placeholder="Name" />
        <FormInput label="Role" value={fRole} onChange={setFRole} placeholder="Role / title" />
        <FormSelect label="Capacity Status" value={fCapacity} onChange={setFCapacity} options={[
          { value: "available", label: "Available" },
          { value: "allocated", label: "Allocated" },
          { value: "overloaded", label: "Overloaded" },
          { value: "unavailable", label: "Unavailable" },
        ]} />
        <FormTextarea label="Notes" value={fNotes} onChange={setFNotes} placeholder="Additional notes" rows={2} />
      </EntityModal>
    </div>
  );
}
