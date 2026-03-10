"use client";

import useSWR, { SWRConfiguration } from "swr";
import { api } from "./api";
import type {
  DashboardData,
  TranscriptList,
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
    () => api.getOpenThreads(status),
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
