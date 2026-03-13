const pptxgen = require("pptxgenjs");

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.33 x 7.5
pres.author = "Azmain Hossain";
pres.title = "CLARA-Gainsight Integration Charter";

// Moody's brand
const navy = "091164";
const blue = "005eff";
const white = "FFFFFF";
const lightGray = "F2F4F8";
const midGray = "6B7280";
const darkText = "1F2937";
const headerH = 0.9;

function addHeader(slide, title, subtitle) {
  slide.addShape(pres.ShapeType.rect, { x: 0, y: 0, w: "100%", h: headerH, fill: { color: navy } });
  slide.addText(title, { x: 0.6, y: 0.12, w: 10, h: 0.5, fontSize: 24, fontFace: "Calibri", bold: true, color: white });
  if (subtitle) {
    slide.addText(subtitle, { x: 0.6, y: 0.52, w: 10, h: 0.3, fontSize: 12, fontFace: "Calibri", color: "CADCFC" });
  }
  // Blue accent line
  slide.addShape(pres.ShapeType.rect, { x: 0, y: headerH, w: "100%", h: 0.04, fill: { color: blue } });
}

function addFooter(slide, pageNum) {
  slide.addText("CLARA-Gainsight Integration Charter  |  v1.0 Draft  |  13 March 2026", {
    x: 0.6, y: 7.0, w: 8, h: 0.3, fontSize: 8, fontFace: "Calibri", color: midGray
  });
  slide.addText(String(pageNum), {
    x: 12.2, y: 7.0, w: 0.8, h: 0.3, fontSize: 8, fontFace: "Calibri", color: midGray, align: "right"
  });
}

const tableHeaderOpts = { fill: { color: navy }, color: white, bold: true, fontSize: 10, fontFace: "Calibri" };
const tableCellOpts = { fontSize: 10, fontFace: "Calibri", color: darkText, valign: "top" };
const tableCellAlt = { ...tableCellOpts, fill: { color: lightGray } };

let pg = 1;

// --- SLIDE 1: Title ---
{
  const s = pres.addSlide();
  s.addShape(pres.ShapeType.rect, { x: 0, y: 0, w: "100%", h: "100%", fill: { color: navy } });
  s.addShape(pres.ShapeType.rect, { x: 0, y: 5.2, w: "100%", h: 0.06, fill: { color: blue } });
  s.addText("CLARA-Gainsight\nIntegration Charter", {
    x: 0.8, y: 1.2, w: 11, h: 2.5, fontSize: 44, fontFace: "Calibri", bold: true, color: white, lineSpacingMultiple: 1.1
  });
  s.addText("Version 1.0 (Draft)  |  13 March 2026", {
    x: 0.8, y: 3.6, w: 8, h: 0.4, fontSize: 16, fontFace: "Calibri", color: "CADCFC"
  });
  s.addText("Author: Azmain Hossain\nCustomer Success Gen AI Programme\nMoody's Analytics — Insurance Division", {
    x: 0.8, y: 5.5, w: 8, h: 1.2, fontSize: 14, fontFace: "Calibri", color: "9CA3AF", lineSpacingMultiple: 1.4
  });
}

// --- SLIDE 2: Purpose ---
pg++;
{
  const s = pres.addSlide();
  addHeader(s, "1. Purpose");
  addFooter(s, pg);
  s.addText("This charter defines the scope, responsibilities, timeline, and success criteria for integrating CLARA with Gainsight.", {
    x: 0.8, y: 1.3, w: 11.5, h: 0.8, fontSize: 16, fontFace: "Calibri", color: darkText, bold: true
  });
  s.addText("It exists to ensure both teams have a shared understanding of what will be built, by whom, and by when — so that no party is surprised by requirements, resource demands, or delivery expectations during execution.", {
    x: 0.8, y: 2.2, w: 11.5, h: 0.8, fontSize: 14, fontFace: "Calibri", color: midGray
  });

  // Key outcomes boxes
  const boxes = [
    { icon: "Scope", desc: "What data objects will be synchronised and in what order" },
    { icon: "Roles", desc: "Who owns what — Gainsight team vs CLARA team vs joint" },
    { icon: "Timeline", desc: "Phased milestones from charter sign-off through production" },
    { icon: "Criteria", desc: "Measurable success criteria for POC and production" },
  ];
  boxes.forEach((b, i) => {
    const bx = 0.8 + i * 3.05;
    s.addShape(pres.ShapeType.rect, { x: bx, y: 3.5, w: 2.8, h: 2.5, fill: { color: lightGray }, rectRadius: 0.1 });
    s.addShape(pres.ShapeType.rect, { x: bx, y: 3.5, w: 2.8, h: 0.06, fill: { color: blue }, rectRadius: 0 });
    s.addText(b.icon, { x: bx + 0.2, y: 3.75, w: 2.4, h: 0.4, fontSize: 16, fontFace: "Calibri", bold: true, color: navy });
    s.addText(b.desc, { x: bx + 0.2, y: 4.25, w: 2.4, h: 1.4, fontSize: 11, fontFace: "Calibri", color: midGray });
  });
}

// --- SLIDE 3: Background ---
pg++;
{
  const s = pres.addSlide();
  addHeader(s, "2. Background");
  addFooter(s, pg);

  // Two-column layout
  // Gainsight box
  s.addShape(pres.ShapeType.rect, { x: 0.6, y: 1.3, w: 5.8, h: 2.8, fill: { color: lightGray }, rectRadius: 0.1 });
  s.addText("Gainsight", { x: 0.9, y: 1.45, w: 5.2, h: 0.4, fontSize: 18, fontFace: "Calibri", bold: true, color: navy });
  s.addText("System of record for CSMs. Unified view of customer health, engagement, time tracking, and BAU activities. Production go-live: 30 March 2026.", {
    x: 0.9, y: 1.95, w: 5.2, h: 1.8, fontSize: 12, fontFace: "Calibri", color: darkText
  });

  // CLARA box
  s.addShape(pres.ShapeType.rect, { x: 6.8, y: 1.3, w: 5.8, h: 2.8, fill: { color: lightGray }, rectRadius: 0.1 });
  s.addText("CLARA", { x: 7.1, y: 1.45, w: 5.2, h: 0.4, fontSize: 18, fontFace: "Calibri", bold: true, color: navy });
  s.addText("Cross-functional IRP adoption tracker. Serves CSMs, product, implementation, and advisory teams. Used in weekly Portfolio Reviews. Primary migration reporting surface.", {
    x: 7.1, y: 1.95, w: 5.2, h: 1.8, fontSize: 12, fontFace: "Calibri", color: darkText
  });

  // Problem / Goal
  s.addShape(pres.ShapeType.rect, { x: 0.6, y: 4.5, w: 12, h: 0.06, fill: { color: blue } });
  s.addText("The Problem", { x: 0.6, y: 4.8, w: 3, h: 0.35, fontSize: 14, fontFace: "Calibri", bold: true, color: navy });
  s.addText("CSMs must duplicate data entry across both systems. Cross-functional teams lose visibility into CSM-side activities.", {
    x: 0.6, y: 5.2, w: 12, h: 0.5, fontSize: 12, fontFace: "Calibri", color: darkText
  });
  s.addText("The Goal", { x: 0.6, y: 5.8, w: 3, h: 0.35, fontSize: 14, fontFace: "Calibri", bold: true, color: blue });
  s.addText("Enable CSMs to work primarily in Gainsight while ensuring IRP adoption data flows seamlessly to CLARA, and cross-functional inputs in CLARA are visible back in Gainsight.", {
    x: 0.6, y: 6.15, w: 12, h: 0.5, fontSize: 12, fontFace: "Calibri", color: darkText
  });
}

