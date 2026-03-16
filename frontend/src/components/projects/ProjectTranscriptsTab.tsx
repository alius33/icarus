import Link from "next/link";
import type { TranscriptBase } from "@/lib/types";
import { formatDate } from "@/lib/utils";

export default function ProjectTranscriptsTab({
  transcripts,
}: {
  transcripts: TranscriptBase[];
}) {
  if (transcripts.length === 0) {
    return (
      <div className="rounded-lg border border-forest-200 bg-white dark:bg-forest-800 p-8 text-center">
        <p className="text-base text-forest-400">
          No transcripts linked to this project yet.
        </p>
      </div>
    );
  }

  return (
    <div className="bg-white dark:bg-forest-800 rounded-lg shadow-sm border border-forest-200 overflow-hidden">
      <table className="w-full">
        <thead>
          <tr className="border-b border-forest-200 bg-forest-50">
            <th className="px-6 py-3 text-left text-sm font-medium uppercase tracking-wider text-forest-400">
              Title
            </th>
            <th className="px-6 py-3 text-left text-sm font-medium uppercase tracking-wider text-forest-400 w-28">
              Date
            </th>
            <th className="px-6 py-3 text-left text-sm font-medium uppercase tracking-wider text-forest-400 w-28">
              Participants
            </th>
            <th className="px-6 py-3 text-left text-sm font-medium uppercase tracking-wider text-forest-400 w-24">
              Words
            </th>
            <th className="px-6 py-3 text-left text-sm font-medium uppercase tracking-wider text-forest-400 w-24">
              Summary
            </th>
          </tr>
        </thead>
        <tbody className="divide-y divide-forest-200">
          {transcripts.map((t) => (
            <tr key={t.id} className="hover:bg-forest-50 transition-colors">
              <td className="px-6 py-4">
                <Link
                  href={`/transcripts/${t.id}`}
                  className="text-base font-medium text-forest-500 hover:text-blue-800"
                >
                  {t.title || t.file_name}
                </Link>
              </td>
              <td className="px-6 py-4 text-base text-forest-400 whitespace-nowrap">
                {t.date ? formatDate(t.date) : "\u2014"}
              </td>
              <td className="px-6 py-4 text-base text-forest-400">
                {t.participant_count}
              </td>
              <td className="px-6 py-4 text-base text-forest-400">
                {t.word_count.toLocaleString()}
              </td>
              <td className="px-6 py-4">
                {t.has_summary ? (
                  <span className="inline-flex items-center rounded-full bg-green-100 px-2 py-0.5 text-sm font-medium text-green-800">
                    Yes
                  </span>
                ) : (
                  <span className="text-sm text-forest-300">No</span>
                )}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
