"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { cn } from "@/lib/utils";

interface Props {
  activeTab: "plans" | "deliverables";
}

const TABS = [
  { key: "plans" as const, label: "Weekly Plans" },
  { key: "deliverables" as const, label: "Deliverables" },
];

export default function WeeklyPlanTabBar({ activeTab }: Props) {
  const pathname = usePathname();

  return (
    <div className="border-b border-forest-200 dark:border-forest-700">
      <nav className="-mb-px flex gap-4">
        {TABS.map((tab) => (
          <Link
            key={tab.key}
            href={`${pathname}?tab=${tab.key}`}
            className={cn(
              "whitespace-nowrap border-b-2 px-1 pb-3 text-sm font-medium transition-colors",
              activeTab === tab.key
                ? "border-forest-500 text-forest-300"
                : "border-transparent text-forest-300 hover:border-gray-600 hover:text-gray-300"
            )}
          >
            {tab.label}
          </Link>
        ))}
      </nav>
    </div>
  );
}