// --- SLIDE 4: Parties ---
pg++;
{
  const s = pres.addSlide();
  addHeader(s, "3. Parties & Stakeholders");
  addFooter(s, pg);

  // CLARA team
  s.addText("CLARA Team", { x: 0.8, y: 1.3, w: 5.5, h: 0.4, fontSize: 16, fontFace: "Calibri", bold: true, color: navy });
  const claraRows = [
    [{ text: "Name", options: tableHeaderOpts }, { text: "Role", options: tableHeaderOpts }],
    [{ text: "Azmain Hossain", options: tableCellOpts }, { text: "Programme Manager & Lead Developer", options: tableCellOpts }],
    [{ text: "Ben Brooks", options: tableCellAlt }, { text: "Product Owner, CLARA", options: tableCellAlt }],
    [{ text: "Richard Dosoo", options: tableCellOpts }, { text: "Programme & Operational Owner", options: tableCellOpts }],
    [{ text: "BenVH", options: tableCellAlt }, { text: "Infrastructure Engineer (AWS, CI/CD, App Factory)", options: tableCellAlt }],
  ];
  s.addTable(claraRows, { x: 0.8, y: 1.8, w: 5.5, colW: [2, 3.5], border: { pt: 0.5, color: "D1D5DB" } });

  // Gainsight team
  s.addText("Gainsight / Business Systems Team", { x: 6.8, y: 1.3, w: 5.5, h: 0.4, fontSize: 16, fontFace: "Calibri", bold: true, color: navy });
  const gsRows = [
    [{ text: "Name", options: tableHeaderOpts }, { text: "Role", options: tableHeaderOpts }],
    [{ text: "Tina Palumbo", options: tableCellOpts }, { text: "Business Systems, Gainsight Programme Lead", options: tableCellOpts }],
    [{ text: "Rajesh", options: tableCellAlt }, { text: "Solution Architect, Gainsight", options: tableCellAlt }],
    [{ text: "Shashank", options: tableCellOpts }, { text: "Technical Lead, Gainsight Application", options: tableCellOpts }],
    [{ text: "Nadeem", options: tableCellAlt }, { text: "Project Manager, Gainsight Programme", options: tableCellAlt }],
  ];
  s.addTable(gsRows, { x: 6.8, y: 1.8, w: 5.5, colW: [2, 3.5], border: { pt: 0.5, color: "D1D5DB" } });
}

// --- SLIDE 5: Guiding Principles ---
pg++;
{
  const s = pres.addSlide();
  addHeader(s, "4. Guiding Principles");
  addFooter(s, pg);

  const principles = [
    ["Gainsight is the system of record for CSM BAU.", "CSMs should not enter the same data in two systems."],
    ["CLARA is the system of record for cross-functional IRP tracking.", "Product, implementation, and advisory teams work in CLARA."],
    ["Integration must be bi-directional.", "Data flows both ways — CSM inputs and cross-functional inputs."],
    ["Neither system replaces the other.", "Gainsight covers full lifecycle. CLARA covers IRP adoption."],
    ["Start small, prove connectivity, then expand.", "POC must demonstrate end-to-end data flow first."],
    ["No disruption to active migrations.", "2026 scorecard target (30+ migrations) takes priority."],
  ];
  principles.forEach((p, i) => {
    const yPos = 1.3 + i * 0.95;
    const bgColor = i % 2 === 0 ? lightGray : white;
    s.addShape(pres.ShapeType.rect, { x: 0.6, y: yPos, w: 12, h: 0.85, fill: { color: bgColor }, rectRadius: 0.05 });
    s.addText(String(i + 1), { x: 0.7, y: yPos + 0.08, w: 0.5, h: 0.5, fontSize: 20, fontFace: "Calibri", bold: true, color: blue, align: "center" });
    s.addText(p[0], { x: 1.4, y: yPos + 0.05, w: 10.8, h: 0.35, fontSize: 13, fontFace: "Calibri", bold: true, color: navy });
    s.addText(p[1], { x: 1.4, y: yPos + 0.42, w: 10.8, h: 0.35, fontSize: 11, fontFace: "Calibri", color: midGray });
  });
}

// --- SLIDE 6: Scope Overview ---
pg++;
{
  const s = pres.addSlide();
  addHeader(s, "5. Scope — Phase Overview");
  addFooter(s, pg);

  // Phase boxes in a row
  const phases = [
    { num: "P1", title: "Foundation", items: "Accounts\n(Parent + Sub)\n\nCustomer\nWeekly Updates", color: "10B981" },
    { num: "P2", title: "Core IRP Data", items: "Contacts / Users\n\nBlockers\n(Bi-directional)\n\nSuccess Criteria", color: "F59E0B" },
    { num: "P3", title: "Extended Data", items: "Product Adoption\n\nTasks / Activity\n(Bi-directional)\n\nFull Case Feed", color: "8B5CF6" },
    { num: "P4+", title: "Future Roadmap", items: "MS 365 Context\n\nUsage Telemetry\n\nNPS Verbatim\n\nGS Health Scores", color: midGray },
  ];
  phases.forEach((p, i) => {
    const bx = 0.6 + i * 3.15;
    s.addShape(pres.ShapeType.rect, { x: bx, y: 1.4, w: 2.9, h: 5.2, fill: { color: white }, rectRadius: 0.1, line: { color: "D1D5DB", width: 1 } });
    s.addShape(pres.ShapeType.rect, { x: bx, y: 1.4, w: 2.9, h: 0.7, fill: { color: p.color }, rectRadius: 0.1 });
    // Fix bottom corners of header
    s.addShape(pres.ShapeType.rect, { x: bx, y: 1.8, w: 2.9, h: 0.35, fill: { color: p.color } });
    s.addText(p.num, { x: bx, y: 1.45, w: 2.9, h: 0.28, fontSize: 11, fontFace: "Calibri", bold: true, color: white, align: "center" });
    s.addText(p.title, { x: bx, y: 1.7, w: 2.9, h: 0.35, fontSize: 15, fontFace: "Calibri", bold: true, color: white, align: "center" });
    s.addText(p.items, { x: bx + 0.25, y: 2.4, w: 2.4, h: 3.8, fontSize: 12, fontFace: "Calibri", color: darkText, align: "center", valign: "top" });
  });

  // Arrow between phases
  for (let i = 0; i < 3; i++) {
    const ax = 0.6 + (i + 1) * 3.15 - 0.15;
    s.addText("\u25B6", { x: ax, y: 3.5, w: 0.3, h: 0.4, fontSize: 16, color: blue, align: "center" });
  }
}

