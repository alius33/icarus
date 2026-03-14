"use client";

import { useEffect, useState, useCallback } from "react";
import { AudioLines, CheckCircle2, AlertTriangle, HelpCircle, Send, CheckCheck } from "lucide-react";
import { cn } from "@/lib/utils";
import { api } from "@/lib/api";
import type {
  SpeakerReviewResponse,
  SpeakerReviewItem,
  ConfirmAction,
} from "@/lib/types";
import SpeakerReviewTable from "@/components/speaker-review/SpeakerReviewTable";
import ContextModal from "@/components/speaker-review/ContextModal";

type Tab = "review" | "applied" | "all";

export default function SpeakerReviewPage() {
  const [data, setData] = useState<SpeakerReviewResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [tab, setTab] = useState<Tab>("review");
  const [actions, setActions] = useState<Map<string, ConfirmAction>>(new Map());
  const [submitting, setSubmitting] = useState(false);
  const [submitResult, setSubmitResult] = useState<{ applied: number; rejected: number; errors: string[] } | null>(null);
  const [contextItem, setContextItem] = useState<SpeakerReviewItem | null>(null);

  const fetchData = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const result = await api.getSpeakerReview();
      setData(result);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Failed to load speaker review data");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchData();
  }, [fetchData]);

  const handleAction = (id: string, action: ConfirmAction) => {
    setActions((prev) => {
      const next = new Map(prev);
      const existing = next.get(id);
      // Toggle off if same action clicked again
      if (existing?.action === action.action && action.action !== "manual") {
        next.delete(id);
      } else {
        next.set(id, action);
      }
      return next;
    });
  };

  const pendingActions = Array.from(actions.values());
  const acceptCount = pendingActions.filter((a) => a.action === "accept" || a.action === "manual").length;
  const rejectCount = pendingActions.filter((a) => a.action === "reject").length;

  const handleSubmit = async () => {
    if (pendingActions.length === 0) return;
    setSubmitting(true);
    setSubmitResult(null);
    try {
      const result = await api.confirmSpeakerIds(pendingActions);
      setSubmitResult(result);
      setActions(new Map());
      // Refresh data
      await fetchData();
    } catch (e) {
      setSubmitResult({
        applied: 0,
        rejected: 0,
        errors: [e instanceof Error ? e.message : "Unknown error"],
      });
    } finally {
      setSubmitting(false);
    }
  };

  const handleAcceptAllFlagged = () => {
    if (!data) return;
    const flagged = data.items.filter((i) => i.status === "flagged" || i.status === "unresolved");
    const next = new Map(actions);
    flagged.forEach((item) => {
      if (!next.has(item.id)) {
        next.set(item.id, { id: item.id, action: "accept" });
      }
    });
    setActions(next);
  };

  // Filter items by tab
  const getFilteredItems = (): SpeakerReviewItem[] => {
    if (!data) return [];
    switch (tab) {
      case "review":
        return data.items.filter((i) => i.status === "flagged" || i.status === "unresolved");
      case "applied":
        return data.items.filter((i) => i.status === "applied");
      case "all":
        return data.items;
    }
  };

  const filteredItems = getFilteredItems();
  const reviewCount = data?.items.filter((i) => i.status === "flagged" || i.status === "unresolved").length || 0;

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <div className="flex items-center gap-3">
          <AudioLines className="h-7 w-7 text-blue-600" />
          <h1 className="text-2xl font-bold text-gray-900 dark:text-gray-100">
            Speaker Identification Review
          </h1>
        </div>
        <p className="text-base text-gray-500 dark:text-gray-400 mt-1">
          Review and confirm speaker identifications from the automated pipeline
        </p>
      </div>

      {/* Loading state */}
      {loading && (
        <div className="flex items-center justify-center py-12">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600" />
        </div>
      )}

      {/* Error state */}
      {error && (
        <div className="rounded-lg bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 p-4">
          <p className="text-red-700 dark:text-red-300 text-base">{error}</p>
          <button
            onClick={fetchData}
            className="mt-2 text-base text-red-600 dark:text-red-400 underline hover:no-underline"
          >
            Try again
          </button>
        </div>
      )}

      {data && !loading && (
        <>
          {/* Summary Cards */}
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
            <MetricCard
              label="Total Identifications"
              value={data.summary.total_identifications}
              icon={<AudioLines className="h-5 w-5" />}
              color="blue"
            />
            <MetricCard
              label="Applied"
              value={data.summary.applied_count}
              icon={<CheckCircle2 className="h-5 w-5" />}
              color="green"
            />
            <MetricCard
              label="Needs Review"
              value={data.summary.flagged_count}
              icon={<AlertTriangle className="h-5 w-5" />}
              color="amber"
            />
            <MetricCard
              label="Unresolved"
              value={data.summary.unresolved_count}
              icon={<HelpCircle className="h-5 w-5" />}
              color="red"
            />
          </div>

          {/* Method breakdown */}
          {Object.keys(data.summary.methods).length > 0 && (
            <div className="flex flex-wrap gap-2">
              {Object.entries(data.summary.methods)
                .sort(([, a], [, b]) => b - a)
                .map(([method, count]) => (
                  <span
                    key={method}
                    className="inline-flex items-center gap-1.5 rounded-full bg-gray-100 dark:bg-gray-800 px-3 py-1 text-sm text-gray-600 dark:text-gray-300"
                  >
                    <span className="font-medium">
                      {method.replace(/_/g, " ")}
                    </span>
                    <span className="text-gray-400 dark:text-gray-500">{count}</span>
                  </span>
                ))}
            </div>
          )}

          {/* Tabs */}
          <div className="flex items-center gap-1 border-b border-gray-200 dark:border-gray-700">
            <TabButton
              active={tab === "review"}
              onClick={() => setTab("review")}
              label="Needs Review"
              count={reviewCount}
              countColor="amber"
            />
            <TabButton
              active={tab === "applied"}
              onClick={() => setTab("applied")}
              label="Applied"
              count={data.summary.applied_count}
              countColor="green"
            />
            <TabButton
              active={tab === "all"}
              onClick={() => setTab("all")}
              label="All"
              count={data.summary.total_identifications}
              countColor="gray"
            />
          </div>

          {/* Table */}
          <div className="bg-white dark:bg-gray-900 rounded-xl border border-gray-200 dark:border-gray-700 overflow-hidden">
            <SpeakerReviewTable
              items={filteredItems}
              stakeholderNames={data.stakeholder_names}
              actions={actions}
              onAction={handleAction}
              onViewContext={setContextItem}
            />
          </div>

          {/* Action bar */}
          {(pendingActions.length > 0 || submitResult) && (
            <div className="sticky bottom-0 bg-white dark:bg-gray-900 border-t border-gray-200 dark:border-gray-700 rounded-xl shadow-lg p-4">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-4 text-base">
                  {pendingActions.length > 0 && (
                    <>
                      <span className="text-gray-600 dark:text-gray-400">
                        {pendingActions.length} pending change{pendingActions.length !== 1 && "s"}
                      </span>
                      {acceptCount > 0 && (
                        <span className="text-green-600 dark:text-green-400">
                          {acceptCount} accept
                        </span>
                      )}
                      {rejectCount > 0 && (
                        <span className="text-red-600 dark:text-red-400">
                          {rejectCount} reject
                        </span>
                      )}
                    </>
                  )}
                  {submitResult && (
                    <div className="flex items-center gap-2">
                      {submitResult.errors.length === 0 ? (
                        <span className="text-green-600 dark:text-green-400 flex items-center gap-1">
                          <CheckCircle2 className="h-4 w-4" />
                          Applied {submitResult.applied}, rejected {submitResult.rejected}
                        </span>
                      ) : (
                        <span className="text-red-600 dark:text-red-400">
                          Errors: {submitResult.errors.join(", ")}
                        </span>
                      )}
                    </div>
                  )}
                </div>

                <div className="flex items-center gap-2">
                  {tab === "review" && reviewCount > 0 && (
                    <button
                      onClick={handleAcceptAllFlagged}
                      className="flex items-center gap-2 px-3 py-2 text-base text-gray-600 dark:text-gray-300 border border-gray-300 dark:border-gray-600 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors"
                    >
                      <CheckCheck className="h-4 w-4" />
                      Accept All Flagged
                    </button>
                  )}
                  {pendingActions.length > 0 && (
                    <>
                      <button
                        onClick={() => setActions(new Map())}
                        className="px-3 py-2 text-base text-gray-600 dark:text-gray-400 hover:text-gray-800 dark:hover:text-gray-200"
                      >
                        Clear
                      </button>
                      <button
                        onClick={handleSubmit}
                        disabled={submitting}
                        className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white text-base font-medium rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                      >
                        <Send className="h-4 w-4" />
                        {submitting ? "Applying…" : `Apply ${pendingActions.length} Changes`}
                      </button>
                    </>
                  )}
                </div>
              </div>
            </div>
          )}
        </>
      )}

      {/* Context modal */}
      {contextItem && (
        <ContextModal item={contextItem} onClose={() => setContextItem(null)} />
      )}
    </div>
  );
}

