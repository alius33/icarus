"use client";

import { useEffect, useState } from "react";
import { api } from "@/lib/api";
import { severityColor } from "@/lib/utils";
import type { OpenThreadSchema, OpenThreadCreate, DependencySchema, DependencyCreate } from "@/lib/types";
import { useEntityModal } from "./hooks/useEntityModal";
import EntityModal, { FormInput, FormTextarea, FormSelect } from "@/components/EntityModal";
import { ShieldAlert, Link2, Plus, Edit2 } from "lucide-react";

export default function RiskDependencyBoard() {
  const [threads, setThreads] = useState<OpenThreadSchema[]>([]);
  const [dependencies, setDependencies] = useState<DependencySchema[]>([]);
  const [loading, setLoading] = useState(true);

  // Thread form state
  const [tTitle, setTTitle] = useState("");
  const [tContext, setTContext] = useState("");
  const [tStatus, setTStatus] = useState("OPEN");
  const [tSeverity, setTSeverity] = useState("");
  const [tTrend, setTTrend] = useState("");

  // Dep form state
  const [dName, setDName] = useState("");
  const [dType, setDType] = useState("technical");
  const [dStatus, setDStatus] = useState("pending");
  const [dBlocking, setDBlocking] = useState("");
  const [dPriority, setDPriority] = useState("medium");
  const [dAssigned, setDAssigned] = useState("");
  const [dNotes, setDNotes] = useState("");

  const loadData = async () => {
    try {
      const [t, d] = await Promise.allSettled([
        api.getOpenThreads({ status: "OPEN" }),
        api.getDependencies(),
      ]);
      if (t.status === "fulfilled") setThreads(t.value);
      if (d.status === "fulfilled") setDependencies(d.value);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { loadData(); }, []);

  const threadModal = useEntityModal<OpenThreadCreate>({
    onSave: async (data) => {
      if (threadModal.editId) {
        await api.updateOpenThread(threadModal.editId, data);
      } else {
        await api.createOpenThread(data);
      }
    },
    onDelete: async (id) => { await api.deleteOpenThread(id); },
    onSuccess: loadData,
  });

  const depModal = useEntityModal<DependencyCreate>({
    onSave: async (data) => {
      if (depModal.editId) {
        await api.updateDependency(depModal.editId, data);
      } else {
        await api.createDependency(data);
      }
    },
    onDelete: async (id) => { await api.deleteDependency(id); },
    onSuccess: loadData,
  });

  const handleThreadEdit = (t: OpenThreadSchema) => {
    setTTitle(t.title);
    setTContext(t.description || "");
    setTStatus(t.status);
    setTSeverity(t.severity || "");
    setTTrend(t.trend || "");
    threadModal.openEdit(t.id);
  };

  const handleThreadCreate = () => {
    setTTitle(""); setTContext(""); setTStatus("OPEN"); setTSeverity(""); setTTrend("");
    threadModal.openCreate();
  };

  const handleDepEdit = (d: DependencySchema) => {
    setDName(d.name);
    setDType(d.dependency_type || "technical");
    setDStatus(d.status);
    setDBlocking(d.blocking_reason || "");
    setDPriority(d.priority || "medium");
    setDAssigned(d.assigned_to || "");
    setDNotes(d.notes || "");
    depModal.openEdit(d.id);
  };

  const handleDepCreate = () => {
    setDName(""); setDType("technical"); setDStatus("pending"); setDBlocking("");
    setDPriority("medium"); setDAssigned(""); setDNotes("");
    depModal.openCreate();
  };

  if (loading) {
    return <div className="p-6 text-base text-gray-500">Loading risks & dependencies...</div>;
  }

  const criticalThreads = threads.filter((t) => t.severity === "CRITICAL");
  const highThreads = threads.filter((t) => t.severity === "HIGH");
  const otherThreads = threads.filter((t) => !["CRITICAL", "HIGH"].includes(t.severity || ""));

  const blockedDeps = dependencies.filter((d) => d.status === "blocked");
  const activeDeps = dependencies.filter((d) => d.status !== "blocked" && d.status !== "completed");

  return (
    <div className="grid grid-cols-1 gap-6 lg:grid-cols-2 p-4">
      {/* Risk Heat Map */}
      <div>
        <div className="flex items-center justify-between mb-3">
          <h4 className="text-sm font-semibold text-gray-500 uppercase tracking-wider flex items-center gap-1.5">
            <ShieldAlert className="h-3.5 w-3.5" />
            Open Risks ({threads.length})
          </h4>
          <button
            onClick={handleThreadCreate}
            className="flex items-center gap-1 text-sm text-blue-600 hover:text-blue-800"
          >
            <Plus className="h-3 w-3" /> Add
          </button>
        </div>

        <div className="space-y-2">
          {criticalThreads.length > 0 && (
            <RiskGroup label="Critical" items={criticalThreads} onEdit={handleThreadEdit} />
          )}
          {highThreads.length > 0 && (
            <RiskGroup label="High" items={highThreads} onEdit={handleThreadEdit} />
          )}
          {otherThreads.length > 0 && (
            <RiskGroup label="Other" items={otherThreads} onEdit={handleThreadEdit} />
          )}
          {threads.length === 0 && (
            <p className="text-base text-gray-500">No open risks.</p>
          )}
        </div>
      </div>

      {/* Dependency List */}
      <div>
        <div className="flex items-center justify-between mb-3">
          <h4 className="text-sm font-semibold text-gray-500 uppercase tracking-wider flex items-center gap-1.5">
            <Link2 className="h-3.5 w-3.5" />
            Dependencies ({dependencies.length})
          </h4>
          <button
            onClick={handleDepCreate}
            className="flex items-center gap-1 text-sm text-blue-600 hover:text-blue-800"
          >
            <Plus className="h-3 w-3" /> Add
          </button>
        </div>

        {blockedDeps.length > 0 && (
          <div className="mb-3">
            <span className="text-[10px] font-semibold uppercase text-red-600 mb-1 block">
              Blocked ({blockedDeps.length})
            </span>
            <div className="space-y-1.5">
              {blockedDeps.map((d) => (
                <DepCard key={d.id} dep={d} onEdit={() => handleDepEdit(d)} />
              ))}
            </div>
          </div>
        )}

        {activeDeps.length > 0 && (
          <div>
            <span className="text-[10px] font-semibold uppercase text-gray-500 mb-1 block">
              Active ({activeDeps.length})
            </span>
            <div className="space-y-1.5">
              {activeDeps.map((d) => (
                <DepCard key={d.id} dep={d} onEdit={() => handleDepEdit(d)} />
              ))}
            </div>
          </div>
        )}

        {dependencies.length === 0 && (
          <p className="text-base text-gray-500">No dependencies tracked.</p>
        )}
      </div>

      {/* Thread/Risk Modal */}
      <EntityModal
        open={threadModal.open}
        onClose={threadModal.close}
        title={threadModal.editId ? "Edit Risk / Thread" : "New Risk / Thread"}
        onSave={() => threadModal.save({ title: tTitle, context: tContext || undefined, status: tStatus, severity: tSeverity || undefined, trend: tTrend || undefined })}
        onDelete={threadModal.editId ? threadModal.handleDelete : undefined}
        saving={threadModal.saving}
        deleting={threadModal.deleting}
        error={threadModal.error}
      >
        <FormInput label="Title" value={tTitle} onChange={setTTitle} placeholder="Risk / thread title" />
        <FormTextarea label="Context" value={tContext} onChange={setTContext} placeholder="What is this about?" rows={2} />
        <FormSelect label="Status" value={tStatus} onChange={setTStatus} options={[
          { value: "OPEN", label: "Open" },
          { value: "WATCHING", label: "Watching" },
          { value: "CLOSED", label: "Closed" },
        ]} />
        <FormSelect label="Severity" value={tSeverity} onChange={setTSeverity} options={[
          { value: "", label: "Unclassified" },
          { value: "CRITICAL", label: "Critical" },
          { value: "HIGH", label: "High" },
          { value: "MEDIUM", label: "Medium" },
          { value: "LOW", label: "Low" },
        ]} />
        <FormSelect label="Trend" value={tTrend} onChange={setTTrend} options={[
          { value: "", label: "None" },
          { value: "escalating", label: "Escalating" },
          { value: "stable", label: "Stable" },
          { value: "de-escalating", label: "De-escalating" },
        ]} />
      </EntityModal>

      {/* Dependency Modal */}
      <EntityModal
        open={depModal.open}
        onClose={depModal.close}
        title={depModal.editId ? "Edit Dependency" : "New Dependency"}
        onSave={() => depModal.save({ name: dName, dependency_type: dType, status: dStatus, blocking_reason: dBlocking || undefined, priority: dPriority, assigned_to: dAssigned || undefined, notes: dNotes || undefined })}
        onDelete={depModal.editId ? depModal.handleDelete : undefined}
        saving={depModal.saving}
        deleting={depModal.deleting}
        error={depModal.error}
      >
        <FormInput label="Name" value={dName} onChange={setDName} placeholder="Dependency name" />
        <FormSelect label="Type" value={dType} onChange={setDType} options={[
          { value: "technical", label: "Technical" },
          { value: "data", label: "Data" },
          { value: "process", label: "Process" },
          { value: "people", label: "People" },
          { value: "external", label: "External" },
        ]} />
        <FormSelect label="Status" value={dStatus} onChange={setDStatus} options={[
          { value: "pending", label: "Pending" },
          { value: "in-progress", label: "In Progress" },
          { value: "blocked", label: "Blocked" },
          { value: "completed", label: "Completed" },
        ]} />
        <FormInput label="Blocking Reason" value={dBlocking} onChange={setDBlocking} placeholder="Why is it blocked?" />
        <FormSelect label="Priority" value={dPriority} onChange={setDPriority} options={[
          { value: "critical", label: "Critical" },
          { value: "high", label: "High" },
          { value: "medium", label: "Medium" },
          { value: "low", label: "Low" },
        ]} />
        <FormInput label="Assigned To" value={dAssigned} onChange={setDAssigned} placeholder="Who is responsible?" />
        <FormTextarea label="Notes" value={dNotes} onChange={setDNotes} placeholder="Additional notes" rows={2} />
      </EntityModal>
    </div>
  );
}

function RiskGroup({
  label,
  items,
  onEdit,
}: {
  label: string;
  items: OpenThreadSchema[];
  onEdit: (t: OpenThreadSchema) => void;
}) {
  return (
    <div>
      <span className="text-[10px] font-semibold uppercase text-gray-500 mb-1 block">
        {label} ({items.length})
      </span>
      <div className="space-y-1.5">
        {items.map((t) => (
          <button
            key={t.id}
            onClick={() => onEdit(t)}
            className="flex items-start gap-2 w-full text-left rounded-md border border-gray-100 bg-white px-3 py-2 hover:bg-gray-50 transition-colors"
          >
            <span
              className={`mt-0.5 inline-flex rounded-full border px-1.5 py-0.5 text-[10px] font-medium ${severityColor(t.severity || "")}`}
            >
              {t.severity || "?"}
            </span>
            <div className="flex-1 min-w-0">
              <p className="text-base font-medium text-gray-900 truncate">
                {t.title}
              </p>
              {t.trend && (
                <span className="text-[10px] text-gray-500">
                  Trend: {t.trend}
                </span>
              )}
            </div>
            <Edit2 className="h-3 w-3 text-gray-400 flex-shrink-0 mt-1" />
          </button>
        ))}
      </div>
    </div>
  );
}

function DepCard({
  dep,
  onEdit,
}: {
  dep: DependencySchema;
  onEdit: () => void;
}) {
  const statusColors: Record<string, string> = {
    blocked: "bg-red-100 text-red-700",
    "in-progress": "bg-blue-100 text-blue-700",
    pending: "bg-yellow-100 text-yellow-700",
    completed: "bg-green-100 text-green-700",
  };

  return (
    <button
      onClick={onEdit}
      className="flex items-start gap-2 w-full text-left rounded-md border border-gray-100 bg-white px-3 py-2 hover:bg-gray-50 transition-colors"
    >
      <span
        className={`mt-0.5 inline-flex rounded-full px-1.5 py-0.5 text-[10px] font-medium ${statusColors[dep.status] || "bg-gray-100 text-gray-600"}`}
      >
        {dep.status}
      </span>
      <div className="flex-1 min-w-0">
        <p className="text-base font-medium text-gray-900 truncate">{dep.name}</p>
        {dep.blocking_reason && (
          <p className="text-[10px] text-gray-500 truncate">
            {dep.blocking_reason}
          </p>
        )}
      </div>
      <Edit2 className="h-3 w-3 text-gray-400 flex-shrink-0 mt-1" />
    </button>
  );
}
