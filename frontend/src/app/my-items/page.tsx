"use client";

import { useState, useEffect, useMemo } from "react";
import { api } from "@/lib/api";
import { formatDate } from "@/lib/utils";
import type { ActionItemSchema, CommitmentSchema, OpenThreadSchema } from "@/lib/types";
import { User, CheckSquare, Handshake, AlertCircle, Clock } from "lucide-react";

interface PersonItems {
  actions: ActionItemSchema[];
  commitments: CommitmentSchema[];
  threads: OpenThreadSchema[];
}

export default function MyItemsPage() {
  const [allActions, setAllActions] = useState<ActionItemSchema[]>([]);
  const [allCommitments, setAllCommitments] = useState<CommitmentSchema[]>([]);
  const [allThreads, setAllThreads] = useState<OpenThreadSchema[]>([]);
  const [selectedPerson, setSelectedPerson] = useState<string>("");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function load() {
      try {
        const [actions, threads] = await Promise.allSettled([
          api.getActionItems("OPEN"),
          api.getOpenThreads({ status: "OPEN" }),
        ]);

        if (actions.status === "fulfilled") setAllActions(actions.value);
        if (threads.status === "fulfilled") setAllThreads(threads.value);

        // Try loading commitments — may not exist yet if Wave 3 backend not deployed
        try {
          const commitments = await api.getCommitments("pending");
          setAllCommitments(commitments);
        } catch {
          // Commitments endpoint may not exist yet
        }
      } finally {
        setLoading(false);
      }
    }
    load();
  }, []);

  // Extract unique people from all entities
  const people = useMemo(() => {
    const names = new Set<string>();
    allActions.forEach((a) => a.owner && names.add(a.owner));
    allCommitments.forEach((c) => c.person && names.add(c.person));
    return Array.from(names).sort();
  }, [allActions, allCommitments]);

  // Filter items for selected person
  const personItems: PersonItems = useMemo(() => {
    if (!selectedPerson) {
      return { actions: allActions, commitments: allCommitments, threads: allThreads };
    }
    return {
      actions: allActions.filter((a) => a.owner === selectedPerson),
      commitments: allCommitments.filter((c) => c.person === selectedPerson),
      threads: allThreads.filter((t) => t.owner === selectedPerson),
    };
  }, [selectedPerson, allActions, allCommitments, allThreads]);

  const overdueActions = personItems.actions.filter(
    (a) => a.due_date && new Date(a.due_date) < new Date(),
  );

  if (loading) {
    return (
      <div className="space-y-6">
        <h2 className="text-xl md:text-2xl font-bold text-gray-900 dark:text-gray-100">What Needs My Attention</h2>
        <div className="animate-pulse space-y-4">
          <div className="h-10 bg-gray-100 rounded w-64" />
          <div className="h-32 bg-gray-100 rounded" />
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex items-start justify-between">
        <div>
          <h2 className="text-xl md:text-2xl font-bold text-gray-900 dark:text-gray-100">
            What Needs My Attention
          </h2>
          <p className="mt-1 text-base text-gray-500">
            Person-centric view of all open items.
          </p>
        </div>
      </div>

      {/* Person selector */}
      <div className="flex items-center gap-3">
        <User className="h-4 w-4 text-gray-400" />
        <select
          value={selectedPerson}
          onChange={(e) => setSelectedPerson(e.target.value)}
          className="rounded-md border border-gray-300 bg-white px-3 py-2 text-base text-gray-700 focus:outline-none focus:ring-1 focus:ring-blue-500"
        >
          <option value="">All People</option>
          {people.map((p) => (
            <option key={p} value={p}>{p}</option>
          ))}
        </select>
        {selectedPerson && (
          <span className="text-base text-gray-500">
            {personItems.actions.length} actions ({overdueActions.length} overdue)
            {personItems.commitments.length > 0 && `, ${personItems.commitments.length} commitments`}
            {personItems.threads.length > 0 && `, ${personItems.threads.length} threads`}
          </span>
        )}
      </div>

      {/* Summary cards */}
      <div className="grid grid-cols-1 gap-4 sm:grid-cols-3">
        <div className="rounded-lg border border-gray-200 bg-white p-4">
          <div className="flex items-center gap-2 mb-2">
            <CheckSquare className="h-4 w-4 text-green-500" />
            <span className="text-base font-semibold text-gray-900">Open Actions</span>
          </div>
          <div className="flex items-baseline gap-2">
            <span className="text-2xl font-bold text-gray-900">
              {personItems.actions.length}
            </span>
            {overdueActions.length > 0 && (
              <span className="text-base font-medium text-red-600">
                ({overdueActions.length} overdue)
              </span>
            )}
          </div>
        </div>

        <div className="rounded-lg border border-gray-200 bg-white p-4">
          <div className="flex items-center gap-2 mb-2">
            <Handshake className="h-4 w-4 text-amber-500" />
            <span className="text-base font-semibold text-gray-900">Pending Commitments</span>
          </div>
          <span className="text-2xl font-bold text-gray-900">
            {personItems.commitments.length}
          </span>
        </div>

        <div className="rounded-lg border border-gray-200 bg-white p-4">
          <div className="flex items-center gap-2 mb-2">
            <AlertCircle className="h-4 w-4 text-red-500" />
            <span className="text-base font-semibold text-gray-900">Owned Threads</span>
          </div>
          <span className="text-2xl font-bold text-gray-900">
            {personItems.threads.length}
          </span>
        </div>
      </div>

      {/* Action items */}
      {personItems.actions.length > 0 && (
        <section>
          <h3 className="text-sm font-semibold text-gray-500 uppercase tracking-wider mb-3">
            Open Actions
          </h3>
          <div className="rounded-lg border border-gray-200 bg-white divide-y divide-gray-100">
            {personItems.actions.map((action) => {
              const isOverdue = action.due_date && new Date(action.due_date) < new Date();
              return (
                <div key={action.id} className="flex items-start gap-3 px-4 py-3">
                  <CheckSquare
                    className={`h-4 w-4 mt-0.5 flex-shrink-0 ${isOverdue ? "text-red-500" : "text-gray-400"}`}
                  />
                  <div className="flex-1 min-w-0">
                    <p className="text-base text-gray-900">
                      {action.title || action.description}
                    </p>
                    <div className="flex items-center gap-2 mt-0.5">
                      {action.owner && (
                        <span className="text-sm text-gray-500">{action.owner}</span>
                      )}
                      {action.due_date && (
                        <span className={`text-sm ${isOverdue ? "text-red-600 font-medium" : "text-gray-400"}`}>
                          <Clock className="inline h-3 w-3 mr-0.5" />
                          {formatDate(action.due_date)}
                        </span>
                      )}
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        </section>
      )}

      {/* Commitments */}
      {personItems.commitments.length > 0 && (
        <section>
          <h3 className="text-sm font-semibold text-gray-500 uppercase tracking-wider mb-3">
            Pending Commitments
          </h3>
          <div className="rounded-lg border border-gray-200 bg-white divide-y divide-gray-100">
            {personItems.commitments.map((c) => (
              <div key={c.id} className="flex items-start gap-3 px-4 py-3">
                <Handshake className="h-4 w-4 mt-0.5 text-amber-500 flex-shrink-0" />
                <div className="flex-1 min-w-0">
                  <p className="text-base text-gray-900">{c.commitment}</p>
                  <div className="flex items-center gap-2 mt-0.5">
                    <span className="text-sm text-gray-500">{c.person}</span>
                    {c.deadline_text && (
                      <span className="text-sm text-gray-400">{c.deadline_text}</span>
                    )}
                    {c.condition && (
                      <span className="text-[10px] text-gray-400 italic">
                        if: {c.condition}
                      </span>
                    )}
                  </div>
                </div>
                <span
                  className={`text-[10px] font-medium px-1.5 py-0.5 rounded-full ${
                    c.status === "pending"
                      ? "bg-amber-100 text-amber-700"
                      : c.status === "broken"
                        ? "bg-red-100 text-red-700"
                        : "bg-gray-100 text-gray-600"
                  }`}
                >
                  {c.status}
                </span>
              </div>
            ))}
          </div>
        </section>
      )}

      {/* Threads */}
      {personItems.threads.length > 0 && (
        <section>
          <h3 className="text-sm font-semibold text-gray-500 uppercase tracking-wider mb-3">
            Owned Threads
          </h3>
          <div className="rounded-lg border border-gray-200 bg-white divide-y divide-gray-100">
            {personItems.threads.map((t) => (
              <div key={t.id} className="flex items-start gap-3 px-4 py-3">
                <AlertCircle className="h-4 w-4 mt-0.5 text-red-500 flex-shrink-0" />
                <div className="flex-1 min-w-0">
                  <p className="text-base font-medium text-gray-900">{t.title}</p>
                  {t.description && (
                    <p className="text-sm text-gray-500 mt-0.5 truncate">
                      {t.description}
                    </p>
                  )}
                </div>
                {t.severity && (
                  <span
                    className={`text-[10px] font-medium px-1.5 py-0.5 rounded-full ${
                      t.severity === "CRITICAL"
                        ? "bg-red-100 text-red-700"
                        : t.severity === "HIGH"
                          ? "bg-orange-100 text-orange-700"
                          : "bg-gray-100 text-gray-600"
                    }`}
                  >
                    {t.severity}
                  </span>
                )}
              </div>
            ))}
          </div>
        </section>
      )}

      {personItems.actions.length === 0 &&
        personItems.commitments.length === 0 &&
        personItems.threads.length === 0 && (
          <div className="rounded-lg border border-gray-200 bg-gray-50 p-8 text-center">
            <p className="text-base text-gray-500">
              {selectedPerson
                ? `No open items found for ${selectedPerson}.`
                : "No open items found."}
            </p>
          </div>
        )}
    </div>
  );
}
