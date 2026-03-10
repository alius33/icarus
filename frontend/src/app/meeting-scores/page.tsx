"use client";

import { useMemo } from "react";
import { useMeetingScores, useMeetingScoreTrend } from "@/lib/swr";
import { BarChart3, TrendingUp, TrendingDown, Minus, Award } from "lucide-react";
import type { MeetingScoreSchema } from "@/lib/types";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Radar,
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
} from "recharts";

// ── Colours & helpers ──────────────────────────────────────────────────────────

const MEETING_TYPE_COLORS: Record<string, string> = {
  standup: "#3b82f6",
  workshop: "#8b5cf6",
  review: "#22c55e",
  planning: "#f59e0b",
  demo: "#06b6d4",
  "one-on-one": "#ec4899",
  governance: "#6b7280",
  default: "#9ca3af",
};

function scoreColor(score: number): string {
  if (score >= 8) return "text-green-600 dark:text-green-400";
  if (score >= 6) return "text-yellow-600 dark:text-yellow-400";
  if (score >= 4) return "text-orange-600 dark:text-orange-400";
  return "text-red-600 dark:text-red-400";
}

function scoreBgColor(score: number): string {
  if (score >= 8) return "bg-green-100 dark:bg-green-900/30";
  if (score >= 6) return "bg-yellow-100 dark:bg-yellow-900/30";
  if (score >= 4) return "bg-orange-100 dark:bg-orange-900/30";
  return "bg-red-100 dark:bg-red-900/30";
}

function meetingTypeColor(type: string | null): string {
  if (!type) return MEETING_TYPE_COLORS.default;
  return MEETING_TYPE_COLORS[type] || MEETING_TYPE_COLORS.default;
}

function meetingTypeBadgeClass(type: string | null): string {
  const map: Record<string, string> = {
    standup: "bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-400",
    workshop: "bg-purple-100 text-purple-700 dark:bg-purple-900/30 dark:text-purple-400",
    review: "bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400",
    planning: "bg-amber-100 text-amber-700 dark:bg-amber-900/30 dark:text-amber-400",
    demo: "bg-cyan-100 text-cyan-700 dark:bg-cyan-900/30 dark:text-cyan-400",
    "one-on-one": "bg-pink-100 text-pink-700 dark:bg-pink-900/30 dark:text-pink-400",
    governance: "bg-gray-100 text-gray-700 dark:bg-gray-700 dark:text-gray-300",
  };
  if (!type) return "bg-gray-100 text-gray-600 dark:bg-gray-700 dark:text-gray-300";
  return map[type] || map.governance;
}

// ── Custom dot component for LineChart ──────────────────────────────────────────

interface CustomDotProps {
  cx?: number;
  cy?: number;
  payload?: { meeting_type: string };
}

function CustomDot({ cx, cy, payload }: CustomDotProps) {
  if (cx === undefined || cy === undefined || !payload) return null;
  const color = meetingTypeColor(payload.meeting_type);
  return (
    <circle
      cx={cx}
      cy={cy}
      r={5}
      fill={color}
      stroke="white"
      strokeWidth={2}
    />
  );
}

// ── Main page ──────────────────────────────────────────────────────────────────

