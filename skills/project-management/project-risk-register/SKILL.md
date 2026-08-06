---
name: project-risk-register
description: Build professional Excel-based Project Risk Registers (PRR) for construction/museum/infrastructure projects — 31+ evidence-based risks, governance-grade styling, RBS taxonomy, P×I heat map, severity matrix, and PM dashboard with KPI cards, charts, and health checks. Also covers the multi-register web architecture (master + per-discipline sub-registers DDR/HSE/AVR with cross-nav banner) and the EXP-RISK-{PLAN}-{YEAR}-{SEQ} xlsx naming + SEQ auto-increment.
version: 1.1.0
author: Hermes Agent
license: MIT
platforms: [macos]
metadata:
  hermes:
    tags: [risk-register, prr, excel, openpyxl, project-management, construction, dashboard, risk-matrix, sub-register, ddr, hse, avr, cross-nav]
    related_skills: [bim-project-register, project-register-manager, evm-analysis-chart]
---

# Project Risk Register (PRR) — Excel + Multi-Register Web

## When to Use

- User asks for a "risk register", "PRR", "project risk register", "risk matrix" Excel file
- Building a risk register for a construction, museum, infrastructure, or fit-out project
- Need a professional workbook: 2 sheets (Summary + Register) for phase-specific registers, or 3 sheets (+ dashboard) for full project registers
- Required: evidence-based risks (from project memory, NOT generic templates), P×I scoring, severity classification
- **Always prioritize real risks from project memory over template/generic risks** — the user explicitly wants evidence-based entries
- **Multi-register project**: ship a master PRR + N discipline sub-registers (DDR, HSE, AVR, …) on the same web app family with cross-nav banner — see `references/samaya-sub-register-architecture.md`

## Variants

| Variant | Sheets | When |
|---------|--------|------|
| **Full** | Risk Register + RBS/Scoring Guide + Dashboard | Single consolidated register for entire project (31+ risks) |
| **Phase** | Summary + Risk Register | Phase-specific register (24 risks, lighter, faster) — ideal when user says "phase by phase" or "phase after phase" |
| **Samaya-templated snapshot** | Dashboard + Risk Register + Action Plan | **A4-portrait, Calibri Samaya palette, cover block (Snapshot No + Date + Time + Source URL), 6-card KPI strip, risk-matrix heatmap (4×4 PRR or 5×5 DDR), 2 charts (Doughnut + Bar), QR code linking to the live webapp, page header/footer with `Page n of N`. File naming `EXP-RISK-<REG>-<YYYY>-<NNN>_Rev<rev>_<status>.xlsx` per the Samaya Engineering Chart Framework §1.4. See `references/samaya-templated-snapshot-pattern.md`.** |
| **Subcontractor** | Markdown document (not Excel) | Package-specific register for a single subcontractor (e.g. MEP Designer, AV Contractor). Phase-gate aligned (Pre-Appointment → Mobilisation → 50% → 90% → IFC → AFC). Sourced from contract documents (offer, SOW, DMP, specialist SOWs), not project memory. See `references/subcontractor-risk-register-pattern.md`. |
| **Subcontractor → Enhanced Excel** | Two-phase: Markdown first, then openpyxl Excel | When the user needs both a decision-support tool during negotiation AND a governance deliverable. Phase 1 = markdown (fast, contract-sourced). Phase 2 = enhanced Excel with data validation, conditional formatting, alternating rows, status/review-date columns, and summary sheet. See `references/subcontractor-risk-register-pattern.md` §Two-Phase Workflow. |
| **Audit** | Multi-sheet audit report | QA an existing risk register (supplier, consultant, or internal). See `references/risk-register-audit-methodology.md` for the full 9-step checklist, common findings, and output format. |
| **Reconcile RMP + DRR** | RMP DOCX + repo + DRR Excel | Cross-reference the Risk Management Plan (DOCX) against the repo Markdown RMP and the Design Risk Register (Excel). Identify discrepancies in scoring scale, RBS categories, risk counts, EMV values, register architecture, and status definitions. Fix all documents to achieve alignment. See `references/rmp-drr-reconciliation.md`. |
| **Template Application** | Source register's layout + styling applied to target | Apply one existing register's full 24-column template, styling, RBS guide, and dashboard to another existing register with different column structure. See `references/template-application-pattern.md`. |
| **Quick** | Single sheet Risk Register | <12 risks, quick stand-up for a meeting |
| **Multi-register web (PRR + DDR + HSE + AVR)** | One self-contained HTML per register, cross-nav banner, one xlsx per register | When a single project ships more than one live risk register on the same web app family. Master + N sub-registers, each with its own scoring scale and category taxonomy, all linking to each other. See `references/samaya-sub-register-architecture.md` (includes banner regex pitfalls, the empty-table `id="matrix"` diagnostic, idempotency rules, and a pre-deploy sanity-check bash block — run those checks on every build, every deploy). |

