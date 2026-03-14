"use client";

import { X } from "lucide-react";
import type { InfluenceGraphData } from "@/lib/types";

interface PersonInfluenceCardProps {
  personId: string;
  data: InfluenceGraphData;
  onClose: () => void;
}

export default function PersonInfluenceCard({
  personId,
  data,
  onClose,
}: PersonInfluenceCardProps) {
  const node = data.nodes.find((n) => n.id === personId);
  if (!node) return null;

  const outgoing = data.edges.filter((e) => e.source === personId);
  const incoming = data.edges.filter((e) => e.target === personId);

  const getNodeName = (id: string) => {
    const n = data.nodes.find((node) => node.id === id);
    return n?.name || id;
  };

  const typeColors: Record<string, string> = {
    support: "text-green-600 bg-green-50 dark:bg-green-900/30 dark:text-green-400",
    opposition: "text-red-600 bg-red-50 dark:bg-red-900/30 dark:text-red-400",
    bridging: "text-blue-600 bg-blue-50 dark:bg-blue-900/30 dark:text-blue-400",
    influence: "text-purple-600 bg-purple-50 dark:bg-purple-900/30 dark:text-purple-400",
    delegation: "text-amber-600 bg-amber-50 dark:bg-amber-900/30 dark:text-amber-400",
  };

  return (
    <div className="border rounded-lg bg-white dark:bg-gray-800 dark:border-gray-700 p-4 space-y-4">
      <div className="flex items-center justify-between">
        <h3 className="text-lg font-semibold">{node.name}</h3>
        <button
          onClick={onClose}
          className="p-1 hover:bg-gray-100 dark:hover:bg-gray-700 rounded"
        >
          <X className="w-4 h-4" />
        </button>
      </div>

      <div className="text-base text-gray-500 dark:text-gray-400">
        {node.signal_count} total signal{node.signal_count !== 1 ? "s" : ""}
      </div>

      {/* Outgoing influences */}
      {outgoing.length > 0 && (
        <div>
          <h4 className="text-base font-medium mb-2 text-gray-700 dark:text-gray-300">
            Influencing ({outgoing.length})
          </h4>
          <div className="space-y-1.5">
            {outgoing.map((edge, i) => (
              <div
                key={`out-${i}`}
                className="flex items-center gap-2 text-base"
              >
                <span
                  className={`px-2 py-0.5 rounded text-sm ${
                    typeColors[edge.type] || "bg-gray-100 dark:bg-gray-700"
                  }`}
                >
                  {edge.type}
                </span>
                <span className="text-gray-400">&rarr;</span>
                <span className="font-medium">{getNodeName(edge.target)}</span>
                <span className="text-gray-400 text-sm ml-auto">
                  weight: {edge.weight}
                </span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Incoming influences */}
      {incoming.length > 0 && (
        <div>
          <h4 className="text-base font-medium mb-2 text-gray-700 dark:text-gray-300">
            Influenced by ({incoming.length})
          </h4>
          <div className="space-y-1.5">
            {incoming.map((edge, i) => (
              <div
                key={`in-${i}`}
                className="flex items-center gap-2 text-base"
              >
                <span className="font-medium">{getNodeName(edge.source)}</span>
                <span className="text-gray-400">&rarr;</span>
                <span
                  className={`px-2 py-0.5 rounded text-sm ${
                    typeColors[edge.type] || "bg-gray-100 dark:bg-gray-700"
                  }`}
                >
                  {edge.type}
                </span>
                <span className="text-gray-400 text-sm ml-auto">
                  weight: {edge.weight}
                </span>
              </div>
            ))}
          </div>
        </div>
      )}

      {outgoing.length === 0 && incoming.length === 0 && (
        <p className="text-base text-gray-400">No connections found for this person.</p>
      )}
    </div>
  );
}
