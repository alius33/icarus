"use client";

import { useState, useRef, useEffect } from "react";
import { ClipboardCopy, Check, Loader2, ChevronDown } from "lucide-react";

type BriefType = "leadership" | "project" | "stakeholder";

const BRIEF_OPTIONS: { value: BriefType; label: string }[] = [
  { value: "leadership", label: "Leadership Brief" },
  { value: "project", label: "Project Brief" },
  { value: "stakeholder", label: "Stakeholder Brief" },
];

export default function CopyBriefButton() {
  const [state, setState] = useState<"idle" | "loading" | "copied">("idle");
  const [menuOpen, setMenuOpen] = useState(false);
  const menuRef = useRef<HTMLDivElement>(null);

  // Close menu on outside click
  useEffect(() => {
    function handleClick(e: MouseEvent) {
      if (menuRef.current && !menuRef.current.contains(e.target as Node)) {
        setMenuOpen(false);
      }
    }
    document.addEventListener("mousedown", handleClick);
    return () => document.removeEventListener("mousedown", handleClick);
  }, []);

  const handleCopy = async (type: BriefType = "leadership") => {
    setState("loading");
    setMenuOpen(false);
    try {
      const apiBase =
        process.env.NEXT_PUBLIC_API_URL || "";
      const url = type === "leadership"
        ? `${apiBase}/api/dashboard/brief`
        : `${apiBase}/api/dashboard/brief?type=${type}`;
      const res = await fetch(url);
      if (!res.ok) throw new Error("Failed to fetch brief");
      const data = await res.json();
      await navigator.clipboard.writeText(data.text);
      setState("copied");
      setTimeout(() => setState("idle"), 2500);
    } catch {
      setState("idle");
    }
  };

  return (
    <div className="relative" ref={menuRef}>
      <div className="inline-flex rounded-md shadow-sm">
        <button
          onClick={() => handleCopy("leadership")}
          disabled={state === "loading"}
          className="inline-flex items-center gap-1.5 rounded-l-md border border-forest-200 bg-white dark:bg-forest-800 px-3 py-1.5 text-base font-medium text-forest-600 transition-colors hover:bg-forest-50 disabled:opacity-50"
        >
          {state === "loading" && <Loader2 className="h-4 w-4 animate-spin" />}
          {state === "copied" && <Check className="h-4 w-4 text-green-600" />}
          {state === "idle" && <ClipboardCopy className="h-4 w-4" />}
          {state === "copied" ? "Copied!" : "Copy Brief"}
        </button>
        <button
          onClick={() => setMenuOpen(!menuOpen)}
          className="inline-flex items-center rounded-r-md border border-l-0 border-forest-200 bg-white dark:bg-forest-800 px-2 py-1.5 text-forest-400 hover:bg-forest-50"
        >
          <ChevronDown className="h-3.5 w-3.5" />
        </button>
      </div>

      {menuOpen && (
        <div className="absolute right-0 z-10 mt-1 w-44 rounded-md border border-forest-200 bg-white dark:bg-forest-800 shadow-lg">
          {BRIEF_OPTIONS.map((opt) => (
            <button
              key={opt.value}
              onClick={() => handleCopy(opt.value)}
              className="block w-full px-3 py-2 text-left text-base text-forest-600 hover:bg-forest-50 first:rounded-t-md last:rounded-b-md"
            >
              {opt.label}
            </button>
          ))}
        </div>
      )}
    </div>
  );
}
