"use client";

import { useState, useMemo, useEffect } from "react";
import { useInfluenceGraph } from "@/lib/swr";
import { api } from "@/lib/api";
import { Users } from "lucide-react";
import type { InfluenceGraphData, InfluenceGraphNode, InfluenceGraphEdge, InfluenceSignalSchema } from "@/lib/types";

// ── Colours & constants ────────────────────────────────────────────────────────

const POSITIVE_TYPES = new Set(["proposal_adopted", "bridging", "support", "delegation", "influence"]);
const NEGATIVE_TYPES = new Set(["blocked", "interrupted", "opposition"]);

function edgeColor(type: string): string {
  if (POSITIVE_TYPES.has(type)) return "#22c55e";
  if (NEGATIVE_TYPES.has(type)) return "#ef4444";
  return "#3b82f6";
}

function nodeColor(signalCount: number, maxSignals: number): string {
  if (maxSignals === 0) return "#3b82f6";
  const ratio = signalCount / maxSignals;
  // Interpolate from light blue (#93c5fd) to dark blue (#1e3a8a)
  const r = Math.round(147 - ratio * (147 - 30));
  const g = Math.round(197 - ratio * (197 - 58));
  const b = Math.round(253 - ratio * (253 - 138));
  return `rgb(${r},${g},${b})`;
}

// ── Force-directed layout ──────────────────────────────────────────────────────

interface PositionedNode extends InfluenceGraphNode {
  x: number;
  y: number;
  vx: number;
  vy: number;
}

function computeLayout(
  nodes: InfluenceGraphNode[],
  edges: InfluenceGraphEdge[],
  width: number,
  height: number,
): PositionedNode[] {
  if (nodes.length === 0) return [];

  const padding = 70;
  const centerX = width / 2;
  const centerY = height / 2;

  // Initialize positions in a circle
  const positioned: PositionedNode[] = nodes.map((n, i) => {
    const angle = (2 * Math.PI * i) / nodes.length - Math.PI / 2;
    const rx = (width - padding * 2) / 3;
    const ry = (height - padding * 2) / 3;
    return {
      ...n,
      x: centerX + rx * Math.cos(angle),
      y: centerY + ry * Math.sin(angle),
      vx: 0,
      vy: 0,
    };
  });

  const nodeIndex = new Map<string, number>();
  positioned.forEach((n, i) => nodeIndex.set(n.id, i));

  // Simple force-directed simulation: run a fixed number of iterations
  const iterations = 80;
  const repulsion = 5000;
  const attraction = 0.005;
  const damping = 0.85;

  for (let iter = 0; iter < iterations; iter++) {
    const cooling = 1 - iter / iterations;

    // Repulsion between all node pairs
    for (let i = 0; i < positioned.length; i++) {
      for (let j = i + 1; j < positioned.length; j++) {
        const dx = positioned[i].x - positioned[j].x;
        const dy = positioned[i].y - positioned[j].y;
        const distSq = Math.max(dx * dx + dy * dy, 1);
        const force = (repulsion * cooling) / distSq;
        const fx = dx * force;
        const fy = dy * force;
        positioned[i].vx += fx;
        positioned[i].vy += fy;
        positioned[j].vx -= fx;
        positioned[j].vy -= fy;
      }
    }

    // Attraction along edges
    for (const edge of edges) {
      const si = nodeIndex.get(edge.source);
      const ti = nodeIndex.get(edge.target);
      if (si === undefined || ti === undefined) continue;
      const dx = positioned[ti].x - positioned[si].x;
      const dy = positioned[ti].y - positioned[si].y;
      const force = attraction * cooling;
      positioned[si].vx += dx * force;
      positioned[si].vy += dy * force;
      positioned[ti].vx -= dx * force;
      positioned[ti].vy -= dy * force;
    }

    // Center gravity
    for (const n of positioned) {
      n.vx += (centerX - n.x) * 0.001 * cooling;
      n.vy += (centerY - n.y) * 0.001 * cooling;
    }

    // Apply velocities
    for (const n of positioned) {
      n.vx *= damping;
      n.vy *= damping;
      n.x += n.vx;
      n.y += n.vy;
      // Clamp to bounds
      n.x = Math.max(padding, Math.min(width - padding, n.x));
      n.y = Math.max(padding, Math.min(height - padding, n.y));
    }
  }

  return positioned;
}

