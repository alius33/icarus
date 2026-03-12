// ── Transcript ──────────────────────────────────────────────────────────────

export interface TranscriptBase {
  id: number;
  file_name: string;
  title: string | null;
  date: string | null;
  participant_count: number;
  word_count: number;
  has_summary: boolean;
  primary_project_id: number | null;
  primary_project_name: string | null;
  secondary_project_id: number | null;
  secondary_project_name: string | null;
  tertiary_project_id: number | null;
  tertiary_project_name: string | null;
}

export interface TranscriptDetail extends TranscriptBase {
  raw_text: string;
  participants: string[];
  summary: SummaryBase | null;
}

export interface TranscriptList {
  items: TranscriptBase[];
  total: number;
  page: number;
  limit: number;
  pages: number;
}

// ── Summary ─────────────────────────────────────────────────────────────────

export interface SummaryBase {
  id: number;
  transcript_id: number;
  transcript_title: string | null;
  date: string | null;
  tldr: string | null;
}

export interface SummaryDetail extends SummaryBase {
  full_summary: string;
  key_decisions: string[];
  action_items: string[];
  risks_and_concerns: string[];
  follow_ups: string[];
}

// ── Weekly Report ───────────────────────────────────────────────────────────

export interface WeeklyReportBase {
  id: number;
  title: string;
  week_start: string;
  week_end: string;
  period_label: string | null;
}

export interface WeeklyReportDetail extends WeeklyReportBase {
  content: string;
  workstream_updates: string[];
  highlights: string[];
  risks: string[];
}

// ── Workstream ──────────────────────────────────────────────────────────────

export interface MilestoneSchema {
  id: number;
  workstream_id: number;
  title: string;
  status: string;
  target_date: string | null;
  notes: string | null;
}

export interface WorkstreamBase {
  id: number;
  code: string;
  name: string;
  owner: string | null;
  status: string;
  progress_pct: number | null;
  blocker_reason: string | null;
  assigned_fte: string | null;
}

export interface WorkstreamDetail extends WorkstreamBase {
  description: string | null;
  milestones: MilestoneSchema[];
  recent_mentions: string[];
}

// ── Stakeholder ─────────────────────────────────────────────────────────────

export interface StakeholderBase {
  id: number;
  name: string;
  role: string | null;
  organisation: string | null;
  tier: number;
  mention_count: number;
  risk_level: string | null;
  morale_notes: string | null;
  is_manual?: boolean;
}

export interface StakeholderDetail extends StakeholderBase {
  notes: string | null;
  aliases: string[];
  recent_mentions: MentionItem[];
}

export interface MentionItem {
  transcript_id: number;
  transcript_title: string | null;
  date: string | null;
  snippet: string;
}

// ── Decision ────────────────────────────────────────────────────────────────

export const DECISION_STATUSES = ["made", "in_progress", "implemented", "reversed", "superseded"] as const;
export type DecisionStatus = typeof DECISION_STATUSES[number];

export const DECISION_STATUS_CONFIG: Record<DecisionStatus, { label: string; color: string; bgColor: string; order: number }> = {
  made:        { label: "Made",        color: "text-blue-600",   bgColor: "bg-blue-100",   order: 0 },
  in_progress: { label: "In Progress", color: "text-yellow-600", bgColor: "bg-yellow-100", order: 1 },
  implemented: { label: "Implemented", color: "text-green-600",  bgColor: "bg-green-100",  order: 2 },
  reversed:    { label: "Reversed",    color: "text-red-600",    bgColor: "bg-red-100",    order: 3 },
  superseded:  { label: "Superseded",  color: "text-gray-600",   bgColor: "bg-gray-100",   order: 4 },
};

export interface DecisionSchema {
  id: number;
  number: number;
  title: string;
  description: string | null;
  date: string | null;
  status: string;
  execution_status: string;
  rationale: string | null;
  key_people: string[];
  owner: string | null;
  workstream: string | null;
  position: number;
  transcript_id: number | null;
  transcript_title: string | null;
  is_manual?: boolean;
}

export interface DecisionCreate {
  decision: string;
  date?: string;
  rationale?: string;
  key_people?: string[];
  execution_status?: string;
  workstream?: string;
}

