# Project Study & Audit Workflow

Systematic study of a BIM project folder, document inventory, compliance audit against requirements, and structured reporting.

## Workflow

### Phase 1 — Study the Project

1. **Read PROJECT_MEMORY.md first** — always start here. It contains project identity, scope, phase, risks, action items, and stakeholder contacts.
2. **Explore the directory tree** — list all folders and files at depth 2-3. Note which standard subfolders have content vs. which are empty.
3. **Take inventory of existing documents** — identify deliverables, correspondence, submittals, drawings, BOQs, schedules, audits, PEP, VE reports. Record file types (PDF, HTML, MD, XLSX, DWG, RVT) and file sizes.
4. **Read key documents** — concept design docs, architectural audits, VE reports, BOQs, PEP (current revision). Understand the project's phase and maturity.
5. **Check `.claude/` directory** — for existing project-specific skills, configuration, or scripts.
6. **Check surrounding projects** in the parent directory for context (e.g., other Tqanny projects in the same portfolio).

### Phase 2 — Audit Against Requirements

1. **Listen for the specific question** — what is the user asking you to check compliance against? (design objectives, budget, schedule, VE proposals, code compliance, etc.)
2. **Search the relevant document** (PEP, BOQ, audit report, etc.) for the requirement using search_files() or grep.
   - Search in both Arabic and English key terms
   - Search for synonyms and translated equivalents
3. **If found:** report where in the document, how it's addressed, and what the current status/compliance level is.
4. **If NOT found:** confirm the absence, explain the significance of the gap, and recommend what action to take.

### Phase 3 — Report Findings

1. **State the verdict first** — tell the user the answer/conclusion before the supporting evidence.
2. **Use list format** for enumerated items — design objectives, findings, gaps, recommendations. Do NOT wrap short standalone items in narrative paragraphs.
3. **Use tables only for structured comparison data** — before/after, pre-VE/post-VE, compliance matrices with multiple columns.
4. **Reference absolute file paths** so the user can locate documents directly.
5. **Organize with clear section headers** for scanability.
6. **If applicable, advise from three perspectives:** Project Manager (schedule, coordination, approvals, risks), Technical Office Manager (design reviews, submittals, specs, technical gaps), Financial Manager (BOQ, cost, commercial).

## Format Preferences (User-Corrected — May 2026)

- **Lists > paragraphs** for enumerated items. When presenting N items of the same kind (objectives, findings, gaps, recommendations, action items), use a clean numbered or bulleted list.
- **Verdict first, evidence second.** State the conclusion, then support it.
- **Clear section headers** with `---` separators between major sections.
- **Minimal conversational filler** — be direct and specific.

## Pitfalls

- ❌ Don't skip PROJECT_MEMORY.md — it's the single source of truth for project context
- ❌ Don't assume all subfolders have content — many are empty at early phases (Concept Design, Schematic Design)
- ❌ Don't wrap short enumerated items in narrative — use lists (this was explicitly corrected)
- ❌ Don't stop at depth 1 — go depth 3-4 to find all documents
- ❌ Don't report compliance without verifying — search for exact terms in both Arabic and English
- ❌ Don't forget to check the PEP revision history — multiple revs may exist with different content coverage
- ❌ Don't overlook `.claude/` directory — may contain project-specific skills and workflows

## Example Session Flow

When user says "study this project" or "audit this project against [requirements]":

1. Read PROJECT_MEMORY.md → understand project identity, phase, budget, risks
2. Explore directories → inventory all existing documents
3. Read key docs → concept design, PEP, audit report, BOQ, VE report
4. Search for requirements in the relevant doc → determine compliance
5. Report: verdict first → evidence → gap analysis → recommended action
6. Present enumerated items as clean lists

### Real Example (Al Faw Visitor Center, May 2026)

User shared 12 architectural design objectives from Concept Design Rev 02.
Audit: searched PEP rev05 for all 12 objectives → **none found** → PEP's "Strategic Objectives" are execution-level, not design-level.
Reported: NOT COMPLIANT, showed PEP's actual objectives vs. missing design objectives, explained the gap impact (no traceability for design review gates, VE decisions, QC, handover criteria), recommended adding a "Design Compliance Matrix" to the PEP.
