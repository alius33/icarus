"use client";

import { useEffect, Suspense } from "react";
import { DashboardProvider, useDashboardDispatch } from "./DashboardContext";
import { useDashboardData } from "./hooks/useDashboardData";
import ProgrammePulse from "./ProgrammePulse";
import type { DashboardDataV2 } from "@/lib/types";

interface Props {
  initialData: DashboardDataV2;
}

function DashboardInner({ initialData }: Props) {
  const { data } = useDashboardData();
  const dispatch = useDashboardDispatch();

  useEffect(() => {
    if (!data) {
      dispatch({ type: "SET_DATA", payload: initialData });
    }
  }, []); // eslint-disable-line react-hooks/exhaustive-deps

  const d = data || initialData;

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Programme Dashboard</h1>
        <p className="text-sm text-gray-500 mt-1">
          {d.projects.length} projects &middot; {d.open_actions} open actions &middot; {d.total_transcripts} transcripts
        </p>
      </div>

      <ProgrammePulse projects={d.projects} />
    </div>
  );
}

export default function DashboardClient({ initialData }: Props) {
  return (
    <Suspense fallback={<DashboardSkeleton />}>
      <DashboardProvider initialData={initialData}>
        <DashboardInner initialData={initialData} />
      </DashboardProvider>
    </Suspense>
  );
}

function DashboardSkeleton() {
  return (
    <div className="space-y-6 animate-pulse">
      <div>
        <div className="h-8 w-64 bg-gray-200 rounded" />
        <div className="h-4 w-48 bg-gray-100 rounded mt-2" />
      </div>
      <div className="grid grid-cols-1 gap-5 md:grid-cols-2 lg:grid-cols-3">
        {Array.from({ length: 9 }).map((_, i) => (
          <div key={i} className="h-48 bg-gray-100 rounded-xl" />
        ))}
      </div>
    </div>
  );
}
