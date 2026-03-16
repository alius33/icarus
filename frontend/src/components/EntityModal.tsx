"use client";

import { ReactNode, useEffect, useCallback } from "react";

interface EntityModalProps {
  open: boolean;
  onClose: () => void;
  title: string;
  children: ReactNode;
  onSave: () => void;
  onDelete?: () => void;
  saving?: boolean;
  deleting?: boolean;
  error?: string | null;
}

export default function EntityModal({
  open,
  onClose,
  title,
  children,
  onSave,
  onDelete,
  saving,
  deleting,
  error,
}: EntityModalProps) {
  const handleKeyDown = useCallback((e: KeyboardEvent) => {
    if (e.key === "Escape") onClose();
  }, [onClose]);

  useEffect(() => {
    if (!open) return;
    document.addEventListener("keydown", handleKeyDown);
    return () => document.removeEventListener("keydown", handleKeyDown);
  }, [open, handleKeyDown]);

  if (!open) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center" role="dialog" aria-modal="true" aria-labelledby="entity-modal-title">
      {/* Backdrop */}
      <div
        className="absolute inset-0 bg-black/40 transition-opacity duration-200"
        onClick={onClose}
        aria-hidden="true"
      />
      {/* Modal */}
      <div className="relative bg-white dark:bg-forest-800 rounded-2xl shadow-2xl w-full max-w-lg mx-2 fold:mx-4 max-h-[90vh] overflow-y-auto">
        {/* Header */}
        <div className="flex items-center justify-between px-6 py-4 border-b border-forest-200 dark:border-forest-700">
          <h3 id="entity-modal-title" className="text-lg font-semibold text-forest-950 dark:text-forest-50">{title}</h3>
          <button
            onClick={onClose}
            aria-label="Close dialog"
            className="text-forest-300 hover:text-forest-500 dark:hover:text-forest-200 text-xl leading-none"
          >
            &times;
          </button>
        </div>

        {/* Body */}
        <div className="px-6 py-4 space-y-4">
          {error && (
            <div className="rounded-md bg-red-50 dark:bg-red-900/30 border border-red-200 dark:border-red-800 px-4 py-2">
              <p className="text-base text-red-700 dark:text-red-400">{error}</p>
            </div>
          )}
          {children}
        </div>

        {/* Footer */}
        <div className="flex items-center justify-between px-6 py-4 border-t border-forest-200 dark:border-forest-700 bg-forest-50 dark:bg-forest-800/50 rounded-b-2xl">
          <div>
            {onDelete && (
              <button
                onClick={onDelete}
                disabled={deleting}
                className="px-4 py-2 text-base font-medium text-red-600 hover:text-red-700 hover:bg-red-50 rounded-md transition-colors disabled:opacity-50"
              >
                {deleting ? "Deleting..." : "Delete"}
              </button>
            )}
          </div>
          <div className="flex gap-3">
            <button
              onClick={onClose}
              className="px-4 py-2 text-base font-medium text-forest-600 dark:text-forest-200 bg-white dark:bg-forest-800 dark:bg-forest-700 border border-forest-200 dark:border-forest-700 rounded-md hover:bg-forest-50 dark:hover:bg-forest-600 transition-colors"
            >
              Cancel
            </button>
            <button
              onClick={onSave}
              disabled={saving}
              className="px-4 py-2 text-base font-medium text-white bg-forest-500 rounded-md hover:bg-forest-600 transition-colors disabled:opacity-50"
            >
              {saving ? "Saving..." : "Save"}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

// Shared form field components
export function FormField({
  label,
  htmlFor,
  children,
}: {
  label: string;
  htmlFor?: string;
  children: ReactNode;
}) {
  return (
    <div>
      <label htmlFor={htmlFor} className="block text-base font-medium text-forest-600 dark:text-forest-200 mb-1">
        {label}
      </label>
      {children}
    </div>
  );
}

export function FormInput({
  label,
  value,
  onChange,
  placeholder,
  type = "text",
  disabled,
}: {
  label: string;
  value: string;
  onChange: (v: string) => void;
  placeholder?: string;
  type?: string;
  disabled?: boolean;
}) {
  const id = `form-input-${label.toLowerCase().replace(/\s+/g, "-")}`;
  return (
    <FormField label={label} htmlFor={id}>
      <input
        id={id}
        type={type}
        value={value}
        onChange={(e) => onChange(e.target.value)}
        placeholder={placeholder}
        disabled={disabled}
        className="w-full border border-forest-200 dark:border-forest-700 rounded-md px-3 py-2 text-base text-forest-950 dark:text-forest-50 bg-white dark:bg-forest-800 focus:outline-none focus:ring-1 focus:ring-forest-500 focus:border-forest-500 disabled:bg-forest-100 dark:disabled:bg-forest-700"
      />
    </FormField>
  );
}

export function FormTextarea({
  label,
  value,
  onChange,
  placeholder,
  rows = 3,
}: {
  label: string;
  value: string;
  onChange: (v: string) => void;
  placeholder?: string;
  rows?: number;
}) {
  const id = `form-textarea-${label.toLowerCase().replace(/\s+/g, "-")}`;
  return (
    <FormField label={label} htmlFor={id}>
      <textarea
        id={id}
        value={value}
        onChange={(e) => onChange(e.target.value)}
        placeholder={placeholder}
        rows={rows}
        className="w-full border border-forest-200 dark:border-forest-700 rounded-md px-3 py-2 text-base text-forest-950 dark:text-forest-50 bg-white dark:bg-forest-800 focus:outline-none focus:ring-1 focus:ring-forest-500 focus:border-forest-500"
      />
    </FormField>
  );
}

export function FormSelect({
  label,
  value,
  onChange,
  options,
}: {
  label: string;
  value: string;
  onChange: (v: string) => void;
  options: { value: string; label: string }[];
}) {
  const id = `form-select-${label.toLowerCase().replace(/\s+/g, "-")}`;
  return (
    <FormField label={label} htmlFor={id}>
      <select
        id={id}
        value={value}
        onChange={(e) => onChange(e.target.value)}
        className="w-full border border-forest-200 dark:border-forest-700 rounded-md px-3 py-2 text-base text-forest-950 dark:text-forest-50 bg-white dark:bg-forest-800 focus:outline-none focus:ring-1 focus:ring-forest-500 focus:border-forest-500"
      >
        {options.map((opt) => (
          <option key={opt.value} value={opt.value}>
            {opt.label}
          </option>
        ))}
      </select>
    </FormField>
  );
}
