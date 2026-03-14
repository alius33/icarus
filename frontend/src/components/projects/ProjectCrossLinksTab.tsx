"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { api } from "@/lib/api";
import { formatDate } from "@/lib/utils";
import type { CrossProjectLinkSchema, ProjectBase } from "@/lib/types";
import EntityModal, {
  FormTextarea,
  FormSelect,
} from "@/components/EntityModal";

const LINK_TYPE_COLORS: Record<string, string> = {
  dependency: "bg-orange-50 text-orange-700 border-orange-200",
  blocker: "bg-red-50 text-red-700 border-red-200",
  related: "bg-blue-50 text-blue-700 border-blue-200",
  synergy: "bg-green-50 text-green-700 border-green-200",
  conflict: "bg-rose-50 text-rose-700 border-rose-200",
  input: "bg-purple-50 text-purple-700 border-purple-200",
  output: "bg-indigo-50 text-indigo-700 border-indigo-200",
};

const SEVERITY_INDICATORS: Record<string, string> = {
  critical: "bg-red-500",
  high: "bg-orange-500",
  medium: "bg-amber-400",
  low: "bg-green-400",
};

const LINK_TYPE_OPTIONS = [
  { value: "dependency", label: "Dependency" },
  { value: "blocker", label: "Blocker" },
  { value: "related", label: "Related" },
  { value: "synergy", label: "Synergy" },
  { value: "conflict", label: "Conflict" },
  { value: "input", label: "Input" },
  { value: "output", label: "Output" },
];

const SEVERITY_OPTIONS = [
  { value: "low", label: "Low" },
  { value: "medium", label: "Medium" },
  { value: "high", label: "High" },
  { value: "critical", label: "Critical" },
];

const STATUS_OPTIONS = [
  { value: "active", label: "Active" },
  { value: "resolved", label: "Resolved" },
  { value: "monitoring", label: "Monitoring" },
];

