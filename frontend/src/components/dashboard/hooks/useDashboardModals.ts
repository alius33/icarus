"use client";

import { useState, useCallback } from "react";
import { api } from "@/lib/api";
import type {
  NeedsAttentionItem,
  ActivityFeedItem,
  StakeholderEngagementItem,
} from "@/lib/types";

export type ModalEntityType =
  | "action_item"
  | "open_thread"
  | "decision"
  | "stakeholder";

export interface ModalFormState {
  title: string;
  description: string;
  status: string;
  owner: string;
  dueDate: string;
  extra: string; // role for stakeholders, rationale for decisions
}

export interface DashboardModalState {
  modalOpen: boolean;
  modalType: ModalEntityType | null;
  modalItemId: number | null;
  form: ModalFormState;
  saving: boolean;
  deleting: boolean;
  modalError: string | null;
}

export interface DashboardModalActions {
  openEntityModal: (
    type: ModalEntityType,
    id: number,
    title: string,
    description: string,
    status: string,
    owner: string,
  ) => void;
  handleAttentionClick: (item: NeedsAttentionItem) => void;
  handleActivityClick: (item: ActivityFeedItem) => void;
  handleStakeholderClick: (item: StakeholderEngagementItem) => void;
  handleModalSave: () => Promise<void>;
  handleModalDelete: () => Promise<void>;
  closeModal: () => void;
  setFormTitle: (v: string) => void;
  setFormDescription: (v: string) => void;
  setFormStatus: (v: string) => void;
  setFormOwner: (v: string) => void;
  setFormDueDate: (v: string) => void;
  setFormExtra: (v: string) => void;
}

interface UseDashboardModalsOptions {
  refreshSection: (section: string) => void;
  onNavigate?: (path: string) => void;
}

