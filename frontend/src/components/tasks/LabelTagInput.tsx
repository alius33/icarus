"use client";

import { useState, KeyboardEvent } from "react";
import { X } from "lucide-react";

interface LabelTagInputProps {
  labels: string[];
  onChange: (labels: string[]) => void;
  suggestions?: string[];
  placeholder?: string;
}

export default function LabelTagInput({ labels, onChange, suggestions = [], placeholder = "Add label..." }: LabelTagInputProps) {
  const [input, setInput] = useState("");
  const [showSuggestions, setShowSuggestions] = useState(false);

  const filtered = suggestions.filter(
    (s) => s.toLowerCase().includes(input.toLowerCase()) && !labels.includes(s)
  );

  function addLabel(label: string) {
    const trimmed = label.trim();
    if (trimmed && !labels.includes(trimmed)) {
      onChange([...labels, trimmed]);
    }
    setInput("");
    setShowSuggestions(false);
  }

  function removeLabel(label: string) {
    onChange(labels.filter((l) => l !== label));
  }

  function handleKeyDown(e: KeyboardEvent<HTMLInputElement>) {
    if (e.key === "Enter" && input.trim()) {
      e.preventDefault();
      addLabel(input);
    }
    if (e.key === "Backspace" && !input && labels.length > 0) {
      removeLabel(labels[labels.length - 1]);
    }
  }

  return (
    <div className="relative">
      <div className="flex flex-wrap gap-1.5 border border-gray-300 dark:border-gray-600 rounded-md px-2 py-1.5 bg-white dark:bg-gray-700 focus-within:ring-1 focus-within:ring-blue-500 focus-within:border-blue-500">
        {labels.map((label) => (
          <span
            key={label}
            className="inline-flex items-center gap-1 px-2 py-0.5 text-xs rounded-full bg-blue-100 dark:bg-blue-900/40 text-blue-700 dark:text-blue-300"
          >
            {label}
            <button
              type="button"
              onClick={() => removeLabel(label)}
              className="hover:text-blue-900 dark:hover:text-blue-100"
            >
              <X className="h-3 w-3" />
            </button>
          </span>
        ))}
        <input
          value={input}
          onChange={(e) => {
            setInput(e.target.value);
            setShowSuggestions(true);
          }}
          onKeyDown={handleKeyDown}
          onFocus={() => setShowSuggestions(true)}
          onBlur={() => setTimeout(() => setShowSuggestions(false), 150)}
          placeholder={labels.length === 0 ? placeholder : ""}
          className="flex-1 min-w-[80px] text-sm bg-transparent outline-none text-gray-900 dark:text-gray-100 placeholder-gray-400"
        />
      </div>

      {/* Suggestions dropdown */}
      {showSuggestions && input && filtered.length > 0 && (
        <div className="absolute z-10 mt-1 w-full bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-md shadow-lg max-h-32 overflow-y-auto">
          {filtered.slice(0, 8).map((s) => (
            <button
              key={s}
              type="button"
              onMouseDown={() => addLabel(s)}
              className="w-full text-left px-3 py-1.5 text-sm hover:bg-gray-100 dark:hover:bg-gray-700 text-gray-900 dark:text-gray-100"
            >
              {s}
            </button>
          ))}
        </div>
      )}
    </div>
  );
}
