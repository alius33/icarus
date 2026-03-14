"use client";

import { AlertCircle } from "lucide-react";
import type { ContradictionSchema } from "@/lib/types";

interface GapCardProps {
  item: ContradictionSchema;
}

export default function GapCard({ item }: GapCardProps) {
  return (
    <div className="border rounded-lg p-4 bg-white dark:bg-gray-800 dark:border-gray-700">
      <div className="flex items-start gap-3">
        <AlertCircle className="w-5 h-5 text-amber-500 mt-0.5 flex-shrink-0" />
        <div className="flex-1 min-w-0">
          <div className="flex items-start justify-between mb-2">
            <h3 className="font-medium text-base">
              {item.gap_description || item.contradiction_type}
            </h3>
            {item.severity && (
              <span
                className={`px-2 py-0.5 rounded-full text-sm flex-shrink-0 ml-2 ${
                  item.severity === "CRITICAL"
                    ? "bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-400"
                    : item.severity === "HIGH"
                      ? "bg-orange-100 text-orange-700 dark:bg-orange-900/30 dark:text-orange-400"
                      : "bg-yellow-100 text-yellow-700 dark:bg-yellow-900/30 dark:text-yellow-400"
                }`}
              >
                {item.severity}
              </span>
            )}
          </div>

          <div className="space-y-1.5 text-base text-gray-600 dark:text-gray-300">
            {item.expected_source && (
              <p>
                <span className="text-gray-400">Expected from:</span>{" "}
                {item.expected_source}
              </p>
            )}
            {item.last_mentioned && (
              <p>
                <span className="text-gray-400">Last mentioned:</span>{" "}
                {item.last_mentioned}
              </p>
            )}
            {item.meetings_absent != null && item.meetings_absent > 0 && (
              <p>
                <span className="text-gray-400">Absent for:</span>{" "}
                <span
                  className={
                    item.meetings_absent >= 3 ? "text-red-600 font-medium" : ""
                  }
                >
                  {item.meetings_absent} meeting{item.meetings_absent !== 1 ? "s" : ""}
                </span>
              </p>
            )}
          </div>

          <div className="flex items-center gap-3 mt-2 text-sm text-gray-400">
            <span>
              Status:{" "}
              <span
                className={
                  item.resolution === "unresolved"
                    ? "text-red-600"
                    : item.resolution === "resolved"
                      ? "text-green-600"
                      : "text-amber-600"
                }
              >
                {item.resolution}
              </span>
            </span>
            {item.confidence && <span>Confidence: {item.confidence}</span>}
          </div>
        </div>
      </div>
    </div>
  );
}