export function useDashboardModals({
  refreshSection,
  onNavigate,
}: UseDashboardModalsOptions): DashboardModalState & DashboardModalActions {
  const [modalOpen, setModalOpen] = useState(false);
  const [modalType, setModalType] = useState<ModalEntityType | null>(null);
  const [modalItemId, setModalItemId] = useState<number | null>(null);
  const [formTitle, setFormTitle] = useState("");
  const [formDescription, setFormDescription] = useState("");
  const [formStatus, setFormStatus] = useState("");
  const [formOwner, setFormOwner] = useState("");
  const [formDueDate, setFormDueDate] = useState("");
  const [formExtra, setFormExtra] = useState("");
  const [saving, setSaving] = useState(false);
  const [deleting, setDeleting] = useState(false);
  const [modalError, setModalError] = useState<string | null>(null);

  const closeModal = useCallback(() => setModalOpen(false), []);

  const openEntityModal = useCallback(
    (
      type: ModalEntityType,
      id: number,
      title: string,
      description: string,
      status: string,
      owner: string,
    ) => {
      setModalType(type);
      setModalItemId(id);
      setFormTitle(title);
      setFormDescription(description);
      setFormStatus(status);
      setFormOwner(owner);
      setFormDueDate("");
      setFormExtra("");
      setModalError(null);
      setModalOpen(true);
    },
    [],
  );

  const handleAttentionClick = useCallback(
    (item: NeedsAttentionItem) => {
      openEntityModal(
        item.entity_type as ModalEntityType,
        item.id,
        item.title,
        item.description || "",
        item.status,
        item.owner || "",
      );
    },
    [openEntityModal],
  );

  const handleActivityClick = useCallback(
    (item: ActivityFeedItem) => {
      if (item.entity_type === "transcript") {
        onNavigate?.(`/transcripts/${item.id}`);
        return;
      }
      openEntityModal(
        item.entity_type as ModalEntityType,
        item.id,
        item.title,
        "",
        "",
        "",
      );
      // Fetch full entity data to populate form
      if (item.entity_type === "action_item") {
        api.getActionItems().then((items) => {
          const found = items.find((a) => a.id === item.id);
          if (found) {
            setFormTitle(found.title);
            setFormDescription(found.description || "");
            setFormStatus(found.status);
            setFormOwner(found.owner || "");
            setFormDueDate(found.due_date || "");
          }
        });
      } else if (item.entity_type === "open_thread") {
        api.getOpenThreads().then((items) => {
          const found = items.find((t) => t.id === item.id);
          if (found) {
            setFormTitle(found.title);
            setFormDescription(found.description || "");
            setFormStatus(found.status);
            setFormOwner(found.owner || "");
          }
        });
      } else if (item.entity_type === "decision") {
        api.getDecisions().then((items) => {
          const found = items.find((d) => d.id === item.id);
          if (found) {
            setFormTitle(found.title);
            setFormDescription(found.description || "");
            setFormStatus(found.status);
            setFormOwner(found.owner || "");
          }
        });
      }
    },
    [openEntityModal, onNavigate],
  );

  const handleStakeholderClick = useCallback(
    (item: StakeholderEngagementItem) => {
      setModalType("stakeholder");
      setModalItemId(item.id);
      setFormTitle(item.name);
      setFormDescription("");
      setFormStatus(String(item.tier));
      setFormOwner("");
      setFormExtra(item.role || "");
      setModalError(null);
      setModalOpen(true);
      // Fetch full stakeholder data
      api
        .getStakeholder(item.id)
        .then((s) => {
          setFormDescription(s.notes || "");
          setFormExtra(s.role || "");
        })
        .catch(() => {});
    },
    [],
  );

  const handleModalSave = useCallback(async () => {
    if (!modalItemId || !modalType) return;
    setSaving(true);
    setModalError(null);
    try {
      if (modalType === "action_item") {
        await api.updateActionItem(modalItemId, {
          description: formTitle,
          owner: formOwner || undefined,
          status: formStatus,
          deadline: formDueDate || undefined,
          context: formDescription || undefined,
        });
      } else if (modalType === "open_thread") {
        await api.updateOpenThread(modalItemId, {
          title: formTitle,
          context: formDescription || undefined,
          status: formStatus,
        });
      } else if (modalType === "decision") {
        await api.updateDecision(modalItemId, {
          decision: formTitle,
          rationale: formDescription || undefined,
        });
      } else if (modalType === "stakeholder") {
        await api.updateStakeholder(modalItemId, {
          name: formTitle,
          role: formExtra || undefined,
          tier: Number(formStatus) || undefined,
          notes: formDescription || undefined,
        });
      }
      setModalOpen(false);
      refreshSection("attention");
    } catch (e) {
      setModalError(e instanceof Error ? e.message : "Save failed");
    } finally {
      setSaving(false);
    }
  }, [
    modalItemId,
    modalType,
    formTitle,
    formDescription,
    formStatus,
    formOwner,
    formDueDate,
    formExtra,
    refreshSection,
  ]);

  const handleModalDelete = useCallback(async () => {
    if (!modalItemId || !modalType) return;
    setDeleting(true);
    try {
      if (modalType === "action_item") {
        await api.deleteActionItem(modalItemId);
      } else if (modalType === "open_thread") {
        await api.deleteOpenThread(modalItemId);
      } else if (modalType === "decision") {
        await api.deleteDecision(modalItemId);
      } else if (modalType === "stakeholder") {
        await api.deleteStakeholder(modalItemId);
      }
      setModalOpen(false);
      refreshSection("attention");
    } catch (e) {
      setModalError(e instanceof Error ? e.message : "Delete failed");
    } finally {
      setDeleting(false);
    }
  }, [modalItemId, modalType, refreshSection]);

  return {
    // State
    modalOpen,
    modalType,
    modalItemId,
    form: {
      title: formTitle,
      description: formDescription,
      status: formStatus,
      owner: formOwner,
      dueDate: formDueDate,
      extra: formExtra,
    },
    saving,
    deleting,
    modalError,
    // Actions
    openEntityModal,
    handleAttentionClick,
    handleActivityClick,
    handleStakeholderClick,
    handleModalSave,
    handleModalDelete,
    closeModal,
    setFormTitle,
    setFormDescription,
    setFormStatus,
    setFormOwner,
    setFormDueDate,
    setFormExtra,
  };
}
