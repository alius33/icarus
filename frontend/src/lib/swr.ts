"use client";

import useSWR, { SWRConfiguration } from "swr";
import { api } from "./api";
import type {
  DashboardData,
  TranscriptList,
  TranscriptNoteCurrent,
  TranscriptAttachment as TranscriptAttachmentType,
  WorkstreamBase,
  StakeholderBase,
  DecisionSchema,
  ActionItemSchema,
  OpenThreadSchema,
  GlossaryGrouped,
  SummaryBase,
  WeeklyReportBase,
  ProjectBase,
  DependencySchema,
  ResourceAllocationSchema,
  ScopeItemSchema,
  ProgrammeWinSchema,
  OutreachSchema,
  SentimentSignalSchema,
  CommitmentSchema,
  CrossProjectLinkSchema,
  TopicSignalSchema,
  TopicEvolutionData,
  TopicMomentum,
  InfluenceGraphData,
  ContradictionSchema,
  MeetingScoreSchema,
  MeetingScoreTrend,
  RiskEntrySchema,
  ProjectSummarySchema,
  ProgrammeDeliverable,
  DeliverableOverview,
  WeeklyPlan,
  WeeklyPlanFull,
} from "./types";

const defaultConfig: SWRConfiguration = {
  revalidateOnFocus: false,
  dedupingInterval: 10000,
  errorRetryCount: 2,
};

// Dashboard
export function useDashboard(config?: SWRConfiguration) {
  return useSWR<DashboardData>("dashboard", () => api.getDashboard(), {
    ...defaultConfig,
    ...config,
  });
}

// Transcripts
export function useTranscripts(
  page = 1,
  limit = 20,
  config?: SWRConfiguration,
) {
  return useSWR<TranscriptList>(
    ["transcripts", page, limit],
    () => api.getTranscripts(page, limit),
    { ...defaultConfig, ...config },
  );
}

// Workstreams
export function useWorkstreams(config?: SWRConfiguration) {
  return useSWR<WorkstreamBase[]>(
    "workstreams",
    () => api.getWorkstreams(),
    { ...defaultConfig, ...config },
  );
}

// Stakeholders
export function useStakeholders(tier?: number, config?: SWRConfiguration) {
  return useSWR<StakeholderBase[]>(
    tier ? ["stakeholders", tier] : "stakeholders",
    () => api.getStakeholders(tier),
    { ...defaultConfig, ...config },
  );
}

// Decisions
export function useDecisions(config?: SWRConfiguration) {
  return useSWR<DecisionSchema[]>("decisions", () => api.getDecisions(), {
    ...defaultConfig,
    ...config,
  });
}

// Action Items
export function useActionItems(
  status?: string,
  owner?: string,
  config?: SWRConfiguration,
) {
  return useSWR<ActionItemSchema[]>(
    ["action-items", status, owner],
    () => api.getActionItems(status, owner),
    { ...defaultConfig, ...config },
  );
}

// Open Threads
export function useOpenThreads(status?: string, config?: SWRConfiguration) {
  return useSWR<OpenThreadSchema[]>(
    status ? ["open-threads", status] : "open-threads",
    () => api.getOpenThreads(status ? { status } : undefined),
    { ...defaultConfig, ...config },
  );
}

// Glossary
export function useGlossary(config?: SWRConfiguration) {
  return useSWR<GlossaryGrouped>("glossary", () => api.getGlossary(), {
    ...defaultConfig,
    ...config,
  });
}

// Summaries
export function useSummaries(config?: SWRConfiguration) {
  return useSWR<SummaryBase[]>("summaries", () => api.getSummaries(), {
    ...defaultConfig,
    ...config,
  });
}

// Weekly Reports
export function useWeeklyReports(config?: SWRConfiguration) {
  return useSWR<WeeklyReportBase[]>(
    "weekly-reports",
    () => api.getWeeklyReports(),
    { ...defaultConfig, ...config },
  );
}

// Projects
export function useProjects(config?: SWRConfiguration) {
  return useSWR<ProjectBase[]>("projects", () => api.getProjects(), {
    ...defaultConfig,
    ...config,
  });
}

// Dependencies
export function useDependencies(config?: SWRConfiguration) {
  return useSWR<DependencySchema[]>(
    "dependencies",
    () => api.getDependencies(),
    { ...defaultConfig, ...config },
  );
}

// Resources
export function useResources(config?: SWRConfiguration) {
  return useSWR<ResourceAllocationSchema[]>(
    "resources",
    () => api.getResources(),
    { ...defaultConfig, ...config },
  );
}

// Scope Items
export function useScopeItems(config?: SWRConfiguration) {
  return useSWR<ScopeItemSchema[]>("scope", () => api.getScopeItems(), {
    ...defaultConfig,
    ...config,
  });
}

// Programme Wins
export function useWins(config?: SWRConfiguration) {
  return useSWR<ProgrammeWinSchema[]>("wins", () => api.getWins(), {
    ...defaultConfig,
    ...config,
  });
}

// Outreach
export function useOutreach(status?: string, config?: SWRConfiguration) {
  return useSWR<OutreachSchema[]>(
    status ? ["outreach", status] : "outreach",
    () => api.getOutreach(status),
    { ...defaultConfig, ...config },
  );
}

