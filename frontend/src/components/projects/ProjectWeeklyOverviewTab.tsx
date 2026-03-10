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

/**
 * Extract project-specific content from a programme-wide weekly report.
 * Pulls the matching workstream section, plus relevant risks and decisions.
 */
function extractProjectStatus(
  markdown: string,
  workstreamCode: string | null,
  projectName: string,
): string {
  if (!workstreamCode && !projectName) return "";

  const lines = markdown.split("\n");
  const sections: string[] = [];

  // --- 1. Extract the matching workstream section from "## Workstream Progress" ---
  const wsContent = extractSection(lines, (heading) => {
    const h = heading.toLowerCase();
    if (workstreamCode && h.includes(workstreamCode.toLowerCase())) return true;
    if (projectName && h.includes(projectName.toLowerCase())) return true;
    return false;
  }, 3); // match ### headings

  if (wsContent.length > 0) {
    sections.push(wsContent.join("\n").trim());
  }

  // --- 2. Extract relevant risks ---
  const risksBlock = extractH2Block(lines, "emerging risks");
  if (risksBlock.length > 0) {
    const relevantRisks = filterBullets(risksBlock, workstreamCode, projectName);
    if (relevantRisks.length > 0) {
      sections.push("## Risks\n" + relevantRisks.join("\n"));
    }
  }

  // --- 3. Extract relevant decisions ---
  const decisionsBlock = extractH2Block(lines, "key decisions");
  if (decisionsBlock.length > 0) {
    const relevantDecisions = filterBullets(decisionsBlock, workstreamCode, projectName);
    if (relevantDecisions.length > 0) {
      sections.push("## Decisions\n" + relevantDecisions.join("\n"));
    }
  }

  return sections.join("\n\n").trim();
}

/** Extract a ### section whose heading matches the predicate */
function extractSection(
  lines: string[],
  matchHeading: (heading: string) => boolean,
  level: number,
): string[] {
  const prefix = "#".repeat(level) + " ";
  const parentPrefix = "#".repeat(level - 1) + " ";
  const result: string[] = [];
  let capturing = false;

  for (const line of lines) {
    if (line.startsWith(prefix)) {
      if (capturing) break; // hit next sibling section
      if (matchHeading(line.slice(prefix.length))) {
        capturing = true;
        // Don't include the heading itself — the UI already shows the project name
        continue;
      }
    } else if (capturing && line.startsWith(parentPrefix)) {
      break; // hit a parent ## section
    }

    if (capturing) {
      result.push(line);
    }
  }

  return result;
}

