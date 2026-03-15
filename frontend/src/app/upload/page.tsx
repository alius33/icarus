"use client";

import { useState, useCallback, useRef, useEffect } from "react";
import Link from "next/link";
import { Upload, X, FileText, CheckCircle2, AlertCircle, Loader2, ChevronDown, ChevronRight, Paperclip } from "lucide-react";
import { api } from "@/lib/api";
import type { ProjectBase } from "@/lib/types";

interface UploadResult {
  status: "inserted" | "updated" | "skipped" | "error";
  id: number | null;
  filename: string;
  title: string | null;
  error?: string;
}

interface UploadResponse {
  uploaded: number;
  total: number;
  results: UploadResult[];
}

interface FileProjectAssignment {
  primary: number | null;
  secondary: number | null;
  tertiary: number | null;
}

const MAX_ATTACHMENT_SIZE = 25 * 1024 * 1024; // 25 MB
const ACCEPTED_ATTACHMENT_EXTS = [".pdf", ".pptx", ".docx"];
const MAX_ATTACHMENTS_PER_TRANSCRIPT = 10;

function validateAttachmentFile(file: File): string | null {
  const ext = "." + (file.name.split(".").pop()?.toLowerCase() || "");
  if (!ACCEPTED_ATTACHMENT_EXTS.includes(ext)) {
    return `${file.name}: only PDF, PPTX, and DOCX files are accepted.`;
  }
  if (file.size > MAX_ATTACHMENT_SIZE) {
    return `${file.name} is too large (${(file.size / (1024 * 1024)).toFixed(1)} MB). Max is 25 MB.`;
  }
  return null;
}

