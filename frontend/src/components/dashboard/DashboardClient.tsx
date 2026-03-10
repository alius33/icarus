"use client";

import { useEffect, useState, Suspense } from "react";
import { DashboardProvider, useDashboardDispatch } from "./DashboardContext";
import { useDashboardData } from "./hooks/useDashboardData";
import { useDashboardFilters } from "./hooks/useDashboardFilters";
import { useKeyboardShortcuts } from "./hooks/useKeyboardShortcuts";
import SectionErrorBoundary from "./SectionErrorBoundary";
import ProgrammeStatusCard from "./ProgrammeStatusCard";
import DashboardHeader from "./DashboardHeader";
import KpiStrip from "./KpiStrip";
import InsightsStrip from "./InsightsStrip";
import ProgrammePulse from "./ProgrammePulse";
import NeedsAttention from "./NeedsAttention";
import TabBar from "./TabBar";
import RiskDependencyBoard from "./RiskDependencyBoard";
import ResourceCapacity from "./ResourceCapacity";
import ScopeTracker from "./ScopeTracker";
import ActivityFeed from "./ActivityFeed";
import StakeholderPanel from "./StakeholderPanel";
import EntityModal, { FormInput, FormTextarea, FormSelect } from "@/components/EntityModal";
import { api } from "@/lib/api";
import type { DashboardDataV2, NeedsAttentionItem, ActivityFeedItem, StakeholderEngagementItem } from "@/lib/types";
import { useRouter } from "next/navigation";

type ModalEntityType = "action_item" | "open_thread" | "decision" | "stakeholder";

interface Props {
  initialData: DashboardDataV2;
}

