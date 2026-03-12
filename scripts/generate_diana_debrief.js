const pptxgen = require("pptxgenjs");

const pres = new pptxgen();
pres.layout = "LAYOUT_16x9";
pres.author = "Customer Success Gen AI Programme";
pres.title = "Programme Debrief for Diana — March 2026";

// ── Moody's Palette ──
const C = {
  navy:      "003A70",
  accent:    "00A3E0",
  white:     "FFFFFF",
  offWhite:  "F5F7FA",
  lightGray: "E2E8F0",
  midGray:   "94A3B8",
  darkGray:  "475569",
  text:      "1E293B",
  green:     "16A34A",
  greenBg:   "F0FDF4",
  amber:     "D97706",
  amberBg:   "FFFBEB",
  red:       "DC2626",
  redBg:     "FEF2F2",
  teal:      "0891B2",
};

// ── RAG helpers ──
const RAG = {
  GREEN:  { bg: C.greenBg, border: C.green,  badge: C.green,  label: "GREEN" },
  AMBER:  { bg: C.amberBg, border: C.amber,  badge: C.amber,  label: "AMBER" },
  RED:    { bg: C.redBg,   border: C.red,    badge: C.red,    label: "RED" },
};

// Status badge configs
const STATUS = {
  LIVE:        { color: C.green,  label: "LIVE" },
  ON_TRACK:    { color: C.green,  label: "ON TRACK" },
  IN_PROGRESS: { color: C.amber,  label: "IN PROGRESS" },
  EARLY_STAGE: { color: C.amber,  label: "EARLY STAGE" },
  STALLED:     { color: C.red,    label: "STALLED" },
  MINIMAL:     { color: C.red,    label: "MINIMAL" },
  EXPANDING:   { color: C.accent, label: "EXPANDING" },
  MATURING:    { color: C.accent, label: "MATURING" },
};

// ── Reusable builders ──

function addNavyHeader(slide, title, subtitle) {
  slide.addShape(pres.shapes.RECTANGLE, {
    x: 0, y: 0, w: 10, h: 1.15,
    fill: { color: C.navy },
  });
  slide.addText(title, {
    x: 0.6, y: 0.15, w: 7.5, h: 0.65,
    fontSize: 28, fontFace: "Calibri", color: C.white, bold: true, margin: 0,
  });
  if (subtitle) {
    slide.addText(subtitle, {
      x: 0.6, y: 0.75, w: 7.5, h: 0.3,
      fontSize: 12, fontFace: "Calibri", color: C.accent, margin: 0,
    });
  }
}

function addStatusBadge(slide, status) {
  const s = STATUS[status];
  if (!s) return;
  slide.addShape(pres.shapes.RECTANGLE, {
    x: 8.0, y: 0.25, w: 1.7, h: 0.4,
    fill: { color: s.color },
  });
  slide.addText(s.label, {
    x: 8.0, y: 0.25, w: 1.7, h: 0.4,
    fontSize: 12, fontFace: "Calibri", bold: true, color: C.white,
    align: "center", valign: "middle", margin: 0,
  });
}

function addFooter(slide, pageLabel) {
  slide.addShape(pres.shapes.RECTANGLE, {
    x: 0, y: 5.25, w: 10, h: 0.375,
    fill: { color: C.navy },
  });
  slide.addText("Customer Success Gen AI Programme  |  Confidential", {
    x: 0.5, y: 5.27, w: 6, h: 0.3,
    fontSize: 8, fontFace: "Calibri", color: C.midGray,
  });
  slide.addText(pageLabel, {
    x: 8.5, y: 5.27, w: 1.2, h: 0.3,
    fontSize: 8, fontFace: "Calibri", color: C.midGray, align: "right",
  });
}

function addCard(slide, { x, y, w, h, accentColor, title, rag, bullets }) {
  // Card background
  slide.addShape(pres.shapes.RECTANGLE, {
    x, y, w, h,
    fill: { color: C.white },
    line: { color: C.lightGray, width: 0.5 },
    shadow: { type: "outer", color: "000000", blur: 3, offset: 1, angle: 135, opacity: 0.08 },
  });
  // Left accent bar
  slide.addShape(pres.shapes.RECTANGLE, {
    x, y, w: 0.06, h,
    fill: { color: accentColor },
  });
  // Title
  slide.addText(title, {
    x: x + 0.2, y: y + 0.08, w: w - 0.5, h: 0.3,
    fontSize: 13, fontFace: "Calibri", bold: true, color: C.text, margin: 0,
  });
  // RAG badge
  if (rag) {
    const r = RAG[rag];
    slide.addShape(pres.shapes.RECTANGLE, {
      x: x + w - 1.05, y: y + 0.08, w: 0.9, h: 0.25,
      fill: { color: r.badge },
    });
    slide.addText(r.label, {
      x: x + w - 1.05, y: y + 0.08, w: 0.9, h: 0.25,
      fontSize: 9, fontFace: "Calibri", bold: true, color: C.white,
      align: "center", valign: "middle", margin: 0,
    });
  }
  // Bullet items
  if (bullets && bullets.length) {
    const items = bullets.map((b, i) => ({
      text: b,
      options: { bullet: true, breakLine: i < bullets.length - 1, fontSize: 10, color: C.text },
    }));
    slide.addText(items, {
      x: x + 0.2, y: y + 0.38, w: w - 0.4, h: h - 0.48,
      fontFace: "Calibri", valign: "top", paraSpaceAfter: 3,
    });
  }
}


