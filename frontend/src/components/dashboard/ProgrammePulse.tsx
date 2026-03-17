"use client";

import Link from "next/link";
import { ragDotColor, formatDate, cn } from "@/lib/utils";
import { useDeliverableOverview } from "@/lib/swr";
import type { DashboardProjectCard } from "@/lib/types";
import {
  TrendingUp,
  TrendingDown,
  Minus,
  FileText,
  CheckCircle2,
  GitBranch,
  MessageSquare,
} from "lucide-react";

// Programme Management identified by name (IDs differ across environments)
const PM_NAME = "Program Management";

// Canonical project-to-pillar mapping — single source of truth for categorisation.
// Always used (not just fallback) so the dashboard stays correct regardless of
// whether deliverables have project_id set in the database.
const PILLAR_NAME_MAP: Record<string, number> = {
  // Pillar 1: IRP Portfolio Governance
  "CLARA (IRP Adoption Tracker)": 1,
  // Pillar 2: Platform-Embedded Customer Intelligence
  "Customer Success Agent": 2,
  "Navigator L1 Automation": 2,
  // Pillar 3: Internal Productivity & Revenue Acceleration
  "Build in Five": 3,
  "App Factory": 3,
  "Slidey (AI Presentations)": 3,
  "Training & Enablement": 3,
  "Cross OU Collaboration": 3,
};

function TrendIcon({ trend }: { trend: "up" | "down" | "flat" }) {
  if (trend === "up") return <TrendingUp className="h-4 w-4 text-green-600" />;
  if (trend === "down")
    return <TrendingDown className="h-4 w-4 text-red-500" />;
  return <Minus className="h-4 w-4 text-forest-300" />;
}

/* ── Compact project card (reused for priority + other sections) ─────── */
function ProjectCard({ p }: { p: DashboardProjectCard }) {
  return (
    <Link
      href={`/projects/${p.id}`}
      className="group block rounded-xl border border-forest-200 bg-white p-5 transition-all hover:shadow-lg hover:border-forest-300 hover:-translate-y-0.5"
      style={{
        borderLeftWidth: "4px",
        borderLeftColor: p.color || "#6b7280",
      }}
    >
      <div className="flex items-start justify-between mb-2">
        <div className="flex items-center gap-2.5 min-w-0">
          <span
            className={`h-3 w-3 rounded-full flex-shrink-0 ${ragDotColor(p.status)}`}
          />
          <h3 className="text-base font-semibold text-forest-950 truncate group-hover:text-forest-600 transition-colors">
            {p.name}
          </h3>
        </div>
        <TrendIcon trend={p.trend} />
      </div>

      <p className="text-sm text-forest-400 mb-4 ml-5.5 truncate">
        {p.status}
      </p>

      <div className="grid grid-cols-2 gap-3 mb-4">
        <div className="flex items-center gap-2 text-sm">
          <CheckCircle2 className="h-4 w-4 text-forest-300" />
          <span className="font-semibold text-forest-950">
            {p.action_count}
          </span>
          <span className="text-forest-400">Actions</span>
        </div>
        <div className="flex items-center gap-2 text-sm">
          <GitBranch className="h-4 w-4 text-forest-300" />
          <span className="font-semibold text-forest-950">
            {p.decision_count}
          </span>
          <span className="text-forest-400">Decisions</span>
        </div>
        <div className="flex items-center gap-2 text-sm">
          <MessageSquare className="h-4 w-4 text-forest-300" />
          <span className="font-semibold text-forest-950">
            {p.open_thread_count}
          </span>
          <span className="text-forest-400">Threads</span>
        </div>
        <div className="flex items-center gap-2 text-sm">
          <FileText className="h-4 w-4 text-forest-300" />
          <span className="font-semibold text-forest-950">
            {p.transcript_count}
          </span>
          <span className="text-forest-400">Transcripts</span>
        </div>
      </div>

      {p.last_activity_date && (
        <p className="text-xs text-forest-300 border-t border-gray-100 pt-3">
          Last activity {formatDate(p.last_activity_date)}
        </p>
      )}
    </Link>
  );
}

