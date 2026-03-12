"use client";

import Link from "next/link";
import { ragDotColor, formatDate } from "@/lib/utils";
import type { DashboardProjectCard } from "@/lib/types";
import { TrendingUp, TrendingDown, Minus, FileText, CheckCircle2, GitBranch, MessageSquare } from "lucide-react";

function TrendIcon({ trend }: { trend: "up" | "down" | "flat" }) {
  if (trend === "up") return <TrendingUp className="h-4 w-4 text-green-600" />;
  if (trend === "down") return <TrendingDown className="h-4 w-4 text-red-500" />;
  return <Minus className="h-4 w-4 text-gray-400" />;
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
          className="group block rounded-xl border border-gray-200 bg-white p-5 transition-all hover:shadow-lg hover:border-gray-300 hover:-translate-y-0.5"
        >
          {/* Header: RAG dot + name + trend */}
          <div className="flex items-start justify-between mb-2">
            <div className="flex items-center gap-2.5 min-w-0">
              <span className={`h-3 w-3 rounded-full flex-shrink-0 ${ragDotColor(p.status)}`} />
              <h3 className="text-base font-semibold text-gray-900 truncate group-hover:text-blue-700 transition-colors">
                {p.name}
              </h3>
            </div>
            <TrendIcon trend={p.trend} />
          </div>

          {/* Status text */}
          <p className="text-sm text-gray-500 mb-4 ml-5.5 truncate">
            {p.status}
          </p>

          {/* 2x2 metric grid */}
          <div className="grid grid-cols-2 gap-3 mb-4">
            <div className="flex items-center gap-2 text-sm">
              <CheckCircle2 className="h-4 w-4 text-gray-400" />
              <span className="font-semibold text-gray-900">{p.action_count}</span>
              <span className="text-gray-500">Actions</span>
            </div>
            <div className="flex items-center gap-2 text-sm">
              <GitBranch className="h-4 w-4 text-gray-400" />
              <span className="font-semibold text-gray-900">{p.decision_count}</span>
              <span className="text-gray-500">Decisions</span>
            </div>
            <div className="flex items-center gap-2 text-sm">
              <MessageSquare className="h-4 w-4 text-gray-400" />
              <span className="font-semibold text-gray-900">{p.open_thread_count}</span>
              <span className="text-gray-500">Threads</span>
            </div>
            <div className="flex items-center gap-2 text-sm">
              <FileText className="h-4 w-4 text-gray-400" />
              <span className="font-semibold text-gray-900">{p.transcript_count}</span>
              <span className="text-gray-500">Transcripts</span>
            </div>
          </div>

          {/* Footer: last activity */}
          {p.last_activity_date && (
            <p className="text-xs text-gray-400 border-t border-gray-100 pt-3">
              Last activity {formatDate(p.last_activity_date)}
            </p>
          )}
        </Link>
      ))}
    </div>
  );
}