// Sentiments
export function useSentiments(
  stakeholderId?: number,
  config?: SWRConfiguration,
) {
  return useSWR<SentimentSignalSchema[]>(
    stakeholderId ? ["sentiments", stakeholderId] : "sentiments",
    () => api.getSentiments(stakeholderId),
    { ...defaultConfig, ...config },
  );
}

// Commitments
export function useCommitments(
  status?: string,
  person?: string,
  config?: SWRConfiguration,
) {
  return useSWR<CommitmentSchema[]>(
    ["commitments", status, person],
    () => api.getCommitments(status, person),
    { ...defaultConfig, ...config },
  );
}

// Cross-Project Links
export function useCrossProjectLinks(
  projectId?: number,
  config?: SWRConfiguration,
) {
  return useSWR<CrossProjectLinkSchema[]>(
    projectId ? ["cross-project-links", projectId] : "cross-project-links",
    () => api.getCrossProjectLinks(projectId),
    { ...defaultConfig, ...config },
  );
}

// Topic Signals
export function useTopicSignals(category?: string, config?: SWRConfiguration) {
  return useSWR<TopicSignalSchema[]>(
    category ? ["topic-signals", category] : "topic-signals",
    () => api.getTopicSignals(category),
    { ...defaultConfig, ...config },
  );
}

export function useTopicEvolution(config?: SWRConfiguration) {
  return useSWR<TopicEvolutionData[]>(
    "topic-evolution",
    () => api.getTopicEvolution(),
    { ...defaultConfig, ...config },
  );
}

export function useTopicMomentum(config?: SWRConfiguration) {
  return useSWR<TopicMomentum>(
    "topic-momentum",
    () => api.getTopicMomentum(),
    { ...defaultConfig, ...config },
  );
}

// Influence Graph
export function useInfluenceGraph(config?: SWRConfiguration) {
  return useSWR<InfluenceGraphData>(
    "influence-graph",
    () => api.getInfluenceGraph(),
    { ...defaultConfig, ...config },
  );
}

// Contradictions
export function useContradictions(kind?: string, config?: SWRConfiguration) {
  return useSWR<ContradictionSchema[]>(
    kind ? ["contradictions", kind] : "contradictions",
    () => api.getContradictions(kind),
    { ...defaultConfig, ...config },
  );
}

// Meeting Scores
export function useMeetingScores(config?: SWRConfiguration) {
  return useSWR<MeetingScoreSchema[]>(
    "meeting-scores",
    () => api.getMeetingScores(),
    { ...defaultConfig, ...config },
  );
}

export function useMeetingScoreTrend(config?: SWRConfiguration) {
  return useSWR<MeetingScoreTrend[]>(
    "meeting-score-trend",
    () => api.getMeetingScoreTrend(),
    { ...defaultConfig, ...config },
  );
}

// Risk Entries
export function useRiskEntries(severity?: string, config?: SWRConfiguration) {
  return useSWR<RiskEntrySchema[]>(
    severity ? ["risk-entries", severity] : "risk-entries",
    () => api.getRiskEntries(severity),
    { ...defaultConfig, ...config },
  );
}

// Transcript Notes
export function useTranscriptNotes(id: number, config?: SWRConfiguration) {
  return useSWR<TranscriptNoteCurrent | null>(
    id ? ["transcript-notes", id] : null,
    () => api.getTranscriptNotes(id),
    { ...defaultConfig, ...config },
  );
}

// Transcript Attachments
export function useTranscriptAttachments(id: number, config?: SWRConfiguration) {
  return useSWR<TranscriptAttachmentType[]>(
    id ? ["transcript-attachments", id] : null,
    () => api.getTranscriptAttachments(id),
    { ...defaultConfig, ...config },
  );
}

// Project Summaries
export function useProjectSummaries(
  projectId: number,
  config?: SWRConfiguration,
) {
  return useSWR<ProjectSummarySchema[]>(
    projectId ? ["project-summaries", projectId] : null,
    () => api.getProjectSummaries(projectId),
    { ...defaultConfig, ...config },
  );
}

// Programme Deliverables
export function useProgrammeDeliverables(config?: SWRConfiguration) {
  return useSWR<ProgrammeDeliverable[]>(
    "programme-deliverables",
    () => api.getProgrammeDeliverables(),
    { ...defaultConfig, ...config },
  );
}

export function useDeliverableOverview(config?: SWRConfiguration) {
  return useSWR<DeliverableOverview>(
    "deliverable-overview",
    () => api.getDeliverableOverview(),
    { ...defaultConfig, ...config },
  );
}

// Weekly Plans
export function useWeeklyPlans(config?: SWRConfiguration) {
  return useSWR<WeeklyPlan[]>(
    "weekly-plans",
    () => api.getWeeklyPlans(),
    { ...defaultConfig, ...config },
  );
}

export function useWeeklyPlan(id: number | null, config?: SWRConfiguration) {
  return useSWR<WeeklyPlanFull>(
    id ? ["weekly-plan", id] : null,
    () => api.getWeeklyPlan(id!),
    { ...defaultConfig, ...config },
  );
}

export function useCurrentWeeklyPlan(config?: SWRConfiguration) {
  return useSWR<WeeklyPlanFull | null>(
    "weekly-plan-current",
    () => api.getCurrentWeeklyPlan(),
    { ...defaultConfig, ...config },
  );
}