export default function ProjectCrossLinksTab({
  projectId,
}: {
  projectId: number;
}) {
  const [links, setLinks] = useState<CrossProjectLinkSchema[]>([]);
  const [projects, setProjects] = useState<ProjectBase[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Modal state
  const [modalOpen, setModalOpen] = useState(false);
  const [editingItem, setEditingItem] =
    useState<CrossProjectLinkSchema | null>(null);
  const [formTargetProjectId, setFormTargetProjectId] = useState("");
  const [formLinkType, setFormLinkType] = useState("related");
  const [formDescription, setFormDescription] = useState("");
  const [formSeverity, setFormSeverity] = useState("medium");
  const [formStatus, setFormStatus] = useState("active");
  const [saving, setSaving] = useState(false);
  const [deleting, setDeleting] = useState(false);
  const [modalError, setModalError] = useState<string | null>(null);

  useEffect(() => {
    Promise.all([
      api.getProjectCrossLinks(projectId),
      api.getProjects(),
    ])
      .then(([linksData, projectsData]) => {
        setLinks(linksData);
        setProjects(projectsData);
      })
      .catch((e) =>
        setError(
          e instanceof Error ? e.message : "Failed to load cross-project links",
        ),
      )
      .finally(() => setLoading(false));
  }, [projectId]);

  const reload = () => {
    api
      .getProjectCrossLinks(projectId)
      .then(setLinks)
      .catch(() => {});
  };

  const otherProjects = projects.filter((p) => p.id !== projectId);

  const openCreate = () => {
    setEditingItem(null);
    setFormTargetProjectId(otherProjects[0]?.id?.toString() || "");
    setFormLinkType("related");
    setFormDescription("");
    setFormSeverity("medium");
    setFormStatus("active");
    setModalError(null);
    setModalOpen(true);
  };

  const openEdit = (link: CrossProjectLinkSchema) => {
    setEditingItem(link);
    const otherId =
      link.source_project_id === projectId
        ? link.target_project_id
        : link.source_project_id;
    setFormTargetProjectId(String(otherId));
    setFormLinkType(link.link_type);
    setFormDescription(link.description || "");
    setFormSeverity(link.severity);
    setFormStatus(link.status);
    setModalError(null);
    setModalOpen(true);
  };

  const handleSave = async () => {
    setSaving(true);
    setModalError(null);
    try {
      const targetId = parseInt(formTargetProjectId, 10);
      if (isNaN(targetId)) {
        setModalError("Please select a target project");
        setSaving(false);
        return;
      }
      if (editingItem) {
        await api.updateCrossProjectLink(editingItem.id, {
          source_project_id: projectId,
          target_project_id: targetId,
          link_type: formLinkType,
          description: formDescription || undefined,
          severity: formSeverity,
          status: formStatus,
        });
      } else {
        await api.createCrossProjectLink({
          source_project_id: projectId,
          target_project_id: targetId,
          link_type: formLinkType,
          description: formDescription || undefined,
          severity: formSeverity,
          status: formStatus,
        });
      }
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
      await api.deleteCrossProjectLink(editingItem.id);
      setModalOpen(false);
      reload();
    } catch (e) {
      setModalError(e instanceof Error ? e.message : "Delete failed");
    } finally {
      setDeleting(false);
    }
  };

  if (loading)
    return (
      <p className="text-base text-gray-500 py-4">
        Loading cross-project links...
      </p>
    );

  if (error)
    return (
      <div className="rounded-lg border border-red-200 bg-red-50 p-6">
        <p className="text-base text-red-700">{error}</p>
      </div>
    );

  return (
    <div className="space-y-4">
      <div className="flex justify-end">
        <button
          onClick={openCreate}
          className="px-4 py-2 text-base font-medium text-white bg-blue-600 rounded-md hover:bg-blue-700 transition-colors"
        >
          + New Link
        </button>
      </div>

      {links.length === 0 ? (
        <div className="rounded-lg border border-gray-200 bg-white p-8 text-center">
          <p className="text-base text-gray-500">
            No cross-project links detected yet.
          </p>
        </div>
      ) : (
        <div className="space-y-3">
          {links.map((link) => {
            const isSource = link.source_project_id === projectId;
            const otherName = isSource
              ? link.target_project_name
              : link.source_project_name;
            const otherId = isSource
              ? link.target_project_id
              : link.source_project_id;
            const direction = isSource ? "\u2192" : "\u2190";

            return (
              <div
                key={link.id}
                className="bg-white rounded-lg border border-gray-200 p-4 hover:border-gray-300 transition-colors"
              >
                <div className="flex items-start justify-between">
                  <div className="flex items-start gap-3">
                    {/* Severity dot */}
                    <span
                      className={`mt-1.5 h-2.5 w-2.5 rounded-full flex-shrink-0 ${SEVERITY_INDICATORS[link.severity] || "bg-gray-400"}`}
                      title={`Severity: ${link.severity}`}
                    />

                    <div className="space-y-1">
                      {/* Project names and direction */}
                      <div className="flex items-center gap-2 text-base">
                        <span className="font-medium text-gray-900">
                          This project
                        </span>
                        <span className="text-gray-400">{direction}</span>
                        <Link
                          href={`/projects/${otherId}`}
                          className="font-medium text-blue-600 hover:text-blue-700 hover:underline"
                        >
                          {otherName || `Project #${otherId}`}
                        </Link>
                      </div>

                      {/* Description */}
                      {link.description && (
                        <p className="text-base text-gray-600">
                          {link.description}
                        </p>
                      )}

                      {/* Badges row */}
                      <div className="flex items-center gap-2 mt-1">
                        <span
                          className={`inline-flex items-center px-2 py-0.5 rounded-full text-sm font-medium border capitalize ${LINK_TYPE_COLORS[link.link_type] || "bg-gray-50 text-gray-600 border-gray-200"}`}
                        >
                          {link.link_type}
                        </span>
                        <span
                          className={`inline-flex items-center px-2 py-0.5 rounded-full text-sm font-medium border capitalize ${
                            link.status === "resolved"
                              ? "bg-green-50 text-green-700 border-green-200"
                              : link.status === "monitoring"
                                ? "bg-yellow-50 text-yellow-700 border-yellow-200"
                                : "bg-gray-50 text-gray-600 border-gray-200"
                          }`}
                        >
                          {link.status}
                        </span>
                        {link.date_detected && (
                          <span className="text-sm text-gray-400">
                            Detected {formatDate(link.date_detected)}
                          </span>
                        )}
                      </div>
                    </div>
                  </div>

                  {/* Edit button */}
                  <button
                    onClick={() => openEdit(link)}
                    className="text-gray-400 hover:text-blue-600 flex-shrink-0"
                    title="Edit"
                  >
                    <svg
                      className="w-4 h-4"
                      fill="none"
                      stroke="currentColor"
                      viewBox="0 0 24 24"
                    >
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={2}
                        d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z"
                      />
                    </svg>
                  </button>
                </div>
              </div>
            );
          })}
        </div>
      )}

      {/* Modal */}
      <EntityModal
        open={modalOpen}
        onClose={() => setModalOpen(false)}
        title={editingItem ? "Edit Cross-Project Link" : "New Cross-Project Link"}
        onSave={handleSave}
        onDelete={editingItem ? handleDelete : undefined}
        saving={saving}
        deleting={deleting}
        error={modalError}
      >
        <FormSelect
          label="Linked Project"
          value={formTargetProjectId}
          onChange={setFormTargetProjectId}
          options={otherProjects.map((p) => ({
            value: String(p.id),
            label: p.name,
          }))}
        />
        <FormSelect
          label="Link Type"
          value={formLinkType}
          onChange={setFormLinkType}
          options={LINK_TYPE_OPTIONS}
        />
        <FormSelect
          label="Severity"
          value={formSeverity}
          onChange={setFormSeverity}
          options={SEVERITY_OPTIONS}
        />
        <FormSelect
          label="Status"
          value={formStatus}
          onChange={setFormStatus}
          options={STATUS_OPTIONS}
        />
        <FormTextarea
          label="Description"
          value={formDescription}
          onChange={setFormDescription}
          placeholder="Describe how these projects are linked"
        />
      </EntityModal>
    </div>
  );
}
