"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { api } from "@/lib/api";

const STATUS_OPTIONS = ["active", "planning", "paused", "completed"];

const COLOR_PRESETS = [
  "#3B82F6", // blue
  "#10B981", // green
  "#F59E0B", // amber
  "#EF4444", // red
  "#8B5CF6", // purple
  "#EC4899", // pink
  "#14B8A6", // teal
  "#F97316", // orange
];

export default function NewProjectPage() {
  const router = useRouter();
  const [name, setName] = useState("");
  const [description, setDescription] = useState("");
  const [status, setStatus] = useState("active");
  const [color, setColor] = useState(COLOR_PRESETS[0]);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!name.trim()) return;

    setSubmitting(true);
    setError(null);

    try {
      const project = await api.createProject({
        name: name.trim(),
        description: description.trim() || undefined,
        status,
        color,
      });
      router.push(`/projects/${project.id}`);
    } catch (err) {
      setError(
        err instanceof Error ? err.message : "Failed to create project",
      );
      setSubmitting(false);
    }
  };

  return (
    <div className="space-y-6">
      <Link
        href="/projects"
        className="inline-block text-base text-forest-500 hover:text-blue-800"
      >
        &larr; Back to Projects
      </Link>

      <div className="mx-auto max-w-lg">
        <h2 className="text-2xl font-bold text-forest-950">New Project</h2>
        <p className="mt-1 text-base text-forest-400">
          Create a custom project to group related items.
        </p>

        <form onSubmit={handleSubmit} className="mt-6 space-y-5">
          {/* Name */}
          <div>
            <label
              htmlFor="name"
              className="block text-base font-medium text-forest-600"
            >
              Project Name *
            </label>
            <input
              id="name"
              type="text"
              required
              value={name}
              onChange={(e) => setName(e.target.value)}
              className="mt-1 block w-full rounded-md border border-forest-200 px-3 py-2 text-base shadow-sm focus:border-forest-500 focus:outline-none focus:ring-1 focus:ring-forest-500"
              placeholder="e.g. Q1 Data Migration"
            />
          </div>

          {/* Description */}
          <div>
            <label
              htmlFor="description"
              className="block text-base font-medium text-forest-600"
            >
              Description
            </label>
            <textarea
              id="description"
              rows={3}
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              className="mt-1 block w-full rounded-md border border-forest-200 px-3 py-2 text-base shadow-sm focus:border-forest-500 focus:outline-none focus:ring-1 focus:ring-forest-500"
              placeholder="Brief description of what this project covers..."
            />
          </div>

          {/* Status */}
          <div>
            <label
              htmlFor="status"
              className="block text-base font-medium text-forest-600"
            >
              Status
            </label>
            <select
              id="status"
              value={status}
              onChange={(e) => setStatus(e.target.value)}
              className="mt-1 block w-full rounded-md border border-forest-200 px-3 py-2 text-base shadow-sm focus:border-forest-500 focus:outline-none focus:ring-1 focus:ring-forest-500"
            >
              {STATUS_OPTIONS.map((s) => (
                <option key={s} value={s}>
                  {s.charAt(0).toUpperCase() + s.slice(1)}
                </option>
              ))}
            </select>
          </div>

          {/* Color */}
          <div>
            <label className="block text-base font-medium text-forest-600">
              Color
            </label>
            <div className="mt-2 flex gap-2">
              {COLOR_PRESETS.map((c) => (
                <button
                  key={c}
                  type="button"
                  onClick={() => setColor(c)}
                  className={`h-8 w-8 rounded-full border-2 transition-transform ${
                    color === c
                      ? "border-gray-900 scale-110"
                      : "border-transparent hover:scale-105"
                  }`}
                  style={{ backgroundColor: c }}
                />
              ))}
            </div>
          </div>

          {/* Error */}
          {error && (
            <div className="rounded-md border border-red-200 bg-red-50 p-3">
              <p className="text-base text-red-700">{error}</p>
            </div>
          )}

          {/* Submit */}
          <div className="flex items-center gap-3 pt-2">
            <button
              type="submit"
              disabled={submitting || !name.trim()}
              className="inline-flex items-center rounded-md bg-forest-500 px-4 py-2 text-base font-medium text-white hover:bg-forest-600 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            >
              {submitting ? "Creating..." : "Create Project"}
            </button>
            <Link
              href="/projects"
              className="text-base text-forest-400 hover:text-forest-600"
            >
              Cancel
            </Link>
          </div>
        </form>
      </div>
    </div>
  );
}