// --- SLIDE 7: Phase 1 Detail ---
pg++;
{
  const s = pres.addSlide();
  addHeader(s, "5. Scope — Phase 1: Foundation", "Accounts & Customer Updates");
  addFooter(s, pg);

  const rows = [
    [{ text: "Source Object", options: tableHeaderOpts }, { text: "CLARA Target", options: tableHeaderOpts }, { text: "Direction", options: tableHeaderOpts }, { text: "Notes", options: tableHeaderOpts }],
    [{ text: "Account\n(Parent + Sub)", options: tableCellOpts }, { text: "parent_accounts /\ncustomers", options: tableCellOpts }, { text: "GS \u2192 CLARA", options: tableCellOpts }, { text: "Establishes account hierarchy. Must include parent-subsidiary relationships. CLARA currently holds 155+ active accounts.", options: tableCellOpts }],
    [{ text: "Customer Weekly\nUpdates", options: tableCellAlt }, { text: "customer_updates", options: tableCellAlt }, { text: "Bi-directional", options: { ...tableCellAlt, bold: true, color: blue } }, { text: "Per-account executive summaries and meeting notes. CLARA auto-generates these from transcribed weekly calls. CSMs also enter updates in Gainsight. Both sources must be visible in both systems.", options: tableCellAlt }],
  ];
  s.addTable(rows, { x: 0.6, y: 1.3, w: 12, colW: [2, 2, 1.5, 6.5], border: { pt: 0.5, color: "D1D5DB" }, rowH: [0.4, 1.0, 1.2] });
}

// --- SLIDE 8: Phase 2 Detail ---
pg++;
{
  const s = pres.addSlide();
  addHeader(s, "5. Scope — Phase 2: Core IRP Data", "Contacts, Blockers & Success Criteria");
  addFooter(s, pg);

  const rows = [
    [{ text: "Source Object", options: tableHeaderOpts }, { text: "CLARA Target", options: tableHeaderOpts }, { text: "Direction", options: tableHeaderOpts }, { text: "Notes", options: tableHeaderOpts }],
    [{ text: "Contact / User", options: tableCellOpts }, { text: "employees\n(CSM assignments)", options: tableCellOpts }, { text: "GS \u2192 CLARA", options: tableCellOpts }, { text: "Maps CSMs and key contacts to accounts.", options: tableCellOpts }],
    [{ text: "Case / Custom Object\n(Blocker)", options: tableCellAlt }, { text: "blockers", options: tableCellAlt }, { text: "Bi-directional", options: { ...tableCellAlt, bold: true, color: blue } }, { text: "CSM-created blockers originate in Gainsight. Product/implementation-created blockers originate in CLARA. Both systems must reflect the full set.", options: tableCellAlt }],
    [{ text: "Success Criteria\n(CSC)", options: tableCellOpts }, { text: "success_criteria", options: tableCellOpts }, { text: "Bi-directional", options: { ...tableCellOpts, bold: true, color: blue } }, { text: "IRP use case success criteria tracked by CSMs in Gainsight, supplemented by product teams in CLARA.", options: tableCellOpts }],
  ];
  s.addTable(rows, { x: 0.6, y: 1.3, w: 12, colW: [2, 2, 1.5, 6.5], border: { pt: 0.5, color: "D1D5DB" }, rowH: [0.4, 0.7, 1.0, 0.9] });
}

// --- SLIDE 9: Phase 3 Detail ---
pg++;
{
  const s = pres.addSlide();
  addHeader(s, "5. Scope — Phase 3: Extended Data", "Adoption, Tasks & Case Feed");
  addFooter(s, pg);

  const rows = [
    [{ text: "Source Object", options: tableHeaderOpts }, { text: "CLARA Target", options: tableHeaderOpts }, { text: "Direction", options: tableHeaderOpts }, { text: "Notes", options: tableHeaderOpts }],
    [{ text: "Product Adoption\n(PAT)", options: tableCellOpts }, { text: "product_adoption_\ntracking", options: tableCellOpts }, { text: "GS \u2192 CLARA", options: tableCellOpts }, { text: "Adoption milestone data for IRP products.", options: tableCellOpts }],
    [{ text: "Task / Activity", options: tableCellAlt }, { text: "action_plans /\nitems", options: tableCellAlt }, { text: "Bi-directional", options: { ...tableCellAlt, bold: true, color: blue } }, { text: "Cross-functional action items. CSM tasks from Gainsight, product/implementation tasks from CLARA.", options: tableCellAlt }],
    [{ text: "Full Case Feed", options: tableCellOpts }, { text: "case_feed\n(new table)", options: tableCellOpts }, { text: "GS \u2192 CLARA", options: tableCellOpts }, { text: "Historical case context for blocker analysis and reporting. New data object in CLARA.", options: tableCellOpts }],
  ];
  s.addTable(rows, { x: 0.6, y: 1.3, w: 12, colW: [2, 2, 1.5, 6.5], border: { pt: 0.5, color: "D1D5DB" }, rowH: [0.4, 0.7, 0.9, 0.8] });
}

// --- SLIDE 10: Phase 4+ Roadmap ---
pg++;
{
  const s = pres.addSlide();
  addHeader(s, "5. Scope — Phase 4+ Roadmap", "Future state — requires separate scoping after Phases 1-3");
  addFooter(s, pg);

  const rows = [
    [{ text: "Capability", options: tableHeaderOpts }, { text: "Description", options: tableHeaderOpts }, { text: "Dependency", options: tableHeaderOpts }],
    [{ text: "Microsoft 365 Context\n(Graph API)", options: tableCellOpts }, { text: "Email + meeting signals per account to enrich CS Agent synthesis", options: tableCellOpts }, { text: "Graph API access, security review", options: tableCellOpts }],
    [{ text: "Usage Telemetry\n(MIDAS / Mixpanel)", options: tableCellAlt }, { text: "Product usage signals for adoption scoring and proactive engagement", options: tableCellAlt }, { text: "MIDAS integration, data pipeline", options: tableCellAlt }],
    [{ text: "NPS Verbatim &\nDetractor CTAs", options: tableCellOpts }, { text: "Survey data for sentiment overlay (closes AMBER scorecard item)", options: tableCellOpts }, { text: "Qualtrics integration", options: tableCellOpts }],
    [{ text: "Gainsight Health Scores\n(read-only)", options: tableCellAlt }, { text: "CSM qualitative health as context signal — Gainsight remains SoR", options: tableCellAlt }, { text: "Gainsight reporting API", options: tableCellAlt }],
    [{ text: "Write-back to\nSalesforce / Gainsight", options: tableCellOpts }, { text: "Gated, future-state capability — requires governance approval", options: tableCellOpts }, { text: "Governance framework, security review", options: tableCellOpts }],
  ];
  s.addTable(rows, { x: 0.6, y: 1.3, w: 12, colW: [3, 5.5, 3.5], border: { pt: 0.5, color: "D1D5DB" } });
}

