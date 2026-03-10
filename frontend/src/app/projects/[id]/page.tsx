import { Suspense } from "react";
import Link from "next/link";
import { api } from "@/lib/api";
import { getStatusColor } from "@/lib/utils";
import ProjectTabBar, { type TabKey } from "@/components/projects/ProjectTabBar";
import ProjectWeeklyOverviewTab from "@/components/projects/ProjectWeeklyOverviewTab";
import ProjectDecisionsTab from "@/components/projects/ProjectDecisionsTab";
import ProjectActionsTab from "@/components/projects/ProjectActionsTab";
import ProjectThreadsTab from "@/components/projects/ProjectThreadsTab";
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
          className="text-sm text-blue-600 hover:text-blue-800"
        >
          &larr; Back to Projects
        </Link>
        <div className="rounded-lg border border-red-200 bg-red-50 p-6">
          <p className="text-sm text-red-700">
            {error || "Unable to load project."}
          </p>
        </div>
      </div>
    );
  }

  const { project } = hub;

  return (
    <div className="space-y-0">
      {/* Back link */}
      <div className="mb-4">
        <Link
          href="/projects"
          className="text-sm text-blue-600 hover:text-blue-800"
        >
          &larr; Back to Projects
        </Link>
      </div>

      {/* Project header */}
      <div className="rounded-t-lg border border-gray-200 bg-white p-6">
        <div className="flex items-start justify-between">
          <div>
            <div className="mb-2 flex items-center gap-2">
              {project.workstream_code && (
                <span className="inline-flex items-center rounded-md bg-blue-100 px-2.5 py-0.5 text-xs font-semibold text-blue-800">
                  {project.workstream_code}
                </span>
              )}
              {project.is_custom && (
                <span className="inline-flex items-center rounded-md bg-purple-100 px-2.5 py-0.5 text-xs font-semibold text-purple-800">
                  Custom
                </span>
              )}
              <span
                className={`inline-flex items-center rounded-full border px-2.5 py-0.5 text-xs font-medium ${getStatusColor(project.status)}`}
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
        <ProjectTabBar />
      </Suspense>

      {/* Tab content */}
      <div className="mt-6">
        {activeTab === "overview" && timeline && (
          <ProjectWeeklyOverviewTab
            timeline={timeline}
            project={project}
            allActions={hub.action_items}
          />
        )}
        {activeTab === "decisions" && (
          <ProjectDecisionsTab decisions={hub.decisions} />
        )}
        {activeTab === "actions" && (
          <ProjectActionsTab actions={hub.action_items} />
        )}
        {activeTab === "threads" && (
          <ProjectThreadsTab threads={hub.open_threads} />
        )}
      </div>
    </div>
  );
}
