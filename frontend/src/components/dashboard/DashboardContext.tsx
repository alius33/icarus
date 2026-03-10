"use client";

import { createContext, useContext, useReducer, ReactNode, Dispatch } from "react";
import type {
  DashboardDataV2,
  DashboardFilters,
  TimeFilter,
  DashboardTab,
} from "@/lib/types";

// ── State ───────────────────────────────────────────────────────────────────

interface DashboardState {
  data: DashboardDataV2 | null;
  filters: DashboardFilters;
  loading: boolean;
  errors: Record<string, string>;
  modalOpen: string | null; // modal type key or null
  modalData: unknown; // data passed to modal
}

const initialFilters: DashboardFilters = {
  timeFilter: "2w",
  workstreamFilter: null,
  activeTab: "risks",
};

const initialState: DashboardState = {
  data: null,
  filters: initialFilters,
  loading: true,
  errors: {},
  modalOpen: null,
  modalData: null,
};

// ── Actions ─────────────────────────────────────────────────────────────────

type DashboardAction =
  | { type: "SET_DATA"; payload: DashboardDataV2 }
  | { type: "SET_LOADING"; payload: boolean }
  | { type: "SET_ERROR"; payload: { section: string; message: string } }
  | { type: "CLEAR_ERROR"; payload: string }
  | { type: "SET_TIME_FILTER"; payload: TimeFilter }
  | { type: "SET_WORKSTREAM_FILTER"; payload: string | null }
  | { type: "SET_TAB"; payload: DashboardTab }
  | { type: "OPEN_MODAL"; payload: { type: string; data?: unknown } }
  | { type: "CLOSE_MODAL" }
  | { type: "OPTIMISTIC_UPDATE"; payload: { section: string; updater: (data: DashboardDataV2) => DashboardDataV2 } }
  | { type: "REFRESH_SECTION"; payload: { section: string; data: Partial<DashboardDataV2> } };

// ── Reducer ─────────────────────────────────────────────────────────────────

function dashboardReducer(state: DashboardState, action: DashboardAction): DashboardState {
  switch (action.type) {
    case "SET_DATA":
      return { ...state, data: action.payload, loading: false };
    case "SET_LOADING":
      return { ...state, loading: action.payload };
    case "SET_ERROR":
      return { ...state, errors: { ...state.errors, [action.payload.section]: action.payload.message } };
    case "CLEAR_ERROR": {
      const rest = { ...state.errors };
      delete rest[action.payload];
      return { ...state, errors: rest };
    }
    case "SET_TIME_FILTER":
      return { ...state, filters: { ...state.filters, timeFilter: action.payload } };
    case "SET_WORKSTREAM_FILTER":
      return { ...state, filters: { ...state.filters, workstreamFilter: action.payload } };
    case "SET_TAB":
      return { ...state, filters: { ...state.filters, activeTab: action.payload } };
    case "OPEN_MODAL":
      return { ...state, modalOpen: action.payload.type, modalData: action.payload.data ?? null };
    case "CLOSE_MODAL":
      return { ...state, modalOpen: null, modalData: null };
    case "OPTIMISTIC_UPDATE":
      return state.data
        ? { ...state, data: action.payload.updater(state.data) }
        : state;
    case "REFRESH_SECTION":
      return state.data
        ? { ...state, data: { ...state.data, ...action.payload.data } }
        : state;
    default:
      return state;
  }
}

// ── Context ─────────────────────────────────────────────────────────────────

const DashboardContext = createContext<DashboardState>(initialState);
const DashboardDispatchContext = createContext<Dispatch<DashboardAction>>(() => {});

export function DashboardProvider({ children, initialData }: { children: ReactNode; initialData?: DashboardDataV2 }) {
  const [state, dispatch] = useReducer(dashboardReducer, {
    ...initialState,
    data: initialData ?? null,
    loading: !initialData,
  });

  return (
    <DashboardContext.Provider value={state}>
      <DashboardDispatchContext.Provider value={dispatch}>
        {children}
      </DashboardDispatchContext.Provider>
    </DashboardContext.Provider>
  );
}

export function useDashboard() {
  return useContext(DashboardContext);
}

export function useDashboardDispatch() {
  return useContext(DashboardDispatchContext);
}
