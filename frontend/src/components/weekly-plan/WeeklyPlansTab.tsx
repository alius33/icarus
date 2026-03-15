"use client";

import { useState, useMemo, useCallback } from "react";
import { useWeeklyPlans, useWeeklyPlan, useProgrammeDeliverables } from "@/lib/swr";
import { api } from "@/lib/api";
import { RAG_CONFIG, type WeeklyPlanAction, type ProgrammeDeliverable } from "@/lib/types";
import { cn } from "@/lib/utils";
import { Sparkles, ChevronDown } from "lucide-react";

const PROGRAMME_START = new Date(2026, 1, 23); // 23 Feb 2026 (month is 0-indexed)

function getWeekDates(weekNum: number): { start: Date; end: Date } {
  const start = new Date(PROGRAMME_START);
  start.setDate(start.getDate() + (weekNum - 1) * 7);
  const end = new Date(start);
  end.setDate(end.getDate() + 4); // Friday
  return { start, end };
}

function formatShortDate(d: Date): string {
  return d.toLocaleDateString("en-GB", { day: "numeric", month: "short" });
}

function getCurrentWeekNumber(): number {
  const now = new Date();
  const diff = now.getTime() - PROGRAMME_START.getTime();
  if (diff < 0) return 1;
  return Math.floor(diff / (7 * 24 * 60 * 60 * 1000)) + 1;
}

function PillarProgressCard({ deliverables }: { deliverables: ProgrammeDeliverable[] }) {
  if (!deliverables.length) return null;
  const pillarName = deliverables[0].pillar_name;
  const avgProgress = Math.round(deliverables.reduce((sum, d) => sum + d.progress_percent, 0) / deliverables.length);
  const totalMilestones = deliverables.reduce((sum, d) => sum + d.milestones.length, 0);
  const completedMilestones = deliverables.reduce((sum, d) => sum + d.milestones.filter(m => m.status === "COMPLETED").length, 0);
  const hasRed = deliverables.some(d => d.rag_status === "RED");
  const hasAmber = deliverables.some(d => d.rag_status === "AMBER");
  const rag = hasRed ? "RED" : hasAmber ? "AMBER" : "GREEN";
  const ragCfg = RAG_CONFIG[rag] || RAG_CONFIG.GREEN;

  return (
    <div className="rounded-lg border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 p-4">
      <div className="flex items-center gap-2 mb-3">
        <span className={cn("h-2.5 w-2.5 rounded-full", ragCfg.dotColor)} />
        <h3 className="text-sm font-semibold text-gray-900 dark:text-white truncate">{pillarName}</h3>
        <span className={cn("ml-auto text-xs px-2 py-0.5 rounded-full", ragCfg.bgColor, ragCfg.color)}>
          {ragCfg.label}
        </span>
      </div>
      <div className="mb-2">
        <div className="flex items-center justify-between text-xs text-gray-400 mb-1">
          <span>{avgProgress}% complete</span>
          <span>{completedMilestones}/{totalMilestones} milestones</span>
        </div>
        <div className="h-2 w-full rounded-full bg-gray-200 dark:bg-gray-700">
          <div
            className={cn("h-2 rounded-full transition-all", rag === "RED" ? "bg-red-500" : rag === "AMBER" ? "bg-amber-500" : "bg-green-500")}
            style={{ width: `${avgProgress}%` }}
          />
        </div>
      </div>
    </div>
  );
}

