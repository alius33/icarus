"use client";

import { useEffect, useState, useCallback } from "react";
import Link from "next/link";
import { api } from "@/lib/api";
import { formatDate, getStatusColor } from "@/lib/utils";
import type { OpenThreadSchema } from "@/lib/types";
import EntityModal, { FormInput, FormTextarea, FormSelect } from "@/components/EntityModal";
import {
  ArrowLeft,
  TrendingUp,
  TrendingDown,
  Minus,
  AlertTriangle,
  ShieldAlert,
  ShieldCheck,
  Shield,
  HelpCircle,
} from "lucide-react";

const SEVERITY_COLUMNS = [
  "CRITICAL",
  "HIGH",
  "MEDIUM",
  "LOW",
  "Unclassified",
] as const;

type SeverityColumn = (typeof SEVERITY_COLUMNS)[number];

const SEVERITY_STYLES: Record<
  SeverityColumn,
  { header: string; border: string; icon: React.ReactNode }
> = {
  CRITICAL: {
    header: "bg-red-600 text-white",
    border: "border-red-300",
    icon: <ShieldAlert className="h-4 w-4" />,
  },
  HIGH: {
    header: "bg-orange-500 text-white",
    border: "border-orange-300",
    icon: <AlertTriangle className="h-4 w-4" />,
  },
  MEDIUM: {
    header: "bg-yellow-400 text-yellow-900",
    border: "border-yellow-300",
    icon: <Shield className="h-4 w-4" />,
  },
  LOW: {
    header: "bg-green-500 text-white",
    border: "border-green-300",
    icon: <ShieldCheck className="h-4 w-4" />,
  },
  Unclassified: {
    header: "bg-gray-400 text-white",
    border: "border-gray-300",
    icon: <HelpCircle className="h-4 w-4" />,
  },
};

function TrendIndicator({ trend }: { trend: string | null }) {
  if (!trend) return null;
  const t = trend.toLowerCase();
  if (t === "escalating") {
    return (
      <span className="inline-flex items-center gap-1 text-xs font-medium text-red-600">
        <TrendingUp className="h-3.5 w-3.5" />
        Escalating
      </span>
    );
  }
  if (t === "de-escalating") {
    return (
      <span className="inline-flex items-center gap-1 text-xs font-medium text-green-600">
        <TrendingDown className="h-3.5 w-3.5" />
        De-escalating
      </span>
    );
  }
  return (
    <span className="inline-flex items-center gap-1 text-xs font-medium text-yellow-600">
      <Minus className="h-3.5 w-3.5" />
      Stable
    </span>
  );
}

function classifyBySeverity(
  threads: OpenThreadSchema[],
): Record<SeverityColumn, OpenThreadSchema[]> {
  const grouped: Record<SeverityColumn, OpenThreadSchema[]> = {
    CRITICAL: [],
    HIGH: [],
    MEDIUM: [],
    LOW: [],
    Unclassified: [],
  };

  for (const thread of threads) {
    const sev = thread.severity?.toUpperCase() as SeverityColumn | undefined;
    if (sev && sev in grouped) {
      grouped[sev].push(thread);
    } else {
      grouped.Unclassified.push(thread);
    }
  }

  return grouped;
}

function truncate(text: string, maxLen: number): string {
  if (text.length <= maxLen) return text;
  return text.slice(0, maxLen).trimEnd() + "...";
}