function DashboardInner({ initialData }: Props) {
  const { data, refreshSection } = useDashboardData();
  const { filters, initFromUrl } = useDashboardFilters();
  const dispatch = useDashboardDispatch();
  const router = useRouter();

  // Inline modal state for entity editing
  const [modalOpen, setModalOpen] = useState(false);
  const [modalType, setModalType] = useState<ModalEntityType | null>(null);
  const [modalItemId, setModalItemId] = useState<number | null>(null);
  const [formTitle, setFormTitle] = useState("");
  const [formDescription, setFormDescription] = useState("");
  const [formStatus, setFormStatus] = useState("");
  const [formOwner, setFormOwner] = useState("");
  const [formDueDate, setFormDueDate] = useState("");
  const [formExtra, setFormExtra] = useState(""); // role for stakeholders, rationale for decisions
  const [saving, setSaving] = useState(false);
  const [deleting, setDeleting] = useState(false);
  const [modalError, setModalError] = useState<string | null>(null);

  const openEntityModal = (type: ModalEntityType, id: number, title: string, description: string, status: string, owner: string) => {
    setModalType(type);
    setModalItemId(id);
    setFormTitle(title);
    setFormDescription(description);
    setFormStatus(status);
    setFormOwner(owner);
    setFormDueDate("");
    setFormExtra("");
    setModalError(null);
    setModalOpen(true);
  };

  const handleAttentionClick = (item: NeedsAttentionItem) => {
    openEntityModal(
      item.entity_type as ModalEntityType,
      item.id,
      item.title,
      item.description || "",
      item.status,
      item.owner || "",
    );
  };

  const handleActivityClick = (item: ActivityFeedItem) => {
    if (item.entity_type === "transcript") {
      router.push(`/transcripts/${item.id}`);
      return;
    }
    openEntityModal(
      item.entity_type as ModalEntityType,
      item.id,
      item.title,
      "",
      "",
      "",
    );
    // Fetch full entity data to populate form
    if (item.entity_type === "action_item") {
      api.getActionItems().then((items) => {
        const found = items.find((a) => a.id === item.id);
        if (found) {
          setFormTitle(found.title);
          setFormDescription(found.description || "");
          setFormStatus(found.status);
          setFormOwner(found.owner || "");
          setFormDueDate(found.due_date || "");
        }
      });
    } else if (item.entity_type === "open_thread") {
      api.getOpenThreads().then((items) => {
        const found = items.find((t) => t.id === item.id);
        if (found) {
          setFormTitle(found.title);
          setFormDescription(found.description || "");
          setFormStatus(found.status);
          setFormOwner(found.owner || "");
        }
      });
    } else if (item.entity_type === "decision") {
      api.getDecisions().then((items) => {
        const found = items.find((d) => d.id === item.id);
        if (found) {
          setFormTitle(found.title);
          setFormDescription(found.description || "");
          setFormStatus(found.status);
          setFormOwner(found.owner || "");
        }
      });
    }
  };

  const handleStakeholderClick = (item: StakeholderEngagementItem) => {
    setModalType("stakeholder");
    setModalItemId(item.id);
    setFormTitle(item.name);
    setFormDescription("");
    setFormStatus(String(item.tier));
    setFormOwner("");
    setFormExtra(item.role || "");
    setModalError(null);
    setModalOpen(true);
    // Fetch full stakeholder data
    api.getStakeholder(item.id).then((s) => {
      setFormDescription(s.notes || "");
      setFormExtra(s.role || "");
    }).catch(() => {});
  };

  const handleModalSave = async () => {
    if (!modalItemId || !modalType) return;
    setSaving(true);
    setModalError(null);
    try {
      if (modalType === "action_item") {
        await api.updateActionItem(modalItemId, {
          description: formTitle,
          owner: formOwner || undefined,
          status: formStatus,
          deadline: formDueDate || undefined,
          context: formDescription || undefined,
        });
      } else if (modalType === "open_thread") {
        await api.updateOpenThread(modalItemId, {
          title: formTitle,
          context: formDescription || undefined,
          status: formStatus,
        });
      } else if (modalType === "decision") {
        await api.updateDecision(modalItemId, {
          decision: formTitle,
          rationale: formDescription || undefined,
        });
      } else if (modalType === "stakeholder") {
        await api.updateStakeholder(modalItemId, {
          name: formTitle,
          role: formExtra || undefined,
          tier: Number(formStatus) || undefined,
          notes: formDescription || undefined,
        });
      }
      setModalOpen(false);
      refreshSection("attention");
    } catch (e) {
      setModalError(e instanceof Error ? e.message : "Save failed");
    } finally {
      setSaving(false);
    }
  };

  const handleModalDelete = async () => {
    if (!modalItemId || !modalType) return;
    setDeleting(true);
    try {
      if (modalType === "action_item") {
        await api.deleteActionItem(modalItemId);
      } else if (modalType === "open_thread") {
        await api.deleteOpenThread(modalItemId);
      } else if (modalType === "decision") {
        await api.deleteDecision(modalItemId);
      } else if (modalType === "stakeholder") {
        await api.deleteStakeholder(modalItemId);
      }
      setModalOpen(false);
      refreshSection("attention");
    } catch (e) {
      setModalError(e instanceof Error ? e.message : "Delete failed");
    } finally {
      setDeleting(false);
    }
  };

  // Keyboard shortcuts (/ for search, 1/2/3 for tabs, Escape to close modal)
  useKeyboardShortcuts({
    onEscape: () => setModalOpen(false),
    onSearch: () => router.push("/search"),
    onTabSwitch: (tab) => dispatch({ type: "SET_TAB", payload: tab }),
    enabled: !modalOpen,
  });

  // Initialize data and filters
  useEffect(() => {
    if (!data) {
      dispatch({ type: "SET_DATA", payload: initialData });
    }
    initFromUrl();
  }, []); // eslint-disable-line react-hooks/exhaustive-deps

  const d = data || initialData;

  // Extract workstreams from project cards for the filter dropdown
  const workstreams = d.projects
    .filter((p) => p.workstream_code)
    .map((p) => ({ code: p.workstream_code!, name: p.name }));

  // Filter projects by workstream if filter is set
  const filteredProjects = filters.workstreamFilter
    ? d.projects.filter(
        (p) => p.workstream_code === filters.workstreamFilter,
      )
    : d.projects;

  return (
    <div className="space-y-5">
      {/* Header with filters */}
      <DashboardHeader workstreams={workstreams} />

      {/* Programme Status Card */}
      {d.programme_status && (
        <SectionErrorBoundary section="Programme Status" onRetry={() => refreshSection("status")}>
          <ProgrammeStatusCard status={d.programme_status} />
        </SectionErrorBoundary>
      )}

      {/* KPI Strip */}
      {d.kpi && (
        <SectionErrorBoundary section="KPIs" onRetry={() => refreshSection("kpi")}>
          <KpiStrip kpi={d.kpi} />
        </SectionErrorBoundary>
      )}

      {/* Insights Strip */}
      {d.insights && (
        <SectionErrorBoundary section="Insights" onRetry={() => refreshSection("insights")}>
          <InsightsStrip insights={d.insights} />
        </SectionErrorBoundary>
      )}

      {/* Programme Pulse */}
      <SectionErrorBoundary section="Programme Pulse" onRetry={() => refreshSection("pulse")}>
        <ProgrammePulse projects={filteredProjects} />
      </SectionErrorBoundary>

      {/* Needs Attention */}
      <SectionErrorBoundary section="Needs Attention" onRetry={() => refreshSection("attention")}>
        <NeedsAttention items={d.needs_attention} onItemClick={handleAttentionClick} />
      </SectionErrorBoundary>

      {/* Tabbed Section */}
      <section className="rounded-lg border border-gray-200 bg-white overflow-hidden">
        <TabBar />
        <div className="min-h-[300px]">
          {filters.activeTab === "risks" && (
            <SectionErrorBoundary section="Risks & Dependencies">
              <RiskDependencyBoard />
            </SectionErrorBoundary>
          )}
          {filters.activeTab === "resources" && (
            <div className="grid grid-cols-1 gap-6 lg:grid-cols-2 p-4">
              <SectionErrorBoundary section="Resource Capacity">
                <ResourceCapacity />
              </SectionErrorBoundary>
              <SectionErrorBoundary section="Scope Tracker">
                <ScopeTracker />
              </SectionErrorBoundary>
            </div>
          )}
          {filters.activeTab === "activity" && (
            <div className="grid grid-cols-1 gap-6 lg:grid-cols-2 p-4">
              <SectionErrorBoundary section="Activity Feed">
                <div className="rounded-lg border border-gray-200 bg-white p-5">
                  <ActivityFeed items={d.recent_activity} onItemClick={handleActivityClick} />
                </div>
              </SectionErrorBoundary>
              <SectionErrorBoundary section="Stakeholder Engagement">
                <div className="rounded-lg border border-gray-200 bg-white p-5">
                  <StakeholderPanel items={d.stakeholder_engagement} onItemClick={handleStakeholderClick} />
                </div>
              </SectionErrorBoundary>
            </div>
          )}
        </div>
      </section>

      {/* Compact stat footer */}
      <div className="flex flex-wrap items-center justify-center gap-x-4 gap-y-1 text-xs text-gray-400 pt-2 border-t border-gray-100">
        <span>{d.total_transcripts} Transcripts</span>
        <span>&middot;</span>
        <span>{d.total_decisions} Decisions</span>
        <span>&middot;</span>
        <span>{d.open_actions} Open Actions</span>
        <span>&middot;</span>
        <span>{d.critical_threads} Open Threads</span>
        <span>&middot;</span>
        <span>{d.projects.length} Projects</span>
      </div>

      {/* Inline edit modal for dashboard items */}
      <EntityModal
        open={modalOpen}
        onClose={() => setModalOpen(false)}
        title={
          modalType === "action_item" ? "Edit Action Item"
          : modalType === "decision" ? "Edit Decision"
          : modalType === "stakeholder" ? "Edit Stakeholder"
          : "Edit Thread"
        }
        onSave={handleModalSave}
        onDelete={handleModalDelete}
        saving={saving}
        deleting={deleting}
        error={modalError}
      >
        {modalType === "action_item" && (
          <>
            <FormInput label="Description" value={formTitle} onChange={setFormTitle} placeholder="Action item description" />
            <FormTextarea label="Context" value={formDescription} onChange={setFormDescription} placeholder="Additional context" rows={2} />
            <FormSelect label="Status" value={formStatus} onChange={setFormStatus} options={[
              { value: "open", label: "Open" },
              { value: "in_progress", label: "In Progress" },
              { value: "done", label: "Done" },
              { value: "blocked", label: "Blocked" },
            ]} />
            <FormInput label="Owner" value={formOwner} onChange={setFormOwner} placeholder="Who is responsible?" />
            <FormInput label="Due Date" value={formDueDate} onChange={setFormDueDate} placeholder="YYYY-MM-DD" />
          </>
        )}
        {modalType === "open_thread" && (
          <>
            <FormInput label="Title" value={formTitle} onChange={setFormTitle} placeholder="Thread title" />
            <FormTextarea label="Context" value={formDescription} onChange={setFormDescription} placeholder="What is this about?" rows={2} />
            <FormSelect label="Status" value={formStatus} onChange={setFormStatus} options={[
              { value: "OPEN", label: "Open" },
              { value: "WATCHING", label: "Watching" },
              { value: "CLOSED", label: "Closed" },
            ]} />
            <FormInput label="Owner" value={formOwner} onChange={setFormOwner} placeholder="Who is responsible?" />
          </>
        )}
        {modalType === "decision" && (
          <>
            <FormInput label="Decision" value={formTitle} onChange={setFormTitle} placeholder="What was decided?" />
            <FormTextarea label="Rationale" value={formDescription} onChange={setFormDescription} placeholder="Why was this decided?" rows={2} />
            <FormInput label="Owner" value={formOwner} onChange={setFormOwner} placeholder="Key people" />
          </>
        )}
        {modalType === "stakeholder" && (
          <>
            <FormInput label="Name" value={formTitle} onChange={setFormTitle} placeholder="Stakeholder name" />
            <FormInput label="Role" value={formExtra} onChange={setFormExtra} placeholder="Role / title" />
            <FormSelect label="Tier" value={formStatus} onChange={setFormStatus} options={[
              { value: "1", label: "Tier 1" },
              { value: "2", label: "Tier 2" },
              { value: "3", label: "Tier 3" },
            ]} />
            <FormTextarea label="Notes" value={formDescription} onChange={setFormDescription} placeholder="Notes about this stakeholder" rows={2} />
          </>
        )}
      </EntityModal>
    </div>
  );
}

export default function DashboardClient({ initialData }: Props) {
  return (
    <Suspense fallback={<DashboardSkeleton />}>
      <DashboardProvider initialData={initialData}>
        <DashboardInner initialData={initialData} />
      </DashboardProvider>
    </Suspense>
  );
}

function DashboardSkeleton() {
  return (
    <div className="space-y-5 animate-pulse">
      <div className="h-8 w-64 bg-gray-200 rounded" />
      <div className="h-24 bg-gray-100 rounded-lg" />
      <div className="grid grid-cols-6 gap-3">
        {Array.from({ length: 6 }).map((_, i) => (
          <div key={i} className="h-20 bg-gray-100 rounded-lg" />
        ))}
      </div>
      <div className="h-10 bg-gray-100 rounded" />
      <div className="grid grid-cols-6 gap-3">
        {Array.from({ length: 6 }).map((_, i) => (
          <div key={i} className="h-28 bg-gray-100 rounded-lg" />
        ))}
      </div>
    </div>
  );
}
