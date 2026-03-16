"use client";

import type { DashboardTab } from "@/lib/types";
import { useDashboardFilters } from "./hooks/useDashboardFilters";
import { ShieldAlert, UserCog, Activity } from "lucide-react";
import { cn } from "@/lib/utils";

const TABS: { value: DashboardTab; label: string; icon: React.ReactNode }[] = [
  {
    value: "risks",
    label: "Risks & Dependencies",
    icon: <ShieldAlert className="h-4 w-4" />,
  },
  {
    value: "resources",
    label: "Resources & Scope",
    icon: <UserCog className="h-4 w-4" />,
  },
  {
    value: "activity",
    label: "Activity & People",
    icon: <Activity className="h-4 w-4" />,
  },
];

export default function TabBar() {
  const { filters, setTab } = useDashboardFilters();

  return (
    <div className="flex border-b border-forest-200">
      {TABS.map((tab) => (
        <button
          key={tab.value}
          onClick={() => setTab(tab.value)}
          className={cn(
            "flex items-center gap-2 px-4 py-2.5 text-base font-medium border-b-2 transition-colors",
            filters.activeTab === tab.value
              ? "border-forest-500 text-forest-500"
              : "border-transparent text-forest-400 hover:text-forest-600 hover:border-forest-200",
          )}
        >
          {tab.icon}
          {tab.label}
        </button>
      ))}
    </div>
  );
}