// ════════════════════════════════════════════════════
// SLIDE 1 — TITLE
// ════════════════════════════════════════════════════
let s1 = pres.addSlide();
s1.background = { color: C.navy };
s1.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 10, h: 0.06, fill: { color: C.accent } });

s1.addText("Customer Success\nGen AI Programme", {
  x: 0.8, y: 1.0, w: 8.4, h: 2.2,
  fontSize: 42, fontFace: "Calibri", color: C.white, bold: true, margin: 0,
});
s1.addShape(pres.shapes.RECTANGLE, { x: 0.8, y: 3.3, w: 2.5, h: 0.04, fill: { color: C.accent } });
s1.addText("Programme Debrief for Diana", {
  x: 0.8, y: 3.55, w: 8, h: 0.6,
  fontSize: 24, fontFace: "Calibri", color: C.accent, margin: 0,
});
s1.addText("Presented by Azmain  |  March 2026", {
  x: 0.8, y: 4.15, w: 8, h: 0.4,
  fontSize: 14, fontFace: "Calibri", color: C.midGray, margin: 0,
});
s1.addText("Moody's Analytics  |  Insurance Solutions", {
  x: 0.8, y: 4.55, w: 8, h: 0.35,
  fontSize: 11, fontFace: "Calibri", color: C.midGray, margin: 0,
});


// ════════════════════════════════════════════════════
// SLIDE 2 — EXECUTIVE OVERVIEW
// ════════════════════════════════════════════════════
let s2 = pres.addSlide();
s2.background = { color: C.offWhite };
addNavyHeader(s2, "Executive Overview");

// KPI strip
const kpis = [
  { num: "6",  label: "Workstreams" },
  { num: "10", label: "Projects" },
  { num: "31", label: "Scorecard\nAccounts" },
  { num: "11", label: "Weeks\nRunning" },
];
kpis.forEach((kpi, i) => {
  const kx = 0.5 + i * 2.3;
  s2.addShape(pres.shapes.RECTANGLE, {
    x: kx, y: 1.3, w: 2.0, h: 0.95,
    fill: { color: C.white },
    shadow: { type: "outer", color: "000000", blur: 3, offset: 1, angle: 135, opacity: 0.08 },
  });
  s2.addText(kpi.num, {
    x: kx, y: 1.3, w: 2.0, h: 0.55,
    fontSize: 30, fontFace: "Calibri", bold: true, color: C.navy, align: "center", margin: 0,
  });
  s2.addText(kpi.label, {
    x: kx, y: 1.82, w: 2.0, h: 0.38,
    fontSize: 9, fontFace: "Calibri", color: C.darkGray, align: "center", margin: 0,
  });
});

// Programme Mission card
addCard(s2, {
  x: 0.5, y: 2.5, w: 4.4, h: 2.5, accentColor: C.navy, title: "Programme Mission", rag: null,
  bullets: [
    "Accelerate AI adoption across Customer Success through practical tools, training, and prototyping",
    "Six workstreams: enablement (WS1), core tooling (WS2), intelligent agents (WS3-WS4), automation (WS5), rapid innovation (WS6)",
    "Reports into Natalia Orzechowska's organisation across multiple Insurance division teams",
    "Diya Sawhny is executive sponsor",
  ],
});

// Priorities & Challenges card
addCard(s2, {
  x: 5.1, y: 2.5, w: 4.4, h: 2.5, accentColor: C.amber, title: "Priorities & Challenges", rag: "AMBER",
  bullets: [
    "CLARA adoption and data quality",
    "Build in Five demo for May exceedance",
    "Gainsight integration (hard launch March 30)",
    "Salesforce one-way read via App Factory MCP",
    "Cross-OU expansion (Banking, Life, AM interested)",
    "Resource concentration risk (Azmain, BenVH, Richard)",
    "AWS Bedrock costs on pace for $10K/month",
  ],
});

