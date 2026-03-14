"use client";

import { useState, useMemo } from "react";
import { useContradictions } from "@/lib/swr";
import { AlertTriangle, HelpCircle, ArrowLeftRight, Calendar, User2, Eye } from "lucide-react";
import type { ContradictionSchema } from "@/lib/types";

type TabKey = "contradictions" | "gaps";

const SEVERITY_COLORS: Record<string, { bg: string; text: string; dot: string }> = {
  CRITICAL: {
    bg: "bg-red-100 dark:bg-red-900/30",
    text: "text-red-700 dark:text-red-400",
    dot: "bg-red-500",
  },
  HIGH: {
    bg: "bg-orange-100 dark:bg-orange-900/30",
    text: "text-orange-700 dark:text-orange-400",
    dot: "bg-orange-500",
  },
  MEDIUM: {
    bg: "bg-yellow-100 dark:bg-yellow-900/30",
    text: "text-yellow-700 dark:text-yellow-400",
    dot: "bg-yellow-500",
  },
  LOW: {
    bg: "bg-green-100 dark:bg-green-900/30",
    text: "text-green-700 dark:text-green-400",
    dot: "bg-green-500",
  },
};

const RESOLUTION_COLORS: Record<string, string> = {
  unresolved: "bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-400",
  partial: "bg-yellow-100 text-yellow-700 dark:bg-yellow-900/30 dark:text-yellow-400",
  resolved: "bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400",
  acknowledged: "bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-400",
};

