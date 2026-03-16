"use client";

import { useMemo } from "react";
import { useRouter, usePathname } from "next/navigation";
import type {
  ProjectWeeklyTimeline,
  ProjectBase,
  ProjectHub,
  ProjectSummarySchema,
} from "@/lib/types";
import { getStatusColor } from "@/lib/utils";
import MarkdownContent from "@/components/MarkdownContent";
import {
  CheckSquare,
  Gavel,
  AlertCircle,
  FileText,
  Activity,
  Clock,
  ArrowRight,
  AlertTriangle,
  MessageSquarePlus,
  MessageSquare,
} from "lucide-react";
import Link from "next/link";

interface Props {
  project: ProjectBase;
  hub: ProjectHub;
  timeline: ProjectWeeklyTimeline | null;
}

function extractProjectStatus(
  markdown: string,
  projectName: string,
): string {
  if (!projectName) return "";

  // Build match terms from the project name — match on significant keywords
  const terms = projectName
    .toLowerCase()
    .split(/[\s/()]+/)
    .filter((w) => w.length > 2);

  const lines = markdown.split("\n");
  const prefix = "### ";
  const parentPrefix = "## ";
  let capturing = false;
  const wsContent: string[] = [];
  for (const line of lines) {
    if (line.startsWith(prefix)) {
      if (capturing) break;
      const heading = line.slice(prefix.length).toLowerCase();
      // Match if the heading contains any significant term from the project name
      if (terms.some((term) => heading.includes(term))) {
        capturing = true;
        continue;
      }
    } else if (capturing && line.startsWith(parentPrefix)) {
      break;
    }
    if (capturing) wsContent.push(line);
  }
  return wsContent.join("\n").trim();
}

function formatStatusDate(dateStr: string): string {
  try {
    const d = new Date(dateStr + "T00:00:00");
    return d.toLocaleDateString("en-GB", {
      day: "numeric",
      month: "short",
      year: "numeric",
    });
  } catch {
    return dateStr;
  }
}

function relevanceBadge(relevance: string | null) {
  if (!relevance) return null;
  const colors: Record<string, string> = {
    HIGH: "bg-blue-100 text-forest-600 dark:bg-blue-900/40 dark:text-blue-300",
    MEDIUM: "bg-forest-100 text-forest-500 dark:bg-forest-800 dark:text-forest-300",
    LOW: "bg-forest-50 text-forest-300 dark:bg-forest-900 dark:text-forest-400",
  };
  return (
    <span className={`text-[10px] font-semibold px-1.5 py-0.5 rounded ${colors[relevance] || colors.MEDIUM}`}>
      {relevance}
    </span>
  );
}

/** Normalise ProjectSummary content — handles both old semicolon format and new bullet format. */
function normaliseContent(content: string): string {
  // New format: already has markdown bullets
  if (content.includes("\n- ")) return content;
  // Old format: semicolon-separated points → convert to markdown bullets
  if (content.includes("; ")) {
    return content.split("; ").map((p) => `- ${p.trim()}`).join("\n");
  }
  // Single point without bullets or semicolons
  return `- ${content}`;
}

