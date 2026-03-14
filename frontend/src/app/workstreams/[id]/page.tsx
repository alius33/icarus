import Link from "next/link";
import { ArrowLeft } from "lucide-react";
import MarkdownContent from "@/components/MarkdownContent";
import { api } from "@/lib/api";
import { getStatusColor, formatDate } from "@/lib/utils";

interface WorkstreamDetailPageProps {
  params: { id: string };
}

export default async function WorkstreamDetailPage({
  params,
}: WorkstreamDetailPageProps) {
  const ws = await api.getWorkstream(Number(params.id));

  const sortedMilestones = [...ws.milestones].sort((a, b) => {
    if (!a.target_date) return 1;
    if (!b.target_date) return -1;
    return new Date(b.target_date).getTime() - new Date(a.target_date).getTime();
  });

  return (
    <div className="space-y-6">
      {/* Back link */}
      <Link
        href="/workstreams"
        className="inline-flex items-center gap-1 text-base text-gray-500 hover:text-gray-700"
      >
        <ArrowLeft className="h-4 w-4" />
        Back to Workstreams
      </Link>

      {/* Header */}
      <div>
        <h2 className="text-2xl font-bold text-gray-900">
          {ws.code}: {ws.name}
        </h2>
        <div className="mt-3 flex flex-wrap items-center gap-3">
          <span
            className={`inline-flex items-center rounded-full border px-2.5 py-0.5 text-sm font-medium ${getStatusColor(ws.status)}`}
          >
            {ws.status}
          </span>
          {ws.owner && (
            <span className="inline-flex items-center rounded-full bg-gray-100 px-2.5 py-0.5 text-sm font-medium text-gray-700">
              Lead: {ws.owner}
            </span>
          )}
          {ws.progress_pct !== null && (
            <span className="text-base text-gray-500">
              {ws.progress_pct}% complete
            </span>
          )}
        </div>
      </div>

      {/* Description */}
      {ws.description && (
        <section className="rounded-lg border border-gray-200 bg-white p-6 shadow-sm">
          <h3 className="text-lg font-semibold text-gray-900 mb-3">
            Description
          </h3>
          <MarkdownContent>{ws.description}</MarkdownContent>
        </section>
      )}

      {/* Milestones */}
      {sortedMilestones.length > 0 && (
        <section className="rounded-lg border border-gray-200 bg-white p-6 shadow-sm">
          <h3 className="text-lg font-semibold text-gray-900 mb-3">
            Milestones
          </h3>
          <div className="relative ml-3">
            {/* Vertical line */}
            <div className="absolute left-0 top-2 bottom-2 border-l-2 border-gray-300" />

            <div className="space-y-6">
              {sortedMilestones.map((milestone) => (
                <div key={milestone.id} className="relative flex gap-4 pl-6">
                  {/* Dot */}
                  <div
                    className={`absolute left-[-5px] top-1.5 h-3 w-3 rounded-full border-2 border-white ${
                      milestone.status === "COMPLETED" || milestone.status === "LIKELY_COMPLETED"
                        ? "bg-green-500"
                        : milestone.status === "STALLED"
                          ? "bg-red-500"
                          : "bg-blue-500"
                    }`}
                  />

                  {/* Date */}
                  <div className="w-28 flex-shrink-0 text-base text-gray-500">
                    {milestone.target_date
                      ? formatDate(milestone.target_date)
                      : "No date"}
                  </div>

                  {/* Content */}
                  <div className="flex-1">
                    <p className="text-base font-medium text-gray-900">
                      {milestone.title}
                    </p>
                    <div className="mt-1 flex items-center gap-2">
                      <span
                        className={`inline-flex items-center rounded-full border px-2 py-0.5 text-sm font-medium ${getStatusColor(milestone.status)}`}
                      >
                        {milestone.status}
                      </span>
                    </div>
                    {milestone.notes && (
                      <p className="mt-1 text-base text-gray-500">
                        {milestone.notes}
                      </p>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </section>
      )}

      {/* Recent Mentions */}
      {ws.recent_mentions.length > 0 && (
        <section className="rounded-lg border border-gray-200 bg-white p-6 shadow-sm">
          <h3 className="text-lg font-semibold text-gray-900 mb-3">
            Recent Mentions
          </h3>
          <ul className="space-y-2">
            {ws.recent_mentions.map((mention, i) => (
              <li
                key={i}
                className="text-base text-gray-700 rounded-md bg-gray-50 px-3 py-2"
              >
                {mention}
              </li>
            ))}
          </ul>
        </section>
      )}
    </div>
  );
}
