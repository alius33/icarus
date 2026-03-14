"use client";

import { Suspense, useEffect, useState } from "react";
import { useSearchParams } from "next/navigation";
import Link from "next/link";
import { api } from "@/lib/api";
import { sanitizeHtml } from "@/lib/sanitize";
import type { SearchResponse, SearchResult } from "@/lib/types";

const ENTITY_TYPE_COLORS: Record<string, string> = {
  transcript: "bg-blue-100 text-blue-800 border-blue-200",
  decision: "bg-purple-100 text-purple-800 border-purple-200",
  stakeholder: "bg-green-100 text-green-800 border-green-200",
  action_item: "bg-orange-100 text-orange-800 border-orange-200",
  open_thread: "bg-red-100 text-red-800 border-red-200",
  workstream: "bg-teal-100 text-teal-800 border-teal-200",
  glossary: "bg-yellow-100 text-yellow-800 border-yellow-200",
  summary: "bg-indigo-100 text-indigo-800 border-indigo-200",
};

function getEntityColor(type: string): string {
  return (
    ENTITY_TYPE_COLORS[type] || "bg-gray-100 text-gray-800 border-gray-200"
  );
}

function buildResultUrl(result: SearchResult): string {
  if (result.url) return result.url;

  switch (result.type) {
    case "transcript":
      return `/transcripts/${result.id}`;
    case "decision":
      return "/decisions";
    case "stakeholder":
      return `/stakeholders/${result.id}`;
    case "action_item":
      return "/action-items";
    case "open_thread":
      return "/open-threads";
    case "workstream":
      return `/workstreams/${result.id}`;
    case "glossary":
      return "/glossary";
    case "summary":
      return `/summaries/${result.id}`;
    default:
      return "#";
  }
}

function formatEntityType(type: string): string {
  return type
    .split("_")
    .map((w) => w.charAt(0).toUpperCase() + w.slice(1))
    .join(" ");
}

function SearchContent() {
  const searchParams = useSearchParams();
  const query = searchParams.get("q") || "";

  const [data, setData] = useState<SearchResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (!query.trim()) {
      setData(null);
      return;
    }

    setLoading(true);
    setError(null);

    api
      .search(query)
      .then(setData)
      .catch((e) =>
        setError(e instanceof Error ? e.message : "Search failed"),
      )
      .finally(() => setLoading(false));
  }, [query]);

  // Group results by entity_type
  const groupedResults: Record<string, SearchResult[]> = {};
  if (data?.results) {
    for (const result of data.results) {
      if (!groupedResults[result.type]) {
        groupedResults[result.type] = [];
      }
      groupedResults[result.type].push(result);
    }
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center gap-3">
        <h2 className="text-2xl font-bold text-gray-900 dark:text-gray-100">Search</h2>
        {query && (
          <span className="text-lg text-gray-500 dark:text-gray-400">
            &ldquo;{query}&rdquo;
          </span>
        )}
      </div>

      {!query.trim() && (
        <div className="text-center py-12">
          <p className="text-base text-gray-500 dark:text-gray-400">
            Enter a search term in the header to get started.
          </p>
        </div>
      )}

      {loading && (
        <p className="text-base text-gray-500 dark:text-gray-400">Searching...</p>
      )}

      {error && (
        <div className="rounded-lg border border-red-200 dark:border-red-800 bg-red-50 dark:bg-red-900/30 p-6">
          <p className="text-base text-red-700 dark:text-red-400">{error}</p>
        </div>
      )}

      {data && !loading && (
        <>
          <p className="text-base text-gray-500 dark:text-gray-400">
            {data.total} result{data.total !== 1 ? "s" : ""} found
          </p>

          {data.results.length === 0 ? (
            <div className="text-center py-12">
              <p className="text-base text-gray-500 dark:text-gray-400">
                No results found for &ldquo;{query}&rdquo;
              </p>
            </div>
          ) : (
            Object.entries(groupedResults).map(
              ([entityType, results], idx) => (
                <div
                  key={entityType}
                  className={
                    idx > 0
                      ? "border-t border-gray-200 dark:border-gray-700 mt-8 pt-8"
                      : ""
                  }
                >
                  <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-4">
                    {formatEntityType(entityType)}
                    <span className="text-base font-normal text-gray-500 dark:text-gray-400 ml-2">
                      ({results.length})
                    </span>
                  </h3>

                  <div className="space-y-3">
                    {results.map((result) => (
                      <div
                        key={`${result.type}-${result.id}`}
                        className="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-4"
                      >
                        <div className="flex items-start gap-3">
                          <span
                            className={`px-2 py-1 rounded-full text-sm font-medium border flex-shrink-0 ${getEntityColor(result.type)}`}
                          >
                            {formatEntityType(result.type)}
                          </span>
                          <div className="min-w-0 flex-1">
                            <Link
                              href={buildResultUrl(result)}
                              className="text-base font-medium text-blue-600 hover:text-blue-800 dark:text-blue-400 dark:hover:text-blue-300 hover:underline"
                            >
                              {result.title}
                            </Link>
                            {result.snippet && (
                              <p
                                className="text-base text-gray-600 dark:text-gray-300 mt-1"
                                dangerouslySetInnerHTML={{
                                  __html: sanitizeHtml(result.snippet),
                                }}
                              />
                            )}
                          </div>
                          {result.score > 0 && (
                            <span className="text-sm text-gray-400 dark:text-gray-500 flex-shrink-0 tabular-nums">
                              {result.score.toFixed(2)}
                            </span>
                          )}
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              ),
            )
          )}
        </>
      )}
    </div>
  );
}

export default function SearchPage() {
  return (
    <Suspense
      fallback={
        <div className="space-y-6">
          <h2 className="text-2xl font-bold text-gray-900 dark:text-gray-100">Search</h2>
          <p className="text-base text-gray-500 dark:text-gray-400">Loading...</p>
        </div>
      }
    >
      <SearchContent />
    </Suspense>
  );
}
