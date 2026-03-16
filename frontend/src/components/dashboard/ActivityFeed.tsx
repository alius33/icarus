"use client";

import { formatDate } from "@/lib/utils";
import type { ActivityFeedItem as ActivityItem } from "@/lib/types";
import { FileText, Gavel, CheckSquare, AlertCircle } from "lucide-react";

function EntityIcon({ type }: { type: string }) {
  if (type === "transcript") return <FileText className="h-4 w-4 text-forest-500" />;
  if (type === "decision") return <Gavel className="h-4 w-4 text-amber-500" />;
  if (type === "action_item") return <CheckSquare className="h-4 w-4 text-green-500" />;
  if (type === "open_thread") return <AlertCircle className="h-4 w-4 text-red-500" />;
  return <FileText className="h-4 w-4 text-forest-300" />;
}

interface Props {
  items: ActivityItem[];
  onItemClick?: (item: ActivityItem) => void;
}

export default function ActivityFeed({ items, onItemClick }: Props) {
  return (
    <div>
      <h4 className="text-sm font-semibold text-forest-400 uppercase tracking-wider mb-3">
        Recent Activity
      </h4>
      {items.length === 0 ? (
        <p className="text-base text-forest-400">No recent activity.</p>
      ) : (
        <ul className="space-y-2.5">
          {items.map((item, i) => (
            <li key={`${item.entity_type}-${item.id}-${i}`}>
              <button
                onClick={() => onItemClick?.(item)}
                className="flex items-start gap-3 w-full text-left hover:bg-forest-50 rounded-md px-1 py-0.5 -mx-1 transition-colors"
              >
                <EntityIcon type={item.entity_type} />
                <div className="flex-1 min-w-0">
                  <p className="text-base text-forest-950 truncate">{item.title}</p>
                  <div className="flex items-center gap-2 mt-0.5">
                    {item.date && (
                      <span className="text-[10px] text-forest-300">
                        {formatDate(item.date)}
                      </span>
                    )}
                    {item.project_name && (
                      <span className="inline-flex items-center rounded bg-forest-100 px-1.5 py-0.5 text-[10px] font-medium text-forest-500">
                        {item.project_name}
                      </span>
                    )}
                  </div>
                </div>
              </button>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
