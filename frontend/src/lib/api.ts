import type {
  DashboardData,
  ProgrammeBrief,
  TranscriptList,
  TranscriptDetail,
  SummaryBase,
  SummaryDetail,
  WeeklyReportBase,
  WeeklyReportDetail,
  WorkstreamBase,
  WorkstreamDetail,
  StakeholderBase,
  StakeholderDetail,
  MentionItem,
  DecisionSchema,
  DecisionCreate,
  DecisionUpdate,
  DecisionPositionUpdate,
  DecisionBoardResponse,
  DecisionTimelineResponse,
  OpenThreadSchema,
  OpenThreadCreate,
  OpenThreadUpdate,
  ThreadPositionUpdate,
  ThreadBoardResponse,
  ActionItemSchema,
  ActionItemCreate,
  GlossaryGrouped,
  GlossaryEntrySchema,
  GlossaryCreate,
  StakeholderCreate,
  SearchResponse,
  TimelineResponse,
  ProjectBase,
  ProjectHub,
  ProjectCreate,
  ProjectLinkCreate,
  ProjectWeeklyTimeline,
  DependencySchema,
  DependencyCreate,
  ResourceAllocationSchema,
  ResourceAllocationCreate,
  ScopeItemSchema,
  ScopeItemCreate,
  ProgrammeWinSchema,
  ProgrammeWinCreate,
  AdoptionMetricSchema,
  AdoptionMetricCreate,
  OutreachSchema,
  OutreachCreate,
  DivisionProfileSchema,
  DivisionProfileCreate,
  SentimentSignalSchema,
  SentimentSignalCreate,
  CommitmentSchema,
  CommitmentCreate,
  CrossProjectLinkSchema,
  CrossProjectLinkCreate,
  TaskSchema,
  TaskCreate,
  TaskUpdate,
  TaskPositionUpdate,
  TaskBoardResponse,
  TaskTimelineResponse,
  SpeakerReviewResponse,
  ConfirmAction,
  ConfirmResponse,
  TranscriptContext,
  TopicSignalSchema,
  TopicEvolutionData,
  TopicMomentum,
  InfluenceSignalSchema,
  InfluenceGraphData,
  ContradictionSchema,
  MeetingScoreSchema,
  MeetingScoreTrend,
  RiskEntrySchema,
  RiskHeatmapRow,
  ProjectSummarySchema,
} from "./types";

async function mutateApi<T>(
  path: string,
  method: string,
  body?: unknown,
): Promise<T> {
  const res = await fetch(`${getApiBase()}${path}`, {
    method,
    ...(body !== undefined && {
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }),
  });
  if (!res.ok) throw new Error(`API error: ${res.status}`);
  return res.json();
}

const getApiBase = () => {
  if (typeof window === "undefined") {
    // Server-side (inside Docker): use container service name
    return process.env.INTERNAL_API_URL || "http://backend:8000";
  }
  // Client-side (browser): use host-mapped port
  return process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
};

async function fetchApi<T>(
  path: string,
  params?: Record<string, string>,
): Promise<T> {
  const url = new URL(`${getApiBase()}${path}`);
  if (params) {
    Object.entries(params).forEach(([k, v]) => {
      if (v !== undefined && v !== "") url.searchParams.set(k, v);
    });
  }
  const res = await fetch(url.toString(), { cache: "no-store" });
  if (!res.ok) {
    let detail = `API error: ${res.status}`;
    try {
      const body = await res.json();
      if (body.detail) detail = typeof body.detail === "string" ? body.detail : JSON.stringify(body.detail);
    } catch {
      // ignore parse errors
    }
    throw new Error(detail);
  }
  return res.json();
}

