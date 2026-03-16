"use client";

import Sparkline from "./Sparkline";
import type { KpiData } from "@/lib/types";
import {
  FileText,
  CheckSquare,
  ShieldAlert,
  Link2,
  Users,
  FolderKanban,
} from "lucide-react";

interface KpiTile {
  label: string;
  primary: number;
  sub: string;
  subColor?: string;
  sparkData: number[];
  sparkColor?: string;
  icon: React.ReactNode;
}

function buildTiles(kpi: KpiData): KpiTile[] {
  return [
    {
      label: "Transcripts",
      primary: kpi.total_transcripts,
      sub: `${kpi.transcripts_this_week} this week`,
      sparkData: kpi.weekly_transcript_counts,
      icon: <FileText className="h-4 w-4 text-forest-500" />,
    },
    {
      label: "Open Actions",
      primary: kpi.open_actions,
      sub: `${kpi.overdue_actions} overdue`,
      subColor: kpi.overdue_actions > 0 ? "text-red-600" : undefined,
      sparkData: kpi.weekly_open_action_counts,
      sparkColor: kpi.overdue_actions > 0 ? "#ef4444" : "#5B6D49",
      icon: <CheckSquare className="h-4 w-4 text-green-500" />,
    },
    {
      label: "Risks",
      primary: kpi.critical_high_risks,
      sub: `${kpi.escalating_risks} escalating`,
      subColor: kpi.escalating_risks > 0 ? "text-amber-600" : undefined,
      sparkData: kpi.weekly_risk_counts,
      sparkColor: "#f59e0b",
      icon: <ShieldAlert className="h-4 w-4 text-red-500" />,
    },
    {
      label: "Dependencies",
      primary: kpi.blocked_dependencies,
      sub: `${kpi.in_progress_dependencies} in progress`,
      sparkData: kpi.weekly_blocked_counts,
      sparkColor: "#8b5cf6",
      icon: <Link2 className="h-4 w-4 text-purple-500" />,
    },
    {
      label: "Utilization",
      primary: Math.round(kpi.avg_utilization),
      sub: `${kpi.overloaded_count} overloaded`,
      subColor: kpi.overloaded_count > 0 ? "text-red-600" : undefined,
      sparkData: kpi.weekly_utilization,
      icon: <Users className="h-4 w-4 text-indigo-500" />,
    },
    {
      label: "Projects",
      primary: kpi.total_projects,
      sub: `${kpi.active_projects} active`,
      sparkData: [],
      icon: <FolderKanban className="h-4 w-4 text-teal-500" />,
    },
  ];
}

interface Props {
  kpi: KpiData;
}

export default function KpiStrip({ kpi }: Props) {
  const tiles = buildTiles(kpi);

  return (
    <div className="grid grid-cols-2 gap-3 sm:grid-cols-3 lg:grid-cols-6">
      {tiles.map((tile) => (
        <div
          key={tile.label}
          className="rounded-lg border border-forest-200 bg-white dark:bg-forest-800 p-3"
        >
          <div className="flex items-center justify-between mb-1">
            <span className="text-[10px] font-semibold uppercase tracking-wider text-forest-400">
              {tile.label}
            </span>
            {tile.icon}
          </div>
          <div className="flex items-end justify-between">
            <div>
              <span className="text-xl font-bold text-forest-950">
                {tile.label === "Utilization" ? `${tile.primary}%` : tile.primary}
              </span>
              <p className={`text-[10px] mt-0.5 ${tile.subColor || "text-forest-400"}`}>
                {tile.sub}
              </p>
            </div>
            {tile.sparkData.length > 1 && (
              <Sparkline
                data={tile.sparkData}
                width={50}
                height={18}
                color={tile.sparkColor || "#5B6D49"}
              />
            )}
          </div>
        </div>
      ))}
    </div>
  );
}
