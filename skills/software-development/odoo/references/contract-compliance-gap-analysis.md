# Contract Compliance Gap Analysis

## When to Use
When the user asks you to compare contract requirements (appendices, SOW, ER sections) against current project registers (Key Personnel Register, Stakeholder Register, Odoo task lists) to identify gaps.

## Workflow

### Phase 1 — Extract Contract Requirements
1. Find the contract document — typically `Appendix B.pdf`, `Scope of Work.pdf`, or `Employer Requirements.pdf` in the project's Subcontractors or Docs folder.
2. Read the PDF with PyMuPDF (`fitz`) and extract text blocks with positions to understand the layout (many contract appendices are diagrams/tables, not linear text).
3. Identify the **columns/groups** — specialist contractor packages vs individual specialists, management roles, authority requirements.
4. Compile a flat list of every required role/package/contractor.

### Phase 2 — Map Current State
1. Read the **Key Personnel Register** Excel via openpyxl — extract all rows with tier, role, name, MoC approval status.
2. Read the **Stakeholder Plan** (Rev 03 HTML or PDF) — extract all tier categories and role names from the stakeholder register table.
3. Read the **Odoo task tree** under the relevant parent package for any related procurement/prequal tasks.

### Phase 3 — Gap Classification
For each contract requirement, classify as one of:

| Status | Meaning | Action |
|--------|---------|--------|
| ✅ **Covered** | KPR has the role with a confirmed vendor/name, status is Approved or Code B | No action |
| ⚠️ **Partial** | KPR has a row but vendor is TBC, or name exists but status is pending/unapproved, or coverage is fragmented across multiple roles | Create/fill vendor, push approval |
| ❌ **Missing** | No KPR entry exists for the requirement at all | Create new KPR row |
| 🔴 **Out of Scope** | Requirement noted but not yet actionable (e.g. post-handover roles) | Track separately |

### Phase 4 — Report
Present as a three-column table:

```
| Contract Requirement | KPR Status | Gap |
|---------------------|------------|-----|
| Lighting Designer & Supplier | R12 ZNA — Code B ✅ | None |
| FF&E Supplier | NOT IN KPR ❌ | Missing — create entry |
```

Include a **Priority Summary** at the top:
- **HIGH** — Missing roles that are on the critical path (ITCA, M&E Contractor)
- **MEDIUM** — Roles that are partially covered or TBC
- **LOW** — Future-phase roles

### Phase 5 — Update Registers
1. Update the **KPR Excel** — add missing rows, update statuses, append notes with source reference
2. Update the **Stakeholder Register Excel** — add new STK entries, update contact info
3. Update **PROJECT_MEMORY.md** — add gap summary to relevant section
4. Update the **Odoo task** description with the gap analysis findings
5. Update the **CG compliance document** if one exists (e.g. CG_Comments_Compliance_Rev03.md)

## CG Comment Disposition Status Conventions

When building or updating a CG comment disposition matrix (e.g. §1.4 in the Stakeholder Management Plan), use these status conventions:

| Status | Badge Class | Meaning | When to Use |
|--------|------------|---------|-------------|
| **COVERED** | `badge-low` | Addressed in this revision, awaiting CG review | SMP-scope items where we made the change but CG hasn't reviewed yet |
| **CLOSED** | `badge-pass` | Confirmed by CG in a prior revision | Round 1 items where CG explicitly accepted the resolution |
| **SUBMITTAL-PENDING** | `badge-high` | Depends on external submittal (CV, PQD, Drawings) | Items where the plan is correct but the actual submission documents are pending |
| **IN-PROGRESS** | `badge-low` | Action underway but not complete | CRS-08 (MEP designer — PQD process) |
| **RE-OPENED** | `badge-critical` | CG confirmed closure was premature | CRS-07 (CG-03 specialist closure withdrawn) |

**Critical rules:**
- **Never mark "CLOSED" for a CG comment that CG hasn't reviewed.** Round 1 items (CG-01 to CG-08) that CG already accepted can stay CLOSED. Round 2 items should be COVERED until CG confirms in the next response.
- **Never rewrite CG comment text.** The CG comment column must contain the EXACT text from the CG response PDF — not a summary, not a paraphrase. Typos, grammar issues, and formatting are preserved as the CG wrote them. Only the Disposition/Action column is ours to write.
- **Round 1 comments genuinely closed by CG** (CG-01 through CG-08) stay CLOSED. Only Round 2 CRS items that are SMP-scope get COVERED.

### Revision History — Formal vs Internal

When building the Revision History table (§1.1):

- Only show **formal submissions** that were sent to CG for review
- **Internal iterations** (QC blocks, formatting fixes, intermediate drafts that were never formally submitted) should NOT appear in the revision history
- The CG reviewer only needs to see the chain of official submissions and their status
- Rule of thumb: If you can't find a transmittal/submission email for it, it was internal and doesn't belong in the table

### Formal Document Number

Always verify the formal document number from the CG response folder:

```
Docs/02_Plans_and_Procedures/[plan_folder]/02_CG_Responses/
```

The CG response PDF filename shows the formal number. Compare your internal doc number against it — they may differ (e.g. internal uses `MOC-ASEER-SIC-1K0-PL-0020` while CG uses `MOC-MUS-ASE-1K0-PL-0020`). Use the CG-facing number in the plan document.

## Pitfalls
- **PDF diagrams extract unpredictably** — use `page.get_text("blocks")` and sort by y/x position to reconstruct layout, don't rely on linear text extraction
- **The user's "OneDrive - SAMAYA INVESTMENT" path** may be a different mount point than `Library/CloudStorage/OneDrive-SAMAYAINVESTMENT`. Always check both paths and read from the one the user specified. The user's natural path is `~/OneDrive - SAMAYA INVESTMENT/...` (with space).
- **Excel files may be open in another app** — openpyxl cannot write to a file open in Excel. If write fails, ask the user to close the file first.
- **KPR rows may have been reordered** — don't hardcode row numbers; search by role name in column 2.
- **Stakeholder Plan Rev 03** uses tier categories (Tier 1 Management, Tier 2 Architecture, etc.) — map contract requirements to the correct tier, not the same row numbers from the KPR.
- **OneDrive sync lag** — after writing, the local filesystem copy updates immediately but the user's Finder view may show stale data until OneDrive finishes syncing. Tell the user to wait for the cloud icon and reopen the file.

## Reference
Based on Aseer Museum Appendix B analysis (2026-06-16). Source document: `Subcontractors/_MANAGER_DASHBOARD/APPendix B.pdf` — lists 21 specialist packages/roles across two columns (Specialist Contractor Packages + Individual Specialists + Exhibition Fit-Out Contractor).
