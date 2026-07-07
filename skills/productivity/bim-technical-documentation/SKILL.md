---
name: bim-technical-documentation
category: productivity
description: Author and refine formal technical documents (Method of Statements, technical submittals, reports) for Samaya BIM/construction projects.
---

# BIM Technical Documentation — Method of Statements & Submittals

Authoring and polishing formal technical documents for Samaya Investment — Technical Office / BIM Unit. Covers MOS, method statements, technical reports, submittal packages, and CG-submission plans (Resource Mgmt, SMP, DMP, BEP).

## When to Load

- User asks to create, edit, review, or polish a Method of Statement (MOS)
- User asks to prepare a technical submittal, report, or formal document
- User says "review", "restudy", "balance", "merge pages", or "update section" on a technical document
- User says "audit" on a Primavera P6 schedule submission — load then follow `references/primavera-schedule-review.md`
- User asks for schedule programme analysis, critical path assessment, material extract, or supplier/brand names against schedule items
- User is working on Aseer Museum or similar Samaya BIM project documentation
- User asks "do we need charts/figures here?" for a management plan section — load then check `references/management-plan-chart-recommendations.md`
- User asks about what charts go in Interface Management, Risk, Schedule, Comms, Quality, or Resource sections

## Core Principles

### 1. Document Structure
- **Cover page** is the single source of truth for QC sign-off (Prepared / Reviewed / Approved)
- **Do NOT** duplicate the sign-off at the end — no separate "Approval & Sign-off" section (Section 13). The cover page is sufficient.
- Distribution list belongs on cover page (as metadata), not on its own page.
- Keep TOC page references accurate after any page number changes.

### 2. Page Economy
- Sparse pages (1 small table, 1 short list) should be merged with adjacent content
- Dense pages (many tables + large SVGs + long lists) should be split at a logical subsection boundary
- Target: each page should have 40–70% content fill. Avoid both <20% and >85%.
- When merging pages, remove duplicate headers and footers; update the combined header text and page number.

### 3. Role Tables
- **Consolidate survey roles**: Use a single "Survey Team" entry covering field ops, scanning, processing, registration, and export. Do not split into Survey Manager + Survey Team + Laser Scanning Specialist + Scan Processing Specialist.
- BIM roles (Modeling Team, QC Specialist) stay separate.

### 4. Timeline Tables
- Use **parallel tracks** (Data Integrity, Point Cloud, Quality, Documentation) rather than flat sequential milestone lists.
- Add a note: "All processing runs in parallel from field data ingestion."
- "All deliverables complete" should span columns and reference the longest track duration.
- Omit "Deviation Analysis" from Round A (AS-IS pre-demolition) — no design model exists yet.

### 5. Appendices
- **Do not embed large image catalogues** (brochures, spec sheets) as base64 inline — they bloat file size from ~100KB to ~5MB.
- Instead, note "refer to attachment" and let the user attach PDFs separately.
- Only list certification/QC documents that exist as actual PDF files. Trim out docs on hand that are not in the file system.

### 6. QC & Template References
- QC logs, NCR registers, field QC logs are referenced as project QMS forms — clarify they are maintained under the project Quality Management System, not blank templates attached to the MOS.
- If CG/PMC requests actual templates, add as a separate appendix.

### 7. Visual Consistency
- Page headers and footers must match the section content shown.
- When moving content between pages, update header labels (e.g. "Section 7 (cont.) & Section 8").
- Page number sequence must be sequential across the whole document after any add/remove.

### 8. CG Submission Preparation

Rules specific to plans and reports issued for CG/PMC/MoC review (Resource Mgmt Plan, SMP, DMP, BEP, Method of Statements).

