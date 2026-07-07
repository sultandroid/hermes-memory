# Submittal Register from SOW/ER Contract Documents

**Use case:** Create a discipline-specific submittal tracking register by extracting requirements from the Scope of Works (SOW) and Employer's Requirements (ER) PDFs — not from a file scan. Registers are organized by design-stage packages (50%/90%/100% DD + IFC/AFC) and placed in project submittals folder + relevant subcontractor folder.

Example deliverables from Jun 2026:
- AV Submittal Register (60 items, 6 sheets) for Aseer Museum — SOW+ER
- Exhibition Fit-Out Submittal Register (96 items, 5 sheets) for Aseer Museum — SOW+ER

## Workflow

### 0. QC Gate — Mandatory Before Delivery

The user explicitly requires: **"alwayes review your work use consaltant like claude or kimi or codex"**.

Before delivering ANY register update:
1. Check 50% items are comprehensive (surveys + Basis of Design + preliminary concepts, not just surveys)
2. Verify all references are SOW § or ER § only — no external sources
3. Verify subfolder structure (not flat files)
4. Verify generator script regenerates without error
5. Delegate QC review to **Kimi** (fast) or **Codex** (deep audit) — do not ship without a second set of eyes

If the user flags an issue, update the register AND this reference with the lesson.

### 1. Subcontractor List Source — Appendix B Only

The authoritative list of subcontractor packages is **SOW Appendix B** (`Subcontractors/_assets/APPendix B.pdf`), a single-page org chart. Do NOT use the project README's subcontractors table.

Appendix B packages (Aseer Museum):
- Exhibition Fit-Out Contractor (Management — Setworks, Partitions & Ceilings, Finishes, Logistics)
- Model Maker
- Lighting Designer and Supplier
- Graphics Artwork and Production Contractor
- AV Hardware Contractor
- Conservation Showcase Contractor
- Specialist Rigging Contractor
- FF&E Supplier
- Interactives Contractor
- Specialists (M&E / MEP)
- Fire Life Safety
- Structural Engineering
- Health and Safety
- IT/Data
- Surveyor
- Accessibility
- Architect
- Acoustic
- Interior Design
- Landscape and Horticulture Contractor

Note: Oddy Testing Lab is a testing service, not an Appendix B subcontractor package.

### 2. Load Contract PDFs with PyMuPDF

Both SOW and ER are typically multi-page PDFs. Use `python3` with `fitz` (PyMuPDF — available on macOS system Python) to extract text:

```python
import fitz
doc = fitz.open(path)
for i in range(doc.page_count):
    text = doc[i].get_text()
    # search for relevant sections
```

### 3. Identify Discipline Sections in SOW + ER

Extract all sections relevant to the target discipline. **References must only come from SOW and ER — no external sources.**

| Document | Key AV Sections | Key Exhibition Fit-Out Sections |
|----------|-----------------|---------------------------------|
| **SOW** | 6.22.2 (AV hardware design), 6.22.4 (Technical Design Deliverables), 8.9 (Off-site Fab AV), Part 7 (Engineering), 6.9 (Design Phase Submittals), 6.10-6.18 | 6.22 (Exhibition drawings & deliverables), 6.22.1 (Graphics), 6.22.4 (Detailed Design Package), 6.20 (BIM), 8.2-8.7 (Off-site Fab: walls, floors, ceilings, joinery), 8.11-8.14 (Interactives, Models, Tactile, Graphics Fab) |
| **ER** | 3.2 (Power), 3.3 (Network/Telecoms), 3.4 (Security), 3.5 (PAVA/Fire Alarm), 5.0 (Room Data Sheets) | 5.0 (Room Data Sheets), 2.3-2.7 (QA/Commissioning/Handover) |

### 4. Use Exact SOW Wording for Descriptions

**CRITICAL:** Descriptions in the register must use the **exact wording from the SOW document**, not extrapolated or paraphrased text. The user will reject items that don't match. Extract verbatim from these sources:

- **SOW 6.22** — list of exhibition deliverables (general arrangement plans, wall/floor finish plans, RCPs, setworks drawings, etc.)
- **SOW 6.22.4(i)-(xviii)** — fully coordinated Detailed Design package items
- **SOW 8.2-8.14** — Off-Site Fabrication items per trade
- **SOW 6.20** — BIM deliverables (model, clash detection, weekly updates, handover)

### 5. Organize by Design-Stage Packages (50%/90%/100%/IFC)