addFooter(s2, "2");


// ════════════════════════════════════════════════════
// SLIDE 3 — PROGRAMME LANDSCAPE
// ════════════════════════════════════════════════════
let s3 = pres.addSlide();
s3.background = { color: C.offWhite };
addNavyHeader(s3, "Programme Landscape", "All Projects at a Glance");

const landscape = [
  { name: "CLARA", ws: "WS2", desc: "IRP Adoption Tracker — the primary tool", color: C.green },
  { name: "Training &\nEnablement", ws: "WS1", desc: "AI upskilling & prompt engineering", color: C.amber },
  { name: "CS Agent", ws: "WS3", desc: "Customer Success AI Agent", color: C.red },
  { name: "Friday", ws: "WS4", desc: "Internal PM app (Diana-sponsored)", color: C.green },
  { name: "Navigator L1\nAutomation", ws: "WS5", desc: "L1 support ticket automation", color: C.amber },
  { name: "Build in Five", ws: "WS6", desc: "Rapid AI prototyping (Martin)", color: C.green },
  { name: "Cross OU\nCollaboration", ws: "", desc: "Banking, AM, Life Insurance outreach", color: C.accent },
  { name: "Programme\nManagement", ws: "", desc: "Governance, steering, portfolio", color: C.accent },
  { name: "TSR\nEnhancements", ws: "", desc: "Cat bond TSR automation (Idris)", color: C.green },
  { name: "App Factory", ws: "", desc: "BenVH's MCP server platform", color: C.green },
];

landscape.forEach((p, i) => {
  const col = i % 5;
  const row = Math.floor(i / 5);
  const px = 0.4 + col * 1.88;
  const py = 1.4 + row * 2.0;

  // Card
  s3.addShape(pres.shapes.RECTANGLE, {
    x: px, y: py, w: 1.72, h: 1.7,
    fill: { color: C.white },
    line: { color: C.lightGray, width: 0.5 },
    shadow: { type: "outer", color: "000000", blur: 2, offset: 1, angle: 135, opacity: 0.06 },
  });
  // Status dot
  s3.addShape(pres.shapes.OVAL, {
    x: px + 1.42, y: py + 0.1, w: 0.18, h: 0.18,
    fill: { color: p.color },
  });
  // WS label
  if (p.ws) {
    s3.addText(p.ws, {
      x: px + 0.1, y: py + 0.08, w: 0.6, h: 0.22,
      fontSize: 8, fontFace: "Calibri", bold: true, color: C.accent, margin: 0,
    });
  }
  // Name
  s3.addText(p.name, {
    x: px + 0.1, y: py + 0.35, w: 1.52, h: 0.65,
    fontSize: 12, fontFace: "Calibri", bold: true, color: C.navy, margin: 0, valign: "top",
  });
  // Description
  s3.addText(p.desc, {
    x: px + 0.1, y: py + 1.05, w: 1.52, h: 0.55,
    fontSize: 8.5, fontFace: "Calibri", color: C.darkGray, margin: 0, valign: "top",
  });
});

addFooter(s3, "3");


// ════════════════════════════════════════════════════
// SLIDES 4-13 — PROJECT SLIDES (card-based layout)
// ════════════════════════════════════════════════════

