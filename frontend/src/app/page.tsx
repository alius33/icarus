import { api } from "@/lib/api";
import DashboardClient from "@/components/dashboard/DashboardClient";
import type { DashboardDataV2 } from "@/lib/types";

export default async function DashboardPage() {
  let data: DashboardDataV2 | null = null;
  let error: string | null = null;

  try {
    const raw = await api.getDashboard();
    // The backend now returns the V2 shape with programme_status, kpi, insights.
    // For backwards compatibility, provide defaults if fields are missing.
    data = {
      ...raw,
      programme_status: (raw as DashboardDataV2).programme_status ?? {
        narrative: "Dashboard data loaded. Health computation pending backend update.",
        health_rag: "amber" as const,
        biggest_win: null,
        biggest_risk: null,
        open_actions: raw.open_actions,
        overdue_count: raw.needs_attention.filter((i) => i.reason === "overdue").length,
        critical_risks: raw.needs_attention.filter((i) => i.reason === "critical_risk").length,
      },
      kpi: (raw as DashboardDataV2).kpi ?? {
        total_transcripts: raw.total_transcripts,
        transcripts_this_week: 0,
        weekly_transcript_counts: [],
        open_actions: raw.open_actions,
        overdue_actions: raw.needs_attention.filter((i) => i.reason === "overdue").length,
        weekly_open_action_counts: [],
        critical_high_risks: raw.critical_threads,
        escalating_risks: 0,
        weekly_risk_counts: [],
        blocked_dependencies: 0,
        in_progress_dependencies: 0,
        weekly_blocked_counts: [],
        avg_utilization: 0,
        overloaded_count: 0,
        weekly_utilization: [],
        total_projects: raw.projects.length,
        active_projects: raw.projects.filter((p) =>
          ["LIVE", "ACTIVE", "active"].some((s) => p.status.toUpperCase().includes(s)),
        ).length,
      },
      insights: (raw as DashboardDataV2).insights ?? {
        action_completion_rate: 0,
        decision_velocity: 0,
        scope_creep_pct: 0,
        risk_velocity: 0,
        overdue_sla_pct: 0,
      },
    };
  } catch (e) {
    error = e instanceof Error ? e.message : "Failed to load dashboard data";
  }

  if (error || !data) {
    return (
      <div className="space-y-6">
        <div>
          <h2 className="text-2xl font-bold text-gray-900">
            Programme Dashboard
          </h2>
          <p className="mt-1 text-base text-gray-500">
            Gen AI Programme overview and status.
          </p>
        </div>
        <div className="rounded-lg border border-red-200 bg-red-50 p-6">
          <p className="text-base text-red-700">
            {error || "Unable to load dashboard data. Please try again later."}
          </p>
        </div>
      </div>
    );
  }

  return <DashboardClient initialData={data} />;
}
