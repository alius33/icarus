"use client";

import { useState, useMemo } from "react";
import Link from "next/link";
import type {
  ProjectWeeklyTimeline,
  ProjectBase,
  ProjectWeek,
  ActionItemSchema,
} from "@/lib/types";
import { getStatusColor } from "@/lib/utils";
import MarkdownContent from "@/components/MarkdownContent";
import { extractProjectStatus } from "@/lib/markdown-extract";
import {
  ChevronDown,
  ChevronRight,
  FileText,
  Gavel,
  CheckSquare,
  AlertCircle,
  Calendar,
  Minus,
  BookOpen,
  CircleDot,
  Clock,
  CheckCircle2,
  Activity,
  User,
} from "lucide-react";

const STAT_CARDS = [
  {
    key: "decision_count" as const,
    label: "Decisions",
    icon: Gavel,
    color: "text-amber-600 bg-amber-50",
  },
  {
    key: "action_count" as const,
    label: "Actions",
    icon: CheckSquare,
    color: "text-green-600 bg-green-50",
  },
  {
    key: "open_thread_count" as const,
    label: "Open Threads",
    icon: AlertCircle,
    color: "text-red-600 bg-red-50",
  },
];

interface Props {
  timeline: ProjectWeeklyTimeline;
  project: ProjectBase;
  allActions: ActionItemSchema[];
}

function isEmptyWeek(week: ProjectWeek): boolean {
  return (
    week.transcripts.length === 0 &&
    week.decisions.length === 0 &&
    week.action_items.length === 0 &&
    !week.weekly_report_content
  );
}

