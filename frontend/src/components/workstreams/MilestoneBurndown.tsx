"use client";

import type { MilestoneSchema } from "@/lib/types";
import { formatDate } from "@/lib/utils";
import { CheckCircle2, Clock, X, ArrowRight } from "lucide-react";

interface Props {
  milestones: MilestoneSchema[];
}

const statusConfig: Record<
  string,
  { icon: React.ReactNode; color: string; bgColor: string }
> = {
  completed: {
    icon: <CheckCircle2 className="h-4 w-4" />,
    color: "text-green-600",
    bgColor: "bg-green-500",
  },
  planned: {
    icon: <Clock className="h-4 w-4" />,
    color: "text-blue-600",
    bgColor: "bg-blue-500",
  },
  missed: {
    icon: <X className="h-4 w-4" />,
    color: "text-red-600",
    bgColor: "bg-red-500",
  },
  deferred: {
    icon: <ArrowRight className="h-4 w-4" />,
    color: "text-gray-500",
    bgColor: "bg-gray-400",
  },
};

export default function MilestoneBurndown({ milestones }: Props) {
  if (milestones.length === 0) {
    return (
      <p className="text-base text-gray-500">No milestones tracked.</p>
    );
  }

  const sorted = [...milestones].sort((a, b) => {
    if (!a.target_date) return 1;
    if (!b.target_date) return -1;
    return a.target_date.localeCompare(b.target_date);
  });

  const completed = sorted.filter((m) => m.status === "completed").length;
  const total = sorted.length;
  const pct = total > 0 ? Math.round((completed / total) * 100) : 0;

  return (
    <div>
      {/* Progress bar */}
      <div className="mb-4">
        <div className="flex items-center justify-between mb-1">
          <span className="text-sm font-medium text-gray-600">
            Milestone Progress
          </span>
          <span className="text-sm font-semibold text-gray-900">
            {completed}/{total} ({pct}%)
          </span>
        </div>
        <div className="relative h-2.5 w-full rounded-full bg-gray-100">
          <div
            className="absolute inset-y-0 left-0 rounded-full bg-green-500 transition-all"
            style={{ width: `${pct}%` }}
          />
        </div>
      </div>

      {/* Timeline */}
      <div className="space-y-0">
        {sorted.map((m, i) => {
          const config = statusConfig[m.status] || statusConfig.planned;
          const isLast = i === sorted.length - 1;

          return (
            <div key={m.id} className="flex gap-3">
              {/* Timeline dot + line */}
              <div className="flex flex-col items-center">
                <div
                  className={`h-3 w-3 rounded-full ${config.bgColor} flex-shrink-0 mt-1`}
                />
                {!isLast && (
                  <div className="w-0.5 flex-1 bg-gray-200 min-h-[24px]" />
                )}
              </div>

              {/* Content */}
              <div className="flex-1 pb-3 min-w-0">
                <div className="flex items-start gap-2">
                  <span className={`${config.color} flex-shrink-0 mt-0.5`}>
                    {config.icon}
                  </span>
                  <div className="flex-1 min-w-0">
                    <p className="text-base text-gray-900">
                      {m.title || m.notes || "Milestone"}
                    </p>
                    <div className="flex items-center gap-2 mt-0.5">
                      {m.target_date && (
                        <span className="text-[10px] text-gray-500">
                          {formatDate(m.target_date)}
                        </span>
                      )}
                      <span
                        className={`text-[10px] font-medium ${config.color}`}
                      >
                        {m.status}
                      </span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