// --- SLIDE 11: Architecture Diagram ---
pg++;
{
  const s = pres.addSlide();
  addHeader(s, "6. Integration Architecture", "Proposed pattern based on 12 March 2026 discussion");
  addFooter(s, pg);

  // Salesforce box
  s.addShape(pres.ShapeType.rect, { x: 1.5, y: 1.5, w: 2.8, h: 1.0, fill: { color: lightGray }, rectRadius: 0.1, line: { color: "D1D5DB", width: 1 } });
  s.addText("Salesforce (CRM)", { x: 1.5, y: 1.65, w: 2.8, h: 0.7, fontSize: 14, fontFace: "Calibri", bold: true, color: navy, align: "center" });

  // Arrow down
  s.addText("\u25BC", { x: 2.6, y: 2.5, w: 0.5, h: 0.4, fontSize: 18, color: midGray, align: "center" });

  // Gainsight box (central, larger)
  s.addShape(pres.ShapeType.rect, { x: 0.8, y: 2.9, w: 4.2, h: 2.2, fill: { color: "EEF2FF" }, rectRadius: 0.1, line: { color: blue, width: 2 } });
  s.addText("Gainsight", { x: 0.8, y: 3.0, w: 4.2, h: 0.45, fontSize: 18, fontFace: "Calibri", bold: true, color: navy, align: "center" });
  s.addText("CSM System of Record", { x: 0.8, y: 3.4, w: 4.2, h: 0.3, fontSize: 11, fontFace: "Calibri", color: blue, align: "center" });
  s.addText("Health  |  Engagement  |  Time Tracking\nUse Cases  |  Blockers  |  Activities", {
    x: 1.0, y: 3.85, w: 3.8, h: 0.8, fontSize: 10, fontFace: "Calibri", color: midGray, align: "center"
  });

  // CLARA box (right side)
  s.addShape(pres.ShapeType.rect, { x: 8.0, y: 2.9, w: 4.2, h: 2.2, fill: { color: "EEF2FF" }, rectRadius: 0.1, line: { color: navy, width: 2 } });
  s.addText("CLARA", { x: 8.0, y: 3.0, w: 4.2, h: 0.45, fontSize: 18, fontFace: "Calibri", bold: true, color: navy, align: "center" });
  s.addText("Cross-Functional IRP Tracker", { x: 8.0, y: 3.4, w: 4.2, h: 0.3, fontSize: 11, fontFace: "Calibri", color: blue, align: "center" });
  s.addText("Migration Reporting  |  Portfolio Reviews\nBlockers  |  Adoption  |  Action Plans", {
    x: 8.2, y: 3.85, w: 3.8, h: 0.8, fontSize: 10, fontFace: "Calibri", color: midGray, align: "center"
  });

  // Arrows between Gainsight and CLARA
  // Batch arrow (top)
  s.addShape(pres.ShapeType.rect, { x: 5.1, y: 3.2, w: 2.8, h: 0.04, fill: { color: "10B981" } });
  s.addText("\u25B6", { x: 7.6, y: 3.0, w: 0.4, h: 0.4, fontSize: 14, color: "10B981", align: "center" });
  s.addShape(pres.ShapeType.rect, { x: 5.3, y: 3.35, w: 2.4, h: 0.5, fill: { color: "ECFDF5" }, rectRadius: 0.05 });
  s.addText("Batch (S3)\nAccounts, Contacts", { x: 5.3, y: 3.35, w: 2.4, h: 0.5, fontSize: 8, fontFace: "Calibri", color: "059669", align: "center" });

  // API arrow (bottom, bi-directional)
  s.addShape(pres.ShapeType.rect, { x: 5.1, y: 4.3, w: 2.8, h: 0.04, fill: { color: blue } });
  s.addText("\u25C0", { x: 4.8, y: 4.1, w: 0.4, h: 0.4, fontSize: 14, color: blue, align: "center" });
  s.addText("\u25B6", { x: 7.6, y: 4.1, w: 0.4, h: 0.4, fontSize: 14, color: blue, align: "center" });
  s.addShape(pres.ShapeType.rect, { x: 5.3, y: 4.45, w: 2.4, h: 0.5, fill: { color: "EFF6FF" }, rectRadius: 0.05 });
  s.addText("API (Real-time)\nBlockers, Tasks, Updates", { x: 5.3, y: 4.45, w: 2.4, h: 0.5, fontSize: 8, fontFace: "Calibri", color: blue, align: "center" });

  // App Factory middleware box
  s.addShape(pres.ShapeType.rect, { x: 5.5, y: 5.5, w: 2.2, h: 0.8, fill: { color: "FEF3C7" }, rectRadius: 0.1, line: { color: "F59E0B", width: 1 } });
  s.addText("App Factory\nMiddleware", { x: 5.5, y: 5.55, w: 2.2, h: 0.7, fontSize: 10, fontFace: "Calibri", bold: true, color: "92400E", align: "center" });
  s.addText("\u25B2", { x: 6.3, y: 5.15, w: 0.5, h: 0.35, fontSize: 12, color: "F59E0B", align: "center" });

  // Databricks box (bottom left)
  s.addShape(pres.ShapeType.rect, { x: 1.5, y: 5.5, w: 2.8, h: 0.8, fill: { color: lightGray }, rectRadius: 0.1, line: { color: "D1D5DB", width: 1 } });
  s.addText("Databricks\nReporting & Analytics", { x: 1.5, y: 5.55, w: 2.8, h: 0.7, fontSize: 11, fontFace: "Calibri", bold: true, color: navy, align: "center" });
  s.addText("\u25BC", { x: 2.6, y: 5.1, w: 0.5, h: 0.4, fontSize: 14, color: midGray, align: "center" });
}

