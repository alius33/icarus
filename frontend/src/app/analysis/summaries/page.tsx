import Link from "next/link";
import { api } from "@/lib/api";
import { formatDate } from "@/lib/utils";

export default async function SummariesListPage() {
  let summaries;
  let error: string | null = null;

  try {
    summaries = await api.getSummaries();
  } catch (e) {
    error = e instanceof Error ? e.message : "Failed to load summaries";
  }

  if (error) {
    return (
      <div className="space-y-6">
        <h2 className="text-2xl font-bold text-gray-900">Summaries</h2>
        <div className="rounded-lg border border-red-200 bg-red-50 p-6">
          <p className="text-sm text-red-700">{error}</p>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <h2 className="text-2xl font-bold text-gray-900">Summaries</h2>

      {!summaries || summaries.length === 0 ? (
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-8 text-center">
          <p className="text-gray-500 text-sm">
            No summaries have been generated yet. Process transcripts with
            Claude to generate summaries.
          </p>
        </div>
      ) : (
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden">
          <ul className="divide-y divide-gray-200">
            {summaries.map((s) => (
              <li key={s.id}>
                <Link
                  href={`/analysis/summaries/${s.id}`}
                  className="flex items-center justify-between px-6 py-4 hover:bg-gray-50 transition-colors"
                >
                  <div className="min-w-0">
                    <p className="text-sm font-medium text-blue-600 hover:text-blue-800 truncate">
                      {s.transcript_title || `Summary #${s.id}`}
                    </p>
                    {s.tldr && (
                      <p className="mt-1 text-xs text-gray-500 truncate">
                        {s.tldr}
                      </p>
                    )}
                  </div>
                  <span className="text-xs text-gray-400 ml-4 flex-shrink-0">
                    {s.date ? formatDate(s.date) : "—"}
                  </span>
                </Link>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}
