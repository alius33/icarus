"use client";

import { useCallback } from "react";
import { api } from "@/lib/api";
import { useDashboard, useDashboardDispatch } from "../DashboardContext";
import type { DashboardDataV2 } from "@/lib/types";

export function useDashboardData() {
  const state = useDashboard();
  const dispatch = useDashboardDispatch();

  const fetchAll = useCallback(async () => {
    dispatch({ type: "SET_LOADING", payload: true });
    try {
      const data = await api.getDashboard() as DashboardDataV2;
      dispatch({ type: "SET_DATA", payload: data });
    } catch (e) {
      dispatch({
        type: "SET_ERROR",
        payload: { section: "dashboard", message: e instanceof Error ? e.message : "Failed to load" },
      });
      dispatch({ type: "SET_LOADING", payload: false });
    }
  }, [dispatch]);

  const refreshSection = useCallback(async (section: string) => {
    try {
      dispatch({ type: "CLEAR_ERROR", payload: section });
      // For now, refresh all data - targeted refresh can be added per-section later
      const data = await api.getDashboard() as DashboardDataV2;
      dispatch({ type: "SET_DATA", payload: data });
    } catch (e) {
      dispatch({
        type: "SET_ERROR",
        payload: { section, message: e instanceof Error ? e.message : "Failed to refresh" },
      });
    }
  }, [dispatch]);

  return { data: state.data, loading: state.loading, errors: state.errors, fetchAll, refreshSection };
}
