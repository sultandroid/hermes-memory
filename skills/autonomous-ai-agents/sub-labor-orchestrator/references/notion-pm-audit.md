# Notion Project Page PM Audit — Methodology

## When To Use
Audit a Notion project hub page from a Project Manager perspective. Use when the user asks for a PM review, health check, or governance audit of their Notion project workspace.

## Workflow
User order → Codex rewrites spec → Claude Code executes audit → Codex audits output → fix → deliver

## 10 PM Audit Criteria

### 1. Governance Clarity
- Is the organization chain clear? (Client → PMC → Consultant → Contractor → Subcontractors)
- Are approval roles and escalation paths documented?
- Are key contacts current (not departed/replaced)?

### 2. Status Snapshot Reliability
- Is the Status Snapshot up to date (not stale by >3 days)?
- Does it cover: DMP status, Programme position, PD contacts, meeting cadence?
- Are immediate management priorities visible?

### 3. Live Database Integrity
Page-embedded Notion databases (Issues, Tasks, Submittals, CRS Items, Stakeholders):
- Check ownership, due dates, status values, dependencies
- Verify that critical risks from narrative sections have corresponding DB entries
- Check for untracked items that should be in a database

### 4. Programme & Milestone Control
- Are RIBA stages mapped with status and dates?
- Are Stage 4 IFC milestones defined?
- Is there a dispute-resolution path for contested stages?
- Are approval dependencies visible?

### 5. Design Approval Workflow
- Is the IFC workflow documented step-by-step?
- Are SLAs for each review step defined (e.g., NRS 72h, CG 7-day baseline)?
- Are submittal codes (A/B/C/D) documented?

### 6. Scope & Responsibility Boundaries
- Are Samaya, NRS, subcontractor, authority, and outside-scope responsibilities separated?
- Is the ER/SOW/BOQ contractual basis referenced?
- Are exclusions (MoC-supplied items) clearly marked?

### 7. Contract & Commercial Control
- Are all contracts listed (Main, Designer, MEP, Supply, Subs)?
- Is the BOQ/pricing schedule referenced?
- Are unpopulated commercial baselines flagged?
- Are active claims/variations tracked?

### 8. Technical & Document Control
- Drawing numbering system documented?
- BIM/CDE standards defined?
- MEP/AV/Lighting/specification coverage complete?
- Locked technical decisions recorded?

### 9. Risk, Issue & Knowledge Gap Management
- Are critical risks and open issues tracked with owners?
- Are knowledge gaps documented with resolution paths?
- Are open NCRs, RFIs, and SIs visible with aging?

### 10. Page Usability as PM Control Hub
- Is the page length manageable? (<500 lines ideal)
- Are there duplicate/repetitive blocks bloating the page?
- Is there a clear separation between live databases and narrative context?
- Are there artifacts or tooling notes that don't belong on a PM hub?

## Finding Classification

| Severity | Definition |
|----------|------------|
| **CRITICAL** | Project-control failure or high-risk ambiguity — could materially affect approvals, programme, scope, or delivery |
| **MAJOR** | Material management weakness — stale statuses, incomplete registers, weak traceability |
| **MINOR** | Lower-risk improvements — repetitive entries, formatting drift, navigation issues |

## Finding Format

Each finding:
- **Lines:** L###-L###
- **Section:** Page section name
- **Issue:** Concise problem description
- **PM impact:** Why this matters
- **Evidence:** Summary from page content
- **Required action:** Specific corrective action
- **Owner role:** Who should own it
- **Closure evidence:** What proves it is fixed

## Common Findings (from real session)

### Duplicate Activity Update Blocks
Page-embedded scripts that append the same content repeatedly. Each block copies the full PROJECT MEMORY narrative. Fix: Keep last 3-5 meaningful entries; archive the rest to a sub-page.

### Critical Risks Without DB Links
Narrative sections flag risks but no Issues/Tasks DB entries exist. Fix: Create DB entries with owners, deadlines, and status.

### Developer/Tooling Artifacts on Live Page
Test paragraph from API, Session Update entries mentioning Codex/Claude/Kimi workflows. Fix: Move to a dev sub-page or remove entirely.

### Unpopulated Commercial Baselines
BOQ with zero rates, unpopulated pricing schedules. Fix: Populate or note the controlling document.

### Stale Register Snapshots
Registers marked Snapshot with no update date. Fix: Either connect to live source or set a refresh schedule.

## Output Structure

1. Executive Summary — 5-8 bullet overview focusing on project-control risk
2. Findings by Severity — CRITICAL, MAJOR, MINOR
3. Required Actions — Owner + priority for each finding
4. Missing Information — What could not be verified from the page
5. PM Readiness Verdict — Fit / Fit with conditions / Not fit