export interface DecisionUpdate {
  decision?: string;
  date?: string;
  rationale?: string;
  key_people?: string[];
  execution_status?: string;
  workstream?: string;
}

export interface DecisionPositionUpdate { execution_status: string; position: number; }

export interface DecisionBoardColumn {
  status: string;
  label: string;
  color: string;
  order: number;
  decisions: DecisionSchema[];
  count: number;
}

export interface DecisionBoardResponse { columns: DecisionBoardColumn[]; total: number; }

export interface DecisionTimelineItem {
  id: number;
  number: number;
  title: string;
  execution_status: string;
  key_people: string[];
  decision_date: string | null;
  workstream: string | null;
}

export interface DecisionTimelineResponse { decisions: DecisionTimelineItem[]; total: number; }

export type DecisionViewMode = "board" | "list" | "timeline";

// ── Open Thread ─────────────────────────────────────────────────────────────

export const THREAD_STATUSES = ["OPEN", "WATCHING", "CLOSED"] as const;
export type ThreadStatus = typeof THREAD_STATUSES[number];

export const THREAD_STATUS_CONFIG: Record<ThreadStatus, { label: string; color: string; bgColor: string; order: number }> = {
  OPEN:     { label: "Open",     color: "text-red-600",    bgColor: "bg-red-100",    order: 0 },
  WATCHING: { label: "Watching", color: "text-yellow-600", bgColor: "bg-yellow-100", order: 1 },
  CLOSED:   { label: "Closed",   color: "text-green-600",  bgColor: "bg-green-100",  order: 2 },
};

export const THREAD_SEVERITIES = ["CRITICAL", "HIGH", "MEDIUM", "LOW"] as const;
export type ThreadSeverity = typeof THREAD_SEVERITIES[number];

export const SEVERITY_CONFIG: Record<ThreadSeverity, { label: string; color: string; dotColor: string }> = {
  CRITICAL: { label: "Critical", color: "text-red-600",    dotColor: "bg-red-500" },
  HIGH:     { label: "High",     color: "text-orange-500", dotColor: "bg-orange-500" },
  MEDIUM:   { label: "Medium",   color: "text-yellow-500", dotColor: "bg-yellow-500" },
  LOW:      { label: "Low",      color: "text-green-400",  dotColor: "bg-green-400" },
};

export const TREND_OPTIONS = ["escalating", "stable", "de-escalating"] as const;

export interface OpenThreadSchema {
  id: number;
  title: string;
  description: string | null;
  status: string;
  priority: string | null;
  owner: string | null;
  opened_date: string | null;
  last_discussed: string | null;
  workstream: string | null;
  severity: string | null;
  trend: string | null;
  position: number;
  question: string | null;
  why_it_matters: string | null;
  resolution: string | null;
  is_manual?: boolean;
}

export interface OpenThreadCreate {
  title: string;
  context?: string;
  question?: string;
  why_it_matters?: string;
  status?: string;
  first_raised?: string;
  severity?: string;
  trend?: string;
}

export interface OpenThreadUpdate {
  title?: string;
  context?: string;
  question?: string;
  why_it_matters?: string;
  status?: string;
  resolution?: string;
  first_raised?: string;
  severity?: string;
  trend?: string;
}

export interface ThreadPositionUpdate { status: string; position: number; }

export interface ThreadBoardColumn {
  status: string;
  label: string;
  color: string;
  order: number;
  threads: OpenThreadSchema[];
  count: number;
}

export interface ThreadBoardResponse { columns: ThreadBoardColumn[]; total: number; }

export type ThreadViewMode = "board" | "list";

// ── Action Item ─────────────────────────────────────────────────────────────

export interface ActionItemSchema {
  id: number;
  title: string;
  description: string | null;
  status: string;
  owner: string | null;
  due_date: string | null;
  source_transcript_id: number | null;
  source_transcript_title: string | null;
  workstream: string | null;
  is_manual?: boolean;
}

// ── Task (Project Management) ──────────────────────────────────────────────

export const TASK_STATUSES = ["TODO", "IN_PROGRESS", "IN_REVIEW", "DONE", "CANCELLED"] as const;
export type TaskStatus = typeof TASK_STATUSES[number];