export default function MeetingScoresPage() {
  const { data: scores, isLoading: loadingScores } = useMeetingScores();
  const { data: trend, isLoading: loadingTrend } = useMeetingScoreTrend();

  const isLoading = loadingScores || loadingTrend;

  // Compute overall stats
  const stats = useMemo(() => {
    if (!scores || scores.length === 0) {
      return {
        average: 0,
        best: null as MeetingScoreSchema | null,
        worst: null as MeetingScoreSchema | null,
        trendDirection: "flat" as "up" | "down" | "flat",
        count: 0,
      };
    }

    const avg = scores.reduce((sum, s) => sum + s.overall_score, 0) / scores.length;
    const sorted = [...scores].sort((a, b) => b.overall_score - a.overall_score);
    const best = sorted[0];
    const worst = sorted[sorted.length - 1];

    // Determine trend from most recent half vs older half
    let trendDirection: "up" | "down" | "flat" = "flat";
    if (trend && trend.length >= 4) {
      const half = Math.floor(trend.length / 2);
      const recentAvg = trend.slice(half).reduce((s, t) => s + t.score, 0) / (trend.length - half);
      const olderAvg = trend.slice(0, half).reduce((s, t) => s + t.score, 0) / half;
      if (recentAvg - olderAvg > 0.3) trendDirection = "up";
      else if (olderAvg - recentAvg > 0.3) trendDirection = "down";
    }

    return { average: avg, best, worst, trendDirection, count: scores.length };
  }, [scores, trend]);

  // Sort scores by date (newest first) for the card layout
  const sortedScores = useMemo(() => {
    if (!scores) return [];
    return [...scores].sort((a, b) => {
      if (!a.date && !b.date) return 0;
      if (!a.date) return 1;
      if (!b.date) return -1;
      return b.date.localeCompare(a.date);
    });
  }, [scores]);

  // Chart data
  const chartData = useMemo(() => {
    if (!trend) return [];
    return trend.map((t) => ({
      date: t.date,
      score: t.score,
      meeting_type: t.meeting_type || "unknown",
    }));
  }, [trend]);

  // Loading
  if (isLoading) {
    return (
      <div className="space-y-6">
        <div>
          <h1 className="text-2xl font-bold text-gray-900 dark:text-gray-100">Meeting Effectiveness</h1>
          <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">
            Track and improve meeting quality across five key dimensions
          </p>
        </div>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          {[1, 2, 3, 4].map((i) => (
            <div key={i} className="h-24 bg-gray-200 dark:bg-gray-700 rounded-lg animate-pulse" />
          ))}
        </div>
        <div className="h-80 bg-gray-200 dark:bg-gray-700 rounded-lg animate-pulse" />
      </div>
    );
  }

  if (!scores || scores.length === 0) {
    return (
      <div className="space-y-6">
        <div>
          <h1 className="text-2xl font-bold text-gray-900 dark:text-gray-100">Meeting Effectiveness</h1>
          <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">
            Track and improve meeting quality across five key dimensions
          </p>
        </div>
        <div className="text-center py-16">
          <BarChart3 className="h-12 w-12 mx-auto text-gray-300 dark:text-gray-600 mb-4" />
          <p className="text-gray-500 dark:text-gray-400">
            No data yet. Run <code className="px-1.5 py-0.5 bg-gray-100 dark:bg-gray-700 rounded text-sm">/analyse-deep</code> to populate.
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-900 dark:text-gray-100">Meeting Effectiveness</h1>
        <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">
          Track and improve meeting quality across five key dimensions
        </p>
      </div>

      {/* Summary stats */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <StatCard
          label="Average Score"
          value={stats.average.toFixed(1)}
          subtext={`/ 10 across ${stats.count} meetings`}
          valueColor={scoreColor(stats.average)}
        />
        <StatCard
          label="Best Meeting"
          value={stats.best ? stats.best.overall_score.toFixed(1) : "--"}
          subtext={stats.best?.meeting_title || ""}
          valueColor="text-green-600 dark:text-green-400"
        />
        <StatCard
          label="Worst Meeting"
          value={stats.worst ? stats.worst.overall_score.toFixed(1) : "--"}
          subtext={stats.worst?.meeting_title || ""}
          valueColor="text-red-600 dark:text-red-400"
        />
        <StatCard
          label="Trend"
          value={stats.trendDirection === "up" ? "Improving" : stats.trendDirection === "down" ? "Declining" : "Stable"}
          icon={
            stats.trendDirection === "up" ? (
              <TrendingUp className="w-5 h-5 text-green-500" />
            ) : stats.trendDirection === "down" ? (
              <TrendingDown className="w-5 h-5 text-red-500" />
            ) : (
              <Minus className="w-5 h-5 text-gray-400" />
            )
          }
          valueColor={
            stats.trendDirection === "up"
              ? "text-green-600 dark:text-green-400"
              : stats.trendDirection === "down"
                ? "text-red-600 dark:text-red-400"
                : "text-gray-600 dark:text-gray-300"
          }
        />
      </div>

      {/* Trend line chart */}
      {chartData.length > 0 && (
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow border border-gray-200 dark:border-gray-700 p-4">
          <h2 className="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-4">
            Score Trend Over Time
          </h2>
          <ResponsiveContainer width="100%" height={350}>
            <LineChart data={chartData} margin={{ top: 10, right: 30, left: 0, bottom: 0 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#374151" opacity={0.2} />
              <XAxis
                dataKey="date"
                tick={{ fontSize: 12, fill: "#9ca3af" }}
                tickFormatter={(v: string) => {
                  const d = new Date(v);
                  return `${d.getDate()}/${d.getMonth() + 1}`;
                }}
              />
              <YAxis
                domain={[0, 10]}
                tick={{ fontSize: 12, fill: "#9ca3af" }}
                tickCount={6}
              />
              <Tooltip
                contentStyle={{
                  backgroundColor: "#1f2937",
                  border: "1px solid #374151",
                  borderRadius: "0.5rem",
                  color: "#f9fafb",
                }}
                labelStyle={{ color: "#9ca3af" }}
                formatter={(value: unknown) => {
                  const num = typeof value === "number" ? value : 0;
                  return [`${num.toFixed(1)} / 10`, "Score"];
                }}
                labelFormatter={(label: unknown) => {
                  const d = new Date(String(label));
                  return d.toLocaleDateString();
                }}
              />
              <Line
                type="monotone"
                dataKey="score"
                stroke="#3b82f6"
                strokeWidth={2.5}
                dot={<CustomDot />}
                activeDot={{ r: 7, stroke: "#3b82f6", strokeWidth: 2 }}
              />
            </LineChart>
          </ResponsiveContainer>

          {/* Meeting type legend */}
          <div className="flex gap-4 flex-wrap mt-3 pt-3 border-t border-gray-100 dark:border-gray-700">
            {Object.entries(MEETING_TYPE_COLORS)
              .filter(([k]) => k !== "default")
              .map(([type, color]) => (
                <div key={type} className="flex items-center gap-1.5 text-xs text-gray-500 dark:text-gray-400">
                  <span
                    className="inline-block w-3 h-3 rounded-full"
                    style={{ backgroundColor: color }}
                  />
                  {type}
                </div>
              ))}
          </div>
        </div>
      )}

      {/* Individual meeting cards with radar charts */}
      <div>
        <h2 className="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-4">
          Meeting Breakdown
        </h2>
        <div className="grid gap-4 md:grid-cols-2">
          {sortedScores.map((meeting) => (
            <MeetingCard key={meeting.id} meeting={meeting} />
          ))}
        </div>
      </div>
    </div>
  );
}

// ── Meeting Card with Radar Chart ──────────────────────────────────────────────

function MeetingCard({ meeting }: { meeting: MeetingScoreSchema }) {
  const radarData = [
    {
      dimension: "Decision Velocity",
      value: meeting.decision_velocity ?? 0,
      fullMark: 10,
    },
    {
      dimension: "Action Clarity",
      value: meeting.action_clarity ?? 0,
      fullMark: 10,
    },
    {
      dimension: "Engagement Balance",
      value: meeting.engagement_balance ?? 0,
      fullMark: 10,
    },
    {
      dimension: "Topic Completion",
      value: meeting.topic_completion ?? 0,
      fullMark: 10,
    },
    {
      dimension: "Follow Through",
      value: meeting.follow_through ?? 0,
      fullMark: 10,
    },
  ];

  const hasRadarData = radarData.some((d) => d.value > 0);

  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow border border-gray-200 dark:border-gray-700 overflow-hidden">
      {/* Card header */}
      <div className="px-5 py-3 border-b border-gray-100 dark:border-gray-700">
        <div className="flex items-start justify-between">
          <div className="flex-1 min-w-0">
            <h3 className="font-medium text-gray-900 dark:text-gray-100 truncate">
              {meeting.meeting_title || "Untitled meeting"}
            </h3>
            <div className="flex items-center gap-2 mt-1 flex-wrap">
              {meeting.date && (
                <span className="text-xs text-gray-500 dark:text-gray-400">{meeting.date}</span>
              )}
              {meeting.meeting_type && (
                <span className={`px-2 py-0.5 rounded-full text-xs font-medium ${meetingTypeBadgeClass(meeting.meeting_type)}`}>
                  {meeting.meeting_type}
                </span>
              )}
              {meeting.duration_category && (
                <span className="text-xs text-gray-400 dark:text-gray-500">
                  {meeting.duration_category}
                </span>
              )}
              {meeting.participant_count !== null && (
                <span className="text-xs text-gray-400 dark:text-gray-500">
                  {meeting.participant_count} participants
                </span>
              )}
            </div>
          </div>

          {/* Big score number */}
          <div className={`flex-shrink-0 ml-3 text-center ${scoreBgColor(meeting.overall_score)} rounded-lg px-3 py-2`}>
            <p className={`text-2xl font-bold ${scoreColor(meeting.overall_score)}`}>
              {meeting.overall_score.toFixed(1)}
            </p>
            <p className="text-xs text-gray-500 dark:text-gray-400">/ 10</p>
          </div>
        </div>
      </div>

      {/* Radar chart + recommendations */}
      <div className="p-4">
        {hasRadarData && (
          <div className="flex justify-center mb-3">
            <ResponsiveContainer width={280} height={220}>
              <RadarChart data={radarData} cx="50%" cy="50%" outerRadius="75%">
                <PolarGrid stroke="#374151" opacity={0.3} />
                <PolarAngleAxis
                  dataKey="dimension"
                  tick={{ fontSize: 10, fill: "#9ca3af" }}
                  tickLine={false}
                />
                <PolarRadiusAxis
                  domain={[0, 10]}
                  tick={{ fontSize: 9, fill: "#6b7280" }}
                  axisLine={false}
                  tickCount={3}
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
          </div>
        )}

        {/* Dimension breakdown */}
        <div className="grid grid-cols-5 gap-2 mb-3">
          {radarData.map((dim) => (
            <div key={dim.dimension} className="text-center">
              <p className={`text-sm font-semibold ${scoreColor(dim.value)}`}>
                {dim.value > 0 ? dim.value.toFixed(1) : "--"}
              </p>
              <p className="text-[10px] text-gray-500 dark:text-gray-400 leading-tight mt-0.5">
                {dim.dimension}
              </p>
            </div>
          ))}
        </div>

        {/* Recommendations */}
        {meeting.recommendations && (
          <div className="mt-3 pt-3 border-t border-gray-100 dark:border-gray-700">
            <p className="text-xs font-medium text-gray-700 dark:text-gray-300 mb-1 flex items-center gap-1">
              <Award className="w-3.5 h-3.5 text-amber-500" />
              Recommendations
            </p>
            <p className="text-xs text-gray-600 dark:text-gray-400 leading-relaxed">
              {meeting.recommendations}
            </p>
          </div>
        )}
      </div>
    </div>
  );
}

// ── Stat Card ──────────────────────────────────────────────────────────────────

function StatCard({
  label,
  value,
  subtext,
  valueColor,
  icon,
}: {
  label: string;
  value: string;
  subtext?: string;
  valueColor?: string;
  icon?: React.ReactNode;
}) {
  return (
    <div className="border rounded-lg p-4 bg-white dark:bg-gray-800 dark:border-gray-700">
      <p className="text-sm text-gray-500 dark:text-gray-400">{label}</p>
      <div className="flex items-center gap-2 mt-1">
        {icon}
        <p className={`text-2xl font-bold ${valueColor || "text-gray-900 dark:text-gray-100"}`}>
          {value}
        </p>
      </div>
      {subtext && (
        <p className="text-xs text-gray-400 dark:text-gray-500 mt-1 truncate">{subtext}</p>
      )}
    </div>
  );
}
