"use client";

import { useParams, useRouter } from "next/navigation";
import Link from "next/link";
import {
  ArrowLeft,
  FileText,
  MessageSquare,
  CheckCircle2,
  Circle,
  Trash2,
  Clock,
  Loader2,
} from "lucide-react";
import { useProjectUpdate } from "@/lib/swr";
import { api } from "@/lib/api";
import { useToast } from "@/lib/hooks/useToast";
import { useState } from "react";
import { mutate } from "swr";

export default function UpdateDetailPage() {
  const params = useParams();
  const router = useRouter();
  const id = Number(params.id);
  const { data: update, isLoading } = useProjectUpdate(id);
  const toast = useToast();
  const [deleting, setDeleting] = useState(false);
  const [showRaw, setShowRaw] = useState(false);

  const handleDelete = async () => {
    if (!confirm("Delete this update? This cannot be undone.")) return;
    setDeleting(true);
    try {
      await api.deleteProjectUpdate(id);
      toast.success("Update deleted");
      mutate((key: unknown) => {
        if (typeof key === "string") return key.includes("project-update");
        if (Array.isArray(key)) return key[0] === "project-updates";
        return false;
      });
      router.push("/updates");
    } catch {
      toast.error("Failed to delete");
    } finally {
      setDeleting(false);
    }
  };

  if (isLoading) {
    return (
      <div className="flex items-center justify-center py-20">
        <Loader2 className="h-8 w-8 animate-spin text-forest-400" />
      </div>
    );
  }

  if (!update) {
    return (
      <div className="text-center py-20 text-forest-400">
        <p className="text-lg">Update not found</p>
        <Link href="/updates" className="text-forest-600 hover:underline text-sm mt-2 block">
          Back to updates
        </Link>
      </div>
    );
  }

  const displayContent = showRaw && update.raw_content ? update.raw_content : update.content;

  return (
    <div className="max-w-3xl mx-auto space-y-6">
      {/* Back link */}
      <Link
        href="/updates"
        className="inline-flex items-center gap-1 text-sm text-forest-500 hover:text-forest-700 dark:hover:text-forest-300"
      >
        <ArrowLeft className="h-4 w-4" /> Back to updates
      </Link>

      {/* Header */}
      <div className="bg-white dark:bg-forest-800 border border-forest-200 dark:border-forest-700 rounded-xl p-6">
        <div className="flex items-start justify-between gap-4 mb-4">
          <div>
            <h1 className="text-xl font-bold text-forest-950 dark:text-forest-50 flex items-center gap-2">
              {update.content_type === "teams_chat" ? (
                <MessageSquare className="h-5 w-5 text-blue-500" />
              ) : (
                <FileText className="h-5 w-5 text-forest-500" />
              )}
              {update.title}
            </h1>
            <div className="flex items-center gap-3 mt-2 text-sm text-forest-500">
              <span className="flex items-center gap-1">
                <Clock className="h-3.5 w-3.5" />
                {new Date(update.created_at).toLocaleString()}
              </span>
              <span className="flex items-center gap-1">
                {update.is_processed ? (
                  <>
                    <CheckCircle2 className="h-3.5 w-3.5 text-green-500" />
                    Processed
                  </>
                ) : (
                  <>
                    <Circle className="h-3.5 w-3.5" />
                    Pending analysis
                  </>
                )}
              </span>
            </div>
          </div>
          <button
            onClick={handleDelete}
            disabled={deleting}
            className="text-red-400 hover:text-red-600 p-2 rounded-lg hover:bg-red-50 dark:hover:bg-red-900/20 transition-colors"
            title="Delete update"
          >
            {deleting ? (
              <Loader2 className="h-4 w-4 animate-spin" />
            ) : (
              <Trash2 className="h-4 w-4" />
            )}
          </button>
        </div>

        {/* Project badges */}
        <div className="flex flex-wrap gap-2 mb-4">
          {update.project_names.map((name, i) => (
            <span
              key={i}
              className="px-3 py-1 rounded-full text-xs font-medium bg-forest-100 dark:bg-forest-700 text-forest-600 dark:text-forest-300"
            >
              {name}
            </span>
          ))}
        </div>

        {/* Raw/Parsed toggle for Teams chats */}
        {update.content_type === "teams_chat" && update.raw_content && (
          <div className="flex items-center gap-2 mb-4">
            <button
              onClick={() => setShowRaw(false)}
              className={`px-3 py-1 rounded-md text-xs font-medium transition-colors ${
                !showRaw
                  ? "bg-forest-600 text-white"
                  : "bg-forest-200 dark:bg-forest-700 text-forest-600 dark:text-forest-300"
              }`}
            >
              Parsed
            </button>
            <button
              onClick={() => setShowRaw(true)}
              className={`px-3 py-1 rounded-md text-xs font-medium transition-colors ${
                showRaw
                  ? "bg-forest-600 text-white"
                  : "bg-forest-200 dark:bg-forest-700 text-forest-600 dark:text-forest-300"
              }`}
            >
              Raw
            </button>
          </div>
        )}

        {/* Content */}
        <div className={`whitespace-pre-wrap text-sm text-forest-800 dark:text-forest-200 leading-relaxed ${
          update.content_type === "teams_chat" ? "font-mono text-xs" : ""
        }`}>
          {displayContent}
        </div>
      </div>
    </div>
  );
}
