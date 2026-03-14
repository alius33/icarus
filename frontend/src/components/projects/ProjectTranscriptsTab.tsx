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
      <div className="rounded-lg border border-gray-200 bg-white p-8 text-center">
        <p className="text-base text-gray-500">
          No transcripts linked to this project yet.
        </p>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden">
      <table className="w-full">
        <thead>
          <tr className="border-b border-gray-200 bg-gray-50">
            <th className="px-6 py-3 text-left text-sm font-medium uppercase tracking-wider text-gray-500">
              Title
            </th>
            <th className="px-6 py-3 text-left text-sm font-medium uppercase tracking-wider text-gray-500 w-28">
              Date
            </th>
            <th className="px-6 py-3 text-left text-sm font-medium uppercase tracking-wider text-gray-500 w-28">
              Participants
            </th>
            <th className="px-6 py-3 text-left text-sm font-medium uppercase tracking-wider text-gray-500 w-24">
              Words
            </th>
            <th className="px-6 py-3 text-left text-sm font-medium uppercase tracking-wider text-gray-500 w-24">
              Summary
            </th>
          </tr>
        </thead>
        <tbody className="divide-y divide-gray-200">
          {transcripts.map((t) => (
            <tr key={t.id} className="hover:bg-gray-50 transition-colors">
              <td className="px-6 py-4">
                <Link
                  href={`/transcripts/${t.id}`}
                  className="text-base font-medium text-blue-600 hover:text-blue-800"
                >
                  {t.title || t.file_name}
                </Link>
              </td>
              <td className="px-6 py-4 text-base text-gray-500 whitespace-nowrap">
                {t.date ? formatDate(t.date) : "\u2014"}
              </td>
              <td className="px-6 py-4 text-base text-gray-500">
                {t.participant_count}
              </td>
              <td className="px-6 py-4 text-base text-gray-500">
                {t.word_count.toLocaleString()}
              </td>
              <td className="px-6 py-4">
                {t.has_summary ? (
                  <span className="inline-flex items-center rounded-full bg-green-100 px-2 py-0.5 text-sm font-medium text-green-800">
                    Yes
                  </span>
                ) : (
                  <span className="text-sm text-gray-400">No</span>
                )}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
