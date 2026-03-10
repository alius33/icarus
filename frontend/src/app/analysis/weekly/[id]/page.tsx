import Link from "next/link";
import { api } from "@/lib/api";
import { formatDate } from "@/lib/utils";
import MarkdownContent from "@/components/MarkdownContent";

interface WeeklyReportDetailPageProps {
  params: Promise<{ id: string }>;
}

export default async function WeeklyReportDetailPage({
  params,
}: WeeklyReportDetailPageProps) {
  const { id } = await params;
  const reportId = Number(id);

  let report;
  let error: string | null = null;

  try {
    report = await api.getWeeklyReport(reportId);
  } catch (e) {
    error = e instanceof Error ? e.message : "Failed to load weekly report";
  }

  if (error || !report) {
    return (
      <div className="space-y-6">
        <Link
          href="/analysis/weekly"
          className="text-sm text-blue-600 hover:text-blue-800"
        >
          &larr; Back to Weekly Reports
        </Link>
        <div className="rounded-lg border border-red-200 bg-red-50 p-6">
          <p className="text-sm text-red-700">
            {error || "Unable to load weekly report. Please try again later."}
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <Link
        href="/analysis/weekly"
        className="inline-block text-sm text-blue-600 hover:text-blue-800"
      >
        &larr; Back to Weekly Reports
      </Link>

      {/* Header */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
        <h2 className="text-2xl font-bold text-gray-900">{report.title}</h2>
        <div className="mt-2 flex items-center gap-3">
          <span className="text-sm text-gray-500">
            {formatDate(report.week_start)} &mdash;{" "}
            {formatDate(report.week_end)}
          </span>
          {report.period_label && (
            <span className="px-2 py-1 rounded-full text-xs font-medium bg-gray-100 text-gray-600 border border-gray-200">
              {report.period_label}
            </span>
          )}
        </div>
      </div>

      {/* Report Content */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
        <MarkdownContent>{report.content}</MarkdownContent>
      </div>

      {/* Structured Sections */}
      <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
        {report.highlights.length > 0 && (
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-3">
              Highlights
            </h3>
            <ul className="space-y-2">
              {report.highlights.map((h, i) => (
                <li
                  key={i}
                  className="flex items-start gap-2 text-sm text-gray-700"
                >
                  <span className="mt-0.5 h-1.5 w-1.5 rounded-full bg-green-500 flex-shrink-0" />
                  {h}
                </li>
              ))}
            </ul>
          </div>
        )}

        {report.workstream_updates.length > 0 && (
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-3">
              Workstream Updates
            </h3>
            <ul className="space-y-2">
              {report.workstream_updates.map((w, i) => (
                <li
                  key={i}
                  className="flex items-start gap-2 text-sm text-gray-700"
                >
                  <span className="mt-0.5 h-1.5 w-1.5 rounded-full bg-blue-500 flex-shrink-0" />
                  {w}
                </li>
              ))}
            </ul>
          </div>
        )}

        {report.risks.length > 0 && (
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-3">
              Risks
            </h3>
            <ul className="space-y-2">
              {report.risks.map((r, i) => (
                <li
                  key={i}
                  className="flex items-start gap-2 text-sm text-gray-700"
                >
                  <span className="mt-0.5 h-1.5 w-1.5 rounded-full bg-red-500 flex-shrink-0" />
                  {r}
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>
    </div>
  );
}
