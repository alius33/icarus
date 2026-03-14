"use client";

import { useState } from "react";
import {
  ChevronDown,
  ChevronRight,
  Check,
  X,
  Pencil,
  Eye,
} from "lucide-react";
import { cn } from "@/lib/utils";
import type { SpeakerReviewItem, ConfirmAction } from "@/lib/types";

interface SpeakerReviewTableProps {
  items: SpeakerReviewItem[];
  stakeholderNames: string[];
  actions: Map<string, ConfirmAction>;
  onAction: (id: string, action: ConfirmAction) => void;
  onViewContext: (item: SpeakerReviewItem) => void;
}

function confidenceColor(c: number): string {
  if (c >= 0.8) return "bg-green-500";
  if (c >= 0.65) return "bg-yellow-500";
  if (c >= 0.5) return "bg-orange-500";
  return "bg-red-500";
}

function confidenceTextColor(c: number): string {
  if (c >= 0.8) return "text-green-600 dark:text-green-400";
  if (c >= 0.65) return "text-yellow-600 dark:text-yellow-400";
  if (c >= 0.5) return "text-orange-600 dark:text-orange-400";
  return "text-red-600 dark:text-red-400";
}

function statusBadge(status: string) {
  const config: Record<string, { label: string; bg: string; text: string }> = {
    applied: { label: "Applied", bg: "bg-green-100 dark:bg-green-900/30", text: "text-green-700 dark:text-green-300" },
    flagged: { label: "Needs Review", bg: "bg-amber-100 dark:bg-amber-900/30", text: "text-amber-700 dark:text-amber-300" },
    unresolved: { label: "Unresolved", bg: "bg-red-100 dark:bg-red-900/30", text: "text-red-700 dark:text-red-300" },
  };
  const c = config[status] || config.flagged;
  return (
    <span className={cn("inline-flex items-center rounded-full px-2 py-0.5 text-sm font-medium", c.bg, c.text)}>
      {c.label}
    </span>
  );
}

function methodBadge(method: string) {
  const short = method
    .replace(/_/g, " ")
    .replace(/\b\w/g, (c) => c.toUpperCase());
  return (
    <span className="inline-flex items-center rounded-md bg-gray-100 dark:bg-gray-700 px-2 py-0.5 text-sm text-gray-600 dark:text-gray-300">
      {short}
    </span>
  );
}

function truncateFilename(name: string, maxLen = 35): string {
  if (name.length <= maxLen) return name;
  return name.slice(0, maxLen - 3) + "…";
}

export default function SpeakerReviewTable({
  items,
  stakeholderNames,
  actions,
  onAction,
  onViewContext,
}: SpeakerReviewTableProps) {
  const [expandedRows, setExpandedRows] = useState<Set<string>>(new Set());
  const [manualInputs, setManualInputs] = useState<Map<string, string>>(new Map());
  const [sortField, setSortField] = useState<"confidence" | "transcript" | "method">("confidence");
  const [sortAsc, setSortAsc] = useState(true);

  const toggleExpand = (id: string) => {
    setExpandedRows((prev) => {
      const next = new Set(prev);
      if (next.has(id)) next.delete(id);
      else next.add(id);
      return next;
    });
  };

  const handleSort = (field: typeof sortField) => {
    if (sortField === field) {
      setSortAsc(!sortAsc);
    } else {
      setSortField(field);
      setSortAsc(true);
    }
  };

  const sorted = [...items].sort((a, b) => {
    const dir = sortAsc ? 1 : -1;
    if (sortField === "confidence") return (a.confidence - b.confidence) * dir;
    if (sortField === "transcript")
      return a.transcript_filename.localeCompare(b.transcript_filename) * dir;
    return a.method.localeCompare(b.method) * dir;
  });

  const getActionState = (id: string) => actions.get(id);

  if (items.length === 0) {
    return (
      <div className="text-center py-12 text-gray-500 dark:text-gray-400">
        <p className="text-lg font-medium">No items in this view</p>
        <p className="text-base mt-1">All identifications are in other tabs.</p>
      </div>
    );
  }

  return (
    <div className="overflow-x-auto">
      <table className="w-full text-base">
        <thead>
          <tr className="border-b border-gray-200 dark:border-gray-700 text-left">
            <th className="w-8 p-3" />
            <th
              className="p-3 font-medium text-gray-500 dark:text-gray-400 cursor-pointer hover:text-gray-700 dark:hover:text-gray-200"
              onClick={() => handleSort("transcript")}
            >
              Transcript {sortField === "transcript" && (sortAsc ? "↑" : "↓")}
            </th>
            <th className="p-3 font-medium text-gray-500 dark:text-gray-400">Speaker Label</th>
            <th className="p-3 font-medium text-gray-500 dark:text-gray-400">→ Identified As</th>
            <th
              className="p-3 font-medium text-gray-500 dark:text-gray-400 cursor-pointer hover:text-gray-700 dark:hover:text-gray-200"
              onClick={() => handleSort("confidence")}
            >
              Confidence {sortField === "confidence" && (sortAsc ? "↑" : "↓")}
            </th>
            <th
              className="p-3 font-medium text-gray-500 dark:text-gray-400 cursor-pointer hover:text-gray-700 dark:hover:text-gray-200"
              onClick={() => handleSort("method")}
            >
              Method {sortField === "method" && (sortAsc ? "↑" : "↓")}
            </th>
            <th className="p-3 font-medium text-gray-500 dark:text-gray-400">Status</th>
            <th className="p-3 font-medium text-gray-500 dark:text-gray-400 text-right">Actions</th>
          </tr>
        </thead>
        <tbody>
          {sorted.map((item) => {
            const isExpanded = expandedRows.has(item.id);
            const action = getActionState(item.id);
            const manualVal = manualInputs.get(item.id) || "";

            return (
              <TableRow
                key={item.id}
                item={item}
                isExpanded={isExpanded}
                action={action}
                manualVal={manualVal}
                stakeholderNames={stakeholderNames}
                onToggleExpand={() => toggleExpand(item.id)}
                onAction={onAction}
                onViewContext={() => onViewContext(item)}
                onManualChange={(val) =>
                  setManualInputs((prev) => new Map(prev).set(item.id, val))
                }
              />
            );
          })}
        </tbody>
      </table>
    </div>
  );
}

