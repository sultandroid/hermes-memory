# Aseer Museum SMP — CG-Facing Document Conventions

## Document Numbering

- Internal path: `MOC-ASEER-SIC-1K0-PL-0020` (Samaya Investment Company)
- CG-facing path: `MOC-MUS-ASE-1K0-PL-0020` (Museum Aseer)
- KPR reference: `MOC-MUS-ASE-1K0-KP-0001`

## Revision Numbering

Only count revisions **formally submitted to CG/MoC**. Internal iterations between submissions must NOT appear in the revision history table.

| Type | Example | Include? |
|------|---------|----------|
| Formal submission | Rev 00 (01-MAR-26) → CODE C | ✅ |
| Formal resubmission | Rev 01 (10-MAY-26) → REVIEW/CRS | ✅ |
| Internal QA draft | Rev 02 (11-MAY-26, 1 day after Rev 01) | ❌ |
| Internal CRS prep | Rev 03 (05-JUN-26) | ❌ |
| Formal resubmission | Rev 02 (16-JUN-26, formal) | ✅ |

## Revision History Rules

- Sort **descending** (most recent revision first: 04, 03, 02, 01, 00)
- **Prepared column: use department/team name** (`Technical Office`), not personal name — never use individual names like "Mohamed Sultan"
- **Approved column: use real person name** with `Eng.` prefix
- Only include revisions formally submitted to CG — no internal drafts
- Description: keep factual, no fluff. List what changed, not why.
- When adding a new revision, insert at the **TOP of the tbody** (before the current first row), not at the bottom.

## QC Sign-Off Chain

Standard 4-row structure:
1. QC-01: Technical Office (Prepared by) — Mohamed Sultan
2. QC-02: Document Controller — Hesham Abdelhamid
3. QC-03: QA/QC Manager — Mohamed Samir (on behalf, when vacant)
4. QC-04: Project Director (Approved by) — Eng. Waris Sultan

## Role-Based References in Plan

In the plan body, use role titles, not names. Reference the live KPR for current names:
- `"Per live KPR"` for most roles
- `"Name · Per live KPR"` for approved roles where name is known

Exception: QC Sign-off and Revision History tables need real names.

## CG Disposition Table

### Column Widths (standard)
| Column | Width | Reason |
|--------|-------|--------|
| # | 44px | Short code |
| Round | 65px | "R2 · 2-Jun" |
| CG Comment | 220-250px | Widest — longest text |
| Disposition | 120px | Short response |
| Ref | 50px | Short code |
| Status | 65px | Badge text |
| Route/Scope | 90px | Category name |

### Round Placement — ALL Rounds in ONE Table
All CG comment rounds (R1, R2, R3, etc.) must be in the **same table**, not split across separate tables on different pages. Adding a new round to a second table while Rounds 1-2 are in the first table is wrong — the user will flag it.

If the table overflows A4, split the table content (move some rows to the next page) but keep the round structure intact. Use a single `<table>` with multiple `<tbody>` sections if needed, or split rows at round boundaries but keep all rounds in the same logical table.

### Comment Preservation
CG comment text must be **preserved verbatim** — never summarize, shorten, or rephrase. Even typos (`"Structrual"`, `"seperatly"`, `"experianced"`) are part of the original CG record.

### Status Conventions
- **CLOSED** = CG confirmed resolution (Round 1 items)
- **COVERED** = Addressed in this revision, awaiting CG review (Round 2 SMP-scope)
- **SUBMITTAL-PENDING** = Depends on external submittals (DS/PQD)
- **IN-PROGRESS** = Action underway
- **RE-OPENED** = Closure withdrawn by CG

### Reference Attached CR Sheet for Approved Rounds
When a CG comment disposition matrix has been previously approved (e.g. ZD-0020 Rev.02 approved by CG), do NOT repeat the full comment-by-comment table in the new revision. Replace with a summary box:
- Round 1: N comments, closure status
- Round 2 (CRS): N comments, closure status
- CG Approval: document reference and date
- Reference: "Full CG Comment Disposition Matrix is attached as separate CR sheet."

This saves 2+ pages and avoids stale comment text that drifts from the approved CRS spreadsheet.

### No Legend Blocks
Do NOT include Status Legend, Route/Scope definitions, Outstanding Submittals, or Notes below the CG disposition matrix. Column headers are self-explanatory.