const projects = [
  {
    title: "CLARA", subtitle: "WS2  |  IRP Adoption Tracker",
    status: "LIVE",
    overview: [
      "CLARA tracks IRP adoption across customer success teams — the central tool CSMs use in weekly Portfolio Reviews facilitated by Natalia Orzechowska",
      "31 scorecard migration accounts are the priority dataset",
      "Live on AWS with CI/CD pipeline, RBAC, and two-week structured release cycle",
      "Nikhil (50%) and Chris recently onboarded — Chris on bugs, Nikhil on scorecard tab",
    ],
    overviewRag: "AMBER",
    priorities: [
      "Gainsight integration alignment (hard launch March 30)",
      "Salesforce one-way read — Cases + Case Feed via App Factory MCP",
      "Scorecard tab and migration burndown completion",
      "User Voice and HD model data integration",
    ],
    prioritiesRag: "GREEN",
    challenges: [
      "Data quality (not features) is the primary adoption challenge — CSMs still need hand-holding after four weeks",
      "Azmain is single point of failure for features; BenVH is single point of failure for deployment",
      "Scope creep from multiple new integration requirements",
    ],
    challengesRag: "AMBER",
  },
  {
    title: "Build in Five", subtitle: "WS6  |  Rapid AI Prototyping (Martin)",
    status: "ON_TRACK",
    overview: [
      "Framework for building demo apps on IRP's Risk Data Lake using Cursor during customer conversations",
      "Martin built a near-complete dashboard builder that exceeded all expectations — drag-drop UI with data, visual, and AI modes",
      "Full white-labelling: themes, dark mode, logos, branding, corner radius",
      "Live Risk Modeller API connection already working — compared to Databricks Genie",
    ],
    overviewRag: "GREEN",
    priorities: [
      "Wire up Navigator MCP server — completes the live demo loop",
      "Stakeholder cascade: tech consulting, then demo team, then sales, then exceedance",
      "Target: May exceedance event (content due April)",
      "Three-pronged convergence: Martin's dashboard + Nikhil's MCP + Elliot's profiling agent",
    ],
    prioritiesRag: "GREEN",
    challenges: [
      "Martin's 12-week assignment is time-limited — clock is ticking but output justifies investment",
      "Product positioning unresolved: Moody's product feature vs customer self-service tool",
      "AIG using MCP for underwriting — elevates this from demo tool to strategic engagement vehicle",
    ],
    challengesRag: "AMBER",
  },
  {
    title: "App Factory", subtitle: "BenVH's MCP Server Platform",
    status: "ON_TRACK",
    overview: [
      "BenVH pivoting core to an MCP server — middleware that any app (CLARA, Slidey, Build in Five) can consume",
      "Apps request an LLM worker, App Factory spins it up and returns the connection — apps stay simple",
      "Connected to BenVH's patented Phantom Agent for enterprise AI governance",
      "Asia-Pac interest (Singapore, Japan, Australia) adds validation and urgency",
    ],
    overviewRag: "GREEN",
    priorities: [
      "MCP server completion (targeting end of this week)",
      "Martin's Build in Five as first integration proof of concept",
      "Wednesday showcase with senior stakeholders and ISLTR in London",
      "Inter-app communication: CLARA to Slidey via App Factory",
    ],
    prioritiesRag: "GREEN",
    challenges: [
      "BenVH is overloaded — MCP server, Slidey auth, Juliet's setup, Martin integration, all deployment duties",
      "BenVH is the only deployer — acute burnout risk and single point of failure",
      "No tested rollback procedure; schema changes have caused production breakage",
    ],
    challengesRag: "RED",
  },
  {
    title: "Friday", subtitle: "WS4  |  Internal PM App (Diana-sponsored)",
    status: "IN_PROGRESS",
    overview: [
      "Internal PM app like Monday.com, built by Azmain using 30 concurrent AI agents in one day",
      "Features: Kanban, list/timeline views, milestones, budgeting, decision tracking, stakeholder heat maps",
      "IRP projects sync bidirectionally with CLARA; non-IRP projects live only in Friday",
      "Diana endorsed it to replace slide-based Wednesday advisory project review",
    ],
    overviewRag: "GREEN",
    priorities: [
      "Diana presenting Friday vision to Ben Brooks and Charlotte for formal approval",
      "Deploy to dev (BenVH) without auth for a four-week pilot",
      "Seed with Diana's Excel file as initial data",
      "Prashant allocated to help with development",
    ],
    prioritiesRag: "GREEN",
    challenges: [
      "Adds to Azmain's already-stretched bandwidth across CLARA + five other workstreams",
      "No formal budget or sanctioning yet — unclear if skunkworks or official",
      "Cost concern: Azmain burned $500 Cursor budget in one day building it",
    ],
    challengesRag: "AMBER",
  },
  {
    title: "Training & Enablement", subtitle: "WS1  |  AI Upskilling Across Teams",
    status: "STALLED",
    overview: [
      "Conceptual framework exists: solution-focused training buckets, competency assessment, train-the-trainer approach",
      "No execution — CLARA consumed all of Azmain's bandwidth since January",
      "Previous training session (Dec 2025): 40 attendees from 80 registered",
      "Cross-OU enablement sessions delivered to Banking and Life (10 March)",
    ],
    overviewRag: "RED",
    priorities: [
      "Two grads arriving April 7 may provide execution capacity",
      "Need an owner other than Azmain — or his workload must be redistributed",
      "Share the insurance team's ROI approach and approval framework cross-OU",
    ],
    prioritiesRag: "AMBER",
    challenges: [
      "Remains stalled unless someone other than Azmain is allocated to execute",
      "Framework is ready — resourcing is the sole blocker",
      "Azmain flagged to Natalia O. as the biggest/quickest win but no time allocated",
    ],
    challengesRag: "RED",
  },
  {
    title: "Customer Success Agent", subtitle: "WS3  |  AI-Powered Customer Engagement",
    status: "MINIMAL",
    overview: [
      "AI agent to support customer success interactions — augment CSM capabilities with AI-driven insights",
      "Kevin Pern built a Copilot Studio + Salesforce prototype independently",
      "No programme oversight or operational integration",
      "Bernard (Life) built a separate Copilot health dashboard — parallel effort",
    ],
    overviewRag: "RED",
    priorities: [
      "Formal check-in with Kevin to assess what exists and what's needed",
      "Potential alignment with Salesforce Cases integration (Kevin is one of four consumers)",
      "Consider whether this converges with the broader Salesforce/App Factory strategy",
    ],
    prioritiesRag: "AMBER",
    challenges: [
      "Operating in isolation with no programme coordination",
      "Risk of duplicate effort across Kevin's work, Bernard's dashboard, and the Salesforce integration",
      "Azmain told Natalia O. this workstream needs engagement — no action taken yet",
    ],
    challengesRag: "RED",
  },
  {
    title: "Navigator L1 Automation", subtitle: "WS5  |  Support Ticket Automation",
    status: "EARLY_STAGE",
    overview: [
      "Concept: use Navigator's upcoming API support to auto-answer L1 support tickets",
      "MCP server discussion held with product team (Cihan, Lonny) in February",
      "No CS-side build started yet",
      "Navigator MCP server is now Build in Five's top integration priority — potential synergy",
    ],
    overviewRag: "AMBER",
    priorities: [
      "Clarity on what CS needs to build vs what the product team delivers",
      "MCP server integration with Martin's dashboard builder",
      "Define CS requirements for L1 automation use cases",
    ],
    prioritiesRag: "AMBER",
    challenges: [
      "Lowest clarity of all workstreams — needs scoping before any resource commitment",
      "Azmain admitted he doesn't fully understand the scope",
      "Integration with existing ticketing systems requires coordination with product",
    ],
    challengesRag: "AMBER",
  },
  {
    title: "Cross-OU Collaboration", subtitle: "Extending the Programme Across Moody's Divisions",
    status: "EXPANDING",
    overview: [
      "Banking (Gina Greer, Olivier) and Life (Jack Cheyne, Christian Curran) both engaged via Diya-requested sessions",
      "Both teams at the same stage insurance was in Nov 2025: siloed initiatives, no dedicated resources",
      "Idrees Deen (banking) formally onboarded as first non-core team member — building retention dashboard",
      "Template / flat-pack CLARA approach proposed for cross-OU reuse",
    ],
    overviewRag: "GREEN",
    priorities: [
      "Wednesday showcase meeting with ISLTR in London",
      "Share ROI framework and approval approach cross-OU",
      "Define resource model for cross-OU support (currently unfunded)",
    ],
    prioritiesRag: "GREEN",
    challenges: [
      "Every new team adds demand on BenVH (only deployer) and Azmain — expansion is unfunded",
      "Each OU has different tools, processes, and maturity levels — one size won't fit all",
      "Building trust and demonstrating value before asking for commitment",
    ],
    challengesRag: "AMBER",
  },
  {
    title: "Programme Management", subtitle: "Governance, Steering & Portfolio Reviews",
    status: "MATURING",
    overview: [
      "Diya endorsed three-pillar structure: IRP governance, customer intelligence, platform enablement",
      "Catherine emerged as a governance ally — volunteered for App Factory intake decision tree",
      "Formal Gainsight integration meeting set up with Tina Palumbo, Nadim, Rajesh",
      "56 decisions logged, 44 risks tracked — meeting intelligence tracked systematically",
    ],
    overviewRag: "AMBER",
    priorities: [
      "Post-twelve-week business case still needs building (clock ticking)",
      "App Factory governance approval board to be established",
      "Formal documentation of contributions and credit attribution",
      "Build Diana into the governance structure",
    ],
    prioritiesRag: "AMBER",
    challenges: [
      "Programme has scaled ambition without scaling governance",
      "Post-twelve-week business case is unaddressed — Diya asked for outcomes and continuation plan",
      "Meeting effectiveness varies — some meetings lack clear follow-through",
    ],
    challengesRag: "AMBER",
  },
  {
    title: "TSR Enhancements", subtitle: "Cat Bond TSR Automation (Idris Abram)",
    status: "IN_PROGRESS",
    overview: [
      "Idris Abram formally onboarded with Ben Brooks's approval for dedicated time",
      "Focus: automating TSR processes for cat bonds — first project outside core insurance CS team",
      "First test of the programme's enablement model: take someone from another team, provide tooling, produce output",
      "Idris has strong domain knowledge of cat bonds and TSRs",
    ],
    overviewRag: "GREEN",
    priorities: [
      "Define formal project scope and plan with Azmain's support",
      "Manage politics with Arno (Idris's current line manager)",
      "Build TSR automation as a reference implementation for enablement",
    ],
    prioritiesRag: "GREEN",
    challenges: [
      "Adds coordination overhead for Azmain — cat bond domain is new to the team",
      "Need to demonstrate value quickly to justify Idris's reallocation of time",
      "Overlap with Navigator L1 work requires careful delineation",
    ],
    challengesRag: "AMBER",
  },
];

