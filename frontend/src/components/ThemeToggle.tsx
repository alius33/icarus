"use client";

import { Sun, Moon, Monitor } from "lucide-react";
import { useTheme } from "./ThemeProvider";

const themeOrder = ["light", "dark", "system"] as const;

const themeIcons = {
  light: Sun,
  dark: Moon,
  system: Monitor,
} as const;

const themeLabels = {
  light: "Light mode",
  dark: "Dark mode",
  system: "System theme",
} as const;

export default function ThemeToggle() {
  const { theme, setTheme } = useTheme();

  const cycleTheme = () => {
    const currentIndex = themeOrder.indexOf(theme);
    const nextIndex = (currentIndex + 1) % themeOrder.length;
    setTheme(themeOrder[nextIndex]);
  };

  const Icon = themeIcons[theme];

  return (
    <button
      onClick={cycleTheme}
      aria-label={`Current: ${themeLabels[theme]}. Click to switch.`}
      title={themeLabels[theme]}
      className="rounded-md p-1.5 text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-800 hover:text-gray-900 dark:hover:text-white transition-colors"
    >
      <Icon className="h-4 w-4" />
    </button>
  );
}
