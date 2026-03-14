"use client";

import Link from "next/link";
import { usePathname, useSearchParams } from "next/navigation";
import { cn } from "@/lib/utils";

interface TabDef {
  key: string;
  label: string;
  countKey?: string;
}

const TABS: TabDef[] = [
  { key: "overview", label: "Overview" },
  { key: "tasks", label: "Tasks", countKey: "action_count" },
  { key: "decisions", label: "Decisions", countKey: "decision_count" },
  { key: "threads", label: "Threads", countKey: "open_thread_count" },
  { key: "summaries", label: "Summaries", countKey: "transcript_count" },
];

export type TabKey = "overview" | "tasks" | "decisions" | "threads" | "summaries";

interface Props {
  counts?: Record<string, number>;
}

export default function ProjectTabBar({ counts }: Props) {
  const pathname = usePathname();
  const searchParams = useSearchParams();
  const activeTab = (searchParams.get("tab") as TabKey) || "overview";

  return (
    <div className="border-b border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-900 overflow-x-auto scrollbar-hide -mx-4 px-4 md:mx-0 md:px-0">
      <nav className="-mb-px flex space-x-4 md:space-x-6 px-4 md:px-6 min-w-max" aria-label="Tabs">
        {TABS.map((tab) => {
          const isActive = activeTab === tab.key;
          const count = tab.countKey && counts ? counts[tab.countKey] : undefined;
          return (
            <Link
              key={tab.key}
              href={`${pathname}?tab=${tab.key}`}
              className={cn(
                "whitespace-nowrap border-b-2 py-3 text-base font-medium transition-colors flex items-center gap-1.5",
                isActive
                  ? "border-blue-600 text-blue-600"
                  : "border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700",
              )}
            >
              {tab.label}
              {count !== undefined && count > 0 && (
                <span
                  className={cn(
                    "rounded-full px-1.5 py-0.5 text-[10px] font-semibold tabular-nums",
                    isActive
                      ? "bg-blue-100 text-blue-700"
                      : "bg-gray-100 text-gray-500",
                  )}
                >
                  {count}
                </span>
              )}
            </Link>
          );
        })}
      </nav>
    </div>
  );
}
