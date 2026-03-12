"use client";

import { useState, useCallback, useRef, useEffect } from "react";
import Link from "next/link";
import { Upload, X, FileText, CheckCircle2, AlertCircle, Loader2 } from "lucide-react";
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

export default function UploadPage() {
  const [files, setFiles] = useState<File[]>([]);
  const [assignments, setAssignments] = useState<Record<string, FileProjectAssignment>>({});
  const [projects, setProjects] = useState<ProjectBase[]>([]);
  const [uploading, setUploading] = useState(false);
  const [response, setResponse] = useState<UploadResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [dragActive, setDragActive] = useState(false);
  const inputRef = useRef<HTMLInputElement>(null);

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

  const removeFile = useCallback((name: string) => {
    setFiles((prev) => prev.filter((f) => f.name !== name));
    setAssignments((prev) => {
      const next = { ...prev };
      delete next[name];
      return next;
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

  const handleUpload = async () => {
    if (files.length === 0 || !allHavePrimary) return;
    setUploading(true);
    setError(null);
    setResponse(null);

    try {
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
      setResponse(result);
      setFiles([]);
      setAssignments({});
    } catch (err) {
      setError(err instanceof Error ? err.message : "Upload failed");
    } finally {
      setUploading(false);
    }
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
        <span className="text-xs text-gray-400 w-20 flex-shrink-0">{label}{required && <span className="text-red-400">*</span>}</span>
        <select
          value={value ?? ""}
          onChange={(e) => onChange(e.target.value ? Number(e.target.value) : null)}
          className={`text-xs border rounded-md px-2 py-1.5 bg-gray-900 text-gray-200 focus:border-blue-500 focus:ring-1 focus:ring-blue-500 focus:outline-none flex-1 min-w-[180px] ${
            required && !value
              ? "border-amber-500/50"
              : "border-gray-600"
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
        <p className="mt-1 text-sm text-gray-500">
          Upload <code>.txt</code> transcript files. Filenames should follow the
          pattern{" "}
          <code className="text-xs bg-gray-100 px-1 py-0.5 rounded">
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
        <p className="text-sm font-medium text-gray-700">
          {dragActive
            ? "Drop files here"
            : "Drag & drop transcript files, or click to browse"}
        </p>
        <p className="mt-1 text-xs text-gray-500">
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

      {/* File list with project assignment */}
      {files.length > 0 && (
        <div className="rounded-lg border border-gray-700 bg-gray-800 shadow-sm">
          <div className="flex items-center justify-between border-b border-gray-700 px-4 py-3">
            <h3 className="text-sm font-semibold text-gray-100">
              {files.length} file{files.length !== 1 ? "s" : ""} selected
            </h3>
            <button
              onClick={() => { setFiles([]); setAssignments({}); }}
              className="text-xs text-gray-400 hover:text-gray-200"
            >
              Clear all
            </button>
          </div>
          <ul className="divide-y divide-gray-700">
            {files.map((file) => {
              const a = getAssignment(file.name);
              return (
                <li key={file.name} className="px-4 py-3">
                  <div className="flex items-center gap-3 mb-3">
                    <FileText className="h-4 w-4 flex-shrink-0 text-gray-400" />
                    <div className="min-w-0 flex-1">
                      <span className="text-sm text-gray-200 truncate block">
                        {file.name}
                      </span>
                      <span className="text-xs text-gray-500">
                        {(file.size / 1024).toFixed(0)} KB
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
                </li>
              );
            })}
          </ul>
          <div className="border-t border-gray-700 px-4 py-3 flex items-center gap-3">
            <button
              onClick={handleUpload}
              disabled={uploading || !allHavePrimary}
              className="inline-flex items-center gap-2 rounded-md bg-blue-600 px-4 py-2 text-sm font-medium text-white shadow-sm hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            >
              {uploading ? (
                <>
                  <Loader2 className="h-4 w-4 animate-spin" />
                  Uploading...
                </>
              ) : (
                <>
                  <Upload className="h-4 w-4" />
                  Upload {files.length} file{files.length !== 1 ? "s" : ""}
                </>
              )}
            </button>
            {!allHavePrimary && (
              <span className="text-xs text-amber-400">
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
            <div>
              <p className="text-sm font-medium text-red-800">Upload failed</p>
              <p className="mt-1 text-sm text-red-700">{error}</p>
            </div>
          </div>
        </div>
      )}

      {/* Results */}
      {response && (
        <div className="rounded-lg border border-gray-200 bg-white shadow-sm">
          <div className="border-b border-gray-200 px-4 py-3">
            <h3 className="text-sm font-semibold text-gray-900">
              Upload complete &mdash; {response.uploaded} of {response.total}{" "}
              file{response.total !== 1 ? "s" : ""} processed
            </h3>
          </div>
          <ul className="divide-y divide-gray-100">
            {response.results.map((r) => (
              <li key={r.filename} className="flex items-center gap-3 px-4 py-3">
                {statusIcon(r.status)}
                <div className="min-w-0 flex-1">
                  <p className="text-sm font-medium text-gray-900 truncate">
                    {r.title || r.filename}
                  </p>
                  <p className="text-xs text-gray-500">{r.filename}</p>
                  {r.error && (
                    <p className="text-xs text-red-600 mt-0.5">{r.error}</p>
                  )}
                </div>
                <span
                  className={`inline-flex items-center rounded-full px-2 py-0.5 text-xs font-medium ${
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
                    className="text-xs text-blue-600 hover:text-blue-800 hover:underline flex-shrink-0"
                  >
                    View
                  </Link>
                )}
              </li>
            ))}
          </ul>
          <div className="border-t border-gray-200 px-4 py-3">
            <Link
              href="/transcripts"
              className="text-sm text-blue-600 hover:text-blue-800 hover:underline"
            >
              Go to Transcripts &rarr;
            </Link>
          </div>
        </div>
      )}
    </div>
  );
}
