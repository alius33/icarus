import { api } from "@/lib/api";
import { getStatusColor } from "@/lib/utils";
import type { DependencySchema } from "@/lib/types";
import {
  GitBranch,
  AlertTriangle,
  Loader2,
  CheckCircle2,
  Clock,
  ShieldAlert,
  ExternalLink,
  Layers,
  User,
} from "lucide-react";

const STATUS_ORDER: Record<string, number> = {
  blocked: 0,
  "in-progress": 1,
  pending: 2,
  completed: 3,
};

const PRIORITY_BADGE: Record<string, string> = {
  CRITICAL: "bg-red-100 text-red-800 border-red-300",
  HIGH: "bg-orange-100 text-orange-800 border-orange-300",
  MEDIUM: "bg-yellow-100 text-yellow-800 border-yellow-300",
  LOW: "bg-green-100 text-green-800 border-green-300",
};

const TYPE_BADGE: Record<string, string> = {
  integration: "bg-purple-100 text-purple-800 border-purple-200",
  external: "bg-sky-100 text-sky-800 border-sky-200",
  internal: "bg-slate-100 text-slate-700 border-slate-200",
};

function priorityBadge(priority: string): string {
  return PRIORITY_BADGE[priority.toUpperCase()] || "bg-gray-100 text-gray-600 border-gray-200";
}

function typeBadge(depType: string): string {
  return TYPE_BADGE[depType.toLowerCase()] || "bg-gray-100 text-gray-600 border-gray-200";
}

function statusIcon(status: string) {
  const s = status.toLowerCase();
  if (s === "blocked") return <ShieldAlert className="w-4 h-4 text-red-600" />;
  if (s === "in-progress") return <Loader2 className="w-4 h-4 text-blue-600" />;
  if (s === "pending") return <Clock className="w-4 h-4 text-yellow-600" />;
  if (s === "completed") return <CheckCircle2 className="w-4 h-4 text-green-600" />;
  return <Clock className="w-4 h-4 text-gray-400" />;
}

function groupByStatus(deps: DependencySchema[]): Record<string, DependencySchema[]> {
  const groups: Record<string, DependencySchema[]> = {};
  const sorted = [...deps].sort(
    (a, b) =>
      (STATUS_ORDER[a.status.toLowerCase()] ?? 99) -
      (STATUS_ORDER[b.status.toLowerCase()] ?? 99),
  );
  for (const dep of sorted) {
    const key = dep.status.toLowerCase();
    if (!groups[key]) groups[key] = [];
    groups[key].push(dep);
  }
  return groups;
}

const STATUS_LABELS: Record<string, string> = {
  blocked: "Blocked",
  "in-progress": "In Progress",
  pending: "Pending",
  completed: "Completed",
};

