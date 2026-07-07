# Stakeholder Management Plan (SMP) Authoring Conventions

## Overview
Conventions and rules for updating the Stakeholder Management Plan HTML — derived from Mohamed's explicit corrections during the June 16, 2026 Rev 04 update session.

## Document Conventions

### Revision History (§1.1)
- **Only show formal versions submitted to CG.** Do not include internal iterative drafts.
- Use formal revision numbers: 00 (initial), 01 (first resubmission), 02 (current), etc.
- Prepared by and Approved columns need **real names** (not "Samaya PMO" or "Per live KPR").

### QC Sign-Off (§1.3)
- Every sign-off row needs an **actual person's name** — not role references.
- Prepare → Register → Review → Approve chain. Current standard:
  - QC-01: Mohamed Sultan (prepare)
  - QC-02: Eng. Hesham Abdelhamid (register)
  - QC-03: Mohamed Samir (on behalf) if QA/QC vacant
  - QC-04: Eng. Waris (approve)

### Document Number
- Use the **formal CG document number** from the CG response folder, not the internal project code.
  - ✅ `MOC-MUS-ASE-1K0-PL-0020` (from CG response PDFs)
  - ❌ `MOC-ASEER-SIC-1K0-PL-0020` (internal code)
- Verify by checking the CG Response folder for the formal number on submitted PDFs.

### Role-Based References (Not Names in Plan Body)
- The plan defines **roles, responsibilities, reporting lines** — the framework.
- The live **Key Personnel Register (KPR)** holds current names, CVs, approval statuses.
- Reference: "Per live KPR" in name fields throughout the plan.
- Exceptions: QC sign-off table and Revision History need **real names** (these are signatures, not live data).

### Table of Contents
- Keep clean: sections, pages, roles count only.
- **Do NOT include CG comment counts** or other metric noise.
- Example: `15 SECTIONS · 24 PAGES · 56 ROLES` — not `... 25 CG COMMENTS`.

## CG Comment Disposition Matrix

### Status Terminology
| Status | Color | When to Use |
|--------|-------|-------------|
| **COVERED** | badge-low | SMP-scope items addressed in the current revision but not yet reviewed by CG |
| **CLOSED** | badge-pass | Confirmed by CG in a prior revision (e.g., Round 1 CG-01 through CG-08) |
| **SUBMITTAL-PENDING** | badge-high | Requires external submission (CV, PQD, etc.) — not plan-scope |
| **IN-PROGRESS** | badge-low | Action underway, not yet complete |
| **RE-OPENED** | badge-critical | Previously CLOSED but withdrawn due to missing submittals |

Key rule: **Round 1 items** (CG-01 to CG-08) stay CLOSED (CG confirmed them). **Round 2 CRS items** that are SMP-scope become COVERED (plan addressed it, CG hasn't reviewed yet).

### CG Comment Preservation
- **NEVER modify the comment/requirement column text.** The CG's original wording must be preserved verbatim — even typos ("Structrual", "seperatly", "experianced") are part of the original record.
- Only update the disposition/action, status, and ref columns.
- When in doubt, compare against the previous revision's disposition table.

### Column Widths
- The **CG Comment column must be the widest** at ~250px (2x the disposition column).
- The **Round column** needs at least 65px for text like "R2 · 2-Jun".
- The **Disposition column** can be ~120px (short responses).
- Standard widths for a 7-column CG table:

| # | Round | CG Comment | Disposition | Ref | Status | Route / Scope |
|---|-------|-----------|-------------|-----|--------|---------------|
| 44px | 65px | 250px | 120px | 50px | 65px | 90px |

### Remove Explanatory Blocks
- Do NOT include Status Legend, Route/Scope explanation, Outstanding Submittals, or Notes blocks below the CG disposition matrix.
- The table headers and status badges are self-explanatory. Additional blocks add clutter and risk page overflow.

## Table Column Width Standardization
Across all tables in the SMP, maintain consistent column widths:

| Column Type | Standard Width |
|-------------|---------------|
| # | 40px |
| Rev | 40px |
| Date | 80px |
| Status | 90px |
| Prepared / Approved | 90px |
| Round | 65px |
| CG Comment | 250px |
| Disposition | 120px |
| Ref | 50px |
| Route / Scope | 90px |

## Honorifics
Use official honorifics (Eng., Dr., etc.) on all names — Mohamed corrected "Waris" → "Eng. Waris" explicitly.

## Cover Page Conventions
- **Subtitle** should match the revision table entry. Current pattern:
  `REV 04 · CG CRS Resubmission — Role-Based Classification`
- **Description line** should mirror the revision table's description column:
  `Resubmission - CG CRS response. Names to live KPR; M&E Contractor added; NRS interior/clarity; Appendix B split.`
- **Cover badge** ("Issued for CG Resubmission") and **disposition chip** (REV 04 · CG CRS RESPONSE) should be consistent with each other.
- Keep the description short — no "Supersedes Rev X" on the cover (revision history covers it).

## Stakeholder Count Consistency
When adding or removing roles:
- Update ALL occurrences of the count across the document:
  - TOC chip (`56 ROLES`)
  - TOC section 4 entry
  - CG-02 disposition text
  - §5 P/I matrix reference
  - Compliance summary CG-02 row
  - Hub-and-spoke SVG center text
- Run `grep "55 roles\|56 roles\|57 roles"` after changes to verify no stale references remain.

## CG Badge Colors Reference
| Color | Badge Class | Meaning |
|-------|-------------|---------|
| 🟢 badge-pass | `badge badge-pass` | CLOSED — confirmed by CG |
| 🟡 badge-low | `badge badge-low` | COVERED (addressed in this rev) or IN-PROGRESS |
| 🟠 badge-high | `badge badge-high` | SUBMITTAL-PENDING |
| 🔴 badge-critical | `badge badge-critical` | RE-OPENED or CODE C |

Always use the pillar shape with `pill` class suffix for category pills (DSN, COND, AUTH, CTR T1, EXT) — these use distinct background/border color combos, not the same badge system.