[rest of SKILL.md body unchanged through "## Reference Files"]...

## Operational Lessons and Mandatory QA

1. Audit duplication across all registers before deployment. Compare IDs, exact titles, near-duplicate titles, and cause/event/consequence text across PRR, DDR, HSE, and AVR. A risk owned by a specialist register should not also remain in PRR unless it is explicitly a master roll-up with a cross-reference.
2. Audit lifecycle dates against the project timeline, not the date the row was entered. Creation dates must fall between NTP and the audit date, target dates must not precede creation dates, and every Open/Watch risk must have a target close date. If a sub-register has no created/target fields, report that limitation rather than inventing dates.
3. Check category, status, owner, P/S score, rating, and target date against current project activity. Reassign procurement risks to Procurement, authority risks to Approvals, and unresolved risks must not remain Closed/Mitigated without evidence. **Recalculate the rating from the stated scoring bands and flag every mismatch.** The user's data may have ratings that drifted from scores (e.g. score 10 labelled Medium instead of High). Scan all risks in all registers with a simple `>=12=Critical >=8=High >=4=Medium else Low` check and fix ratings to match. This catches the silent data-rot pattern where ratings were set manually once and never recalculated after score changes.
4. Snapshot workbooks must use formulas for dashboard KPIs, matrix counts, category/status/owner breakdowns, and charts. Dashboard cells should reference the Risk Register sheet with COUNTIF/COUNTIFS rather than storing Python-only totals. Validate formula strings after saving and confirm charts reference the formula cells.
5. Put the live-register hyperlink and QR code in the Dashboard header. Keep the Samaya logo and QR in the top header, not in the body. Constrain chart width/height and verify the drawing XML or rendered workbook so charts do not overflow the printable page.
6. When a user supplies a manually formatted XLSX, save an untouched copy under the project webapp templates directory and apply it as the common snapshot template to PRR, DDR, HSE, and AVR. Preserve the template's sheet names, merged cells, cover block, colours, charts, header/footer, Owner column, Target column, Response/Action column, and Action Plan sheet. Populate the Action Plan from structured actions; if the source only has response_action text, copy that text rather than writing "No discrete actions".
7. Dashboard formulas must be wired after the template is applied, not left as copied snapshot numbers. Use COUNTIF/COUNTIFS against the actual Risk Register rows for KPI, rating, status, category, owner, and matrix values. If a template omits probability/severity columns but includes a matrix, retain them in hidden helper columns and reference those columns with COUNTIFS. Formula owner counts are automatic; owner-name roster may be seeded from current distinct owners for Excel/LibreOffice compatibility.
6. Verify every download href against the actual server file, not only the HTML. DDR/HSE pages previously pointed to an obsolete PRR filename while the server contained register-specific EXP-RISK-DDR and EXP-RISK-HSE files. Test each URL with HTTP 200 and confirm the content type is XLSX.
7. For externally generated DDR/HSE pages, preserve their source data and patch only the link/navigation as needed. Do not rebuild them from the PRR template unless the complete source payload and analytics structure are available.

## Template-Based Snapshot Dashboard QA

When a user supplies a manually formatted workbook and asks for one common template across PRR, DDR, HSE, and AVR:

