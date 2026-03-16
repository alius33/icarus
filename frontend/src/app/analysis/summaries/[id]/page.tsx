import Link from "next/link";
import { api } from "@/lib/api";
import { formatDate } from "@/lib/utils";
import MarkdownContent from "@/components/MarkdownContent";

interface SummaryDetailPageProps {
  params: Promise<{ id: string }>;
}

export default async function SummaryDetailPage({
  params,
}: SummaryDetailPageProps) {
  const { id } = await params;
  const summaryId = Number(id);

  let summary;
  let error: string | null = null;

  try {
    summary = await api.getSummary(summaryId);
  } catch (e) {
    error = e instanceof Error ? e.message : "Failed to load summary";
  }

  if (error || !summary) {
    return (
      <div className="space-y-6">
        <Link
          href="/analysis/summaries"
          className="text-base text-forest-500 hover:text-blue-800"
        >
          &larr; Back to Summaries
        </Link>
        <div className="rounded-lg border border-red-200 bg-red-50 p-6">
          <p className="text-base text-red-700">
            {error || "Unable to load summary. Please try again later."}
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <Link
        href="/analysis/summaries"
        className="inline-block text-base text-forest-500 hover:text-blue-800"
      >
        &larr; Back to Summaries
      </Link>

      {/* Header */}
      <div className="bg-white dark:bg-forest-800 rounded-lg shadow-sm border border-forest-200 p-6">
        <h2 className="text-2xl font-bold text-forest-950">
          {summary.transcript_title || `Summary #${summary.id}`}
        </h2>
        <div className="mt-2 flex items-center gap-3">
          {summary.date && (
            <span className="text-base text-forest-400">
              {formatDate(summary.date)}
            </span>
          )}
          {summary.transcript_id && (
            <Link
              href={`/transcripts/${summary.transcript_id}`}
              className="text-base text-forest-500 hover:text-blue-800"
            >
              View Source Transcript
            </Link>
          )}
        </div>
        {summary.tldr && (
          <p className="mt-3 text-base text-forest-500 italic">
            TL;DR: {summary.tldr}
          </p>
        )}
      </div>

      {/* Full Summary */}
      <div className="bg-white dark:bg-forest-800 rounded-lg shadow-sm border border-forest-200 p-6">
        <MarkdownContent>{summary.full_summary}</MarkdownContent>
      </div>

      {/* Structured Sections */}
      <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
        {summary.key_decisions.length > 0 && (
          <div className="bg-white dark:bg-forest-800 rounded-lg shadow-sm border border-forest-200 p-6">
            <h3 className="text-lg font-semibold text-forest-950 mb-3">
              Key Decisions
            </h3>
            <ul className="space-y-2">
              {summary.key_decisions.map((d, i) => (
                <li key={i} className="flex items-start gap-2 text-base text-forest-600">
                  <span className="mt-0.5 h-1.5 w-1.5 rounded-full bg-forest-500 flex-shrink-0" />
                  {d}
                </li>
              ))}
            </ul>
          </div>
        )}

        {summary.action_items.length > 0 && (
          <div className="bg-white dark:bg-forest-800 rounded-lg shadow-sm border border-forest-200 p-6">
            <h3 className="text-lg font-semibold text-forest-950 mb-3">
              Action Items
            </h3>
            <ul className="space-y-2">
              {summary.action_items.map((a, i) => (
                <li key={i} className="flex items-start gap-2 text-base text-forest-600">
                  <span className="mt-0.5 h-1.5 w-1.5 rounded-full bg-green-500 flex-shrink-0" />
                  {a}
                </li>
              ))}
            </ul>
          </div>
        )}

        {summary.risks_and_concerns.length > 0 && (
          <div className="bg-white dark:bg-forest-800 rounded-lg shadow-sm border border-forest-200 p-6">
            <h3 className="text-lg font-semibold text-forest-950 mb-3">
              Risks & Concerns
            </h3>
            <ul className="space-y-2">
              {summary.risks_and_concerns.map((r, i) => (
                <li key={i} className="flex items-start gap-2 text-base text-forest-600">
                  <span className="mt-0.5 h-1.5 w-1.5 rounded-full bg-red-500 flex-shrink-0" />
                  {r}
                </li>
              ))}
            </ul>
          </div>
        )}

        {summary.follow_ups.length > 0 && (
          <div className="bg-white dark:bg-forest-800 rounded-lg shadow-sm border border-forest-200 p-6">
            <h3 className="text-lg font-semibold text-forest-950 mb-3">
              Follow-ups
            </h3>
            <ul className="space-y-2">
              {summary.follow_ups.map((f, i) => (
                <li key={i} className="flex items-start gap-2 text-base text-forest-600">
                  <span className="mt-0.5 h-1.5 w-1.5 rounded-full bg-yellow-500 flex-shrink-0" />
                  {f}
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>
    </div>
  );
}
