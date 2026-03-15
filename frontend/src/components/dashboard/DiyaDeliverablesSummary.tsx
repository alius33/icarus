"use client";

import Link from "next/link";
import { useDeliverableOverview } from "@/lib/swr";
import { cn } from "@/lib/utils";

const RAG_COLORS: Record<string, string> = {
  GREEN: "bg-green-500",
  AMBER: "bg-amber-500",
  RED: "bg-red-500",
};

export default function DiyaDeliverablesSummary() {
  const { data, isLoading } = useDeliverableOverview();

  if (isLoading) {
    return (
      <div className="rounded-xl border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 p-5 animate-pulse">
        <div className="h-5 w-48 bg-gray-200 dark:bg-gray-700 rounded mb-4" />
        <div className="space-y-3">
          {[1, 2, 3].map((i) => (
            <div key={i} className="h-16 bg-gray-100 dark:bg-gray-700 rounded-lg" />
          ))}
        </div>
      </div>
    );
  }

  if (!data?.pillars?.length) return null;

  return (
    <div className="rounded-xl border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 p-5">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-sm font-semibold text-gray-900 dark:text-white uppercase tracking-wide">
          Diya Deliverables
        </h3>
        <Link
          href="/weekly-plan?tab=deliverables"
          className="text-xs text-blue-600 dark:text-blue-400 hover:underline"
        >
          View details &rarr;
        </Link>
      </div>
      <div className="space-y-3">
        {data.pillars.map((pillar) => {
          const totalMilestones = pillar.deliverables.reduce(
            (sum, d) => sum + (d.milestones?.length || 0),
            0
          );
          const completedMilestones = pillar.deliverables.reduce(
            (sum, d) =>
              sum +
              (d.milestones?.filter((m) => m.status === "COMPLETED").length || 0),
            0
          );

          return (
            <div
              key={pillar.pillar}
              className="flex items-center gap-3 rounded-lg bg-gray-50 dark:bg-gray-700/50 p-3"
            >
              <div
                className={cn(
                  "h-3 w-3 rounded-full flex-shrink-0",
                  RAG_COLORS[pillar.aggregate_rag] || "bg-gray-400"
                )}
              />
              <div className="flex-1 min-w-0">
                <p className="text-sm font-medium text-gray-900 dark:text-white truncate">
                  {pillar.pillar_name}
                </p>
                <div className="mt-1 flex items-center gap-2">
                  <div className="flex-1 h-1.5 bg-gray-200 dark:bg-gray-600 rounded-full overflow-hidden">
                    <div
                      className="h-full bg-blue-500 rounded-full transition-all"
                      style={{ width: `${pillar.aggregate_progress}%` }}
                    />
                  </div>
                  <span className="text-xs text-gray-500 dark:text-gray-400 tabular-nums whitespace-nowrap">
                    {completedMilestones}/{totalMilestones}
                  </span>
                </div>
              </div>
              <span className="text-xs font-medium text-gray-500 dark:text-gray-400 tabular-nums">
                {pillar.aggregate_progress}%
              </span>
            </div>
          );
        })}
      </div>
    </div>
  );
}
