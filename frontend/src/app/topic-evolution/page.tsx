"use client";

import { useState, useMemo } from "react";
import { useTopicEvolution, useTopicMomentum } from "@/lib/swr";
import { TrendingUp, TrendingDown, Clock, MessageSquare, BarChart2 } from "lucide-react";
import type { TopicSignalSchema } from "@/lib/types";
import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Legend,
} from "recharts";

const CATEGORY_COLORS: Record<string, string> = {
  technical: "#3b82f6",
  strategic: "#8b5cf6",
  interpersonal: "#f97316",
  operational: "#22c55e",
  governance: "#6b7280",
};

const CATEGORY_BG: Record<string, string> = {
  technical: "bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-300",
  strategic: "bg-purple-100 text-purple-700 dark:bg-purple-900/30 dark:text-purple-300",
  interpersonal: "bg-orange-100 text-orange-700 dark:bg-orange-900/30 dark:text-orange-300",
  operational: "bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-300",
  governance: "bg-gray-100 text-gray-700 dark:bg-gray-700 dark:text-gray-300",
};

const INTENSITY_MAP: Record<string, number> = {
  LOW: 1,
  MEDIUM: 2,
  HIGH: 3,
  CRITICAL: 4,
};

const CATEGORIES = ["all", "technical", "strategic", "interpersonal", "operational", "governance"];

function intensityToNumber(intensity: string | null): number {
  if (!intensity) return 0;
  return INTENSITY_MAP[intensity] ?? 0;
}