export const TASK_PRIORITIES = ["URGENT", "HIGH", "MEDIUM", "LOW", "NONE"] as const;
export type TaskPriority = typeof TASK_PRIORITIES[number];

export const STATUS_CONFIG: Record<TaskStatus, { label: string; color: string; bgColor: string; order: number }> = {
  TODO:        { label: "Todo",        color: "text-blue-600",   bgColor: "bg-blue-100",   order: 0 },
  IN_PROGRESS: { label: "In Progress", color: "text-yellow-600", bgColor: "bg-yellow-100", order: 1 },
  IN_REVIEW:   { label: "In Review",   color: "text-purple-600", bgColor: "bg-purple-100", order: 2 },
  DONE:        { label: "Done",        color: "text-green-600",  bgColor: "bg-green-100",  order: 3 },
  CANCELLED:   { label: "Cancelled",   color: "text-red-600",    bgColor: "bg-red-100",    order: 4 },
};

export const PRIORITY_CONFIG: Record<TaskPriority, { label: string; color: string; dotColor: string }> = {
  URGENT: { label: "Urgent", color: "text-red-600",    dotColor: "bg-red-500" },
  HIGH:   { label: "High",   color: "text-orange-500", dotColor: "bg-orange-500" },
  MEDIUM: { label: "Medium", color: "text-yellow-500", dotColor: "bg-yellow-500" },
  LOW:    { label: "Low",    color: "text-blue-400",   dotColor: "bg-blue-400" },
  NONE:   { label: "None",   color: "text-gray-400",   dotColor: "bg-gray-300" },
};

export interface TaskSchema {
  id: number;
  identifier: string;
  title: string;
  description: string | null;
  status: TaskStatus;
  priority: TaskPriority;
  assignee: string | null;
  labels: string[];
  due_date: string | null;
  start_date: string | null;
  estimate: number | null;
  position: number;
  project_id: number | null;
  project_name: string | null;
  parent_id: number | null;
  parent_identifier: string | null;
  sub_task_count: number;
  created_date: string | null;
  completed_date: string | null;
  is_manual: boolean;
}

export interface TaskCreate {
  title: string;
  description?: string;
  status?: string;
  priority?: string;
  assignee?: string;
  labels?: string[];
  due_date?: string;
  start_date?: string;
  estimate?: number;
  project_id?: number;
  parent_id?: number;
}

export interface TaskUpdate {
  title?: string;
  description?: string;
  status?: string;
  priority?: string;
  assignee?: string;
  labels?: string[];
  due_date?: string;
  start_date?: string;
  estimate?: number;
  project_id?: number;
  parent_id?: number;
}

export interface TaskPositionUpdate {
  status: string;
  position: number;
}

export interface TaskBoardColumn {
  status: string;
  label: string;
  color: string;
  order: number;
  tasks: TaskSchema[];
  count: number;
}

export interface TaskBoardResponse {
  columns: TaskBoardColumn[];
  total: number;
}

export interface TaskTimelineItem {
  id: number;
  identifier: string;
  title: string;
  status: string;
  priority: string;
  assignee: string | null;
  start_date: string | null;
  due_date: string | null;
  project_name: string | null;
}

export interface TaskTimelineResponse {
  tasks: TaskTimelineItem[];
  total: number;
}

export type TaskViewMode = "board" | "list" | "timeline";

// ── Glossary ────────────────────────────────────────────────────────────────

export interface GlossaryEntrySchema {
  id: number;
  term: string;
  definition: string;
  category: string;
  aliases: string[];
  is_manual?: boolean;
}

// ── Create/Update Types ────────────────────────────────────────────────────

export interface ActionItemCreate {
  description: string;
  owner?: string;
  deadline?: string;
  context?: string;
  status?: string;
}

export interface StakeholderCreate {
  name: string;
  tier?: number;
  role?: string;
  notes?: string;
  risk_level?: string;
  morale_notes?: string;
}

export interface GlossaryCreate {
  term: string;
  definition: string;
  category?: string;
}

export type GlossaryGrouped = Record<string, GlossaryEntrySchema[]>;

// ── Search ──────────────────────────────────────────────────────────────────