export default function RiskRegisterPage() {
  const [threads, setThreads] = useState<OpenThreadSchema[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  // Modal state
  const [modalOpen, setModalOpen] = useState(false);
  const [editingItem, setEditingItem] = useState<OpenThreadSchema | null>(null);
  const [formTitle, setFormTitle] = useState("");
  const [formContext, setFormContext] = useState("");
  const [formStatus, setFormStatus] = useState("OPEN");
  const [saving, setSaving] = useState(false);
  const [deleting, setDeleting] = useState(false);
  const [modalError, setModalError] = useState<string | null>(null);

  const reload = useCallback(() => {
    api.getOpenThreads().then(setThreads).catch(() => {});
  }, []);

  useEffect(() => {
    api.getOpenThreads()
      .then(setThreads)
      .catch((e) => setError(e instanceof Error ? e.message : "Failed to load risk data"))
      .finally(() => setLoading(false));
  }, []);

  const openEdit = (t: OpenThreadSchema) => {
    setEditingItem(t);
    setFormTitle(t.title);
    setFormContext(t.description || "");
    setFormStatus(t.status);
    setModalError(null);
    setModalOpen(true);
  };

  const handleSave = async () => {
    if (!editingItem) return;
    setSaving(true);
    setModalError(null);
    try {
      await api.updateOpenThread(editingItem.id, {
        title: formTitle,
        context: formContext || undefined,
        status: formStatus,
      });
      setModalOpen(false);
      reload();
    } catch (e) {
      setModalError(e instanceof Error ? e.message : "Save failed");
    } finally {
      setSaving(false);
    }
  };

  const handleDelete = async () => {
    if (!editingItem) return;
    setDeleting(true);
    try {
      await api.deleteOpenThread(editingItem.id);
      setModalOpen(false);
      reload();
    } catch (e) {
      setModalError(e instanceof Error ? e.message : "Delete failed");
    } finally {
      setDeleting(false);
    }
  };

  if (loading) {
    return (
      <div className="space-y-6">
        <h2 className="text-2xl font-bold text-gray-900">Risk Register</h2>
        <p className="text-sm text-gray-500">Loading risks...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="space-y-6">
        <div className="flex items-center gap-3">
          <Link href="/" className="text-gray-400 hover:text-gray-600 transition-colors">
            <ArrowLeft className="h-5 w-5" />
          </Link>
          <h2 className="text-2xl font-bold text-gray-900">Risk Register</h2>
        </div>
        <div className="rounded-lg border border-red-200 bg-red-50 p-6">
          <p className="text-sm text-red-700">{error}</p>
        </div>
      </div>
    );
  }

  const grouped = classifyBySeverity(threads);
  const totalCount = threads.length;

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          <Link href="/" className="text-gray-400 hover:text-gray-600 transition-colors">
            <ArrowLeft className="h-5 w-5" />
          </Link>
          <div>
            <h2 className="text-2xl font-bold text-gray-900">Risk Register</h2>
            <p className="mt-1 text-sm text-gray-500">
              {totalCount} open thread{totalCount !== 1 ? "s" : ""} across all
              severity levels
            </p>
          </div>
        </div>
      </div>

      {/* Summary bar */}
      <div className="grid grid-cols-2 gap-3 sm:grid-cols-5">
        {SEVERITY_COLUMNS.map((sev) => {
          const count = grouped[sev].length;
          const style = SEVERITY_STYLES[sev];
          return (
            <div
              key={sev}
              className={`rounded-lg border ${style.border} bg-white p-4 text-center`}
            >
              <p className="text-2xl font-bold text-gray-900">{count}</p>
              <p className="text-xs font-medium text-gray-500 uppercase tracking-wide mt-1">
                {sev}
              </p>
            </div>
          );
        })}
      </div>

      {/* Risk board columns */}
      {totalCount === 0 ? (
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-12 text-center">
          <p className="text-sm text-gray-500">
            No open threads found. Risks will appear here once open threads are
            recorded.
          </p>
        </div>
      ) : (
        <div className="grid grid-cols-1 gap-6 lg:grid-cols-5">
          {SEVERITY_COLUMNS.map((sev) => {
            const items = grouped[sev];
            const style = SEVERITY_STYLES[sev];

            return (
              <div key={sev} className="flex flex-col">
                <div
                  className={`rounded-t-lg px-4 py-2.5 flex items-center justify-between ${style.header}`}
                >
                  <div className="flex items-center gap-2">
                    {style.icon}
                    <span className="text-sm font-semibold">{sev}</span>
                  </div>
                  <span className="text-sm font-medium opacity-80">
                    {items.length}
                  </span>
                </div>

                <div
                  className={`flex-1 space-y-3 rounded-b-lg border-x border-b ${style.border} bg-gray-50 p-3`}
                >
                  {items.length === 0 ? (
                    <p className="text-xs text-gray-400 text-center py-6">
                      No items
                    </p>
                  ) : (
                    items.map((thread) => (
                      <div
                        key={thread.id}
                        className="rounded-lg bg-white border border-gray-200 p-4 shadow-sm hover:shadow-md hover:border-gray-300 transition-all cursor-pointer"
                        onClick={() => openEdit(thread)}
                      >
                        <h4 className="text-sm font-semibold text-gray-900 leading-snug">
                          {thread.title}
                        </h4>

                        {thread.description && (
                          <p className="mt-2 text-xs text-gray-600 leading-relaxed">
                            {truncate(thread.description, 120)}
                          </p>
                        )}

                        <div className="mt-3 flex flex-wrap items-center gap-2">
                          <span
                            className={`inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium border ${getStatusColor(thread.status)}`}
                          >
                            {thread.status}
                          </span>
                          <TrendIndicator trend={thread.trend} />
                        </div>

                        <div className="mt-2 flex flex-wrap items-center gap-x-3 gap-y-1 text-xs text-gray-400">
                          {thread.opened_date && (
                            <span>Opened {formatDate(thread.opened_date)}</span>
                          )}
                          {thread.owner && <span>Owner: {thread.owner}</span>}
                          {thread.workstream && (
                            <span>{thread.workstream}</span>
                          )}
                        </div>
                      </div>
                    ))
                  )}
                </div>
              </div>
            );
          })}
        </div>
      )}

      <EntityModal
        open={modalOpen}
        onClose={() => setModalOpen(false)}
        title="Edit Thread / Risk"
        onSave={handleSave}
        onDelete={handleDelete}
        saving={saving}
        deleting={deleting}
        error={modalError}
      >
        <FormInput label="Title" value={formTitle} onChange={setFormTitle} placeholder="Thread title" />
        <FormTextarea label="Context" value={formContext} onChange={setFormContext} placeholder="What is this about?" />
        <FormSelect label="Status" value={formStatus} onChange={setFormStatus} options={[{ value: "OPEN", label: "Open" }, { value: "WATCHING", label: "Watching" }, { value: "CLOSED", label: "Closed" }]} />
      </EntityModal>
    </div>
  );
}