export default function TopicEvolutionPage() {
  const [category, setCategory] = useState<string | undefined>();
  const { data: evolution, isLoading: loadingEvolution } = useTopicEvolution();
  const { data: momentum, isLoading: loadingMomentum } = useTopicMomentum();

  const isLoading = loadingEvolution || loadingMomentum;

  // Build chart data: merge all topic evolution points into unified date rows
  const { chartData, topicNames } = useMemo(() => {
    if (!evolution || evolution.length === 0) return { chartData: [], topicNames: [] };

    // Filter by category if selected
    const filtered = category
      ? evolution.filter((t) => t.category === category)
      : evolution;

    // Collect all unique dates and topics
    const dateSet = new Set<string>();
    const topics: string[] = [];

    filtered.forEach((topic) => {
      topics.push(topic.topic);
      topic.data_points.forEach((dp) => dateSet.add(dp.date));
    });

    const sortedDates = Array.from(dateSet).sort();

    // Build rows keyed by date, with each topic as a column
    const rows = sortedDates.map((date) => {
      const row: Record<string, string | number> = { date };
      filtered.forEach((topic) => {
        const point = topic.data_points.find((dp) => dp.date === date);
        row[topic.topic] = point ? intensityToNumber(point.intensity) : 0;
      });
      return row;
    });

    return { chartData: rows, topicNames: topics };
  }, [evolution, category]);

  // Assign colors to topics based on their category
  const topicColorMap = useMemo(() => {
    const map: Record<string, string> = {};
    if (!evolution) return map;
    const categoryTopicCounts: Record<string, number> = {};
    evolution.forEach((t) => {
      const cat = t.category || "governance";
      const baseColor = CATEGORY_COLORS[cat] || CATEGORY_COLORS.governance;
      const idx = categoryTopicCounts[cat] || 0;
      categoryTopicCounts[cat] = idx + 1;
      // Adjust opacity for multiple topics in same category
      const opacity = Math.max(0.3, 1 - idx * 0.15);
      map[t.topic] = baseColor;
      map[`${t.topic}_opacity`] = String(opacity);
    });
    return map;
  }, [evolution]);

  // Filter momentum by category
  const filteredMomentum = useMemo(() => {
    if (!momentum) return null;
    if (!category) return momentum;
    return {
      rising: momentum.rising.filter((t) => t.category === category),
      declining: momentum.declining.filter((t) => t.category === category),
      going_cold: momentum.going_cold.filter((t) => t.category === category),
    };
  }, [momentum, category]);

  if (isLoading) {
    return (
      <div className="space-y-6">
        <div>
          <h1 className="text-2xl font-bold text-gray-900 dark:text-gray-100">Topic Evolution</h1>
          <p className="text-base text-gray-500 dark:text-gray-400 mt-1">
            Track how themes emerge, intensify, and fade across meetings
          </p>
        </div>
        <div className="space-y-4">
          <div className="h-10 bg-gray-200 dark:bg-gray-700 rounded animate-pulse" />
          <div className="h-80 bg-gray-200 dark:bg-gray-700 rounded-lg animate-pulse" />
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {[1, 2, 3].map((i) => (
              <div key={i} className="h-40 bg-gray-200 dark:bg-gray-700 rounded-lg animate-pulse" />
            ))}
          </div>
        </div>
      </div>
    );
  }

  const hasData =
    (evolution && evolution.length > 0) ||
    (momentum && (momentum.rising.length > 0 || momentum.declining.length > 0 || momentum.going_cold.length > 0));

  if (!hasData) {
    return (
      <div className="space-y-6">
        <div>
          <h1 className="text-2xl font-bold text-gray-900 dark:text-gray-100">Topic Evolution</h1>
          <p className="text-base text-gray-500 dark:text-gray-400 mt-1">
            Track how themes emerge, intensify, and fade across meetings
          </p>
        </div>
        <div className="text-center py-16">
          <BarChart2 className="h-12 w-12 mx-auto text-gray-300 dark:text-gray-600 mb-4" />
          <p className="text-gray-500 dark:text-gray-400">
            No data yet. Run <code className="px-1.5 py-0.5 bg-gray-100 dark:bg-gray-700 rounded text-base">/analyse-deep</code> to populate.
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-900 dark:text-gray-100">Topic Evolution</h1>
        <p className="text-base text-gray-500 dark:text-gray-400 mt-1">
          Track how themes emerge, intensify, and fade across meetings
        </p>
      </div>

      {/* Category filter */}
      <div className="flex gap-2 flex-wrap">
        {CATEGORIES.map((cat) => (
          <button
            key={cat}
            onClick={() => setCategory(cat === "all" ? undefined : cat)}
            className={`px-3 py-1.5 text-base rounded-full border transition-colors ${
              (cat === "all" && !category) || cat === category
                ? "bg-blue-50 border-blue-200 text-blue-700 dark:bg-blue-900/30 dark:border-blue-700 dark:text-blue-300"
                : "bg-white border-gray-200 text-gray-600 hover:bg-gray-50 dark:bg-gray-800 dark:border-gray-700 dark:text-gray-300 dark:hover:bg-gray-700"
            }`}
          >
            <span className="flex items-center gap-1.5">
              {cat !== "all" && (
                <span
                  className="inline-block w-2.5 h-2.5 rounded-full"
                  style={{ backgroundColor: CATEGORY_COLORS[cat] }}
                />
              )}
              {cat.charAt(0).toUpperCase() + cat.slice(1)}
            </span>
          </button>
        ))}
      </div>

      {/* Stacked Area Chart */}
      {chartData.length > 0 && (
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-4 border border-gray-200 dark:border-gray-700">
          <h2 className="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-4">
            Topic Intensity Over Time
          </h2>
          <ResponsiveContainer width="100%" height={400}>
            <AreaChart data={chartData} margin={{ top: 10, right: 30, left: 0, bottom: 0 }}>
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
                tick={{ fontSize: 12, fill: "#9ca3af" }}
                tickFormatter={(v: number) => {
                  const labels = ["", "LOW", "MED", "HIGH", "CRIT"];
                  return labels[v] || String(v);
                }}
                domain={[0, 4]}
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
                  const labels = ["None", "LOW", "MEDIUM", "HIGH", "CRITICAL"];
                  return [labels[num] || String(num), ""];
                }}
              />
              <Legend
                wrapperStyle={{ paddingTop: "1rem" }}
                formatter={(value: string) => (
                  <span className="text-base text-gray-600 dark:text-gray-300">{value}</span>
                )}
              />
              {topicNames.map((topic) => {
                const fillColor = topicColorMap[topic] || "#6b7280";
                const opacity = parseFloat(topicColorMap[`${topic}_opacity`] || "0.6");
                return (
                  <Area
                    key={topic}
                    type="monotone"
                    dataKey={topic}
                    stackId="1"
                    stroke={fillColor}
                    fill={fillColor}
                    fillOpacity={opacity}
                    strokeWidth={1.5}
                  />
                );
              })}
            </AreaChart>
          </ResponsiveContainer>
        </div>
      )}

      {/* Momentum Sections */}
      {filteredMomentum && filteredMomentum.rising.length > 0 && (
        <MomentumSection
          title="Rising Topics"
          icon={<TrendingUp className="w-5 h-5 text-green-600" />}
          topics={filteredMomentum.rising}
        />
      )}

      {filteredMomentum && filteredMomentum.declining.length > 0 && (
        <MomentumSection
          title="Declining Topics"
          icon={<TrendingDown className="w-5 h-5 text-amber-600" />}
          topics={filteredMomentum.declining}
        />
      )}

      {filteredMomentum && filteredMomentum.going_cold.length > 0 && (
        <MomentumSection
          title="Going Cold"
          icon={<Clock className="w-5 h-5 text-red-500" />}
          topics={filteredMomentum.going_cold}
        />
      )}
    </div>
  );
}

