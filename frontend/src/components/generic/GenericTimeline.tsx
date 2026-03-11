"use client";

import { useMemo, ReactNode } from "react";
import { addDays, diffDays, startOfWeek, formatWeekLabel } from "@/lib/date-utils";

// ── Types ────────────────────────────────────────────────────────────

export interface TimelineItem {
  id: number;
  /** Single date (point marker) or range start */
  startDate: string | null;
  /** Range end date — if null, renders as point marker */
  endDate: string | null;
}

export interface GenericTimelineProps<T> {
  items: T[];
  entityName: string;
  emptyMessage?: string;
  /** Extract timeline dates from an item */
  getDates: (item: T) => { start: string | null; end: string | null };
  /** Render the left label cell for a row */
  renderLabel: (item: T) => ReactNode;
  /** Render the marker/bar on the timeline grid */
  renderMarker: (
    item: T,
    layout: { leftPct: number; widthPct: number; isPoint: boolean }
  ) => ReactNode;
  onItemClick: (item: T) => void;
}

// ── Component ────────────────────────────────────────────────────────

export default function GenericTimeline<T extends { id: number }>({
  items,
  entityName,
  emptyMessage,
  getDates,
  renderLabel,
  renderMarker,
  onItemClick,
}: GenericTimelineProps<T>) {
  const today = useMemo(() => new Date(), []);

  // Filter to items with at least one date
  const datedItems = useMemo(
    () => items.filter((item) => {
      const { start, end } = getDates(item);
      return start || end;
    }),
    [items, getDates]
  );

  // Compute timeline range
  const { startDate, endDate, weeks } = useMemo(() => {
    if (datedItems.length === 0) {
      const s = startOfWeek(today);
      const e = addDays(s, 28);
      return { startDate: s, endDate: e, weeks: 4 };
    }

    let minDate = new Date(today);
    let maxDate = new Date(today);

    datedItems.forEach((item) => {
      const { start, end } = getDates(item);
      if (start) {
        const d = new Date(start);
        if (d < minDate) minDate = d;
        if (d > maxDate) maxDate = d;
      }
      if (end) {
        const d = new Date(end);
        if (d < minDate) minDate = d;
        if (d > maxDate) maxDate = d;
      }
    });

    const s = startOfWeek(addDays(minDate, -7));
    const e = addDays(startOfWeek(maxDate), 14);
    const w = Math.max(4, Math.ceil(diffDays(s, e) / 7));
    return { startDate: s, endDate: e, weeks: w };
  }, [datedItems, today, getDates]);

  const totalDays = diffDays(startDate, endDate);
  const todayOffset = Math.max(0, diffDays(startDate, today));

  // Week labels
  const weekLabels = useMemo(() => {
    const labels: { label: string; offset: number }[] = [];
    for (let i = 0; i < weeks; i++) {
      const d = addDays(startDate, i * 7);
      labels.push({ label: formatWeekLabel(d), offset: i * 7 });
    }
    return labels;
  }, [startDate, weeks]);

  if (datedItems.length === 0) {
    return (
      <div className="flex items-center justify-center py-12 text-gray-400 text-sm">
        {emptyMessage ?? `No ${entityName} with dates to show on timeline.`}
      </div>
    );
  }

  return (
    <div className="border border-gray-200 dark:border-gray-700 rounded-lg overflow-hidden">
      {/* Header: week columns */}
      <div className="flex bg-gray-50 dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700">
        <div className="w-64 shrink-0 px-3 py-2 text-xs font-medium text-gray-500 dark:text-gray-400 border-r border-gray-200 dark:border-gray-700">
          {entityName}
        </div>
        <div className="flex-1 relative">
          <div className="flex" style={{ width: `${weeks * 120}px` }}>
            {weekLabels.map((wl, i) => (
              <div
                key={i}
                className="text-xs text-gray-400 px-2 py-2 border-r border-gray-200 dark:border-gray-700"
                style={{ width: "120px" }}
              >
                {wl.label}
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Rows */}
      <div className="relative overflow-x-auto">
        {datedItems.map((item) => {
          const { start, end } = getDates(item);
          const isPoint = !end || start === end;

          let leftPct: number;
          let widthPct: number;

          if (isPoint) {
            const d = new Date((start || end)!);
            const offset = Math.max(0, diffDays(startDate, d));
            leftPct = (offset / totalDays) * 100;
            widthPct = 0;
          } else {
            const s = start ? new Date(start) : new Date(end!);
            const e = end ? new Date(end) : addDays(new Date(start!), 7);
            const startOff = Math.max(0, diffDays(startDate, s));
            const duration = Math.max(1, diffDays(s, e));
            leftPct = (startOff / totalDays) * 100;
            widthPct = (duration / totalDays) * 100;
          }

          return (
            <div
              key={item.id}
              className="flex border-b border-gray-100 dark:border-gray-800 hover:bg-gray-50 dark:hover:bg-gray-800/30"
            >
              {/* Label */}
              <div
                className="w-64 shrink-0 px-3 py-2 border-r border-gray-200 dark:border-gray-700 cursor-pointer"
                onClick={() => onItemClick(item)}
              >
                {renderLabel(item)}
              </div>

              {/* Timeline area */}
              <div className="flex-1 relative py-1.5" style={{ minWidth: `${weeks * 120}px` }}>
                {/* Week gridlines */}
                {weekLabels.map((_, i) => (
                  <div
                    key={i}
                    className="absolute top-0 bottom-0 border-r border-gray-100 dark:border-gray-800"
                    style={{ left: `${((i * 7) / totalDays) * 100}%` }}
                  />
                ))}

                {/* Today marker */}
                <div
                  className="absolute top-0 bottom-0 w-px bg-red-400 z-10"
                  style={{ left: `${(todayOffset / totalDays) * 100}%` }}
                />

                {/* Item marker/bar */}
                {renderMarker(item, { leftPct, widthPct, isPoint })}
              </div>
            </div>
          );
        })}

        {/* Today line spanning full height */}
        <div
          className="absolute top-0 h-full w-px bg-red-400 z-20 pointer-events-none"
          style={{ left: `calc(256px + ${(todayOffset / totalDays) * 100}%)` }}
        />
      </div>
    </div>
  );
}
