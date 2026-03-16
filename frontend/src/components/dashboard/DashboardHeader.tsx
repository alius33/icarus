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
  projects: { code: string; name: string }[];
}

export default function DashboardHeader({ projects }: Props) {
  const { filters, setTimeFilter, setProjectFilter } = useDashboardFilters();

  return (
    <div className="flex items-start justify-between flex-wrap gap-3">
      <div>
        <h2 className="text-2xl font-bold text-forest-950">
          Programme Dashboard
        </h2>
        <p className="mt-1 text-base text-forest-400">
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
          className="rounded-md border border-forest-200 bg-white dark:bg-forest-800 px-3 py-1.5 text-base text-forest-600 focus:outline-none focus:ring-1 focus:ring-forest-500"
        >
          {TIME_OPTIONS.map((opt) => (
            <option key={opt.value} value={opt.value}>
              {opt.label}
            </option>
          ))}
        </select>

        {/* Project filter */}
        <select
          value={filters.projectFilter || ""}
          onChange={(e) =>
            setProjectFilter(e.target.value || null)
          }
          className="rounded-md border border-forest-200 bg-white dark:bg-forest-800 px-3 py-1.5 text-base text-forest-600 focus:outline-none focus:ring-1 focus:ring-forest-500"
        >
          <option value="">All Projects</option>
          {projects.map((p) => (
            <option key={p.code} value={p.code}>
              {p.name}
            </option>
          ))}
        </select>

        <CopyBriefButton />
      </div>
    </div>
  );
}
