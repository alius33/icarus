"use client";

import type { NeedsAttentionItem } from "@/lib/types";
import { AlertTriangle, Clock, AlertCircle } from "lucide-react";

function AttentionIcon({ reason }: { reason: string }) {
  if (reason === "overdue") return <AlertTriangle className="h-4 w-4 text-red-500" />;
  if (reason === "stale") return <Clock className="h-4 w-4 text-amber-500" />;
  return <AlertCircle className="h-4 w-4 text-amber-500" />;
}

interface GroupedItems {
  overdue: NeedsAttentionItem[];
  stale: NeedsAttentionItem[];
  critical: NeedsAttentionItem[];
  unresolved: NeedsAttentionItem[];
}

function groupItems(items: NeedsAttentionItem[]): GroupedItems {
  return {
    overdue: items.filter((i) => i.reason === "overdue"),
    stale: items.filter((i) => i.reason === "stale"),
    critical: items.filter((i) => i.reason === "critical_risk"),
    unresolved: items.filter((i) => i.reason === "unresolved"),
  };
}

interface Props {
  items: NeedsAttentionItem[];
  onItemClick?: (item: NeedsAttentionItem) => void;
}

export default function NeedsAttention({ items, onItemClick }: Props) {
  if (items.length === 0) return null;

  const groups = groupItems(items);
  const sections = [
    { key: "overdue", label: "Overdue", items: groups.overdue, color: "border-red-200 bg-red-50/40" },
    { key: "stale", label: "Stale", items: groups.stale, color: "border-amber-200 bg-amber-50/40" },
    { key: "critical", label: "Critical Risks", items: groups.critical, color: "border-red-200 bg-red-50/40" },
    { key: "unresolved", label: "Unresolved Threads", items: groups.unresolved, color: "border-amber-200 bg-amber-50/40" },
  ].filter((s) => s.items.length > 0);

  // If no groups (items don't match the predefined reasons), show flat list
  if (sections.length === 0) {
    return (
      <FlatList items={items} onItemClick={onItemClick} />
    );
  }

  return (
    <section>
      <h3 className="text-sm font-semibold text-gray-500 uppercase tracking-wider mb-3 flex items-center gap-1.5">
        <AlertTriangle className="h-3.5 w-3.5 text-amber-500" />
        Needs Attention
        <span className="ml-1 text-gray-400">({items.length})</span>
      </h3>
      <div className="space-y-3">
        {sections.map((section) => (
          <div
            key={section.key}
            className={`rounded-lg border ${section.color} divide-y divide-gray-100/50`}
          >
            <div className="px-4 py-2">
              <span className="text-[10px] font-semibold uppercase tracking-wider text-gray-500">
                {section.label} ({section.items.length})
              </span>
            </div>
            {section.items.map((item) => (
              <AttentionRow
                key={`${item.entity_type}-${item.id}`}
                item={item}
                onClick={onItemClick}
              />
            ))}
          </div>
        ))}
      </div>
    </section>
  );
}

function FlatList({
  items,
  onItemClick,
}: {
  items: NeedsAttentionItem[];
  onItemClick?: (item: NeedsAttentionItem) => void;
}) {
  return (
    <section>
      <h3 className="text-sm font-semibold text-gray-500 uppercase tracking-wider mb-3 flex items-center gap-1.5">
        <AlertTriangle className="h-3.5 w-3.5 text-amber-500" />
        Needs Attention
        <span className="ml-1 text-gray-400">({items.length})</span>
      </h3>
      <div className="rounded-lg border border-amber-200 bg-amber-50/40 divide-y divide-amber-100">
        {items.map((item) => (
          <AttentionRow
            key={`${item.entity_type}-${item.id}`}
            item={item}
            onClick={onItemClick}
          />
        ))}
      </div>
    </section>
  );
}

function AttentionRow({
  item,
  onClick,
}: {
  item: NeedsAttentionItem;
  onClick?: (item: NeedsAttentionItem) => void;
}) {
  return (
    <button
      onClick={() => onClick?.(item)}
      className="flex items-start gap-3 px-4 py-3 w-full text-left hover:bg-white/50 transition-colors"
    >
      <AttentionIcon reason={item.reason} />
      <div className="flex-1 min-w-0">
        <p className="text-base text-gray-900">
          <span className="font-medium">{item.title}</span>
          {item.owner && (
            <span className="text-gray-500"> — {item.owner}</span>
          )}
        </p>
        <div className="flex items-center gap-2 mt-0.5">
          {item.reason === "overdue" && item.days_overdue != null && (
            <span className="text-sm text-red-600 font-medium">
              {item.days_overdue} day{item.days_overdue !== 1 ? "s" : ""} overdue
            </span>
          )}
          {item.reason === "stale" && (
            <span className="text-sm text-amber-600 font-medium">Stale</span>
          )}
          {item.reason === "unresolved" && (
            <span className="text-sm text-amber-600 font-medium">
              Open thread
            </span>
          )}
          {item.project_name && (
            <span className="text-[10px] text-gray-400">
              {item.project_name}
            </span>
          )}
        </div>
      </div>
    </button>
  );
}
