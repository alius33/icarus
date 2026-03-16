"use client";

import { useState, useEffect, useCallback, useRef } from "react";
import { X, MessageSquare, FileText, Loader2 } from "lucide-react";
import { api } from "@/lib/api";
import { useToast } from "@/lib/hooks/useToast";
import { mutate } from "swr";
import type { ProjectBase } from "@/lib/types";

interface QuickUpdateModalProps {
  open: boolean;
  onClose: () => void;
}

// Simple Teams chat detection (mirrors backend logic)
function looksLikeTeamsChat(text: string): boolean {
  const bracketPattern = /^\[\d{1,2}\/\d{1,2}\/\d{4}\s+\d{1,2}:\d{2}/m;
  const inlinePattern = /^.{2,40}\s+\d{1,2}:\d{2}\s*(?:AM|PM)/im;
  let count = 0;
  for (const line of text.split("\n")) {
    if (bracketPattern.test(line.trim()) || inlinePattern.test(line.trim())) {
      count++;
      if (count >= 2) return true;
    }
  }
  return false;
}

export default function QuickUpdateModal({ open, onClose }: QuickUpdateModalProps) {
  const [title, setTitle] = useState("");
  const [content, setContent] = useState("");
  const [selectedProjects, setSelectedProjects] = useState<number[]>([]);
  const [contentType, setContentType] = useState<"note" | "teams_chat">("note");
  const [autoDetected, setAutoDetected] = useState(false);
  const [projects, setProjects] = useState<ProjectBase[]>([]);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const toast = useToast();
  const detectTimer = useRef<ReturnType<typeof setTimeout>>();

  // Fetch projects on mount
  useEffect(() => {
    api.getProjects().then(setProjects).catch(() => {});
  }, []);

  // Auto-detect Teams chat format
  useEffect(() => {
    if (detectTimer.current) clearTimeout(detectTimer.current);
    detectTimer.current = setTimeout(() => {
      if (content.length > 20) {
        const isTeams = looksLikeTeamsChat(content);
        if (isTeams && contentType === "note") {
          setContentType("teams_chat");
          setAutoDetected(true);
        } else if (!isTeams && autoDetected) {
          setContentType("note");
          setAutoDetected(false);
        }
      }
    }, 500);
    return () => {
      if (detectTimer.current) clearTimeout(detectTimer.current);
    };
  }, [content, contentType, autoDetected]);

  const handleKeyDown = useCallback(
    (e: KeyboardEvent) => {
      if (e.key === "Escape") onClose();
    },
    [onClose],
  );

  useEffect(() => {
    if (!open) return;
    document.addEventListener("keydown", handleKeyDown);
    return () => document.removeEventListener("keydown", handleKeyDown);
  }, [open, handleKeyDown]);

  const reset = () => {
    setTitle("");
    setContent("");
    setSelectedProjects([]);
    setContentType("note");
    setAutoDetected(false);
    setError(null);
  };

  const handleClose = () => {
    reset();
    onClose();
  };

  const toggleProject = (id: number) => {
    setSelectedProjects((prev) =>
      prev.includes(id) ? prev.filter((p) => p !== id) : [...prev, id],
    );
  };

  const handleSubmit = async () => {
    if (!title.trim()) {
      setError("Title is required");
      return;
    }
    if (!content.trim()) {
      setError("Content is required");
      return;
    }
    if (selectedProjects.length === 0) {
      setError("Select at least one project");
      return;
    }

    setSaving(true);
    setError(null);
    try {
      await api.createProjectUpdate({
        title: title.trim(),
        content,
        content_type: contentType,
        project_ids: selectedProjects,
      });
      toast.success("Update created");
      // Revalidate SWR caches
      mutate((key: unknown) => {
        if (typeof key === "string") return key.includes("project-update");
        if (Array.isArray(key)) return key[0] === "project-updates" || key[0] === "project-update";
        return false;
      });
      handleClose();
    } catch (e) {
      setError(e instanceof Error ? e.message : "Failed to create update");
    } finally {
      setSaving(false);
    }
  };

  if (!open) return null;

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center"
      role="dialog"
      aria-modal="true"
      aria-labelledby="update-modal-title"
    >
      {/* Backdrop */}
      <div
        className="absolute inset-0 bg-black/40"
        onClick={handleClose}
        aria-hidden="true"
      />
      {/* Modal */}
      <div className="relative bg-white dark:bg-forest-800 rounded-2xl shadow-2xl w-full max-w-2xl mx-2 max-h-[90vh] overflow-y-auto">
        {/* Header */}
        <div className="flex items-center justify-between px-6 py-4 border-b border-forest-200 dark:border-forest-700">
          <h3
            id="update-modal-title"
            className="text-lg font-semibold text-forest-950 dark:text-forest-50"
          >
            Add Project Update
          </h3>
          <button
            onClick={handleClose}
            aria-label="Close dialog"
            className="text-forest-300 hover:text-forest-500 dark:hover:text-forest-200"
          >
            <X className="h-5 w-5" />
          </button>
        </div>

        {/* Body */}
        <div className="px-6 py-4 space-y-4">
          {/* Title */}
          <div>
            <label className="block text-sm font-medium text-forest-700 dark:text-forest-200 mb-1">
              Title
            </label>
            <input
              type="text"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              placeholder="Brief description of this update"
              className="w-full rounded-lg border border-forest-300 dark:border-forest-600 bg-white dark:bg-forest-900 px-3 py-2 text-sm text-forest-900 dark:text-forest-100 placeholder:text-forest-400 focus:outline-none focus:ring-2 focus:ring-forest-500"
            />
          </div>

          {/* Projects multi-select */}
          <div>
            <label className="block text-sm font-medium text-forest-700 dark:text-forest-200 mb-1">
              Projects
            </label>
            <div className="flex flex-wrap gap-2 max-h-32 overflow-y-auto p-2 rounded-lg border border-forest-300 dark:border-forest-600 bg-forest-50 dark:bg-forest-900">
              {projects.map((p) => (
                <button
                  key={p.id}
                  type="button"
                  onClick={() => toggleProject(p.id)}
                  className={`px-3 py-1 rounded-full text-xs font-medium transition-colors ${
                    selectedProjects.includes(p.id)
                      ? "bg-forest-600 text-white"
                      : "bg-forest-200 dark:bg-forest-700 text-forest-700 dark:text-forest-200 hover:bg-forest-300 dark:hover:bg-forest-600"
                  }`}
                >
                  {p.code ? `${p.code} ` : ""}
                  {p.name}
                </button>
              ))}
            </div>
          </div>

          {/* Content type indicator */}
          <div className="flex items-center gap-2">
            <button
              type="button"
              onClick={() => {
                setContentType("note");
                setAutoDetected(false);
              }}
              className={`flex items-center gap-1 px-3 py-1 rounded-full text-xs font-medium transition-colors ${
                contentType === "note"
                  ? "bg-forest-600 text-white"
                  : "bg-forest-200 dark:bg-forest-700 text-forest-600 dark:text-forest-300"
              }`}
            >
              <FileText className="h-3 w-3" /> Note
            </button>
            <button
              type="button"
              onClick={() => {
                setContentType("teams_chat");
                setAutoDetected(false);
              }}
              className={`flex items-center gap-1 px-3 py-1 rounded-full text-xs font-medium transition-colors ${
                contentType === "teams_chat"
                  ? "bg-blue-600 text-white"
                  : "bg-forest-200 dark:bg-forest-700 text-forest-600 dark:text-forest-300"
              }`}
            >
              <MessageSquare className="h-3 w-3" /> Teams Chat
            </button>
            {autoDetected && (
              <span className="text-xs text-blue-600 dark:text-blue-400">
                Auto-detected
              </span>
            )}
          </div>

          {/* Content */}
          <div>
            <label className="block text-sm font-medium text-forest-700 dark:text-forest-200 mb-1">
              Content
            </label>
            <textarea
              value={content}
              onChange={(e) => setContent(e.target.value)}
              placeholder={
                contentType === "teams_chat"
                  ? "Paste Teams chat here..."
                  : "Type your update, observations, or notes..."
              }
              rows={10}
              className={`w-full rounded-lg border border-forest-300 dark:border-forest-600 bg-white dark:bg-forest-900 px-3 py-2 text-sm text-forest-900 dark:text-forest-100 placeholder:text-forest-400 focus:outline-none focus:ring-2 focus:ring-forest-500 resize-y min-h-[200px] ${
                contentType === "teams_chat" ? "font-mono text-xs" : ""
              }`}
            />
            <p className="text-xs text-forest-400 mt-1">
              {content.length.toLocaleString()} characters
            </p>
          </div>

          {/* Error */}
          {error && (
            <p className="text-sm text-red-600 dark:text-red-400">{error}</p>
          )}
        </div>

        {/* Footer */}
        <div className="flex items-center justify-end gap-3 px-6 py-4 border-t border-forest-200 dark:border-forest-700">
          <button
            onClick={handleClose}
            className="px-4 py-2 text-sm font-medium text-forest-600 dark:text-forest-300 hover:text-forest-800 dark:hover:text-forest-100"
          >
            Cancel
          </button>
          <button
            onClick={handleSubmit}
            disabled={saving}
            className="flex items-center gap-2 px-4 py-2 text-sm font-medium text-white bg-forest-600 hover:bg-forest-700 rounded-lg disabled:opacity-50 transition-colors"
          >
            {saving && <Loader2 className="h-4 w-4 animate-spin" />}
            {saving ? "Saving..." : "Save Update"}
          </button>
        </div>
      </div>
    </div>
  );
}
