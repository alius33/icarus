"use client";

import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Legend,
} from "recharts";
import type { MeetingScoreTrend } from "@/lib/types";

interface ScoreTrendChartProps {
  data: MeetingScoreTrend[];
}

const MEETING_TYPE_COLORS: Record<string, string> = {
  standup: "#3b82f6",
  workshop: "#8b5cf6",
  review: "#22c55e",
  strategy: "#f59e0b",
  "1:1": "#ef4444",
  governance: "#06b6d4",
  default: "#6b7280",
};

export default function ScoreTrendChart({ data }: ScoreTrendChartProps) {
  if (!data.length) {
    return (
      <div className="flex items-center justify-center h-64 text-gray-400">
        No trend data available.
      </div>
    );
  }

  // Prepare chart data with colored dots
  const chartData = data.map((point) => ({
    date: point.date,
    score: point.score,
    meetingType: point.meeting_type || "unknown",
  }));

  // Get unique meeting types
  const meetingTypes = Array.from(
    new Set(data.map((d) => d.meeting_type || "unknown"))
  );

  return (
    <div className="border rounded-lg p-4 bg-white dark:bg-gray-800 dark:border-gray-700">
      <h3 className="text-sm font-semibold mb-4">Score Trend Over Time</h3>
      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={chartData}>
          <CartesianGrid strokeDasharray="3 3" opacity={0.3} />
          <XAxis
            dataKey="date"
            tick={{ fontSize: 11 }}
            tickFormatter={(val: string) => {
              const d = new Date(val);
              return `${d.getMonth() + 1}/${d.getDate()}`;
            }}
          />
          <YAxis domain={[0, 100]} tick={{ fontSize: 11 }} />
          <Tooltip
            content={({ active, payload }) => {
              if (!active || !payload?.length) return null;
              const item = payload[0].payload;
              return (
                <div className="bg-white dark:bg-gray-800 border dark:border-gray-700 rounded-lg shadow-lg p-3 text-sm">
                  <p className="font-medium">{item.date}</p>
                  <p>
                    Score: <span className="font-semibold">{item.score}</span>
                  </p>
                  <p className="text-gray-500">Type: {item.meetingType}</p>
                </div>
              );
            }}
          />
          <Legend
            formatter={(value: string) => (
              <span className="text-xs capitalize">{value}</span>
            )}
          />
          <Line
            type="monotone"
            dataKey="score"
            stroke="#3b82f6"
            strokeWidth={2}
            dot={(props: Record<string, unknown>) => {
              const { cx, cy, payload } = props as { cx: number; cy: number; payload: { meetingType: string } };
              const color =
                MEETING_TYPE_COLORS[payload.meetingType] ||
                MEETING_TYPE_COLORS.default;
              return (
                <circle
                  key={`dot-${cx}-${cy}`}
                  cx={cx}
                  cy={cy}
                  r={5}
                  fill={color}
                  stroke="white"
                  strokeWidth={2}
                />
              );
            }}
          />
        </LineChart>
      </ResponsiveContainer>

      {/* Meeting type color legend */}
      <div className="flex gap-3 mt-2 flex-wrap justify-center">
        {meetingTypes.map((type) => (
          <div key={type} className="flex items-center gap-1.5 text-xs">
            <div
              className="w-3 h-3 rounded-full"
              style={{
                backgroundColor:
                  MEETING_TYPE_COLORS[type] || MEETING_TYPE_COLORS.default,
              }}
            />
            <span className="capitalize text-gray-500 dark:text-gray-400">
              {type}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}
