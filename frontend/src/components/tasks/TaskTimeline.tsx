"use client";

import { useMemo } from "react";
import { TaskTimelineItem, STATUS_CONFIG, PRIORITY_CONFIG, TaskStatus, TaskPriority } from "@/lib/types";

interface TaskTimelineProps {
  tasks: TaskTimelineItem[];
  onTaskClick: (taskId: number) => void;
}

function addDays(date: Date, days: number): Date {
  const d = new Date(date);
  d.setDate(d.getDate() + days);
  return d;
}

function diffDays(a: Date, b: Date): number {
  return Math.round((b.getTime() - a.getTime()) / (1000 * 60 * 60 * 24));
}

function startOfWeek(date: Date): Date {
  const d = new Date(date);
  const day = d.getDay();
  d.setDate(d.getDate() - (day === 0 ? 6 : day - 1));
  d.setHours(0, 0, 0, 0);
  return d;
}

export default function TaskTimeline({ tasks, onTaskClick }: TaskTimelineProps) {
  const today = useMemo(() => new Date(), []);

  // Compute timeline range
  const { startDate, endDate, weeks } = useMemo(() => {
    if (tasks.length === 0) {
      const s = startOfWeek(today);
      const e = addDays(s, 28);
      return { startDate: s, endDate: e, weeks: 4 };
    }

    let minDate = new Date(today);
    let maxDate = new Date(today);

    tasks.forEach((t) => {
      if (t.start_date) {
        const sd = new Date(t.start_date);
        if (sd < minDate) minDate = sd;
      }
      if (t.due_date) {
        const dd = new Date(t.due_date);
        if (dd > maxDate) maxDate = dd;
        if (dd < minDate) minDate = dd;
      }
      if (t.start_date) {
        const sd = new Date(t.start_date);
        if (sd > maxDate) maxDate = sd;
      }
    });

    const s = startOfWeek(addDays(minDate, -7));
    const e = addDays(startOfWeek(maxDate), 14);
    const w = Math.max(4, Math.ceil(diffDays(s, e) / 7));
    return { startDate: s, endDate: e, weeks: w };
  }, [tasks, today]);

  const totalDays = diffDays(startDate, endDate);
  const todayOffset = Math.max(0, diffDays(startDate, today));

  // Week labels
  const weekLabels = useMemo(() => {
    const labels: { label: string; offset: number }[] = [];
    for (let i = 0; i < weeks; i++) {
      const d = addDays(startDate, i * 7);
      labels.push({
        label: d.toLocaleDateString("en-GB", { day: "numeric", month: "short" }),
        offset: i * 7,
      });
    }
    return labels;
  }, [startDate, weeks]);

  if (tasks.length === 0) {
    return (
      <div className="flex items-center justify-center py-12 text-forest-300 text-base">
        No tasks with dates to show on timeline. Add start or due dates to see tasks here.
      </div>
    );
  }

  return (
    <div className="border border-forest-200 dark:border-forest-700 rounded-lg overflow-hidden">
      {/* Header: week columns */}
      <div className="flex bg-forest-50 dark:bg-forest-800 border-b border-forest-200 dark:border-forest-700">
        <div className="w-64 shrink-0 px-3 py-2 text-sm font-medium text-forest-400 dark:text-forest-300 border-r border-forest-200 dark:border-forest-700">
          Task
        </div>
        <div className="flex-1 relative">
          <div className="flex" style={{ width: `${weeks * 120}px` }}>
            {weekLabels.map((wl, i) => (
              <div
                key={i}
                className="text-sm text-forest-300 px-2 py-2 border-r border-forest-200 dark:border-forest-700"
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
        {tasks.map((task) => {
          const taskStart = task.start_date ? new Date(task.start_date) : task.due_date ? new Date(task.due_date) : null;
          const taskEnd = task.due_date ? new Date(task.due_date) : task.start_date ? addDays(new Date(task.start_date), 7) : null;

          if (!taskStart || !taskEnd) return null;

          const startOffset = Math.max(0, diffDays(startDate, taskStart));
          const duration = Math.max(1, diffDays(taskStart, taskEnd));
          const leftPct = (startOffset / totalDays) * 100;
          const widthPct = (duration / totalDays) * 100;

          const statusCfg = STATUS_CONFIG[task.status as TaskStatus];
          const priorityCfg = PRIORITY_CONFIG[task.priority as TaskPriority];
          const barColor = statusCfg?.bgColor ?? "bg-gray-200";
          const textColor = statusCfg?.color ?? "text-forest-500";

          return (
            <div key={task.id} className="flex border-b border-gray-100 dark:border-forest-700 hover:bg-forest-50 dark:hover:bg-forest-700/30">
              {/* Task label */}
              <div
                className="w-64 shrink-0 px-3 py-2 border-r border-forest-200 dark:border-forest-700 cursor-pointer"
                onClick={() => onTaskClick(task.id)}
              >
                <div className="flex items-center gap-2">
                  {priorityCfg && (
                    <span className={`w-2 h-2 rounded-full shrink-0 ${priorityCfg.dotColor}`} />
                  )}
                  <div className="min-w-0">
                    <p className="text-base text-forest-950 dark:text-forest-50 truncate">{task.title}</p>
                    <p className="text-sm text-forest-300">{task.identifier} {task.assignee && `· ${task.assignee}`}</p>
                  </div>
                </div>
              </div>

              {/* Bar area */}
              <div className="flex-1 relative py-1.5" style={{ minWidth: `${weeks * 120}px` }}>
                {/* Week gridlines */}
                {weekLabels.map((_, i) => (
                  <div
                    key={i}
                    className="absolute top-0 bottom-0 border-r border-gray-100 dark:border-forest-700"
                    style={{ left: `${((i * 7) / totalDays) * 100}%` }}
                  />
                ))}

                {/* Today marker */}
                <div
                  className="absolute top-0 bottom-0 w-px bg-red-400 z-10"
                  style={{ left: `${(todayOffset / totalDays) * 100}%` }}
                />

                {/* Task bar */}
                <div
                  className={`absolute h-6 top-1/2 -translate-y-1/2 rounded ${barColor} border ${textColor} cursor-pointer flex items-center px-2`}
                  style={{
                    left: `${leftPct}%`,
                    width: `${Math.max(widthPct, 1)}%`,
                    minWidth: "24px",
                  }}
                  onClick={() => onTaskClick(task.id)}
                  title={`${task.title} (${task.start_date ?? "?"} → ${task.due_date ?? "?"})`}
                >
                  <span className={`text-sm truncate ${textColor} font-medium`}>
                    {task.identifier}
                  </span>
                </div>
              </div>
            </div>
          );
        })}

        {/* Today line in header area */}
        <div
          className="absolute top-0 h-full w-px bg-red-400 z-20 pointer-events-none"
          style={{ left: `calc(256px + ${(todayOffset / totalDays) * 100}%)` }}
        />
      </div>
    </div>
  );
}
