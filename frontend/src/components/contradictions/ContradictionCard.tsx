"use client";

import type { ContradictionSchema } from "@/lib/types";

interface ContradictionCardProps {
  item: ContradictionSchema;
}

const severityColors: Record<string, string> = {
  CRITICAL: "bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-400",
  HIGH: "bg-orange-100 text-orange-700 dark:bg-orange-900/30 dark:text-orange-400",
  MEDIUM: "bg-yellow-100 text-yellow-700 dark:bg-yellow-900/30 dark:text-yellow-400",
  LOW: "bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400",
};

const resolutionColors: Record<string, string> = {
  unresolved: "text-red-600",
  acknowledged: "text-amber-600",
  resolved: "text-green-600",
  disputed: "text-purple-600",
};

export default function ContradictionCard({ item }: ContradictionCardProps) {
  return (
    <div className="border rounded-lg p-4 bg-white dark:bg-gray-800 dark:border-gray-700">
      <div className="flex items-start justify-between mb-3">
        <div className="flex items-center gap-2">
          {item.person && (
            <span className="font-medium">{item.person}</span>
          )}
          <span className="text-xs text-gray-400">{item.contradiction_type}</span>
        </div>
        <div className="flex items-center gap-2">
          {item.severity && (
            <span
              className={`px-2 py-0.5 rounded-full text-xs ${
                severityColors[item.severity] || "bg-gray-100 dark:bg-gray-700"
              }`}
            >
              {item.severity}
            </span>
          )}
          <span
            className={`text-xs font-medium ${
              resolutionColors[item.resolution] || "text-gray-500"
            }`}
          >
            {item.resolution}
          </span>
        </div>
      </div>

      {/* Side-by-side statements */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
        <div className="p-3 rounded bg-red-50 dark:bg-red-900/10 border border-red-100 dark:border-red-900/30">
          <p className="text-xs text-red-600 dark:text-red-400 font-medium mb-1">
            Statement A {item.date_a ? `(${item.date_a})` : ""}
          </p>
          <p className="text-sm">{item.statement_a || "No statement recorded"}</p>
        </div>
        <div className="p-3 rounded bg-blue-50 dark:bg-blue-900/10 border border-blue-100 dark:border-blue-900/30">
          <p className="text-xs text-blue-600 dark:text-blue-400 font-medium mb-1">
            Statement B {item.date_b ? `(${item.date_b})` : ""}
          </p>
          <p className="text-sm">{item.statement_b || "No statement recorded"}</p>
        </div>
      </div>

      {item.confidence && (
        <p className="text-xs text-gray-400 mt-2">
          Confidence: {item.confidence}
        </p>
      )}
    </div>
  );
}
