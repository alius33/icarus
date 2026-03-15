"use client";

import { useState } from "react";
import { useProgrammeDeliverables } from "@/lib/swr";
import { RAG_CONFIG, MILESTONE_STATUS_CONFIG, type ProgrammeDeliverable, type DeliverableMilestone } from "@/lib/types";
import { cn } from "@/lib/utils";
import { ChevronDown, ChevronRight, Check, Clock, AlertCircle, Minus } from "lucide-react";

const PROGRAMME_START = new Date(2026, 1, 23);
const TOTAL_WEEKS = 12;

function getCurrentWeekNumber(): number {
  const now = new Date();
  const diff = now.getTime() - PROGRAMME_START.getTime();
  if (diff < 0) return 0;
  return Math.min(Math.floor(diff / (7 * 24 * 60 * 60 * 1000)) + 1, TOTAL_WEEKS + 1);
}

function WeekTimeline() {
  const currentWeek = getCurrentWeekNumber();
  return (
    <div className="rounded-lg border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 p-4">
      <div className="flex items-center justify-between text-xs text-gray-400 mb-2">
        <span>23 Feb</span>
        <span className="font-medium text-gray-900 dark:text-white">Week {Math.min(currentWeek, TOTAL_WEEKS)} of {TOTAL_WEEKS}</span>
        <span>15 May</span>
      </div>
      <div className="flex gap-0.5">
        {Array.from({ length: TOTAL_WEEKS }, (_, i) => {
          const weekNum = i + 1;
          const isPast = weekNum < currentWeek;
          const isCurrent = weekNum === currentWeek;
          return (
            <div
              key={weekNum}
              className={cn(
                "h-3 flex-1 rounded-sm transition-colors",
                isPast ? "bg-green-600" : isCurrent ? "bg-blue-500" : "bg-gray-200 dark:bg-gray-700"
              )}
              title={`Week ${weekNum}`}
            />
          );
        })}
      </div>
      <div className="flex items-center gap-4 mt-2 text-[10px] text-gray-500">
        <span className="flex items-center gap-1"><span className="h-2 w-2 rounded-sm bg-green-600" /> Completed</span>
        <span className="flex items-center gap-1"><span className="h-2 w-2 rounded-sm bg-blue-500" /> Current</span>
        <span className="flex items-center gap-1"><span className="h-2 w-2 rounded-sm bg-gray-200 dark:bg-gray-700" /> Remaining</span>
      </div>
    </div>
  );
}

function MilestoneStatusIcon({ status }: { status: string }) {
  switch (status) {
    case "COMPLETED": return <Check className="h-3.5 w-3.5 text-green-500" />;
    case "IN_PROGRESS": return <Clock className="h-3.5 w-3.5 text-blue-500" />;
    case "BLOCKED": return <AlertCircle className="h-3.5 w-3.5 text-red-500" />;
    default: return <Minus className="h-3.5 w-3.5 text-gray-500" />;
  }
}

function MilestoneRow({ milestone }: { milestone: DeliverableMilestone }) {
  const cfg = MILESTONE_STATUS_CONFIG[milestone.status as keyof typeof MILESTONE_STATUS_CONFIG] || MILESTONE_STATUS_CONFIG.NOT_STARTED;
  return (
    <div className="flex items-start gap-3 py-2 px-3 rounded hover:bg-gray-100 dark:hover:bg-gray-800/50">
      <MilestoneStatusIcon status={milestone.status} />
      <div className="flex-1 min-w-0">
        <p className="text-sm text-gray-700 dark:text-gray-200">{milestone.title}</p>
        {milestone.evidence && (
          <p className="text-xs text-gray-500 mt-0.5">{milestone.evidence}</p>
        )}
      </div>
      <div className="flex items-center gap-2 flex-shrink-0">
        {milestone.target_week && (
          <span className="text-[10px] text-gray-500">Wk {milestone.target_week}</span>
        )}
        <span className={cn("text-[10px] px-1.5 py-0.5 rounded", cfg.bgColor, cfg.color)}>
          {cfg.label}
        </span>
      </div>
    </div>
  );
}