projects.forEach((proj, i) => {
  const slide = pres.addSlide();
  slide.background = { color: C.offWhite };
  addNavyHeader(slide, proj.title, proj.subtitle);
  addStatusBadge(slide, proj.status);

  // Overview card (left, top)
  addCard(slide, {
    x: 0.4, y: 1.3, w: 4.45, h: 2.15,
    accentColor: C.navy, title: "Overview",
    rag: proj.overviewRag, bullets: proj.overview,
  });

  // Priorities card (right, top)
  addCard(slide, {
    x: 5.05, y: 1.3, w: 4.55, h: 2.15,
    accentColor: C.green, title: "Priorities & Next Steps",
    rag: proj.prioritiesRag, bullets: proj.priorities,
  });

  // Challenges card (full width, bottom)
  addCard(slide, {
    x: 0.4, y: 3.6, w: 9.2, h: 1.45,
    accentColor: C.amber, title: "Challenges",
    rag: proj.challengesRag, bullets: proj.challenges,
  });

  addFooter(slide, `${i + 4}`);
});


// ════════════════════════════════════════════════════
// SLIDE 14 — APPENDIX TITLE
// ════════════════════════════════════════════════════
let sAppTitle = pres.addSlide();
sAppTitle.background = { color: C.navy };
sAppTitle.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 10, h: 0.06, fill: { color: C.accent } });
sAppTitle.addText("Appendix", {
  x: 0.8, y: 1.8, w: 8.4, h: 1.2,
  fontSize: 42, fontFace: "Calibri", color: C.white, bold: true, margin: 0,
});
sAppTitle.addText("Detailed Programme Reference", {
  x: 0.8, y: 3.0, w: 8, h: 0.5,
  fontSize: 18, fontFace: "Calibri", color: C.accent, margin: 0,
});