export interface SearchResult {
  type: string;
  id: number;
  title: string;
  snippet: string;
  score: number;
  url: string;
}

export interface SearchResponse {
  query: string;
  total: number;
  results: SearchResult[];
}

// ── Dashboard ───────────────────────────────────────────────────────────────

export interface DashboardProjectCard {
  id: number;
  name: string;
  status: string;
  color: string | null;
  workstream_code: string | null;
  is_custom: boolean;
  transcript_count: number;
  action_count: number;
  open_thread_count: number;
  decision_count: number;
  last_activity_date: string | null;
  trend: "up" | "down" | "flat";
}

export interface ActivityFeedItem {
  id: number;
  entity_type: string;
  title: string;
  date: string | null;
  project_id: number | null;
  project_name: string | null;
}

export interface NeedsAttentionItem {
  id: number;
  entity_type: string;
  title: string;
  description: string | null;
  status: string;
  owner: string | null;
  reason: string;
  days_overdue: number | null;
  project_id: number | null;
  project_name: string | null;
}

export interface StakeholderEngagementItem {
  id: number;
  name: string;
  tier: number;
  role: string | null;
  recent_mentions: number;
  previous_mentions: number;
  trend: "rising" | "stable" | "declining" | "silent";
  last_mentioned_date: string | null;
}

export interface DashboardData {
  total_transcripts: number;
  total_decisions: number;
  open_actions: number;
  critical_threads: number;
  projects: DashboardProjectCard[];
  recent_activity: ActivityFeedItem[];
  needs_attention: NeedsAttentionItem[];
  stakeholder_engagement: StakeholderEngagementItem[];
}

export interface ProgrammeBrief {
  date: string;
  text: string;
}

// ── Project ────────────────────────────────────────────────────────────────

export type EntityType =
  | "transcript"
  | "summary"
  | "decision"
  | "action_item"
  | "open_thread"
  | "stakeholder";

export interface ProjectBase {
  id: number;
  name: string;
  description: string | null;
  is_custom: boolean;
  status: string;
  color: string | null;
  icon: string | null;
  workstream_id: number | null;
  workstream_code: string | null;
  transcript_count: number;
  summary_count: number;
  decision_count: number;
  action_count: number;
  open_thread_count: number;
  stakeholder_count: number;
}

export interface ProjectCreate {
  name: string;
  description?: string;
  status?: string;
  color?: string;
  icon?: string;
}

export interface ProjectHub {
  project: ProjectBase;
  transcripts: TranscriptBase[];
  summaries: SummaryBase[];
  decisions: DecisionSchema[];
  action_items: ActionItemSchema[];
  open_threads: OpenThreadSchema[];
  stakeholders: StakeholderBase[];
  project_summaries: ProjectSummarySchema[];
}

export interface ProjectLinkCreate {
  entity_type: EntityType;
  entity_id: number;
}

// ── Project Weekly Timeline ────────────────────────────────────────────────

export interface WeekTranscriptItem {
  id: number;
  title: string | null;
  file_name: string;
  date: string | null;
  participant_count: number;
  word_count: number;
  has_summary: boolean;
  summary_id: number | null;
  summary_tldr: string | null;
  summary_content: string | null;
}

export interface WeekDecisionItem {
  id: number;
  number: number;
  decision: string;
  rationale: string | null;
  key_people: string[];
}

export interface WeekActionItem {
  id: number;
  number: string;
  description: string;
  owner: string | null;
  status: string;
  deadline: string | null;
}

export interface ProjectWeek {
  week_start: string;
  week_end: string;
  week_label: string;
  weekly_report_id: number | null;
  weekly_report_content: string | null;
  transcripts: WeekTranscriptItem[];
  decisions: WeekDecisionItem[];
  action_items: WeekActionItem[];
  transcript_count: number;
  decision_count: number;
  action_count: number;
}

export interface ProjectWeeklyTimeline {
  project: ProjectBase;
  weeks: ProjectWeek[];
  total_weeks: number;
}

// ── Timeline ────────────────────────────────────────────────────────────────

export interface TimelineEvent {
  date: string;
  type: string;
  title: string;
  description: string | null;
  reference_id: number | null;
  reference_url: string | null;
}