function ActionRow({ action, onToggle }: { action: WeeklyPlanAction; onToggle: (id: number, status: string) => void }) {
  const isDone = action.status === "DONE" || action.status === "SKIPPED";
  const priorityColors: Record<string, string> = {
    HIGH: "text-red-400 bg-red-900/30",
    MEDIUM: "text-amber-400 bg-amber-900/30",
    LOW: "text-gray-400 bg-white dark:bg-gray-800",
  };

  return (
    <div className={cn("flex items-start gap-3 rounded-md px-3 py-2 transition-colors hover:bg-gray-100 dark:hover:bg-gray-800/50", isDone && "opacity-50")}>
      <input
        type="checkbox"
        checked={isDone}
        onChange={() => onToggle(action.id, isDone ? "PENDING" : "DONE")}
        className="mt-1 h-4 w-4 rounded border-gray-300 dark:border-gray-600 bg-gray-200 dark:bg-gray-700 text-blue-500 focus:ring-blue-500"
      />
      <div className="flex-1 min-w-0">
        <div className="flex items-center gap-2 flex-wrap">
          <span className={cn("text-sm text-gray-700 dark:text-gray-200", isDone && "line-through")}>{action.title}</span>
          {action.is_ai_generated && (
            <Sparkles className="h-3 w-3 text-purple-400 flex-shrink-0" />
          )}
          {action.carried_from_week && (
            <span className="text-[10px] px-1.5 py-0.5 rounded bg-amber-900/30 text-amber-400">
              Week {action.carried_from_week}
            </span>
          )}
        </div>
        {action.description && (
          <p className="text-xs text-gray-500 mt-0.5">{action.description}</p>
        )}
      </div>
      <div className="flex items-center gap-2 flex-shrink-0">
        {action.owner && (
          <span className="text-xs text-gray-400">{action.owner}</span>
        )}
        <span className={cn("text-[10px] px-1.5 py-0.5 rounded", priorityColors[action.priority] || priorityColors.MEDIUM)}>
          {action.priority}
        </span>
      </div>
    </div>
  );
}

function ActionGroup({ title, actions, onToggle }: { title: string; actions: WeeklyPlanAction[]; onToggle: (id: number, status: string) => void }) {
  if (!actions.length) return null;
  return (
    <div className="space-y-1">
      <h4 className="text-xs font-semibold uppercase tracking-wider text-gray-500 px-3 pt-2">{title}</h4>
      {actions.map((action) => (
        <ActionRow key={action.id} action={action} onToggle={onToggle} />
      ))}
    </div>
  );
}

