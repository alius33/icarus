"use client";

import { useState, useCallback } from "react";

interface UseEntityModalOptions<T> {
  onSave: (data: T) => Promise<void>;
  onDelete?: (id: number) => Promise<void>;
  onSuccess?: () => void;
}

export function useEntityModal<T>(options: UseEntityModalOptions<T>) {
  const [open, setOpen] = useState(false);
  const [editId, setEditId] = useState<number | null>(null);
  const [saving, setSaving] = useState(false);
  const [deleting, setDeleting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [confirmDelete, setConfirmDelete] = useState(false);

  const openCreate = useCallback(() => {
    setEditId(null);
    setError(null);
    setConfirmDelete(false);
    setOpen(true);
  }, []);

  const openEdit = useCallback((id: number) => {
    setEditId(id);
    setError(null);
    setConfirmDelete(false);
    setOpen(true);
  }, []);

  const close = useCallback(() => {
    setOpen(false);
    setEditId(null);
    setError(null);
    setConfirmDelete(false);
  }, []);

  const save = useCallback(async (data: T) => {
    setSaving(true);
    setError(null);
    try {
      await options.onSave(data);
      close();
      options.onSuccess?.();
    } catch (e) {
      setError(e instanceof Error ? e.message : "Save failed");
    } finally {
      setSaving(false);
    }
  }, [options, close]);

  const handleDelete = useCallback(async () => {
    if (!confirmDelete) {
      setConfirmDelete(true);
      return;
    }
    if (!editId || !options.onDelete) return;
    setDeleting(true);
    setError(null);
    try {
      await options.onDelete(editId);
      close();
      options.onSuccess?.();
    } catch (e) {
      setError(e instanceof Error ? e.message : "Delete failed");
    } finally {
      setDeleting(false);
    }
  }, [editId, confirmDelete, options, close]);

  return {
    open,
    editId,
    saving,
    deleting,
    error,
    confirmDelete,
    openCreate,
    openEdit,
    close,
    save,
    handleDelete,
  };
}