export default function ProjectOverviewTab({ project, hub, timeline }: Props) {
  const router = useRouter();
  const pathname = usePathname();

  const navigateToTab = (tab: string) => {
    router.push(`${pathname}?tab=${tab}`);
  };

  const stats = [
    {
      label: "Tasks",
      count: project.action_count,
      icon: CheckSquare,
      color: "text-green-600 bg-green-50 border-green-200",
      tab: "tasks",
      detail: `${hub.action_items.filter((a) => ["open", "in progress", "todo", "in_progress"].includes((a.status || "").toLowerCase())).length} open`,
    },
    {
      label: "Decisions",
      count: project.decision_count,
      icon: Gavel,
      color: "text-amber-600 bg-amber-50 border-amber-200",
      tab: "decisions",
    },
    {
      label: "Threads",
      count: project.open_thread_count,
      icon: AlertCircle,
      color: "text-red-600 bg-red-50 border-red-200",
      tab: "threads",
      detail: `${hub.open_threads.filter((t) => t.status === "OPEN").length} open`,
    },
    {
      label: "Summaries",
      count: project.transcript_count,
      icon: FileText,
      color: "text-forest-500 bg-blue-50 border-blue-200",
      tab: "summaries",
    },
  ];

  // Map transcript_id → title for meeting title lookup
  const transcriptTitles = useMemo(() => {
    const map = new Map<number, string>();
    for (const t of hub.transcripts || []) if (t.title) map.set(t.id, t.title);
    return map;
  }, [hub.transcripts]);

  // Map project_update_id → title for update title lookup
  const updateTitles = useMemo(() => {
    const map = new Map<number, string>();
    for (const u of hub.project_updates || []) if (u.title) map.set(u.id, u.title);
    return map;
  }, [hub.project_updates]);

  const statusEntries = useMemo(() => {
    const summaries = hub.project_summaries || [];
    if (summaries.length > 0) {
      // Group ProjectSummary entries by date, most recent first
      const grouped = new Map<string, ProjectSummarySchema[]>();
      for (const s of summaries) {
        const key = s.date || "Unknown";
        if (!grouped.has(key)) grouped.set(key, []);
        grouped.get(key)!.push(s);
      }
      return Array.from(grouped.entries())
        .sort((a, b) => b[0].localeCompare(a[0]))
        .slice(0, 5)
        .map(([date, items]) => ({ type: "summary" as const, date, items }));
    }

    // Fallback: extract from weekly reports if no ProjectSummary entries exist
    if (!timeline) return null;
    for (const week of timeline.weeks) {
      if (week.weekly_report_content) {
        const status = extractProjectStatus(week.weekly_report_content, project.name);
        if (status) return [{ type: "legacy" as const, content: status, weekLabel: week.week_label }];
      }
    }
    return null;
  }, [hub.project_summaries, timeline, project.name]);

  const recentActivity = useMemo(() => {
    const items: { type: string; title: string; date: string | null; status: string; tab: string }[] = [];

    hub.action_items.slice(0, 5).forEach((a) => {
      items.push({
        type: "task",
        title: a.description || a.title,
        date: a.due_date || null,
        status: a.status,
        tab: "tasks",
      });
    });

    hub.decisions.slice(0, 5).forEach((d) => {
      items.push({
        type: "decision",
        title: d.title || d.description || `Decision #${d.id}`,
        date: d.date || null,
        status: d.execution_status || "made",
        tab: "decisions",
      });
    });

    hub.open_threads.slice(0, 5).forEach((t) => {
      items.push({
        type: "thread",
        title: t.title,
        date: t.opened_date || null,
        status: t.status,
        tab: "threads",
      });
    });

    return items.slice(0, 10);
  }, [hub]);

  const attentionItems = useMemo(() => {
    const items: { title: string; severity?: string }[] = [];

    hub.open_threads
      .filter((t) => t.status === "OPEN" && (t.severity === "CRITICAL" || t.severity === "HIGH"))
      .forEach((t) => {
        items.push({ title: t.title, severity: t.severity || undefined });
      });

    return items.slice(0, 5);
  }, [hub]);

  const typeIcons: Record<string, typeof CheckSquare> = {
    task: CheckSquare,
    decision: Gavel,
    thread: AlertCircle,
  };

  return (
    <div className="space-y-6">
      {/* Stat cards */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        {stats.map((stat) => {
          const Icon = stat.icon;
          return (
            <button
              key={stat.label}
              onClick={() => navigateToTab(stat.tab)}
              className={`rounded-lg border p-4 text-left transition-all hover:shadow-md ${stat.color}`}
            >
              <div className="flex items-center justify-between">
                <Icon className="h-5 w-5" />
                <ArrowRight className="h-4 w-4 opacity-50" />
              </div>
              <p className="mt-3 text-2xl font-bold">{stat.count}</p>
              <p className="text-sm font-medium">{stat.label}</p>
              {stat.detail && (
                <p className="text-[10px] opacity-75 mt-0.5">{stat.detail}</p>
              )}
            </button>
          );
        })}
      </div>

      {/* Current Status */}
      {statusEntries && statusEntries.length > 0 && (
        <div className="rounded-lg border border-blue-200 bg-gradient-to-br from-blue-50/80 to-white p-6">
          <h3 className="flex items-center gap-2 text-base font-semibold text-forest-950 mb-4">
            <Activity className="h-4 w-4 text-forest-500" />
            Current Status
          </h3>
          <div className="space-y-4">
            {statusEntries.map((entry, i) => {
              if (entry.type === "legacy") {
                return (
                  <div key={i}>
                    <span className="text-sm text-forest-300 mb-2 block">as of {entry.weekLabel}</span>
                    <div className="prose prose-sm max-w-none prose-headings:text-forest-950 prose-h2:mt-4 prose-h2:mb-2 prose-h2:text-base prose-h2:font-semibold prose-p:text-forest-600 prose-li:text-forest-600 prose-strong:text-forest-950">
                      <MarkdownContent>{entry.content}</MarkdownContent>
                    </div>
                  </div>
                );
              }
              return (
                <div key={entry.date} className={i > 0 ? "border-t border-blue-100 dark:border-forest-700 pt-4" : ""}>
                  <div className="mb-3 flex items-center gap-2">
                    <span className="text-sm font-medium text-forest-500 dark:text-forest-300">{formatStatusDate(entry.date)}</span>
                  </div>
                  <div className="space-y-3">
                    {entry.items.map((s) => {
                      const isUpdate = !s.transcript_id && !!s.project_update_id;
                      const title = s.transcript_id
                        ? transcriptTitles.get(s.transcript_id)
                        : s.project_update_id
                          ? updateTitles.get(s.project_update_id)
                          : undefined;
                      return (
                        <div key={s.id} className="border-l-2 border-blue-300 dark:border-blue-700 pl-4 py-1">
                          <div className="flex items-center gap-2 mb-1.5">
                            {title && (
                              <span className="text-sm font-medium text-forest-800 dark:text-forest-100">{title}</span>
                            )}
                            {isUpdate && (
                              <span className="text-[10px] font-semibold px-1.5 py-0.5 rounded bg-purple-100 text-purple-700 dark:bg-purple-900/40 dark:text-purple-300">
                                Update
                              </span>
                            )}
                            {relevanceBadge(s.relevance)}
                          </div>
                          <div className="prose prose-sm max-w-none prose-headings:text-forest-950 dark:prose-headings:text-forest-50 prose-p:text-forest-600 dark:prose-p:text-forest-300 prose-li:text-forest-600 dark:prose-li:text-forest-300 prose-strong:text-forest-950 dark:prose-strong:text-forest-100">
                            <MarkdownContent>{normaliseContent(s.content)}</MarkdownContent>
                          </div>
                        </div>
                      );
                    })}
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      )}

      {/* Attention Required */}
      {attentionItems.length > 0 && (
        <div className="rounded-lg border border-orange-200 bg-orange-50/50 p-5">
          <h3 className="flex items-center gap-2 text-base font-semibold text-forest-950 mb-3">
            <AlertTriangle className="h-4 w-4 text-orange-600" />
            Attention Required
          </h3>
          <div className="space-y-2">
            {attentionItems.map((item, i) => (
              <div key={i} className="flex items-start gap-2 text-base">
                <AlertCircle className="h-4 w-4 flex-shrink-0 text-orange-500 mt-0.5" />
                <div>
                  <span className="text-forest-950">{item.title}</span>
                  {item.severity && (
                    <span className={`ml-2 text-[10px] font-semibold px-1.5 py-0.5 rounded ${
                      item.severity === "CRITICAL" ? "bg-red-100 text-red-700" : "bg-orange-100 text-orange-700"
                    }`}>
                      {item.severity}
                    </span>
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Project Updates */}
      {hub.project_updates && hub.project_updates.length > 0 && (
        <div className="rounded-lg border border-forest-200 bg-white dark:bg-forest-800">
          <div className="border-b border-gray-100 dark:border-forest-700 px-5 py-4 flex items-center justify-between">
            <h3 className="flex items-center gap-2 text-base font-semibold text-forest-950 dark:text-forest-50">
              <MessageSquarePlus className="h-4 w-4 text-forest-400" />
              Recent Updates
            </h3>
            <Link
              href="/updates"
              className="text-xs text-forest-500 hover:text-forest-700 dark:hover:text-forest-300"
            >
              View all
            </Link>
          </div>
          <div className="divide-y divide-gray-50 dark:divide-forest-700">
            {hub.project_updates.slice(0, 5).map((u) => (
              <Link
                key={u.id}
                href={`/updates/${u.id}`}
                className="flex items-start gap-3 px-5 py-3 hover:bg-forest-50 dark:hover:bg-forest-700/50 transition-colors"
              >
                {u.content_type === "teams_chat" ? (
                  <MessageSquare className="h-4 w-4 flex-shrink-0 text-blue-400 mt-0.5" />
                ) : (
                  <FileText className="h-4 w-4 flex-shrink-0 text-forest-300 mt-0.5" />
                )}
                <div className="min-w-0 flex-1">
                  <p className="text-sm text-forest-900 dark:text-forest-100 truncate">{u.title}</p>
                  <p className="text-xs text-forest-400 mt-0.5">
                    {new Date(u.created_at).toLocaleDateString()}
                  </p>
                </div>
              </Link>
            ))}
          </div>
        </div>
      )}

      {/* Recent Activity */}
      {recentActivity.length > 0 && (
        <div className="rounded-lg border border-forest-200 bg-white dark:bg-forest-800">
          <div className="border-b border-gray-100 px-5 py-4">
            <h3 className="flex items-center gap-2 text-base font-semibold text-forest-950">
              <Clock className="h-4 w-4 text-forest-400" />
              Recent Activity
            </h3>
          </div>
          <div className="divide-y divide-gray-50">
            {recentActivity.map((item, i) => {
              const TypeIcon = typeIcons[item.type] || FileText;
              return (
                <button
                  key={i}
                  onClick={() => navigateToTab(item.tab)}
                  className="flex w-full items-start gap-3 px-5 py-3 text-left hover:bg-forest-50 transition-colors"
                >
                  <TypeIcon className="h-4 w-4 flex-shrink-0 text-forest-300 mt-0.5" />
                  <div className="min-w-0 flex-1">
                    <p className="text-base text-forest-950 truncate">{item.title}</p>
                    <div className="mt-0.5 flex items-center gap-2">
                      <span className="text-[10px] text-forest-300 capitalize">{item.type}</span>
                      {item.date && (
                        <span className="text-[10px] text-forest-300">{item.date}</span>
                      )}
                    </div>
                  </div>
                  <span className={`inline-flex flex-shrink-0 rounded-full border px-2 py-0.5 text-[10px] font-medium ${getStatusColor(item.status)}`}>
                    {item.status}
                  </span>
                </button>
              );
            })}
          </div>
        </div>
      )}
    </div>
  );
}
