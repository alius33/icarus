"use client";

import { usePathname, useRouter } from "next/navigation";
import { Search, Menu } from "lucide-react";
import { useState, useCallback, type FormEvent } from "react";
import { useSidebarState } from "@/lib/hooks/useSidebarState";

const routeLabels: Record<string, string> = {
  "/": "Dashboard",
  "/transcripts": "Transcripts",
  "/summaries": "Summaries",
  "/weekly-reports": "Weekly Reports",
  "/stakeholders": "Stakeholders",
  "/timeline": "Timeline",
  "/decisions": "Decisions",
  "/action-items": "Action Items",
  "/open-threads": "Open Threads",
  "/glossary": "Glossary",
  "/search": "Search",
};

function getBreadcrumb(pathname: string): string {
  if (routeLabels[pathname]) return routeLabels[pathname];

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
  const { toggle } = useSidebarState();

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
    <header className="sticky top-0 z-30 flex h-16 items-center justify-between border-b border-forest-200 dark:border-forest-700 bg-white dark:bg-forest-950 px-4 md:px-8">
      <div className="flex items-center gap-3">
        {/* Hamburger — mobile only */}
        <button
          onClick={toggle}
          className="inline-flex items-center justify-center rounded-md p-2 -ml-2 text-forest-500 dark:text-forest-200 hover:bg-forest-100 dark:hover:bg-forest-700 transition-colors md:hidden min-h-[44px] min-w-[44px]"
          aria-label="Open navigation menu"
        >
          <Menu className="h-5 w-5" />
        </button>

        {/* Breadcrumb */}
        <h1 className="text-lg font-semibold text-forest-950 dark:text-forest-50 truncate">
          {breadcrumb}
        </h1>
      </div>

      {/* Search */}
      <form onSubmit={handleSearch} className="relative w-full max-w-xs md:w-72 ml-4">
        <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-forest-400" />
        <input
          type="text"
          placeholder="Search..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          className="w-full rounded-lg border border-forest-200 dark:border-forest-700 bg-forest-50 dark:bg-forest-800 py-2 pl-10 pr-4 text-base text-forest-950 dark:text-forest-50 placeholder-forest-400 dark:placeholder-forest-400 transition-colors focus:border-forest-500 focus:bg-white dark:focus:bg-forest-700 focus:outline-none focus:ring-1 focus:ring-forest-500"
        />
      </form>
    </header>
  );
}
