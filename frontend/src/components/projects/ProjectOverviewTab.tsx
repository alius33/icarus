import Link from "next/link";
import type { ProjectHub } from "@/lib/types";
import { getStatusColor } from "@/lib/utils";
import MarkdownContent from "@/components/MarkdownContent";
import {
  FileText,
  FileBarChart,
  Gavel,
  CheckSquare,
  AlertCircle,
  Users,
} from "lucide-react";

const STAT_CARDS = [
  { key: "transcript_count" as const, label: "Transcripts", tab: "transcripts", icon: FileText, color: "text-blue-600 bg-blue-50" },
  { key: "summary_count" as const, label: "Summaries", tab: "summaries", icon: FileBarChart, color: "text-purple-600 bg-purple-50" },
  { key: "decision_count" as const, label: "Decisions", tab: "decisions", icon: Gavel, color: "text-amber-600 bg-amber-50" },
  { key: "action_count" as const, label: "Actions", tab: "actions", icon: CheckSquare, color: "text-green-600 bg-green-50" },
  { key: "open_thread_count" as const, label: "Open Threads", tab: "threads", icon: AlertCircle, color: "text-red-600 bg-red-50" },
  { key: "stakeholder_count" as const, label: "Stakeholders", tab: "stakeholders", icon: Users, color: "text-teal-600 bg-teal-50" },
];

export default function ProjectOverviewTab({ hub }: { hub: ProjectHub }) {
  const { project } = hub;

  return (
    <div className="space-y-6">
      {/* Stat cards */}
      <div className="grid grid-cols-2 gap-4 sm:grid-cols-3 lg:grid-cols-6">
        {STAT_CARDS.map((card) => {
          const Icon = card.icon;
          const count = project[card.key];
          return (
            <Link
              key={card.key}
              href={`/projects/${project.id}?tab=${card.tab}`}
              className="rounded-lg border border-gray-200 bg-white p-4 transition-shadow hover:shadow-md hover:border-gray-300"
            >
              <div className={`inline-flex rounded-md p-2 ${card.color}`}>
                <Icon className="h-4 w-4" />
              </div>
              <p className="mt-2 text-2xl font-bold text-gray-900">{count}</p>
              <p className="text-xs text-gray-500">{card.label}</p>
            </Link>
          );
        })}
      </div>

      {/* Description */}
      {project.description && (
        <div className="rounded-lg border border-gray-200 bg-white p-6">
          <h3 className="mb-3 text-sm font-semibold text-gray-900">
            Description
          </h3>
          <MarkdownContent>{project.description}</MarkdownContent>
        </div>
      )}

      {/* Recent activity */}
      <div className="rounded-lg border border-gray-200 bg-white p-6">
        <h3 className="mb-3 text-sm font-semibold text-gray-900">
          Recent Activity
        </h3>
        {hub.transcripts.length === 0 &&
        hub.decisions.length === 0 &&
        hub.action_items.length === 0 ? (
          <p className="text-sm text-gray-500">
            No linked items yet. Use the other tabs to explore, or link
            entities to this project.
          </p>
        ) : (
          <ul className="space-y-2">
            {hub.transcripts.slice(0, 3).map((t) => (
              <li key={`t-${t.id}`} className="flex items-center gap-3 text-sm">
                <FileText className="h-4 w-4 text-blue-500 flex-shrink-0" />
                <Link
                  href={`/transcripts/${t.id}`}
                  className="text-blue-600 hover:underline truncate"
                >
                  {t.title || t.file_name}
                </Link>
                {t.date && (
                  <span className="text-xs text-gray-400 flex-shrink-0">
                    {t.date}
                  </span>
                )}
              </li>
            ))}
            {hub.decisions.slice(0, 3).map((d) => (
              <li key={`d-${d.id}`} className="flex items-center gap-3 text-sm">
                <Gavel className="h-4 w-4 text-amber-500 flex-shrink-0" />
                <span className="text-gray-900 truncate">{d.title}</span>
                {d.date && (
                  <span className="text-xs text-gray-400 flex-shrink-0">
                    {d.date}
                  </span>
                )}
              </li>
            ))}
            {hub.action_items.slice(0, 3).map((a) => (
              <li key={`a-${a.id}`} className="flex items-center gap-3 text-sm">
                <CheckSquare className="h-4 w-4 text-green-500 flex-shrink-0" />
                <span className="text-gray-900 truncate">{a.title}</span>
                <span
                  className={`ml-auto inline-flex rounded-full border px-2 py-0.5 text-xs font-medium ${getStatusColor(a.status)}`}
                >
                  {a.status}
                </span>
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
}
