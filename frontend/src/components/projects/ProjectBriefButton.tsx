"use client";

import { useState } from "react";
import { ClipboardCopy, Check } from "lucide-react";
import type { ProjectBase, ActionItemSchema, ProjectWeeklyTimeline } from "@/lib/types";

interface Props {
  project: ProjectBase;
  actions: ActionItemSchema[];
  timeline: ProjectWeeklyTimeline;
}

function generateBrief(project: ProjectBase, actions: ActionItemSchema[], timeline: ProjectWeeklyTimeline): string {
  const openActions = actions.filter(
    (a) => a.status.toLowerCase() === "open" || a.status.toLowerCase() === "in progress"
  );

  // Find the most recent weekly report content for executive summary
  let execSummary = "";
  let weekLabel = "";
  for (const week of timeline.weeks) {
    if (week.weekly_report_content) {
      weekLabel = week.week_label;
      // Extract executive summary section
      const lines = week.weekly_report_content.split("\n");
      let capturing = false;
      const summaryLines: string[] = [];
      for (const line of lines) {
        const h2Match = line.match(/^## (.+)/);
        if (h2Match) {
          const heading = h2Match[1].trim().toLowerCase();
          if (heading.includes("executive summary")) {
            capturing = true;
            continue;
          } else if (capturing) {
            break;
          }
        }
        if (capturing && line.trim()) {
          // Strip markdown formatting for plain text
          summaryLines.push(line.replace(/[*_#`]/g, "").trim());
        }
      }
      execSummary = summaryLines.join(" ").slice(0, 500);
      break;
    }
  }

  const parts: string[] = [];
  parts.push(`${project.name} — Status Update`);
  parts.push(`Status: ${project.status}`);
  if (weekLabel) parts.push(`As of: ${weekLabel}`);
  parts.push("");

  if (execSummary) {
    parts.push(execSummary);
    parts.push("");
  }

  parts.push(`Open Actions: ${openActions.length}`);
  if (openActions.length > 0) {
    openActions.forEach((a) => {
      const owner = a.owner ? ` (${a.owner})` : "";
      const due = a.due_date ? ` — due ${a.due_date}` : "";
      parts.push(`  - ${a.description || a.title}${owner}${due}`);
    });
    parts.push("");
  }

  parts.push(`Key Numbers: ${project.decision_count} decisions, ${project.action_count} total actions, ${project.open_thread_count} open threads`);

  return parts.join("\n");
}

export default function ProjectBriefButton({ project, actions, timeline }: Props) {
  const [state, setState] = useState<"idle" | "copied">("idle");

  const handleCopy = async () => {
    const text = generateBrief(project, actions, timeline);
    await navigator.clipboard.writeText(text);
    setState("copied");
    setTimeout(() => setState("idle"), 2500);
  };

  return (
    <button
      onClick={handleCopy}
      className="inline-flex items-center gap-1.5 rounded-md border border-forest-200 bg-white dark:bg-forest-800 px-3 py-1.5 text-base font-medium text-forest-600 shadow-sm transition-colors hover:bg-forest-50"
    >
      {state === "copied" ? (
        <Check className="h-4 w-4 text-green-600" />
      ) : (
        <ClipboardCopy className="h-4 w-4" />
      )}
      {state === "copied" ? "Copied!" : "Copy Brief"}
    </button>
  );
}
