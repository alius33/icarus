import Link from "next/link";
import { api } from "@/lib/api";
import { getStatusColor } from "@/lib/utils";
import { Plus, FileText, Gavel, CheckSquare, AlertCircle, Users } from "lucide-react";

export default async function ProjectsListPage() {
  let projects;
  let error: string | null = null;

  try {
    projects = await api.getProjects();
  } catch (e) {
    error = e instanceof Error ? e.message : "Failed to load projects";
  }

  if (error) {
    return (
      <div className="space-y-6">
        <h2 className="text-2xl font-bold text-gray-900">Project Hub</h2>
        <div className="rounded-lg border border-red-200 bg-red-50 p-6">
          <p className="text-sm text-red-700">{error}</p>
        </div>
      </div>
    );
  }

  const workstreamProjects = (projects || []).filter((p) => !p.is_custom);
  const customProjects = (projects || []).filter((p) => p.is_custom);

  return (
    <div className="space-y-8">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold text-gray-900">Project Hub</h2>
          <p className="mt-1 text-sm text-gray-500">
            Each project aggregates all related transcripts, decisions, actions,
            and more.
          </p>
        </div>
        <Link
          href="/projects/new"
          className="inline-flex items-center gap-2 rounded-md bg-blue-600 px-4 py-2 text-sm font-medium text-white hover:bg-blue-700 transition-colors"
        >
          <Plus className="h-4 w-4" />
          New Project
        </Link>
      </div>

      {/* Workstream Projects */}
      {workstreamProjects.length > 0 && (
        <section>
          <h3 className="mb-3 text-sm font-semibold uppercase tracking-wider text-gray-500">
            Workstream Projects
          </h3>
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
            {workstreamProjects.map((p) => (
              <ProjectCard key={p.id} project={p} />
            ))}
          </div>
        </section>
      )}

      {/* Custom Projects */}
      {customProjects.length > 0 && (
        <section>
          <h3 className="mb-3 text-sm font-semibold uppercase tracking-wider text-gray-500">
            Custom Projects
          </h3>
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
            {customProjects.map((p) => (
              <ProjectCard key={p.id} project={p} />
            ))}
          </div>
        </section>
      )}

      {(!projects || projects.length === 0) && (
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-8 text-center">
          <p className="text-gray-500 text-sm">
            No projects yet. Projects are automatically created from workstreams
            when the import pipeline runs.
          </p>
        </div>
      )}
    </div>
  );
}

function ProjectCard({ project: p }: { project: { id: number; name: string; description: string | null; is_custom: boolean; status: string; color: string | null; workstream_code: string | null; transcript_count: number; decision_count: number; action_count: number; open_thread_count: number; stakeholder_count: number } }) {
  const totalItems =
    p.transcript_count +
    p.decision_count +
    p.action_count +
    p.open_thread_count +
    p.stakeholder_count;

  return (
    <Link
      href={`/projects/${p.id}`}
      className="block rounded-lg border border-gray-200 bg-white shadow-sm transition-all hover:border-blue-300 hover:shadow-md overflow-hidden"
    >
      {/* Color accent bar */}
      <div
        className="h-1.5"
        style={{ backgroundColor: p.color || "#3B82F6" }}
      />

      <div className="p-5">
        <div className="mb-3 flex items-center justify-between">
          <div className="flex items-center gap-2">
            {p.workstream_code && (
              <span className="inline-flex items-center rounded-md bg-blue-100 px-2 py-0.5 text-xs font-semibold text-blue-800">
                {p.workstream_code}
              </span>
            )}
            {p.is_custom && (
              <span className="inline-flex items-center rounded-md bg-purple-100 px-2 py-0.5 text-xs font-semibold text-purple-800">
                Custom
              </span>
            )}
          </div>
          <span
            className={`inline-flex items-center rounded-full border px-2.5 py-0.5 text-xs font-medium ${getStatusColor(p.status)}`}
          >
            {p.status}
          </span>
        </div>

        <h3 className="text-base font-semibold text-gray-900">{p.name}</h3>

        {p.description && (
          <p className="mt-1 text-xs text-gray-500 line-clamp-2">
            {p.description}
          </p>
        )}

        {/* Entity count pills */}
        {totalItems > 0 && (
          <div className="mt-4 flex flex-wrap gap-2">
            {p.transcript_count > 0 && (
              <CountPill icon={<FileText className="h-3 w-3" />} count={p.transcript_count} label="transcripts" />
            )}
            {p.decision_count > 0 && (
              <CountPill icon={<Gavel className="h-3 w-3" />} count={p.decision_count} label="decisions" />
            )}
            {p.action_count > 0 && (
              <CountPill icon={<CheckSquare className="h-3 w-3" />} count={p.action_count} label="actions" />
            )}
            {p.open_thread_count > 0 && (
              <CountPill icon={<AlertCircle className="h-3 w-3" />} count={p.open_thread_count} label="threads" />
            )}
            {p.stakeholder_count > 0 && (
              <CountPill icon={<Users className="h-3 w-3" />} count={p.stakeholder_count} label="people" />
            )}
          </div>
        )}
      </div>
    </Link>
  );
}

function CountPill({
  icon,
  count,
  label,
}: {
  icon: React.ReactNode;
  count: number;
  label: string;
}) {
  return (
    <span className="inline-flex items-center gap-1 rounded-full bg-gray-100 px-2 py-0.5 text-xs text-gray-600">
      {icon}
      {count} {label}
    </span>
  );
}
