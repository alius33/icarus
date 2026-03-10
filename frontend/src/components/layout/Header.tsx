"use client";

import { usePathname, useRouter } from "next/navigation";
import { Search } from "lucide-react";
import { useState, useCallback, type FormEvent } from "react";

const routeLabels: Record<string, string> = {
  "/": "Dashboard",
  "/transcripts": "Transcripts",
  "/summaries": "Summaries",
  "/weekly-reports": "Weekly Reports",
  "/workstreams": "Workstreams",
  "/stakeholders": "Stakeholders",
  "/timeline": "Timeline",
  "/decisions": "Decisions",
  "/action-items": "Action Items",
  "/open-threads": "Open Threads",
  "/glossary": "Glossary",
  "/search": "Search",
};

function getBreadcrumb(pathname: string): string {
  // Exact match first
  if (routeLabels[pathname]) return routeLabels[pathname];

  // Try parent route for detail pages like /transcripts/123
  const segments = pathname.split("/").filter(Boolean);
  if (segments.length >= 2) {
    const parentPath = `/${segments[0]}`;
    const parentLabel = routeLabels[parentPath];
    if (parentLabel) {
      return `${parentLabel} / Detail`;
    }
  }

  return "Page";
}

export default function Header() {
  const pathname = usePathname();
  const router = useRouter();
  const [query, setQuery] = useState("");

  const handleSearch = useCallback(
    (e: FormEvent) => {
      e.preventDefault();
      const trimmed = query.trim();
      if (trimmed) {
        router.push(`/search?q=${encodeURIComponent(trimmed)}`);
      }
    },
    [query, router],
  );

  const breadcrumb = getBreadcrumb(pathname);

  return (
    <header className="sticky top-0 z-40 flex h-16 items-center justify-between border-b border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 px-8">
      {/* Breadcrumb */}
      <div>
        <h1 className="text-lg font-semibold text-gray-900 dark:text-gray-100">{breadcrumb}</h1>
      </div>

      {/* Search */}
      <form onSubmit={handleSearch} className="relative w-72">
        <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-gray-400" />
        <input
          type="text"
          placeholder="Search transcripts, decisions..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          className="w-full rounded-lg border border-gray-300 dark:border-gray-600 bg-gray-50 dark:bg-gray-700 py-2 pl-10 pr-4 text-sm text-gray-900 dark:text-gray-100 placeholder-gray-400 dark:placeholder-gray-500 transition-colors focus:border-blue-500 focus:bg-white dark:focus:bg-gray-600 focus:outline-none focus:ring-1 focus:ring-blue-500"
        />
      </form>
    </header>
  );
}