1. Preserve the template as an untouched source file under `webapp/templates/`.
2. Populate every register using the same sheet structure, including Owner, Target, Response/Action, and Action Plan columns.
3. Clear all old dashboard rows before writing current category/status/owner data. Updating only codes leaves stale category names and zero rows beside new values.
4. Calculate the dashboard layout dynamically. Set `TOP OWNERS` below the longer of the status and category tables, and move the footer down when required. Never hard-code row 37 or another fixed owner-table position.
5. Refresh both category display names and category codes from the current `rbs_categories` payload. Formula counts alone do not fix stale labels.
6. Use formulas against the Risk Register sheet for KPI, rating, status, category, owner, and matrix counts. If the template has no visible P/S columns, add hidden helper columns and reference them with `COUNTIFS`.
7. After rebuilding, inspect the rendered workbook or drawing XML for chart/image extents and verify no table overlap. Test all four download URLs with HTTP 200.
8. When category names are long, split Exposure by Category into two side-by-side tables with separate Category, Code, Count, and % of total columns. Refresh both display names and codes; clear stale rows before repopulation. Position TOP OWNERS below the taller category half, and move the footer down if the owner list extends beyond the original template footer.
9. **Include ALL categories, not only the template's hardcoded subset.** The template may only list 8 categories but the register may have 17+. Collect all unique category codes from the actual risk data and build the category table dynamically. Missing categories cause the % of total column to sum below 100%, which the user will catch.
10. **Clear chart numCache after template copy.** Charts in the template carry cached (stale) data from when the template was created. After populating the register, clear each chart's `numCache` (set `None` on each `numRef.numCache` element) so Excel recalculates from live formulas on first open. Without this, the chart initially displays the template's old values.
11. Use the manually formatted workbook supplied in the latest user turn as the current template authority. Do not revert to an earlier template or generic builder styling without explicit instruction.

## Latest Operational Lessons

- Treat a user-supplied formatted workbook as the current template authority. Save an untouched copy under `webapp/templates/` and use it for every register, not only the register named in the filename.
- Preserve Owner, Target, Response/Action, and Action Plan fields. If a sub-register has blank owners or targets, fix the source payload and regenerate both the register sheet and Action Plan; do not populate only the dashboard.
- Assign missing owners from the actual discipline responsibility matrix. Typical mappings are schedule to Planner, procurement to Procurement Lead, statutory approvals to Approvals Consultant, quality to QA/QC Director, commercial to Commercial Manager, BIM to BIM Coordinator, MEP to MEP Lead, AV to AV Lead, and conservation/Oddy to Conservation Consultant. Flag any inferred assignment for review.
- Assign missing DDR target dates using rating and current programme status, then write the same target to Risk Register and Action Plan. Check that open risks have targets, target dates do not precede creation dates, and avoid non-working-day deadlines.
- Formula cells can exist without visible values in Preview or non-recalculating viewers. Preserve the formulas, set full calculation on load, and add cached dashboard results when the deliverable must display correctly before Excel recalculates.
- Long category tables need a split layout. Use two side-by-side Category/Code/Count/% tables, clear stale rows before repopulation, and place Top Owners below the taller table dynamically.
- Add `id="schedule"` to the detailed register table and make Risk Matrix and Exposure by Category headings link to `#schedule` on every register page.
- Remove decorative symbols and AI-style wording from source JSON, HTML, and generated workbooks. Replace symbols such as `§`, `·`, em dashes, arrows, bullets, and check marks with plain words or standard punctuation. Use short, direct engineering English.
- After deployment, verify both page HTML and workbook downloads. Check jump-link anchors, prohibited-symbol scans, HTTP 200, formula strings, cached values, Owner/Target fields, and Action Plan targets.

## Excel Workbook Column Order (Must Match Website)

The Download Snapshot workbook columns MUST match the website table columns exactly. If they differ, the user will ask for correction, sometimes multiple times.

**Required column order in `Risk Register` sheet (row 9 = headers, row 10+ = data):**

| Col | Header | Content | Formula? |
|-----|--------|---------|----------|
| A | ID | Risk ID (e.g. PRR-PRC-01) | No |
| B | CAT | Category code (e.g. PRC, SCH) | No |
| C | RISK | Risk title / event text | No |
| D | P | Probability (1-5, user-entered) | No |
| E | S | Severity (1-5, user-entered) | No |
| F | SCORE | Calculated score | Yes: `=D{row}*E{row}` |
| G | RATING | Rating label | Yes: `=IF(F{row}>=12,"Critical",IF(F{row}>=8,"High",IF(F{row}>=4,"Medium","Low")))` |
| H | STATUS | Risk status | No |
| I | OWNER | Risk owner | No |
| J | TARGET | Target close date | No |
| K | CAUSE | Risk cause text | No |
| L | CONSEQUENCE | Risk consequence text | No |
| M | RESPONSE / ACTION | Mitigation/response text | No |
| N | EVIDENCE | Supporting evidence references | No |