// --- SLIDE 12: Integration Methods ---
pg++;
{
  const s = pres.addSlide();
  addHeader(s, "6. Integration Methods", "Batch vs real-time by data type");
  addFooter(s, pg);

  const batchOpts = { ...tableCellOpts, color: "059669", bold: true };
  const batchAltOpts = { ...tableCellAlt, color: "059669", bold: true };
  const apiOpts = { ...tableCellOpts, color: blue, bold: true };
  const apiAltOpts = { ...tableCellAlt, color: blue, bold: true };

  const rows = [
    [{ text: "Data Type", options: tableHeaderOpts }, { text: "Method", options: tableHeaderOpts }, { text: "Frequency", options: tableHeaderOpts }, { text: "Rationale", options: tableHeaderOpts }],
    [{ text: "Account (Parent + Sub)", options: tableCellOpts }, { text: "Batch (S3)", options: batchOpts }, { text: "Daily", options: tableCellOpts }, { text: "Low change frequency. Proven and low-risk.", options: tableCellOpts }],
    [{ text: "Customer Weekly Updates", options: tableCellAlt }, { text: "API (real-time)", options: apiAltOpts }, { text: "On create/update", options: tableCellAlt }, { text: "Auto-generated summaries from CLARA, CSM updates from Gainsight.", options: tableCellAlt }],
    [{ text: "Contact / User", options: tableCellOpts }, { text: "Batch (S3)", options: batchOpts }, { text: "Daily", options: tableCellOpts }, { text: "Low change frequency.", options: tableCellOpts }],
    [{ text: "Blocker (Case / Custom)", options: tableCellAlt }, { text: "API (real-time)", options: apiAltOpts }, { text: "On create/update", options: tableCellAlt }, { text: "CSMs and product teams need immediacy. Delay causes duplication.", options: tableCellAlt }],
    [{ text: "Success Criteria", options: tableCellOpts }, { text: "API (real-time)", options: apiOpts }, { text: "On create/update", options: tableCellOpts }, { text: "Active during engagements. Timeliness matters.", options: tableCellOpts }],
    [{ text: "Product Adoption (PAT)", options: tableCellAlt }, { text: "Batch (S3)", options: batchAltOpts }, { text: "Daily", options: tableCellAlt }, { text: "Milestone data, not time-critical.", options: tableCellAlt }],
    [{ text: "Task / Activity", options: tableCellOpts }, { text: "API (real-time)", options: apiOpts }, { text: "On create/update", options: tableCellOpts }, { text: "Cross-functional coordination requires immediacy.", options: tableCellOpts }],
    [{ text: "Case Feed", options: tableCellAlt }, { text: "Batch (S3)", options: batchAltOpts }, { text: "Daily", options: tableCellAlt }, { text: "Historical context. No real-time requirement.", options: tableCellAlt }],
  ];
  s.addTable(rows, { x: 0.4, y: 1.3, w: 12.4, colW: [2.5, 1.8, 1.8, 6.3], border: { pt: 0.5, color: "D1D5DB" } });
}

// --- SLIDE 13: Auth & Connectivity ---
pg++;
{
  const s = pres.addSlide();
  addHeader(s, "6. Authentication & Connectivity");
  addFooter(s, pg);

  // Gainsight provides
  s.addText("Gainsight Team Provides:", { x: 0.8, y: 1.3, w: 5.5, h: 0.4, fontSize: 16, fontFace: "Calibri", bold: true, color: navy });
  const gsItems = [
    "API documentation (endpoints, schemas, rate limits, error handling)",
    "Authentication method and credentials (API key, OAuth, SSO — TBC)",
    "S3 bucket configuration for batch exchange (IAM roles, encryption)",
    "Sandbox / test environment access for POC",
  ];
  gsItems.forEach((item, i) => {
    const yy = 1.85 + i * 0.55;
    s.addShape(pres.ShapeType.rect, { x: 0.8, y: yy, w: 5.5, h: 0.45, fill: { color: i % 2 === 0 ? lightGray : white }, rectRadius: 0.05 });
    s.addText(`${i + 1}.  ${item}`, { x: 1.0, y: yy, w: 5.1, h: 0.45, fontSize: 11, fontFace: "Calibri", color: darkText, valign: "middle" });
  });

  // CLARA provides
  s.addText("CLARA Team Provides:", { x: 7.0, y: 1.3, w: 5.5, h: 0.4, fontSize: 16, fontFace: "Calibri", bold: true, color: navy });
  const clItems = [
    "CLARA API specification (REST endpoints for all in-scope objects)",
    "Authentication details for CLARA's API",
    "Data mapping document (GS field \u2192 CLARA field + transformations)",
    "Test environment access",
  ];
  clItems.forEach((item, i) => {
    const yy = 1.85 + i * 0.55;
    s.addShape(pres.ShapeType.rect, { x: 7.0, y: yy, w: 5.5, h: 0.45, fill: { color: i % 2 === 0 ? lightGray : white }, rectRadius: 0.05 });
    s.addText(`${i + 1}.  ${item}`, { x: 7.2, y: yy, w: 5.1, h: 0.45, fontSize: 11, fontFace: "Calibri", color: darkText, valign: "middle" });
  });

  // Middleware box
  s.addShape(pres.ShapeType.rect, { x: 0.8, y: 4.5, w: 11.7, h: 0.06, fill: { color: blue } });
  s.addText("Middleware — App Factory", { x: 0.8, y: 4.8, w: 5, h: 0.4, fontSize: 16, fontFace: "Calibri", bold: true, color: navy });
  s.addText("Integration orchestration managed through App Factory (CLARA's AWS infrastructure layer). Handles API orchestration, retry logic, data transformation, error logging, rate limiting, and backpressure management. This approach is vendor-agnostic — the integration layer can be adapted if underlying systems change.", {
    x: 0.8, y: 5.3, w: 11.7, h: 1.2, fontSize: 12, fontFace: "Calibri", color: darkText
  });
}

// --- SLIDE 14: Responsibilities ---
pg++;
{
  const s = pres.addSlide();
  addHeader(s, "7. Responsibilities");
  addFooter(s, pg);

  // GS team
  s.addShape(pres.ShapeType.rect, { x: 0.6, y: 1.3, w: 3.8, h: 0.5, fill: { color: navy }, rectRadius: 0.05 });
  s.addText("Gainsight Team Owns", { x: 0.6, y: 1.3, w: 3.8, h: 0.5, fontSize: 13, fontFace: "Calibri", bold: true, color: white, align: "center" });
  const gsResp = [
    "API documentation & access provisioning",
    "S3 bucket setup & batch export config",
    "Sandbox environment for POC",
    "Data export scheduling & reliability",
    "Webhook / event config for real-time sync",
    "Data model documentation",
    "CSM change management & training",
    "GS-side testing & validation",
    "Project management (Nadeem)",
  ];
  gsResp.forEach((r, i) => {
    s.addText(`\u2022  ${r}`, { x: 0.7, y: 1.9 + i * 0.42, w: 3.6, h: 0.38, fontSize: 10, fontFace: "Calibri", color: darkText });
  });

  // CLARA team
  s.addShape(pres.ShapeType.rect, { x: 4.7, y: 1.3, w: 3.8, h: 0.5, fill: { color: navy }, rectRadius: 0.05 });
  s.addText("CLARA Team Owns", { x: 4.7, y: 1.3, w: 3.8, h: 0.5, fontSize: 13, fontFace: "Calibri", bold: true, color: white, align: "center" });
  const clResp = [
    "API endpoints for receiving & sending data",
    "Data transformation & mapping logic",
    "Storage, indexing & display of GS data",
    "Integration orchestration (App Factory)",
    "CLARA-side testing & validation",
    "Reporting & dashboards",
    "Technical architecture & infrastructure",
  ];
  clResp.forEach((r, i) => {
    s.addText(`\u2022  ${r}`, { x: 4.8, y: 1.9 + i * 0.42, w: 3.6, h: 0.38, fontSize: 10, fontFace: "Calibri", color: darkText });
  });

  // Joint
  s.addShape(pres.ShapeType.rect, { x: 8.8, y: 1.3, w: 3.8, h: 0.5, fill: { color: blue }, rectRadius: 0.05 });
  s.addText("Joint Responsibilities", { x: 8.8, y: 1.3, w: 3.8, h: 0.5, fontSize: 13, fontFace: "Calibri", bold: true, color: white, align: "center" });
  const jtResp = [
    "Data mapping agreement",
    "Integration testing (end-to-end)",
    "Error handling & escalation procedures",
    "POC evaluation & go/no-go decision",
    "Ongoing monitoring & incident response",
  ];
  jtResp.forEach((r, i) => {
    s.addText(`\u2022  ${r}`, { x: 8.9, y: 1.9 + i * 0.42, w: 3.6, h: 0.38, fontSize: 10, fontFace: "Calibri", color: darkText });
  });
}