// ── Strength badge ─────────────────────────────────────────────────────────────

function StrengthBadge({ strength }: { strength: string | null }) {
  const colors: Record<string, string> = {
    STRONG: "bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400",
    MODERATE: "bg-yellow-100 text-yellow-700 dark:bg-yellow-900/30 dark:text-yellow-400",
    WEAK: "bg-gray-100 text-gray-600 dark:bg-gray-700 dark:text-gray-300",
  };
  if (!strength) return <span className="text-gray-400 text-sm">--</span>;
  return (
    <span className={`px-2 py-0.5 rounded-full text-sm ${colors[strength] || "bg-gray-100 dark:bg-gray-700"}`}>
      {strength}
    </span>
  );
}

function ConfidenceBadge({ confidence }: { confidence: string | null }) {
  const colors: Record<string, string> = {
    HIGH: "text-green-600 dark:text-green-400",
    MEDIUM: "text-amber-600 dark:text-amber-400",
    LOW: "text-red-500 dark:text-red-400",
  };
  if (!confidence) return null;
  return <span className={`text-sm font-medium ${colors[confidence] || ""}`}>{confidence}</span>;
}

// ── Main page ──────────────────────────────────────────────────────────────────

export default function InfluenceGraphPage() {
  const { data, isLoading: loadingGraph } = useInfluenceGraph();
  const [signals, setSignals] = useState<InfluenceSignalSchema[]>([]);
  const [loadingSignals, setLoadingSignals] = useState(true);
  const [selectedNode, setSelectedNode] = useState<string | null>(null);
  const [hoveredNode, setHoveredNode] = useState<string | null>(null);

  useEffect(() => {
    api
      .getInfluenceSignals()
      .then(setSignals)
      .catch(console.error)
      .finally(() => setLoadingSignals(false));
  }, []);

  const isLoading = loadingGraph || loadingSignals;

  // SVG layout
  const svgWidth = 900;
  const svgHeight = 550;

  const positionedNodes = useMemo(() => {
    if (!data || data.nodes.length === 0) return [];
    return computeLayout(data.nodes, data.edges, svgWidth, svgHeight);
  }, [data]);

  const nodeMap = useMemo(() => {
    const map = new Map<string, PositionedNode>();
    positionedNodes.forEach((n) => map.set(n.id, n));
    return map;
  }, [positionedNodes]);

  const maxSignals = useMemo(() => {
    if (!data) return 0;
    return Math.max(1, ...data.nodes.map((n) => n.signal_count));
  }, [data]);

  // Sorted signals (newest first)
  const sortedSignals = useMemo(() => {
    return [...signals].sort((a, b) => {
      if (!a.date && !b.date) return 0;
      if (!a.date) return 1;
      if (!b.date) return -1;
      return b.date.localeCompare(a.date);
    });
  }, [signals]);

  // Loading state
  if (isLoading) {
    return (
      <div className="space-y-6">
        <div>
          <h1 className="text-2xl font-bold text-gray-900 dark:text-gray-100">Influence Map</h1>
          <p className="text-base text-gray-500 dark:text-gray-400 mt-1">
            Visualise stakeholder influence patterns, coalitions, and power dynamics
          </p>
        </div>
        <div className="h-[550px] bg-gray-200 dark:bg-gray-700 rounded-lg animate-pulse" />
        <div className="h-64 bg-gray-200 dark:bg-gray-700 rounded-lg animate-pulse" />
      </div>
    );
  }

  const hasGraphData = data && data.nodes.length > 0;

  if (!hasGraphData && signals.length === 0) {
    return (
      <div className="space-y-6">
        <div>
          <h1 className="text-2xl font-bold text-gray-900 dark:text-gray-100">Influence Map</h1>
          <p className="text-base text-gray-500 dark:text-gray-400 mt-1">
            Visualise stakeholder influence patterns, coalitions, and power dynamics
          </p>
        </div>
        <div className="text-center py-16">
          <Users className="h-12 w-12 mx-auto text-gray-600 dark:text-gray-300 dark:text-gray-600 mb-4" />
          <p className="text-gray-500 dark:text-gray-400">
            No data yet. Run <code className="px-1.5 py-0.5 bg-gray-100 dark:bg-gray-700 rounded text-base">/analyse-deep</code> to populate.
          </p>
        </div>
      </div>
    );
  }

  const getNodeRadius = (signalCount: number) => Math.max(18, Math.min(38, 14 + signalCount * 3));

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-900 dark:text-gray-100">Influence Map</h1>
        <p className="text-base text-gray-500 dark:text-gray-400 mt-1">
          Visualise stakeholder influence patterns, coalitions, and power dynamics
        </p>
      </div>

      {/* Summary stats */}
      {hasGraphData && (
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <StatCard label="People" value={data.nodes.length} />
          <StatCard label="Connections" value={data.edges.length} />
          <StatCard
            label="Positive links"
            value={data.edges.filter((e) => POSITIVE_TYPES.has(e.type)).length}
            color="text-green-600"
          />
          <StatCard
            label="Negative links"
            value={data.edges.filter((e) => NEGATIVE_TYPES.has(e.type)).length}
            color="text-red-600"
          />
        </div>
      )}

      {/* Network Graph */}
      {hasGraphData && (
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow border border-gray-200 dark:border-gray-700 overflow-hidden">
          <div className="px-4 py-3 border-b border-gray-200 dark:border-gray-700">
            <h2 className="text-lg font-semibold text-gray-900 dark:text-gray-100">Network Graph</h2>
            <p className="text-sm text-gray-500 dark:text-gray-400">
              Click a node to highlight. Node size reflects signal count.
            </p>
          </div>
          <svg
            viewBox={`0 0 ${svgWidth} ${svgHeight}`}
            className="w-full h-auto"
            style={{ minHeight: 400, maxHeight: 600 }}
          >
            {/* Edges */}
            {data.edges.map((edge, i) => {
              const source = nodeMap.get(edge.source);
              const target = nodeMap.get(edge.target);
              if (!source || !target) return null;

              const color = edgeColor(edge.type);
              const isConnected =
                (hoveredNode && (hoveredNode === edge.source || hoveredNode === edge.target)) ||
                (selectedNode && (selectedNode === edge.source || selectedNode === edge.target));
              const dimmed = (hoveredNode || selectedNode) && !isConnected;
              const strokeWidth = Math.max(1, Math.min(4, edge.weight));

              return (
                <line
                  key={`edge-${i}`}
                  x1={source.x}
                  y1={source.y}
                  x2={target.x}
                  y2={target.y}
                  stroke={color}
                  strokeWidth={strokeWidth}
                  opacity={dimmed ? 0.1 : 0.7}
                  strokeDasharray={NEGATIVE_TYPES.has(edge.type) ? "6,3" : undefined}
                />
              );
            })}

            {/* Nodes */}
            {positionedNodes.map((node) => {
              const radius = getNodeRadius(node.signal_count);
              const isSelected = selectedNode === node.id;
              const isHovered = hoveredNode === node.id;
              const anyActive = hoveredNode || selectedNode;
              const isConnected =
                anyActive &&
                data.edges.some(
                  (e) =>
                    ((e.source === node.id || e.target === node.id) &&
                      (e.source === (hoveredNode || selectedNode) || e.target === (hoveredNode || selectedNode)))
                );
              const dimmed = anyActive && !isSelected && !isHovered && !isConnected;

              const fill = isSelected
                ? "#3b82f6"
                : isHovered
                  ? "#60a5fa"
                  : nodeColor(node.signal_count, maxSignals);

              return (
                <g
                  key={node.id}
                  className="cursor-pointer"
                  onClick={() => setSelectedNode(isSelected ? null : node.id)}
                  onMouseEnter={() => setHoveredNode(node.id)}
                  onMouseLeave={() => setHoveredNode(null)}
                  opacity={dimmed ? 0.3 : 1}
                >
                  {isSelected && (
                    <circle
                      cx={node.x}
                      cy={node.y}
                      r={radius + 4}
                      fill="none"
                      stroke="#3b82f6"
                      strokeWidth={2}
                      strokeDasharray="4,2"
                    />
                  )}
                  <circle
                    cx={node.x}
                    cy={node.y}
                    r={radius}
                    fill={fill}
                    stroke={isSelected ? "#1d4ed8" : "#475569"}
                    strokeWidth={isSelected ? 2.5 : 1.5}
                  />
                  <text
                    x={node.x}
                    y={node.y - radius - 8}
                    textAnchor="middle"
                    className="text-sm font-medium"
                    fill="currentColor"
                  >
                    {node.name}
                  </text>
                  <text
                    x={node.x}
                    y={node.y + 4}
                    textAnchor="middle"
                    className="text-[10px] font-bold"
                    fill="white"
                  >
                    {node.signal_count}
                  </text>
                </g>
              );
            })}
          </svg>

          {/* Legend */}
          <div className="flex gap-5 px-4 py-2.5 border-t dark:border-gray-700 text-sm text-gray-500 dark:text-gray-400 flex-wrap">
            <div className="flex items-center gap-1.5">
              <span className="inline-block w-4 h-0.5 bg-green-500 rounded" />
              Positive (support, bridging)
            </div>
            <div className="flex items-center gap-1.5">
              <span className="inline-block w-4 h-0.5 bg-red-500 rounded" style={{ borderTop: "2px dashed #ef4444" }} />
              Negative (blocked, opposition)
            </div>
            <div className="flex items-center gap-1.5">
              <span className="inline-block w-4 h-0.5 bg-blue-500 rounded" />
              Neutral
            </div>
          </div>
        </div>
      )}

      {/* Selected node detail */}
      {selectedNode && hasGraphData && (
        <SelectedNodeDetail
          nodeId={selectedNode}
          data={data}
          onClose={() => setSelectedNode(null)}
        />
      )}

      {/* Influence Signals Table */}
      {sortedSignals.length > 0 && (
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow border border-gray-200 dark:border-gray-700">
          <div className="px-4 py-3 border-b border-gray-200 dark:border-gray-700">
            <h2 className="text-lg font-semibold text-gray-900 dark:text-gray-100">
              Influence Signals
              <span className="ml-2 text-base font-normal text-gray-500 dark:text-gray-400">
                ({sortedSignals.length})
              </span>
            </h2>
          </div>
          <div className="overflow-x-auto">
            <table className="w-full text-base">
              <thead>
                <tr className="border-b border-gray-200 dark:border-gray-700 text-left text-gray-500 dark:text-gray-400">
                  <th className="px-4 py-2.5 font-medium">Date</th>
                  <th className="px-4 py-2.5 font-medium">Person</th>
                  <th className="px-4 py-2.5 font-medium">Type</th>
                  <th className="px-4 py-2.5 font-medium">Direction</th>
                  <th className="px-4 py-2.5 font-medium">Target</th>
                  <th className="px-4 py-2.5 font-medium">Topic</th>
                  <th className="px-4 py-2.5 font-medium">Strength</th>
                  <th className="px-4 py-2.5 font-medium">Confidence</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-100 dark:divide-gray-700">
                {sortedSignals.map((s) => (
                  <tr
                    key={s.id}
                    className="hover:bg-gray-50 dark:hover:bg-gray-700/50 transition-colors"
                  >
                    <td className="px-4 py-2.5 text-gray-600 dark:text-gray-300 whitespace-nowrap">
                      {s.date || "\u2014"}
                    </td>
                    <td className="px-4 py-2.5 font-medium text-gray-900 dark:text-gray-100">
                      {s.person}
                    </td>
                    <td className="px-4 py-2.5">
                      <span
                        className={`inline-block px-2 py-0.5 rounded text-sm font-medium ${
                          POSITIVE_TYPES.has(s.influence_type)
                            ? "bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400"
                            : NEGATIVE_TYPES.has(s.influence_type)
                              ? "bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-400"
                              : "bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-400"
                        }`}
                      >
                        {s.influence_type}
                      </span>
                    </td>
                    <td className="px-4 py-2.5 text-gray-600 dark:text-gray-300">
                      {s.direction || "\u2014"}
                    </td>
                    <td className="px-4 py-2.5 text-gray-600 dark:text-gray-300">
                      {s.target_person || "\u2014"}
                    </td>
                    <td className="px-4 py-2.5 text-gray-600 dark:text-gray-300 max-w-[200px] truncate">
                      {s.topic || "\u2014"}
                    </td>
                    <td className="px-4 py-2.5">
                      <StrengthBadge strength={s.strength} />
                    </td>
                    <td className="px-4 py-2.5">
                      <ConfidenceBadge confidence={s.confidence} />
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
}

// ── Sub-components ─────────────────────────────────────────────────────────────

function StatCard({ label, value, color }: { label: string; value: number; color?: string }) {
  return (
    <div className="border rounded-lg p-4 bg-white dark:bg-gray-800 dark:border-gray-700">
      <p className="text-base text-gray-500 dark:text-gray-400">{label}</p>
      <p className={`text-2xl font-bold mt-1 ${color || "text-gray-900 dark:text-gray-100"}`}>
        {value}
      </p>
    </div>
  );
}

function SelectedNodeDetail({
  nodeId,
  data,
  onClose,
}: {
  nodeId: string;
  data: InfluenceGraphData;
  onClose: () => void;
}) {
  const node = data.nodes.find((n) => n.id === nodeId);
  if (!node) return null;

  const outgoing = data.edges.filter((e) => e.source === nodeId);
  const incoming = data.edges.filter((e) => e.target === nodeId);
  const getNodeName = (id: string) => data.nodes.find((n) => n.id === id)?.name || id;

  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow border border-gray-200 dark:border-gray-700 p-5">
      <div className="flex items-center justify-between mb-4">
        <div>
          <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100">{node.name}</h3>
          <p className="text-base text-gray-500 dark:text-gray-400">
            {node.signal_count} signals | {outgoing.length} outgoing | {incoming.length} incoming
          </p>
        </div>
        <button
          onClick={onClose}
          className="text-gray-400 hover:text-gray-600 dark:hover:text-gray-200 text-base"
        >
          Close
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {outgoing.length > 0 && (
          <div>
            <h4 className="text-base font-medium text-gray-700 dark:text-gray-300 mb-2">
              Influencing ({outgoing.length})
            </h4>
            <div className="space-y-1.5">
              {outgoing.map((edge, i) => (
                <div key={`o-${i}`} className="flex items-center gap-2 text-base">
                  <span
                    className={`px-2 py-0.5 rounded text-sm ${
                      POSITIVE_TYPES.has(edge.type)
                        ? "bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400"
                        : NEGATIVE_TYPES.has(edge.type)
                          ? "bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-400"
                          : "bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-400"
                    }`}
                  >
                    {edge.type}
                  </span>
                  <span className="text-gray-400">&rarr;</span>
                  <span className="font-medium text-gray-900 dark:text-gray-100">{getNodeName(edge.target)}</span>
                </div>
              ))}
            </div>
          </div>
        )}
        {incoming.length > 0 && (
          <div>
            <h4 className="text-base font-medium text-gray-700 dark:text-gray-300 mb-2">
              Influenced by ({incoming.length})
            </h4>
            <div className="space-y-1.5">
              {incoming.map((edge, i) => (
                <div key={`i-${i}`} className="flex items-center gap-2 text-base">
                  <span className="font-medium text-gray-900 dark:text-gray-100">{getNodeName(edge.source)}</span>
                  <span className="text-gray-400">&rarr;</span>
                  <span
                    className={`px-2 py-0.5 rounded text-sm ${
                      POSITIVE_TYPES.has(edge.type)
                        ? "bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400"
                        : NEGATIVE_TYPES.has(edge.type)
                          ? "bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-400"
                          : "bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-400"
                    }`}
                  >
                    {edge.type}
                  </span>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