export default function ContradictionsPage() {
  const [activeTab, setActiveTab] = useState<TabKey>("contradictions");
  const [severityFilter, setSeverityFilter] = useState("");

  const { data: contradictions, isLoading: loadingContradictions } = useContradictions("contradiction");
  const { data: gaps, isLoading: loadingGaps } = useContradictions("gap");

  const isLoading = loadingContradictions || loadingGaps;

  const currentData = activeTab === "contradictions" ? contradictions : gaps;

  const filtered = useMemo(() => {
    if (!currentData) return [];
    let items = [...currentData];
    if (severityFilter) {
      items = items.filter((item) => item.severity === severityFilter);
    }
    // Sort by date (newest first), then by severity
    const severityOrder: Record<string, number> = { CRITICAL: 0, HIGH: 1, MEDIUM: 2, LOW: 3 };
    items.sort((a, b) => {
      const dateA = a.date || "";
      const dateB = b.date || "";
      if (dateB !== dateA) return dateB.localeCompare(dateA);
      return (severityOrder[a.severity || "LOW"] || 3) - (severityOrder[b.severity || "LOW"] || 3);
    });
    return items;
  }, [currentData, severityFilter]);

  const tabs: { key: TabKey; label: string; count: number; icon: React.ReactNode }[] = [
    {
      key: "contradictions",
      label: "Contradictions",
      count: contradictions?.length || 0,
      icon: <ArrowLeftRight className="w-4 h-4" />,
    },
    {
      key: "gaps",
      label: "Information Gaps",
      count: gaps?.length || 0,
      icon: <HelpCircle className="w-4 h-4" />,
    },
  ];

  // Loading state
  if (isLoading) {
    return (
      <div className="space-y-6">
        <div>
          <h1 className="text-2xl font-bold text-gray-900 dark:text-gray-100">
            Contradictions & Information Gaps
          </h1>
          <p className="text-base text-gray-500 dark:text-gray-400 mt-1">
            Identify contradictory statements and missing information across meetings
          </p>
        </div>
        <div className="space-y-4">
          <div className="h-10 bg-gray-200 dark:bg-gray-700 rounded animate-pulse" />
          {[1, 2, 3].map((i) => (
            <div key={i} className="h-48 bg-gray-200 dark:bg-gray-700 rounded-lg animate-pulse" />
          ))}
        </div>
      </div>
    );
  }

  const totalCount = (contradictions?.length || 0) + (gaps?.length || 0);

  if (totalCount === 0) {
    return (
      <div className="space-y-6">
        <div>
          <h1 className="text-2xl font-bold text-gray-900 dark:text-gray-100">
            Contradictions & Information Gaps
          </h1>
          <p className="text-base text-gray-500 dark:text-gray-400 mt-1">
            Identify contradictory statements and missing information across meetings
          </p>
        </div>
        <div className="text-center py-16">
          <AlertTriangle className="h-12 w-12 mx-auto text-gray-300 dark:text-gray-600 mb-4" />
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
        <h1 className="text-2xl font-bold text-gray-900 dark:text-gray-100">
          Contradictions & Information Gaps
        </h1>
        <p className="text-base text-gray-500 dark:text-gray-400 mt-1">
          Identify contradictory statements and missing information across meetings
        </p>
      </div>

      {/* Tabs */}
      <div className="flex gap-1 border-b border-gray-200 dark:border-gray-700">
        {tabs.map((tab) => (
          <button
            key={tab.key}
            onClick={() => {
              setActiveTab(tab.key);
              setSeverityFilter("");
            }}
            className={`flex items-center gap-2 px-4 py-2.5 text-base font-medium border-b-2 transition-colors ${
              activeTab === tab.key
                ? "border-blue-600 text-blue-600 dark:text-blue-400 dark:border-blue-400"
                : "border-transparent text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-300"
            }`}
          >
            {tab.icon}
            {tab.label}
            <span className="ml-1 text-sm bg-gray-100 dark:bg-gray-700 px-1.5 py-0.5 rounded-full">
              {tab.count}
            </span>
          </button>
        ))}
      </div>

      {/* Severity filter */}
      <div className="flex gap-3 items-center">
        <label className="text-base text-gray-500 dark:text-gray-400">Filter by severity:</label>
        <select
          value={severityFilter}
          onChange={(e) => setSeverityFilter(e.target.value)}
          className="text-base border rounded-md px-3 py-1.5 bg-white dark:bg-gray-800 dark:border-gray-700 dark:text-gray-200"
        >
          <option value="">All Severities</option>
          <option value="CRITICAL">Critical</option>
          <option value="HIGH">High</option>
          <option value="MEDIUM">Medium</option>
          <option value="LOW">Low</option>
        </select>
        {severityFilter && (
          <button
            onClick={() => setSeverityFilter("")}
            className="text-sm text-blue-600 hover:underline dark:text-blue-400"
          >
            Clear
          </button>
        )}
        <span className="ml-auto text-base text-gray-500 dark:text-gray-400">
          {filtered.length} result{filtered.length !== 1 ? "s" : ""}
        </span>
      </div>

      {/* Cards */}
      {filtered.length > 0 ? (
        <div className="space-y-4">
          {filtered.map((item) =>
            activeTab === "contradictions" ? (
              <ContradictionCard key={item.id} item={item} />
            ) : (
              <GapCard key={item.id} item={item} />
            ),
          )}
        </div>
      ) : (
        <div className="text-center py-12 text-gray-400 dark:text-gray-500">
          No {activeTab === "contradictions" ? "contradictions" : "information gaps"} found
          {severityFilter ? " matching the selected severity" : ""}.
        </div>
      )}
    </div>
  );
}

// ── Contradiction Card ─────────────────────────────────────────────────────────

function ContradictionCard({ item }: { item: ContradictionSchema }) {
  const sev = SEVERITY_COLORS[item.severity || "LOW"] || SEVERITY_COLORS.LOW;
  const resClass = RESOLUTION_COLORS[item.resolution] || RESOLUTION_COLORS.unresolved;

  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow border border-gray-200 dark:border-gray-700 overflow-hidden">
      {/* Header */}
      <div className="px-5 py-3 border-b border-gray-100 dark:border-gray-700 flex items-center justify-between">
        <div className="flex items-center gap-3">
          {item.person && (
            <span className="flex items-center gap-1.5 text-base font-medium text-gray-900 dark:text-gray-100">
              <User2 className="w-4 h-4 text-gray-400" />
              {item.person}
            </span>
          )}
          <span className={`px-2 py-0.5 rounded-full text-sm font-medium ${sev.bg} ${sev.text}`}>
            {item.severity || "UNKNOWN"}
          </span>
          <span className={`px-2 py-0.5 rounded-full text-sm font-medium ${resClass}`}>
            {item.resolution}
          </span>
        </div>
        {item.confidence && (
          <ConfidenceBadge confidence={item.confidence} />
        )}
      </div>

      {/* Statements side-by-side */}
      <div className="grid grid-cols-1 md:grid-cols-2 divide-y md:divide-y-0 md:divide-x divide-gray-100 dark:divide-gray-700">
        {/* Statement A */}
        <div className="px-5 py-4">
          <div className="flex items-center gap-2 mb-2">
            <span className="text-sm font-semibold text-red-500 uppercase tracking-wider">Statement A</span>
            {item.date_a && (
              <span className="flex items-center gap-1 text-sm text-gray-400">
                <Calendar className="w-3 h-3" />
                {item.date_a}
              </span>
            )}
          </div>
          <p className="text-base text-gray-700 dark:text-gray-300 leading-relaxed">
            {item.statement_a || "Not recorded"}
          </p>
        </div>

        {/* Statement B */}
        <div className="px-5 py-4">
          <div className="flex items-center gap-2 mb-2">
            <span className="text-sm font-semibold text-blue-500 uppercase tracking-wider">Statement B</span>
            {item.date_b && (
              <span className="flex items-center gap-1 text-sm text-gray-400">
                <Calendar className="w-3 h-3" />
                {item.date_b}
              </span>
            )}
          </div>
          <p className="text-base text-gray-700 dark:text-gray-300 leading-relaxed">
            {item.statement_b || "Not recorded"}
          </p>
        </div>
      </div>

      {/* Footer */}
      {item.contradiction_type && (
        <div className="px-5 py-2 border-t border-gray-100 dark:border-gray-700 bg-gray-50 dark:bg-gray-800/50">
          <span className="text-sm text-gray-500 dark:text-gray-400">
            Type: <span className="font-medium text-gray-700 dark:text-gray-300">{item.contradiction_type}</span>
          </span>
        </div>
      )}
    </div>
  );
}

