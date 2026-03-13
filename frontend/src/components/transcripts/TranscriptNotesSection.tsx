"use client";

import { useState, useCallback } from "react";
import { Pencil, History, Save, X, ChevronDown, ChevronRight } from "lucide-react";
import { api } from "@/lib/api";
import { useTranscriptNotes } from "@/lib/swr";
import { formatDate } from "@/lib/utils";
import type { TranscriptNoteBase } from "@/lib/types";

interface TranscriptNotesSectionProps {
  transcriptId: number;
}

export default function TranscriptNotesSection({ transcriptId }: TranscriptNotesSectionProps) {
  const { data: note, mutate } = useTranscriptNotes(transcriptId);
  const [mode, setMode] = useState<"view" | "edit" | "history">("view");
  const [editContent, setEditContent] = useState("");
  const [saving, setSaving] = useState(false);
  const [history, setHistory] = useState<TranscriptNoteBase[]>([]);
  const [historyLoading, setHistoryLoading] = useState(false);
  const [expandedVersions, setExpandedVersions] = useState<Set<number>>(new Set());

  const startEdit = useCallback(() => {
    setEditContent(note?.content || "");
    setMode("edit");
  }, [note]);

  const cancelEdit = useCallback(() => {
    setMode("view");
    setEditContent("");
  }, []);

  const saveNote = useCallback(async () => {
    if (!editContent.trim()) return;
    setSaving(true);
    try {
      await api.updateTranscriptNote(transcriptId, editContent.trim());
      await mutate();
      setMode("view");
      setEditContent("");
    } catch (err) {
      console.error("Failed to save note:", err);
    } finally {
      setSaving(false);
    }
  }, [transcriptId, editContent, mutate]);

  const loadHistory = useCallback(async () => {
    if (mode === "history") {
      setMode("view");
      return;
    }
    setHistoryLoading(true);
    try {
      const data = await api.getTranscriptNoteHistory(transcriptId);
      setHistory(data.versions);
      setMode("history");
    } catch (err) {
      console.error("Failed to load history:", err);
    } finally {
      setHistoryLoading(false);
    }
  }, [transcriptId, mode]);

  const toggleVersion = (version: number) => {
    setExpandedVersions((prev) => {
      const next = new Set(prev);
      if (next.has(version)) next.delete(version);
      else next.add(version);
      return next;
    });
  };

  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-2">
          <h3 className="text-lg font-semibold text-gray-900">Analyst Notes</h3>
          {note && (
            <span className="text-xs text-gray-400 bg-gray-100 px-2 py-0.5 rounded-full">
              v{note.version}
            </span>
          )}
        </div>
        <div className="flex items-center gap-2">
          {note && note.version_count > 1 && (
            <button
              onClick={loadHistory}
              disabled={historyLoading}
              className="inline-flex items-center gap-1 text-xs text-gray-500 hover:text-gray-700 transition-colors"
            >
              <History className="h-3.5 w-3.5" />
              {mode === "history" ? "Hide" : `${note.version_count} versions`}
            </button>
          )}
          {mode === "view" && (
            <button
              onClick={startEdit}
              className="inline-flex items-center gap-1 text-xs text-blue-600 hover:text-blue-800 transition-colors"
            >
              <Pencil className="h-3.5 w-3.5" />
              {note ? "Edit" : "Add notes"}
            </button>
          )}
        </div>
      </div>

      {mode === "view" && (
        <>
          {note ? (
            <div className="prose prose-sm max-w-none text-gray-700 whitespace-pre-wrap">
              {note.content}
            </div>
          ) : (
            <p className="text-sm text-gray-400 italic">
              Add notes to provide context for analysis (meeting agendas, key topics, pre-reads).
            </p>
          )}
        </>
      )}

      {mode === "edit" && (
        <div className="space-y-3">
          <textarea
            value={editContent}
            onChange={(e) => setEditContent(e.target.value)}
            rows={8}
            placeholder="Add context for this transcript... (meeting agenda, key topics to watch, pre-read notes)"
            className="w-full rounded-md border border-gray-300 px-3 py-2 text-sm text-gray-900 placeholder:text-gray-400 focus:border-blue-500 focus:ring-1 focus:ring-blue-500 focus:outline-none resize-y"
            autoFocus
          />
          <div className="flex items-center gap-2">
            <button
              onClick={saveNote}
              disabled={saving || !editContent.trim()}
              className="inline-flex items-center gap-1.5 rounded-md bg-blue-600 px-3 py-1.5 text-xs font-medium text-white hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            >
              <Save className="h-3.5 w-3.5" />
              {saving ? "Saving..." : "Save"}
            </button>
            <button
              onClick={cancelEdit}
              className="inline-flex items-center gap-1.5 rounded-md border border-gray-300 px-3 py-1.5 text-xs font-medium text-gray-600 hover:bg-gray-50 transition-colors"
            >
              <X className="h-3.5 w-3.5" />
              Cancel
            </button>
          </div>
        </div>
      )}

      {mode === "history" && (
        <div className="space-y-2">
          {history.map((v) => (
            <div key={v.id} className="border border-gray-100 rounded-md">
              <button
                onClick={() => toggleVersion(v.version)}
                className="w-full flex items-center gap-2 px-3 py-2 text-left hover:bg-gray-50 transition-colors"
              >
                {expandedVersions.has(v.version) ? (
                  <ChevronDown className="h-3.5 w-3.5 text-gray-400 flex-shrink-0" />
                ) : (
                  <ChevronRight className="h-3.5 w-3.5 text-gray-400 flex-shrink-0" />
                )}
                <span className="text-xs font-medium text-gray-700">
                  Version {v.version}
                </span>
                <span className="text-xs text-gray-400">
                  {v.created_at ? formatDate(v.created_at) : ""}
                </span>
                {v.version === note?.version && (
                  <span className="text-xs bg-blue-100 text-blue-700 px-1.5 py-0.5 rounded-full">
                    current
                  </span>
                )}
              </button>
              {expandedVersions.has(v.version) && (
                <div className="px-3 pb-3 text-sm text-gray-600 whitespace-pre-wrap border-t border-gray-100 pt-2">
                  {v.content}
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
