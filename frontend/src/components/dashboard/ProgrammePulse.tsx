"use client";

import { useState } from "react";
import Link from "next/link";
import { ragDotColor, formatDate } from "@/lib/utils";
import type { DashboardProjectCard } from "@/lib/types";
import { ChevronDown, ChevronUp, TrendingUp, TrendingDown, Minus } from "lucide-react";

function TrendIcon({ trend }: { trend: "up" | "down" | "flat" }) {
  if (trend === "up") return <TrendingUp className="h-3.5 w-3.5 text-green-600" />;
  if (trend === "down") return <TrendingDown className="h-3.5 w-3.5 text-red-500" />;
  return <Minus className="h-3.5 w-3.5 text-gray-400" />;
}

interface Props {
  projects: DashboardProjectCard[];
}

function sortProjects(projects: DashboardProjectCard[]): DashboardProjectCard[] {
  return [...projects].sort((a, b) => a.name.localeCompare(b.name));
}

export default function ProgrammePulse({ projects }: Props) {
  const [expandedId, setExpandedId] = useState<number | null>(null);
  const sorted = sortProjects(projects);

  return (
    <section>
      <h3 className="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-3">
        Programme Pulse
      </h3>
      <div className="grid grid-cols-2 gap-3 sm:grid-cols-3 lg:grid-cols-6">
        {sorted.map((p) => {
          const isExpanded = expandedId === p.id;
          return (
            <div
              key={p.id}
              className="rounded-lg border border-gray-200 bg-white transition-all hover:shadow-md hover:border-gray-300"
            >
              {/* Card header — clickable to expand */}
              <button
                onClick={() => setExpandedId(isExpanded ? null : p.id)}
                className="w-full text-left p-4"
              >
                <div className="flex items-center gap-2 mb-1.5">
                  <span
                    className={`h-2.5 w-2.5 rounded-full flex-shrink-0 ${ragDotColor(p.status)}`}
                  />
                  <span className="text-sm font-semibold text-gray-900 truncate">
                    {p.name}
                  </span>
                  {isExpanded ? (
                    <ChevronUp className="h-3.5 w-3.5 text-gray-400 ml-auto flex-shrink-0" />
                  ) : (
                    <ChevronDown className="h-3.5 w-3.5 text-gray-400 ml-auto flex-shrink-0" />
                  )}
                </div>
                <p className="text-[11px] text-gray-500 truncate mb-2">
                  {p.status}
                </p>
                <div className="flex items-center justify-between">
                  <span className="text-xs text-gray-600">
                    {p.action_count} action{p.action_count !== 1 ? "s" : ""}
                  </span>
                  <TrendIcon trend={p.trend} />
                </div>
                {p.last_activity_date && (
                  <p className="mt-1 text-[10px] text-gray-400">
                    {formatDate(p.last_activity_date)}
                  </p>
                )}
              </button>

              {/* Expanded details */}
              {isExpanded && (
                <div className="border-t border-gray-100 px-4 py-3 space-y-2 bg-gray-50/50">
                  <div className="grid grid-cols-2 gap-2 text-xs">
                    <div>
                      <span className="text-gray-500">Transcripts</span>
                      <span className="ml-1 font-semibold text-gray-900">
                        {p.transcript_count}
                      </span>
                    </div>
                    <div>
                      <span className="text-gray-500">Decisions</span>
                      <span className="ml-1 font-semibold text-gray-900">
                        {p.decision_count}
                      </span>
                    </div>
                    <div>
                      <span className="text-gray-500">Actions</span>
                      <span className="ml-1 font-semibold text-gray-900">
                        {p.action_count}
                      </span>
                    </div>
                    <div>
                      <span className="text-gray-500">Threads</span>
                      <span className="ml-1 font-semibold text-gray-900">
                        {p.open_thread_count}
                      </span>
                    </div>
                  </div>
                  <Link
                    href={`/projects/${p.id}`}
                    className="block text-center text-xs font-medium text-blue-600 hover:text-blue-800 pt-1"
                  >
                    View Project →
                  </Link>
                </div>
              )}
            </div>
          );
        })}
      </div>
    </section>
  );
}
