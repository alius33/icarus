"use client";

import { useState, useMemo } from "react";
import Link from "next/link";
import {
  MessageSquarePlus,
  FileText,
  MessageSquare,
  Clock,
  FolderKanban,
  CheckCircle2,
  Circle,
} from "lucide-react";
import { useProjectUpdates } from "@/lib/swr";
import type { ProjectUpdateBase } from "@/lib/types";

type ViewMode = "timeline" | "by-project";

function UpdateCard({ update }: { update: ProjectUpdateBase }) {
  const preview = update.content.length > 200
    ? update.content.slice(0, 200) + "..."
    : update.content;

  return (
    <Link href={`/updates/${update.id}`}>
      <div className="bg-white dark:bg-forest-800 border border-forest-200 dark:border-forest-700 rounded-xl p-4 hover:shadow-md transition-shadow cursor-pointer">
        <div className="flex items-start justify-between gap-2 mb-2">
          <h3 className="font-medium text-forest-900 dark:text-forest-100 line-clamp-1">
            {update.content_type === "teams_chat" ? (
              <MessageSquare className="h-4 w-4 inline mr-1 text-blue-500" />
            ) : (
              <FileText className="h-4 w-4 inline mr-1 text-forest-500" />
            )}
            {update.title}
          </h3>
          {update.is_processed ? (
            <CheckCircle2 className="h-4 w-4 text-green-500 shrink-0" />
          ) : (
            <Circle className="h-4 w-4 text-forest-300 shrink-0" />
          )}
        </div>

        <p className="text-sm text-forest-600 dark:text-forest-300 line-clamp-3 mb-3">
          {preview}
        </p>

        <div className="flex items-center justify-between">
          <div className="flex flex-wrap gap-1">
            {update.project_names.map((name, i) => (
              <span
                key={i}
                className="px-2 py-0.5 rounded-full text-xs bg-forest-100 dark:bg-forest-700 text-forest-600 dark:text-forest-300"
              >
                {name}
              </span>
            ))}
          </div>
          <span className="text-xs text-forest-400 flex items-center gap-1 shrink-0 ml-2">
            <Clock className="h-3 w-3" />
            {new Date(update.created_at).toLocaleDateString()}
          </span>
        </div>
      </div>
    </Link>
  );
}

export default function UpdatesPage() {
  const [viewMode, setViewMode] = useState<ViewMode>("timeline");
  const { data: updates, isLoading } = useProjectUpdates();

  const groupedByProject = useMemo(() => {
    if (!updates) return {};
    const groups: Record<string, ProjectUpdateBase[]> = {};
    for (const u of updates) {
      for (const name of u.project_names) {
        if (!groups[name]) groups[name] = [];
        groups[name].push(u);
      }
      if (u.project_names.length === 0) {
        if (!groups["Unlinked"]) groups["Unlinked"] = [];
        groups["Unlinked"].push(u);
      }
    }
    return groups;
  }, [updates]);

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-forest-950 dark:text-forest-50 flex items-center gap-2">
          <MessageSquarePlus className="h-6 w-6" />
          Project Updates
        </h1>
        <div className="flex items-center gap-1 bg-forest-100 dark:bg-forest-800 rounded-lg p-1">
          <button
            onClick={() => setViewMode("timeline")}
            className={`px-3 py-1.5 text-sm font-medium rounded-md transition-colors ${
              viewMode === "timeline"
                ? "bg-white dark:bg-forest-700 text-forest-900 dark:text-forest-100 shadow-sm"
                : "text-forest-500 dark:text-forest-400 hover:text-forest-700 dark:hover:text-forest-200"
            }`}
          >
            <Clock className="h-4 w-4 inline mr-1" />
            Timeline
          </button>
          <button
            onClick={() => setViewMode("by-project")}
            className={`px-3 py-1.5 text-sm font-medium rounded-md transition-colors ${
              viewMode === "by-project"
                ? "bg-white dark:bg-forest-700 text-forest-900 dark:text-forest-100 shadow-sm"
                : "text-forest-500 dark:text-forest-400 hover:text-forest-700 dark:hover:text-forest-200"
            }`}
          >
            <FolderKanban className="h-4 w-4 inline mr-1" />
            By Project
          </button>
        </div>
      </div>

      {/* Content */}
      {isLoading ? (
        <div className="grid gap-4 md:grid-cols-2">
          {[1, 2, 3, 4].map((i) => (
            <div
              key={i}
              className="h-40 bg-forest-100 dark:bg-forest-800 rounded-xl animate-pulse"
            />
          ))}
        </div>
      ) : !updates?.length ? (
        <div className="text-center py-16 text-forest-400">
          <MessageSquarePlus className="h-12 w-12 mx-auto mb-3 opacity-50" />
          <p className="text-lg font-medium">No updates yet</p>
          <p className="text-sm mt-1">
            Use the + button to add your first project update
          </p>
        </div>
      ) : viewMode === "timeline" ? (
        <div className="grid gap-4 md:grid-cols-2">
          {updates.map((u) => (
            <UpdateCard key={u.id} update={u} />
          ))}
        </div>
      ) : (
        <div className="space-y-8">
          {Object.entries(groupedByProject)
            .sort(([a], [b]) => a.localeCompare(b))
            .map(([projectName, projectUpdates]) => (
              <div key={projectName}>
                <h2 className="text-lg font-semibold text-forest-900 dark:text-forest-100 mb-3 flex items-center gap-2">
                  <FolderKanban className="h-5 w-5 text-forest-500" />
                  {projectName}
                  <span className="text-sm font-normal text-forest-400">
                    ({projectUpdates.length})
                  </span>
                </h2>
                <div className="grid gap-4 md:grid-cols-2">
                  {projectUpdates.map((u) => (
                    <UpdateCard key={u.id} update={u} />
                  ))}
                </div>
              </div>
            ))}
        </div>
      )}
    </div>
  );
}