// --- SLIDE 15: POC Success Criteria ---
pg++;
{
  const s = pres.addSlide();
  addHeader(s, "8. Success Criteria — POC");
  addFooter(s, pg);

  const criteria = [
    ["Connectivity proven", "CLARA can authenticate with and read from the Gainsight API (or consume S3 exports)."],
    ["Account sync working", "At least 10 parent accounts with subsidiaries synced with correct hierarchy."],
    ["Blocker round-trip", "A blocker created in either system appears in the other within 5 minutes."],
    ["Data integrity", "Synced records match — no data loss, no field truncation, no encoding issues."],
    ["No regression", "CLARA's existing functionality (Portfolio Reviews, dashboards, reporting) is unaffected."],
    ["Performance", "API responses under 2 seconds. Batch jobs complete within agreed windows."],
  ];
  criteria.forEach((c, i) => {
    const yy = 1.3 + i * 0.9;
    s.addShape(pres.ShapeType.rect, { x: 0.6, y: yy, w: 12, h: 0.8, fill: { color: i % 2 === 0 ? lightGray : white }, rectRadius: 0.05 });
    s.addText(`${i + 1}`, { x: 0.7, y: yy + 0.05, w: 0.5, h: 0.5, fontSize: 22, fontFace: "Calibri", bold: true, color: blue, align: "center" });
    s.addText(c[0], { x: 1.4, y: yy + 0.05, w: 10.8, h: 0.3, fontSize: 13, fontFace: "Calibri", bold: true, color: navy });
    s.addText(c[1], { x: 1.4, y: yy + 0.4, w: 10.8, h: 0.3, fontSize: 11, fontFace: "Calibri", color: midGray });
  });
}

// --- SLIDE 16: Production Success Criteria ---
pg++;
{
  const s = pres.addSlide();
  addHeader(s, "8. Success Criteria — Production");
  addFooter(s, pg);

  const criteria = [
    "All Phase 1-3 data objects synchronised per the schedule defined in integration methods.",
    "CSMs can enter IRP use cases and blockers in Gainsight and see them reflected in CLARA without manual intervention.",
    "Cross-functional teams can enter blockers and action items in CLARA and have them visible in Gainsight without manual intervention.",
    "Zero instances of CSMs needing to double-enter data across both systems for objects covered by the integration.",
    "CLARA's management reporting accurately reflects data from both sources.",
    "Integration uptime of 99.5% during business hours (08:00-18:00 GMT).",
  ];
  criteria.forEach((c, i) => {
    const yy = 1.3 + i * 0.9;
    s.addShape(pres.ShapeType.rect, { x: 0.6, y: yy, w: 12, h: 0.75, fill: { color: i % 2 === 0 ? lightGray : white }, rectRadius: 0.05 });
    s.addText(`${i + 1}`, { x: 0.7, y: yy + 0.1, w: 0.5, h: 0.5, fontSize: 22, fontFace: "Calibri", bold: true, color: blue, align: "center" });
    s.addText(c, { x: 1.4, y: yy + 0.1, w: 10.8, h: 0.5, fontSize: 12, fontFace: "Calibri", color: darkText, valign: "middle" });
  });
}

// --- SLIDE 17: Timeline Constraints ---
pg++;
{
  const s = pres.addSlide();
  addHeader(s, "9. Timeline — Constraints");
  addFooter(s, pg);

  const constraints = [
    { title: "Gainsight Onboarding", detail: "30 March 2026 deadline (RMS, Cape, Predicate teams). No capacity for integration before this.", icon: "\u23F0" },
    { title: "Post-Launch Stabilisation", detail: "~4 weeks after go-live (April 2026) for Gainsight to stabilise with new user groups.", icon: "\u2699" },
    { title: "CLARA Graduate Onboarding", detail: "Two rotating graduates arriving 7 April 2026. Available for integration support from May.", icon: "\uD83C\uDF93" },
    { title: "CLARA Team Priority", detail: "2026 insurance scorecard target (30+ migrations) is the primary obligation. Integration is secondary.", icon: "\u26A0" },
  ];
  constraints.forEach((c, i) => {
    const yy = 1.4 + i * 1.35;
    s.addShape(pres.ShapeType.rect, { x: 0.6, y: yy, w: 12, h: 1.15, fill: { color: i % 2 === 0 ? lightGray : white }, rectRadius: 0.1 });
    s.addShape(pres.ShapeType.rect, { x: 0.6, y: yy, w: 0.08, h: 1.15, fill: { color: i === 3 ? "EF4444" : blue } });
    s.addText(c.title, { x: 1.0, y: yy + 0.1, w: 10, h: 0.4, fontSize: 15, fontFace: "Calibri", bold: true, color: navy });
    s.addText(c.detail, { x: 1.0, y: yy + 0.55, w: 11, h: 0.45, fontSize: 12, fontFace: "Calibri", color: midGray });
  });
}