function DeliverableRow({ deliverable }: { deliverable: ProgrammeDeliverable }) {
  const [expanded, setExpanded] = useState(false);
  const ragCfg = RAG_CONFIG[deliverable.rag_status] || RAG_CONFIG.GREEN;
  const totalMs = deliverable.milestones.length;
  const completedMs = deliverable.milestones.filter(m => m.status === "COMPLETED").length;

  return (
    <div className="border-t border-gray-200 dark:border-gray-700/50 first:border-t-0">
      <button
        onClick={() => setExpanded(!expanded)}
        className="flex items-center gap-3 w-full px-4 py-3 text-left hover:bg-gray-800/30 transition-colors"
      >
        {expanded ? <ChevronDown className="h-4 w-4 text-gray-400" /> : <ChevronRight className="h-4 w-4 text-gray-400" />}
        <span className={cn("h-2 w-2 rounded-full flex-shrink-0", ragCfg.dotColor)} />
        <span className="text-sm text-gray-700 dark:text-gray-200 flex-1 truncate">{deliverable.title}</span>
        <span className="text-xs text-gray-500">{completedMs}/{totalMs}</span>
        <div className="w-20 h-1.5 rounded-full bg-gray-200 dark:bg-gray-700 flex-shrink-0">
          <div
            className={cn("h-1.5 rounded-full", deliverable.rag_status === "RED" ? "bg-red-500" : deliverable.rag_status === "AMBER" ? "bg-amber-500" : "bg-green-500")}
            style={{ width: `${totalMs > 0 ? (completedMs / totalMs) * 100 : 0}%` }}
          />
        </div>
      </button>
      {expanded && deliverable.milestones.length > 0 && (
        <div className="pl-8 pr-4 pb-3 space-y-0.5">
          {deliverable.milestones.map((m) => (
            <MilestoneRow key={m.id} milestone={m} />
          ))}
        </div>
      )}
    </div>
  );
}

function PillarSection({ deliverables }: { deliverables: ProgrammeDeliverable[] }) {
  const [collapsed, setCollapsed] = useState(false);
  if (!deliverables.length) return null;

  const pillarName = deliverables[0].pillar_name;
  const avgProgress = Math.round(deliverables.reduce((sum, d) => sum + d.progress_percent, 0) / deliverables.length);
  const hasRed = deliverables.some(d => d.rag_status === "RED");
  const hasAmber = deliverables.some(d => d.rag_status === "AMBER");
  const rag = hasRed ? "RED" : hasAmber ? "AMBER" : "GREEN";
  const ragCfg = RAG_CONFIG[rag] || RAG_CONFIG.GREEN;

  return (
    <div className="rounded-lg border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 overflow-hidden">
      <button
        onClick={() => setCollapsed(!collapsed)}
        className="flex items-center gap-3 w-full px-4 py-3 hover:bg-gray-100 dark:hover:bg-gray-750 transition-colors"
      >
        {collapsed ? <ChevronRight className="h-4 w-4 text-gray-400" /> : <ChevronDown className="h-4 w-4 text-gray-400" />}
        <span className={cn("h-2.5 w-2.5 rounded-full", ragCfg.dotColor)} />
        <h3 className="text-sm font-semibold text-gray-900 dark:text-white flex-1 text-left">{pillarName}</h3>
        <span className={cn("text-xs px-2 py-0.5 rounded-full", ragCfg.bgColor, ragCfg.color)}>
          {ragCfg.label}
        </span>
        <div className="w-24 h-2 rounded-full bg-gray-200 dark:bg-gray-700">
          <div
            className={cn("h-2 rounded-full", rag === "RED" ? "bg-red-500" : rag === "AMBER" ? "bg-amber-500" : "bg-green-500")}
            style={{ width: `${avgProgress}%` }}
          />
        </div>
        <span className="text-xs text-gray-500 w-10 text-right">{avgProgress}%</span>
      </button>
      {!collapsed && (
        <div>
          {deliverables.map((d) => (
            <DeliverableRow key={d.id} deliverable={d} />
          ))}
        </div>
      )}
    </div>
  );
}

export default function DeliverablesTab() {
  const { data: deliverables } = useProgrammeDeliverables();

  if (!deliverables) {
    return <div className="text-gray-400">Loading deliverables...</div>;
  }

  const pillarGroups: Record<number, ProgrammeDeliverable[]> = {};
  deliverables.forEach(d => {
    (pillarGroups[d.pillar] ||= []).push(d);
  });

  return (
    <div className="space-y-6">
      <WeekTimeline />
      <div className="space-y-4">
        {[1, 2, 3].map(pillar => (
          <PillarSection
            key={pillar}
            deliverables={pillarGroups[pillar] || []}
          />
        ))}
      </div>
    </div>
  );
}