export const api = {
  // Dashboard
  getDashboard: () => fetchApi<DashboardData>("/api/dashboard"),
  getBrief: () => fetchApi<ProgrammeBrief>("/api/dashboard/brief"),

  // Transcripts
  getTranscripts: (page = 1, limit = 20) =>
    fetchApi<TranscriptList>("/api/transcripts", {
      page: String(page),
      limit: String(limit),
    }),
  getTranscript: (id: number) =>
    fetchApi<TranscriptDetail>(`/api/transcripts/${id}`),
  getTranscriptSummary: (id: number) =>
    fetchApi<SummaryDetail>(`/api/transcripts/${id}/summary`),

  // Workstreams
  getWorkstreams: () => fetchApi<WorkstreamBase[]>("/api/workstreams"),
  getWorkstream: (id: number) =>
    fetchApi<WorkstreamDetail>(`/api/workstreams/${id}`),

  // Stakeholders
  getStakeholders: (tier?: number) =>
    fetchApi<StakeholderBase[]>(
      "/api/stakeholders",
      tier ? { tier: String(tier) } : undefined,
    ),
  getStakeholder: (id: number) =>
    fetchApi<StakeholderDetail>(`/api/stakeholders/${id}`),
  getStakeholderMentions: (id: number) =>
    fetchApi<MentionItem[]>(`/api/stakeholders/${id}/mentions`),

  // Decisions
  getDecisions: (params?: Record<string, string>) =>
    fetchApi<DecisionSchema[]>("/api/decisions", params),
  getDecision: (id: number) => fetchApi<DecisionSchema>(`/api/decisions/${id}`),
  getDecisionBoard: (workstreamId?: number, projectId?: number) => {
    const params: Record<string, string> = {};
    if (workstreamId) params.workstream_id = String(workstreamId);
    if (projectId) params.project_id = String(projectId);
    return fetchApi<DecisionBoardResponse>("/api/decisions/board", Object.keys(params).length ? params : undefined);
  },
  getDecisionTimeline: (workstreamId?: number, projectId?: number) => {
    const params: Record<string, string> = {};
    if (workstreamId) params.workstream_id = String(workstreamId);
    if (projectId) params.project_id = String(projectId);
    return fetchApi<DecisionTimelineResponse>("/api/decisions/timeline", Object.keys(params).length ? params : undefined);
  },
  createDecision: (data: DecisionCreate) =>
    mutateApi<DecisionSchema>("/api/decisions", "POST", data),
  updateDecision: (id: number, data: DecisionUpdate) =>
    mutateApi<DecisionSchema>(`/api/decisions/${id}`, "PATCH", data),
  updateDecisionPosition: (id: number, data: DecisionPositionUpdate) =>
    mutateApi<DecisionSchema>(`/api/decisions/${id}/position`, "PATCH", data),
  deleteDecision: (id: number) =>
    mutateApi<{ ok: boolean }>(`/api/decisions/${id}`, "DELETE"),

  // Open Threads
  getOpenThreads: (params?: Record<string, string>) =>
    fetchApi<OpenThreadSchema[]>("/api/open-threads", params),
  getOpenThread: (id: number) => fetchApi<OpenThreadSchema>(`/api/open-threads/${id}`),
  getThreadBoard: (projectId?: number) =>
    fetchApi<ThreadBoardResponse>("/api/open-threads/board", projectId ? { project_id: String(projectId) } : undefined),
  createOpenThread: (data: OpenThreadCreate) =>
    mutateApi<OpenThreadSchema>("/api/open-threads", "POST", data),
  updateOpenThread: (id: number, data: OpenThreadUpdate) =>
    mutateApi<OpenThreadSchema>(`/api/open-threads/${id}`, "PATCH", data),
  updateOpenThreadPosition: (id: number, data: ThreadPositionUpdate) =>
    mutateApi<OpenThreadSchema>(`/api/open-threads/${id}/position`, "PATCH", data),
  deleteOpenThread: (id: number) =>
    mutateApi<{ ok: boolean }>(`/api/open-threads/${id}`, "DELETE"),

  // Action Items
  getActionItems: (status?: string, owner?: string) =>
    fetchApi<ActionItemSchema[]>("/api/action-items", {
      ...(status && { status }),
      ...(owner && { owner }),
    }),
  createActionItem: (data: ActionItemCreate) =>
    mutateApi<ActionItemSchema>("/api/action-items", "POST", data),
  updateActionItem: (id: number, data: Partial<ActionItemCreate>) =>
    mutateApi<ActionItemSchema>(`/api/action-items/${id}`, "PATCH", data),
  completeActionItem: (id: number) =>
    mutateApi<ActionItemSchema>(`/api/action-items/${id}/complete`, "POST"),
  deleteActionItem: (id: number) =>
    mutateApi<{ ok: boolean }>(`/api/action-items/${id}`, "DELETE"),

  // Stakeholders
  createStakeholder: (data: StakeholderCreate) =>
    mutateApi<StakeholderBase>("/api/stakeholders", "POST", data),
  updateStakeholder: (id: number, data: Partial<StakeholderCreate>) =>
    mutateApi<StakeholderBase>(`/api/stakeholders/${id}`, "PATCH", data),
  deleteStakeholder: (id: number) =>
    mutateApi<{ ok: boolean }>(`/api/stakeholders/${id}`, "DELETE"),

  // Glossary
  getGlossary: () => fetchApi<GlossaryGrouped>("/api/glossary"),
  createGlossaryEntry: (data: GlossaryCreate) =>
    mutateApi<GlossaryEntrySchema>("/api/glossary", "POST", data),
  updateGlossaryEntry: (id: number, data: Partial<GlossaryCreate>) =>
    mutateApi<GlossaryEntrySchema>(`/api/glossary/${id}`, "PATCH", data),
  deleteGlossaryEntry: (id: number) =>
    mutateApi<{ ok: boolean }>(`/api/glossary/${id}`, "DELETE"),

  // Summaries
  getSummaries: () => fetchApi<SummaryBase[]>("/api/summaries"),
  getSummary: (id: number) => fetchApi<SummaryDetail>(`/api/summaries/${id}`),

  // Weekly Reports
  getWeeklyReports: () => fetchApi<WeeklyReportBase[]>("/api/weekly-reports"),
  getWeeklyReport: (id: number) =>
    fetchApi<WeeklyReportDetail>(`/api/weekly-reports/${id}`),

  // Search
  search: (q: string, types = "all", limit = 20) =>
    fetchApi<SearchResponse>("/api/search", {
      q,
      types,
      limit: String(limit),
    }),

  // Timeline
  getTimeline: (from?: string, to?: string) =>
    fetchApi<TimelineResponse>("/api/timeline", {
      ...(from && { from_date: from }),
      ...(to && { to_date: to }),
    }),

  // Projects
  getProjects: () => fetchApi<ProjectBase[]>("/api/projects"),
  getProject: (id: number) => fetchApi<ProjectBase>(`/api/projects/${id}`),
  getProjectHub: (id: number) => fetchApi<ProjectHub>(`/api/projects/${id}/hub`),
  getProjectWeekly: (id: number) =>
    fetchApi<ProjectWeeklyTimeline>(`/api/projects/${id}/weekly`),
  createProject: async (data: ProjectCreate) => {
    const res = await fetch(`${getApiBase()}/api/projects`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    });
    if (!res.ok) throw new Error(`API error: ${res.status}`);
    return res.json() as Promise<ProjectBase>;
  },
  updateProject: async (id: number, data: Partial<ProjectCreate>) => {
    const res = await fetch(`${getApiBase()}/api/projects/${id}`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    });
    if (!res.ok) throw new Error(`API error: ${res.status}`);
    return res.json() as Promise<ProjectBase>;
  },
  deleteProject: async (id: number) => {
    const res = await fetch(`${getApiBase()}/api/projects/${id}`, {
      method: "DELETE",
    });
    if (!res.ok) throw new Error(`API error: ${res.status}`);
    return res.json();
  },
  addProjectLinks: async (id: number, links: ProjectLinkCreate[]) => {
    const res = await fetch(`${getApiBase()}/api/projects/${id}/links`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ links }),
    });
    if (!res.ok) throw new Error(`API error: ${res.status}`);
    return res.json();
  },

  // Dependencies
  getDependencies: () => fetchApi<DependencySchema[]>("/api/dependencies"),
  createDependency: (data: DependencyCreate) =>
    mutateApi<DependencySchema>("/api/dependencies", "POST", data),
  updateDependency: (id: number, data: Partial<DependencyCreate>) =>
    mutateApi<DependencySchema>(`/api/dependencies/${id}`, "PATCH", data),
  deleteDependency: (id: number) =>
    mutateApi<{ ok: boolean }>(`/api/dependencies/${id}`, "DELETE"),

  // Resources
  getResources: () => fetchApi<ResourceAllocationSchema[]>("/api/resources"),
  createResource: (data: ResourceAllocationCreate) =>
    mutateApi<ResourceAllocationSchema>("/api/resources", "POST", data),
  updateResource: (id: number, data: Partial<ResourceAllocationCreate>) =>
    mutateApi<ResourceAllocationSchema>(`/api/resources/${id}`, "PATCH", data),
  deleteResource: (id: number) =>
    mutateApi<{ ok: boolean }>(`/api/resources/${id}`, "DELETE"),

  // Scope
  getScopeItems: () => fetchApi<ScopeItemSchema[]>("/api/scope"),
  createScopeItem: (data: ScopeItemCreate) =>
    mutateApi<ScopeItemSchema>("/api/scope", "POST", data),
  updateScopeItem: (id: number, data: Partial<ScopeItemCreate>) =>
    mutateApi<ScopeItemSchema>(`/api/scope/${id}`, "PATCH", data),
  deleteScopeItem: (id: number) =>
    mutateApi<{ ok: boolean }>(`/api/scope/${id}`, "DELETE"),

  // Import
  triggerImport: () =>
    fetch(`${getApiBase()}/api/import/trigger`, { method: "POST" }).then((r) =>
      r.json(),
    ),

  // Upload transcripts
  uploadTranscripts: async (
    files: File[],
    projectIds?: (number | null)[],
    secondaryProjectIds?: (number | null)[],
    tertiaryProjectIds?: (number | null)[],
  ) => {
    const formData = new FormData();
    files.forEach((f) => formData.append("files", f));
    if (projectIds) {
      formData.append("project_ids", JSON.stringify(projectIds));
    }
    if (secondaryProjectIds) {
      formData.append("secondary_project_ids", JSON.stringify(secondaryProjectIds));
    }
    if (tertiaryProjectIds) {
      formData.append("tertiary_project_ids", JSON.stringify(tertiaryProjectIds));
    }
    const res = await fetch(`${getApiBase()}/api/transcripts/upload`, {
      method: "POST",
      body: formData,
    });
    if (!res.ok) {
      const text = await res.text();
      throw new Error(`Upload failed (${res.status}): ${text}`);
    }
    return res.json();
  },

  // Programme Wins
  getWins: () => fetchApi<ProgrammeWinSchema[]>("/api/wins"),
  createWin: (data: ProgrammeWinCreate) =>
    mutateApi<ProgrammeWinSchema>("/api/wins", "POST", data),
  updateWin: (id: number, data: Partial<ProgrammeWinCreate>) =>
    mutateApi<ProgrammeWinSchema>(`/api/wins/${id}`, "PATCH", data),
  deleteWin: (id: number) =>
    mutateApi<{ ok: boolean }>(`/api/wins/${id}`, "DELETE"),

  // Adoption Metrics
  getAdoption: (workstream?: string) =>
    fetchApi<AdoptionMetricSchema[]>("/api/adoption", workstream ? { workstream } : undefined),
  createAdoption: (data: AdoptionMetricCreate) =>
    mutateApi<AdoptionMetricSchema>("/api/adoption", "POST", data),
  deleteAdoption: (id: number) =>
    mutateApi<{ ok: boolean }>(`/api/adoption/${id}`, "DELETE"),

  // Outreach
  getOutreach: (status?: string) =>
    fetchApi<OutreachSchema[]>("/api/outreach", status ? { status } : undefined),
  createOutreach: (data: OutreachCreate) =>
    mutateApi<OutreachSchema>("/api/outreach", "POST", data),
  updateOutreach: (id: number, data: Partial<OutreachCreate>) =>
    mutateApi<OutreachSchema>(`/api/outreach/${id}`, "PATCH", data),
  deleteOutreach: (id: number) =>
    mutateApi<{ ok: boolean }>(`/api/outreach/${id}`, "DELETE"),

  // Divisions
  getDivisions: () => fetchApi<DivisionProfileSchema[]>("/api/divisions"),
  createDivision: (data: DivisionProfileCreate) =>
    mutateApi<DivisionProfileSchema>("/api/divisions", "POST", data),
  updateDivision: (id: number, data: Partial<DivisionProfileCreate>) =>
    mutateApi<DivisionProfileSchema>(`/api/divisions/${id}`, "PATCH", data),
  deleteDivision: (id: number) =>
    mutateApi<{ ok: boolean }>(`/api/divisions/${id}`, "DELETE"),

  // Sentiments
  getSentiments: (stakeholderId?: number) =>
    fetchApi<SentimentSignalSchema[]>("/api/sentiments", stakeholderId ? { stakeholder_id: String(stakeholderId) } : undefined),
  getSentimentTimeline: (stakeholderId: number) =>
    fetchApi<SentimentSignalSchema[]>(`/api/sentiments/timeline/${stakeholderId}`),
  createSentiment: (data: SentimentSignalCreate) =>
    mutateApi<SentimentSignalSchema>("/api/sentiments", "POST", data),
  updateSentiment: (id: number, data: Partial<SentimentSignalCreate>) =>
    mutateApi<SentimentSignalSchema>(`/api/sentiments/${id}`, "PATCH", data),
  deleteSentiment: (id: number) =>
    mutateApi<{ ok: boolean }>(`/api/sentiments/${id}`, "DELETE"),

  // Commitments
  getCommitments: (status?: string, person?: string) =>
    fetchApi<CommitmentSchema[]>("/api/commitments", {
      ...(status && { status }),
      ...(person && { person }),
    }),
  createCommitment: (data: CommitmentCreate) =>
    mutateApi<CommitmentSchema>("/api/commitments", "POST", data),
  updateCommitment: (id: number, data: Partial<CommitmentCreate>) =>
    mutateApi<CommitmentSchema>(`/api/commitments/${id}`, "PATCH", data),
  deleteCommitment: (id: number) =>
    mutateApi<{ ok: boolean }>(`/api/commitments/${id}`, "DELETE"),

  // Tasks (Project Management)
  getTasks: (params?: { status?: string; priority?: string; assignee?: string; project_id?: string; label?: string; search?: string }) =>
    fetchApi<TaskSchema[]>("/api/tasks", params as Record<string, string>),
  getTask: (id: number) => fetchApi<TaskSchema>(`/api/tasks/${id}`),
  getTaskBoard: (projectId?: number) =>
    fetchApi<TaskBoardResponse>("/api/tasks/board", projectId ? { project_id: String(projectId) } : undefined),
  getTaskTimeline: (projectId?: number, fromDate?: string, toDate?: string) =>
    fetchApi<TaskTimelineResponse>("/api/tasks/timeline", {
      ...(projectId && { project_id: String(projectId) }),
      ...(fromDate && { from_date: fromDate }),
      ...(toDate && { to_date: toDate }),
    }),
  createTask: (data: TaskCreate) =>
    mutateApi<TaskSchema>("/api/tasks", "POST", data),
  updateTask: (id: number, data: TaskUpdate) =>
    mutateApi<TaskSchema>(`/api/tasks/${id}`, "PATCH", data),
  updateTaskPosition: (id: number, data: TaskPositionUpdate) =>
    mutateApi<TaskSchema>(`/api/tasks/${id}/position`, "PATCH", data),
  completeTask: (id: number) =>
    mutateApi<TaskSchema>(`/api/tasks/${id}/complete`, "POST"),
  deleteTask: (id: number) =>
    mutateApi<{ ok: boolean }>(`/api/tasks/${id}`, "DELETE"),
  getTaskLabels: () => fetchApi<string[]>("/api/tasks/labels"),

  // Speaker Review
  getSpeakerReview: () =>
    fetchApi<SpeakerReviewResponse>("/api/speaker-review"),
  confirmSpeakerIds: (actions: ConfirmAction[]) =>
    mutateApi<ConfirmResponse>("/api/speaker-review/confirm", "POST", { actions }),
  getSpeakerContext: (filename: string, timestamp?: string, label?: string) =>
    fetchApi<TranscriptContext>(`/api/speaker-review/context/${encodeURIComponent(filename)}`, {
      ...(timestamp && { timestamp }),
      ...(label && { label }),
    }),

  // Cross-Project Links
  getCrossProjectLinks: (projectId?: number) =>
    fetchApi<CrossProjectLinkSchema[]>("/api/cross-project-links", projectId ? { project_id: String(projectId) } : undefined),
  getProjectCrossLinks: (projectId: number) =>
    fetchApi<CrossProjectLinkSchema[]>(`/api/cross-project-links/project/${projectId}`),
  createCrossProjectLink: (data: CrossProjectLinkCreate) =>
    mutateApi<CrossProjectLinkSchema>("/api/cross-project-links", "POST", data),
  updateCrossProjectLink: (id: number, data: Partial<CrossProjectLinkCreate>) =>
    mutateApi<CrossProjectLinkSchema>(`/api/cross-project-links/${id}`, "PATCH", data),
  deleteCrossProjectLink: (id: number) =>
    mutateApi<{ ok: boolean }>(`/api/cross-project-links/${id}`, "DELETE"),

  // Topic Signals
  getTopicSignals: (category?: string) =>
    fetchApi<TopicSignalSchema[]>(`/api/topic-signals${category ? `?category=${category}` : ""}`),
  getTopicEvolution: () =>
    fetchApi<TopicEvolutionData[]>("/api/topic-signals/evolution"),
  getTopicMomentum: () =>
    fetchApi<TopicMomentum>("/api/topic-signals/momentum"),

  // Influence Signals
  getInfluenceSignals: (person?: string) =>
    fetchApi<InfluenceSignalSchema[]>(`/api/influence-signals${person ? `?person=${person}` : ""}`),
  getInfluenceGraph: () =>
    fetchApi<InfluenceGraphData>("/api/influence-signals/graph"),

  // Contradictions
  getContradictions: (kind?: string) =>
    fetchApi<ContradictionSchema[]>(`/api/contradictions${kind ? `?entry_kind=${kind}` : ""}`),
  getGaps: () =>
    fetchApi<ContradictionSchema[]>("/api/contradictions/gaps"),

  // Meeting Scores
  getMeetingScores: () =>
    fetchApi<MeetingScoreSchema[]>("/api/meeting-scores"),
  getMeetingScoreTrend: () =>
    fetchApi<MeetingScoreTrend[]>("/api/meeting-scores/trend"),

  // Risk Entries
  getRiskEntries: (severity?: string) =>
    fetchApi<RiskEntrySchema[]>(`/api/risk-entries${severity ? `?severity=${severity}` : ""}`),
  getRiskHeatmap: () =>
    fetchApi<{ rows: RiskHeatmapRow[] }>("/api/risk-entries/heatmap"),

  // Project Summaries
  getProjectSummaries: (projectId: number) =>
    fetchApi<ProjectSummarySchema[]>(`/api/projects/${projectId}/project-summaries`),
};
