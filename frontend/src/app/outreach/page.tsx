"use client";

import { useEffect, useState, useCallback } from "react";
import { api } from "@/lib/api";
import { formatDate } from "@/lib/utils";
import type {
  OutreachSchema,
  OutreachCreate,
  DivisionProfileSchema,
  DivisionProfileCreate,
} from "@/lib/types";
import EntityModal, {
  FormInput,
  FormTextarea,
  FormSelect,
} from "@/components/EntityModal";

/* ── constants ───────────────────────────────────────────────────────── */

const KANBAN_COLUMNS = [
  { key: "initial_contact", label: "Initial Contact", color: "border-gray-300" },
  { key: "interested", label: "Interested", color: "border-blue-400" },
  { key: "engaged", label: "Engaged", color: "border-amber-400" },
  { key: "committed", label: "Committed", color: "border-green-400" },
];

const STATUS_OPTIONS = [
  { value: "initial_contact", label: "Initial Contact" },
  { value: "interested", label: "Interested" },
  { value: "engaged", label: "Engaged" },
  { value: "committed", label: "Committed" },
  { value: "cold", label: "Cold" },
];

const DIVISION_STATUS_OPTIONS = [
  { value: "prospect", label: "Prospect" },
  { value: "in_discussion", label: "In Discussion" },
  { value: "pilot", label: "Pilot" },
  { value: "active", label: "Active" },
];

/* ── sub-components ──────────────────────────────────────────────────── */

function Stars({ count, max = 5 }: { count: number; max?: number }) {
  return (
    <span className="inline-flex gap-0.5">
      {Array.from({ length: max }, (_, i) => (
        <svg
          key={i}
          className={`w-3.5 h-3.5 ${i < count ? "text-amber-400" : "text-gray-200"}`}
          fill="currentColor"
          viewBox="0 0 20 20"
        >
          <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
        </svg>
      ))}
    </span>
  );
}

function ContactCard({
  contact,
  onClick,
}: {
  contact: OutreachSchema;
  onClick: () => void;
}) {
  return (
    <div
      onClick={onClick}
      className="bg-white rounded-lg border border-gray-200 shadow-sm hover:shadow-md transition-shadow cursor-pointer p-4"
    >
      <div className="flex items-start justify-between mb-2">
        <div>
          <h4 className="text-sm font-semibold text-gray-900">
            {contact.contact_name}
          </h4>
          {contact.contact_role && (
            <p className="text-xs text-gray-500">{contact.contact_role}</p>
          )}
        </div>
        <Stars count={contact.interest_level} />
      </div>

      {contact.division && (
        <span className="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-purple-50 text-purple-700 border border-purple-200 mb-2">
          {contact.division}
        </span>
      )}

      <div className="flex items-center gap-3 text-xs text-gray-400 mt-2">
        {contact.meeting_count > 0 && (
          <span className="flex items-center gap-1">
            <svg
              className="w-3 h-3"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"
              />
            </svg>
            {contact.meeting_count} meeting{contact.meeting_count !== 1 ? "s" : ""}
          </span>
        )}
        {contact.last_contact_date && (
          <span>Last: {formatDate(contact.last_contact_date)}</span>
        )}
      </div>

      {contact.next_step && (
        <div className="mt-3 p-2 bg-blue-50 border border-blue-100 rounded-md">
          <p className="text-xs font-medium text-blue-600 mb-0.5">Next Step</p>
          <p className="text-xs text-blue-800">{contact.next_step}</p>
          {contact.next_step_date && (
            <p className="text-xs text-blue-500 mt-0.5">
              Due: {formatDate(contact.next_step_date)}
            </p>
          )}
        </div>
      )}
    </div>
  );
}

