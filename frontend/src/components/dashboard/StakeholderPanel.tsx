"use client";

import type { StakeholderEngagementItem } from "@/lib/types";
import { Users } from "lucide-react";

function TrendLabel({ trend }: { trend: "rising" | "stable" | "declining" | "silent" }) {
  const colors: Record<string, string> = {
    rising: "text-green-600",
    stable: "text-gray-500",
    declining: "text-amber-600",
    silent: "text-red-500",
  };
  return (
    <span className={`text-[10px] font-medium ${colors[trend] || "text-gray-400"}`}>
      {trend}
    </span>
  );
}

function EngagementBar({
  recent,
  previous,
  max,
}: {
  recent: number;
  previous: number;
  max: number;
}) {
  const pctRecent = max > 0 ? Math.min((recent / max) * 100, 100) : 0;
  const pctPrev = max > 0 ? Math.min((previous / max) * 100, 100) : 0;
  return (
    <div className="flex items-center gap-1.5 w-24">
      <div className="relative h-2 flex-1 rounded-full bg-gray-100">
        <div
          className="absolute inset-y-0 left-0 rounded-full bg-gray-300"
          style={{ width: `${pctPrev}%` }}
        />
        <div
          className="absolute inset-y-0 left-0 rounded-full bg-blue-500"
          style={{ width: `${pctRecent}%` }}
        />
      </div>
      <span className="text-[10px] font-medium text-gray-500 tabular-nums w-4 text-right">
        {recent}
      </span>
    </div>
  );
}

interface Props {
  items: StakeholderEngagementItem[];
  onItemClick?: (item: StakeholderEngagementItem) => void;
}

export default function StakeholderPanel({ items, onItemClick }: Props) {
  const maxMentions = Math.max(
    ...items.map((s) => Math.max(s.recent_mentions, s.previous_mentions, 1)),
    1,
  );

  return (
    <div>
      <h4 className="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-3 flex items-center gap-1.5">
        <Users className="h-3.5 w-3.5" />
        Stakeholder Engagement
      </h4>
      {items.length === 0 ? (
        <p className="text-sm text-gray-500">No tier 1-2 stakeholder data.</p>
      ) : (
        <div className="space-y-2.5">
          {items.map((s) => (
            <button
              key={s.id}
              onClick={() => onItemClick?.(s)}
              className="flex items-center gap-3 w-full text-left group"
            >
              <div className="flex-1 min-w-0">
                <div className="flex items-center gap-2">
                  <span className="text-sm font-medium text-gray-900 group-hover:text-blue-700 truncate">
                    {s.name}
                  </span>
                  <span className="inline-flex items-center rounded bg-blue-50 px-1.5 py-0.5 text-[10px] font-medium text-blue-700">
                    T{s.tier}
                  </span>
                </div>
                {s.role && (
                  <p className="text-[10px] text-gray-400 truncate">{s.role}</p>
                )}
              </div>
              <EngagementBar
                recent={s.recent_mentions}
                previous={s.previous_mentions}
                max={maxMentions}
              />
              <TrendLabel trend={s.trend} />
            </button>
          ))}
        </div>
      )}
    </div>
  );
}