## AI Fingerprint Removal (CG-Facing Documents)

CG-facing documents must read as human-written. Remove all of these:

| Pattern | Replace with | Reason |
|---------|-------------|--------|
| `§` symbol | `Clause` or `Section` | § is an AI/legal-notation symbol, not human writing |
| Verbose section subtitles (e.g. "audit trail · baseline integrity") | Remove entirely | Adds no value for CG reader |
| Internal doc references in client-facing text (e.g. "Aligned with BEP Code B (17-Mar-2026) · NRS Methodology Pkg ZD-0026") | Remove or move to internal notes | CG doesn't need to know which internal docs were consulted |
| "Plan Snapshot" cards with icons and metrics | Remove | Visual clutter, not useful for CG review |
| "NEW" badges on TOC items | Remove | Self-evident from revision history |
| Elaborate spec-strip explanations (Scoring Convention, Tier 2 coverage, Register Total) | Condense to 1-2 sentences | CG knows what these mean |
| "honest status" in headers | Remove | Implies other statuses are dishonest |
| Compliance notice boxes with doc references | Shorten to 1 line | CG doesn't need the doc chain |
| Approval sequence with gate criteria | Remove gate criteria details | CG knows their own process |
| SLA convention with calendar-day equivalents | Remove | Working days is standard |
| RACI definitions with full descriptions | Shorten to 1-2 words per role | Self-explanatory |
| Concurrent escalation rules with register lists | Condense to 1 sentence | Detail belongs in procedure, not plan |

## Cover Page Rules

- Keep cover description brief — 1-2 sentences max
- Do NOT list methodology references, BEP codes, or internal doc numbers
- "Issued for CG Resubmission" + "REV N · Status Update" + one short sentence is sufficient
- Example: "Status update per specialist deployment review (Jun 2026). Rev 03 updates specialist assignments, statuses, and vendor names per live Key Personnel Register."

## Revision History Rules

- Sort **descending** (most recent revision first: 04, 03, 02, 01, 00)
- Prepared column: use **department/team name** (`Technical Office`), not personal name — never use individual names
- Approved column: use **real person name** with `Eng.` prefix
- Only include revisions formally submitted to CG — no internal drafts
- Description: keep factual, no fluff. List what changed, not why.
- When adding a new revision, insert at the TOP of the tbody (before the current first row), not at the bottom.

## Stakeholder Count Updates

When roles are added/removed, update ALL of these locations:
1. TOC chip (`15 SECTIONS · 24 PAGES · 56 ROLES`)
2. Hub diagram center (`56 stakeholder roles`)
3. Snapshot cards (Tier 1-3, External, OP, Authorities)
4. Bar chart segments
5. Section heading (`headline counts · 56 total roles`)
6. Register total text
7. CG-02 disposition (`Register with 56 roles`)
8. P/I reference text
9. Compliance summary (`56 mapped roles`)
10. TOC line entry

## Abbreviations Section

Place between §1.1 Revision History and §1.2 Document Identification:
- CTR T1 = Contractor Tier 1
- CP = Control Point
- DSN = Design Specialist
- COND = Conditional Specialist
- PI = Power/Interest score
- KPR = Key Personnel Register (live)

## Approval Status Tracking

When updating KPR statuses, distinguish:
- **Approved** = CG/MoC formally accepted (name + date known)
- **Code B** = Approved with comments (conditional approval)
- **Code C** = Revise and Resubmit (NOT approved)
- **Pending submission** = CV/PQD not yet sent to CG
- **Not yet appointed** = Role exists but no person assigned
- **Vacant** = Person left, replacement being hired
- **Nominated** = Person identified, not yet submitted to CG

## File Backup Protocol

Before delegating ANY file manipulation to a subagent:
```bash
cp <target-file> <target-file>.bak
```

Verify backup exists before making the delegate_task call. If the file is overwritten/corrupted, restore from `.bak`.

## Concurrent Version Awareness

Multiple write_file/terminal→python opens of the same Excel/HTML file can cause:
- Lost formatting when a later script writes over a formatted file
- State corruption (openpyxl's `data_only` vs formula mode)
- Duplicate rows or section-level text from string-based insertion

Always verify the file state immediately after each write.