export interface TimelineResponse {
  from_date: string;
  to_date: string;
  events: TimelineEvent[];
  total: number;
}

// ── Dependency ──────────────────────────────────────────────────────────────

export interface DependencySchema {
  id: number;
  name: string;
  dependency_type: string;
  status: string;
  blocking_reason: string | null;
  estimated_effort: string | null;
  assigned_to: string | null;
  affected_workstreams: string | null;
  priority: string;
  notes: string | null;
}

export interface DependencyCreate {
  name: string;
  dependency_type?: string;
  status?: string;
  blocking_reason?: string;
  estimated_effort?: string;
  assigned_to?: string;
  affected_workstreams?: string;
  priority?: string;
  notes?: string;
}

// ── Resource Allocation ────────────────────────────────────────────────────

export interface AllocationEntry {
  workstream: string;
  percentage: number;
}

export interface ResourceAllocationSchema {
  id: number;
  person_name: string;
  role: string | null;
  allocations: AllocationEntry[];
  capacity_status: string;
  notes: string | null;
  start_date: string | null;
  end_date: string | null;
}

export interface ResourceAllocationCreate {
  person_name: string;
  role?: string;
  allocations?: AllocationEntry[];
  capacity_status?: string;
  notes?: string;
  start_date?: string;
  end_date?: string;
}

// ── Scope Item ─────────────────────────────────────────────────────────────

export interface ScopeItemSchema {
  id: number;
  name: string;
  scope_type: string;
  workstream: string | null;
  added_date: string | null;
  estimated_effort: string | null;
  budgeted: boolean;
  status: string;
  description: string | null;
  impact_notes: string | null;
}

export interface ScopeItemCreate {
  name: string;
  scope_type?: string;
  workstream?: string;
  added_date?: string;
  estimated_effort?: string;
  budgeted?: boolean;
  status?: string;
  description?: string;
  impact_notes?: string;
}

// ── Dashboard V2 Types ──────────────────────────────────────────────────────

export interface KpiData {
  total_transcripts: number;
  transcripts_this_week: number;
  weekly_transcript_counts: number[];
  open_actions: number;
  overdue_actions: number;
  weekly_open_action_counts: number[];
  critical_high_risks: number;
  escalating_risks: number;
  weekly_risk_counts: number[];
  blocked_dependencies: number;
  in_progress_dependencies: number;
  weekly_blocked_counts: number[];
  avg_utilization: number;
  overloaded_count: number;
  weekly_utilization: number[];
  total_projects: number;
  active_projects: number;
}

export interface InsightsData {
  action_completion_rate: number;
  decision_velocity: number;
  scope_creep_pct: number;
  risk_velocity: number;
  overdue_sla_pct: number;
}

export interface HealthScore {
  score: number;
  rag: "green" | "amber" | "red";
  breakdown: Record<string, number>;
}

export interface ProgrammeStatus {
  narrative: string;
  health_rag: "green" | "amber" | "red";
  biggest_win: string | null;
  biggest_risk: string | null;
  open_actions: number;
  overdue_count: number;
  critical_risks: number;
}

// Update DashboardData to include new fields
export interface DashboardDataV2 extends DashboardData {
  programme_status: ProgrammeStatus;
  kpi: KpiData;
  insights: InsightsData;
}

export interface ProgrammeBriefV2 extends ProgrammeBrief {
  narrative: string | null;
  health_rag: string | null;
  biggest_win: string | null;
  biggest_risk: string | null;
}

// ── Dashboard Filter Types ──────────────────────────────────────────────────

export type TimeFilter = "1w" | "2w" | "1m" | "all";
export type DashboardTab = "risks" | "resources" | "activity";

export interface DashboardFilters {
  timeFilter: TimeFilter;
  workstreamFilter: string | null; // workstream code or null for all
  activeTab: DashboardTab;
}

// ── Programme Win ────────────────────────────────────────────────────────
export interface ProgrammeWinSchema {
  id: number;
  category: string;
  title: string;
  description: string | null;
  before_state: string | null;
  after_state: string | null;
  workstream: string | null;
  confidence: string;
  date_recorded: string | null;
  notes: string | null;
  is_manual: boolean;
}