function DivisionCard({
  division,
  onClick,
}: {
  division: DivisionProfileSchema;
  onClick: () => void;
}) {
  const statusColors: Record<string, string> = {
    prospect: "bg-gray-100 text-gray-700 border-gray-200",
    in_discussion: "bg-blue-100 text-blue-700 border-blue-200",
    pilot: "bg-amber-100 text-amber-700 border-amber-200",
    active: "bg-green-100 text-green-700 border-green-200",
  };
  const sc = statusColors[division.status] ?? statusColors.prospect;

  return (
    <div
      onClick={onClick}
      className="bg-white rounded-lg border border-gray-200 shadow-sm hover:shadow-md transition-shadow cursor-pointer p-4 min-w-[220px]"
    >
      <div className="flex items-start justify-between mb-2">
        <h4 className="text-sm font-semibold text-gray-900">{division.name}</h4>
        <span
          className={`inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium border ${sc}`}
        >
          {division.status.replace(/_/g, " ")}
        </span>
      </div>
      {division.key_contact && (
        <p className="text-xs text-gray-500 mb-1">
          <span className="font-medium">Contact:</span> {division.key_contact}
        </p>
      )}
      {division.pain_points && (
        <p className="text-xs text-gray-400 line-clamp-2">
          {division.pain_points}
        </p>
      )}
    </div>
  );
}

/* ── main component ──────────────────────────────────────────────────── */