Use a **4-sheet structure** where each sheet represents a submission package:

| Sheet | Colour | Items | Content |
|-------|--------|-------|---------|
| **50% Design Package** | Blue (#2E75B6) | Items due at interim design | Block schematics, design intent, load estimates, general arrangement, finish schedules |
| **90% Design Package** | Green (#548235) | Items due at draft final design | Coordinated drawings, detailed schedules, material selections, samples presentation |
| **100% Design Package** | Gold (#BF8F00) | Items due at final design | Complete coordinated design ready for IFC documentation |
| **IFC  AFC  Construction** | Brown (#843C0C) | Post-design submittals | Shop drawings, fabrication, material submittals, commissioning, handover |

**Masking logic:** Each item has a binary mask `[50%, 90%, 100%, IFC]`. Items that span multiple stages (e.g., `[1,1,1,0]`) appear in all relevant sheets. Items with stage-specific status columns (blank = due at that stage, "—" = not applicable).

**50% content rule (user correction, Jun 2026):** 50% must include surveys + **Basis of Design report** + **design programme** + **preliminary concepts** (SLDs, load schedules, cooling loads). Not just site assessment. The user flagged MEP 50% having only 4 survey items as insufficient.

**Long-lead item rule (Jun 2026):** When a subcontractor has a long lead time (e.g., Showcases at 14 weeks, bespoke seating 8-12 weeks), the 50% package must include MORE items — design decisions, material selections, and procurement specs must start at 50% to avoid schedule compression. Check the SPEC.md `## 6. Long-Lead Items` section to determine which items need early release. Example: Showcases had 8 items at 50% (schedule, materials, environmental control, GA drawings, structural design, lighting, power/data, lock system).

### 9b. Excel Formatting for Submission (Consultant-Ready)

When the register is for **submission to CG/consultant** (not internal tracking):

**Numbers & formulas:**
- All prices/quantities must be actual numeric values, NOT text strings
- Apply number formatting: `#,##0" SAR"` for currency, `#,##0` for quantities
- Use formulas for calculated cells: totals = `=SUM(range)`, VAT = `=total*0.15`, final = `=total+vat`
- Never leave empty placeholder cells (no "--" or "—" in numeric columns where N/A) — truly blank

**Structure:**
- Include a Cover sheet with: project name, document ref, revision, date, submitting party, distribution table
- Submit ALL 4 stages as a full package: 50%, 90%, 100%, IFC/AFC/Construction — not just one stage
- Include a Legend sheet with column definitions and status codes
- Status column: pre-fill as "P" (Pending) with red highlight for items due at that stage

**Pagination & layout:**
- Freeze header panes below the header row
- Set landscape orientation
- Use A3 paper size for wide tables (10+ columns)
- Color-code status cells (red=Pending, yellow=Submitted, green=Approved)

**Document reference:**
- Check DMP Sec 7.2 for project-specific discipline codes before assigning
- Check BEP Document Numbering Procedure for the authoritative standard
- Follow CG directive (Jun 2026): simple discipline-based numbering like AV-XXXX

**Writing style:** No verbose executive summaries or AI-sounding introductions. Brief, factual, direct.

### 10. File Placement — Subfolder Structure

For ALL subcontractor packages, create a **SPEC.md** in `_MANAGER_DASHBOARD/` FIRST, then generate the Excel register FROM it. The spec is the authoritative source; the register is a derived output.

SPEC.md structure (place at `Subcontractors/{NN}_{Name}/_MANAGER_DASHBOARD/SPEC.md`):
```markdown
# SPEC — {Discipline Name}
**Package:** {NN} — {Name}
**Folder:** `Subcontractors/{NN}_{Name}/`
**Appendix B ref:** {Name}
**SOW sections:** {relevant sections}
**Lead time:** {weeks or TBC}

## 1. Scope  ## 2. Exclusions
## 3. Deliverables by Stage  ## 4. Standards & Codes
## 5. Coordination Interfaces  ## 6. Long-Lead Items
## 7. Quality Gates
```

### 5c. _MANAGER_DASHBOARD/ Conventions

- **SPEC.md, SCOPE_REQUEST.md, SITUATION_REPORT.md** go in `_MANAGER_DASHBOARD/`
- **Excel registers stay in their own subfolder** (e.g., `Showcase_Submittal_Register/Showcase_Submittal_Register.xlsx`) — NOT in `_MANAGER_DASHBOARD/`
- **No draft email .md files** — delete `_Email_to_*.md`, `DRAFT_EMAIL_*.md`. Do not keep draft emails as files.

### 6. Categorize within Each Package Sheet

Group items by source category using merged header rows with green fill (`#E2EFDA`). Typical categories depend on discipline:

**Exhibition Fit-Out categories:**
- A — Exhibition Design Drawings (SOW 6.22)
- B — Graphic Design (SOW 6.22.1)
- C — Detailed Design Package (SOW 6.22.4)
- D — Off-Site Fabrication (SOW Part 3)
- E — QA / Commissioning / Handover
- F — BIM (SOW 6.20)

**AV categories:**
- A — Technical Design: AV Hardware (SOW 6.22.2 / 6.22.4)
- B — Off-Site Fabrication: AV Hardware Supply (SOW 8.9)
- C — PAVA & Fire Alarm (ER 3.5)
- D — Network & Telecoms (ER 3.3)
- E — Security Systems (ER 3.4)
- F — Electrical: AV Power Supply (ER 3.2)
- G — HVAC: AV Room Cooling (ER 5.0)
- H — QA / Testing / Commissioning / Handover

**FLS categories:**
- A — FLS Strategy
- B — Active Fire Protection
- C — Passive Fire Protection
- D — FLS Coordination
- E — Commissioning & Approvals
- F — QA / Handover

### 7. Columns per Sheet

| Column | Purpose |
|--------|---------|
| Ref # | Unique ID per item — discipline prefix (AV-xxx, FO-xxx) |
| Submittal / Deliverable | Exact wording from SOW document |
| SOW § | Section reference in Scope of Works (e.g., "6.22", "8.7") |
| ER § | Section reference in Employer's Requirements (e.g., "3.5", "—") |
| Discipline | Primary responsible party (AV / Elec / MEP / FLS / IT / Struct / BIM / QA) |
| 50% / 90% / 100% / IFC | Status per stage — blank when due, "—" when N/A. Populate as: Pending, Submitted, Under Review, Approved, Revise & Resubmit, Rejected |
| Sub-Package | Related sub-package grouping (e.g., "Exhibition Drawings", "Showcases") |
| Remarks | Cross-references, scale requirements, coordination notes |

### 8. Generate via Python Script

Write a generator script using `openpyxl` (run via terminal, not execute_code — sandbox lacks openpyxl). Save the script alongside the generated file for future regeneration:

```
02_Submittals/{Discipline}_Submittal_Register.py
02_Submittals/{Discipline}_Submittal_Register.xlsx
```

The script should:
- Define all items as tuples with stage masks
- Build 4 package sheets + Legend sheet using colour-coded headers
- Apply category grouping via merged header rows
- Save to all 3 locations

### 9. File Placement — Subfolder Structure

**CRITICAL — files MUST go inside named subfolders**, not as standalone files in parent directories. The user explicitly corrected this (Jun 2026).

Save the register to **3 locations** (update all copies from the same script run):

| # | Location | Purpose |
|---|----------|---------|
| 1 | `02_Submittals/{Discipline}_Submittal_Register/{Discipline}_Submittal_Register.xlsx` | Master copy — inside named subfolder |
| 2 | `Docs/09_Registers/{Discipline}_Submittal_Register/{Discipline}_Submittal_Register.xlsx` | Project-wide registers folder (inside named subfolder, matching other register patterns) |
| 3 | `Subcontractors/{NN}_{Subcon_Name}/{Discipline}_Submittal_Register/{Discipline}_Submittal_Register.xlsx` | Subcontractor working folder (inside named subfolder) |

Create subdirectory before saving:
```python
import os
for d in dirs:
    path = f'{base}/{d}/{register_name}/{register_name}.xlsx'
    os.makedirs(os.path.dirname(path), exist_ok=True)
    wb.save(path)
```

### 10. Email Drafting Pattern

When asked to send a register to a stakeholder:

```
To: {Name}
Subject: Aseer Museum — {Discipline} Submittals Register

Dear {Title} {Name},

Please find attached the {Discipline} Submittal Register for the Aseer Museum project.

The file is also available at:
`Bim Unit/Aseer-Museum/Subcontractors/{NN}_{Discipline}/{Register_Name}/`

Kindly confirm receipt.

Regards,
Mohamed Essa
Director of Technical Office & BIM Unit
```

→ Do NOT include register contents in the email body. The attachment is the register.

## Discipline Prefix Convention

Each submittal register uses a unique prefix matching the subcontractor discipline. **Before assigning a discipline code, verify against authoritative sources:**
- DMP Sec 7.2 naming convention for project-specific codes
- BEP Document Numbering Procedure (`Invoices/Docs/design managment plan/BEP/DOCUMENT NUMBERING PROCEDURE.xlsx`)
- Actual existing project documents (e.g., `MOC-MUS-ASE-1E0-ZD-0038` confirms 1E0 covers AV/Electrical in this project)
- CG directive (Jun 2026): Prefer simple discipline-based numbering (AV-XXXX, MEP-XXXX) over full project codes for submittals

| Discipline | Prefix | Example |
|------------|--------|---------|
| AV / IT | AV- | AV-001 |
| Exhibition Fit-Out | FO- | FO-001 |
| Graphics | GR- | GR-001 |
| Structural | ST- | ST-001 |
| MEP | ME- | ME-001 |
| FLS | FL- | FL-001 |
| Model Maker / Replicas | MM- | MM-001 |
| Lighting | LG- | LG-001 |
| Showcases | SC- | SC-001 |
| Rigging | RG- | RG-001 |
| FF&E | FF- | FF-001 |
| Interactives | IN- | IN-001 |
| Acoustic | AC- | AC-001 |
| Landscape | LS- | LS-001 |
| CITC / IT-Data | CT- | CT-001 |

Start numbering at 001 within each discipline.

## Single-Sheet vs Multi-Sheet Format

For small-scope disciplines (<20 items), a **single-sheet** format is acceptable instead of the 4-package-sheet structure:

- **Multi-sheet (4 packages):** AV, Exhibition Fit-Out, Graphics, Structural, MEP, FLS — these have 30+ items spanning all design stages
- **Single-sheet:** Small scopes (Oddy Testing Lab — 16 items). Use a "Design Stage" column instead of separate sheets.

Decision rule: if the discipline has deliverables at only one stage (e.g., testing at construction only), use single-sheet. If it spans design stages, use multi-sheet.

## Pitfalls

- **Must use EXACT SOW wording** — the user will reject paraphrased or extrapolated descriptions. Extract verbatim from SOW sections 6.22, 6.22.4, and Part 3.
- **References must be SOW or ER only** — no Interface Matrices, external specs, or other sources. If a deliverable has no SOW/ER reference, mark as "—".
- **50% stage must include surveys + Basis of Design + preliminary concepts** — not just site assessment items. The user corrected this (Jun 2026): 50% should cover existing conditions surveys, Basis of Design report, design programme, preliminary load schedules, preliminary SLDs, and concept-level designs for each discipline.
- **Network/Telecom and Security disciplines often lack 50% items** — need to add existing system surveys and concept assessments at 50% if the ER describes a scope that requires surveying existing conditions first.
- **Kick-off items** (transformer assessment, existing system survey) have all-zeros mask `[0,0,0,0]` — handle by marking with a "Preliminary" indicator rather than forcing them into a stage.
- **Sheet titles cannot contain `/`** — use double spaces ("IFC  AFC  Construction") instead of "IFC / AFC / Construction".
- **Subcontractor list = Appendix B only** — not the README. Oddy Testing Lab is not an Appendix B package.
- **QC before delivery** — always delegate review to Kimi/Claude/Codex before shipping. User reinforced this.
- **SPEC.md first, register second** — do not create the Excel register without first writing the SPEC.md. The spec is the source of truth. If you generate a register without a spec, you'll miss scope boundaries, exclusions, long-lead items, and coordination interfaces.
- **Long-lead check before stage assignment** — always check the subcontractor's README or SITUATION_REPORT for lead time data before assigning 50% stage masks. 14-week lead time = 50% needs 8+ items. 4-week lead time = normal 2-4 items is fine.
- **Delete draft email .md files** — `_Email_to_*.md` and `DRAFT_EMAIL_*.md` are not kept. Send the email directly via Outlook/SendMessage tool and delete the draft.

## Related

- [BIM Project Register (`bim-project-register`)](/skills/productivity/bim-project-register/) — for file-scan-based registers (Drawing Register, Submittal Register from files on disk). This reference covers the complementary workflow of creating registers from contract requirements.
- [Subcontractor Folder Setup (`subcontractor-folder-setup`)](/skills/productivity/subcontractor-folder-setup/) — for creating the subcontractor folder structure that receives the register copy.
