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
} from "lucide-react";

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
    HIGH: "bg-blue-100 text-blue-700",
    MEDIUM: "bg-gray-100 text-gray-600",
    LOW: "bg-gray-50 text-gray-400",
  };
  return (
    <span className={`text-[10px] font-semibold px-1.5 py-0.5 rounded ${colors[relevance] || colors.MEDIUM}`}>
      {relevance}
    </span>
  );
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
      color: "text-blue-600 bg-blue-50 border-blue-200",
      tab: "summaries",
    },
  ];

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
              <p className="text-xs font-medium">{stat.label}</p>
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
          <h3 className="flex items-center gap-2 text-sm font-semibold text-gray-900 mb-4">
            <Activity className="h-4 w-4 text-blue-600" />
            Current Status
          </h3>
          <div className="space-y-4">
            {statusEntries.map((entry, i) => {
              if (entry.type === "legacy") {
                return (
                  <div key={i}>
                    <span className="text-xs text-gray-400 mb-2 block">as of {entry.weekLabel}</span>
                    <div className="prose prose-sm max-w-none prose-headings:text-gray-900 prose-h2:mt-4 prose-h2:mb-2 prose-h2:text-sm prose-h2:font-semibold prose-p:text-gray-700 prose-li:text-gray-700 prose-strong:text-gray-900">
                      <MarkdownContent>{entry.content}</MarkdownContent>
                    </div>
                  </div>
                );
              }
              return (
                <div key={entry.date} className={i > 0 ? "border-t border-blue-100 pt-4" : ""}>
                  <div className="mb-2 flex items-center gap-2">
                    <span className="text-xs font-medium text-gray-600">{formatStatusDate(entry.date)}</span>
                  </div>
                  {entry.items.map((s) => (
                    <div key={s.id} className="mb-2 last:mb-0">
                      <div className="flex items-center gap-2 mb-1">
                        {relevanceBadge(s.relevance)}
                      </div>
                      <div className="prose prose-sm max-w-none prose-headings:text-gray-900 prose-p:text-gray-700 prose-li:text-gray-700 prose-strong:text-gray-900">
                        <MarkdownContent>{s.content}</MarkdownContent>
                      </div>
                    </div>
                  ))}
                </div>
              );
            })}
          </div>
        </div>
      )}

      {/* Attention Required */}
      {attentionItems.length > 0 && (
        <div className="rounded-lg border border-orange-200 bg-orange-50/50 p-5">
          <h3 className="flex items-center gap-2 text-sm font-semibold text-gray-900 mb-3">
            <AlertTriangle className="h-4 w-4 text-orange-600" />
            Attention Required
          </h3>
          <div className="space-y-2">
            {attentionItems.map((item, i) => (
              <div key={i} className="flex items-start gap-2 text-sm">
                <AlertCircle className="h-4 w-4 flex-shrink-0 text-orange-500 mt-0.5" />
                <div>
                  <span className="text-gray-900">{item.title}</span>
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

      {/* Recent Activity */}
      {recentActivity.length > 0 && (
        <div className="rounded-lg border border-gray-200 bg-white">
          <div className="border-b border-gray-100 px-5 py-4">
            <h3 className="flex items-center gap-2 text-sm font-semibold text-gray-900">
              <Clock className="h-4 w-4 text-gray-500" />
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
                  className="flex w-full items-start gap-3 px-5 py-3 text-left hover:bg-gray-50 transition-colors"
                >
                  <TypeIcon className="h-4 w-4 flex-shrink-0 text-gray-400 mt-0.5" />
                  <div className="min-w-0 flex-1">
                    <p className="text-sm text-gray-900 truncate">{item.title}</p>
                    <div className="mt-0.5 flex items-center gap-2">
                      <span className="text-[10px] text-gray-400 capitalize">{item.type}</span>
                      {item.date && (
                        <span className="text-[10px] text-gray-400">{item.date}</span>
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
