"use client";

import { useEffect, Suspense } from "react";
import { DashboardProvider, useDashboardDispatch } from "./DashboardContext";
import { useDashboardData } from "./hooks/useDashboardData";
import { useDashboardFilters } from "./hooks/useDashboardFilters";
import { useKeyboardShortcuts } from "./hooks/useKeyboardShortcuts";
import { useDashboardModals } from "./hooks/useDashboardModals";
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
import type { DashboardDataV2 } from "@/lib/types";
import { useRouter } from "next/navigation";

interface Props {
  initialData: DashboardDataV2;
}

function DashboardInner({ initialData }: Props) {
  const { data, refreshSection } = useDashboardData();
  const { filters, initFromUrl } = useDashboardFilters();
  const dispatch = useDashboardDispatch();
  const router = useRouter();

  const modal = useDashboardModals({
    refreshSection,
    onNavigate: (path) => router.push(path),
  });

  // Keyboard shortcuts (/ for search, 1/2/3 for tabs, Escape to close modal)
  useKeyboardShortcuts({
    onEscape: modal.closeModal,
    onSearch: () => router.push("/search"),
    onTabSwitch: (tab) => dispatch({ type: "SET_TAB", payload: tab }),
    enabled: !modal.modalOpen,
  });

  // Initialize data and filters
  useEffect(() => {
    if (!data) {
      dispatch({ type: "SET_DATA", payload: initialData });
    }
    initFromUrl();
  }, []); // eslint-disable-line react-hooks/exhaustive-deps

  const d = data || initialData;

  // Extract project list for the filter dropdown
  const projectOptions = d.projects
    .map((p) => ({ code: String(p.id), name: p.name }))
    .sort((a, b) => a.name.localeCompare(b.name));

  // Filter projects by name if filter is set
  const filteredProjects = filters.workstreamFilter
    ? d.projects.filter((p) => String(p.id) === filters.workstreamFilter)
    : d.projects;

  return (
    <div className="space-y-5">
      {/* Header with filters */}
      <DashboardHeader workstreams={projectOptions} />

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
        <NeedsAttention items={d.needs_attention} onItemClick={modal.handleAttentionClick} />
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
                  <ActivityFeed items={d.recent_activity} onItemClick={modal.handleActivityClick} />
                </div>
              </SectionErrorBoundary>
              <SectionErrorBoundary section="Stakeholder Engagement">
                <div className="rounded-lg border border-gray-200 bg-white p-5">
                  <StakeholderPanel items={d.stakeholder_engagement} onItemClick={modal.handleStakeholderClick} />
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
        open={modal.modalOpen}
        onClose={modal.closeModal}
        title={
          modal.modalType === "action_item" ? "Edit Action Item"
          : modal.modalType === "decision" ? "Edit Decision"
          : modal.modalType === "stakeholder" ? "Edit Stakeholder"
          : "Edit Thread"
        }
        onSave={modal.handleModalSave}
        onDelete={modal.handleModalDelete}
        saving={modal.saving}
        deleting={modal.deleting}
        error={modal.modalError}
      >
        {modal.modalType === "action_item" && (
          <>
            <FormInput label="Description" value={modal.form.title} onChange={modal.setFormTitle} placeholder="Action item description" />
            <FormTextarea label="Context" value={modal.form.description} onChange={modal.setFormDescription} placeholder="Additional context" rows={2} />
            <FormSelect label="Status" value={modal.form.status} onChange={modal.setFormStatus} options={[
              { value: "open", label: "Open" },
              { value: "in_progress", label: "In Progress" },
              { value: "done", label: "Done" },
              { value: "blocked", label: "Blocked" },
            ]} />
            <FormInput label="Owner" value={modal.form.owner} onChange={modal.setFormOwner} placeholder="Who is responsible?" />
            <FormInput label="Due Date" value={modal.form.dueDate} onChange={modal.setFormDueDate} placeholder="YYYY-MM-DD" />
          </>
        )}
        {modal.modalType === "open_thread" && (
          <>
            <FormInput label="Title" value={modal.form.title} onChange={modal.setFormTitle} placeholder="Thread title" />
            <FormTextarea label="Context" value={modal.form.description} onChange={modal.setFormDescription} placeholder="What is this about?" rows={2} />
            <FormSelect label="Status" value={modal.form.status} onChange={modal.setFormStatus} options={[
              { value: "OPEN", label: "Open" },
              { value: "WATCHING", label: "Watching" },
              { value: "CLOSED", label: "Closed" },
            ]} />
            <FormInput label="Owner" value={modal.form.owner} onChange={modal.setFormOwner} placeholder="Who is responsible?" />
          </>
        )}
        {modal.modalType === "decision" && (
          <>
            <FormInput label="Decision" value={modal.form.title} onChange={modal.setFormTitle} placeholder="What was decided?" />
            <FormTextarea label="Rationale" value={modal.form.description} onChange={modal.setFormDescription} placeholder="Why was this decided?" rows={2} />
            <FormInput label="Owner" value={modal.form.owner} onChange={modal.setFormOwner} placeholder="Key people" />
          </>
        )}
        {modal.modalType === "stakeholder" && (
          <>
            <FormInput label="Name" value={modal.form.title} onChange={modal.setFormTitle} placeholder="Stakeholder name" />
            <FormInput label="Role" value={modal.form.extra} onChange={modal.setFormExtra} placeholder="Role / title" />
            <FormSelect label="Tier" value={modal.form.status} onChange={modal.setFormStatus} options={[
              { value: "1", label: "Tier 1" },
              { value: "2", label: "Tier 2" },
              { value: "3", label: "Tier 3" },
            ]} />
            <FormTextarea label="Notes" value={modal.form.description} onChange={modal.setFormDescription} placeholder="Notes about this stakeholder" rows={2} />
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