// --- SLIDE 18: Milestones ---
pg++;
{
  const s = pres.addSlide();
  addHeader(s, "9. Proposed Milestones");
  addFooter(s, pg);

  const rows = [
    [{ text: "Phase", options: tableHeaderOpts }, { text: "Milestone", options: tableHeaderOpts }, { text: "Target", options: tableHeaderOpts }, { text: "Owner", options: tableHeaderOpts }],
    [{ text: "0", options: tableCellOpts }, { text: "Charter signed off by both teams", options: tableCellOpts }, { text: "TBD", options: tableCellOpts }, { text: "Azmain / Tina", options: tableCellOpts }],
    [{ text: "0", options: tableCellAlt }, { text: "Gainsight API documentation shared", options: tableCellAlt }, { text: "TBD", options: tableCellAlt }, { text: "Rajesh / Shashank", options: tableCellAlt }],
    [{ text: "0", options: tableCellOpts }, { text: "CLARA API specification shared", options: tableCellOpts }, { text: "TBD", options: tableCellOpts }, { text: "Azmain / BenVH", options: tableCellOpts }],
    [{ text: "0", options: tableCellAlt }, { text: "Data mapping document agreed", options: tableCellAlt }, { text: "TBD", options: tableCellAlt }, { text: "Joint", options: tableCellAlt }],
    [{ text: "1", options: tableCellOpts }, { text: "POC environment setup (sandbox both sides)", options: tableCellOpts }, { text: "TBD", options: tableCellOpts }, { text: "Joint", options: tableCellOpts }],
    [{ text: "1", options: tableCellAlt }, { text: "POC: Batch account sync + customer updates", options: tableCellAlt }, { text: "TBD", options: tableCellAlt }, { text: "Joint", options: tableCellAlt }],
    [{ text: "1", options: tableCellOpts }, { text: "POC: Real-time blocker sync", options: tableCellOpts }, { text: "TBD", options: tableCellOpts }, { text: "Joint", options: tableCellOpts }],
    [{ text: "1", options: tableCellAlt }, { text: "POC evaluation and go/no-go decision", options: tableCellAlt }, { text: "TBD", options: tableCellAlt }, { text: "Joint + Governance", options: tableCellAlt }],
    [{ text: "2", options: tableCellOpts }, { text: "Phase 2 production build", options: tableCellOpts }, { text: "TBD", options: tableCellOpts }, { text: "Joint", options: tableCellOpts }],
    [{ text: "3", options: tableCellAlt }, { text: "Phase 3 production build", options: tableCellAlt }, { text: "TBD", options: tableCellAlt }, { text: "Joint", options: tableCellAlt }],
    [{ text: "4+", options: tableCellOpts }, { text: "Phase 4+ scoping begins", options: tableCellOpts }, { text: "TBD", options: tableCellOpts }, { text: "Joint", options: tableCellOpts }],
  ];
  s.addTable(rows, { x: 0.4, y: 1.2, w: 12.4, colW: [0.8, 5.5, 1.2, 4.9], border: { pt: 0.5, color: "D1D5DB" } });
}

// --- SLIDE 19: Governance Checkpoints ---
pg++;
{
  const s = pres.addSlide();
  addHeader(s, "9. Governance Checkpoints");
  addFooter(s, pg);

  s.addText("Integration work reviewed as part of CLARA governance (fortnightly Tuesday reviews, facilitated by Natalia Plant).", {
    x: 0.8, y: 1.3, w: 11.5, h: 0.5, fontSize: 13, fontFace: "Calibri", color: darkText
  });

  const gates = [
    { num: "Gate 1", title: "Charter Approval", desc: "Both teams and governance leads sign off on this charter." },
    { num: "Gate 2", title: "POC Go / No-Go", desc: "Based on POC success criteria (Section 8). All six criteria must be met." },
    { num: "Gate 3", title: "Phase 2 Go / No-Go", desc: "Based on POC results and resource availability." },
    { num: "Gate 4", title: "Phase 3 Go / No-Go", desc: "Based on Phase 2 stability and remaining scope." },
  ];
  gates.forEach((g, i) => {
    const bx = 0.6 + i * 3.1;
    s.addShape(pres.ShapeType.rect, { x: bx, y: 2.3, w: 2.85, h: 3.0, fill: { color: lightGray }, rectRadius: 0.1 });
    s.addShape(pres.ShapeType.rect, { x: bx, y: 2.3, w: 2.85, h: 0.06, fill: { color: blue } });
    s.addText(g.num, { x: bx + 0.2, y: 2.55, w: 2.45, h: 0.35, fontSize: 12, fontFace: "Calibri", bold: true, color: blue });
    s.addText(g.title, { x: bx + 0.2, y: 2.95, w: 2.45, h: 0.4, fontSize: 15, fontFace: "Calibri", bold: true, color: navy });
    s.addText(g.desc, { x: bx + 0.2, y: 3.5, w: 2.45, h: 1.4, fontSize: 11, fontFace: "Calibri", color: midGray });
  });

  // Arrows between gates
  for (let i = 0; i < 3; i++) {
    const ax = 0.6 + (i + 1) * 3.1 - 0.15;
    s.addText("\u25B6", { x: ax, y: 3.3, w: 0.3, h: 0.4, fontSize: 16, color: blue, align: "center" });
  }
}

// --- SLIDE 20: Risks (1) ---
pg++;
{
  const s = pres.addSlide();
  addHeader(s, "10. Risks & Mitigations", "Risks 1-4");
  addFooter(s, pg);

  const risks = [
    { id: "1", risk: "Gainsight API limitations prevent real-time sync for blockers/tasks", sev: "HIGH", mit: "POC specifically tests real-time capability. Fallback: near-real-time batch (every 15 min) via S3." },
    { id: "2", risk: "Integration work diverts CLARA team from migration support", sev: "HIGH", mit: "Integration is explicitly secondary. Governed via fortnightly reviews. Graduates (from May) allocated to integration." },
    { id: "3", risk: "Data model mismatch between Gainsight and CLARA", sev: "MEDIUM", mit: "Data mapping agreed before build. Transformation centralised in App Factory middleware." },
    { id: "4", risk: "Gainsight team capacity constrained by RMS onboarding", sev: "MEDIUM", mit: "Timeline accounts for March-April stabilisation. No POC work until May at earliest." },
  ];
  const sevColor = { HIGH: "EF4444", MEDIUM: "F59E0B" };
  risks.forEach((r, i) => {
    const yy = 1.3 + i * 1.4;
    s.addShape(pres.ShapeType.rect, { x: 0.6, y: yy, w: 12, h: 1.2, fill: { color: i % 2 === 0 ? lightGray : white }, rectRadius: 0.05 });
    s.addShape(pres.ShapeType.rect, { x: 0.6, y: yy, w: 0.08, h: 1.2, fill: { color: sevColor[r.sev] } });
    s.addText(r.sev, { x: 0.9, y: yy + 0.1, w: 0.9, h: 0.3, fontSize: 9, fontFace: "Calibri", bold: true, color: sevColor[r.sev] });
    s.addText(`R${r.id}: ${r.risk}`, { x: 1.8, y: yy + 0.1, w: 10.5, h: 0.35, fontSize: 12, fontFace: "Calibri", bold: true, color: navy });
    s.addText(`Mitigation: ${r.mit}`, { x: 1.8, y: yy + 0.55, w: 10.5, h: 0.5, fontSize: 11, fontFace: "Calibri", color: midGray });
  });
}

