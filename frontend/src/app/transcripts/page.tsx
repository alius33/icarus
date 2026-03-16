import Link from "next/link";
import { Pencil, Paperclip } from "lucide-react";
import { api } from "@/lib/api";
import { formatDate } from "@/lib/utils";

interface TranscriptListPageProps {
  searchParams: Promise<{ page?: string }>;
}

export default async function TranscriptListPage({
  searchParams,
}: TranscriptListPageProps) {
  const params = await searchParams;
  const currentPage = Number(params.page) || 1;
  const limit = 20;

  let data;
  let error: string | null = null;

  try {
    data = await api.getTranscripts(currentPage, limit);
  } catch (e) {
    error = e instanceof Error ? e.message : "Failed to load transcripts";
  }

  if (error || !data) {
    return (
      <div className="space-y-6">
        <h2 className="text-xl md:text-2xl font-bold text-forest-950 dark:text-forest-50">Transcripts</h2>
        <div className="rounded-lg border border-red-200 bg-red-50 p-6">
          <p className="text-base text-red-700">
            {error || "Unable to load transcripts. Please try again later."}
          </p>
        </div>
      </div>
    );
  }

  function formatParticipants(participants: string[] | undefined): string {
    if (!participants || participants.length === 0) return "—";
    if (participants.length <= 3) return participants.join(", ");
    return `${participants.slice(0, 3).join(", ")} +${participants.length - 3} more`;
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h2 className="text-xl md:text-2xl font-bold text-forest-950 dark:text-forest-50">Transcripts</h2>
        <span className="text-base text-forest-400">
          {data.total} total transcript{data.total !== 1 ? "s" : ""}
        </span>
      </div>

      {/* Mobile card view */}
      <div className="space-y-2 md:hidden">
        {data.items.length === 0 ? (
          <div className="rounded-lg border-2 border-dashed border-forest-200 p-8 text-center">
            <p className="text-base text-forest-400">No transcripts found.</p>
          </div>
        ) : (
          data.items.map((t) => (
            <Link
              key={t.id}
              href={`/transcripts/${t.id}`}
              className="block rounded-lg border border-forest-200 bg-white dark:bg-forest-800 p-3 active:bg-forest-50"
            >
              <div className="text-sm text-forest-300 mb-1">
                {t.date ? formatDate(t.date) : "—"}
              </div>
              <div className="flex items-center gap-2 mb-1">
                <span className="text-base text-forest-950 line-clamp-2">
                  {t.title || t.file_name}
                </span>
                {t.has_notes && <Pencil className="h-3.5 w-3.5 text-amber-500 shrink-0" />}
                {t.attachments_count > 0 && <Paperclip className="h-3.5 w-3.5 text-forest-300 shrink-0" />}
              </div>
              <div className="text-sm text-forest-400">
                {t.word_count.toLocaleString()} words
              </div>
            </Link>
          ))
        )}
      </div>

      {/* Desktop table */}
      <div className="hidden md:block bg-white dark:bg-forest-800 rounded-lg shadow-sm border border-forest-200 overflow-hidden">
        <table className="w-full">
          <thead>
            <tr className="border-b border-forest-200 bg-forest-50">
              <th className="px-6 py-3 text-left text-sm font-medium uppercase tracking-wider text-forest-400">
                Date
              </th>
              <th className="px-6 py-3 text-left text-sm font-medium uppercase tracking-wider text-forest-400">
                Title
              </th>
              <th className="px-6 py-3 text-left text-sm font-medium uppercase tracking-wider text-forest-400">
                Participants
              </th>
              <th className="px-6 py-3 text-right text-sm font-medium uppercase tracking-wider text-forest-400">
                Words
              </th>
            </tr>
          </thead>
          <tbody className="divide-y divide-forest-200">
            {data.items.length === 0 ? (
              <tr>
                <td
                  colSpan={4}
                  className="px-6 py-8 text-center text-base text-forest-400"
                >
                  No transcripts found.
                </td>
              </tr>
            ) : (
              data.items.map((t) => (
                <tr key={t.id} className="hover:bg-forest-50 transition-colors">
                  <td className="px-6 py-4 text-base text-forest-400 whitespace-nowrap">
                    {t.date ? formatDate(t.date) : "—"}
                  </td>
                  <td className="px-6 py-4">
                    <div className="flex items-center gap-2">
                      <Link
                        href={`/transcripts/${t.id}`}
                        className="text-base text-forest-500 hover:text-blue-800"
                      >
                        {t.title || t.file_name}
                      </Link>
                      {t.has_notes && (
                        <span title="Has notes">
                          <Pencil className="h-3.5 w-3.5 text-amber-500 flex-shrink-0" />
                        </span>
                      )}
                      {t.attachments_count > 0 && (
                        <span className="inline-flex items-center gap-0.5 text-forest-300" title={`${t.attachments_count} attachment${t.attachments_count !== 1 ? "s" : ""}`}>
                          <Paperclip className="h-3.5 w-3.5" />
                          <span className="text-sm">{t.attachments_count}</span>
                        </span>
                      )}
                    </div>
                  </td>
                  <td className="px-6 py-4 text-base text-forest-500">
                    {formatParticipants(undefined)}
                  </td>
                  <td className="px-6 py-4 text-base text-forest-400 text-right tabular-nums">
                    {t.word_count.toLocaleString()}
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>

      {/* Pagination */}
      {data.pages > 1 && (
        <div className="flex items-center justify-between">
          <div>
            {currentPage > 1 ? (
              <Link
                href={`/transcripts?page=${currentPage - 1}`}
                className="rounded-md border border-forest-200 bg-white dark:bg-forest-800 px-4 py-2 text-base font-medium text-forest-600 hover:bg-forest-50"
              >
                Previous
              </Link>
            ) : (
              <span className="rounded-md border border-forest-200 bg-forest-100 px-4 py-2 text-base font-medium text-forest-300 cursor-not-allowed">
                Previous
              </span>
            )}
          </div>
          <span className="text-base text-forest-400">
            Page {currentPage} of {data.pages}
          </span>
          <div>
            {currentPage < data.pages ? (
              <Link
                href={`/transcripts?page=${currentPage + 1}`}
                className="rounded-md border border-forest-200 bg-white dark:bg-forest-800 px-4 py-2 text-base font-medium text-forest-600 hover:bg-forest-50"
              >
                Next
              </Link>
            ) : (
              <span className="rounded-md border border-forest-200 bg-forest-100 px-4 py-2 text-base font-medium text-forest-300 cursor-not-allowed">
                Next
              </span>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
