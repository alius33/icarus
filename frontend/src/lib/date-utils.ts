/** Shared date utilities for timeline components */

export function addDays(d: Date, n: number): Date {
  const result = new Date(d);
  result.setDate(result.getDate() + n);
  return result;
}

export function diffDays(a: Date, b: Date): number {
  return Math.round((b.getTime() - a.getTime()) / 86_400_000);
}

export function startOfWeek(d: Date): Date {
  const result = new Date(d);
  const day = result.getDay();
  const diff = day === 0 ? 6 : day - 1; // Monday = start of week
  result.setDate(result.getDate() - diff);
  result.setHours(0, 0, 0, 0);
  return result;
}

export function formatWeekLabel(d: Date): string {
  return d.toLocaleDateString("en-GB", { day: "numeric", month: "short" });
}
