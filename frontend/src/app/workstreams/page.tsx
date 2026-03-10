import Link from "next/link";
import { api } from "@/lib/api";
import { getStatusColor } from "@/lib/utils";
import { AlertTriangle, Users, Activity } from "lucide-react";

export default async function WorkstreamsPage() {
  const workstreams = await api.getWorkstreams();

  const blockedCount = workstreams.filter(
    (ws) => ws.status.toLowerCase().includes("stalled") || ws.blocker_reason
  ).length;

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold text-gray-900">Workstreams</h2>
          <p className="mt-1 text-sm text-gray-500">
            {workstreams.length} programme workstreams
            {blockedCount > 0 && (
              <span className="ml-2 text-amber-600 font-medium">
                ({blockedCount} blocked/stalled)
              </span>
            )}
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 gap-6 md:grid-cols-2">
        {workstreams.map((ws) => {
          const isBlocked =
            ws.status.toLowerCase().includes("stalled") || !!ws.blocker_reason;

          return (
            <Link
              key={ws.id}
              href={`/workstreams/${ws.id}`}
              className={`block rounded-lg border bg-white p-6 shadow-sm transition-shadow hover:shadow-md ${
                isBlocked
                  ? "border-amber-300 bg-amber-50/30"
                  : "border-gray-200"
              }`}
            >
              <div className="mb-3 flex items-center justify-between">
                <span className="inline-flex items-center rounded-md bg-blue-100 px-2.5 py-0.5 text-xs font-semibold text-blue-800">
                  {ws.code}
                </span>
                <div className="flex items-center gap-2">
                  {isBlocked && (
                    <AlertTriangle className="h-4 w-4 text-amber-500" />
                  )}
                  <span
                    className={`inline-flex items-center rounded-full border px-2.5 py-0.5 text-xs font-medium ${getStatusColor(ws.status)}`}
                  >
                    {ws.status}
                  </span>
                </div>
              </div>

              <h3 className="text-lg font-semibold text-gray-900">{ws.name}</h3>

              <div className="mt-2 flex flex-wrap items-center gap-3">
                {ws.owner && (
                  <span className="flex items-center gap-1 text-sm text-gray-500">
                    <Users className="h-3.5 w-3.5" />
                    {ws.owner}
                  </span>
                )}
                {ws.assigned_fte && (
                  <span className="flex items-center gap-1 text-sm text-gray-500">
                    <Activity className="h-3.5 w-3.5" />
                    {ws.assigned_fte} FTE
                  </span>
                )}
              </div>

              {ws.blocker_reason && (
                <div className="mt-3 rounded-md border border-amber-200 bg-amber-50 px-3 py-2">
                  <p className="text-xs font-medium text-amber-800">Blocked</p>
                  <p className="text-xs text-amber-700">{ws.blocker_reason}</p>
                </div>
              )}

              {ws.progress_pct !== null && (
                <div className="mt-3">
                  <div className="flex items-center justify-between text-xs text-gray-500">
                    <span>Progress</span>
                    <span>{ws.progress_pct}%</span>
                  </div>
                  <div className="mt-1 h-1.5 w-full rounded-full bg-gray-200">
                    <div
                      className="h-1.5 rounded-full bg-blue-600"
                      style={{ width: `${ws.progress_pct}%` }}
                    />
                  </div>
                </div>
              )}
            </Link>
          );
        })}
      </div>
    </div>
  );
}