/* ── Programme Management card (full-width, with latest summary) ─────── */
function ProgrammeManagementCard({ p }: { p: DashboardProjectCard }) {
  return (
    <Link
      href={`/projects/${p.id}`}
      className="group block rounded-xl border border-forest-200 bg-white p-6 transition-all hover:shadow-lg hover:border-forest-300"
      style={{
        borderLeftWidth: "4px",
        borderLeftColor: p.color || "#091164",
      }}
    >
      <div className="flex items-start justify-between mb-3">
        <div className="flex items-center gap-2.5">
          <span
            className={`h-3.5 w-3.5 rounded-full flex-shrink-0 ${ragDotColor(p.status)}`}
          />
          <h3 className="text-lg font-bold text-forest-950 group-hover:text-forest-600 transition-colors">
            {p.name}
          </h3>
        </div>
        <TrendIcon trend={p.trend} />
      </div>

      <div className="flex flex-col md:flex-row gap-6">
        {/* Metrics */}
        <div className="flex gap-6 flex-shrink-0">
          <div className="text-center">
            <p className="text-2xl font-bold text-forest-950">
              {p.action_count}
            </p>
            <p className="text-xs text-forest-400">Actions</p>
          </div>
          <div className="text-center">
            <p className="text-2xl font-bold text-forest-950">
              {p.decision_count}
            </p>
            <p className="text-xs text-forest-400">Decisions</p>
          </div>
          <div className="text-center">
            <p className="text-2xl font-bold text-forest-950">
              {p.open_thread_count}
            </p>
            <p className="text-xs text-forest-400">Threads</p>
          </div>
          <div className="text-center">
            <p className="text-2xl font-bold text-forest-950">
              {p.transcript_count}
            </p>
            <p className="text-xs text-forest-400">Transcripts</p>
          </div>
        </div>

        {/* Latest summary */}
        {p.latest_summary && (
          <div className="flex-1 border-l border-forest-100 pl-6 min-w-0">
            <p className="text-xs font-medium text-forest-400 mb-1">
              Latest update
              {p.latest_summary_date &&
                ` — ${formatDate(p.latest_summary_date)}`}
            </p>
            <p className="text-sm text-forest-600 line-clamp-3">
              {p.latest_summary}
            </p>
          </div>
        )}
      </div>
    </Link>
  );
}

/* ── Pillar header with RAG dot + progress bar ─────────────────────── */
const RAG_COLORS: Record<string, string> = {
  GREEN: "bg-green-500",
  AMBER: "bg-amber-500",
  RED: "bg-red-500",
};

function PillarHeader({
  name,
  rag,
  progress,
  completed,
  total,
}: {
  name: string;
  rag: string;
  progress: number;
  completed: number;
  total: number;
}) {
  return (
    <div className="flex items-center gap-3 mb-3">
      <div
        className={cn(
          "h-2.5 w-2.5 rounded-full flex-shrink-0",
          RAG_COLORS[rag] || "bg-gray-400"
        )}
      />
      <h3 className="text-sm font-semibold text-forest-700 uppercase tracking-wide flex-shrink-0">
        {name}
      </h3>
      <div className="flex-1 h-1.5 bg-gray-200 rounded-full overflow-hidden max-w-48">
        <div
          className="h-full bg-forest-500 rounded-full transition-all"
          style={{ width: `${progress}%` }}
        />
      </div>
      <span className="text-xs text-forest-400 tabular-nums whitespace-nowrap">
        {completed}/{total} milestones
      </span>
    </div>
  );
}

/* ── Main component ──────────────────────────────────────────────────── */

interface Props {
  projects: DashboardProjectCard[];
}