#### 8.1 Internal Data — Zero Tolerance
- **No PD/HR action items, KPR update notes, amber callout boxes with internal workflows**
- **No "Updated per PD recommendations"** or any reference to internal emails/meetings
- **No "DRAFT" status** — use `[ISSUED FOR CG REVIEW]` or `[ISSUED FOR REVIEW]`
- **No "hiring in progress"**, "pending submission", or "submission in progress" as role-status text — keep it simple: "Vacant", "TBC", or just the name
- **No internal tool names** (e.g., "Primavera P6", "QS_Template.xlsx" → use "QS Template")
- **No PMBOK/RBS methodology jargon** in section titles or descriptions
- **No internal cross-references** (e.g., "aligned to SMP Rev 03")
- **CRITICAL: TBC roles get ZERO status commentary** — never append `— pending submission`, `— prequal in progress`, `— Code C`, `⚠ CRITICAL PATH`, or any other status note to a TBC entry. Just `TBC`. Status commentary is only acceptable when a firm IS named and has a CG approval status (e.g., `Rawasen — pending approved`). Rule of thumb: named firm = status OK; TBC = just TBC.

#### 8.2 Reference Citations
- Only cite **contract documents**: ER, SOW (SoW), DMP, BEP, or approved site instructions
- Never cite internal communications (PD emails, PD recommendations, Samaya internal notes)
- Format: `SoW §5.5 Staffing & Deployments · §10 On Site Fit-Out`

#### 8.2.1 Authority Basis Table — Default Sources
When building the **1.3 Authority Basis** table in any plan document (Resource Mgmt, SMP, DMP, BEP, etc.), always include these sources by default — they are standard, not optional additions:

| SOURCE | CLAUSE / DOC | WHAT IT REQUIRES |
|--------|-------------|-------------------|
| Main Contract | 0010003521 — §4 Art. 2 | Single-point design + construction responsibility |
| ER R02 | §2.4 — §2.4.D.3 | Mobilization, resource commitment, QA/QC resourcing |
| SoW | §5.4 — §5.5 | Design team composition — Key Personnel locked |
| SoW | §6.19 — §13.6 | Authority liaison resourcing |
| **DMP** | MOC-ASEER-SIC-1K0-PL-0001 Rev C04 | Organisation tier structure, role definitions, resource governance framework |
| **BEP** | MOC-ASEER-SIC-1K0-PL-0002 | BIM roles, software/hardware resource requirements, CDE access provisioning |
| KPR | MOC-ASEER-SIC-1K0-KP-0001 | Live register of all named persons, CV refs, MoC approval status |
| Master Programme | MOC-ASEER-GN-DS-006 Rev.03 | Time baseline for D-NN mobilization milestones |

The DMP and BEP are not optional extras — they are the governing documents for the tier structure and the BIM resource requirements that every plan depends on. Include them proactively; the user will correct you if they're missing.

#### 8.3 Revision History
- Description: list changes briefly — no "per PD" or internal-process rationale
- Before: `"Updated per PD recommendations: Added Accessibility Consultant..."`
- After: `"Updated: Added Accessibility Consultant, Acoustic Consultant..."`

#### 8.4 Tier / Org Structure Rules (Resource Management Plans)
- Every tier classification must trace to an approved source document (DMP for tiers)
- **Never invent tier labels**: no "Construction Tier", no "P4 Tier" — only T1, T2, T3 per DMP
- P4 Site Execution Team is an operational chart, not a DMP tier
- Role allocation tables and location matrices must use **current tier groupings** (T1 Mgmt, T2 Design Specialists, T3 Support)
- Keep location matrix rows grouped (not per-person exhaustive) but update group names to current tier labels
- **Merge duplicate roles** — When one person handles two roles (e.g., Document Controller + Submittals Coordinator), merge into a single row with a combined title (e.g., "Document Controller / Submittals Coordinator"). Do NOT list as two separate rows with "(same as X)" notes. The merged row keeps the person's name and combines the scope descriptions.

