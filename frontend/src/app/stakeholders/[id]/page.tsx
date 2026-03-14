import Link from "next/link";
import { ArrowLeft } from "lucide-react";
import MarkdownContent from "@/components/MarkdownContent";
import { api } from "@/lib/api";
import { tierLabels, formatDate } from "@/lib/utils";

interface StakeholderDetailPageProps {
  params: { id: string };
}

export default async function StakeholderDetailPage({
  params,
}: StakeholderDetailPageProps) {
  const [stakeholder, mentions] = await Promise.all([
    api.getStakeholder(Number(params.id)),
    api.getStakeholderMentions(Number(params.id)),
  ]);

  return (
    <div className="space-y-6">
      {/* Back link */}
      <Link
        href="/stakeholders"
        className="inline-flex items-center gap-1 text-base text-gray-500 hover:text-gray-700"
      >
        <ArrowLeft className="h-4 w-4" />
        Back to Stakeholders
      </Link>

      {/* Header */}
      <div>
        <h2 className="text-2xl font-bold text-gray-900">
          {stakeholder.name}
        </h2>
        <div className="mt-3 flex flex-wrap items-center gap-3">
          <span className="inline-flex items-center rounded-full bg-blue-50 px-2.5 py-0.5 text-sm font-medium text-blue-700 border border-blue-200">
            Tier {stakeholder.tier} &mdash;{" "}
            {tierLabels[stakeholder.tier] || "Other"}
          </span>
          {stakeholder.role && (
            <span className="text-base text-gray-600">{stakeholder.role}</span>
          )}
          {stakeholder.organisation && (
            <span className="inline-flex items-center rounded-full bg-gray-100 px-2.5 py-0.5 text-sm font-medium text-gray-700">
              {stakeholder.organisation}
            </span>
          )}
        </div>
      </div>

      {/* Aliases */}
      {stakeholder.aliases.length > 0 && (
        <div className="text-base text-gray-500">
          Also known as:{" "}
          {stakeholder.aliases.map((alias, i) => (
            <span key={i}>
              {i > 0 && ", "}
              <span className="font-medium text-gray-600">{alias}</span>
            </span>
          ))}
        </div>
      )}

      {/* Notes */}
      {stakeholder.notes && (
        <section className="rounded-lg border border-gray-200 bg-white p-6 shadow-sm">
          <h3 className="text-lg font-semibold text-gray-900 mb-3">Notes</h3>
          <MarkdownContent>{stakeholder.notes}</MarkdownContent>
        </section>
      )}

      {/* Transcript Appearances */}
      <section className="rounded-lg border border-gray-200 bg-white p-6 shadow-sm">
        <h3 className="text-lg font-semibold text-gray-900 mb-3">
          Transcript Appearances
        </h3>

        {mentions.length > 0 ? (
          <div className="space-y-3">
            {mentions.map((mention, i) => (
              <Link
                key={i}
                href={`/transcripts/${mention.transcript_id}`}
                className="block rounded-md border border-gray-100 bg-gray-50 p-4 transition-colors hover:bg-gray-100"
              >
                <div className="flex items-center justify-between">
                  <p className="text-base font-medium text-gray-900">
                    {mention.transcript_title || `Transcript #${mention.transcript_id}`}
                  </p>
                  {mention.date && (
                    <span className="text-sm text-gray-500">
                      {formatDate(mention.date)}
                    </span>
                  )}
                </div>
                {mention.snippet && (
                  <p className="mt-1 text-base text-gray-600 line-clamp-2">
                    &ldquo;{mention.snippet}&rdquo;
                  </p>
                )}
              </Link>
            ))}
          </div>
        ) : (
          <p className="text-base text-gray-500">
            No transcript appearances recorded.
          </p>
        )}
      </section>
    </div>
  );
}
