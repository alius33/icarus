"use client";

import { useState, useCallback, useRef, useEffect } from "react";
import { Upload, Trash2, Download, FileText, ChevronDown, ChevronRight, Loader2, AlertCircle } from "lucide-react";
import { api } from "@/lib/api";
import { useTranscriptAttachments } from "@/lib/swr";
import { formatDate } from "@/lib/utils";

interface TranscriptAttachmentsSectionProps {
  transcriptId: number;
}

const FILE_TYPE_ICONS: Record<string, string> = {
  pdf: "text-red-500",
  pptx: "text-orange-500",
  docx: "text-blue-500",
};

const MAX_FILE_SIZE = 25 * 1024 * 1024; // 25 MB
const ACCEPTED_TYPES = ".pdf,.pptx,.docx";

function formatSize(bytes: number): string {
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(0)} KB`;
  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
}

export default function TranscriptAttachmentsSection({ transcriptId }: TranscriptAttachmentsSectionProps) {
  const { data: attachments, mutate } = useTranscriptAttachments(transcriptId);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [expandedText, setExpandedText] = useState<Set<number>>(new Set());
  const [confirmDelete, setConfirmDelete] = useState<number | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleUpload = useCallback(async (files: FileList | File[]) => {
    const fileArray = Array.from(files);

    // Client-side validation
    for (const f of fileArray) {
      if (f.size > MAX_FILE_SIZE) {
        setError(`${f.name} is too large (${formatSize(f.size)}). Max is 25 MB.`);
        return;
      }
      const ext = f.name.split(".").pop()?.toLowerCase();
      if (!["pdf", "pptx", "docx"].includes(ext || "")) {
        setError(`${f.name}: only PDF, PPTX, and DOCX files are accepted.`);
        return;
      }
    }

    if ((attachments?.length || 0) + fileArray.length > 10) {
      setError("Maximum 10 attachments per transcript.");
      return;
    }

    setUploading(true);
    setError(null);
    try {
      await api.uploadTranscriptAttachments(transcriptId, fileArray);
      await mutate();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Upload failed");
    } finally {
      setUploading(false);
    }
  }, [transcriptId, attachments, mutate]);

  const handleDelete = useCallback(async (attId: number) => {
    try {
      await api.deleteTranscriptAttachment(transcriptId, attId);
      await mutate();
      setConfirmDelete(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Delete failed");
    }
  }, [transcriptId, mutate]);

  const toggleText = (id: number) => {
    setExpandedText((prev) => {
      const next = new Set(prev);
      if (next.has(id)) next.delete(id);
      else next.add(id);
      return next;
    });
  };

  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-2">
          <h3 className="text-lg font-semibold text-gray-900">Attachments</h3>
          {attachments && attachments.length > 0 && (
            <span className="text-xs text-gray-400 bg-gray-100 px-2 py-0.5 rounded-full">
              {attachments.length}
            </span>
          )}
        </div>
        <button
          onClick={() => fileInputRef.current?.click()}
          disabled={uploading || (attachments?.length || 0) >= 10}
          className="inline-flex items-center gap-1 text-xs text-blue-600 hover:text-blue-800 disabled:text-gray-400 disabled:cursor-not-allowed transition-colors"
        >
          {uploading ? (
            <>
              <Loader2 className="h-3.5 w-3.5 animate-spin" />
              Uploading...
            </>
          ) : (
            <>
              <Upload className="h-3.5 w-3.5" />
              Add attachment
            </>
          )}
        </button>
        <input
          ref={fileInputRef}
          type="file"
          accept={ACCEPTED_TYPES}
          multiple
          className="hidden"
          onChange={(e) => {
            if (e.target.files) handleUpload(e.target.files);
            e.target.value = "";
          }}
        />
      </div>

      {error && (
        <div className="flex items-start gap-2 mb-4 p-3 rounded-md bg-red-50 border border-red-200">
          <AlertCircle className="h-4 w-4 text-red-500 flex-shrink-0 mt-0.5" />
          <p className="text-xs text-red-700">{error}</p>
          <button onClick={() => setError(null)} className="ml-auto text-red-400 hover:text-red-600">
            <span className="sr-only">Dismiss</span>&times;
          </button>
        </div>
      )}

      {(!attachments || attachments.length === 0) && !uploading && (
        <p className="text-sm text-gray-400 italic">
          Attach supporting files (PDF, PPTX, DOCX) to include in analysis.
        </p>
      )}

      {attachments && attachments.length > 0 && (
        <ul className="space-y-2">
          {attachments.map((att) => (
            <li key={att.id} className="border border-gray-100 rounded-md">
              <div className="flex items-center gap-3 px-3 py-2.5">
                <FileText className={`h-4 w-4 flex-shrink-0 ${FILE_TYPE_ICONS[att.file_type] || "text-gray-400"}`} />
                <div className="min-w-0 flex-1">
                  <p className="text-sm font-medium text-gray-800 truncate">
                    {att.original_filename}
                  </p>
                  <div className="flex items-center gap-2 mt-0.5">
                    <span className="text-xs text-gray-400 uppercase">{att.file_type}</span>
                    <span className="text-xs text-gray-400">{formatSize(att.size_bytes)}</span>
                    {att.created_at && (
                      <span className="text-xs text-gray-400">{formatDate(att.created_at)}</span>
                    )}
                    {att.has_extracted_text && (
                      <button
                        onClick={() => toggleText(att.id)}
                        className="text-xs text-green-600 hover:text-green-800 flex items-center gap-0.5"
                      >
                        {expandedText.has(att.id) ? (
                          <ChevronDown className="h-3 w-3" />
                        ) : (
                          <ChevronRight className="h-3 w-3" />
                        )}
                        Text extracted
                      </button>
                    )}
                  </div>
                </div>
                <a
                  href={api.getAttachmentDownloadUrl(transcriptId, att.id)}
                  className="text-gray-400 hover:text-blue-600 transition-colors"
                  title="Download"
                >
                  <Download className="h-4 w-4" />
                </a>
                {confirmDelete === att.id ? (
                  <div className="flex items-center gap-1">
                    <button
                      onClick={() => handleDelete(att.id)}
                      className="text-xs text-red-600 hover:text-red-800 font-medium"
                    >
                      Confirm
                    </button>
                    <button
                      onClick={() => setConfirmDelete(null)}
                      className="text-xs text-gray-400 hover:text-gray-600"
                    >
                      Cancel
                    </button>
                  </div>
                ) : (
                  <button
                    onClick={() => setConfirmDelete(att.id)}
                    className="text-gray-400 hover:text-red-500 transition-colors"
                    title="Delete"
                  >
                    <Trash2 className="h-4 w-4" />
                  </button>
                )}
              </div>
              {expandedText.has(att.id) && (
                <ExtractedTextPreview transcriptId={transcriptId} attachmentId={att.id} />
              )}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

function ExtractedTextPreview({ transcriptId, attachmentId }: { transcriptId: number; attachmentId: number }) {
  const [text, setText] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.getTranscriptAttachment(transcriptId, attachmentId)
      .then((data) => setText(data.extracted_text))
      .catch(() => setText(null))
      .finally(() => setLoading(false));
  }, [transcriptId, attachmentId]);

  if (loading) {
    return (
      <div className="px-3 pb-3 border-t border-gray-100 pt-2">
        <p className="text-xs text-gray-400">Loading extracted text...</p>
      </div>
    );
  }

  if (!text) {
    return (
      <div className="px-3 pb-3 border-t border-gray-100 pt-2">
        <p className="text-xs text-gray-400 italic">No text available</p>
      </div>
    );
  }

  return (
    <div className="px-3 pb-3 border-t border-gray-100 pt-2">
      <pre className="text-xs text-gray-600 whitespace-pre-wrap max-h-60 overflow-y-auto font-sans">
        {text.length > 2000 ? text.substring(0, 2000) + "\n\n[... truncated]" : text}
      </pre>
    </div>
  );
}
