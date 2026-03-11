/**
 * Board configuration for each entity type.
 *
 * Centralizes the entity-specific differences so generic board components
 * can render decisions, tasks, and threads identically.
 */

import {
  DecisionSchema,
  DecisionBoardResponse,
  DECISION_STATUS_CONFIG,
  TaskSchema,
  TaskBoardResponse,
  STATUS_CONFIG,
  OpenThreadSchema,
  ThreadBoardResponse,
  THREAD_STATUS_CONFIG,
} from "@/lib/types";
import { api } from "@/lib/api";
import { BoardColumn, StatusConfig } from "@/components/generic/GenericBoard";

// ── Helpers ──────────────────────────────────────────────────────────

/** Convert an entity-specific board response to generic BoardColumn format */
function toBoardColumns<T extends { id: number }>(
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  response: { columns: any[]; total: number },
  itemsKey: string,
): BoardColumn<T>[] {
  return response.columns.map((col) => ({
    status: col.status,
    label: col.label,
    color: col.color,
    order: col.order,
    items: (col[itemsKey] || []) as T[],
    count: col.count,
  }));
}

// ── Decision Board Config ────────────────────────────────────────────

export const decisionBoardConfig = {
  entityName: "decisions",
  statusConfig: Object.fromEntries(
    Object.entries(DECISION_STATUS_CONFIG).map(([k, v]) => [k, v as StatusConfig])
  ) as Record<string, StatusConfig>,
  toColumns: (data: DecisionBoardResponse) =>
    toBoardColumns<DecisionSchema>(data, "decisions"),
  updatePosition: async (id: number, status: string, position: number) => {
    await api.updateDecisionPosition(id, { execution_status: status, position });
  },
};

// ── Task Board Config ────────────────────────────────────────────────

export const taskBoardConfig = {
  entityName: "tasks",
  statusConfig: Object.fromEntries(
    Object.entries(STATUS_CONFIG).map(([k, v]) => [k, v as StatusConfig])
  ) as Record<string, StatusConfig>,
  toColumns: (data: TaskBoardResponse) =>
    toBoardColumns<TaskSchema>(data, "tasks"),
  updatePosition: async (id: number, status: string, position: number) => {
    await api.updateTaskPosition(id, { status, position });
  },
};

// ── Thread Board Config ──────────────────────────────────────────────

export const threadBoardConfig = {
  entityName: "threads",
  statusConfig: Object.fromEntries(
    Object.entries(THREAD_STATUS_CONFIG).map(([k, v]) => [k, v as StatusConfig])
  ) as Record<string, StatusConfig>,
  toColumns: (data: ThreadBoardResponse) =>
    toBoardColumns<OpenThreadSchema>(data, "threads"),
  updatePosition: async (id: number, status: string, position: number) => {
    await api.updateOpenThreadPosition(id, { status, position });
  },
};