**Pitfalls:**
- NEVER embed score text in RESPONSE/ACTION (e.g. "Risk Score: 8 (MEDIUM)"). The score belongs ONLY in the SCORE column with a formula. The user will reject this immediately.
- NEVER put probability/severity in hidden side columns. They MUST be visible in columns D/E, matching the website P/S columns.
- The SCORE formula must reference D and E (the visible P/S columns), not hidden columns.
- The RATING formula must reference F (the SCORE column), not D or E directly.
- Dashboard KPI formulas must reference the RATING column (G) and STATUS column (H).
- Do NOT write a risk matrix into the Risk Register sheet starting at row 9 — it will overwrite the column headers. The risk matrix belongs ONLY on the Dashboard sheet.
- Variable name collision (e.g. using `s` for both a sheet object and a loop variable) causes silent data corruption in openpyxl scripts.

## Public-Facing Register QA

- Do not expose internal-only source names in public HTML or downloaded workbooks, including PM Consolidated Risk Register files or internal project reviews not issued to CG. Replace them with an approved external evidence reference or neutral wording such as `Project risk review` only when the underlying statement is suitable for public issue.
- Use plain, human engineering English. Remove decorative symbols and AI-style wording from source JSON, HTML, and XLSX output. Avoid `§`, bullets, arrows, em/en dashes, check marks, and phrases such as `seamlessly`, `robust`, `cutting-edge`, or other promotional wording. Run a symbol and phrase scan after generation.
- For dashboard navigation, place `id="schedule"` on the detailed register table and make Risk Matrix, Exposure by Category, By Status, and Top Owners headings execute a direct smooth scroll to the schedule. Verify the live HTML contains the anchor and click handler, not only a visually styled link.

## Public Snapshot and Source-Control Lessons

- Treat the user's latest manually formatted workbook as the authority for all four register snapshots, not only the register named in its filename. Preserve its dashboard, table layout, Owner/Target/Action Plan fields, and visual conventions.
- Every downloaded workbook must show visible Probability, Severity, Score, Rating, and Status columns. Use formula-driven scoring such as `=M10*N10` and formula-driven rating bands; do not deliver a Rating-only register or static score values. Keep score/rating text out of Response / Action; that field is reserved for controls and actions.
- Dashboard formulas must reference the workbook's Risk Register sheet. When viewers show blank formula results, preserve the formulas and provide verified cached values through recalculation or XML cache handling.
- Do not expose internal-only references in public registers. Remove self-references such as `RMP APP`, `PRR-APP-*` references inside evidence text, and internal consolidated-register names. Risk IDs may remain as IDs, but evidence must point to consultant-visible or approved external records.
- Remove Print and CSV controls when the requested public page is download-only; label the remaining workbook control `Download Snapshot`.
- Verify every live page and download after deployment: visible scoring columns, formula strings, owner/action-plan fields, target dates, no prohibited symbols, no internal-source names, and HTTP 200.
- Before changing a risk status, owner, target, or evidence, inspect the authoritative repository risk row and the relevant source register. Do not infer closure or RFI linkage from a user statement alone. If an RFI is claimed but no matching reference exists in the RFI register or source file, report the gap and request the exact reference rather than fabricating one.
- Reconcile sub-register risks against current project status before carrying them forward. If the risk event has passed, cite the dated project evidence, then set Mitigated or Closed only at the level supported by that evidence. Distinguish an active project delay from a stale risk description and assign ownership to the actual responsible role, not automatically to Planner.
- Never place master PRR IDs or internal register names in a discipline register's evidence. A risk ID may remain as an identifier in the master register, but public evidence must cite consultant-visible documents or neutral wording. Remove self-references such as `RMP APP` and `PRR-APP-*` from evidence text.
- **Split download filename from server filename in HTML templates.** The `href` attribute points to the server file (e.g. `EXP-RISK-PRR-2026-036_RevC12_ACTIVE.xlsx`) but the `download` attribute should be a user-friendly name with project name, register code, snapshot date, and time (e.g. `Aseer_Regional_Museum_PRR_2026-07-25_1430.xlsx`). Use separate placeholders (`__XLSX_HREF__` and `__XLSX_DOWNLOAD__`) in the HTML template and generate both from the build script. The thumb rule: the server name is versioned and auto-incremented; the download name is what the user saves to their desktop.