// ── Gap Card ───────────────────────────────────────────────────────────────────

function GapCard({ item }: { item: ContradictionSchema }) {
  const sev = SEVERITY_COLORS[item.severity || "LOW"] || SEVERITY_COLORS.LOW;

  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow border border-gray-200 dark:border-gray-700 p-5">
      <div className="flex items-start justify-between mb-3">
        <div className="flex-1">
          <p className="text-base font-medium text-gray-900 dark:text-gray-100 mb-1">
            {item.gap_description || "Unspecified information gap"}
          </p>
          {item.expected_source && (
            <p className="text-sm text-gray-500 dark:text-gray-400">
              Expected source: <span className="font-medium text-gray-700 dark:text-gray-300">{item.expected_source}</span>
            </p>
          )}
        </div>
        <span className={`px-2 py-0.5 rounded-full text-sm font-medium flex-shrink-0 ml-3 ${sev.bg} ${sev.text}`}>
          {item.severity || "UNKNOWN"}
        </span>
      </div>

      <div className="flex items-center gap-4 text-sm text-gray-500 dark:text-gray-400">
        {item.last_mentioned && (
          <span className="flex items-center gap-1">
            <Calendar className="w-3 h-3" />
            Last mentioned: {item.last_mentioned}
          </span>
        )}
        {item.meetings_absent !== null && item.meetings_absent !== undefined && (
          <span className="flex items-center gap-1">
            <Eye className="w-3 h-3" />
            Absent from {item.meetings_absent} meeting{item.meetings_absent !== 1 ? "s" : ""}
          </span>
        )}
        {item.confidence && (
          <ConfidenceBadge confidence={item.confidence} />
        )}
      </div>

      {item.person && (
        <div className="mt-2 flex items-center gap-1.5 text-sm text-gray-500 dark:text-gray-400">
          <User2 className="w-3 h-3" />
          Related to: <span className="font-medium text-gray-700 dark:text-gray-300">{item.person}</span>
        </div>
      )}
    </div>
  );
}

// ── Confidence badge ───────────────────────────────────────────────────────────

function ConfidenceBadge({ confidence }: { confidence: string | null }) {
  const colors: Record<string, string> = {
    HIGH: "bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400",
    MEDIUM: "bg-amber-100 text-amber-700 dark:bg-amber-900/30 dark:text-amber-400",
    LOW: "bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-400",
  };
  if (!confidence) return null;
  return (
    <span className={`px-2 py-0.5 rounded-full text-sm ${colors[confidence] || "bg-gray-100 dark:bg-gray-700"}`}>
      {confidence} confidence
    </span>
  );
}