/** Get all lines within an h2 block matching a name (e.g., "emerging risks") */
function extractH2Block(lines: string[], sectionName: string): string[] {
  const result: string[] = [];
  let capturing = false;

  for (const line of lines) {
    const h2Match = line.match(/^## (.+)/);
    if (h2Match) {
      if (capturing) break;
      if (h2Match[1].trim().toLowerCase().includes(sectionName)) {
        capturing = true;
        continue; // skip the heading
      }
    }
    if (capturing) result.push(line);
  }

  return result;
}

/** Filter bullet lines that mention the workstream code or project name */
function filterBullets(
  lines: string[],
  wsCode: string | null,
  projectName: string,
): string[] {
  // Group lines into bullets (a bullet starts with "- ")
  const bullets: string[][] = [];
  for (const line of lines) {
    if (line.startsWith("- ")) {
      bullets.push([line]);
    } else if (bullets.length > 0 && line.trim() !== "") {
      bullets[bullets.length - 1].push(line);
    }
  }

  const terms: string[] = [];
  if (wsCode) terms.push(wsCode.toLowerCase());
  if (projectName) {
    terms.push(projectName.toLowerCase());
    // Also match key words from the project name (e.g., "Build in Five" → "build in five")
    // and common abbreviations
    const words = projectName.split(/[\s/()]+/).filter((w) => w.length > 3);
    terms.push(...words.map((w) => w.toLowerCase()));
  }

  return bullets
    .filter((bullet) => {
      const text = bullet.join(" ").toLowerCase();
      return terms.some((term) => text.includes(term));
    })
    .map((bullet) => bullet.join("\n"));
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
          project.workstream_code,
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
  }, [timeline.weeks, project.workstream_code, project.name, project.description]);

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
              className="rounded-lg border border-gray-200 bg-white p-4"
            >
              <div className={`inline-flex rounded-md p-2 ${card.color}`}>
                <Icon className="h-4 w-4" />
              </div>
              <p className="mt-2 text-2xl font-bold text-gray-900">{count}</p>
              <p className="text-xs text-gray-500">{card.label}</p>
            </div>
          );
        })}
      </div>

      {/* ── CURRENT STATUS ──────────────────────────────────── */}
      {currentStatus && (
        <div className="rounded-lg border border-blue-200 bg-gradient-to-br from-blue-50/80 to-white p-6">
          <div className="mb-3 flex items-center justify-between">
            <h3 className="flex items-center gap-2 text-sm font-semibold text-gray-900">
              <Activity className="h-4 w-4 text-blue-600" />
              Current Status
            </h3>
            {statusWeekLabel && (
              <span className="text-xs text-gray-400">
                as of {statusWeekLabel}
              </span>
            )}
          </div>
          <div className="prose prose-sm max-w-none prose-headings:text-gray-900 prose-h2:mt-4 prose-h2:mb-2 prose-h2:text-sm prose-h2:font-semibold prose-p:text-gray-700 prose-li:text-gray-700 prose-strong:text-gray-900">
            <MarkdownContent>{currentStatus}</MarkdownContent>
          </div>
        </div>
      )}

      {/* ── ACTIONS (up front) ──────────────────────────────── */}
      {allActions.length > 0 && (
        <div className="rounded-lg border border-gray-200 bg-white">
          <div className="flex items-center justify-between border-b border-gray-100 px-5 py-4">
            <h3 className="flex items-center gap-2 text-sm font-semibold text-gray-900">
              <CheckSquare className="h-4 w-4 text-green-600" />
              Actions
              {openActions.length > 0 && (
                <span className="rounded-full bg-green-100 px-2 py-0.5 text-xs font-medium text-green-700">
                  {openActions.length} open
                </span>
              )}
            </h3>
            {completedActions.length > 0 && (
              <button
                onClick={() => setShowCompletedActions(!showCompletedActions)}
                className="text-xs text-gray-500 hover:text-gray-700"
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
                <p className="text-sm text-gray-400 italic">
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
                  <p className="text-sm text-gray-900">
                    {a.description || a.title}
                  </p>
                  <div className="mt-1 flex flex-wrap items-center gap-3">
                    {a.owner && (
                      <span className="flex items-center gap-1 text-xs text-gray-500">
                        <User className="h-3 w-3" />
                        {a.owner}
                      </span>
                    )}
                    {a.due_date && (
                      <span className="flex items-center gap-1 text-xs text-gray-400">
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
                  className="flex items-start gap-3 bg-gray-50/50 px-5 py-3 opacity-70"
                >
                  <CheckCircle2 className="mt-0.5 h-4 w-4 flex-shrink-0 text-gray-400" />
                  <div className="min-w-0 flex-1">
                    <p className="text-sm text-gray-500 line-through">
                      {a.description || a.title}
                    </p>
                    <div className="mt-1 flex flex-wrap items-center gap-3">
                      {a.owner && (
                        <span className="flex items-center gap-1 text-xs text-gray-400">
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
        <div className="rounded-lg border border-gray-200 bg-white p-6">
          <p className="text-sm text-gray-500">
            No dated activity found for this project yet.
          </p>
        </div>
      ) : (
        <div className="space-y-3">
          {/* Timeline header with controls */}
          <div className="flex items-center justify-between">
            <h3 className="flex items-center gap-2 text-sm font-semibold text-gray-900">
              <Calendar className="h-4 w-4 text-gray-500" />
              Weekly Summaries
              <span className="text-xs font-normal text-gray-400">
                ({timeline.total_weeks} week
                {timeline.total_weeks !== 1 ? "s" : ""})
              </span>
            </h3>
            <div className="flex gap-2">
              <button
                onClick={expandAll}
                className="text-xs text-blue-600 hover:text-blue-800"
              >
                Expand all
              </button>
              <span className="text-xs text-gray-300">|</span>
              <button
                onClick={collapseAll}
                className="text-xs text-blue-600 hover:text-blue-800"
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
                    ? "border-gray-100 bg-gray-50/50"
                    : "border-gray-200 bg-white"
                }`}
              >
                {/* Week header */}
                <button
                  onClick={() => !empty && toggle(idx)}
                  className={`flex w-full items-center justify-between px-5 py-3 text-left transition-colors ${
                    empty
                      ? "cursor-default"
                      : "cursor-pointer hover:bg-gray-50"
                  }`}
                >
                  <div className="flex items-center gap-2">
                    {empty ? (
                      <Minus className="h-4 w-4 flex-shrink-0 text-gray-300" />
                    ) : isOpen ? (
                      <ChevronDown className="h-4 w-4 flex-shrink-0 text-gray-400" />
                    ) : (
                      <ChevronRight className="h-4 w-4 flex-shrink-0 text-gray-400" />
                    )}
                    <span
                      className={`text-sm font-semibold ${
                        empty ? "text-gray-400" : "text-gray-900"
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
                      <span className="text-xs italic text-gray-400">
                        No activity this week
                      </span>
                    )}
                  </div>
                  {!empty && (
                    <div className="flex flex-shrink-0 items-center gap-2">
                      {week.transcript_count > 0 && (
                        <span className="inline-flex items-center gap-1 rounded-full bg-blue-50 px-2 py-0.5 text-[10px] font-medium text-blue-700">
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
                    <p className="pl-6 text-xs text-gray-400 line-clamp-2">
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
                        <div className="prose prose-sm max-w-none prose-headings:text-gray-900 prose-h2:mt-6 prose-h2:mb-3 prose-h2:text-base prose-h3:mt-4 prose-h3:mb-2 prose-h3:text-sm prose-p:text-gray-700 prose-li:text-gray-700 prose-strong:text-gray-900">
                          <MarkdownContent>
                            {week.weekly_report_content!}
                          </MarkdownContent>
                        </div>
                      </div>
                    )}

                    {/* ── INDIVIDUAL CALL SUMMARIES (drill-down) ──── */}
                    {week.transcripts.length > 0 && (
                      <div
                        className={`border-t border-gray-100 ${hasReport ? "bg-gray-50/30" : ""}`}
                      >
                        <button
                          onClick={() => toggleCallList(idx)}
                          className="flex w-full items-center gap-2 px-5 py-3 text-left hover:bg-gray-50"
                        >
                          {callsOpen ? (
                            <ChevronDown className="h-3.5 w-3.5 text-gray-400" />
                          ) : (
                            <ChevronRight className="h-3.5 w-3.5 text-gray-400" />
                          )}
                          <FileText className="h-3.5 w-3.5 text-blue-500" />
                          <span className="text-xs font-semibold uppercase tracking-wider text-gray-500">
                            Individual Call Summaries
                          </span>
                          <span className="text-xs text-gray-400">
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
                                    <FileText className="h-4 w-4 flex-shrink-0 text-blue-500" />
                                    <Link
                                      href={`/transcripts/${t.id}`}
                                      className="text-sm font-semibold text-blue-700 hover:underline"
                                    >
                                      {t.title || t.file_name}
                                    </Link>
                                    {t.date && (
                                      <span className="text-xs text-gray-400">
                                        {t.date}
                                      </span>
                                    )}
                                    <div className="ml-auto flex flex-shrink-0 items-center gap-1.5">
                                      {t.participant_count > 0 && (
                                        <span className="text-[10px] text-gray-400">
                                          {t.participant_count} participants
                                        </span>
                                      )}
                                      {t.word_count > 0 && (
                                        <span className="text-[10px] text-gray-400">
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
                                        className="mb-1 flex items-center gap-1 text-xs text-purple-600 hover:text-purple-800"
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
                                        <div className="rounded-md border border-gray-100 bg-white p-4">
                                          <MarkdownContent>
                                            {t.summary_content}
                                          </MarkdownContent>
                                        </div>
                                      ) : (
                                        t.summary_tldr && (
                                          <p className="text-sm text-gray-600 line-clamp-2">
                                            {t.summary_tldr}
                                          </p>
                                        )
                                      )}
                                    </div>
                                  ) : (
                                    <p className="ml-6 mt-1 text-xs italic text-gray-400">
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
                        <h4 className="mb-3 flex items-center gap-2 text-xs font-semibold uppercase tracking-wider text-gray-500">
                          <Gavel className="h-3.5 w-3.5 text-amber-500" />
                          Decisions Made
                        </h4>
                        <div className="ml-6 space-y-2.5">
                          {week.decisions.map((d) => (
                            <div
                              key={d.id}
                              className="rounded-md border border-amber-100 bg-amber-50/40 p-3"
                            >
                              <p className="text-sm">
                                <span className="font-semibold text-gray-900">
                                  Decision #{d.number}:
                                </span>{" "}
                                <span className="text-gray-700">
                                  {d.decision}
                                </span>
                              </p>
                              {d.rationale && (
                                <p className="mt-1 text-xs italic text-gray-500">
                                  Rationale: {d.rationale}
                                </p>
                              )}
                              {d.key_people.length > 0 && (
                                <p className="mt-1 text-[10px] text-gray-400">
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
                        <h4 className="mb-3 flex items-center gap-2 text-xs font-semibold uppercase tracking-wider text-gray-500">
                          <CheckSquare className="h-3.5 w-3.5 text-green-500" />
                          Actions
                        </h4>
                        <div className="ml-6 space-y-1.5">
                          {week.action_items.map((a) => (
                            <div
                              key={a.id}
                              className="flex items-start gap-2 py-1 text-sm"
                            >
                              <div className="min-w-0 flex-1">
                                <span className="font-medium text-gray-900">
                                  {a.number}:
                                </span>{" "}
                                <span className="text-gray-700">
                                  {a.description}
                                </span>
                                {a.owner && (
                                  <span className="text-xs text-gray-500">
                                    {" "}
                                    — {a.owner}
                                  </span>
                                )}
                                {a.deadline && (
                                  <span className="text-xs text-gray-400">
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