#### 8.5 Headcount Charts (Section 5)
- Stacked SVG area chart = T1 Management / T2 Design Specialists / T3 Tech Office (3 layers, not 4 — no separate Site/Const. layer; site team is absorbed into the tier breakdown)
- Y-axis scale: max ~40 persons, grid lines every 10
- Stacked dimensions (approximate, per phase):
  - P1 (D-14→D0): T1=2, T2=2, T3=1 → total ~5
  - P2 (D0→D14): T1=4, T2=4, T3=4 → total ~12
  - P3 peak (D65): T1=6, T2=19, T3=13 → total ~38
  - P3→P4 (D88): T1=5, T2=12, T3=8 → total ~25
  - P4 mid (D180): T1=5, T2=14, T3=9 → total ~28
  - P4→P5 (D270): T1=4, T2=8, T3=5 → total ~17
  - P5 end (D300): T1=2, T2=3, T3=3 → total ~8
- SVG construction: use 3 stacked `<path>` elements with semi-transparent fills (T3 bottom = #64748B 0.5, T2 middle = #0284C7 0.4, T1 top = #0F172A 0.3), plus a total-outline `<path>` stroke (#0F172A 2px)
- Data callouts with circles + leader lines at 7 key points: Backbone ~5, Full team ~12, Peak ~38 (gold #F59E0B), Post-AFC ~25, Construction ~28, Phase-down ~17, Demob ~8
- Color legend in top-right corner of SVG with labeled squares
- Gate markers: vertical dashed lines for G2 (D35), G3 (D65), G5 AFC (D88)
- X-axis: D-14, D0, D14, D35, D65, D88, D180, D270, D300 with phase labels P1-P5 below
- Y-axis: 0-40 with "Headcount" label (rotated -90°)
- SVG viewBox: 600 × 260 (extra height for legend), max-width: 540px
- All text: font-family="Inter,sans-serif"
- Role allocation table: one row per individual role, organized by tier sections with sub-headers
- Commitment levels: FT (pill-navy), part (pill-slate), stage (pill-amber), — (not required)

#### 8.6 Subcontractor Status Conventions (Exhibition Team Matrix)
| KPR Status | Display in CG Plan |
|---|---|
| Approved | `Approved` or `Approved DD-MMM` — no code history |
| Code B (Approved with Comments) | `Code B approved DD-MMM` |
| Pending / Not yet approved by CG | `[Firm] — pending approved` (only for named firms) |
| TBC / Not appointed | `TBC` — no status commentary |
| Named firm, not yet CG-approved | `[Firm] — pending approved` |
| Named firm, n/a or in review | `[Firm]` (status omitted if neutral) |
- **Never show revision cycle codes** (Code C, Code D, R1, R2, etc.) in plan documents — the KPR is the source of truth for that level of detail
- **Rule of thumb**: If the entry says TBC, Omit all status suffixes. Just write "TBC". Status notes (`— pending approved`, `— prequal in progress`, `⚠ CRITICAL PATH`) are acceptable only when a firm name is present and the note communicates CG review progress.

#### 8.7 KPR Sync Rules
- KPR is the source of truth for firm/entity names — plan reflects KPR data
- **Internal Samaya staff** (BIM team, Planner, Doc Controller, Tech Office Mgr) are NOT KPR Key Personnel — they stay in the plan as operational staff but don't get added to the KPR register
- Two-way sync: plan → KPR for role renames and new tier additions; KPR → plan for firm names and approval statuses

#### 8.8 Section 3 Compact Layout Pattern (Org Structure on One Page)

When the org structure section (T1 cards + T2 table + T3 table + 3.2 Construction) must fit on one A4 page:

1. **Page padding**: Reduce to `8mm 11mm` (from default `12mm 16mm`)
2. **Section-specific CSS class** (e.g., `.s3`):
   ```css
   .s3 td { font-size:0.35rem !important; padding:1px 3px !important; line-height:1.15 !important; }
   .s3 th { font-size:0.33rem !important; padding:1px 3px !important; }
   .s3 .pill { font-size:0.32rem !important; padding:0 3px !important; }
   ```
3. **T1 cards**: Single row of 6 in `grid-template-columns:1fr 1fr 1fr 1fr 1fr 1fr` with 1px padding cards
4. **T2 table**: 4 columns (Role / Firm / Scope / Type) at `font-size:0.35rem`, abbreviated scope descriptions
5. **T3 + Construction**: 2-column grid (`grid-template-columns:1fr 1fr`) — left column T3 table (11 rows), right column 3.2 Construction table (7 rows with Qty)
6. **Abbreviated type pills**: Use `FT` (full-time) and `SP` (specialist firm) instead of full pill text
7. **Trim descriptions**: T2 scope descriptions are 2-5 words (not full sentences)
8. **Abbreviated names**: "Anwar A. · Ali A. M." instead of full names in T3 table

## Pitfalls

- **Base64 images explode file size** — a single brochure page as base64 JPEG can be 1.5MB+. Avoid embedding catalogues.
- **/XX total mismatch** — after removing or merging pages, always update ALL page footers AND TOC references. A single missed `/20` breaks consistency.
- **Section numbering drift** — removing a section (e.g. Section 13) requires updating the TOC group headings too (e.g. "5 — APPROVAL" becomes orphaned).
- **HTML comments** — the `<!-- PAGE XX · SECTION -->` comments must match actual page numbers; update them when reshuffling pages.
- **Replace-all dangers** — `replace_all=True` on common patterns like `p. 07` or `/ 20` can hit unintended targets. Verify after.
- **Bulk rename of role titles** — renaming "Construction Manager" to "Site Manager" with replace_all affects EVERY occurrence including P4 site team charts, succession matrices, RACI rows, and footnotes. Review each hit before committing.
- **Page overflow from expanded tables** — When adding rows to tables (e.g., role allocation tables expanding from 11→45 rows), the page can overflow A4 height. Check using `grep -n '<section class="page"'` to count pages, then compare content density. Pages with >80 lines of table content (measured between `<section>` tags) will likely overflow. Split at a logical section boundary (e.g., after Tier 3, before Construction table).
- **TBC status suffix creep** — It's easy to leave `— pending submission` or `⚠ CRITICAL PATH` on TBC entries because they feel informative. Strip ALL such suffixes from TBC entries. Named firms only get status notes.
- **Output location — never Desktop** — All generated documents (HTML, DOCX, PDF) must be saved directly to the project's OneDrive folder structure, never to Desktop or /tmp. The user will correct you. Determine the correct subfolder before writing the file. For schedule review reports: `10_Plans/Schedule_Programme/`. For plan documents: `02_Plans_and_Procedures/<DOC_TYPE>/`. For correspondence: `09_Correspondence/YYYY-MM/`.
- **write_file destroys OneDrive files** — Never use `write_file` to overwrite a OneDrive-stored HTML plan file. `write_file` replaces the ENTIRE file, which OneDrive interprets as a new file, triggering extended-attribute locks that make the file unreadable (`[Errno 1] Operation not permitted`). Always use **`patch`** for targeted string replacements — OneDrive handles delta changes gracefully. To replace a large section, use `patch` with the entire old block as `old_string` (even hundreds of lines) rather than `write_file`. **Recovery if you already overwrote**: use `ditto` (macOS) to copy a backup back to the OneDrive path — `ditto` bypasses the extended-attribute lock that blocks `cp`, `cat`, and `open()`:
  ```bash
  ditto /tmp/backup.html /original/onedrive/path/file.html
  ```
  If no backup exists, `ditto` can also read files from the locked OneDrive directory (ditto bypasses the lock), so copy a Rev C00 or DRAFT version from the same folder to use as a base, then reapply via patch.
  **Verify**: `python3 -c "open('/path/file.html').read()"` — if `[Errno 1]`, lock persists. Re-run ditto.
- **Nested `<section class="page">` when patching page content** — When using `patch` to replace HTML page content, verify the replacement doesn't create nested `<section class="page">` tags. The old content in the file already opens a `<section>`, and if your replacement also starts with `<section>`, you get invalid nesting. Verify with:
  ```bash
  grep -n '<section class="page"' file.html
  ```
  #### 8.9 Formal Visual Styling for Tier / Org Tables

When designing representation tables for Section 3 (Tier 1 Management, Tier 2 Specialists, Tier 3 Support):

1. **No gradients** — tier banner bars use solid colors (primary navy, secondary sky, or amber). No `linear-gradient` or multi-stop backgrounds.
2. **No colored status badges** — status values are plain text (Active / Remote / Vacant / Pending). No green/red/amber pill badges, no `●` status dots with color styling.
3. **No colored row backgrounds** — alternating rows use only `background:var(--bg-light)` (very light grey) vs white. No green-tint for "approved" rows, no red-tint for vacant rows.
4. **Approval status** is plain text, not a colored pill with background. Use `Approved` / `Hiring` / `Activates D88` — no `background:#BBF7D0` or `color:var(--pass)`.
5. **TYPE badges** (FT / SP / INT) are the only colored inline elements allowed — keep them minimal (primary for FT, secondary for SP, `var(--text-muted)` for INT), small font, no extra tinting on the row.
6. **Headers** use `background:var(--primary); color:white` — consistent with all other tables in the document. **Do not use colored headers per tier** (e.g., sky blue for T2 headers, amber for T3 headers). All tier tables use the same dark primary header.
7. **Section headers** for grouped rows (e.g., "Full-Time Samaya", "Specialist Firms") use `background:var(--bg-light)` — the same light grey as alternating rows, not tier-specific colors.
8. **Footer/legend** uses `color:var(--text-muted)` — minimal.

**Rationale:** Formal business documents (Resource Mgmt Plans, SMPs, BEPs) must look consistent and professional. Color overload (gradients, green/red badges, tinted rows, tier-colored headers) makes the document feel informal or dashboard-like rather than a CG-submission plan. The Samaya style guide uses navy/sky as the only accent colors — adding extra palettes per tier or per status breaks visual cohesion.

## Verification Checklist

After any page merge/split/remove:
1. All `PAGE XX / YY` footers sequential and total YY correct
2. HTML comments (`<!-- PAGE XX · ... -->`) match actual page numbers
3. TOC page references match new page numbers
4. No orphaned TOC group headings (empty "5 — APPROVAL" etc.)
5. File size reasonable (no surprise base64 bloat)
6. Browser refresh shows changes; hard refresh (Cmd+Shift+R) if cached

**CG Submission Check:**
1. No internal PD/HR action items, KPR notes, or amber callout boxes
2. No "DRAFT" or "per PD recommendations" anywhere
3. Revision descriptions reference document changes only — no internal rationale
4. Tier labels match DMP (T1/T2/T3 only)
5. Subcontractor statuses use approved format (no Code C, no revision cycle codes)
6. Reference citations are from contract docs (ER, SOW, DMP) only
7. **No status suffixes on TBC entries** — grep for "TBC —" to catch any that slipped through. Named firms only get status notes.

## Reference Files

- `references/management-plan-chart-recommendations.md` — What charts/figures are needed in each management plan section (Interface, Risk, Schedule, Comms, Quality), with priority tiers and rationale for museum/cultural projects. Use when the user asks "do we need charts here?" for a specific section.
- `references/mos-layout-patterns.md` — concrete page map, merge patterns, and font compression guide from the Aseer Museum LiDAR MOS session.
- `references/onedrive-lock-recovery.md` — How to recover a OneDrive file that became locked after a write_file overwrite.
- `references/primavera-schedule-review.md` — End-to-end workflow for reviewing contractor Primavera P6 schedule submissions: extraction, WBS analysis, critical path, design phase deep-dive, materials cross-referencing, Excel extract, HTML report generation, and project folder conventions.
- `references/multi-plan-specialist-sync.md` — Multi-document sync pattern: updating SMP, Resource Plan, and KPR consistently when specialist deployment data changes (triggered by CG clarification requests, status updates, or deployment reviews). Covers revision bumping, cross-sectional changes, web deploy, and email reply drafting.