export default function OutreachPage() {
  const [contacts, setContacts] = useState<OutreachSchema[]>([]);
  const [divisions, setDivisions] = useState<DivisionProfileSchema[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  /* contact modal */
  const [contactModalOpen, setContactModalOpen] = useState(false);
  const [editingContact, setEditingContact] = useState<OutreachSchema | null>(
    null,
  );
  const [saving, setSaving] = useState(false);
  const [deleting, setDeleting] = useState(false);
  const [modalError, setModalError] = useState<string | null>(null);

  /* contact form fields */
  const [formName, setFormName] = useState("");
  const [formRole, setFormRole] = useState("");
  const [formDivision, setFormDivision] = useState("");
  const [formStatus, setFormStatus] = useState("initial_contact");
  const [formInterest, setFormInterest] = useState("3");
  const [formFirstContact, setFormFirstContact] = useState("");
  const [formLastContact, setFormLastContact] = useState("");
  const [formMeetings, setFormMeetings] = useState("0");
  const [formNotes, setFormNotes] = useState("");
  const [formNextStep, setFormNextStep] = useState("");
  const [formNextStepDate, setFormNextStepDate] = useState("");

  /* division modal */
  const [divModalOpen, setDivModalOpen] = useState(false);
  const [editingDiv, setEditingDiv] = useState<DivisionProfileSchema | null>(
    null,
  );
  const [divSaving, setDivSaving] = useState(false);
  const [divDeleting, setDivDeleting] = useState(false);
  const [divModalError, setDivModalError] = useState<string | null>(null);

  /* division form fields */
  const [divName, setDivName] = useState("");
  const [divStatus, setDivStatus] = useState("prospect");
  const [divTools, setDivTools] = useState("");
  const [divPainPoints, setDivPainPoints] = useState("");
  const [divKeyContact, setDivKeyContact] = useState("");
  const [divNotes, setDivNotes] = useState("");

  const reload = useCallback(() => {
    Promise.all([api.getOutreach(), api.getDivisions()])
      .then(([c, d]) => {
        setContacts(c);
        setDivisions(d);
      })
      .catch(() => {});
  }, []);

  useEffect(() => {
    Promise.all([api.getOutreach(), api.getDivisions()])
      .then(([c, d]) => {
        setContacts(c);
        setDivisions(d);
      })
      .catch((e) =>
        setError(e instanceof Error ? e.message : "Failed to load data"),
      )
      .finally(() => setLoading(false));
  }, []);

  /* ── contact modal helpers ─────────────────────────────────────────── */

  const resetContactForm = () => {
    setFormName("");
    setFormRole("");
    setFormDivision("");
    setFormStatus("initial_contact");
    setFormInterest("3");
    setFormFirstContact("");
    setFormLastContact("");
    setFormMeetings("0");
    setFormNotes("");
    setFormNextStep("");
    setFormNextStepDate("");
  };

  const openCreateContact = () => {
    setEditingContact(null);
    resetContactForm();
    setModalError(null);
    setContactModalOpen(true);
  };

  const openEditContact = (c: OutreachSchema) => {
    setEditingContact(c);
    setFormName(c.contact_name);
    setFormRole(c.contact_role || "");
    setFormDivision(c.division || "");
    setFormStatus(c.status);
    setFormInterest(String(c.interest_level));
    setFormFirstContact(c.first_contact_date || "");
    setFormLastContact(c.last_contact_date || "");
    setFormMeetings(String(c.meeting_count));
    setFormNotes(c.notes || "");
    setFormNextStep(c.next_step || "");
    setFormNextStepDate(c.next_step_date || "");
    setModalError(null);
    setContactModalOpen(true);
  };

  const handleSaveContact = async () => {
    if (!formName.trim()) {
      setModalError("Contact name is required.");
      return;
    }
    setSaving(true);
    setModalError(null);
    try {
      const data: OutreachCreate = {
        contact_name: formName.trim(),
        contact_role: formRole.trim() || undefined,
        division: formDivision.trim() || undefined,
        status: formStatus,
        interest_level: parseInt(formInterest, 10) || 3,
        first_contact_date: formFirstContact || undefined,
        last_contact_date: formLastContact || undefined,
        meeting_count: parseInt(formMeetings, 10) || 0,
        notes: formNotes.trim() || undefined,
        next_step: formNextStep.trim() || undefined,
        next_step_date: formNextStepDate || undefined,
      };
      if (editingContact) {
        await api.updateOutreach(editingContact.id, data);
      } else {
        await api.createOutreach(data);
      }
      setContactModalOpen(false);
      reload();
    } catch (e) {
      setModalError(e instanceof Error ? e.message : "Save failed");
    } finally {
      setSaving(false);
    }
  };

  const handleDeleteContact = async () => {
    if (!editingContact) return;
    setDeleting(true);
    try {
      await api.deleteOutreach(editingContact.id);
      setContactModalOpen(false);
      reload();
    } catch (e) {
      setModalError(e instanceof Error ? e.message : "Delete failed");
    } finally {
      setDeleting(false);
    }
  };

  /* ── division modal helpers ────────────────────────────────────────── */

  const resetDivForm = () => {
    setDivName("");
    setDivStatus("prospect");
    setDivTools("");
    setDivPainPoints("");
    setDivKeyContact("");
    setDivNotes("");
  };

  const openCreateDiv = () => {
    setEditingDiv(null);
    resetDivForm();
    setDivModalError(null);
    setDivModalOpen(true);
  };

  const openEditDiv = (d: DivisionProfileSchema) => {
    setEditingDiv(d);
    setDivName(d.name);
    setDivStatus(d.status);
    setDivTools(d.current_tools || "");
    setDivPainPoints(d.pain_points || "");
    setDivKeyContact(d.key_contact || "");
    setDivNotes(d.notes || "");
    setDivModalError(null);
    setDivModalOpen(true);
  };

  const handleSaveDiv = async () => {
    if (!divName.trim()) {
      setDivModalError("Division name is required.");
      return;
    }
    setDivSaving(true);
    setDivModalError(null);
    try {
      const data: DivisionProfileCreate = {
        name: divName.trim(),
        status: divStatus,
        current_tools: divTools.trim() || undefined,
        pain_points: divPainPoints.trim() || undefined,
        key_contact: divKeyContact.trim() || undefined,
        notes: divNotes.trim() || undefined,
      };
      if (editingDiv) {
        await api.updateDivision(editingDiv.id, data);
      } else {
        await api.createDivision(data);
      }
      setDivModalOpen(false);
      reload();
    } catch (e) {
      setDivModalError(e instanceof Error ? e.message : "Save failed");
    } finally {
      setDivSaving(false);
    }
  };

  const handleDeleteDiv = async () => {
    if (!editingDiv) return;
    setDivDeleting(true);
    try {
      await api.deleteDivision(editingDiv.id);
      setDivModalOpen(false);
      reload();
    } catch (e) {
      setDivModalError(e instanceof Error ? e.message : "Delete failed");
    } finally {
      setDivDeleting(false);
    }
  };

  /* ── derived data ──────────────────────────────────────────────────── */

  const coldContacts = contacts.filter((c) => c.status === "cold");
  const columnData = KANBAN_COLUMNS.map((col) => ({
    ...col,
    contacts: contacts.filter((c) => c.status === col.key),
  }));

  /* ── render ────────────────────────────────────────────────────────── */

  if (loading) {
    return (
      <div className="space-y-6">
        <h2 className="text-2xl font-bold text-gray-900">Outreach Tracker</h2>
        <p className="text-sm text-gray-500">Loading...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="space-y-6">
        <h2 className="text-2xl font-bold text-gray-900">Outreach Tracker</h2>
        <div className="rounded-lg border border-red-200 bg-red-50 p-6">
          <p className="text-sm text-red-700">{error}</p>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* header */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold text-gray-900">
            Outreach Tracker
          </h2>
          <p className="mt-1 text-sm text-gray-500">
            Track cross-division outreach contacts and engagement pipeline
          </p>
        </div>
        <div className="flex gap-2">
          <button
            onClick={openCreateDiv}
            className="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50 transition-colors"
          >
            + Division
          </button>
          <button
            onClick={openCreateContact}
            className="px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-md hover:bg-blue-700 transition-colors"
          >
            + Contact
          </button>
        </div>
      </div>

      {/* division profiles */}
      {divisions.length > 0 && (
        <div>
          <h3 className="text-sm font-semibold text-gray-700 mb-3 uppercase tracking-wider">
            Division Profiles
          </h3>
          <div className="flex gap-4 overflow-x-auto pb-2">
            {divisions.map((d) => (
              <DivisionCard
                key={d.id}
                division={d}
                onClick={() => openEditDiv(d)}
              />
            ))}
          </div>
        </div>
      )}

      {/* kanban board */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {columnData.map((col) => (
          <div key={col.key}>
            <div
              className={`flex items-center gap-2 mb-3 pb-2 border-b-2 ${col.color}`}
            >
              <h3 className="text-sm font-semibold text-gray-700">
                {col.label}
              </h3>
              <span className="inline-flex items-center justify-center w-5 h-5 rounded-full bg-gray-100 text-xs font-medium text-gray-600">
                {col.contacts.length}
              </span>
            </div>
            <div className="space-y-3">
              {col.contacts.length === 0 ? (
                <p className="text-xs text-gray-400 italic py-4 text-center">
                  No contacts
                </p>
              ) : (
                col.contacts.map((c) => (
                  <ContactCard
                    key={c.id}
                    contact={c}
                    onClick={() => openEditContact(c)}
                  />
                ))
              )}
            </div>
          </div>
        ))}
      </div>

      {/* cold contacts */}
      {coldContacts.length > 0 && (
        <div>
          <div className="flex items-center gap-2 mb-3 pb-2 border-b-2 border-red-300">
            <h3 className="text-sm font-semibold text-gray-700">Cold</h3>
            <span className="inline-flex items-center justify-center w-5 h-5 rounded-full bg-gray-100 text-xs font-medium text-gray-600">
              {coldContacts.length}
            </span>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-3">
            {coldContacts.map((c) => (
              <ContactCard
                key={c.id}
                contact={c}
                onClick={() => openEditContact(c)}
              />
            ))}
          </div>
        </div>
      )}

      {/* empty state */}
      {contacts.length === 0 && divisions.length === 0 && (
        <div className="text-center py-12">
          <p className="text-sm text-gray-500">
            No outreach contacts or divisions yet. Use the buttons above to get
            started.
          </p>
        </div>
      )}

      {/* contact modal */}
      <EntityModal
        open={contactModalOpen}
        onClose={() => setContactModalOpen(false)}
        title={editingContact ? "Edit Contact" : "New Outreach Contact"}
        onSave={handleSaveContact}
        onDelete={editingContact ? handleDeleteContact : undefined}
        saving={saving}
        deleting={deleting}
        error={modalError}
      >
        <FormInput
          label="Contact Name"
          value={formName}
          onChange={setFormName}
          placeholder="Full name"
        />
        <div className="grid grid-cols-2 gap-4">
          <FormInput
            label="Role"
            value={formRole}
            onChange={setFormRole}
            placeholder="Job title"
          />
          <FormInput
            label="Division"
            value={formDivision}
            onChange={setFormDivision}
            placeholder="Division name"
          />
        </div>
        <div className="grid grid-cols-2 gap-4">
          <FormSelect
            label="Status"
            value={formStatus}
            onChange={setFormStatus}
            options={STATUS_OPTIONS}
          />
          <FormSelect
            label="Interest Level"
            value={formInterest}
            onChange={setFormInterest}
            options={[
              { value: "1", label: "1 - Minimal" },
              { value: "2", label: "2 - Low" },
              { value: "3", label: "3 - Moderate" },
              { value: "4", label: "4 - High" },
              { value: "5", label: "5 - Very High" },
            ]}
          />
        </div>
        <div className="grid grid-cols-2 gap-4">
          <FormInput
            label="First Contact"
            value={formFirstContact}
            onChange={setFormFirstContact}
            type="date"
          />
          <FormInput
            label="Last Contact"
            value={formLastContact}
            onChange={setFormLastContact}
            type="date"
          />
        </div>
        <FormInput
          label="Meeting Count"
          value={formMeetings}
          onChange={setFormMeetings}
          type="number"
        />
        <FormTextarea
          label="Notes"
          value={formNotes}
          onChange={setFormNotes}
          placeholder="Additional notes"
          rows={2}
        />
        <FormInput
          label="Next Step"
          value={formNextStep}
          onChange={setFormNextStep}
          placeholder="What happens next?"
        />
        <FormInput
          label="Next Step Date"
          value={formNextStepDate}
          onChange={setFormNextStepDate}
          type="date"
        />
      </EntityModal>

      {/* division modal */}
      <EntityModal
        open={divModalOpen}
        onClose={() => setDivModalOpen(false)}
        title={editingDiv ? "Edit Division" : "New Division Profile"}
        onSave={handleSaveDiv}
        onDelete={editingDiv ? handleDeleteDiv : undefined}
        saving={divSaving}
        deleting={divDeleting}
        error={divModalError}
      >
        <FormInput
          label="Division Name"
          value={divName}
          onChange={setDivName}
          placeholder="e.g. Life Insurance"
        />
        <FormSelect
          label="Status"
          value={divStatus}
          onChange={setDivStatus}
          options={DIVISION_STATUS_OPTIONS}
        />
        <FormInput
          label="Current Tools"
          value={divTools}
          onChange={setDivTools}
          placeholder="What tools do they use today?"
        />
        <FormTextarea
          label="Pain Points"
          value={divPainPoints}
          onChange={setDivPainPoints}
          placeholder="Key pain points or challenges"
          rows={2}
        />
        <FormInput
          label="Key Contact"
          value={divKeyContact}
          onChange={setDivKeyContact}
          placeholder="Primary contact person"
        />
        <FormTextarea
          label="Notes"
          value={divNotes}
          onChange={setDivNotes}
          placeholder="Additional notes"
          rows={2}
        />
      </EntityModal>
    </div>
  );
}
