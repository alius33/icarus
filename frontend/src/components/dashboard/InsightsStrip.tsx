"use client";

import type { InsightsData } from "@/lib/types";

interface InsightMetric {
  label: string;
  value: string;
  dotColor: string;
}

function buildMetrics(insights: InsightsData): InsightMetric[] {
  const completionDot =
    insights.action_completion_rate >= 70
      ? "bg-green-500"
      : insights.action_completion_rate >= 40
        ? "bg-amber-500"
        : "bg-red-500";

  const overdueDot =
    insights.overdue_sla_pct <= 10
      ? "bg-green-500"
      : insights.overdue_sla_pct <= 25
        ? "bg-amber-500"
        : "bg-red-500";

  const riskVelDot =
    insights.risk_velocity <= 0
      ? "bg-green-500"
      : insights.risk_velocity <= 2
        ? "bg-amber-500"
        : "bg-red-500";

  return [
    {
      label: "Action Completion",
      value: `${Math.round(insights.action_completion_rate)}%`,
      dotColor: completionDot,
    },
    {
      label: "Decision Velocity",
      value: insights.decision_velocity >= 0
        ? `+${insights.decision_velocity}`
        : `${insights.decision_velocity}`,
      dotColor: insights.decision_velocity >= 0 ? "bg-green-500" : "bg-amber-500",
    },
    {
      label: "Scope Creep",
      value: `${Math.round(insights.scope_creep_pct)}%`,
      dotColor:
        insights.scope_creep_pct <= 15
          ? "bg-green-500"
          : insights.scope_creep_pct <= 30
            ? "bg-amber-500"
            : "bg-red-500",
    },
    {
      label: "Risk Velocity",
      value: insights.risk_velocity >= 0
        ? `+${insights.risk_velocity}`
        : `${insights.risk_velocity}`,
      dotColor: riskVelDot,
    },
    {
      label: "Overdue SLA",
      value: `${Math.round(insights.overdue_sla_pct)}%`,
      dotColor: overdueDot,
    },
  ];
}

interface Props {
  insights: InsightsData;
}

export default function InsightsStrip({ insights }: Props) {
  const metrics = buildMetrics(insights);

  return (
    <div className="flex flex-wrap items-center gap-4 rounded-lg border border-gray-100 bg-gray-50/50 px-4 py-2.5">
      <span className="text-[10px] font-semibold uppercase tracking-wider text-gray-400">
        Insights
      </span>
      {metrics.map((m) => (
        <div key={m.label} className="flex items-center gap-1.5">
          <span className={`h-2 w-2 rounded-full ${m.dotColor}`} />
          <span className="text-sm text-gray-600">
            {m.label}:{" "}
            <span className="font-semibold text-gray-900">{m.value}</span>
          </span>
        </div>
      ))}
    </div>
  );
}