// ════════════════════════════════════════════════════
// SLIDE 15 — KEY PEOPLE
// ════════════════════════════════════════════════════
let sPeople = pres.addSlide();
sPeople.background = { color: C.offWhite };
addNavyHeader(sPeople, "Key Stakeholders");

const people = [
  { name: "Richard Dosoo", role: "Programme / Operational Owner", note: "Strategic bridge between vision and execution. Manages Diya relationship. Flight risk (interviewing NYC)." },
  { name: "Azmain Hossain", role: "PM & CLARA Developer", note: "Builds everything. Reports to Diana. Stretched across CLARA, Friday, and 5 other workstreams." },
  { name: "Ben Brooks", role: "Product Owner (de facto)", note: "Built CLARA v1. Pushes for speed. Shopping CLARA cross-OU. Exceedance panel planning." },
  { name: "BenVH (Van Houten)", role: "Infrastructure & Deployment", note: "Only person who can deploy. App Factory architect. Owns patented Phantom Agent. Burnout risk." },
  { name: "Natalia Orzechowska", role: "Senior Director / CS Lead", note: "Runs Portfolio Reviews. Practical, process-focused. Your skip-level manager." },
  { name: "Natalia Plant", role: "Gainsight Team Lead", note: "Leads the Gainsight team. Key contact for Gainsight integration." },
  { name: "Martin Davies", role: "Build in Five Developer", note: "12-week assignment. Output exceeds all expectations. Dashboard builder compared to Databricks Genie." },
  { name: "Nikhil", role: "Tech Consulting (50/50)", note: "Bedrock API working. Being redirected from App Factory due to interpersonal conflict with BenVH." },
  { name: "Chris M", role: "Developer (CLARA)", note: "Methodical, adapting well. Bug fixes. Next assignment: Salesforce integration." },
  { name: "Idrees Deen", role: "Banking CS / Cross-OU", note: "Cross-OU coalition builder. Retention dashboard. Strategic thinker, strong banking ally." },
  { name: "Idris Abram", role: "TSR Enhancements", note: "First expansion outside core team. Cat bond / TSR automation. Ben Brooks approved dedicated time." },
  { name: "Catherine", role: "Data & Gainsight Governance", note: "Strongest new ally. Volunteered for App Factory governance. Full advocate conversion." },
  { name: "Diya Sawhny", role: "Executive Sponsor", note: "Impatient with detail. Wants elevator pitches. Engagement improved after Feb governance session." },
];

