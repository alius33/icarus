"use client";

import {
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  Radar,
  ResponsiveContainer,
  Tooltip,
} from "recharts";
import type { MeetingScoreSchema } from "@/lib/types";

interface MeetingRadarProps {
  meeting: MeetingScoreSchema;
}

export default function MeetingRadar({ meeting }: MeetingRadarProps) {
  const radarData = [
    {
      dimension: "Decision Velocity",
      value: meeting.decision_velocity ?? 0,
      fullMark: 100,
    },
    {
      dimension: "Action Clarity",
      value: meeting.action_clarity ?? 0,
      fullMark: 100,
    },
    {
      dimension: "Engagement",
      value: meeting.engagement_balance ?? 0,
      fullMark: 100,
    },
    {
      dimension: "Topic Completion",
      value: meeting.topic_completion ?? 0,
      fullMark: 100,
    },
    {
      dimension: "Follow Through",
      value: meeting.follow_through ?? 0,
      fullMark: 100,
    },
  ];

  const scoreColor =
    meeting.overall_score >= 75
      ? "#22c55e"
      : meeting.overall_score >= 50
        ? "#f59e0b"
        : "#ef4444";

  return (
    <div className="border rounded-lg p-4 bg-white dark:bg-gray-800 dark:border-gray-700">
      <div className="flex items-center justify-between mb-2">
        <h3 className="text-base font-semibold">
          {meeting.meeting_title || "Meeting"} Breakdown
        </h3>
        <div className="flex items-center gap-2">
          <span
            className="text-lg font-bold"
            style={{ color: scoreColor }}
          >
            {meeting.overall_score}
          </span>
          <span className="text-sm text-gray-400">/ 100</span>
        </div>
      </div>

      {meeting.date && (
        <p className="text-sm text-gray-500 dark:text-gray-400 mb-3">
          {meeting.date}
          {meeting.meeting_type && (
            <span className="ml-2 px-2 py-0.5 bg-gray-100 dark:bg-gray-700 rounded-full">
              {meeting.meeting_type}
            </span>
          )}
        </p>
      )}

      <ResponsiveContainer width="100%" height={250}>
        <RadarChart data={radarData}>
          <PolarGrid stroke="#e5e7eb" />
          <PolarAngleAxis
            dataKey="dimension"
            tick={{ fontSize: 11, fill: "#9ca3af" }}
          />
          <PolarRadiusAxis
            angle={90}
            domain={[0, 100]}
            tick={{ fontSize: 9 }}
            tickCount={5}
          />
          <Tooltip
            content={({ active, payload }) => {
              if (!active || !payload?.length) return null;
              const item = payload[0].payload;
              return (
                <div className="bg-white dark:bg-gray-800 border dark:border-gray-700 rounded-lg shadow-lg p-2 text-base">
                  <p className="font-medium">{item.dimension}</p>
                  <p className="text-blue-600">{item.value} / 100</p>
                </div>
              );
            }}
          />
          <Radar
            name="Score"
            dataKey="value"
            stroke="#3b82f6"
            fill="#3b82f6"
            fillOpacity={0.25}
            strokeWidth={2}
          />
        </RadarChart>
      </ResponsiveContainer>

      {meeting.recommendations && (
        <div className="mt-3 p-2 bg-amber-50 dark:bg-amber-900/10 rounded text-sm text-amber-800 dark:text-amber-300">
          <span className="font-medium">Recommendations: </span>
          {meeting.recommendations}
        </div>
      )}
    </div>
  );
}
