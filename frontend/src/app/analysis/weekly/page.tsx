import Link from "next/link";
import { api } from "@/lib/api";
import { formatDate } from "@/lib/utils";

export default async function WeeklyReportsListPage() {
  let reports;
  let error: string | null = null;

  try {
    reports = await api.getWeeklyReports();
  } catch (e) {
    error = e instanceof Error ? e.message : "Failed to load weekly reports";
  }

  if (error) {
    return (
      <div className="space-y-6">
        <h2 className="text-2xl font-bold text-forest-950">Weekly Reports</h2>
        <div className="rounded-lg border border-red-200 bg-red-50 p-6">
          <p className="text-base text-red-700">{error}</p>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <h2 className="text-2xl font-bold text-forest-950">Weekly Reports</h2>

      {!reports || reports.length === 0 ? (
        <div className="bg-white dark:bg-forest-800 rounded-lg shadow-sm border border-forest-200 p-8 text-center">
          <p className="text-forest-400 text-base">
            No weekly reports have been generated yet. Weekly reports are
            compiled from transcript summaries and programme activity.
          </p>
        </div>
      ) : (
        <div className="bg-white dark:bg-forest-800 rounded-lg shadow-sm border border-forest-200 overflow-hidden">
          <ul className="divide-y divide-forest-200">
            {reports.map((r) => (
              <li key={r.id}>
                <Link
                  href={`/analysis/weekly/${r.id}`}
                  className="flex items-center justify-between px-6 py-4 hover:bg-forest-50 transition-colors"
                >
                  <div className="min-w-0">
                    <p className="text-base font-medium text-forest-500 hover:text-blue-800 truncate">
                      {r.title}
                    </p>
                    {r.period_label && (
                      <p className="mt-1 text-sm text-forest-400">
                        {r.period_label}
                      </p>
                    )}
                  </div>
                  <span className="text-sm text-forest-300 ml-4 flex-shrink-0">
                    {formatDate(r.week_start)} &mdash;{" "}
                    {formatDate(r.week_end)}
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
