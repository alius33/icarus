"use client";

import { useMemo } from "react";
import { DecisionTimelineItem, DECISION_STATUS_CONFIG, DecisionStatus } from "@/lib/types";

interface DecisionTimelineProps {
  decisions: DecisionTimelineItem[];
  onDecisionClick: (decisionId: number) => void;
}

function addDays(date: Date, days: number): Date {
  const d = new Date(date);
  d.setDate(d.getDate() + days);
  return d;
}

function diffDays(a: Date, b: Date): number {
  return Math.round((b.getTime() - a.getTime()) / (1000 * 60 * 60 * 24));
}

function startOfWeek(date: Date): Date {
  const d = new Date(date);
  const day = d.getDay();
  d.setDate(d.getDate() - (day === 0 ? 6 : day - 1));
  d.setHours(0, 0, 0, 0);
  return d;
}

export default function DecisionTimeline({ decisions, onDecisionClick }: DecisionTimelineProps) {
  const today = useMemo(() => new Date(), []);

  // Filter to decisions that have dates
  const datedDecisions = useMemo(
    () => decisions.filter((d) => d.decision_date),
    [decisions]
  );

  // Compute timeline range
  const { startDate, endDate, weeks } = useMemo(() => {
    if (datedDecisions.length === 0) {
      const s = startOfWeek(today);
      const e = addDays(s, 28);
      return { startDate: s, endDate: e, weeks: 4 };
    }

    let minDate = new Date(today);
    let maxDate = new Date(today);

    datedDecisions.forEach((d) => {
      const dd = new Date(d.decision_date!);
      if (dd < minDate) minDate = dd;
      if (dd > maxDate) maxDate = dd;
    });

    const s = startOfWeek(addDays(minDate, -7));
    const e = addDays(startOfWeek(maxDate), 14);
    const w = Math.max(4, Math.ceil(diffDays(s, e) / 7));
    return { startDate: s, endDate: e, weeks: w };
  }, [datedDecisions, today]);

  const totalDays = diffDays(startDate, endDate);
  const todayOffset = Math.max(0, diffDays(startDate, today));

  // Week labels
  const weekLabels = useMemo(() => {
    const labels: { label: string; offset: number }[] = [];
    for (let i = 0; i < weeks; i++) {
      const d = addDays(startDate, i * 7);
      labels.push({
        label: d.toLocaleDateString("en-GB", { day: "numeric", month: "short" }),
        offset: i * 7,
      });
    }
    return labels;
  }, [startDate, weeks]);

  if (datedDecisions.length === 0) {
    return (
      <div className="flex items-center justify-center py-12 text-forest-300 text-base">
        No decisions with dates to show on timeline. Add dates to see decisions here.
      </div>
    );
  }

  return (
    <div className="border border-forest-200 dark:border-forest-700 rounded-lg overflow-hidden">
      {/* Header: week columns */}
      <div className="flex bg-forest-50 dark:bg-forest-800 border-b border-forest-200 dark:border-forest-700">
        <div className="w-64 shrink-0 px-3 py-2 text-sm font-medium text-forest-400 dark:text-forest-300 border-r border-forest-200 dark:border-forest-700">
          Decision
        </div>
        <div className="flex-1 relative">
          <div className="flex" style={{ width: `${weeks * 120}px` }}>
            {weekLabels.map((wl, i) => (
              <div
                key={i}
                className="text-sm text-forest-300 px-2 py-2 border-r border-forest-200 dark:border-forest-700"
                style={{ width: "120px" }}
              >
                {wl.label}
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Rows */}
      <div className="relative overflow-x-auto">
        {datedDecisions.map((decision) => {
          const decisionDate = new Date(decision.decision_date!);
          const dayOffset = Math.max(0, diffDays(startDate, decisionDate));
          const leftPct = (dayOffset / totalDays) * 100;

          const statusCfg = DECISION_STATUS_CONFIG[decision.execution_status as DecisionStatus];
          const markerColor = statusCfg?.bgColor ?? "bg-gray-200";
          const borderColor = statusCfg?.color ?? "text-forest-500";

          return (
            <div key={decision.id} className="flex border-b border-gray-100 dark:border-forest-700 hover:bg-forest-50 dark:hover:bg-forest-700/30">
              {/* Decision label */}
              <div
                className="w-64 shrink-0 px-3 py-2 border-r border-forest-200 dark:border-forest-700 cursor-pointer"
                onClick={() => onDecisionClick(decision.id)}
              >
                <div className="min-w-0">
                  <p className="text-base text-forest-950 dark:text-forest-50 truncate">{decision.title}</p>
                  <div className="flex items-center gap-2 mt-0.5">
                    <span className="text-sm font-mono text-forest-300">#{decision.number}</span>
                    {decision.key_people.length > 0 && (
                      <span className="text-sm text-forest-300 truncate">
                        {decision.key_people.slice(0, 2).join(", ")}
                        {decision.key_people.length > 2 && ` +${decision.key_people.length - 2}`}
                      </span>
                    )}
                    {statusCfg && (
                      <span className={`text-sm font-medium px-1 py-0.5 rounded ${statusCfg.bgColor} ${statusCfg.color}`}>
                        {statusCfg.label}
                      </span>
                    )}
                  </div>
                </div>
              </div>

              {/* Marker area */}
              <div className="flex-1 relative py-1.5" style={{ minWidth: `${weeks * 120}px` }}>
                {/* Week gridlines */}
                {weekLabels.map((_, i) => (
                  <div
                    key={i}
                    className="absolute top-0 bottom-0 border-r border-gray-100 dark:border-forest-700"
                    style={{ left: `${((i * 7) / totalDays) * 100}%` }}
                  />
                ))}

                {/* Today marker */}
                <div
                  className="absolute top-0 bottom-0 w-px bg-red-400 z-10"
                  style={{ left: `${(todayOffset / totalDays) * 100}%` }}
                />

                {/* Diamond marker at decision date */}
                <div
                  className={`absolute top-1/2 -translate-y-1/2 -translate-x-1/2 w-4 h-4 rotate-45 ${markerColor} border-2 ${borderColor} cursor-pointer z-20`}
                  style={{ left: `${leftPct}%` }}
                  onClick={() => onDecisionClick(decision.id)}
                  title={`${decision.title} (${decision.decision_date})`}
                />
              </div>
            </div>
          );
        })}

        {/* Today line in header area */}
        <div
          className="absolute top-0 h-full w-px bg-red-400 z-20 pointer-events-none"
          style={{ left: `calc(256px + ${(todayOffset / totalDays) * 100}%)` }}
        />
      </div>
    </div>
  );
}