export default async function DependenciesPage() {
  let dependencies: DependencySchema[];
  try {
    dependencies = await api.getDependencies();
  } catch {
    return (
      <div className="space-y-6">
        <h2 className="text-2xl font-bold text-gray-900">
          Dependencies / Integration Queue
        </h2>
        <div className="rounded-lg border border-red-200 bg-red-50 p-6">
          <p className="text-base text-red-700">
            Failed to load dependencies. Is the backend running?
          </p>
        </div>
      </div>
    );
  }

  const grouped = groupByStatus(dependencies);
  const blockedCount = (grouped["blocked"] || []).length;
  const inProgressCount = (grouped["in-progress"] || []).length;
  const total = dependencies.length;

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          <GitBranch className="w-6 h-6 text-gray-700" />
          <h2 className="text-2xl font-bold text-gray-900">
            Dependencies / Integration Queue
          </h2>
        </div>
      </div>

      {/* Summary Stats */}
      <div className="grid grid-cols-3 gap-4">
        <div className="bg-white rounded-lg border border-gray-200 p-4 shadow-sm">
          <div className="flex items-center gap-2 text-base text-gray-500 mb-1">
            <Layers className="w-4 h-4" />
            Total
          </div>
          <p className="text-2xl font-semibold text-gray-900">{total}</p>
        </div>
        <div className="bg-white rounded-lg border border-red-200 p-4 shadow-sm">
          <div className="flex items-center gap-2 text-base text-red-600 mb-1">
            <AlertTriangle className="w-4 h-4" />
            Blocked
          </div>
          <p className="text-2xl font-semibold text-red-700">{blockedCount}</p>
        </div>
        <div className="bg-white rounded-lg border border-blue-200 p-4 shadow-sm">
          <div className="flex items-center gap-2 text-base text-blue-600 mb-1">
            <Loader2 className="w-4 h-4" />
            In Progress
          </div>
          <p className="text-2xl font-semibold text-blue-700">
            {inProgressCount}
          </p>
        </div>
      </div>

      {/* Dependency Groups */}
      {total === 0 ? (
        <div className="text-center py-12 bg-white rounded-lg border border-gray-200 shadow-sm">
          <GitBranch className="w-8 h-8 text-gray-300 mx-auto mb-3" />
          <p className="text-base text-gray-500">
            No dependencies tracked yet.
          </p>
        </div>
      ) : (
        Object.entries(grouped).map(([status, deps]) => (
          <div key={status} className="space-y-2">
            <div className="flex items-center gap-2 px-1">
              {statusIcon(status)}
              <h3 className="text-base font-semibold text-gray-700 uppercase tracking-wide">
                {STATUS_LABELS[status] || status}
              </h3>
              <span className="text-sm text-gray-400">({deps.length})</span>
            </div>

            <div className="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden">
              <table className="w-full">
                <thead>
                  <tr className="border-b border-gray-200 bg-gray-50">
                    <th className="px-4 py-3 text-left text-sm font-medium uppercase tracking-wider text-gray-500">
                      Name
                    </th>
                    <th className="px-4 py-3 text-left text-sm font-medium uppercase tracking-wider text-gray-500 w-28">
                      Type
                    </th>
                    <th className="px-4 py-3 text-left text-sm font-medium uppercase tracking-wider text-gray-500 w-28">
                      Status
                    </th>
                    <th className="px-4 py-3 text-left text-sm font-medium uppercase tracking-wider text-gray-500 w-24">
                      Priority
                    </th>
                    <th className="px-4 py-3 text-left text-sm font-medium uppercase tracking-wider text-gray-500">
                      Blocking Reason
                    </th>
                    <th className="px-4 py-3 text-left text-sm font-medium uppercase tracking-wider text-gray-500 w-28">
                      Effort
                    </th>
                    <th className="px-4 py-3 text-left text-sm font-medium uppercase tracking-wider text-gray-500 w-32">
                      Assigned To
                    </th>
                    <th className="px-4 py-3 text-left text-sm font-medium uppercase tracking-wider text-gray-500 w-40">
                      Workstreams
                    </th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-200">
                  {deps.map((dep) => {
                    const isBlocked = dep.status.toLowerCase() === "blocked";
                    return (
                      <tr
                        key={dep.id}
                        className={
                          isBlocked
                            ? "bg-red-50/60 hover:bg-red-50 transition-colors"
                            : "hover:bg-gray-50 transition-colors"
                        }
                      >
                        <td className="px-4 py-4">
                          <p className="text-base font-medium text-gray-900">
                            {dep.name}
                          </p>
                          {dep.notes && (
                            <p className="text-sm text-gray-500 mt-0.5 line-clamp-2">
                              {dep.notes}
                            </p>
                          )}
                        </td>
                        <td className="px-4 py-4">
                          <span
                            className={`inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-sm font-medium border ${typeBadge(dep.dependency_type)}`}
                          >
                            {dep.dependency_type.toLowerCase() ===
                            "integration" ? (
                              <GitBranch className="w-3 h-3" />
                            ) : dep.dependency_type.toLowerCase() ===
                              "external" ? (
                              <ExternalLink className="w-3 h-3" />
                            ) : (
                              <Layers className="w-3 h-3" />
                            )}
                            {dep.dependency_type}
                          </span>
                        </td>
                        <td className="px-4 py-4">
                          <span
                            className={`px-2 py-1 rounded-full text-sm font-medium border ${getStatusColor(dep.status)}`}
                          >
                            {dep.status.replace(/[-_]/g, " ")}
                          </span>
                        </td>
                        <td className="px-4 py-4">
                          <span
                            className={`px-2 py-0.5 rounded-full text-sm font-medium border ${priorityBadge(dep.priority)}`}
                          >
                            {dep.priority}
                          </span>
                        </td>
                        <td className="px-4 py-4">
                          {dep.blocking_reason ? (
                            <p className="text-base text-gray-700">
                              {dep.blocking_reason}
                            </p>
                          ) : (
                            <span className="text-base text-gray-400">
                              &mdash;
                            </span>
                          )}
                        </td>
                        <td className="px-4 py-4 text-base text-gray-600 whitespace-nowrap">
                          {dep.estimated_effort || "\u2014"}
                        </td>
                        <td className="px-4 py-4">
                          {dep.assigned_to ? (
                            <span className="inline-flex items-center gap-1 text-base text-gray-700">
                              <User className="w-3.5 h-3.5 text-gray-400" />
                              {dep.assigned_to}
                            </span>
                          ) : (
                            <span className="text-base text-gray-400">
                              &mdash;
                            </span>
                          )}
                        </td>
                        <td className="px-4 py-4">
                          {dep.affected_workstreams ? (
                            <div className="flex flex-wrap gap-1">
                              {dep.affected_workstreams
                                .split(",")
                                .map((ws) => ws.trim())
                                .filter(Boolean)
                                .map((ws) => (
                                  <span
                                    key={ws}
                                    className="inline-flex items-center px-2 py-0.5 rounded text-sm font-medium bg-indigo-50 text-indigo-700 border border-indigo-200"
                                  >
                                    {ws}
                                  </span>
                                ))}
                            </div>
                          ) : (
                            <span className="text-base text-gray-400">
                              &mdash;
                            </span>
                          )}
                        </td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </div>
          </div>
        ))
      )}
    </div>
  );
}