function formatFileSize(bytes: number): string {
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(0)} KB`;
  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
}

export default function UploadPage() {
  const [files, setFiles] = useState<File[]>([]);
  const [assignments, setAssignments] = useState<Record<string, FileProjectAssignment>>({});
  const [projects, setProjects] = useState<ProjectBase[]>([]);
  const [uploading, setUploading] = useState(false);
  const [response, setResponse] = useState<UploadResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [dragActive, setDragActive] = useState(false);
  const inputRef = useRef<HTMLInputElement>(null);

  // Context state (per-file)
  const [notes, setNotes] = useState<Record<string, string>>({});
  const [contextAttachments, setContextAttachments] = useState<Record<string, File[]>>({});
  const [contextExpanded, setContextExpanded] = useState<Record<string, boolean>>({});
  const [uploadPhase, setUploadPhase] = useState<"idle" | "uploading" | "notes" | "attachments">("idle");
  const [contextResults, setContextResults] = useState<Record<string, { notes?: boolean; attachments?: boolean }>>({});

  // Fetch projects on mount
  useEffect(() => {
    api.getProjects().then(setProjects).catch(() => {});
  }, []);

  const getAssignment = (filename: string): FileProjectAssignment =>
    assignments[filename] ?? { primary: null, secondary: null, tertiary: null };

  const setAssignment = (filename: string, field: keyof FileProjectAssignment, value: number | null) => {
    setAssignments((prev) => {
      const current = prev[filename] ?? { primary: null, secondary: null, tertiary: null };
      return {
        ...prev,
        [filename]: { ...current, [field]: value },
      };
    });
  };

  const addFiles = useCallback((newFiles: FileList | File[]) => {
    const txtFiles = Array.from(newFiles).filter((f) =>
      f.name.endsWith(".txt")
    );
    if (txtFiles.length === 0) return;
    setFiles((prev) => {
      const existing = new Set(prev.map((f) => f.name));
      const unique = txtFiles.filter((f) => !existing.has(f.name));
      return [...prev, ...unique];
    });
    setResponse(null);
    setError(null);
  }, []);

  const clearAll = useCallback(() => {
    setFiles([]);
    setAssignments({});
    setNotes({});
    setContextAttachments({});
    setContextExpanded({});
  }, []);

  const removeFile = useCallback((name: string) => {
    setFiles((prev) => prev.filter((f) => f.name !== name));
    setAssignments((prev) => { const next = { ...prev }; delete next[name]; return next; });
    setNotes((prev) => { const next = { ...prev }; delete next[name]; return next; });
    setContextAttachments((prev) => { const next = { ...prev }; delete next[name]; return next; });
    setContextExpanded((prev) => { const next = { ...prev }; delete next[name]; return next; });
  }, []);

  const toggleContext = useCallback((filename: string) => {
    setContextExpanded((prev) => ({ ...prev, [filename]: !prev[filename] }));
  }, []);

  const setNote = useCallback((filename: string, text: string) => {
    setNotes((prev) => ({ ...prev, [filename]: text }));
  }, []);

  const addContextFiles = useCallback((filename: string, newFiles: File[]) => {
    setContextAttachments((prev) => {
      const existing = prev[filename] || [];
      const existingKeys = new Set(existing.map((f) => `${f.name}:${f.size}`));
      const unique = newFiles.filter((f) => !existingKeys.has(`${f.name}:${f.size}`));
      return { ...prev, [filename]: [...existing, ...unique] };
    });
  }, []);

  const removeContextFile = useCallback((filename: string, attIndex: number) => {
    setContextAttachments((prev) => {
      const current = prev[filename] || [];
      return { ...prev, [filename]: current.filter((_, i) => i !== attIndex) };
    });
  }, []);

  const handleDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(true);
  }, []);

  const handleDragLeave = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
  }, []);

  const handleDrop = useCallback(
    (e: React.DragEvent) => {
      e.preventDefault();
      e.stopPropagation();
      setDragActive(false);
      if (e.dataTransfer.files) {
        addFiles(e.dataTransfer.files);
      }
    },
    [addFiles]
  );

  // Check all files have a primary project
  const allHavePrimary = files.every((f) => {
    const a = getAssignment(f.name);
    return a.primary !== null;
  });

  // Tracks transcript IDs from the last upload (for retry)
  const [uploadedIdMap, setUploadedIdMap] = useState<Map<string, number>>(new Map());

  // Retry helper: attempt an async call up to `attempts` times
  const withRetry = async <T,>(fn: () => Promise<T>, attempts = 3, delayMs = 500): Promise<T> => {
    for (let i = 0; i < attempts; i++) {
      try {
        return await fn();
      } catch (err) {
        if (i === attempts - 1) throw err;
        await new Promise((r) => setTimeout(r, delayMs * (i + 1)));
      }
    }
    throw new Error("Retry exhausted");
  };

  const handleUpload = async () => {
    if (files.length === 0 || !allHavePrimary) return;
    setUploading(true);
    setUploadPhase("uploading");
    setError(null);
    setResponse(null);
    setContextResults({});

    try {
      // Phase 1: Upload transcript files
      const primaryIds = files.map((f) => getAssignment(f.name).primary);
      const secondaryIds = files.map((f) => getAssignment(f.name).secondary);
      const tertiaryIds = files.map((f) => getAssignment(f.name).tertiary);
      const hasSecondary = secondaryIds.some((id) => id !== null);
      const hasTertiary = tertiaryIds.some((id) => id !== null);
      const result = await api.uploadTranscripts(
        files,
        primaryIds,
        hasSecondary ? secondaryIds : undefined,
        hasTertiary ? tertiaryIds : undefined,
      );

      // Build filename -> transcript ID map for successful uploads
      const idMap = new Map<string, number>();
      for (const r of result.results) {
        if (r.id && (r.status === "inserted" || r.status === "updated")) {
          idMap.set(r.filename, r.id);
        }
      }
      setUploadedIdMap(idMap);

      // Save context with retry
      const ctxErrors: string[] = [];
      const ctxResults: Record<string, { notes?: boolean; attachments?: boolean }> = {};

      // Phase 2: Save context notes (with retry)
      const filesWithNotes = files.filter(
        (f) => notes[f.name]?.trim() && idMap.has(f.name)
      );
      if (filesWithNotes.length > 0) {
        setUploadPhase("notes");
        for (const f of filesWithNotes) {
          try {
            await withRetry(() =>
              api.updateTranscriptNote(idMap.get(f.name)!, notes[f.name].trim())
            );
            ctxResults[f.name] = { ...ctxResults[f.name], notes: true };
          } catch (err) {
            ctxErrors.push(`Notes for ${f.name}: ${err instanceof Error ? err.message : "failed"}`);
          }
        }
      }

      // Phase 3: Upload attachments (with retry)
      const filesWithAttachments = files.filter(
        (f) => (contextAttachments[f.name]?.length ?? 0) > 0 && idMap.has(f.name)
      );
      if (filesWithAttachments.length > 0) {
        setUploadPhase("attachments");
        for (const f of filesWithAttachments) {
          try {
            await withRetry(() =>
              api.uploadTranscriptAttachments(idMap.get(f.name)!, contextAttachments[f.name])
            );
            ctxResults[f.name] = { ...ctxResults[f.name], attachments: true };
          } catch (err) {
            ctxErrors.push(`Attachments for ${f.name}: ${err instanceof Error ? err.message : "failed"}`);
          }
        }
      }

      setResponse(result);
      setContextResults(ctxResults);

      if (ctxErrors.length > 0) {
        // DO NOT clear form — preserve notes/attachments so user can retry
        setError("Transcripts uploaded, but some context failed:\n" + ctxErrors.join("\n"));
      } else {
        // Only clear when everything succeeded
        clearAll();
        setUploadedIdMap(new Map());
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : "Upload failed");
    } finally {
      setUploading(false);
      setUploadPhase("idle");
    }
  };

  // Retry failed context for already-uploaded transcripts
  const handleRetryContext = async () => {
    if (uploadedIdMap.size === 0) return;
    setUploading(true);
    setError(null);

    const ctxErrors: string[] = [];
    const ctxResults: Record<string, { notes?: boolean; attachments?: boolean }> = { ...contextResults };

    // Retry notes that haven't succeeded yet
    const filesNeedingNotes = files.filter(
      (f) => notes[f.name]?.trim() && uploadedIdMap.has(f.name) && !contextResults[f.name]?.notes
    );
    if (filesNeedingNotes.length > 0) {
      setUploadPhase("notes");
      for (const f of filesNeedingNotes) {
        try {
          await withRetry(() =>
            api.updateTranscriptNote(uploadedIdMap.get(f.name)!, notes[f.name].trim())
          );
          ctxResults[f.name] = { ...ctxResults[f.name], notes: true };
        } catch (err) {
          ctxErrors.push(`Notes for ${f.name}: ${err instanceof Error ? err.message : "failed"}`);
        }
      }
    }

    // Retry attachments that haven't succeeded yet
    const filesNeedingAttachments = files.filter(
      (f) => (contextAttachments[f.name]?.length ?? 0) > 0 && uploadedIdMap.has(f.name) && !contextResults[f.name]?.attachments
    );
    if (filesNeedingAttachments.length > 0) {
      setUploadPhase("attachments");
      for (const f of filesNeedingAttachments) {
        try {
          await withRetry(() =>
            api.uploadTranscriptAttachments(uploadedIdMap.get(f.name)!, contextAttachments[f.name])
          );
          ctxResults[f.name] = { ...ctxResults[f.name], attachments: true };
        } catch (err) {
          ctxErrors.push(`Attachments for ${f.name}: ${err instanceof Error ? err.message : "failed"}`);
        }
      }
    }

    setContextResults(ctxResults);

    if (ctxErrors.length > 0) {
      setError("Some context still failed:\n" + ctxErrors.join("\n"));
    } else {
      setError(null);
      clearAll();
      setUploadedIdMap(new Map());
    }

    setUploading(false);
    setUploadPhase("idle");
  };

  const statusIcon = (status: string) => {
    switch (status) {
      case "inserted":
        return <CheckCircle2 className="h-4 w-4 text-green-600" />;
      case "updated":
        return <CheckCircle2 className="h-4 w-4 text-blue-600" />;
      case "skipped":
        return <CheckCircle2 className="h-4 w-4 text-gray-400" />;
      case "error":
        return <AlertCircle className="h-4 w-4 text-red-600" />;
      default:
        return null;
    }
  };

  const statusLabel = (status: string) => {
    switch (status) {
      case "inserted":
        return "New";
      case "updated":
        return "Updated";
      case "skipped":
        return "Unchanged";
      case "error":
        return "Error";
      default:
        return status;
    }
  };

  const sortedProjects = [...projects].sort((a, b) => a.name.localeCompare(b.name));

  const ProjectSelect = ({
    value,
    onChange,
    label,
    required,
    excludeIds,
  }: {
    value: number | null;
    onChange: (v: number | null) => void;
    label: string;
    required?: boolean;
    excludeIds?: (number | null)[];
  }) => {
    const filtered = excludeIds
      ? sortedProjects.filter((p) => !excludeIds.includes(p.id))
      : sortedProjects;
    return (
      <div className="flex items-center gap-2">
        <span className="text-sm text-gray-400 w-20 flex-shrink-0">{label}{required && <span className="text-red-400">*</span>}</span>
        <select
          value={value ?? ""}
          onChange={(e) => onChange(e.target.value ? Number(e.target.value) : null)}
          className={`text-sm border rounded-md px-2 py-1.5 bg-gray-900 text-gray-700 dark:text-gray-200 focus:border-blue-500 focus:ring-1 focus:ring-blue-500 focus:outline-none flex-1 min-w-[180px] ${
            required && !value
              ? "border-amber-500/50"
              : "border-gray-300 dark:border-gray-600"
          }`}
        >
          <option value="">{required ? "Select project..." : "None"}</option>
          {filtered.map((p) => (
            <option key={p.id} value={p.id}>
              {p.name}
            </option>
          ))}
        </select>
      </div>
    );
  };

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold text-gray-900">
          Upload Transcripts
        </h2>
        <p className="mt-1 text-base text-gray-500">
          Upload <code>.txt</code> transcript files. Filenames should follow the
          pattern{" "}
          <code className="text-sm bg-gray-100 px-1 py-0.5 rounded">
            YYYY-MM-DD_-_Title.txt
          </code>{" "}
          for automatic date and title extraction.
        </p>
      </div>

      {/* Drop zone */}
      <div
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        onClick={() => inputRef.current?.click()}
        className={`relative flex flex-col items-center justify-center rounded-lg border-2 border-dashed p-12 text-center cursor-pointer transition-colors ${
          dragActive
            ? "border-blue-500 bg-blue-50"
            : "border-gray-300 bg-gray-50 hover:border-gray-400 hover:bg-gray-100"
        }`}
      >
        <Upload
          className={`h-10 w-10 mb-3 ${
            dragActive ? "text-blue-500" : "text-gray-400"
          }`}
        />
        <p className="text-base font-medium text-gray-700">
          {dragActive
            ? "Drop files here"
            : "Drag & drop transcript files, or click to browse"}
        </p>
        <p className="mt-1 text-sm text-gray-500">
          Accepts .txt files up to 10 MB each
        </p>
        <input
          ref={inputRef}
          type="file"
          accept=".txt"
          multiple
          className="hidden"
          onChange={(e) => {
            if (e.target.files) addFiles(e.target.files);
            e.target.value = "";
          }}
        />
      </div>

      {/* File list with project assignment + context */}
      {files.length > 0 && (
        <div className="rounded-lg border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 shadow-sm">
          <div className="flex items-center justify-between border-b border-gray-200 dark:border-gray-700 px-4 py-3">
            <h3 className="text-base font-semibold text-gray-800 dark:text-gray-100">
              {files.length} file{files.length !== 1 ? "s" : ""} selected
            </h3>
            <button
              onClick={clearAll}
              className="text-sm text-gray-400 hover:text-gray-200"
            >
              Clear all
            </button>
          </div>
          <ul className="divide-y divide-gray-200 dark:divide-gray-700">
            {files.map((file) => {
              const a = getAssignment(file.name);
              const isExpanded = contextExpanded[file.name] ?? false;
              const noteText = notes[file.name] || "";
              const atts = contextAttachments[file.name] || [];
              const hasContext = noteText.trim().length > 0 || atts.length > 0;

              return (
                <li key={file.name} className="px-4 py-3">
                  <div className="flex items-center gap-3 mb-3">
                    <FileText className="h-4 w-4 flex-shrink-0 text-gray-400" />
                    <div className="min-w-0 flex-1">
                      <span className="text-base text-gray-700 dark:text-gray-200 truncate block">
                        {file.name}
                      </span>
                      <span className="text-sm text-gray-500">
                        {formatFileSize(file.size)}
                      </span>
                    </div>
                    <button
                      onClick={() => removeFile(file.name)}
                      className="text-gray-500 hover:text-red-400"
                    >
                      <X className="h-4 w-4" />
                    </button>
                  </div>
                  <div className="ml-7 space-y-2">
                    <ProjectSelect
                      value={a.primary}
                      onChange={(v) => setAssignment(file.name, "primary", v)}
                      label="Primary"
                      required
                      excludeIds={[a.secondary, a.tertiary]}
                    />
                    <ProjectSelect
                      value={a.secondary}
                      onChange={(v) => setAssignment(file.name, "secondary", v)}
                      label="Secondary"
                      excludeIds={[a.primary, a.tertiary]}
                    />
                    <ProjectSelect
                      value={a.tertiary}
                      onChange={(v) => setAssignment(file.name, "tertiary", v)}
                      label="Third"
                      excludeIds={[a.primary, a.secondary]}
                    />
                  </div>

                  {/* Context toggle */}
                  <div className="ml-7 mt-2">
                    <button
                      onClick={() => toggleContext(file.name)}
                      className="inline-flex items-center gap-1.5 text-sm text-gray-400 hover:text-gray-200 transition-colors"
                    >
                      {isExpanded ? (
                        <ChevronDown className="h-3.5 w-3.5" />
                      ) : (
                        <ChevronRight className="h-3.5 w-3.5" />
                      )}
                      <Paperclip className="h-3 w-3" />
                      Add context
                      {!isExpanded && hasContext && (
                        <span className="text-blue-400 ml-1">
                          {[
                            noteText.trim() ? "notes" : null,
                            atts.length > 0 ? `${atts.length} file${atts.length !== 1 ? "s" : ""}` : null,
                          ].filter(Boolean).join(" + ")}
                        </span>
                      )}
                    </button>

                    {isExpanded && (
                      <div className="mt-2 space-y-3 pl-3 border-l-2 border-gray-200 dark:border-gray-700 ml-1">
                        {/* Notes textarea */}
                        <div>
                          <label className="text-sm text-gray-400 block mb-1">
                            Context notes
                          </label>
                          <textarea
                            value={noteText}
                            onChange={(e) => setNote(file.name, e.target.value)}
                            rows={3}
                            placeholder="Meeting agenda, key topics to watch, pre-read notes..."
                            className="w-full rounded-md border border-gray-300 dark:border-gray-600 bg-gray-900 px-3 py-2 text-base text-gray-700 dark:text-gray-200 placeholder:text-gray-500 focus:border-blue-500 focus:ring-1 focus:ring-blue-500 focus:outline-none resize-y"
                          />
                        </div>

                        {/* Attachment picker */}
                        <div>
                          <label className="text-sm text-gray-400 block mb-1">
                            Supporting documents
                            <span className="text-gray-500 ml-1">(PDF, PPTX, DOCX, max 25 MB)</span>
                          </label>
                          <div className="flex items-center gap-2 mb-2">
                            <button
                              onClick={() => {
                                const input = document.createElement("input");
                                input.type = "file";
                                input.accept = ".pdf,.pptx,.docx";
                                input.multiple = true;
                                input.onchange = () => {
                                  if (!input.files) return;
                                  const fileArray = Array.from(input.files);
                                  for (const f of fileArray) {
                                    const validationError = validateAttachmentFile(f);
                                    if (validationError) {
                                      setError(validationError);
                                      return;
                                    }
                                  }
                                  const currentCount = atts.length;
                                  if (currentCount + fileArray.length > MAX_ATTACHMENTS_PER_TRANSCRIPT) {
                                    setError(`Maximum ${MAX_ATTACHMENTS_PER_TRANSCRIPT} attachments per transcript.`);
                                    return;
                                  }
                                  setError(null);
                                  addContextFiles(file.name, fileArray);
                                };
                                input.click();
                              }}
                              disabled={atts.length >= MAX_ATTACHMENTS_PER_TRANSCRIPT}
                              className="inline-flex items-center gap-1 rounded-md border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 px-2.5 py-1.5 text-sm text-gray-600 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 hover:text-gray-100 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                            >
                              <Paperclip className="h-3 w-3" />
                              Choose files
                            </button>
                            <span className="text-sm text-gray-500">
                              {atts.length}/{MAX_ATTACHMENTS_PER_TRANSCRIPT}
                            </span>
                          </div>

                          {atts.length > 0 && (
                            <ul className="space-y-1">
                              {atts.map((att, attIdx) => (
                                <li
                                  key={`${att.name}-${att.size}-${attIdx}`}
                                  className="flex items-center gap-2 text-sm text-gray-600 dark:text-gray-300 bg-gray-50 dark:bg-gray-800/50 rounded px-2 py-1.5"
                                >
                                  <FileText
                                    className={`h-3 w-3 flex-shrink-0 ${
                                      att.name.endsWith(".pdf")
                                        ? "text-red-500"
                                        : att.name.endsWith(".pptx")
                                        ? "text-orange-500"
                                        : "text-blue-500"
                                    }`}
                                  />
                                  <span className="truncate flex-1">{att.name}</span>
                                  <span className="text-gray-500 flex-shrink-0">
                                    {formatFileSize(att.size)}
                                  </span>
                                  <button
                                    onClick={() => removeContextFile(file.name, attIdx)}
                                    className="text-gray-500 hover:text-red-400 flex-shrink-0"
                                  >
                                    <X className="h-3 w-3" />
                                  </button>
                                </li>
                              ))}
                            </ul>
                          )}
                        </div>
                      </div>
                    )}
                  </div>
                </li>
              );
            })}
          </ul>
          <div className="border-t border-gray-200 dark:border-gray-700 px-4 py-3 flex items-center gap-3">
            <button
              onClick={handleUpload}
              disabled={uploading || !allHavePrimary}
              className="inline-flex items-center gap-2 rounded-md bg-blue-600 px-4 py-2 text-base font-medium text-white shadow-sm hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            >
              {uploading ? (
                <>
                  <Loader2 className="h-4 w-4 animate-spin" />
                  {uploadPhase === "uploading" && "Uploading transcripts..."}
                  {uploadPhase === "notes" && "Saving notes..."}
                  {uploadPhase === "attachments" && "Uploading attachments..."}
                </>
              ) : (
                <>
                  <Upload className="h-4 w-4" />
                  Upload {files.length} file{files.length !== 1 ? "s" : ""}
                </>
              )}
            </button>
            {!allHavePrimary && (
              <span className="text-sm text-amber-400">
                All files need a primary project assigned
              </span>
            )}
          </div>
        </div>
      )}

      {/* Error */}
      {error && (
        <div className="rounded-lg border border-red-200 bg-red-50 p-4">
          <div className="flex items-start gap-2">
            <AlertCircle className="h-5 w-5 text-red-600 flex-shrink-0 mt-0.5" />
            <div className="flex-1">
              <p className="text-base font-medium text-red-800">
                {uploadedIdMap.size > 0 ? "Context save failed" : "Upload failed"}
              </p>
              <p className="mt-1 text-base text-red-700 whitespace-pre-line">{error}</p>
              {uploadedIdMap.size > 0 && (
                <button
                  onClick={handleRetryContext}
                  disabled={uploading}
                  className="mt-2 inline-flex items-center gap-2 rounded-md bg-red-600 px-3 py-1.5 text-base font-medium text-white hover:bg-red-700 disabled:opacity-50 transition-colors"
                >
                  {uploading ? (
                    <><Loader2 className="h-3.5 w-3.5 animate-spin" /> Retrying...</>
                  ) : (
                    "Retry failed context"
                  )}
                </button>
              )}
            </div>
          </div>
        </div>
      )}

      {/* Results */}
      {response && (
        <div className="rounded-lg border border-gray-200 bg-white shadow-sm">
          <div className="border-b border-gray-200 px-4 py-3">
            <h3 className="text-base font-semibold text-gray-900">
              Upload complete &mdash; {response.uploaded} of {response.total}{" "}
              file{response.total !== 1 ? "s" : ""} processed
            </h3>
          </div>
          <ul className="divide-y divide-gray-100">
            {response.results.map((r) => {
              const ctx = contextResults[r.filename];
              return (
                <li key={r.filename} className="flex items-center gap-3 px-4 py-3">
                  {statusIcon(r.status)}
                  <div className="min-w-0 flex-1">
                    <p className="text-base font-medium text-gray-900 truncate">
                      {r.title || r.filename}
                    </p>
                    <div className="flex items-center gap-2">
                      <p className="text-sm text-gray-500">{r.filename}</p>
                      {ctx?.notes && (
                        <span className="inline-flex items-center rounded-full bg-purple-50 px-1.5 py-0.5 text-[10px] font-medium text-purple-700">
                          notes
                        </span>
                      )}
                      {ctx?.attachments && (
                        <span className="inline-flex items-center rounded-full bg-indigo-50 px-1.5 py-0.5 text-[10px] font-medium text-indigo-700">
                          attachments
                        </span>
                      )}
                    </div>
                    {r.error && (
                      <p className="text-sm text-red-600 mt-0.5">{r.error}</p>
                    )}
                  </div>
                  <span
                    className={`inline-flex items-center rounded-full px-2 py-0.5 text-sm font-medium ${
                      r.status === "inserted"
                        ? "bg-green-50 text-green-700"
                        : r.status === "updated"
                        ? "bg-blue-50 text-blue-700"
                        : r.status === "skipped"
                        ? "bg-gray-100 text-gray-600"
                        : "bg-red-50 text-red-700"
                    }`}
                  >
                    {statusLabel(r.status)}
                  </span>
                  {r.id && (
                    <Link
                      href={`/transcripts/${r.id}`}
                      className="text-sm text-blue-600 hover:text-blue-800 hover:underline flex-shrink-0"
                    >
                      View
                    </Link>
                  )}
                </li>
              );
            })}
          </ul>
          <div className="border-t border-gray-200 px-4 py-3">
            <Link
              href="/transcripts"
              className="text-base text-blue-600 hover:text-blue-800 hover:underline"
            >
              Go to Transcripts &rarr;
            </Link>
          </div>
        </div>
      )}
    </div>
  );
}
