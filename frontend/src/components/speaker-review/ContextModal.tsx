"use client";

import { useEffect, useState } from "react";
import { X } from "lucide-react";
import { cn } from "@/lib/utils";
import { api } from "@/lib/api";
import type { SpeakerReviewItem, TranscriptContext } from "@/lib/types";

interface ContextModalProps {
  item: SpeakerReviewItem;
  onClose: () => void;
}

export default function ContextModal({ item, onClose }: ContextModalProps) {
  const [context, setContext] = useState<TranscriptContext | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;
    setLoading(true);
    setError(null);

    api
      .getSpeakerContext(item.transcript_filename, item.timestamp, item.speaker_label)
      .then((data) => {
        if (!cancelled) setContext(data);
      })
      .catch((e) => {
        if (!cancelled) setError(e.message);
      })
      .finally(() => {
        if (!cancelled) setLoading(false);
      });

    return () => {
      cancelled = true;
    };
  }, [item.transcript_filename, item.timestamp, item.speaker_label]);

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50" onClick={onClose}>
      <div
        className="bg-white dark:bg-forest-800 dark:bg-forest-900 rounded-xl shadow-2xl w-full max-w-2xl max-h-[80vh] flex flex-col"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header */}
        <div className="flex items-center justify-between px-6 py-4 border-b border-forest-200 dark:border-forest-700">
          <div>
            <h3 className="text-lg font-semibold text-forest-950 dark:text-forest-50">
              Transcript Context
            </h3>
            <p className="text-base text-forest-400 dark:text-forest-300 mt-0.5">
              {item.transcript_filename}
              {item.timestamp && <span className="ml-2">@ {item.timestamp}</span>}
            </p>
          </div>
          <button
            onClick={onClose}
            className="p-1.5 rounded-md hover:bg-forest-100 dark:hover:bg-forest-700 text-forest-300 hover:text-forest-500 dark:hover:text-gray-200"
          >
            <X className="h-5 w-5" />
          </button>
        </div>

        {/* Body */}
        <div className="flex-1 overflow-y-auto p-6">
          {loading && (
            <div className="flex items-center justify-center py-8">
              <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-forest-500" />
            </div>
          )}

          {error && (
            <div className="text-red-600 dark:text-red-400 text-base py-4">
              Failed to load context: {error}
            </div>
          )}

          {context && (
            <div className="space-y-1 font-mono text-base">
              {context.lines.map((line, i) => (
                <div
                  key={i}
                  className={cn(
                    "px-3 py-1 rounded",
                    i === context.highlight_line
                      ? "bg-yellow-100 dark:bg-yellow-900/30 border-l-4 border-yellow-500"
                      : "text-forest-500 dark:text-forest-300"
                  )}
                >
                  {line || "\u00A0"}
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Footer info */}
        <div className="px-6 py-3 border-t border-forest-200 dark:border-forest-700 text-sm text-forest-400 dark:text-forest-300 flex gap-4">
          <span>
            <strong>Speaker:</strong> {item.speaker_label}
          </span>
          <span>
            <strong>→</strong> {item.identified_as || "Unidentified"}
          </span>
          <span>
            <strong>Confidence:</strong> {(item.confidence * 100).toFixed(0)}%
          </span>
          <span>
            <strong>Method:</strong> {item.method.replace(/_/g, " ")}
          </span>
        </div>
      </div>
    </div>
  );
}
