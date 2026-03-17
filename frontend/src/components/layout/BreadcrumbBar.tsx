"use client";

import { usePathname } from "next/navigation";
import Breadcrumbs, { type BreadcrumbItem } from "@/components/Breadcrumbs";

/**
 * Route-to-label mapping derived from the Sidebar navSections.
 * Flat map of href -> label for all known routes.
 */
const routeMap: Record<string, string> = {
  "/": "Dashboard",
  "/timeline": "Timeline",
  "/transcripts": "Transcripts",
  "/upload": "Upload",
  "/analysis": "Analysis",
  "/analysis/summaries": "Summaries",
  "/analysis/weekly": "Weekly Reports",
  "/projects": "Projects",
  "/stakeholders": "Stakeholders",
  "/decisions": "Decisions",
  "/action-items": "Actions",
  "/open-threads": "Open Threads",
  "/commitments": "Commitments",
  "/my-items": "My Items",
  "/wins": "Programme Wins",
  "/outreach": "Outreach Tracker",
  "/glossary": "Glossary",
  "/search": "Search",
  "/updates": "Updates",
};

/**
 * Section groupings: maps first-level routes to their parent section
 * for routes that live under a logical parent in the sidebar.
 */
const sectionParents: Record<string, { label: string; href: string }> = {
  "/analysis/summaries": { label: "Analysis", href: "/analysis/summaries" },
  "/analysis/weekly": { label: "Analysis", href: "/analysis/summaries" },
};

function buildBreadcrumbs(pathname: string): BreadcrumbItem[] {
  // Dashboard is the root — no breadcrumbs needed
  if (pathname === "/") return [];

  const crumbs: BreadcrumbItem[] = [{ label: "Dashboard", href: "/" }];
  const segments = pathname.split("/").filter(Boolean);

  // Check for a known section parent
  const fullPath = `/${segments.join("/")}`;
  const parent = sectionParents[fullPath];
  if (parent) {
    crumbs.push({ label: parent.label, href: parent.href });
  }

  // Build progressive path segments
  let currentPath = "";
  for (let i = 0; i < segments.length; i++) {
    currentPath += `/${segments[i]}`;
    const label = routeMap[currentPath];
    const isLast = i === segments.length - 1;

    if (label) {
      // Skip if it duplicates the parent we already added
      if (parent && currentPath === parent.href && !isLast) continue;
      crumbs.push({
        label,
        href: isLast ? undefined : currentPath,
      });
    } else if (isLast) {
      // Dynamic segment (e.g., /transcripts/[id]) — show "Detail"
      const parentPath = `/${segments.slice(0, i).join("/")}`;
      const parentLabel = routeMap[parentPath];
      if (parentLabel && !crumbs.some((c) => c.label === parentLabel)) {
        crumbs.push({ label: parentLabel, href: parentPath });
      }
      crumbs.push({ label: "Detail" });
    }
  }

  return crumbs;
}

export default function BreadcrumbBar() {
  const pathname = usePathname();
  const items = buildBreadcrumbs(pathname);

  if (items.length === 0) return null;

  return (
    <div className="border-b border-forest-200 dark:border-forest-700 bg-white dark:bg-forest-950 px-4 md:px-8 py-2.5 overflow-hidden">
      <Breadcrumbs items={items} />
    </div>
  );
}