## Updating Risk Scores from CG Responses

When a CG response arrives that changes the status of a risk (e.g. a Code C submission gets Code B on resubmission):

1. **Verify the CG response in Outlook** — confirm the doc ref, date, and code from the actual email, not from memory or inference
2. **Recalculate P×S** — if the risk event has passed or been resolved, reduce probability and/or severity accordingly
3. **Update the risk JSON** — change `status`, `score`, `rating`, `probability`, `severity`, `last_reviewed`, and `target_close`
4. **Update the event/consequence text** — reflect the new reality (e.g. "Rev.02 got Code B — BOD now approved")
5. **Mark completed actions** — any action that was waiting on this CG response gets `status: Completed` with evidence
6. **Add a history entry** — date, action taken, by whom, and what changed
7. **Do NOT close the risk** if residual actions remain (e.g. site investigations still in progress) — downgrade to Watch instead

### Example: PRR-DES-07 (Structural DD Code C → B)

| Field | Before | After |
|-------|--------|-------|
| Score | 16 Critical | 9 High |
| Status | Open | Watch |
| P×S | 4×4 | 3×3 |
| A6 (resubmit) | Not Started | Completed |
| Event text | "CG returned Rev.01 as Code C" | "Rev.02 got Code B — BOD approved" |

## Risk Review / Discussion Protocol (Telegram / One-by-One)

When the user asks to "show risks" or "discuss risks" in a conversational channel (Telegram, chat):

### Presentation Format

Present each risk as a structured card with these fields in order:

| Field | Example |
|-------|---------|
| **ID** | PRR-DES-05 |
| **Category** | DES (Design) |
| **Title** | New MoC object list triggers cross-discipline DD redesign |
| **P×S** | 4 × 4 = **16** |
| **Rating** | **Critical** |
| **Status** | Open |
| **Owner** | Design Manager |
| **Cause** | MoC issued new object list after DD gate passed |
| **Consequence** | Cascading redesign across all disciplines — 90%/IFC gates slip |
| **Response Strategy** | [Avoid] Issue cross-discipline impact register; agree cut-off date with MoC |
| **Actions** | Table of action items with #, text, owner, due date, status |
| **Target Close** | 2026-08-21 |

### Mandatory Elements

1. **Always state the action needed** — after presenting the risk, explicitly say what the user/owner should do next. The user said: *"always tell me the action or the response so i know what is the update you need"* (18-Jul-2026 session).

2. **Flag overdue actions** — if any action item is past its due date, highlight it with "(overdue X days)".

3. **Answer "did we add this before?"** — when the user asks if a risk existed previously, search session history and provide the timeline:
   - When the risk was created
   - What changed in each revision
   - Whether the RFI/action was actually executed or just planned
   - Source: the risk was added during which merge/update event

4. **Show the full action plan** — not just the response strategy. The user needs to see individual action items with owners and due dates to know who to chase.

5. **One risk per turn** — present one risk, wait for discussion, then move to the next. Do not dump multiple risks in a single message unless the user asks for a summary.

### Order of Review

1. Critical risks first (highest score first)
2. Then High risks
3. Then Medium risks
4. Within each rating, newest risks first (by creation date)

### Pitfalls

- Do NOT embed score text in the Response/Action field — the user will reject it
- Do NOT present risks without their action items — the user needs to know what to do
- When the user says "show the most recent risks", sort by creation date descending, not by ID
- If a risk has no actions defined, say "No discrete actions recorded" rather than fabricating them
- When the user asks about a specific risk, load its full JSON from `risks.json` (not just the markdown table) to get actions, evidence, history, and treatment file path

### Drafting RFIs / Emails from Risk Discussions

When the user asks to draft an email or RFI about a specific risk (e.g. PRR-AV-01 — AV content 'by others'):