const headerRow = [
  { text: "Name", options: { fill: { color: C.navy }, color: C.white, bold: true, fontSize: 9, fontFace: "Calibri" } },
  { text: "Role", options: { fill: { color: C.navy }, color: C.white, bold: true, fontSize: 9, fontFace: "Calibri" } },
  { text: "Notes", options: { fill: { color: C.navy }, color: C.white, bold: true, fontSize: 9, fontFace: "Calibri" } },
];
const dataRows = people.map((p, i) => [
  { text: p.name, options: { fontSize: 8, fontFace: "Calibri", bold: true, color: C.text, fill: { color: i % 2 === 0 ? C.white : C.offWhite } } },
  { text: p.role, options: { fontSize: 8, fontFace: "Calibri", color: C.darkGray, fill: { color: i % 2 === 0 ? C.white : C.offWhite } } },
  { text: p.note, options: { fontSize: 8, fontFace: "Calibri", color: C.text, fill: { color: i % 2 === 0 ? C.white : C.offWhite } } },
]);

sPeople.addTable([headerRow, ...dataRows], {
  x: 0.4, y: 1.25, w: 9.2,
  colW: [1.8, 2.0, 5.2],
  border: { pt: 0.5, color: C.lightGray },
  rowH: 0.28,
  autoPage: false,
});

sPeople.addText("Full stakeholder map includes 40+ individuals across multiple teams and tiers.", {
  x: 0.4, y: 5.05, w: 9.2, h: 0.2,
  fontSize: 8, fontFace: "Calibri", italic: true, color: C.midGray, margin: 0,
});

addFooter(sPeople, "A1");


// ════════════════════════════════════════════════════
// SLIDE 16 — KEY MILESTONES
// ════════════════════════════════════════════════════
let sTimeline = pres.addSlide();
sTimeline.background = { color: C.offWhite };
addNavyHeader(sTimeline, "Key Milestones");

const milestones = [
  { date: "Jan 6", text: "Programme kick-off" },
  { date: "Jan 14", text: "First CLARA AWS deployment" },
  { date: "Jan 21", text: "Data input hub live; Portfolio Review designed" },
  { date: "Jan 26", text: "First live Portfolio Review; exec session with Ari/Diya" },
  { date: "Feb 2", text: "Data loss incident — trust damage with CSMs" },
  { date: "Feb 12", text: "CSM workshop hands-on sessions" },
  { date: "Feb 23", text: "Diya governance session; 3-pillar structure endorsed" },
  { date: "Mar 3", text: "Nikhil + Chris onboarded; Life SLT demo; Bedrock API working" },
  { date: "Mar 4", text: "Friday PM app revealed; 2-week release cycle adopted" },
  { date: "Mar 10", text: "Build in Five breakthrough; cross-OU sessions; Idris Abram onboarded" },
  { date: "Mar 11", text: "App Factory MCP pivot; Salesforce integration designed" },
  { date: "Mar 30", text: "Gainsight hard launch (upcoming)" },
  { date: "May", text: "Exceedance event — Build in Five demo target" },
];

milestones.forEach((m, i) => {
  const my = 1.3 + i * 0.3;
  sTimeline.addText(m.date, {
    x: 0.5, y: my, w: 1.0, h: 0.26,
    fontSize: 9, fontFace: "Calibri", bold: true, color: C.navy, align: "right", margin: 0,
  });
  sTimeline.addShape(pres.shapes.OVAL, {
    x: 1.7, y: my + 0.06, w: 0.14, h: 0.14,
    fill: { color: i >= 11 ? C.accent : C.navy },
  });
  if (i < milestones.length - 1) {
    sTimeline.addShape(pres.shapes.RECTANGLE, {
      x: 1.75, y: my + 0.2, w: 0.04, h: 0.16,
      fill: { color: C.lightGray },
    });
  }
  sTimeline.addText(m.text, {
    x: 2.05, y: my, w: 7.5, h: 0.26,
    fontSize: 9, fontFace: "Calibri", color: C.text, margin: 0,
  });
});

addFooter(sTimeline, "A2");


// ════════════════════════════════════════════════════
// SLIDE 17 — TOP RISKS
// ════════════════════════════════════════════════════
let sRisks = pres.addSlide();
sRisks.background = { color: C.offWhite };
addNavyHeader(sRisks, "Top Risks & Watchlist");