function MomentumSection({
  title,
  icon,
  topics,
}: {
  title: string;
  icon: React.ReactNode;
  topics: TopicSignalSchema[];
}) {
  return (
    <section>
      <h2 className="text-lg font-semibold flex items-center gap-2 mb-3 text-gray-900 dark:text-gray-100">
        {icon}
        {title}
        <span className="text-base font-normal text-gray-500 dark:text-gray-400">({topics.length})</span>
      </h2>
      <div className="grid gap-3 md:grid-cols-2 lg:grid-cols-3">
        {topics.map((topic) => (
          <TopicCard key={topic.id} topic={topic} />
        ))}
      </div>
    </section>
  );
}

function TopicCard({ topic }: { topic: TopicSignalSchema }) {
  const catClass = CATEGORY_BG[topic.category || "governance"] || CATEGORY_BG.governance;

  return (
    <div className="border rounded-lg p-4 bg-white dark:bg-gray-800 dark:border-gray-700 hover:shadow-md transition-shadow">
      <div className="flex items-start justify-between mb-2">
        <h3 className="font-medium text-gray-900 dark:text-gray-100">{topic.topic}</h3>
        <TrendBadge trend={topic.trend} />
      </div>

      <div className="flex gap-2 flex-wrap mb-3">
        <span className={`px-2 py-0.5 rounded-full text-sm ${catClass}`}>
          {topic.category || "unknown"}
        </span>
        <ConfidenceBadge confidence={topic.confidence} />
      </div>

      <div className="flex items-center gap-3 text-sm text-gray-500 dark:text-gray-400 mb-2">
        <span className="flex items-center gap-1">
          <MessageSquare className="w-3 h-3" />
          {topic.meetings_count} meetings
        </span>
        {topic.first_raised && (
          <span>Since {topic.first_raised}</span>
        )}
      </div>

      {topic.key_quote && (
        <p className="text-sm text-gray-600 dark:text-gray-300 mt-2 italic border-l-2 border-gray-200 dark:border-gray-600 pl-2 line-clamp-3">
          &ldquo;{topic.key_quote}&rdquo;
        </p>
      )}
    </div>
  );
}

function TrendBadge({ trend }: { trend: string | null }) {
  const config: Record<string, { bg: string; text: string; arrow: string }> = {
    rising: { bg: "bg-green-100 dark:bg-green-900/30", text: "text-green-700 dark:text-green-400", arrow: "\u2191" },
    stable: { bg: "bg-gray-100 dark:bg-gray-700", text: "text-gray-600 dark:text-gray-300", arrow: "\u2192" },
    declining: { bg: "bg-amber-100 dark:bg-amber-900/30", text: "text-amber-700 dark:text-amber-400", arrow: "\u2193" },
    new: { bg: "bg-blue-100 dark:bg-blue-900/30", text: "text-blue-700 dark:text-blue-400", arrow: "\u2605" },
  };
  if (!trend) return null;
  const c = config[trend] || config.stable;
  return (
    <span className={`inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-sm font-medium ${c.bg} ${c.text}`}>
      {c.arrow} {trend}
    </span>
  );
}

function ConfidenceBadge({ confidence }: { confidence: string | null }) {
  const colors: Record<string, string> = {
    HIGH: "bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400",
    MEDIUM: "bg-amber-100 text-amber-700 dark:bg-amber-900/30 dark:text-amber-400",
    LOW: "bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-400",
  };
  if (!confidence) return null;
  return (
    <span className={`px-2 py-0.5 rounded-full text-sm ${colors[confidence] || "bg-gray-100 dark:bg-gray-700"}`}>
      {confidence}
    </span>
  );
}