function MetricCard({
  label,
  value,
  icon,
  color,
}: {
  label: string;
  value: number;
  icon: React.ReactNode;
  color: "blue" | "green" | "amber" | "red";
}) {
  const colorMap = {
    blue: "bg-blue-50 dark:bg-blue-900/20 text-blue-600 dark:text-blue-400 border-blue-200 dark:border-blue-800",
    green: "bg-green-50 dark:bg-green-900/20 text-green-600 dark:text-green-400 border-green-200 dark:border-green-800",
    amber: "bg-amber-50 dark:bg-amber-900/20 text-amber-600 dark:text-amber-400 border-amber-200 dark:border-amber-800",
    red: "bg-red-50 dark:bg-red-900/20 text-red-600 dark:text-red-400 border-red-200 dark:border-red-800",
  };

  return (
    <div className={cn("rounded-xl border p-4", colorMap[color])}>
      <div className="flex items-center justify-between">
        {icon}
        <span className="text-2xl font-bold">{value}</span>
      </div>
      <p className="text-sm mt-1 opacity-80">{label}</p>
    </div>
  );
}

function TabButton({
  active,
  onClick,
  label,
  count,
  countColor,
}: {
  active: boolean;
  onClick: () => void;
  label: string;
  count: number;
  countColor: "amber" | "green" | "gray";
}) {
  const badgeColors = {
    amber: "bg-amber-100 dark:bg-amber-900/30 text-amber-700 dark:text-amber-300",
    green: "bg-green-100 dark:bg-green-900/30 text-green-700 dark:text-green-300",
    gray: "bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-300",
  };

  return (
    <button
      onClick={onClick}
      className={cn(
        "px-4 py-2.5 text-base font-medium border-b-2 transition-colors",
        active
          ? "border-blue-600 text-blue-600 dark:text-blue-400"
          : "border-transparent text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-200"
      )}
    >
      {label}
      <span className={cn("ml-2 inline-flex items-center rounded-full px-2 py-0.5 text-sm font-medium", badgeColors[countColor])}>
        {count}
      </span>
    </button>
  );
}
