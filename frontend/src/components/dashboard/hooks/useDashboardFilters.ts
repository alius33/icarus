"use client";

import { useCallback } from "react";
import { useSearchParams, useRouter, usePathname } from "next/navigation";
import { useDashboard, useDashboardDispatch } from "../DashboardContext";
import type { TimeFilter, DashboardTab } from "@/lib/types";

export function useDashboardFilters() {
  const state = useDashboard();
  const dispatch = useDashboardDispatch();
  const searchParams = useSearchParams();
  const router = useRouter();
  const pathname = usePathname();

  const updateUrl = useCallback((params: Record<string, string | null>) => {
    const newParams = new URLSearchParams(searchParams.toString());
    Object.entries(params).forEach(([key, value]) => {
      if (value === null) {
        newParams.delete(key);
      } else {
        newParams.set(key, value);
      }
    });
    const qs = newParams.toString();
    router.replace(qs ? `${pathname}?${qs}` : pathname, { scroll: false });
  }, [searchParams, router, pathname]);

  const setTimeFilter = useCallback((value: TimeFilter) => {
    dispatch({ type: "SET_TIME_FILTER", payload: value });
    updateUrl({ time: value === "2w" ? null : value }); // 2w is default, don't show in URL
  }, [dispatch, updateUrl]);

  const setWorkstreamFilter = useCallback((value: string | null) => {
    dispatch({ type: "SET_WORKSTREAM_FILTER", payload: value });
    updateUrl({ ws: value });
  }, [dispatch, updateUrl]);

  const setTab = useCallback((value: DashboardTab) => {
    dispatch({ type: "SET_TAB", payload: value });
    updateUrl({ tab: value === "risks" ? null : value }); // risks is default
  }, [dispatch, updateUrl]);

  // Initialize filters from URL on mount
  const initFromUrl = useCallback(() => {
    const time = searchParams.get("time") as TimeFilter | null;
    const ws = searchParams.get("ws");
    const tab = searchParams.get("tab") as DashboardTab | null;
    if (time) dispatch({ type: "SET_TIME_FILTER", payload: time });
    if (ws) dispatch({ type: "SET_WORKSTREAM_FILTER", payload: ws });
    if (tab) dispatch({ type: "SET_TAB", payload: tab });
  }, [searchParams, dispatch]);

  return {
    filters: state.filters,
    setTimeFilter,
    setWorkstreamFilter,
    setTab,
    initFromUrl,
  };
}
