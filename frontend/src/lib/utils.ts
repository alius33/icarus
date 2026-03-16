import { clsx, type ClassValue } from "clsx";

export function cn(...inputs: ClassValue[]) {
  return clsx(inputs);
}

export const statusColor: Record<string, string> = {
  LIVE: "bg-green-100 text-green-800 border-green-200",
  ACTIVE: "bg-green-100 text-green-800 border-green-200",
  "LIVE — Stabilising": "bg-green-100 text-green-800 border-green-200",
  "EARLY STAGE": "bg-yellow-100 text-yellow-800 border-yellow-200",
  "PARTIALLY FOLDED INTO WS2": "bg-yellow-100 text-yellow-800 border-yellow-200",
  STALLED: "bg-red-100 text-red-800 border-red-200",
  "MINIMAL PROGRESS": "bg-gray-100 text-gray-600 border-gray-200",
  "ACTIVE — Demo targeting March 21":
    "bg-green-100 text-green-800 border-green-200",
  OPEN: "bg-red-100 text-red-800 border-red-200",
  WATCHING: "bg-yellow-100 text-yellow-800 border-yellow-200",
  CLOSED: "bg-green-100 text-green-800 border-green-200",
  LIKELY_COMPLETED: "bg-blue-100 text-blue-800 border-blue-200",
  COMPLETED: "bg-green-100 text-green-800 border-green-200",
  active: "bg-green-100 text-green-800 border-green-200",
  planning: "bg-blue-100 text-blue-800 border-blue-200",
  paused: "bg-yellow-100 text-yellow-800 border-yellow-200",
  completed: "bg-gray-100 text-gray-600 border-gray-200",
  archived: "bg-gray-100 text-gray-500 border-gray-200",
};

export function getStatusColor(status: string): string {
  return statusColor[status] || "bg-gray-100 text-gray-600 border-gray-200";
}

export function formatDate(dateStr: string): string {
  return new Date(dateStr).toLocaleDateString("en-GB", {
    day: "numeric",
    month: "short",
    year: "numeric",
  });
}

export const tierLabels: Record<number, string> = {
  1: "Decision Makers & Sponsors",
  2: "Influential Gatekeepers",
  3: "Technical & Delivery",
  4: "Adjacent / Emerging",
};

/** RAG dot colour for project status */
export function ragDotColor(status: string): string {
  const s = status.toUpperCase();
  if (["LIVE", "ACTIVE", "COMPLETED"].some((k) => s.includes(k)))
    return "bg-green-500";
  if (["EARLY", "WATCHING", "PLANNING"].some((k) => s.includes(k)))
    return "bg-amber-500";
  if (["STALLED", "MINIMAL"].some((k) => s.includes(k))) return "bg-red-500";
  return "bg-gray-400";
}

/** Severity color for risks/threads */
export function severityColor(severity: string): string {
  const s = severity.toUpperCase();
  if (s === "CRITICAL") return "bg-red-100 text-red-800 border-red-200";
  if (s === "HIGH") return "bg-orange-100 text-orange-800 border-orange-200";
  if (s === "MEDIUM") return "bg-yellow-100 text-yellow-800 border-yellow-200";
  if (s === "LOW") return "bg-green-100 text-green-800 border-green-200";
  return "bg-gray-100 text-gray-600 border-gray-200";
}

/** Capacity status color for resource allocation */
export function capacityColor(status: string): string {
  const s = status.toLowerCase();
  if (s === "available") return "text-green-600";
  if (s === "stretched") return "text-amber-600";
  if (s === "overloaded") return "text-red-600";
  return "text-gray-500";
}

/** Trend arrow for numeric changes */
export function trendArrow(current: number, previous: number): { icon: string; color: string; label: string } {
  if (current > previous) return { icon: "↑", color: "text-green-600", label: "up" };
  if (current < previous) return { icon: "↓", color: "text-red-600", label: "down" };
  return { icon: "→", color: "text-gray-400", label: "flat" };
}

/** Health score to RAG color */
export function healthRagColor(rag: string): string {
  if (rag === "green") return "bg-green-500";
  if (rag === "amber") return "bg-amber-500";
  if (rag === "red") return "bg-red-500";
  return "bg-gray-400";
}

/** Health score to text color */
export function healthRagTextColor(rag: string): string {
  if (rag === "green") return "text-green-700";
  if (rag === "amber") return "text-amber-700";
  if (rag === "red") return "text-red-700";
  return "text-gray-500";
}

/** Task status colors for the PM board */
export const taskStatusColor: Record<string, string> = {
  TODO: "bg-blue-100 text-blue-800 border-blue-200",
  IN_PROGRESS: "bg-yellow-100 text-yellow-800 border-yellow-200",
  IN_REVIEW: "bg-purple-100 text-purple-800 border-purple-200",
  DONE: "bg-green-100 text-green-800 border-green-200",
  CANCELLED: "bg-red-100 text-red-800 border-red-200",
};

export function getTaskStatusColor(status: string): string {
  return taskStatusColor[status] || "bg-gray-100 text-gray-600 border-gray-200";
}

/** Priority dot colors */
export const priorityDotColor: Record<string, string> = {
  URGENT: "bg-red-500",
  HIGH: "bg-orange-500",
  MEDIUM: "bg-yellow-500",
  LOW: "bg-blue-400",
  NONE: "bg-gray-300",
};

export function getPriorityDotColor(priority: string): string {
  return priorityDotColor[priority] || "bg-gray-300";
}

/** Check if a date string is overdue */
export function isOverdue(dateStr: string | null): boolean {
  if (!dateStr) return false;
  return new Date(dateStr) < new Date(new Date().toDateString());
}