const risks = [
  { sev: "CRITICAL", title: "Key personnel concentration", detail: "Richard (strategy), BenVH (infra), Azmain (features) carry the programme. Richard interviewing in NYC. BenVH emotionally depleted. No succession plan." },
  { sev: "HIGH", title: "AWS cost trajectory", detail: "Bedrock at $1,163 in two weeks, on pace for $10K/month. No per-project or per-user cost attribution. Tags not configured." },
  { sev: "HIGH", title: "Scope outpacing capacity", detail: "Salesforce, Gainsight, cross-OU, Asia-Pac all emerging simultaneously. Every new consumer adds load to a team that hasn't grown." },
  { sev: "HIGH", title: "Deployment fragility", detail: "No tested rollback procedure. BenVH is the only deployer. Schema changes have caused production breakage." },
  { sev: "MEDIUM", title: "Post-12-week business case", detail: "Diya asked for outcomes and a continuation plan. Not addressed. Clock is ticking." },
  { sev: "MEDIUM", title: "Gainsight March 30 launch", detail: "Hard date confirmed. Immediate questions about CLARA sync expected. Phase 2 planning needs to accelerate." },
  { sev: "MEDIUM", title: "Documentation debt", detail: "CLARA has zero formal documentation. If Azmain is unavailable, nobody can maintain it independently." },
];

const sevColors = { CRITICAL: C.red, HIGH: C.amber, MEDIUM: C.teal };

risks.forEach((r, i) => {
  const ry = 1.3 + i * 0.55;
  const sc = sevColors[r.sev] || C.midGray;
  sRisks.addShape(pres.shapes.RECTANGLE, {
    x: 0.5, y: ry, w: 1.1, h: 0.22,
    fill: { color: sc },
  });
  sRisks.addText(r.sev, {
    x: 0.5, y: ry, w: 1.1, h: 0.22,
    fontSize: 8, fontFace: "Calibri", bold: true, color: C.white, align: "center", valign: "middle", margin: 0,
  });
  sRisks.addText(r.title, {
    x: 1.75, y: ry - 0.02, w: 3.0, h: 0.22,
    fontSize: 10, fontFace: "Calibri", bold: true, color: C.navy, margin: 0,
  });
  sRisks.addText(r.detail, {
    x: 1.75, y: ry + 0.2, w: 7.75, h: 0.3,
    fontSize: 8.5, fontFace: "Calibri", color: C.darkGray, margin: 0,
  });
});

addFooter(sRisks, "A3");


// ════════════════════════════════════════════════════
// SLIDE 18 — KEY THREADS TO WATCH
// ════════════════════════════════════════════════════
let sThreads = pres.addSlide();
sThreads.background = { color: C.offWhite };
addNavyHeader(sThreads, "Key Threads to Watch");

const threads = [
  { title: "CLARA Adoption", text: "Are CSMs using it daily? Feedback loop functioning? Data quality blocking trust." },
  { title: "Resource Strain", text: "Azmain's bandwidth, token costs, dev capacity across 10 projects. Grads arriving April." },
  { title: "Salesforce / Gainsight", text: "Gainsight hard launch March 30. Salesforce one-way read designed. Both via App Factory MCP." },
  { title: "Build in Five Demo", text: "Martin's May exceedance target. MCP server integration is the critical next step." },
  { title: "Cross-OU Expansion", text: "Banking, AM, Life all interested. Wednesday showcase with ISLTR. Currently unfunded." },
  { title: "Stakeholder Engagement", text: "Who's leaning in (Catherine, Idrees), who's drifting (Diya attention span)." },
  { title: "BenVH / Nikhil Conflict", text: "At breaking point. Richard planning confrontation. Nikhil to be redirected to Salesforce." },
  { title: "Governance Maturity", text: "Transitioning from informal to structured. Post-12-week case needed. Catherine as new ally." },
];

threads.forEach((t, i) => {
  const col = i % 2;
  const row = Math.floor(i / 2);
  const tx = 0.4 + col * 4.7;
  const ty = 1.3 + row * 1.0;

  sThreads.addShape(pres.shapes.RECTANGLE, {
    x: tx, y: ty, w: 4.5, h: 0.85,
    fill: { color: C.white },
    line: { color: C.lightGray, width: 0.5 },
  });
  sThreads.addText(t.title, {
    x: tx + 0.15, y: ty + 0.06, w: 4.2, h: 0.25,
    fontSize: 11, fontFace: "Calibri", bold: true, color: C.navy, margin: 0,
  });
  sThreads.addText(t.text, {
    x: tx + 0.15, y: ty + 0.32, w: 4.2, h: 0.45,
    fontSize: 9, fontFace: "Calibri", color: C.darkGray, margin: 0,
  });
});

addFooter(sThreads, "A4");


// ════════════════════════════════════════════════════
// WRITE FILE
// ════════════════════════════════════════════════════
pres.writeFile({ fileName: "C:\\Users\\maila\\Music\\icarus\\Diana_Debrief_March_2026_v2.pptx" })
  .then(() => console.log("PPTX created successfully — 18 slides"))
  .catch(err => console.error("Error:", err));
