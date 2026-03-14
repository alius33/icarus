import { api } from "@/lib/api";
import type { ResourceAllocationSchema, AllocationEntry } from "@/lib/types";
import { User, BarChart3, AlertTriangle, Calendar } from "lucide-react";

function capacityBadge(status: string) {
  const s = status.toLowerCase();
  if (s === "available")
    return (
      <span className="inline-flex items-center gap-1 rounded-full bg-green-50 px-2.5 py-0.5 text-sm font-medium text-green-700 border border-green-200">
        Available
      </span>
    );
  if (s === "stretched")
    return (
      <span className="inline-flex items-center gap-1 rounded-full bg-amber-50 px-2.5 py-0.5 text-sm font-medium text-amber-700 border border-amber-200">
        Stretched
      </span>
    );
  if (s === "overloaded")
    return (
      <span className="inline-flex items-center gap-1 rounded-full bg-red-50 px-2.5 py-0.5 text-sm font-medium text-red-700 border border-red-200">
        <AlertTriangle className="h-3 w-3" />
        Overloaded
      </span>
    );
  return (
    <span className="inline-flex items-center rounded-full bg-gray-50 px-2.5 py-0.5 text-sm font-medium text-gray-600 border border-gray-200">
      {status}
    </span>
  );
}

function allocationBarColor(index: number): string {
  const colors = [
    "bg-blue-500",
    "bg-indigo-500",
    "bg-violet-500",
    "bg-emerald-500",
    "bg-amber-500",
    "bg-rose-500",
    "bg-cyan-500",
    "bg-teal-500",
  ];
  return colors[index % colors.length];
}

function AllocationBar({
  allocation,
  colorIndex,
}: {
  allocation: AllocationEntry;
  colorIndex: number;
}) {
  const pct = Math.min(allocation.percentage, 100);
  return (
    <div className="space-y-1">
      <div className="flex items-center justify-between text-sm">
        <span className="text-gray-600 truncate mr-2">
          {allocation.workstream}
        </span>
        <span className="font-medium text-gray-900 tabular-nums">
          {allocation.percentage}%
        </span>
      </div>
      <div className="h-2 w-full rounded-full bg-gray-100">
        <div
          className={`h-2 rounded-full ${allocationBarColor(colorIndex)}`}
          style={{ width: `${pct}%` }}
        />
      </div>
    </div>
  );
}

function ResourceCard({ resource }: { resource: ResourceAllocationSchema }) {
  const totalAllocation = resource.allocations.reduce(
    (sum, a) => sum + a.percentage,
    0,
  );
  const isOver100 = totalAllocation > 100;

  return (
    <div className="rounded-lg border border-gray-200 bg-white p-6 shadow-sm transition-shadow hover:shadow-md">
      <div className="flex items-start justify-between gap-3">
        <div className="flex items-start gap-3 min-w-0">
          <div className="flex-shrink-0 mt-0.5 rounded-full bg-gray-100 p-2">
            <User className="h-5 w-5 text-gray-500" />
          </div>
          <div className="min-w-0">
            <h3 className="text-lg font-semibold text-gray-900 truncate">
              {resource.person_name}
            </h3>
            {resource.role && (
              <p className="text-base text-gray-500 truncate">{resource.role}</p>
            )}
          </div>
        </div>
        {capacityBadge(resource.capacity_status)}
      </div>

      {resource.allocations.length > 0 && (
        <div className="mt-5 space-y-3">
          {resource.allocations.map((a, i) => (
            <AllocationBar key={a.workstream} allocation={a} colorIndex={i} />
          ))}
        </div>
      )}

      <div className="mt-4 flex items-center justify-between border-t border-gray-100 pt-3">
        <div className="flex items-center gap-1.5 text-base">
          <BarChart3 className="h-4 w-4 text-gray-400" />
          <span className="text-gray-500">Total:</span>
          <span
            className={`font-semibold tabular-nums ${isOver100 ? "text-red-600" : "text-gray-900"}`}
          >
            {totalAllocation}%
          </span>
          {isOver100 && (
            <AlertTriangle className="h-3.5 w-3.5 text-red-500" />
          )}
        </div>
        {(resource.start_date || resource.end_date) && (
          <div className="flex items-center gap-1 text-sm text-gray-400">
            <Calendar className="h-3 w-3" />
            <span>
              {resource.start_date ?? "..."} &ndash;{" "}
              {resource.end_date ?? "ongoing"}
            </span>
          </div>
        )}
      </div>

      {resource.notes && (
        <p className="mt-3 text-sm text-gray-500 leading-relaxed">
          {resource.notes}
        </p>
      )}
    </div>
  );
}