1. **Load the full risk JSON** from `risks.json` — the markdown table doesn't show actions, evidence, or history
2. **Check if the action was already planned** — the risk's `actions` array may already contain the RFI as a planned action. If so, the email is executing an existing action, not creating a new one
3. **Flag overdue actions** — if the RFI action was due days/weeks ago, note it in the draft
4. **Include contract references** — every RFI must cite the governing contract documents:
   - **ER** (Employer's Requirements) — service life, performance criteria, AV equipment specs
   - **SOW §2.2** — scope exclusions (e.g. "AV software/media → supplied by others")
   - **SOW p.17** — MoC-supplied items list (research, text, images, film list)
   - **RACI Matrix** — who is Responsible/Accountable for each AV item (AV-01 through AV-08)
   - **MoC Object Schedule** — what objects exist and what display methods they need
5. **Distinguish physical objects from digital content** — the MoC object list contains physical artifacts only. AV content (videos, motion graphics, interactives) is a separate scope. The RFI must clarify this boundary explicitly
6. **Structure the RFI by gallery** — group questions by gallery (Welcome Gallery screens, Flowersmen slideshow) with specific object IDs
7. **Add a contractual protection question** — if content specs arrive after hardware freeze, who bears rework cost? Cite Contract Art. 14 (variations)
8. **Send the draft as plain text** — the user copies and sends manually. No Outlook drafts, no attachments. Keep the draft short — no preamble explaining what the email contains

## Reference Files
- `references/av-content-vs-object-list.md` — Distinction between MoC-approved physical object list (295 artifacts) and AV digital content (videos, motion graphics, interactives). Critical for PRR-AV-01: the object list contains NO AV content files. Use when discussing AV content risks or drafting RFIs about 'by others' content boundaries.
- `references/design-coordination-risk-identification.md` — 7-phase methodology for extracting coordination risks between AV/IT/ELV specialist submissions and base build MEP infrastructure. Covers BOQ power load extraction, rack room heat analysis, projection path spatial conflicts, containment segregation, UPS strategy gaps, and scope boundary risks. Use when reviewing a specialist design submission (AV, IT, Security, ELV) before IFC or before D&B tender.
- `references/template-application-pattern.md` — Apply one existing register's column layout, styling, sheets, and dashboard structure to another existing register. Covers data column mapping, scoring scale bridging, source styling capture, Cover preservation, and verification.
- `references/subcontractor-risk-register-pattern.md` — Markdown risk register for single-subcontractor packages during contract negotiation. Phase-gate aligned (D0→D300), sourced from contract documents (offer, SOW, DMP), not project memory. Use when the user is negotiating with a specific subcontractor and needs decision-support risks, not a governance deliverable.
- `references/risk-register-audit-methodology.md` — 9-step audit checklist for QA-checking an existing risk register. Covers scoring integrity, cross-referencing, lifecycle gaps, residual risk, mitigation quality, and dashboard verification. Use when the user sends an existing XLSX and asks "check this" or "audit this".
- `references/rmp-drr-reconciliation.md` — Cross-reference RMP DOCX, repo Markdown RMP, and DRR Excel to eliminate conflicts. Covers scoring scale alignment, RBS category sync, risk count verification, EMV values, register architecture, status definitions, common DOCX fixes (heading styles, cantSplit, rebuild_table), and common Excel fixes (legends, formulas). Use when the user asks to "check" or "fix" risk management documents that should agree but don't.
- `references/samaya-templated-snapshot-pattern.md` — Build the A4-portrait Samaya-styled xlsx snapshot (Dashboard + Risk Register + Action Plan, cover block, KPI strip, heatmap, charts, QR, page header/footer, versioned file naming). Reference build_xlsx.py, the deploy pipeline, the snapshot_counter.json pattern, and the OneDrive / Hostinger caveats covered by `macos-onedrive-recovery`.
- `references/samaya-sub-register-architecture.md` — Multi-register architecture for projects that ship more than one live risk register (master PRR + DDR + HSE + AVR) on the same web app family. Covers cross-nav banner (4-card grid with `reg-current` marker), `is_ddr/is_hse/is_av` JSON flags, `EXP-RISK-{PLAN}-{YEAR}-{SEQ}_RevC{REV}_{STATE}.xlsx` naming + SEQ auto-increment, `rsync --delete` with `--exclude` for sibling subfolders, and the in-place patch pattern for registers built by an external pipeline. Use whenever a project has more than one live risk register on the same site.
- `references/formula-driven-register-pattern.md` — Live Excel formulas
- `references/dashboard-layout-and-language-qa.md` — Formula cache checks, dynamic dashboard layout, schedule jump links, symbol cleanup, and plain engineering language QA. (`=I*J`, nested `IF` for rating, `COUNTIF`/`COUNTIFS` for the dashboard) instead of static computed values. For registers that need to be interactive (user edits P/S, score/rating auto-update).