export default function WeeklyPlansTab() {
  const { data: plans } = useWeeklyPlans();
  const { data: deliverables } = useProgrammeDeliverables();
  const currentWeek = getCurrentWeekNumber();
  const [selectedWeekNum, setSelectedWeekNum] = useState<number>(currentWeek);

  const selectedPlan = useMemo(() => {
    if (!plans) return null;
    return plans.find(p => p.week_number === selectedWeekNum) || null;
  }, [plans, selectedWeekNum]);

  const { data: planDetail, mutate: mutatePlan } = useWeeklyPlan(selectedPlan?.id ?? null);

  const handleToggleAction = useCallback(async (actionId: number, newStatus: string) => {
    try {
      await api.updatePlanAction(actionId, { status: newStatus });
      mutatePlan();
    } catch (e) {
      console.error("Failed to update action:", e);
    }
  }, [mutatePlan]);

  // Group actions by section
  const deliverableStrategic = planDetail?.actions.filter(a => a.category === "deliverable_strategic") || [];
  const deliverableTactical = planDetail?.actions.filter(a => a.category === "deliverable_tactical") || [];
  const programmeStrategic = planDetail?.actions.filter(a => a.category === "programme_strategic") || [];
  const programmeTactical = planDetail?.actions.filter(a => a.category === "programme_tactical") || [];

  // Group deliverables by pillar
  const pillarGroups = useMemo(() => {
    if (!deliverables) return {};
    const groups: Record<number, ProgrammeDeliverable[]> = {};
    deliverables.forEach(d => {
      (groups[d.pillar] ||= []).push(d);
    });
    return groups;
  }, [deliverables]);

  const weekOptions = Array.from({ length: 12 }, (_, i) => i + 1);

  return (
    <div className="space-y-6">
      {/* Week Selector */}
      <div className="flex items-center gap-3">
        <label className="text-sm text-gray-400">Week:</label>
        <div className="relative">
          <select
            value={selectedWeekNum}
            onChange={(e) => setSelectedWeekNum(Number(e.target.value))}
            className="appearance-none rounded-md border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 px-3 py-1.5 pr-8 text-sm text-gray-900 dark:text-white focus:border-blue-500 focus:outline-none"
          >
            {weekOptions.map((w) => {
              const { start, end } = getWeekDates(w);
              const isPast = w < currentWeek;
              const isCurrent = w === currentWeek;
              return (
                <option key={w} value={w}>
                  Week {w} · {formatShortDate(start)}–{formatShortDate(end)}
                  {isCurrent ? " (Current)" : isPast ? " (Completed)" : ""}
                </option>
              );
            })}
          </select>
          <ChevronDown className="pointer-events-none absolute right-2 top-1/2 h-4 w-4 -translate-y-1/2 text-gray-400" />
        </div>
        {selectedWeekNum < currentWeek && (
          <span className="text-xs text-gray-500 bg-white dark:bg-gray-800 rounded px-2 py-1">
            Week {selectedWeekNum} · Completed
          </span>
        )}
      </div>

      {/* Deliverable Progress */}
      <div>
        <h2 className="text-lg font-semibold text-gray-900 dark:text-white mb-3">Deliverable Progress</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {[1, 2, 3].map(pillar => (
            <PillarProgressCard key={pillar} deliverables={pillarGroups[pillar] || []} />
          ))}
        </div>
        {planDetail?.deliverable_progress_summary && (
          <div className="mt-3 rounded-lg border border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-800/50 p-4">
            <p className="text-sm text-gray-600 dark:text-gray-300 whitespace-pre-wrap">{planDetail.deliverable_progress_summary}</p>
          </div>
        )}
      </div>

      {!planDetail ? (
        /* Empty state */
        <div className="rounded-lg border border-dashed border-gray-300 dark:border-gray-600 bg-gray-50 dark:bg-gray-800/30 p-8 text-center">
          <p className="text-gray-400 mb-2">No plan generated for Week {selectedWeekNum} yet.</p>
          <p className="text-sm text-gray-500">
            Run <code className="bg-gray-200 dark:bg-gray-700 px-1.5 py-0.5 rounded text-gray-600 dark:text-gray-300">/weekly-plan</code> in Claude Code to generate.
          </p>
        </div>
      ) : (
        <>
          {/* Deliverable Actions */}
          <div>
            <h2 className="text-lg font-semibold text-gray-900 dark:text-white mb-3">Deliverable Actions</h2>
            <div className="rounded-lg border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
              <ActionGroup title="Strategic" actions={deliverableStrategic} onToggle={handleToggleAction} />
              <ActionGroup title="Tactical" actions={deliverableTactical} onToggle={handleToggleAction} />
              {!deliverableStrategic.length && !deliverableTactical.length && (
                <p className="text-sm text-gray-500 p-4">No deliverable actions for this week.</p>
              )}
            </div>
          </div>

          {/* Programme Actions */}
          <div>
            <h2 className="text-lg font-semibold text-gray-900 dark:text-white mb-3">Programme Actions</h2>
            <div className="rounded-lg border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
              <ActionGroup title="Strategic" actions={programmeStrategic} onToggle={handleToggleAction} />
              <ActionGroup title="Tactical" actions={programmeTactical} onToggle={handleToggleAction} />
              {!programmeStrategic.length && !programmeTactical.length && (
                <p className="text-sm text-gray-500 p-4">No programme actions for this week.</p>
              )}
            </div>
          </div>

          {planDetail.programme_actions_summary && (
            <div className="rounded-lg border border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-800/50 p-4">
              <h3 className="text-sm font-medium text-gray-600 dark:text-gray-300 mb-2">Programme Summary</h3>
              <p className="text-sm text-gray-400 whitespace-pre-wrap">{planDetail.programme_actions_summary}</p>
            </div>
          )}
        </>
      )}
    </div>
  );
}
