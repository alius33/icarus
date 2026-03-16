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
        <h2 className="text-2xl font-bold text-forest-950">Project Hub</h2>
        <div className="rounded-lg border border-red-200 bg-red-50 p-6">
          <p className="text-base text-red-700">{error}</p>
        </div>
      </div>
    );
  }

  const allProjects = (projects || []).sort((a, b) => a.name.localeCompare(b.name));

  return (
    <div className="space-y-8">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold text-forest-950">Project Hub</h2>
          <p className="mt-1 text-base text-forest-400">
            Each project aggregates all related transcripts, decisions, actions,
            and more.
          </p>
        </div>
        <Link
          href="/projects/new"
          className="inline-flex items-center gap-2 rounded-md bg-forest-500 px-4 py-2 text-base font-medium text-white hover:bg-forest-600 transition-colors"
        >
          <Plus className="h-4 w-4" />
          New Project
        </Link>
      </div>

      {/* All Projects */}
      {allProjects.length > 0 && (
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {allProjects.map((p) => (
            <ProjectCard key={p.id} project={p} />
          ))}
        </div>
      )}

      {(!projects || projects.length === 0) && (
        <div className="bg-white dark:bg-forest-800 rounded-lg shadow-sm border border-forest-200 p-8 text-center">
          <p className="text-forest-400 text-base">
            No projects yet. Projects are automatically created
            when the import pipeline runs.
          </p>
        </div>
      )}
    </div>
  );
}

function ProjectCard({ project: p }: { project: { id: number; name: string; description: string | null; is_custom: boolean; status: string; color: string | null; code: string | null; transcript_count: number; decision_count: number; action_count: number; open_thread_count: number; stakeholder_count: number } }) {
  const totalItems =
    p.transcript_count +
    p.decision_count +
    p.action_count +
    p.open_thread_count +
    p.stakeholder_count;

  return (
    <Link
      href={`/projects/${p.id}`}
      className="block rounded-lg border border-forest-200 bg-white dark:bg-forest-800 shadow-sm transition-all hover:border-blue-300 hover:shadow-md overflow-hidden"
    >
      {/* Color accent bar */}
      <div
        className="h-1.5"
        style={{ backgroundColor: p.color || "#3B82F6" }}
      />

      <div className="p-5">
        <div className="mb-3 flex items-center justify-between">
          <div className="flex items-center gap-2" />
          <span
            className={`inline-flex items-center rounded-full border px-2.5 py-0.5 text-sm font-medium ${getStatusColor(p.status)}`}
          >
            {p.status}
          </span>
        </div>

        <h3 className="text-base font-semibold text-forest-950">{p.name}</h3>

        {p.description && (
          <p className="mt-1 text-sm text-forest-400 line-clamp-2">
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
    <span className="inline-flex items-center gap-1 rounded-full bg-forest-100 px-2 py-0.5 text-sm text-forest-500">
      {icon}
      {count} {label}
    </span>
  );
}
