import Link from "next/link";
import type { SummaryBase } from "@/lib/types";

export default function ProjectSummariesTab({
  summaries,
}: {
  summaries: SummaryBase[];
}) {
  if (summaries.length === 0) {
    return (
      <div className="rounded-lg border border-gray-200 bg-white p-8 text-center">
        <p className="text-sm text-gray-500">
          No summaries linked to this project yet.
        </p>
      </div>
    );
  }

  return (
    <div className="space-y-3">
      {summaries.map((s) => (
        <Link
          key={s.id}
          href={`/analysis/summaries/${s.id}`}
          className="block rounded-lg border border-gray-200 bg-white p-4 transition-shadow hover:shadow-md"
        >
          <h4 className="text-sm font-medium text-gray-900">
            {s.transcript_title || `Summary #${s.id}`}
          </h4>
          {s.tldr && (
            <p className="mt-1 text-xs text-gray-500 line-clamp-2">{s.tldr}</p>
          )}
          <div className="mt-2 text-xs text-gray-400">
            {s.date && <span>{s.date}</span>}
          </div>
        </Link>
      ))}
    </div>
  );
}
