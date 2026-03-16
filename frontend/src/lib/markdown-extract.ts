/**
 * Shared helpers for extracting project-specific content from
 * programme-wide weekly report markdown.
 */

/** Extract a ### section whose heading matches the predicate */
export function extractSection(
  lines: string[],
  matchHeading: (heading: string) => boolean,
  level: number,
): string[] {
  const prefix = "#".repeat(level) + " ";
  const parentPrefix = "#".repeat(level - 1) + " ";
  const result: string[] = [];
  let capturing = false;

  for (const line of lines) {
    if (line.startsWith(prefix)) {
      if (capturing) break; // hit next sibling section
      if (matchHeading(line.slice(prefix.length))) {
        capturing = true;
        // Don't include the heading itself — the UI already shows the project name
        continue;
      }
    } else if (capturing && line.startsWith(parentPrefix)) {
      break; // hit a parent ## section
    }

    if (capturing) {
      result.push(line);
    }
  }

  return result;
}

/** Get all lines within an h2 block matching a name (e.g., "emerging risks") */
export function extractH2Block(lines: string[], sectionName: string): string[] {
  const result: string[] = [];
  let capturing = false;

  for (const line of lines) {
    const h2Match = line.match(/^## (.+)/);
    if (h2Match) {
      if (capturing) break;
      if (h2Match[1].trim().toLowerCase().includes(sectionName)) {
        capturing = true;
        continue; // skip the heading
      }
    }
    if (capturing) result.push(line);
  }

  return result;
}

/** Filter bullet lines that mention the project name */
export function filterBullets(
  lines: string[],
  projectName: string,
): string[] {
  // Group lines into bullets (a bullet starts with "- ")
  const bullets: string[][] = [];
  for (const line of lines) {
    if (line.startsWith("- ")) {
      bullets.push([line]);
    } else if (bullets.length > 0 && line.trim() !== "") {
      bullets[bullets.length - 1].push(line);
    }
  }

  const terms: string[] = [projectName.toLowerCase()];
  // Also match key words from the project name (e.g., "Build in Five" → "build in five")
  const words = projectName.split(/[\s/()]+/).filter((w) => w.length > 3);
  terms.push(...words.map((w) => w.toLowerCase()));

  return bullets
    .filter((bullet) => {
      const text = bullet.join(" ").toLowerCase();
      return terms.some((term) => text.includes(term));
    })
    .map((bullet) => bullet.join("\n"));
}

/** Build match terms from a project name — significant keywords (>2 chars) */
function buildTerms(projectName: string): string[] {
  return projectName
    .toLowerCase()
    .split(/[\s/()]+/)
    .filter((w) => w.length > 2);
}

/**
 * Extract project-specific content from a programme-wide weekly report.
 * Pulls the matching project section, plus relevant risks and decisions.
 * Used by the Overview tab's "Current Status" section.
 */
export function extractProjectStatus(
  markdown: string,
  projectName: string,
): string {
  if (!projectName) return "";

  const lines = markdown.split("\n");
  const sections: string[] = [];
  const terms = buildTerms(projectName);

  // 1. Extract the matching project section from "## Project Progress"
  const wsContent = extractSection(lines, (heading) => {
    const h = heading.toLowerCase();
    return terms.some((term) => h.includes(term));
  }, 3);

  if (wsContent.length > 0) {
    sections.push(wsContent.join("\n").trim());
  }

  // 2. Extract relevant risks
  const risksBlock = extractH2Block(lines, "emerging risks");
  if (risksBlock.length > 0) {
    const relevantRisks = filterBullets(risksBlock, projectName);
    if (relevantRisks.length > 0) {
      sections.push("## Risks\n" + relevantRisks.join("\n"));
    }
  }

  // 3. Extract relevant decisions
  const decisionsBlock = extractH2Block(lines, "key decisions");
  if (decisionsBlock.length > 0) {
    const relevantDecisions = filterBullets(decisionsBlock, projectName);
    if (relevantDecisions.length > 0) {
      sections.push("## Decisions\n" + relevantDecisions.join("\n"));
    }
  }

  return sections.join("\n\n").trim();
}

/**
 * Extract project-specific headlines + progress from a weekly report.
 * Used by the Summaries tab to show only relevant content per project.
 */
export function extractProjectContent(
  markdown: string,
  projectName: string,
): string {
  if (!projectName || !markdown) return "";

  const lines = markdown.split("\n");
  const sections: string[] = [];
  const terms = buildTerms(projectName);

  // 1. Extract headlines mentioning this project
  const headlinesBlock = extractH2Block(lines, "headlines");
  if (headlinesBlock.length > 0) {
    const relevantHeadlines = filterBullets(headlinesBlock, projectName);
    if (relevantHeadlines.length > 0) {
      sections.push("## Headlines\n" + relevantHeadlines.join("\n"));
    }
  }

  // 2. Extract the matching project progress section
  const wsContent = extractSection(lines, (heading) => {
    const h = heading.toLowerCase();
    return terms.some((term) => h.includes(term));
  }, 3);

  if (wsContent.length > 0) {
    sections.push("## Progress\n" + wsContent.join("\n").trim());
  }

  return sections.join("\n\n").trim();
}
