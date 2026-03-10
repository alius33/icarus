"use client";

import { useEffect } from "react";
import type { DashboardTab } from "@/lib/types";

interface Options {
  onEscape?: () => void;
  onSearch?: () => void;
  onNew?: () => void;
  onTabSwitch?: (tab: DashboardTab) => void;
  enabled?: boolean;
}

const TAB_MAP: Record<string, DashboardTab> = {
  "1": "risks",
  "2": "resources",
  "3": "activity",
};

export function useKeyboardShortcuts({
  onEscape,
  onSearch,
  onNew,
  onTabSwitch,
  enabled = true,
}: Options) {
  useEffect(() => {
    if (!enabled) return;

    function handleKeyDown(e: KeyboardEvent) {
      // Ignore if typing in an input/textarea/select
      const target = e.target as HTMLElement;
      if (
        target.tagName === "INPUT" ||
        target.tagName === "TEXTAREA" ||
        target.tagName === "SELECT" ||
        target.isContentEditable
      ) {
        // Allow Escape even in inputs
        if (e.key === "Escape" && onEscape) {
          onEscape();
        }
        return;
      }

      switch (e.key) {
        case "Escape":
          onEscape?.();
          break;
        case "/":
          e.preventDefault();
          onSearch?.();
          break;
        case "n":
          onNew?.();
          break;
        case "1":
        case "2":
        case "3":
          if (TAB_MAP[e.key] && onTabSwitch) {
            onTabSwitch(TAB_MAP[e.key]);
          }
          break;
      }
    }

    document.addEventListener("keydown", handleKeyDown);
    return () => document.removeEventListener("keydown", handleKeyDown);
  }, [enabled, onEscape, onSearch, onNew, onTabSwitch]);
}