export interface ProgrammeWinCreate {
  category: string;
  title: string;
  description?: string;
  before_state?: string;
  after_state?: string;
  workstream?: string;
  confidence?: string;
  date_recorded?: string;
  notes?: string;
}

// ── Adoption Metric ────────────────────────────────────────────────────
export interface AdoptionMetricSchema {
  id: number;
  date: string;
  metric_type: string;
  value: number;
  workstream: string | null;
  notes: string | null;
}

export interface AdoptionMetricCreate {
  date: string;
  metric_type: string;
  value: number;
  workstream?: string;
  notes?: string;
}

// ── Outreach ────────────────────────────────────────────────────────────
export interface OutreachSchema {
  id: number;
  contact_name: string;
  contact_role: string | null;
  division: string | null;
  status: string;
  interest_level: number;
  first_contact_date: string | null;
  last_contact_date: string | null;
  meeting_count: number;
  notes: string | null;
  next_step: string | null;
  next_step_date: string | null;
}

export interface OutreachCreate {
  contact_name: string;
  contact_role?: string;
  division?: string;
  status?: string;
  interest_level?: number;
  first_contact_date?: string;
  last_contact_date?: string;
  meeting_count?: number;
  notes?: string;
  next_step?: string;
  next_step_date?: string;
}

// ── Division Profile ────────────────────────────────────────────────────
export interface DivisionProfileSchema {
  id: number;
  name: string;
  status: string;
  current_tools: string | null;
  pain_points: string | null;
  key_contact: string | null;
  notes: string | null;
}

export interface DivisionProfileCreate {
  name: string;
  status?: string;
  current_tools?: string;
  pain_points?: string;
  key_contact?: string;
  notes?: string;
}

// ── Sentiment Signal ────────────────────────────────────────────────────
export interface SentimentSignalSchema {
  id: number;
  stakeholder_id: number;
  stakeholder_name?: string;
  transcript_id: number | null;
  date: string | null;
  sentiment: string;
  shift: string | null;
  topic: string | null;
  quote: string | null;
  notes: string | null;
  is_manual: boolean;
}

export interface SentimentSignalCreate {
  stakeholder_id: number;
  transcript_id?: number;
  date?: string;
  sentiment: string;
  shift?: string;
  topic?: string;
  quote?: string;
  notes?: string;
}

// ── Commitment ──────────────────────────────────────────────────────────
export interface CommitmentSchema {
  id: number;
  person: string;
  commitment: string;
  transcript_id: number | null;
  date_made: string | null;
  deadline_text: string | null;
  deadline_resolved: string | null;
  deadline_type: string | null;
  condition: string | null;
  linked_action_id: number | null;
  status: string;
  verified_date: string | null;
  notes: string | null;
  is_manual: boolean;
}

export interface CommitmentCreate {
  person: string;
  commitment: string;
  transcript_id?: number;
  date_made?: string;
  deadline_text?: string;
  deadline_resolved?: string;
  deadline_type?: string;
  condition?: string;
  linked_action_id?: number;
  status?: string;
  notes?: string;
}

// ── Cross-Project Link ──────────────────────────────────────────────────
export interface CrossProjectLinkSchema {
  id: number;
  source_project_id: number;
  source_project_name?: string;
  target_project_id: number;
  target_project_name?: string;
  link_type: string;
  description: string | null;
  transcript_id: number | null;
  date_detected: string | null;
  severity: string;
  status: string;
  is_manual: boolean;
}

export interface CrossProjectLinkCreate {
  source_project_id: number;
  target_project_id: number;
  link_type: string;
  description?: string;
  transcript_id?: number;
  date_detected?: string;
  severity?: string;
  status?: string;
}

// ── Speaker Review ──────────────────────────────────────────────────────────

export interface SpeakerReviewItem {
  id: string; // "{filename}::{label}::{timestamp}"
  transcript_filename: string;
  meeting_type: string;
  known_speakers: string[];
  speaker_label: string;
  timestamp: string;
  identified_as: string;
  confidence: number;
  method: string;
  evidence: string;
  status: string; // "applied" | "flagged" | "unresolved"
}

