"use client";

import { useMemo, useState } from "react";
import type { InfluenceGraphData, InfluenceGraphNode } from "@/lib/types";

interface InfluenceNetworkProps {
  data: InfluenceGraphData;
  onSelectNode: (nodeId: string | null) => void;
  selectedNode: string | null;
}

interface PositionedNode extends InfluenceGraphNode {
  x: number;
  y: number;
}

const EDGE_COLORS: Record<string, string> = {
  support: "#22c55e",
  opposition: "#ef4444",
  bridging: "#3b82f6",
  influence: "#8b5cf6",
  delegation: "#f59e0b",
  default: "#9ca3af",
};

export default function InfluenceNetwork({
  data,
  onSelectNode,
  selectedNode,
}: InfluenceNetworkProps) {
  const [hoveredNode, setHoveredNode] = useState<string | null>(null);

  const width = 800;
  const height = 500;
  const padding = 60;

  const positionedNodes = useMemo<PositionedNode[]>(() => {
    if (!data.nodes.length) return [];

    const count = data.nodes.length;
    const centerX = width / 2;
    const centerY = height / 2;
    const radiusX = (width - padding * 2) / 2.5;
    const radiusY = (height - padding * 2) / 2.5;

    // Arrange nodes in an ellipse
    return data.nodes.map((node, i) => {
      const angle = (2 * Math.PI * i) / count - Math.PI / 2;
      return {
        ...node,
        x: centerX + radiusX * Math.cos(angle),
        y: centerY + radiusY * Math.sin(angle),
      };
    });
  }, [data.nodes]);

  const nodeMap = useMemo(() => {
    const map = new Map<string, PositionedNode>();
    positionedNodes.forEach((n) => map.set(n.id, n));
    return map;
  }, [positionedNodes]);

  const getNodeRadius = (signalCount: number) => {
    return Math.max(18, Math.min(35, 12 + signalCount * 3));
  };

  if (!data.nodes.length) {
    return (
      <div className="flex items-center justify-center h-96 text-gray-400">
        No influence data available yet.
      </div>
    );
  }

  return (
    <div className="border rounded-lg bg-white dark:bg-gray-800 dark:border-gray-700 overflow-hidden">
      <svg
        viewBox={`0 0 ${width} ${height}`}
        className="w-full h-auto"
        style={{ minHeight: 400 }}
      >
        {/* Edges */}
        {data.edges.map((edge, i) => {
          const source = nodeMap.get(edge.source);
          const target = nodeMap.get(edge.target);
          if (!source || !target) return null;

          const color = EDGE_COLORS[edge.type] || EDGE_COLORS.default;
          const opacity =
            hoveredNode && hoveredNode !== edge.source && hoveredNode !== edge.target
              ? 0.15
              : 0.6;
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
              opacity={opacity}
              strokeDasharray={edge.type === "opposition" ? "6,3" : undefined}
            />
          );
        })}

        {/* Nodes */}
        {positionedNodes.map((node) => {
          const radius = getNodeRadius(node.signal_count);
          const isSelected = selectedNode === node.id;
          const isHovered = hoveredNode === node.id;
          const dimmed =
            hoveredNode !== null && hoveredNode !== node.id;

          return (
            <g
              key={node.id}
              className="cursor-pointer"
              onClick={() => onSelectNode(isSelected ? null : node.id)}
              onMouseEnter={() => setHoveredNode(node.id)}
              onMouseLeave={() => setHoveredNode(null)}
              opacity={dimmed ? 0.4 : 1}
            >
              <circle
                cx={node.x}
                cy={node.y}
                r={radius}
                fill={isSelected ? "#3b82f6" : isHovered ? "#60a5fa" : "#1e293b"}
                stroke={isSelected ? "#1d4ed8" : "#475569"}
                strokeWidth={isSelected ? 3 : 1.5}
              />
              <text
                x={node.x}
                y={node.y - radius - 6}
                textAnchor="middle"
                className="text-xs font-medium"
                fill="currentColor"
              >
                {node.name}
              </text>
              <text
                x={node.x}
                y={node.y + 4}
                textAnchor="middle"
                className="text-[10px]"
                fill="white"
              >
                {node.signal_count}
              </text>
            </g>
          );
        })}
      </svg>

      {/* Legend */}
      <div className="flex gap-4 px-4 py-2 border-t dark:border-gray-700 text-xs text-gray-500 dark:text-gray-400">
        {Object.entries(EDGE_COLORS)
          .filter(([k]) => k !== "default")
          .map(([type, color]) => (
            <div key={type} className="flex items-center gap-1.5">
              <div
                className="w-4 h-0.5"
                style={{
                  backgroundColor: color,
                  borderTop: type === "opposition" ? "2px dashed" : undefined,
                  borderColor: type === "opposition" ? color : undefined,
                }}
              />
              <span className="capitalize">{type}</span>
            </div>
          ))}
      </div>
    </div>
  );
}
