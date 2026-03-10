"use client";

import Link from "next/link";
import { usePathname, useSearchParams } from "next/navigation";
import { cn } from "@/lib/utils";

const TABS = [
  { key: "overview", label: "Overview" },
  { key: "decisions", label: "Decisions" },
  { key: "actions", label: "Actions" },
  { key: "threads", label: "Threads" },
] as const;

export type TabKey = (typeof TABS)[number]["key"];

export default function ProjectTabBar() {
  const pathname = usePathname();
  const searchParams = useSearchParams();
  const activeTab = (searchParams.get("tab") as TabKey) || "overview";

  return (
    <div className="border-b border-gray-200 bg-white">
      <nav className="-mb-px flex space-x-6 px-6" aria-label="Tabs">
        {TABS.map((tab) => {
          const isActive = activeTab === tab.key;
          return (
            <Link
              key={tab.key}
              href={`${pathname}?tab=${tab.key}`}
              className={cn(
                "whitespace-nowrap border-b-2 py-3 text-sm font-medium transition-colors",
                isActive
                  ? "border-blue-600 text-blue-600"
                  : "border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700",
              )}
            >
              {tab.label}
            </Link>
          );
        })}
      </nav>
    </div>
  );
}