export default function ProjectWeeklyOverviewTab({
  timeline,
  project,
  allActions,
}: Props) {
  // Auto-expand the 2 most recent weeks that have activity
  const [expanded, setExpanded] = useState<Set<number>>(() => {
    const initial = new Set<number>();
    let activeCount = 0;
    for (let i = 0; i < timeline.weeks.length && activeCount < 2; i++) {
      if (!isEmptyWeek(timeline.weeks[i])) {
        initial.add(i);
        activeCount++;
      }
    }
    return initial;
  });

  const [expandedCalls, setExpandedCalls] = useState<Set<string>>(new Set());
  const [callListExpanded, setCallListExpanded] = useState<Set<number>>(
    new Set()
  );

  // Derive project-specific status from the most recent weekly report
  const currentStatus = useMemo(() => {
    for (const week of timeline.weeks) {
      if (week.weekly_report_content) {
        const status = extractProjectStatus(
          week.weekly_report_content,
          project.name,
        );
        if (status) return status;
      }
    }
    // Fallback: synthesize from transcript TLDRs
    for (const week of timeline.weeks) {
      const tldrs = week.transcripts
        .filter((t) => t.summary_tldr)
        .map((t) => `- **${t.title || t.file_name}:** ${t.summary_tldr}`);
      if (tldrs.length > 0) {
        return tldrs.join("\n");
      }
    }
    return project.description || null;
  }, [timeline.weeks, project.name, project.description]);

  // The week label for the most recent report
  const statusWeekLabel = useMemo(() => {
    for (const week of timeline.weeks) {
      if (week.weekly_report_content) {
        return week.week_label;
      }
    }
    return null;
  }, [timeline.weeks]);

  // Split actions by status
  const openActions = useMemo(
    () =>
      allActions.filter(
        (a) =>
          a.status.toLowerCase() === "open" ||
          a.status.toLowerCase() === "in progress"
      ),
    [allActions]
  );
  const completedActions = useMemo(
    () =>
      allActions.filter(
        (a) =>
          a.status.toLowerCase() === "completed" ||
          a.status.toLowerCase() === "likely completed"
      ),
    [allActions]
  );

  const [showCompletedActions, setShowCompletedActions] = useState(false);

  const toggle = (idx: number) => {
    setExpanded((prev) => {
      const next = new Set(prev);
      if (next.has(idx)) next.delete(idx);
      else next.add(idx);
      return next;
    });
  };

  const toggleCallList = (idx: number) => {
    setCallListExpanded((prev) => {
      const next = new Set(prev);
      if (next.has(idx)) next.delete(idx);
      else next.add(idx);
      return next;
    });
  };

  const toggleCall = (key: string) => {
    setExpandedCalls((prev) => {
      const next = new Set(prev);
      if (next.has(key)) next.delete(key);
      else next.add(key);
      return next;
    });
  };

  const expandAll = () => {
    const all = new Set<number>();
    timeline.weeks.forEach((_, i) => all.add(i));
    setExpanded(all);
  };

  const collapseAll = () => {
    setExpanded(new Set());
    setCallListExpanded(new Set());
    setExpandedCalls(new Set());
  };

  return (
    <div className="space-y-6">
      {/* Compact stat strip */}
      <div className="grid grid-cols-3 gap-4">
        {STAT_CARDS.map((card) => {
          const Icon = card.icon;
          const count = project[card.key];
          return (
            <div
              key={card.key}
              className="rounded-lg border border-forest-200 bg-white dark:bg-forest-800 p-4"
            >
              <div className={`inline-flex rounded-md p-2 ${card.color}`}>
                <Icon className="h-4 w-4" />
              </div>
              <p className="mt-2 text-2xl font-bold text-forest-950">{count}</p>
              <p className="text-sm text-forest-400">{card.label}</p>
            </div>
          );
        })}
      </div>

      {/* ── CURRENT STATUS ──────────────────────────────────── */}
      {currentStatus && (
        <div className="rounded-lg border border-blue-200 bg-gradient-to-br from-blue-50/80 to-white p-6">
          <div className="mb-3 flex items-center justify-between">
            <h3 className="flex items-center gap-2 text-base font-semibold text-forest-950">
              <Activity className="h-4 w-4 text-forest-500" />
              Current Status
            </h3>
            {statusWeekLabel && (
              <span className="text-sm text-forest-300">
                as of {statusWeekLabel}
              </span>
            )}
          </div>
          <div className="prose prose-sm max-w-none prose-headings:text-forest-950 prose-h2:mt-4 prose-h2:mb-2 prose-h2:text-base prose-h2:font-semibold prose-p:text-forest-600 prose-li:text-forest-600 prose-strong:text-forest-950">
            <MarkdownContent>{currentStatus}</MarkdownContent>
          </div>
        </div>
      )}

      {/* ── ACTIONS (up front) ──────────────────────────────── */}
      {allActions.length > 0 && (
        <div className="rounded-lg border border-forest-200 bg-white dark:bg-forest-800">
          <div className="flex items-center justify-between border-b border-gray-100 px-5 py-4">
            <h3 className="flex items-center gap-2 text-base font-semibold text-forest-950">
              <CheckSquare className="h-4 w-4 text-green-600" />
              Actions
              {openActions.length > 0 && (
                <span className="rounded-full bg-green-100 px-2 py-0.5 text-sm font-medium text-green-700">
                  {openActions.length} open
                </span>
              )}
            </h3>
            {completedActions.length > 0 && (
              <button
                onClick={() => setShowCompletedActions(!showCompletedActions)}
                className="text-sm text-forest-400 hover:text-forest-600"
              >
                {showCompletedActions
                  ? "Hide completed"
                  : `Show ${completedActions.length} completed`}
              </button>
            )}
          </div>

          <div className="divide-y divide-gray-50">
            {/* Open actions */}
            {openActions.length === 0 && (
              <div className="px-5 py-4">
                <p className="text-base text-forest-300 italic">
                  No open actions — all caught up.
                </p>
              </div>
            )}
            {openActions.map((a) => (
              <div
                key={a.id}
                className="flex items-start gap-3 px-5 py-3"
              >
                <CircleDot className="mt-0.5 h-4 w-4 flex-shrink-0 text-green-500" />
                <div className="min-w-0 flex-1">
                  <p className="text-base text-forest-950">
                    {a.description || a.title}
                  </p>
                  <div className="mt-1 flex flex-wrap items-center gap-3">
                    {a.owner && (
                      <span className="flex items-center gap-1 text-sm text-forest-400">
                        <User className="h-3 w-3" />
                        {a.owner}
                      </span>
                    )}
                    {a.due_date && (
                      <span className="flex items-center gap-1 text-sm text-forest-300">
                        <Clock className="h-3 w-3" />
                        {a.due_date}
                      </span>
                    )}
                    <span
                      className={`inline-flex rounded-full border px-2 py-0.5 text-[10px] font-medium ${getStatusColor(a.status)}`}
                    >
                      {a.status}
                    </span>
                  </div>
                </div>
              </div>
            ))}

            {/* Completed actions (toggle) */}
            {showCompletedActions &&
              completedActions.map((a) => (
                <div
                  key={a.id}
                  className="flex items-start gap-3 bg-forest-50/50 px-5 py-3 opacity-70"
                >
                  <CheckCircle2 className="mt-0.5 h-4 w-4 flex-shrink-0 text-forest-300" />
                  <div className="min-w-0 flex-1">
                    <p className="text-base text-forest-400 line-through">
                      {a.description || a.title}
                    </p>
                    <div className="mt-1 flex flex-wrap items-center gap-3">
                      {a.owner && (
                        <span className="flex items-center gap-1 text-sm text-forest-300">
                          <User className="h-3 w-3" />
                          {a.owner}
                        </span>
                      )}
                      <span
                        className={`inline-flex rounded-full border px-2 py-0.5 text-[10px] font-medium ${getStatusColor(a.status)}`}
                      >
                        {a.status}
                      </span>
                    </div>
                  </div>
                </div>
              ))}
          </div>
        </div>
      )}

      {/* ── WEEKLY TIMELINE ─────────────────────────────────── */}
      {timeline.weeks.length === 0 ? (
        <div className="rounded-lg border border-forest-200 bg-white dark:bg-forest-800 p-6">
          <p className="text-base text-forest-400">
            No dated activity found for this project yet.
          </p>
        </div>
      ) : (
        <div className="space-y-3">
          {/* Timeline header with controls */}
          <div className="flex items-center justify-between">
            <h3 className="flex items-center gap-2 text-base font-semibold text-forest-950">
              <Calendar className="h-4 w-4 text-forest-400" />
              Weekly Summaries
              <span className="text-sm font-normal text-forest-300">
                ({timeline.total_weeks} week
                {timeline.total_weeks !== 1 ? "s" : ""})
              </span>
            </h3>
            <div className="flex gap-2">
              <button
                onClick={expandAll}
                className="text-sm text-forest-500 hover:text-blue-800"
              >
                Expand all
              </button>
              <span className="text-sm text-forest-500 dark:text-forest-200">|</span>
              <button
                onClick={collapseAll}
                className="text-sm text-forest-500 hover:text-blue-800"
              >
                Collapse all
              </button>
            </div>
          </div>

          {/* Weeks */}
          {timeline.weeks.map((week, idx) => {
            const isOpen = expanded.has(idx);
            const empty = isEmptyWeek(week);
            const hasReport = !!week.weekly_report_content;
            const callsOpen = callListExpanded.has(idx);

            return (
              <div
                key={week.week_start}
                className={`overflow-hidden rounded-lg border ${
                  empty
                    ? "border-gray-100 bg-forest-50/50"
                    : "border-forest-200 bg-white dark:bg-forest-800"
                }`}
              >
                {/* Week header */}
                <button
                  onClick={() => !empty && toggle(idx)}
                  className={`flex w-full items-center justify-between px-5 py-3 text-left transition-colors ${
                    empty
                      ? "cursor-default"
                      : "cursor-pointer hover:bg-forest-50"
                  }`}
                >
                  <div className="flex items-center gap-2">
                    {empty ? (
                      <Minus className="h-4 w-4 flex-shrink-0 text-forest-500 dark:text-forest-200" />
                    ) : isOpen ? (
                      <ChevronDown className="h-4 w-4 flex-shrink-0 text-forest-300" />
                    ) : (
                      <ChevronRight className="h-4 w-4 flex-shrink-0 text-forest-300" />
                    )}
                    <span
                      className={`text-base font-semibold ${
                        empty ? "text-forest-300" : "text-forest-950"
                      }`}
                    >
                      {week.week_label}
                    </span>
                    {hasReport && !isOpen && (
                      <span className="inline-flex items-center gap-1 rounded-full bg-indigo-50 px-2 py-0.5 text-[10px] font-medium text-indigo-700">
                        <BookOpen className="h-3 w-3" />
                        Weekly summary
                      </span>
                    )}
                    {empty && (
                      <span className="text-sm italic text-forest-300">
                        No activity this week
                      </span>
                    )}
                  </div>
                  {!empty && (
                    <div className="flex flex-shrink-0 items-center gap-2">
                      {week.transcript_count > 0 && (
                        <span className="inline-flex items-center gap-1 rounded-full bg-blue-50 px-2 py-0.5 text-[10px] font-medium text-forest-600">
                          <FileText className="h-3 w-3" />
                          {week.transcript_count}
                        </span>
                      )}
                      {week.decision_count > 0 && (
                        <span className="inline-flex items-center gap-1 rounded-full bg-amber-50 px-2 py-0.5 text-[10px] font-medium text-amber-700">
                          <Gavel className="h-3 w-3" />
                          {week.decision_count}
                        </span>
                      )}
                      {week.action_count > 0 && (
                        <span className="inline-flex items-center gap-1 rounded-full bg-green-50 px-2 py-0.5 text-[10px] font-medium text-green-700">
                          <CheckSquare className="h-3 w-3" />
                          {week.action_count}
                        </span>
                      )}
                    </div>
                  )}
                </button>

                {/* Collapsed preview */}
                {!isOpen && !empty && !hasReport && week.transcripts.length > 0 && (
                  <div className="-mt-1 px-5 pb-3">
                    <p className="pl-6 text-sm text-forest-300 line-clamp-2">
                      {week.transcripts
                        .filter((t) => t.summary_tldr)
                        .map((t) => t.title || t.file_name)
                        .join(" · ") || ""}
                    </p>
                  </div>
                )}

                {/* ── EXPANDED WEEK CONTENT ─────────────────────────── */}
                {isOpen && !empty && (
                  <div className="border-t border-gray-100">
                    {/* ── WEEKLY REPORT (primary content) ─────────── */}
                    {hasReport && (
                      <div className="px-6 py-5">
                        <div className="prose prose-sm max-w-none prose-headings:text-forest-950 prose-h2:mt-6 prose-h2:mb-3 prose-h2:text-base prose-h3:mt-4 prose-h3:mb-2 prose-h3:text-base prose-p:text-forest-600 prose-li:text-forest-600 prose-strong:text-forest-950">
                          <MarkdownContent>
                            {week.weekly_report_content!}
                          </MarkdownContent>
                        </div>
                      </div>
                    )}

                    {/* ── INDIVIDUAL CALL SUMMARIES (drill-down) ──── */}
                    {week.transcripts.length > 0 && (
                      <div
                        className={`border-t border-gray-100 ${hasReport ? "bg-forest-50/30" : ""}`}
                      >
                        <button
                          onClick={() => toggleCallList(idx)}
                          className="flex w-full items-center gap-2 px-5 py-3 text-left hover:bg-forest-50"
                        >
                          {callsOpen ? (
                            <ChevronDown className="h-3.5 w-3.5 text-forest-300" />
                          ) : (
                            <ChevronRight className="h-3.5 w-3.5 text-forest-300" />
                          )}
                          <FileText className="h-3.5 w-3.5 text-forest-500" />
                          <span className="text-sm font-semibold uppercase tracking-wider text-forest-400">
                            Individual Call Summaries
                          </span>
                          <span className="text-sm text-forest-300">
                            ({week.transcripts.length} call
                            {week.transcripts.length !== 1 ? "s" : ""})
                          </span>
                        </button>

                        {callsOpen && (
                          <div className="divide-y divide-gray-50">
                            {week.transcripts.map((t) => {
                              const callKey = `${idx}-${t.id}`;
                              const callOpen = expandedCalls.has(callKey);

                              return (
                                <div key={t.id} className="px-5 py-3">
                                  {/* Call header */}
                                  <div className="flex items-center gap-2">
                                    <FileText className="h-4 w-4 flex-shrink-0 text-forest-500" />
                                    <Link
                                      href={`/transcripts/${t.id}`}
                                      className="text-base font-semibold text-forest-600 hover:underline"
                                    >
                                      {t.title || t.file_name}
                                    </Link>
                                    {t.date && (
                                      <span className="text-sm text-forest-300">
                                        {t.date}
                                      </span>
                                    )}
                                    <div className="ml-auto flex flex-shrink-0 items-center gap-1.5">
                                      {t.participant_count > 0 && (
                                        <span className="text-[10px] text-forest-300">
                                          {t.participant_count} participants
                                        </span>
                                      )}
                                      {t.word_count > 0 && (
                                        <span className="text-[10px] text-forest-300">
                                          · ~{Math.round(t.word_count / 150)}{" "}
                                          min
                                        </span>
                                      )}
                                    </div>
                                  </div>

                                  {/* Call summary expand/collapse */}
                                  {t.summary_content ? (
                                    <div className="ml-6 mt-1">
                                      <button
                                        onClick={() => toggleCall(callKey)}
                                        className="mb-1 flex items-center gap-1 text-sm text-purple-600 hover:text-purple-800"
                                      >
                                        {callOpen ? (
                                          <ChevronDown className="h-3 w-3" />
                                        ) : (
                                          <ChevronRight className="h-3 w-3" />
                                        )}
                                        {callOpen ? "Hide" : "Show"} detailed
                                        summary
                                      </button>

                                      {callOpen ? (
                                        <div className="rounded-md border border-gray-100 bg-white dark:bg-forest-800 p-4">
                                          <MarkdownContent>
                                            {t.summary_content}
                                          </MarkdownContent>
                                        </div>
                                      ) : (
                                        t.summary_tldr && (
                                          <p className="text-base text-forest-500 line-clamp-2">
                                            {t.summary_tldr}
                                          </p>
                                        )
                                      )}
                                    </div>
                                  ) : (
                                    <p className="ml-6 mt-1 text-sm italic text-forest-300">
                                      No summary available.
                                    </p>
                                  )}
                                </div>
                              );
                            })}
                          </div>
                        )}
                      </div>
                    )}

                    {/* ── DECISIONS ───────────────────────────────── */}
                    {week.decisions.length > 0 && !hasReport && (
                      <div className="border-t border-gray-100 px-5 py-4">
                        <h4 className="mb-3 flex items-center gap-2 text-sm font-semibold uppercase tracking-wider text-forest-400">
                          <Gavel className="h-3.5 w-3.5 text-amber-500" />
                          Decisions Made
                        </h4>
                        <div className="ml-6 space-y-2.5">
                          {week.decisions.map((d) => (
                            <div
                              key={d.id}
                              className="rounded-md border border-amber-100 bg-amber-50/40 p-3"
                            >
                              <p className="text-base">
                                <span className="font-semibold text-forest-950">
                                  Decision #{d.number}:
                                </span>{" "}
                                <span className="text-forest-600">
                                  {d.decision}
                                </span>
                              </p>
                              {d.rationale && (
                                <p className="mt-1 text-sm italic text-forest-400">
                                  Rationale: {d.rationale}
                                </p>
                              )}
                              {d.key_people.length > 0 && (
                                <p className="mt-1 text-[10px] text-forest-300">
                                  Involved: {d.key_people.join(", ")}
                                </p>
                              )}
                            </div>
                          ))}
                        </div>
                      </div>
                    )}

                    {/* ── ACTIONS ─────────────────────────────────── */}
                    {week.action_items.length > 0 && !hasReport && (
                      <div className="border-t border-gray-100 px-5 py-4">
                        <h4 className="mb-3 flex items-center gap-2 text-sm font-semibold uppercase tracking-wider text-forest-400">
                          <CheckSquare className="h-3.5 w-3.5 text-green-500" />
                          Actions
                        </h4>
                        <div className="ml-6 space-y-1.5">
                          {week.action_items.map((a) => (
                            <div
                              key={a.id}
                              className="flex items-start gap-2 py-1 text-base"
                            >
                              <div className="min-w-0 flex-1">
                                <span className="font-medium text-forest-950">
                                  {a.number}:
                                </span>{" "}
                                <span className="text-forest-600">
                                  {a.description}
                                </span>
                                {a.owner && (
                                  <span className="text-sm text-forest-400">
                                    {" "}
                                    — {a.owner}
                                  </span>
                                )}
                                {a.deadline && (
                                  <span className="text-sm text-forest-300">
                                    {" "}
                                    (due: {a.deadline})
                                  </span>
                                )}
                              </div>
                              <span
                                className={`inline-flex flex-shrink-0 rounded-full border px-2 py-0.5 text-[10px] font-medium ${getStatusColor(a.status)}`}
                              >
                                {a.status}
                              </span>
                            </div>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>
                )}
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
