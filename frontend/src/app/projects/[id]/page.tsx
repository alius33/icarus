import { Suspense } from "react";
import Link from "next/link";
import { api } from "@/lib/api";
import { getStatusColor } from "@/lib/utils";
import ProjectTabBar, { type TabKey } from "@/components/projects/ProjectTabBar";
import ProjectOverviewTab from "@/components/projects/ProjectOverviewTab";
import ProjectTasksTab from "@/components/projects/ProjectTasksTab";
import ProjectDecisionsTab from "@/components/projects/ProjectDecisionsTab";
import ProjectThreadsTab from "@/components/projects/ProjectThreadsTab";
import ProjectSummariesTab from "@/components/projects/ProjectSummariesTab";
import ProjectBriefButton from "@/components/projects/ProjectBriefButton";

interface ProjectHubPageProps {
  params: Promise<{ id: string }>;
  searchParams: Promise<{ tab?: string }>;
}

export default async function ProjectHubPage({
  params,
  searchParams,
}: ProjectHubPageProps) {
  const { id } = await params;
  const { tab } = await searchParams;
  const activeTab = (tab as TabKey) || "overview";
  const projectId = Number(id);

  let hub;
  let timeline;
  let error: string | null = null;

  try {
    [hub, timeline] = await Promise.all([
      api.getProjectHub(projectId),
      api.getProjectWeekly(projectId),
    ]);
  } catch (e) {
    error = e instanceof Error ? e.message : "Failed to load project";
  }

  if (error || !hub) {
    return (
      <div className="space-y-6">
        <Link
          href="/projects"
          className="text-base text-blue-600 hover:text-blue-800"
        >
          &larr; Back to Projects
        </Link>
        <div className="rounded-lg border border-red-200 bg-red-50 p-6">
          <p className="text-base text-red-700">
            {error || "Unable to load project."}
          </p>
        </div>
      </div>
    );
  }

  const { project } = hub;

  const counts: Record<string, number> = {
    action_count: project.action_count,
    decision_count: project.decision_count,
    open_thread_count: project.open_thread_count,
    transcript_count: project.transcript_count,
  };

  return (
    <div className="space-y-0">
      {/* Back link */}
      <div className="mb-4">
        <Link
          href="/projects"
          className="text-base text-blue-600 hover:text-blue-800"
        >
          &larr; Back to Projects
        </Link>
      </div>

      {/* Project header */}
      <div className="rounded-t-lg border border-gray-200 bg-white p-6">
        <div className="flex items-start justify-between">
          <div>
            <div className="mb-2 flex items-center gap-2">
              <span
                className={`inline-flex items-center rounded-full border px-2.5 py-0.5 text-sm font-medium ${getStatusColor(project.status)}`}
              >
                {project.status}
              </span>
            </div>
            <h2 className="text-2xl font-bold text-gray-900">
              {project.name}
            </h2>
          </div>
          {timeline && (
            <ProjectBriefButton
              project={project}
              actions={hub.action_items}
              timeline={timeline}
            />
          )}
        </div>
      </div>

      {/* Tab bar */}
      <Suspense fallback={null}>
        <ProjectTabBar counts={counts} />
      </Suspense>

      {/* Tab content */}
      <div className="mt-6">
        <Suspense fallback={<div className="flex items-center justify-center py-12"><div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600" /></div>}>
          {activeTab === "overview" && (
            <ProjectOverviewTab
              project={project}
              hub={hub}
              timeline={timeline || null}
            />
          )}
          {activeTab === "tasks" && (
            <ProjectTasksTab projectId={projectId} />
          )}
          {activeTab === "decisions" && (
            <ProjectDecisionsTab projectId={projectId} />
          )}
          {activeTab === "threads" && (
            <ProjectThreadsTab projectId={projectId} />
          )}
          {activeTab === "summaries" && timeline && (
            <ProjectSummariesTab timeline={timeline} project={project} />
          )}
        </Suspense>
      </div>
    </div>
  );
}
