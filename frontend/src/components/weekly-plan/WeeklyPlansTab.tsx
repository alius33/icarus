"use client";

import { useState, useMemo, useCallback } from "react";
import { useWeeklyPlans, useWeeklyPlan, useProgrammeDeliverables } from "@/lib/swr";
import { api } from "@/lib/api";
import { RAG_CONFIG, type WeeklyPlanAction, type ProgrammeDeliverable } from "@/lib/types";
import { cn } from "@/lib/utils";
import Link from "next/link";
import { Sparkles, ChevronDown, ChevronRight, Info, Link2 } from "lucide-react";
import MarkdownContent from "@/components/MarkdownContent";

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
    <div className="rounded-lg border border-forest-200 dark:border-forest-700 bg-white dark:bg-forest-800 p-4">
      <div className="flex items-center gap-2 mb-3">
        <span className={cn("h-2.5 w-2.5 rounded-full", ragCfg.dotColor)} />
        <h3 className="text-sm font-semibold text-forest-950 dark:text-white truncate">{pillarName}</h3>
        <span className={cn("ml-auto text-xs px-2 py-0.5 rounded-full", ragCfg.bgColor, ragCfg.color)}>
          {ragCfg.label}
        </span>
      </div>
      <div className="mb-2">
        <div className="flex items-center justify-between text-xs text-forest-300 mb-1">
          <span>{avgProgress}% complete</span>
          <span>{completedMilestones}/{totalMilestones} milestones</span>
        </div>
        <div className="h-2 w-full rounded-full bg-gray-200 dark:bg-forest-800">
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
  const [isExpanded, setIsExpanded] = useState(false);
  const isDone = action.status === "DONE" || action.status === "SKIPPED";
  const hasContext = !!(action.source_transcript_id || action.source_update_id || action.context);
  const priorityColors: Record<string, string> = {
    HIGH: "text-red-700 bg-red-100 dark:text-red-400 dark:bg-red-900/30",
    MEDIUM: "text-amber-700 bg-amber-100 dark:text-amber-400 dark:bg-amber-900/30",
    LOW: "text-forest-500 bg-forest-100 dark:text-forest-300 dark:bg-forest-800",
  };

  return (
    <div>
      <div className={cn("flex items-start gap-3 rounded-md px-3 py-2 transition-colors hover:bg-forest-100 dark:hover:bg-forest-700/50", isDone && "opacity-50")}>
        <input
          type="checkbox"
          checked={isDone}
          onChange={() => onToggle(action.id, isDone ? "PENDING" : "DONE")}
          className="mt-1 h-4 w-4 rounded border-forest-200 dark:border-forest-700 bg-gray-200 dark:bg-forest-800 text-forest-500 focus:ring-forest-500"
        />
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2 flex-wrap">
            <span className={cn("text-sm text-forest-600 dark:text-forest-200", isDone && "line-through")}>{action.title}</span>
            {action.is_ai_generated && (
              <Sparkles className="h-3 w-3 text-purple-400 flex-shrink-0" />
            )}
            {action.carried_from_week && (
              <span className="text-[10px] px-1.5 py-0.5 rounded bg-amber-100 text-amber-700 dark:bg-amber-900/30 dark:text-amber-400">
                Week {action.carried_from_week}
              </span>
            )}
            {hasContext && (
              <button
                onClick={() => setIsExpanded(!isExpanded)}
                className="flex items-center gap-0.5 text-[10px] px-1.5 py-0.5 rounded bg-blue-50 text-blue-600 hover:bg-blue-100 dark:bg-blue-900/30 dark:text-blue-400 dark:hover:bg-blue-900/50 transition-colors"
              >
                <Info className="h-3 w-3" />
                <span>Context</span>
                {isExpanded ? <ChevronDown className="h-3 w-3" /> : <ChevronRight className="h-3 w-3" />}
              </button>
            )}
          </div>
          {action.description && (
            <p className="text-xs text-forest-400 mt-0.5">{action.description}</p>
          )}
        </div>
        <div className="flex items-center gap-2 flex-shrink-0">
          {action.owner && (
            <span className="text-xs text-forest-300">{action.owner}</span>
          )}
          <span className={cn("text-[10px] px-1.5 py-0.5 rounded", priorityColors[action.priority] || priorityColors.MEDIUM)}>
            {action.priority}
          </span>
        </div>
      </div>
      {/* Expandable context panel */}
      {isExpanded && hasContext && (
        <div className="ml-10 mr-3 mt-1 mb-2 rounded-md border border-forest-200 dark:border-forest-700 bg-forest-50 dark:bg-forest-800/50 p-3 space-y-2">
          {action.source_transcript_id && (
            <div className="flex items-center gap-1.5 text-xs">
              <Link2 className="h-3 w-3 text-forest-400" />
              <span className="text-forest-400">From:</span>
              <Link
                href={`/transcripts/${action.source_transcript_id}`}
                className="text-blue-600 dark:text-blue-400 hover:underline font-medium"
              >
                {action.source_transcript_title || `Transcript #${action.source_transcript_id}`}
              </Link>
            </div>
          )}
          {action.source_update_id && (
            <div className="flex items-center gap-1.5 text-xs">
              <Link2 className="h-3 w-3 text-purple-400" />
              <span className="text-forest-400">From update:</span>
              <Link
                href={`/updates/${action.source_update_id}`}
                className="text-purple-600 dark:text-purple-400 hover:underline font-medium"
              >
                {action.source_update_title || `Update #${action.source_update_id}`}
              </Link>
            </div>
          )}
          {(action.source_transcript_id || action.source_update_id) && action.context && (
            <hr className="border-forest-200 dark:border-forest-700" />
          )}
          {action.context && (
            <div className="prose prose-sm max-w-none prose-p:text-forest-600 dark:prose-p:text-forest-300 prose-li:text-forest-600 dark:prose-li:text-forest-300 prose-strong:text-forest-950 dark:prose-strong:text-forest-100">
              <MarkdownContent>{action.context}</MarkdownContent>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

function ActionGroup({ title, actions, onToggle }: { title: string; actions: WeeklyPlanAction[]; onToggle: (id: number, status: string) => void }) {
  if (!actions.length) return null;
  return (
    <div className="space-y-1">
      <h4 className="text-xs font-semibold uppercase tracking-wider text-forest-400 px-3 pt-2">{title}</h4>
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
        <label className="text-sm text-forest-300">Week:</label>
        <div className="relative">
          <select
            value={selectedWeekNum}
            onChange={(e) => setSelectedWeekNum(Number(e.target.value))}
            className="appearance-none rounded-md border border-forest-200 dark:border-forest-700 bg-white dark:bg-forest-800 px-3 py-1.5 pr-8 text-sm text-forest-950 dark:text-white focus:border-forest-500 focus:outline-none"
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
          <ChevronDown className="pointer-events-none absolute right-2 top-1/2 h-4 w-4 -translate-y-1/2 text-forest-300" />
        </div>
        {selectedWeekNum < currentWeek && (
          <span className="text-xs text-forest-400 bg-white dark:bg-forest-800 rounded px-2 py-1">
            Week {selectedWeekNum} · Completed
          </span>
        )}
      </div>

      {/* Deliverable Progress */}
      <div>
        <h2 className="text-lg font-semibold text-forest-950 dark:text-white mb-3">Deliverable Progress</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {[1, 2, 3].map(pillar => (
            <PillarProgressCard key={pillar} deliverables={pillarGroups[pillar] || []} />
          ))}
        </div>
        {planDetail?.deliverable_progress_summary && (
          <div className="mt-3 rounded-lg border border-forest-200 dark:border-forest-700 bg-forest-50 dark:bg-forest-800/50 p-4">
            <MarkdownContent className="text-sm">{planDetail.deliverable_progress_summary}</MarkdownContent>
          </div>
        )}
      </div>

      {!planDetail ? (
        /* Empty state */
        <div className="rounded-lg border border-dashed border-forest-200 dark:border-forest-700 bg-forest-50 dark:bg-forest-800/30 p-8 text-center">
          <p className="text-forest-300 mb-2">No plan generated for Week {selectedWeekNum} yet.</p>
          <p className="text-sm text-forest-400">
            Run <code className="bg-gray-200 dark:bg-forest-800 px-1.5 py-0.5 rounded text-forest-500 dark:text-forest-200">/weekly-plan</code> in Claude Code to generate.
          </p>
        </div>
      ) : (
        <>
          {/* Deliverable Actions */}
          <div>
            <h2 className="text-lg font-semibold text-forest-950 dark:text-white mb-3">Deliverable Actions</h2>
            <div className="rounded-lg border border-forest-200 dark:border-forest-700 bg-white dark:bg-forest-800 divide-y divide-forest-200 dark:divide-forest-700">
              <ActionGroup title="Strategic" actions={deliverableStrategic} onToggle={handleToggleAction} />
              <ActionGroup title="Tactical" actions={deliverableTactical} onToggle={handleToggleAction} />
              {!deliverableStrategic.length && !deliverableTactical.length && (
                <p className="text-sm text-forest-400 p-4">No deliverable actions for this week.</p>
              )}
            </div>
          </div>

          {/* Programme Actions */}
          <div>
            <h2 className="text-lg font-semibold text-forest-950 dark:text-white mb-3">Programme Actions</h2>
            <div className="rounded-lg border border-forest-200 dark:border-forest-700 bg-white dark:bg-forest-800 divide-y divide-forest-200 dark:divide-forest-700">
              <ActionGroup title="Strategic" actions={programmeStrategic} onToggle={handleToggleAction} />
              <ActionGroup title="Tactical" actions={programmeTactical} onToggle={handleToggleAction} />
              {!programmeStrategic.length && !programmeTactical.length && (
                <p className="text-sm text-forest-400 p-4">No programme actions for this week.</p>
              )}
            </div>
          </div>

          {planDetail.programme_actions_summary && (
            <div className="rounded-lg border border-forest-200 dark:border-forest-700 bg-forest-50 dark:bg-forest-800/50 p-4">
              <h3 className="text-sm font-medium text-forest-500 dark:text-forest-200 mb-2">Programme Summary</h3>
              <MarkdownContent className="text-sm">{planDetail.programme_actions_summary}</MarkdownContent>
            </div>
          )}
        </>
      )}
    </div>
  );
}
