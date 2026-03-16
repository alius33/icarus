"use client";

import Link from "next/link";
import { ragDotColor, formatDate } from "@/lib/utils";
import type { DashboardProjectCard } from "@/lib/types";
import { TrendingUp, TrendingDown, Minus, FileText, CheckCircle2, GitBranch, MessageSquare } from "lucide-react";

function TrendIcon({ trend }: { trend: "up" | "down" | "flat" }) {
  if (trend === "up") return <TrendingUp className="h-4 w-4 text-green-600" />;
  if (trend === "down") return <TrendingDown className="h-4 w-4 text-red-500" />;
  return <Minus className="h-4 w-4 text-forest-300" />;
}

interface Props {
  projects: DashboardProjectCard[];
}

export default function ProgrammePulse({ projects }: Props) {
  const sorted = [...projects].sort((a, b) => a.name.localeCompare(b.name));

  return (
    <div className="grid grid-cols-1 gap-5 md:grid-cols-2 lg:grid-cols-3">
      {sorted.map((p) => (
        <Link
          key={p.id}
          href={`/projects/${p.id}`}
          className="group block rounded-xl border border-forest-200 bg-white dark:bg-forest-800 p-5 transition-all hover:shadow-lg hover:border-forest-200 hover:-translate-y-0.5"
        >
          {/* Header: RAG dot + name + trend */}
          <div className="flex items-start justify-between mb-2">
            <div className="flex items-center gap-2.5 min-w-0">
              <span className={`h-3 w-3 rounded-full flex-shrink-0 ${ragDotColor(p.status)}`} />
              <h3 className="text-base font-semibold text-forest-950 truncate group-hover:text-forest-600 transition-colors">
                {p.name}
              </h3>
            </div>
            <TrendIcon trend={p.trend} />
          </div>

          {/* Status text */}
          <p className="text-base text-forest-400 mb-4 ml-5.5 truncate">
            {p.status}
          </p>

          {/* 2x2 metric grid */}
          <div className="grid grid-cols-2 gap-3 mb-4">
            <div className="flex items-center gap-2 text-base">
              <CheckCircle2 className="h-4 w-4 text-forest-300" />
              <span className="font-semibold text-forest-950">{p.action_count}</span>
              <span className="text-forest-400">Actions</span>
            </div>
            <div className="flex items-center gap-2 text-base">
              <GitBranch className="h-4 w-4 text-forest-300" />
              <span className="font-semibold text-forest-950">{p.decision_count}</span>
              <span className="text-forest-400">Decisions</span>
            </div>
            <div className="flex items-center gap-2 text-base">
              <MessageSquare className="h-4 w-4 text-forest-300" />
              <span className="font-semibold text-forest-950">{p.open_thread_count}</span>
              <span className="text-forest-400">Threads</span>
            </div>
            <div className="flex items-center gap-2 text-base">
              <FileText className="h-4 w-4 text-forest-300" />
              <span className="font-semibold text-forest-950">{p.transcript_count}</span>
              <span className="text-forest-400">Transcripts</span>
            </div>
          </div>

          {/* Footer: last activity */}
          {p.last_activity_date && (
            <p className="text-sm text-forest-300 border-t border-gray-100 pt-3">
              Last activity {formatDate(p.last_activity_date)}
            </p>
          )}
        </Link>
      ))}
    </div>
  );
}