export default async function ResourcesPage() {
  let resources: ResourceAllocationSchema[];
  try {
    resources = await api.getResources();
  } catch {
    return (
      <div className="space-y-6">
        <h2 className="text-2xl font-bold text-gray-900">
          Resource Allocation
        </h2>
        <div className="rounded-lg border border-red-200 bg-red-50 p-6">
          <p className="text-base text-red-700">
            Failed to load resource allocations. Make sure the backend is
            running.
          </p>
        </div>
      </div>
    );
  }

  const totalPeople = resources.length;
  const overloadedCount = resources.filter(
    (r) => r.capacity_status.toLowerCase() === "overloaded",
  ).length;
  const avgUtilization =
    totalPeople > 0
      ? Math.round(
          resources.reduce(
            (sum, r) =>
              sum + r.allocations.reduce((s, a) => s + a.percentage, 0),
            0,
          ) / totalPeople,
        )
      : 0;

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold text-gray-900">
          Resource Allocation
        </h2>
        <p className="mt-1 text-base text-gray-500">
          Team capacity and workstream allocation overview
        </p>
      </div>

      <div className="grid grid-cols-1 gap-4 sm:grid-cols-3">
        <div className="rounded-lg border border-gray-200 bg-white p-5 shadow-sm">
          <div className="flex items-center gap-3">
            <div className="rounded-full bg-blue-50 p-2">
              <User className="h-5 w-5 text-blue-600" />
            </div>
            <div>
              <p className="text-2xl font-bold text-gray-900">{totalPeople}</p>
              <p className="text-base text-gray-500">Total People</p>
            </div>
          </div>
        </div>

        <div className="rounded-lg border border-gray-200 bg-white p-5 shadow-sm">
          <div className="flex items-center gap-3">
            <div
              className={`rounded-full p-2 ${overloadedCount > 0 ? "bg-red-50" : "bg-green-50"}`}
            >
              <AlertTriangle
                className={`h-5 w-5 ${overloadedCount > 0 ? "text-red-600" : "text-green-600"}`}
              />
            </div>
            <div>
              <p className="text-2xl font-bold text-gray-900">
                {overloadedCount}
              </p>
              <p className="text-base text-gray-500">Overloaded</p>
            </div>
          </div>
        </div>

        <div className="rounded-lg border border-gray-200 bg-white p-5 shadow-sm">
          <div className="flex items-center gap-3">
            <div className="rounded-full bg-indigo-50 p-2">
              <BarChart3 className="h-5 w-5 text-indigo-600" />
            </div>
            <div>
              <p className="text-2xl font-bold text-gray-900">
                {avgUtilization}%
              </p>
              <p className="text-base text-gray-500">Avg Utilization</p>
            </div>
          </div>
        </div>
      </div>

      {resources.length > 0 ? (
        <div className="grid grid-cols-1 gap-4 md:grid-cols-2 xl:grid-cols-3">
          {resources.map((r) => (
            <ResourceCard key={r.id} resource={r} />
          ))}
        </div>
      ) : (
        <div className="rounded-lg border border-gray-200 bg-white p-12 text-center shadow-sm">
          <User className="mx-auto h-10 w-10 text-gray-300" />
          <p className="mt-3 text-gray-500">
            No resource allocations found.
          </p>
          <p className="mt-1 text-base text-gray-400">
            Add resources via the API to see them here.
          </p>
        </div>
      )}
    </div>
  );
}