// --- SLIDE 21: Risks (2) ---
pg++;
{
  const s = pres.addSlide();
  addHeader(s, "10. Risks & Mitigations", "Risks 5-8");
  addFooter(s, pg);

  const risks = [
    { id: "5", risk: "Bi-directional sync creates data conflicts", sev: "MEDIUM", mit: "Clear ownership rules per data type. Conflict resolution: source system wins. Audit trail for all sync ops." },
    { id: "6", risk: "Scope creep into Phase 4+ items during POC", sev: "MEDIUM", mit: "Phase 4+ explicitly deferred. Any additions require governance approval and charter amendment." },
    { id: "7", risk: "CSM adoption of new Gainsight IRP workflows is low", sev: "MEDIUM", mit: "Gainsight team owns CSM change management and training. CLARA provides cross-functional docs." },
    { id: "8", risk: "Authentication/security review delays access provisioning", sev: "LOW", mit: "Raise security review requests early (Phase 0). Both teams engage security contacts in parallel." },
  ];
  const sevColor = { HIGH: "EF4444", MEDIUM: "F59E0B", LOW: "10B981" };
  risks.forEach((r, i) => {
    const yy = 1.3 + i * 1.4;
    s.addShape(pres.ShapeType.rect, { x: 0.6, y: yy, w: 12, h: 1.2, fill: { color: i % 2 === 0 ? lightGray : white }, rectRadius: 0.05 });
    s.addShape(pres.ShapeType.rect, { x: 0.6, y: yy, w: 0.08, h: 1.2, fill: { color: sevColor[r.sev] } });
    s.addText(r.sev, { x: 0.9, y: yy + 0.1, w: 0.9, h: 0.3, fontSize: 9, fontFace: "Calibri", bold: true, color: sevColor[r.sev] });
    s.addText(`R${r.id}: ${r.risk}`, { x: 1.8, y: yy + 0.1, w: 10.5, h: 0.35, fontSize: 12, fontFace: "Calibri", bold: true, color: navy });
    s.addText(`Mitigation: ${r.mit}`, { x: 1.8, y: yy + 0.55, w: 10.5, h: 0.5, fontSize: 11, fontFace: "Calibri", color: midGray });
  });
}

// --- SLIDE 22: Change Control ---
pg++;
{
  const s = pres.addSlide();
  addHeader(s, "11. Change Control");
  addFooter(s, pg);

  s.addText("Any changes to scope, timeline, or responsibilities must follow this process:", {
    x: 0.8, y: 1.3, w: 11.5, h: 0.5, fontSize: 14, fontFace: "Calibri", color: darkText, bold: true
  });

  const steps = [
    "Raised in writing (email or shared document comment)",
    "Reviewed at the next fortnightly governance session",
    "Agreed by both CLARA lead (Azmain) and Gainsight lead (Tina)",
    "Approved by governance (Natalia Orzechowska)",
    "Documented as a charter amendment with version number and date",
  ];
  steps.forEach((st, i) => {
    const yy = 2.2 + i * 0.85;
    s.addShape(pres.ShapeType.ellipse, { x: 1.0, y: yy + 0.05, w: 0.55, h: 0.55, fill: { color: blue } });
    s.addText(String(i + 1), { x: 1.0, y: yy + 0.05, w: 0.55, h: 0.55, fontSize: 18, fontFace: "Calibri", bold: true, color: white, align: "center", valign: "middle" });
    s.addText(st, { x: 1.8, y: yy, w: 10, h: 0.65, fontSize: 14, fontFace: "Calibri", color: darkText, valign: "middle" });
    if (i < 4) {
      s.addText("|", { x: 1.15, y: yy + 0.55, w: 0.25, h: 0.35, fontSize: 16, color: "D1D5DB", align: "center" });
    }
  });

  // Callout
  s.addShape(pres.ShapeType.rect, { x: 0.8, y: 6.2, w: 11.7, h: 0.6, fill: { color: "FEF2F2" }, rectRadius: 0.05, line: { color: "EF4444", width: 1 } });
  s.addText("No work outside the defined scope will be undertaken without an approved charter amendment.", {
    x: 1.0, y: 6.2, w: 11.3, h: 0.6, fontSize: 12, fontFace: "Calibri", bold: true, color: "991B1B", valign: "middle"
  });
}

// --- SLIDE 23: Assumptions ---
pg++;
{
  const s = pres.addSlide();
  addHeader(s, "12. Assumptions");
  addFooter(s, pg);

  const assumptions = [
    "Gainsight will have stable API and S3 export capabilities available for the POC.",
    "The Gainsight team will provide dedicated technical resource (Rajesh/Shashank) for integration sessions.",
    "CLARA's existing AWS infrastructure (App Factory) can support the integration middleware without additional provisioning.",
    "Both teams will have sandbox/test environments available that mirror production data structures.",
    "CSMs will have been trained on entering IRP data in Gainsight before the integration goes live.",
    "Salesforce data (accounts, contacts, cases) will continue to flow into Gainsight and does not need to be independently sourced by CLARA.",
  ];
  assumptions.forEach((a, i) => {
    const yy = 1.3 + i * 0.9;
    s.addShape(pres.ShapeType.rect, { x: 0.6, y: yy, w: 12, h: 0.75, fill: { color: i % 2 === 0 ? lightGray : white }, rectRadius: 0.05 });
    s.addText(String(i + 1), { x: 0.7, y: yy + 0.05, w: 0.5, h: 0.5, fontSize: 20, fontFace: "Calibri", bold: true, color: blue, align: "center" });
    s.addText(a, { x: 1.4, y: yy + 0.05, w: 10.8, h: 0.6, fontSize: 12, fontFace: "Calibri", color: darkText, valign: "middle" });
  });
}

// --- SLIDE 24: Closing ---
pg++;
{
  const s = pres.addSlide();
  s.addShape(pres.ShapeType.rect, { x: 0, y: 0, w: "100%", h: "100%", fill: { color: navy } });
  s.addShape(pres.ShapeType.rect, { x: 0, y: 5.2, w: "100%", h: 0.06, fill: { color: blue } });
  s.addText("Next Steps", {
    x: 0.8, y: 1.5, w: 11, h: 0.8, fontSize: 40, fontFace: "Calibri", bold: true, color: white
  });
  const nextSteps = [
    "Review and agree this charter (both teams)",
    "Exchange API documentation and specifications",
    "Agree data mapping document",
    "Schedule POC kick-off (post Gainsight stabilisation)",
  ];
  nextSteps.forEach((ns, i) => {
    s.addText(`${i + 1}.   ${ns}`, {
      x: 0.8, y: 2.8 + i * 0.65, w: 11, h: 0.5, fontSize: 18, fontFace: "Calibri", color: "CADCFC"
    });
  });
  s.addText("CLARA-Gainsight Integration Charter  |  v1.0 Draft  |  13 March 2026", {
    x: 0.8, y: 6.0, w: 11, h: 0.4, fontSize: 12, fontFace: "Calibri", color: "6B7280"
  });
}

const outPath = process.argv[2] || "CLARA_Gainsight_Integration_Charter_v1.pptx";
pres.writeFile({ fileName: outPath }).then(() => {
  console.log("PPTX created: " + outPath);
}).catch(err => {
  console.error("Error:", err);
});