export default function ProgrammePulse({ projects }: Props) {
  const { data: deliverableData } = useDeliverableOverview();

  const pillars = deliverableData?.pillars || [];

  // Priority = any project in PILLAR_NAME_MAP (always used, not just fallback).
  // Also merge any deliverable-linked project IDs for completeness.
  const nameMapIds = new Set(
    projects
      .filter((p) => p.name in PILLAR_NAME_MAP)
      .map((p) => p.id)
  );
  const deliverableLinkedIds = new Set(
    pillars.flatMap((pillar) =>
      pillar.deliverables
        .map((d) => d.project_id)
        .filter((id): id is number => id !== null)
    )
  );
  const priorityIds = new Set([...nameMapIds, ...deliverableLinkedIds]);

  const pmProject = projects.find((p) => p.name === PM_NAME);
  const pmId = pmProject?.id;

  const priorityProjects = projects.filter(
    (p) => priorityIds.has(p.id) && p.id !== pmId
  );
  const otherProjects = projects.filter(
    (p) => !priorityIds.has(p.id) && p.id !== pmId
  );

  // Group priority projects by pillar — always use PILLAR_NAME_MAP,
  // merge with any deliverable project_id links for completeness
  const pillarProjectMap = new Map<number, DashboardProjectCard[]>();
  for (const pillar of pillars) {
    // Projects matched by name
    const nameMatched = new Set(
      projects
        .filter((p) => PILLAR_NAME_MAP[p.name] === pillar.pillar)
        .map((p) => p.id)
    );
    // Projects linked via deliverables
    const deliverableMatched = new Set(
      pillar.deliverables
        .map((d) => d.project_id)
        .filter((id): id is number => id !== null)
    );
    const pillarProjectIds = new Set([...nameMatched, ...deliverableMatched]);
    const cards = priorityProjects.filter((p) => pillarProjectIds.has(p.id));
    if (cards.length > 0) {
      pillarProjectMap.set(pillar.pillar, cards);
    }
  }

  // Any priority projects not matched to a pillar (fallback before deliverable data loads)
  const matchedIds = new Set(
    Array.from(pillarProjectMap.values())
      .flat()
      .map((p) => p.id)
  );
  const unmatchedPriority = priorityProjects.filter(
    (p) => !matchedIds.has(p.id)
  );

  return (
    <div className="space-y-8">
      {/* Section A: Programme Management */}
      {pmProject && <ProgrammeManagementCard p={pmProject} />}

      {/* Section B: Priority Projects (Diya Deliverables) */}
      <div>
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-sm font-bold text-forest-950 uppercase tracking-wide">
            Priority Projects
          </h2>
          <Link
            href="/weekly-plan?tab=deliverables"
            className="text-xs text-forest-500 hover:underline"
          >
            View deliverables &rarr;
          </Link>
        </div>

        <div className="space-y-6">
          {pillars.map((pillar) => {
            const cards = pillarProjectMap.get(pillar.pillar) || [];
            if (cards.length === 0) return null;

            const totalMilestones = pillar.deliverables.reduce(
              (sum, d) => sum + (d.milestones?.length || 0),
              0
            );
            const completedMilestones = pillar.deliverables.reduce(
              (sum, d) =>
                sum +
                (d.milestones?.filter((m) => m.status === "COMPLETED").length ||
                  0),
              0
            );

            return (
              <div key={pillar.pillar}>
                <PillarHeader
                  name={pillar.pillar_name}
                  rag={pillar.aggregate_rag}
                  progress={pillar.aggregate_progress}
                  completed={completedMilestones}
                  total={totalMilestones}
                />
                <div className="grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-3">
                  {cards.map((p) => (
                    <ProjectCard key={p.id} p={p} />
                  ))}
                </div>
              </div>
            );
          })}

          {/* Unmatched priority projects (if deliverable data hasn't loaded) */}
          {unmatchedPriority.length > 0 && (
            <div className="grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-3">
              {unmatchedPriority.map((p) => (
                <ProjectCard key={p.id} p={p} />
              ))}
            </div>
          )}
        </div>
      </div>

      {/* Section C: Other Projects */}
      {otherProjects.length > 0 && (
        <div>
          <h2 className="text-sm font-bold text-forest-950 uppercase tracking-wide mb-4">
            Other Projects
          </h2>
          <div className="grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-3">
            {otherProjects.map((p) => (
              <ProjectCard key={p.id} p={p} />
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
