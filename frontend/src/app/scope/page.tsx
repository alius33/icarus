import { api } from "@/lib/api";
import { getStatusColor, formatDate } from "@/lib/utils";
import { Target, PlusCircle, DollarSign, Check, X } from "lucide-react";
import type { ScopeItemSchema } from "@/lib/types";

function ScopeCard({ item }: { item: ScopeItemSchema }) {
  const isAddition = item.scope_type === "addition";
  const statusClasses = getStatusColor(item.status);

  return (
    <div
      className={`rounded-lg border bg-white p-4 ${
        isAddition
          ? "border-l-4 border-l-amber-400 border-t-gray-200 border-r-gray-200 border-b-gray-200"
          : "border-gray-200"
      }`}
    >
      <div className="flex items-start justify-between gap-3">
        <div className="flex items-start gap-3 min-w-0 flex-1">
          {isAddition ? (
            <PlusCircle className="h-5 w-5 text-amber-500 flex-shrink-0 mt-0.5" />
          ) : (
            <Target className="h-5 w-5 text-blue-500 flex-shrink-0 mt-0.5" />
          )}
          <div className="min-w-0 flex-1">
            <h4 className="text-base font-semibold text-gray-900">{item.name}</h4>
            <div className="flex flex-wrap items-center gap-2 mt-1.5">
              {item.workstream && (
                <span className="inline-flex items-center rounded bg-blue-50 px-2 py-0.5 text-[11px] font-medium text-blue-700">
                  {item.workstream}
                </span>
              )}
              <span
                className={`inline-flex items-center rounded border px-2 py-0.5 text-[11px] font-medium ${statusClasses}`}
              >
                {item.status}
              </span>
              {item.estimated_effort && (
                <span className="inline-flex items-center rounded bg-gray-100 px-2 py-0.5 text-[11px] text-gray-600">
                  {item.estimated_effort}
                </span>
              )}
              {item.added_date && (
                <span className="text-[11px] text-gray-400">
                  Added {formatDate(item.added_date)}
                </span>
              )}
            </div>
            {item.description && (
              <p className="mt-2 text-sm text-gray-600 line-clamp-2">
                {item.description}
              </p>
            )}
            {item.impact_notes && (
              <details className="mt-2 group">
                <summary className="text-[11px] font-medium text-amber-700 cursor-pointer hover:text-amber-800">
                  Impact notes
                </summary>
                <p className="mt-1 text-sm text-gray-600 bg-amber-50 rounded p-2 border border-amber-100">
                  {item.impact_notes}
                </p>
              </details>
            )}
          </div>
        </div>
        <div className="flex-shrink-0" title={item.budgeted ? "Budgeted" : "Unbudgeted"}>
          {item.budgeted ? (
            <span className="inline-flex items-center gap-1 rounded-full bg-green-50 px-2 py-1 text-[11px] font-medium text-green-700 border border-green-200">
              <Check className="h-3.5 w-3.5" />
              <DollarSign className="h-3.5 w-3.5" />
            </span>
          ) : (
            <span className="inline-flex items-center gap-1 rounded-full bg-red-50 px-2 py-1 text-[11px] font-medium text-red-600 border border-red-200">
              <X className="h-3.5 w-3.5" />
              <DollarSign className="h-3.5 w-3.5" />
            </span>
          )}
        </div>
      </div>
    </div>
  );
}

export default async function ScopeTrackerPage() {
  let items: ScopeItemSchema[] = [];
  let error: string | null = null;

  try {
    items = await api.getScopeItems();
  } catch (e) {
    error = e instanceof Error ? e.message : "Failed to load scope items";
  }

  const original = items.filter((i) => i.scope_type === "original");
  const additions = items.filter((i) => i.scope_type === "addition");
  const budgetedAdditions = additions.filter((i) => i.budgeted);
  const unbudgetedAdditions = additions.filter((i) => !i.budgeted);

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h2 className="text-2xl font-bold text-gray-900">Scope Creep Tracker</h2>
        <p className="mt-1 text-base text-gray-500">
          Original scope vs. additions across the Gen AI Programme.
        </p>
      </div>

      {/* Error state */}
      {error && (
        <div className="rounded-lg border border-red-200 bg-red-50 p-6">
          <p className="text-base text-red-700">{error}</p>
        </div>
      )}

      {/* Summary Stats */}
      {!error && (
        <div className="grid grid-cols-2 gap-3 sm:grid-cols-4">
          <div className="rounded-lg border border-gray-200 bg-white p-4">
            <div className="flex items-center gap-2 mb-1">
              <Target className="h-4 w-4 text-blue-500" />
              <span className="text-sm font-medium text-gray-500 uppercase tracking-wider">
                Original
              </span>
            </div>
            <p className="text-2xl font-bold text-gray-900">{original.length}</p>
          </div>
          <div className="rounded-lg border border-amber-200 bg-amber-50/30 p-4">
            <div className="flex items-center gap-2 mb-1">
              <PlusCircle className="h-4 w-4 text-amber-500" />
              <span className="text-sm font-medium text-gray-500 uppercase tracking-wider">
                Additions
              </span>
            </div>
            <p className="text-2xl font-bold text-gray-900">{additions.length}</p>
          </div>
          <div className="rounded-lg border border-green-200 bg-green-50/30 p-4">
            <div className="flex items-center gap-2 mb-1">
              <DollarSign className="h-4 w-4 text-green-600" />
              <span className="text-sm font-medium text-gray-500 uppercase tracking-wider">
                Budgeted
              </span>
            </div>
            <p className="text-2xl font-bold text-gray-900">{budgetedAdditions.length}</p>
          </div>
          <div className="rounded-lg border border-red-200 bg-red-50/30 p-4">
            <div className="flex items-center gap-2 mb-1">
              <DollarSign className="h-4 w-4 text-red-500" />
              <span className="text-sm font-medium text-gray-500 uppercase tracking-wider">
                Unbudgeted
              </span>
            </div>
            <p className="text-2xl font-bold text-gray-900">{unbudgetedAdditions.length}</p>
          </div>
        </div>
      )}

      {/* Original Scope Section */}
      {!error && original.length > 0 && (
        <section>
          <h3 className="text-sm font-semibold text-gray-500 uppercase tracking-wider mb-3 flex items-center gap-1.5">
            <Target className="h-3.5 w-3.5 text-blue-500" />
            Original Scope ({original.length})
          </h3>
          <div className="space-y-3">
            {original.map((item) => (
              <ScopeCard key={item.id} item={item} />
            ))}
          </div>
        </section>
      )}

      {/* Additions Section */}
      {!error && additions.length > 0 && (
        <section>
          <h3 className="text-sm font-semibold text-amber-600 uppercase tracking-wider mb-3 flex items-center gap-1.5">
            <PlusCircle className="h-3.5 w-3.5 text-amber-500" />
            Additions ({additions.length})
          </h3>
          <div className="space-y-3">
            {additions.map((item) => (
              <ScopeCard key={item.id} item={item} />
            ))}
          </div>
        </section>
      )}

      {/* Empty state */}
      {!error && items.length === 0 && (
        <div className="rounded-lg border border-gray-200 bg-white p-12 text-center">
          <Target className="h-10 w-10 text-gray-600 dark:text-gray-300 mx-auto mb-3" />
          <p className="text-base text-gray-500">No scope items recorded yet.</p>
        </div>
      )}
    </div>
  );
}