function TableRow({
  item,
  isExpanded,
  action,
  manualVal,
  stakeholderNames,
  onToggleExpand,
  onAction,
  onViewContext,
  onManualChange,
}: {
  item: SpeakerReviewItem;
  isExpanded: boolean;
  action: ConfirmAction | undefined;
  manualVal: string;
  stakeholderNames: string[];
  onToggleExpand: () => void;
  onAction: (id: string, action: ConfirmAction) => void;
  onViewContext: () => void;
  onManualChange: (val: string) => void;
}) {
  const [showManual, setShowManual] = useState(false);
  const [suggestions, setSuggestions] = useState<string[]>([]);

  const handleManualInput = (val: string) => {
    onManualChange(val);
    if (val.length >= 2) {
      const matches = stakeholderNames.filter((n) =>
        n.toLowerCase().includes(val.toLowerCase())
      );
      setSuggestions(matches.slice(0, 5));
    } else {
      setSuggestions([]);
    }
  };

  const submitManual = (name: string) => {
    if (name.trim()) {
      onAction(item.id, { id: item.id, action: "manual", manual_name: name.trim() });
      setShowManual(false);
      setSuggestions([]);
    }
  };

  const rowHighlight = action
    ? action.action === "accept" || action.action === "manual"
      ? "bg-green-50 dark:bg-green-900/10"
      : action.action === "reject"
      ? "bg-red-50 dark:bg-red-900/10"
      : ""
    : "";

  return (
    <>
      <tr
        className={cn(
          "border-b border-gray-100 dark:border-gray-800 hover:bg-gray-50 dark:hover:bg-gray-800/50 transition-colors",
          rowHighlight
        )}
      >
        {/* Expand toggle */}
        <td className="p-3">
          <button
            onClick={onToggleExpand}
            className="text-gray-400 hover:text-gray-600 dark:hover:text-gray-300"
          >
            {isExpanded ? (
              <ChevronDown className="h-4 w-4" />
            ) : (
              <ChevronRight className="h-4 w-4" />
            )}
          </button>
        </td>

        {/* Transcript */}
        <td className="p-3">
          <span className="text-gray-900 dark:text-gray-100 font-medium" title={item.transcript_filename}>
            {truncateFilename(item.transcript_filename)}
          </span>
          {item.timestamp && (
            <span className="ml-2 text-sm text-gray-400">@{item.timestamp}</span>
          )}
        </td>

        {/* Speaker Label */}
        <td className="p-3 text-gray-600 dark:text-gray-300">
          {item.speaker_label}
        </td>

        {/* Identified As */}
        <td className="p-3">
          <span className="font-medium text-gray-900 dark:text-gray-100">
            {action?.action === "manual" && action.manual_name
              ? action.manual_name
              : item.identified_as || "—"}
          </span>
        </td>

        {/* Confidence */}
        <td className="p-3">
          <div className="flex items-center gap-2">
            <div className="w-16 h-2 bg-gray-200 dark:bg-gray-700 rounded-full overflow-hidden">
              <div
                className={cn("h-full rounded-full", confidenceColor(item.confidence))}
                style={{ width: `${Math.round(item.confidence * 100)}%` }}
              />
            </div>
            <span className={cn("text-sm font-mono", confidenceTextColor(item.confidence))}>
              {(item.confidence * 100).toFixed(0)}%
            </span>
          </div>
        </td>

        {/* Method */}
        <td className="p-3">{methodBadge(item.method)}</td>

        {/* Status */}
        <td className="p-3">{statusBadge(item.status)}</td>

        {/* Actions */}
        <td className="p-3">
          <div className="flex items-center justify-end gap-1">
            <button
              onClick={onViewContext}
              title="View transcript context"
              className="p-1.5 rounded hover:bg-gray-200 dark:hover:bg-gray-700 text-gray-500 dark:text-gray-400"
            >
              <Eye className="h-4 w-4" />
            </button>
            <button
              onClick={() =>
                onAction(item.id, { id: item.id, action: "accept" })
              }
              title="Accept identification"
              className={cn(
                "p-1.5 rounded",
                action?.action === "accept"
                  ? "bg-green-100 dark:bg-green-900/40 text-green-600"
                  : "hover:bg-green-100 dark:hover:bg-green-900/30 text-gray-500 dark:text-gray-400 hover:text-green-600"
              )}
            >
              <Check className="h-4 w-4" />
            </button>
            <button
              onClick={() =>
                onAction(item.id, { id: item.id, action: "reject" })
              }
              title="Reject identification"
              className={cn(
                "p-1.5 rounded",
                action?.action === "reject"
                  ? "bg-red-100 dark:bg-red-900/40 text-red-600"
                  : "hover:bg-red-100 dark:hover:bg-red-900/30 text-gray-500 dark:text-gray-400 hover:text-red-600"
              )}
            >
              <X className="h-4 w-4" />
            </button>
            <button
              onClick={() => setShowManual(!showManual)}
              title="Manual override"
              className={cn(
                "p-1.5 rounded",
                action?.action === "manual"
                  ? "bg-blue-100 dark:bg-blue-900/40 text-blue-600"
                  : "hover:bg-blue-100 dark:hover:bg-blue-900/30 text-gray-500 dark:text-gray-400 hover:text-blue-600"
              )}
            >
              <Pencil className="h-4 w-4" />
            </button>
          </div>
        </td>
      </tr>

      {/* Manual name input row */}
      {showManual && (
        <tr className="bg-blue-50/50 dark:bg-blue-900/10">
          <td colSpan={8} className="p-3 pl-12">
            <div className="flex items-center gap-2 relative">
              <label className="text-base text-gray-600 dark:text-gray-400 whitespace-nowrap">
                Assign to:
              </label>
              <div className="relative flex-1 max-w-xs">
                <input
                  type="text"
                  value={manualVal}
                  onChange={(e) => handleManualInput(e.target.value)}
                  onKeyDown={(e) => {
                    if (e.key === "Enter") submitManual(manualVal);
                    if (e.key === "Escape") setShowManual(false);
                  }}
                  placeholder="Type stakeholder name…"
                  className="w-full rounded-md border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 px-3 py-1.5 text-base focus:outline-none focus:ring-2 focus:ring-blue-500"
                  autoFocus
                />
                {suggestions.length > 0 && (
                  <div className="absolute z-10 top-full left-0 right-0 mt-1 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-md shadow-lg">
                    {suggestions.map((name) => (
                      <button
                        key={name}
                        onClick={() => {
                          onManualChange(name);
                          submitManual(name);
                        }}
                        className="block w-full text-left px-3 py-2 text-base hover:bg-blue-50 dark:hover:bg-blue-900/30 text-gray-700 dark:text-gray-200"
                      >
                        {name}
                      </button>
                    ))}
                  </div>
                )}
              </div>
              <button
                onClick={() => submitManual(manualVal)}
                disabled={!manualVal.trim()}
                className="px-3 py-1.5 text-base bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                Apply
              </button>
              <button
                onClick={() => setShowManual(false)}
                className="px-3 py-1.5 text-base text-gray-600 dark:text-gray-400 hover:text-gray-800 dark:hover:text-gray-200"
              >
                Cancel
              </button>
            </div>
          </td>
        </tr>
      )}

      {/* Expanded evidence row */}
      {isExpanded && (
        <tr className="bg-gray-50/50 dark:bg-gray-800/30">
          <td colSpan={8} className="p-4 pl-12">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-base">
              <div>
                <h4 className="font-medium text-gray-700 dark:text-gray-300 mb-1">Evidence</h4>
                <p className="text-gray-600 dark:text-gray-400 whitespace-pre-wrap">
                  {item.evidence || "No evidence provided."}
                </p>
              </div>
              <div>
                <h4 className="font-medium text-gray-700 dark:text-gray-300 mb-1">Details</h4>
                <dl className="space-y-1">
                  <div className="flex gap-2">
                    <dt className="text-gray-500 dark:text-gray-500">Meeting type:</dt>
                    <dd className="text-gray-700 dark:text-gray-300">{item.meeting_type}</dd>
                  </div>
                  <div className="flex gap-2">
                    <dt className="text-gray-500 dark:text-gray-500">Known speakers:</dt>
                    <dd className="text-gray-700 dark:text-gray-300">
                      {item.known_speakers.join(", ") || "—"}
                    </dd>
                  </div>
                  {item.timestamp && (
                    <div className="flex gap-2">
                      <dt className="text-gray-500 dark:text-gray-500">Timestamp:</dt>
                      <dd className="text-gray-700 dark:text-gray-300">{item.timestamp}</dd>
                    </div>
                  )}
                </dl>
              </div>
            </div>
          </td>
        </tr>
      )}
    </>
  );
}
