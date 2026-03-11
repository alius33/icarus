"use client";

import { useState, useMemo } from "react";
import Link from "next/link";
import type { ProjectWeeklyTimeline, ProjectWeek, ProjectBase } from "@/lib/types";
import MarkdownContent from "@/components/MarkdownContent";
import { extractProjectContent } from "@/lib/markdown-extract";
import {
  ChevronDown,
  ChevronRight,
  FileText,
  Minus,
  BookOpen,
  Calendar,
  Gavel,
  CheckSquare,
  ExternalLink,
} from "lucide-react";

interface Props {
  timeline: ProjectWeeklyTimeline;
  project: ProjectBase;
}

function isEmptyWeek(week: ProjectWeek): boolean {
  return (
    week.transcripts.length === 0 &&
    week.decisions.length === 0 &&
    week.action_items.length === 0 &&
    !week.weekly_report_content
  );
}

export default function ProjectSummariesTab({ timeline, project }: Props) {
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
  const [callListExpanded, setCallListExpanded] = useState<Set<number>>(new Set());

  const activeWeeks = useMemo(
    () => timeline.weeks.filter((w) => !isEmptyWeek(w)).length,
    [timeline.weeks],
  );

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

  if (timeline.weeks.length === 0) {
    return (
      <div className="rounded-lg border border-gray-200 bg-white p-8 text-center">
        <Calendar className="mx-auto h-8 w-8 text-gray-300 mb-2" />
        <p className="text-sm text-gray-500">No summaries available for this project yet.</p>
      </div>
    );
  }

  return (
    <div className="space-y-3">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2 text-sm text-gray-500">
          <Calendar className="h-4 w-4" />
          <span>
            {activeWeeks} active week{activeWeeks !== 1 ? "s" : ""} of {timeline.total_weeks} total
          </span>
        </div>
        <div className="flex gap-2">
          <button onClick={expandAll} className="text-xs text-blue-600 hover:text-blue-800">
            Expand all
          </button>
          <span className="text-xs text-gray-300">|</span>
          <button onClick={collapseAll} className="text-xs text-blue-600 hover:text-blue-800">
            Collapse all
          </button>
        </div>
      </div>

      {timeline.weeks.map((week, idx) => {
        const isOpen = expanded.has(idx);
        const empty = isEmptyWeek(week);
        const hasReport = !!week.weekly_report_content;
        const callsOpen = callListExpanded.has(idx);

        return (
          <div
            key={week.week_start}
            className={`overflow-hidden rounded-lg border ${
              empty ? "border-gray-100 bg-gray-50/50" : "border-gray-200 bg-white"
            }`}
          >
            <button
              onClick={() => !empty && toggle(idx)}
              className={`flex w-full items-center justify-between px-5 py-3 text-left transition-colors ${
                empty ? "cursor-default" : "cursor-pointer hover:bg-gray-50"
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
                <span className={`text-sm font-semibold ${empty ? "text-gray-400" : "text-gray-900"}`}>
                  {week.week_label}
                </span>
                {hasReport && !isOpen && (
                  <span className="inline-flex items-center gap-1 rounded-full bg-indigo-50 px-2 py-0.5 text-[10px] font-medium text-indigo-700">
                    <BookOpen className="h-3 w-3" />
                    Weekly summary
                  </span>
                )}
                {empty && (
                  <span className="text-xs italic text-gray-400">No activity this week</span>
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

            {!isOpen && !empty && !hasReport && week.transcripts.length > 0 && (
              <div className="-mt-1 px-5 pb-3">
                <p className="pl-6 text-xs text-gray-400 line-clamp-2">
                  {week.transcripts
                    .filter((t) => t.summary_tldr)
                    .map((t) => t.title || t.file_name)
                    .join(" \u00b7 ") || ""}
                </p>
              </div>
            )}

            {isOpen && !empty && (
              <div className="border-t border-gray-100">
                {hasReport && (() => {
                  const filtered = extractProjectContent(week.weekly_report_content!, project.name);
                  return (
                    <div className="px-6 py-5">
                      <div className="mb-3 flex items-center justify-between">
                        <div className="flex items-center gap-2">
                          <BookOpen className="h-4 w-4 text-indigo-600" />
                          <span className="text-sm font-semibold text-gray-900">Weekly Report</span>
                        </div>
                        {week.weekly_report_id && (
                          <Link
                            href={`/analysis/weekly/${week.weekly_report_id}`}
                            className="flex items-center gap-1 text-xs text-gray-400 hover:text-indigo-600 transition-colors"
                          >
                            Full report <ExternalLink className="h-3 w-3" />
                          </Link>
                        )}
                      </div>
                      {filtered ? (
                        <div className="prose prose-sm max-w-none prose-headings:text-gray-900 prose-h2:mt-6 prose-h2:mb-3 prose-h2:text-base prose-h3:mt-4 prose-h3:mb-2 prose-h3:text-sm prose-p:text-gray-700 prose-li:text-gray-700 prose-strong:text-gray-900">
                          <MarkdownContent>{filtered}</MarkdownContent>
                        </div>
                      ) : (
                        <p className="text-sm text-gray-400 italic">No project-specific updates this week.</p>
                      )}
                    </div>
                  );
                })()}

                {week.transcripts.length > 0 && (
                  <div className={`border-t border-gray-100 ${hasReport ? "bg-gray-50/30" : ""}`}>
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
                        ({week.transcripts.length} call{week.transcripts.length !== 1 ? "s" : ""})
                      </span>
                    </button>

                    {callsOpen && (
                      <div className="divide-y divide-gray-50">
                        {week.transcripts.map((t) => {
                          const callKey = `${idx}-${t.id}`;
                          const callOpen = expandedCalls.has(callKey);

                          return (
                            <div key={t.id} className="px-5 py-3">
                              <div className="flex items-center gap-2">
                                <FileText className="h-4 w-4 flex-shrink-0 text-blue-500" />
                                <Link
                                  href={`/transcripts/${t.id}`}
                                  className="text-sm font-semibold text-blue-700 hover:underline"
                                >
                                  {t.title || t.file_name}
                                </Link>
                                {t.date && (
                                  <span className="text-xs text-gray-400">{t.date}</span>
                                )}
                                <div className="ml-auto flex flex-shrink-0 items-center gap-1.5">
                                  {t.participant_count > 0 && (
                                    <span className="text-[10px] text-gray-400">
                                      {t.participant_count} participants
                                    </span>
                                  )}
                                  {t.word_count > 0 && (
                                    <span className="text-[10px] text-gray-400">
                                      · ~{Math.round(t.word_count / 150)} min
                                    </span>
                                  )}
                                </div>
                              </div>

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
                                    {callOpen ? "Hide" : "Show"} detailed summary
                                  </button>

                                  {callOpen ? (
                                    <div className="rounded-md border border-gray-100 bg-white p-4">
                                      <MarkdownContent>{t.summary_content}</MarkdownContent>
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
              </div>
            )}
          </div>
        );
      })}
    </div>
  );
}
