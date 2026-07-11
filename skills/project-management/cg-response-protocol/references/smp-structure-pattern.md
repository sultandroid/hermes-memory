# Stakeholder Management Plan (SMP) — 5-Part Structure Pattern

Derived from Aseer Museum SMP Rev 04 (MOC-MUS-ASE-1K0-PL-0020, 23 pages, 56 roles).

## Document Architecture

```
PART 01 — Foundation & Governance
  §1  Document Control (Rev log, Doc ID, QC Block, CG Disposition)
  §2  Purpose, Scope & Definitions

PART 02 — Identification & Register
  §3  Stakeholder Identification (methodology, ecology diagram, snapshot)
  §4  Stakeholder Register (3 parts: T1+Client, T2 Specialists, T3+External+Ops)

PART 03 — Analysis & Strategy
  §5  Stakeholder Analysis (P/I matrix, Salience, Influence/Impact)
  §6  Engagement Assessment Matrix
  §7  Engagement Strategy

PART 04 — Execution Framework
  §8  Communication Plan
  §9  Roles & Responsibilities (RACI)
  §10 Interface Coordination
  §11 Escalation Procedure

PART 05 — Performance & Closeout
  §12 Monitoring & KPIs
  §13 Change Management for Engagement
  §14 Visual Tools & Schedules
  §15 Compliance & Authorization
```

## Key Design Elements

### Cover Page
- Dark navy background, white text
- 5 stakeholder logos (MoC, PMC, CG, NRS, Samaya) at bottom
- Bilingual title (EN primary, AR subtitle)
- Status badge: "Issued for CG Resubmission · Rev 04"
- Doc ref + date in top-right

### TOC Page
- Part dividers with SVG icons + color-coded left borders
- Section entries with page numbers right-aligned
- Disposition chip showing total sections/pages/roles
- Rev notice box at bottom

### Section Structure
- `.h2-row` with colored bar + SVG icon + h2 title + disposition chip
- `.sec-banner` for subsection headers
- `.eng-table` for structured data
- `.spec-strip` for key-value metadata blocks
- `.snapshot-grid` for KPI cards
- `.pg-footer` with doc ref, context, page number

### CG Disposition Matrix
- Single consolidated table across all review rounds
- `.cat-row` separators per round (dark background, white text)
- 7 columns: #, Round, CG Comment, Disposition, Ref, Status, Route/Scope
- Status badges: CLOSED (green), SUBMITTAL-PENDING (amber), IN-PROGRESS (blue), RE-OPENED (red)
- Comments that span rounds get RE-OPENED badge with explanation

### Stakeholder Register
- 9 attributes: ID, Stakeholder, Category, Role/Scope, Power (1-5), Interest (1-5), Engagement Method, Frequency, Escalation Route
- Split across 3 pages: T1+Client, T2 Specialists, T3+External+Ops
- `.cat-row` separators per stakeholder category
- Color-coded P/I pills

### Ecology Diagram
- Hub-and-spoke SVG: central "56 roles" hub with 6 surrounding groups
- Each group: colored left border, count badge, role descriptions
- Groups: Tier 1 (Internal), Tier 2 (Design), Tier 3 (Specialists), External, Ops/Public, Statutory

## CSS Classes Used
- `.page` — A4 sheet (210mm × 297mm, 12mm 16mm padding)
- `.page-cover` — full-bleed cover (padding: 0)
- `.compact` — tighter spacing for dense content
- `.tight` — even tighter for register pages
- `.eng-table` — standard data table
- `.spec-strip` — metadata block with left border
- `.snapshot-grid` / `.snapshot-card` — KPI cards
- `.h2-row` / `.h2-bar` — section header with colored bar
- `.pg-footer` — page footer with doc ref + page number
- `.badge-*` — status badges (pass, high, critical, low)
- `.cat-row` — category separator row in tables
- `.mono` — monospace font for codes/IDs
- `.disposition-chip` — section metadata badge
