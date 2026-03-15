"use client";

import { useSearchParams } from "next/navigation";
import { Suspense } from "react";
import WeeklyPlanTabBar from "@/components/weekly-plan/WeeklyPlanTabBar";
import WeeklyPlansTab from "@/components/weekly-plan/WeeklyPlansTab";
import DeliverablesTab from "@/components/weekly-plan/DeliverablesTab";

function WeeklyPlanContent() {
  const searchParams = useSearchParams();
  const activeTab = (searchParams.get("tab") as "plans" | "deliverables") || "plans";

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-gray-900 dark:text-white">Weekly Plan</h1>
      </div>
      <WeeklyPlanTabBar activeTab={activeTab} />
      {activeTab === "plans" && <WeeklyPlansTab />}
      {activeTab === "deliverables" && <DeliverablesTab />}
    </div>
  );
}

export default function WeeklyPlanPage() {
  return (
    <Suspense fallback={<div className="text-gray-400">Loading...</div>}>
      <WeeklyPlanContent />
    </Suspense>
  );
}