export interface ReviewSummary {
  total_transcripts: number;
  total_identifications: number;
  applied_count: number;
  flagged_count: number;
  unresolved_count: number;
  methods: Record<string, number>;
}

export interface SpeakerReviewResponse {
  summary: ReviewSummary;
  items: SpeakerReviewItem[];
  stakeholder_names: string[];
}

export interface ConfirmAction {
  id: string;
  action: "accept" | "reject" | "manual";
  manual_name?: string;
}

export interface ConfirmResponse {
  applied: number;
  rejected: number;
  errors: string[];
}

export interface TranscriptContext {
  filename: string;
  lines: string[];
  highlight_line: number;
}

// ── Analysis Engine Types ───────────────────────────────────────────

export interface TopicSignalSchema {
  id: number;
  date: string | null;
  topic: string;
  category: string | null;
  intensity: string | null;
  first_raised: string | null;
  meetings_count: number;
  trend: string | null;
  key_quote: string | null;
  confidence: string | null;
  transcript_id: number | null;
  is_manual: boolean;
}

export interface TopicEvolutionPoint {
  date: string;
  intensity: string;
  meetings_count: number;
}

export interface TopicEvolutionData {
  topic: string;
  category: string | null;
  data_points: TopicEvolutionPoint[];
}

export interface TopicMomentum {
  rising: TopicSignalSchema[];
  declining: TopicSignalSchema[];
  going_cold: TopicSignalSchema[];
}

export interface InfluenceSignalSchema {
  id: number;
  date: string | null;
  person: string;
  influence_type: string;
  direction: string | null;
  target_person: string | null;
  topic: string | null;
  evidence: string | null;
  strength: string | null;
  confidence: string | null;
  coalition_name: string | null;
  coalition_members: string | null;
  alignment: string | null;
  transcript_id: number | null;
  is_manual: boolean;
}

export interface InfluenceGraphNode {
  id: string;
  name: string;
  signal_count: number;
}

export interface InfluenceGraphEdge {
  source: string;
  target: string;
  type: string;
  weight: number;
}

export interface InfluenceGraphData {
  nodes: InfluenceGraphNode[];
  edges: InfluenceGraphEdge[];
}

export interface ContradictionSchema {
  id: number;
  date: string | null;
  contradiction_type: string;
  person: string | null;
  statement_a: string | null;
  date_a: string | null;
  statement_b: string | null;
  date_b: string | null;
  severity: string | null;
  resolution: string;
  confidence: string | null;
  gap_description: string | null;
  expected_source: string | null;
  last_mentioned: string | null;
  meetings_absent: number | null;
  entry_kind: string;
  transcript_id: number | null;
  is_manual: boolean;
}

export interface MeetingScoreSchema {
  id: number;
  transcript_id: number;
  date: string | null;
  meeting_title: string | null;
  meeting_type: string | null;
  overall_score: number;
  decision_velocity: number | null;
  action_clarity: number | null;
  engagement_balance: number | null;
  topic_completion: number | null;
  follow_through: number | null;
  participant_count: number | null;
  duration_category: string | null;
  recommendations: string | null;
  is_manual: boolean;
}

export interface MeetingScoreTrend {
  date: string;
  score: number;
  meeting_type: string | null;
}

export interface RiskEntrySchema {
  id: number;
  risk_id: string;
  date: string | null;
  title: string;
  description: string | null;
  category: string | null;
  severity: string;
  trajectory: string | null;
  source_type: string | null;
  owner: string | null;
  mitigation: string | null;
  last_reviewed: string | null;
  meetings_mentioned: number;
  confidence: string | null;
  transcript_id: number | null;
  is_manual: boolean;
}

export interface RiskHeatmapRow {
  category: string;
  CRITICAL: number;
  HIGH: number;
  MEDIUM: number;
  LOW: number;
}

export interface ProjectSummarySchema {
  id: number;
  project_id: number;
  transcript_id: number;
  date: string | null;
  relevance: string | null;
  content: string;
  source_file: string | null;
}

export interface AnalysisInsights {
  avg_meeting_score: number;
  active_critical_risks: number;
  escalating_risks: number;
  new_contradictions_this_week: number;
  top_rising_topic: string | null;
}
