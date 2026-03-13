import Link from "next/link";
import { api } from "@/lib/api";
import { formatDate } from "@/lib/utils";
import TranscriptNotesSection from "@/components/transcripts/TranscriptNotesSection";
import TranscriptAttachmentsSection from "@/components/transcripts/TranscriptAttachmentsSection";

interface TranscriptDetailPageProps {
  params: Promise<{ id: string }>;
}

function formatTranscriptContent(rawText: string): React.ReactNode[] {
  const lines = rawText.split("\n");
  const speakerPattern = /^([A-Za-z\s.'-]+)\s{2,}\d+:\d{2}/;

  return lines.map((line, i) => {
    const match = line.match(speakerPattern);
    if (match) {
      const speakerEnd = line.indexOf(match[0]) + match[0].length;
      const timestampMatch = line.match(/(\d+:\d{2})/);
      const timestampEnd = timestampMatch
        ? line.indexOf(timestampMatch[0]) + timestampMatch[0].length
        : speakerEnd;

      return (
        <div key={i} className="mb-1">
          <span className="font-semibold text-blue-700">
            {match[1].trim()}
          </span>
          <span className="text-xs text-gray-400 ml-2">
            {timestampMatch ? timestampMatch[0] : ""}
          </span>
          <br />
          <span className="text-gray-800">
            {line.substring(timestampEnd).trim()}
          </span>
        </div>
      );
    }

    if (line.trim() === "") {
      return <div key={i} className="h-3" />;
    }

    return (
      <div key={i} className="text-gray-800 mb-1">
        {line}
      </div>
    );
  });
}

export default async function TranscriptDetailPage({
  params,
}: TranscriptDetailPageProps) {
  const { id } = await params;
  const transcriptId = Number(id);

  let transcript;
  let error: string | null = null;

  try {
    transcript = await api.getTranscript(transcriptId);
  } catch (e) {
    error = e instanceof Error ? e.message : "Failed to load transcript";
  }

  if (error || !transcript) {
    return (
      <div className="space-y-6">
        <Link
          href="/transcripts"
          className="text-sm text-blue-600 hover:text-blue-800"
        >
          &larr; Back to Transcripts
        </Link>
        <div className="rounded-lg border border-red-200 bg-red-50 p-6">
          <p className="text-sm text-red-700">
            {error || "Unable to load transcript. Please try again later."}
          </p>
        </div>
      </div>
    );
  }

  let hasSummary = false;
  try {
    await api.getTranscriptSummary(transcriptId);
    hasSummary = true;
  } catch {
    // No summary available
  }

  return (
    <div className="space-y-6">
      <Link
        href="/transcripts"
        className="inline-block text-sm text-blue-600 hover:text-blue-800"
      >
        &larr; Back to Transcripts
      </Link>

      {/* Header */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
        <h2 className="text-2xl font-bold text-gray-900">
          {transcript.title || transcript.file_name}
        </h2>

        <div className="mt-3 flex flex-wrap items-center gap-3">
          {transcript.date && (
            <span className="text-sm text-gray-500">
              {formatDate(transcript.date)}
            </span>
          )}

          <span className="px-2 py-1 rounded-full text-xs font-medium bg-gray-100 text-gray-600 border border-gray-200">
            {transcript.word_count.toLocaleString()} words
          </span>

          {hasSummary && (
            <Link
              href={`/analysis/summaries/${transcriptId}`}
              className="px-2 py-1 rounded-full text-xs font-medium bg-blue-100 text-blue-700 border border-blue-200 hover:bg-blue-200 transition-colors"
            >
              View Summary
            </Link>
          )}
        </div>

        {/* Participants */}
        {transcript.participants.length > 0 && (
          <div className="mt-4">
            <p className="text-xs font-medium uppercase tracking-wider text-gray-500 mb-2">
              Participants
            </p>
            <div className="flex flex-wrap gap-2">
              {transcript.participants.map((name) => (
                <span
                  key={name}
                  className="px-2 py-1 rounded-full text-xs font-medium bg-blue-50 text-blue-700 border border-blue-200"
                >
                  {name}
                </span>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* Notes */}
      <TranscriptNotesSection transcriptId={transcriptId} />

      {/* Attachments */}
      <TranscriptAttachmentsSection transcriptId={transcriptId} />

      {/* Transcript Content */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">
          Transcript
        </h3>
        <div className="font-mono text-sm leading-relaxed max-w-none">
          {formatTranscriptContent(transcript.raw_text)}
        </div>
      </div>
    </div>
  );
}
