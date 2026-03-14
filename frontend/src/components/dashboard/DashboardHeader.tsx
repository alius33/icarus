"use client";

import { useDashboardFilters } from "./hooks/useDashboardFilters";
import CopyBriefButton from "./CopyBriefButton";
import type { TimeFilter } from "@/lib/types";

const TIME_OPTIONS: { value: TimeFilter; label: string }[] = [
  { value: "1w", label: "This Week" },
  { value: "2w", label: "Last 2 Weeks" },
  { value: "1m", label: "This Month" },
  { value: "all", label: "All Time" },
];

interface Props {
  workstreams: { code: string; name: string }[];
}

export default function DashboardHeader({ workstreams }: Props) {
  const { filters, setTimeFilter, setWorkstreamFilter } = useDashboardFilters();

  return (
    <div className="flex items-start justify-between flex-wrap gap-3">
      <div>
        <h2 className="text-2xl font-bold text-gray-900">
          Programme Dashboard
        </h2>
        <p className="mt-1 text-base text-gray-500">
          Gen AI Programme &middot; Updated{" "}
          {new Date().toLocaleDateString("en-GB", {
            day: "numeric",
            month: "short",
            year: "numeric",
          })}
        </p>
      </div>

      <div className="flex items-center gap-3">
        {/* Time filter */}
        <select
          value={filters.timeFilter}
          onChange={(e) => setTimeFilter(e.target.value as TimeFilter)}
          className="rounded-md border border-gray-300 bg-white px-3 py-1.5 text-base text-gray-700 focus:outline-none focus:ring-1 focus:ring-blue-500"
        >
          {TIME_OPTIONS.map((opt) => (
            <option key={opt.value} value={opt.value}>
              {opt.label}
            </option>
          ))}
        </select>

        {/* Project filter */}
        <select
          value={filters.workstreamFilter || ""}
          onChange={(e) =>
            setWorkstreamFilter(e.target.value || null)
          }
          className="rounded-md border border-gray-300 bg-white px-3 py-1.5 text-base text-gray-700 focus:outline-none focus:ring-1 focus:ring-blue-500"
        >
          <option value="">All Projects</option>
          {workstreams.map((ws) => (
            <option key={ws.code} value={ws.code}>
              {ws.name}
            </option>
          ))}
        </select>

        <CopyBriefButton />
      </div>
    </div>
  );
}
