"use client";

import { healthRagColor, healthRagTextColor } from "@/lib/utils";
import type { ProgrammeStatus } from "@/lib/types";
import { Shield, TrendingUp, AlertTriangle, CheckCircle2, Clock } from "lucide-react";

interface Props {
  status: ProgrammeStatus;
}

export default function ProgrammeStatusCard({ status }: Props) {
  return (
    <div className="rounded-lg border border-forest-200 bg-white dark:bg-forest-800 p-5">
      <div className="flex items-start gap-4">
        {/* Health RAG indicator */}
        <div className="flex flex-col items-center gap-1">
          <div
            className={`h-10 w-10 rounded-full flex items-center justify-center ${healthRagColor(status.health_rag)}`}
          >
            <Shield className="h-5 w-5 text-forest-950 dark:text-white" />
          </div>
          <span
            className={`text-[10px] font-semibold uppercase ${healthRagTextColor(status.health_rag)}`}
          >
            {status.health_rag}
          </span>
        </div>

        {/* Narrative */}
        <div className="flex-1 min-w-0">
          <h3 className="text-base font-semibold text-forest-950 mb-1">
            Programme Health
          </h3>
          <p className="text-base text-forest-600 leading-relaxed">
            {status.narrative}
          </p>

          {/* Win / Risk row */}
          <div className="mt-3 grid grid-cols-1 gap-2 sm:grid-cols-2">
            {status.biggest_win && (
              <div className="flex items-start gap-2 rounded-md bg-green-50 px-3 py-2">
                <TrendingUp className="h-4 w-4 text-green-600 mt-0.5 flex-shrink-0" />
                <div>
                  <span className="text-[10px] font-semibold uppercase text-green-700">
                    Biggest Win
                  </span>
                  <p className="text-sm text-green-800 mt-0.5">
                    {status.biggest_win}
                  </p>
                </div>
              </div>
            )}
            {status.biggest_risk && (
              <div className="flex items-start gap-2 rounded-md bg-red-50 px-3 py-2">
                <AlertTriangle className="h-4 w-4 text-red-600 mt-0.5 flex-shrink-0" />
                <div>
                  <span className="text-[10px] font-semibold uppercase text-red-700">
                    Biggest Risk
                  </span>
                  <p className="text-sm text-red-800 mt-0.5">
                    {status.biggest_risk}
                  </p>
                </div>
              </div>
            )}
          </div>
        </div>

        {/* Key numbers */}
        <div className="hidden sm:flex gap-4 text-center">
          <div>
            <div className="flex items-center justify-center gap-1">
              <CheckCircle2 className="h-3.5 w-3.5 text-forest-300" />
              <span className="text-lg font-bold text-forest-950">
                {status.open_actions}
              </span>
            </div>
            <span className="text-[10px] text-forest-400">Open Actions</span>
          </div>
          <div>
            <div className="flex items-center justify-center gap-1">
              <Clock className="h-3.5 w-3.5 text-red-400" />
              <span className="text-lg font-bold text-red-600">
                {status.overdue_count}
              </span>
            </div>
            <span className="text-[10px] text-forest-400">Overdue</span>
          </div>
          <div>
            <div className="flex items-center justify-center gap-1">
              <AlertTriangle className="h-3.5 w-3.5 text-amber-400" />
              <span className="text-lg font-bold text-amber-600">
                {status.critical_risks}
              </span>
            </div>
            <span className="text-[10px] text-forest-400">Critical Risks</span>
          </div>
        </div>
      </div>
    </div>
  );
}
