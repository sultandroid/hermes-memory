---
name: project-register-manager
description: Manage BIM project Excel registers by appending data to existing files. NEVER create new files — only find existing xlsx files and add rows. Use MD file caching (.pdf.md sidecars) to avoid rescanning.
version: 2.0.0
author: Hermes Agent
license: MIT
platforms: [macos]
metadata:
  hermes:
    tags: [bim, registers, excel, project-management, document-control, md-cache]
    related_skills: [samaya-technical-office]
---

# Project Register Manager

## 🔴 CARDINAL RULES (NEVER VIOLATE)

1. **SPEC.md FIRST, register second** — before generating any Excel register, write `SPEC.md` into the subcontractor's `_MANAGER_DASHBOARD/`. The spec defines scope, deliverables by stage, standards, coordination interfaces, and long-lead items. The Excel register is a **derived output** from the spec.
2. **SPEC.md in _MANAGER_DASHBOARD, register in its OWN subfolder** — spec file in `_MANAGER_DASHBOARD/SPEC.md`; Excel register in its own subfolder at subcontractor root (e.g., `Subcontractors/04_AV_IT_Contractor/AV_Submittal_Register/AV_Submittal_Register.xlsx`).
3. **Prefer updating existing Excel files** by appending rows. Only create new when the register type genuinely doesn't exist.
4. Always scan the project for existing `.xlsx`/`.xls` files first — all subdirectories.
5. Find the best-matching existing file by filename + column headers.
6. Append rows at the bottom of the data sheet — **never** overwrite or restructure.
7. Preserve ALL existing formatting, formulas, styles, merged cells, and structure.
8. Only if absolutely zero Excel files exist for a register type, then ask the user before creating.
9. Registers MUST have: Cover page (project info + revision history) + styled data sheet (dark blue headers, alternating rows, auto-filter, frozen panes).
10. Use format: `_Register.xlsx` suffix (not `_Log.xlsx` or bare name).

### Per-Register Column Templates (use exactly)
10. **Scan first, labor second** — use direct Python file-system scanning (`os.walk`) for enumeration tasks; reserve labor agents (Claude/Kimi) only for content analysis and decision-making on register entries
11. **Only update the exact register the user specifies** — do NOT auto-update sibling/related registers. If the user says "update ASM_Master_Material_Submittal_Register with X", only update that one file. Do not also update Material Sample Register, BOQ files, or other registers alongside it unless the user explicitly lists them. The user tracks specific registers only, and updating extra ones wastes their review time.

## Workflow

### Step 0: Plan → Audit → Implement
Before scanning a project or creating registers:
1. Read the project index (`bim_project_index.json`) to understand what exists
2. Audit the project's existing Excel files first
3. Proceed only after understanding the full picture

### Step 1: Find Existing Excel Files
---
file: original_filename.pdf
type: Submittal
date: 2026-05-28
project: Aseer Museum
code: ASR-SAM-KP-CV-PACK-SITE-001
subject: "description"
parties: [Samaya, CG, MoC]
revision: Rev 01
status: Submitted
checksum: md5_first64kb
---
Summary paragraph here...
```

## Workflow

### Step 1: Find Existing Excel Files
Scan ALL subdirectories for `.xlsx`/`.xls`/`.xlsb` files.
Match by filename keywords to determine register type.

**NEVER create new files — only append to existing ones.**

### Step 2: Read Project Files (Use Kimi CLI)
For reading/scanning project files and extracting data for registers, use **Kimi CLI**:
```
kimi -p "Scan all files in [project] and extract [data type] for [register type]" -y --afk --quiet
```
Kimi is faster and cheaper for file scanning than Claude Code.

### Step 3: Append to Existing Registers
For each existing Excel file:
1. Open with openpyxl (read-only mode to check structure)
2. Read headers from the data sheet
3. Map extracted data to matching columns
4. Append rows at the end (after last row with data)
5. Save preserving formatting

### Step 4: MD Sidecar Caching
When a labor analyzes a file:
1. Extract metadata (type, code, date, parties, subject)
2. Compute checksum (MD5 of first 64KB)
3. Write `.pdf.md` sidecar with YAML frontmatter + summary
4. If `.pdf.md` already exists with matching checksum → skip

## Excel Notes
- Use `openpyxl` for .xlsx files
- `.xlsb` files — do NOT modify (openpyxl incompatible)
- Always write to temp file first, then atomic rename
- Check if file is open in Excel before writing
- Preserve ALL existing formatting
- **Append rows only** — never create new sheets or files

### Register × Outlook Cross-Reference

When asked to "update from Outlook" or check if a register is current:
0. **Check register mtime** — `os.path.getmtime()` on the register file. If modified within 3-5 days, skip deep scan and report the file is already current. Saves 2+ min of SQLite + attachment work.
1. **Read the register** — extract current status per item (RFI/submittal/whatever)
2. **Query Outlook SQLite** — find related emails by vendor code, RFI ID, or subject keywords
3. **Extract attachments for verification (optional)** — when the email references a submittal code (ZD-, MS-, PL-) and has attachments, extract the PDF and run pdftotext to read the formal response code (A/B/C/D). Email subjects can be misleading — only the attached PDF has the actual decision.
4. **Compare** — check if status says "Escalated" but NRS already responded, or "Open" but a response thread exists
5. **Report discrepancies** — compact table with item ID, register status, email evidence, recommended update. Include peripheral findings (schedule updates, new drawings) that don't directly map to register rows.

See `references/register-outlook-reconciliation.md` for full workflow, SQL templates, and worked example (Showcase RFIs, June 2026).

## Related Reference Files

- `references/kpr-maintenance-pattern.md` — Full end-to-end workflow for KPR updates
- `references/stakeholder-plan-authoring-conventions.md` — SMP authoring conventions
- `references/gates-plan-alignment-workflow.md` — Full workflow for aligning register ref numbers and items with a consultant's Stage 04 Submission Plan (Gates plan): gap analysis, numbering patterns (per-floor sequences vs uniform), missing item categories, floor-zone reorganization, date handling, pitfalls.
- `references/cg-data-package-forwarding.md` (in `outlook-email` skill) — Extract, compare, map, and forward CG data packages (object schedules, material lists) with formal Excel deliverables
- `references/materials-register-from-nrs-schedules.md` — Full materials register creation from NRS 6930 exhibition schedules: 15 schedule types, NRS spec reference format (A2742-{CODE}), column structure, full project scope (~170+ items), Oddy testing requirements, Excel generation pattern, critical path items.
- `references/cross-subcontractor-conflict-audit.md` — Audit a new RFP/SOW against all other subcontractors for scope overlaps, interface gaps, contradictions, and missing coordination. Worked example: Acoustic Ceiling RFP vs 7 subcontractors (12 conflicts).

## Related Skills
- `samaya-technical-office` — project context, folder structure, document conventions
- `project-initializer` — for greenfield projects needing full folder scaffolding
- `subcontractor-procurement` — RFP generation, cross-subcontractor conflict audit, SPEC.md updates
- `design-change-control` — Backup Report (DCR) generation for Stage 3→4 deviations

## Key Lessons

### El-Ghamama Gift Shop 2 (May 2026)
- **Deduplicate immediately** on every append — collect all existing IDs first, skip any new entry whose ID already exists
- **Path prefix consistency** — if existing entries use `04_Design_Files/...`, new entries must match exactly; `Design Files/...` is a different path and creates duplicate entries for the same file
- **Cover sheet + data sheet** — registers have two sheets: `Cover` (project metadata, revision history) and the data sheet
- **Auto-filter** on the data sheet aids usability
- **`Submittal's` vs `Submittals`** — some projects use `Submittal's` (apostrophe). Always use the exact subfolder name found in the project
- **Labor CLIs for file enumeration are slow and timeout** — use direct `os.walk` Python for scanning 500+ files; reserve Claude/Kimi for content analysis and decision-making only
- **openpyxl lives on system Python 3.13** (`python3`), not the venv — use `terminal(python3 -c "...")` not `execute_code` for openpyxl operations

### Aseer Museum — NRS Showcase Routing (May 28, 2026)
- **NRS (Nissen Richards Studio) showcase submittals go to `Subcontractors/01_Showcase_Contractor/`**, NOT `Submittals/Showcases/From NSR/`
- When filing NRS submittals, invoices, and M&E docs: `Subcontractors/01_Showcase_Contractor/Submittal_NN_date/` or `Subcontractors/01_Showcase_Contractor/Lighting_*.pdf`
- Always confirm the correct subfolder with the project's existing folder structure before filing
- After filing: append to `Register_ASEER_Professional.csv` (path: `.../Email Archive/مشروع متحف عسير الإقليمي/`)

### Register Audit Against Filesystem

When a user asks why a role/subcontractor is missing from a register, or to verify completeness:
1. See `references/register-audit-against-filesystem.md` for the full multi-source audit workflow
2. Cross-reference: Excel register ↔ live `Subcontractors/` folder ↔ contract obligation docs ↔ recent scope requests
3. Determine root cause: newly-identified gap vs out-of-scope vs overlapping role
4. Report findings with exact gap, root cause, and recommended new row content

### Communication Rule (ALL tasks — no exceptions)
- **ALWAYS report task completion to Mohamed Essa** for every task, including terminal/CLI commands
- Do NOT say "ok done" or bare acknowledgments — state specifically what was done, what changed, and any issues
- This applies to: file copies, moves, conversions, PDF extractions, register updates, email operations, everything

### Drawing Register vs Submittal Register

Two distinct register types exist:

| Dimension | Submittal Register | Drawing Register |
|-----------|-------------------|------------------|
| **What it tracks** | SOW/ER deliverables by item code (FL-001, SC-003) | Actual drawing sheets by number (LSP-01, SLF-0001) |
| **Source** | SOW scope + ER requirements | Submitted PDF/DWG files found on filesystem |
| **Key columns** | Ref #, Submittal/Deliverable, SOW §, ER §, Stage mask (50/90/100/IFC) | Drawing #, Title, Format, Level, Latest Rev, Submitted, Returned, Status, Comments |
| **Status** | Stage completion (in_progress/done) | CG review code (A/B/C/D) |
| **Use case** | What the contractor must deliver per contract | What was actually received and where it's at in review |

**Drawing Register creation workflow:**
1. **Discover files** — search all project directories where drawings may reside (Submittals/, Docs/03_Submittals/, Email_Archive/, Completed_Tender_Package/, Subcontractors/.../Existing_FLS_AsBuilt/). Check both old and newly reorganized paths (the project may have been restructured).
2. **Categorize** — actual submittal sheets (the submitted drawing set) vs reference drawings (fire strategy, fire fighting, existing conditions)
3. **Determine status** — check CG response PDFs and emails for the review code. A/B = approved, C = revise & resubmit, D = rejected
4. **Include the submittal transmittal** — the cover PDF (e.g. MOC-MUS-ASE-1K0-IFC-0004.pdf) and any CG comments PDF
5. **Highlight the blocking issue** prominently — Code C always needs a clear note about why
6. **Structure sheets** — Drawing Register (main data), Status Summary (condensed overview), CG Comments (verbatim text from reviewer)
7. **Store** in the subcontractor's `FLS_Submittal_Register/` alongside the existing submittal register

### SOW/ER-Based Submittal Register Creation

When Mohamed asks for a **submittal register** for a subcontractor discipline from the SOW or ER:

1. **Locate source documents** — SOW lives in `Contracts/01_Main_Contract/Contractors Scope of Works Document - Technical_250313/`; ER lives in `Contracts/01_Main_Contract/Contractors Employers Requirements - Engineering_250313/`. Both are PDF.
2. **Extract text** using `python3 -c "import fitz; doc = fitz.open('path.pdf')"` (system Python 3.13 has pymupdf). Use `terminal()` not `execute_code` — pymupdf/openpyxl aren't in sandbox.
3. **Extract deliverables by SOW section** — especially SOW 6.22.x (Technical Design Deliverables), SOW 6.9 (Design Phase Submittals), SOW 6.10-6.18 (product data/certificates), SOW Part 3 (Off-Site Fabrication sections 8.x), and ER 3.x (MEPF/IT/Security scope).
4. **Use EXACT SOW wording** for descriptions — Mohamed corrected: "list same as SOW Listed". Copy the deliverable name verbatim from the SOW. Do NOT paraphrase or extrapolate. Add clarifying notes only in the Remarks column.
5. **Every SOW-listed deliverable gets its own row** — do NOT collapse related items. Mohamed asks about specific items if missing (e.g. "where is the setwork?").
6. **Organize by design stage (package)** per SOW 6.22.4 — each package gets its own sheet:
   - **50% Design Package** — interim: block schematics, design intent
   - **90% Design Package** — draft final: refined drawings, coordinated layouts
   - **100% Design Package** — final: fully coordinated, ready for IFC
   - **IFC / AFC / Construction** — post-design: shop dwgs, fabrication, handover
   For small-scope subcontractors (e.g. Oddy Testing Lab), a single-sheet register is acceptable.
7. **Item mask pattern** — each item has a `[50%, 90%, 100%, IFC]` mask controlling which sheets it appears in. Single items can span multiple stages.
8. **Category headers** matching SOW section structure within each sheet.
9. **Column structure**: Ref #, Submittal, SOW §, ER §, Discipline, 50%, 90%, 100%, IFC/AFC, Sub-Package, Remarks. Status columns are blank for items due; "—" = not applicable.
10. **References only SOW and ER** — no external specs, interface matrices, or other sources.
11. **Subfolder organization** — ALL copies go into subfolders (not standalone files):
    - `02_Submittals/<Register_Name>/<Register_Name>.xlsx` — working original + generator script
    - `Docs/09_Registers/<Register_Name>/<Register_Name>.xlsx` — project-wide
    - `Subcontractors/NN_xxx_Contractor/<Register_Name>/<Register_Name>.xlsx` — subcon root
    The subfolder name matches the register name. Other registers in 09_Registers/ follow this pattern.
12. **Two delivery files always** — after creating the individual register, ALSO generate `Master_Submittal_Register.xlsx` (Dashboard + all packages) and `Design_Schedule_Programme.xlsx` (programme from DMP data). Deploy both to `_MANAGER_DASHBOARD/` of all subcontractors.
13. **Long-lead item flagging** — check the project README and existing SCOPE_REQUESTs for lead times BEFORE creating the register. Packages with 8+ week lead times (Showcases 14wks, MEP 12-16wks, Exhibition Fit-Out 8-12wks, FF&E 8-12wks) need more items at 50% stage to enable early procurement. Mohamed will call you out if 50% is too thin — "why you waite me to tell you".
14. **SPEC.md-first workflow** — write SPEC.md (scope, deliverables by stage, standards, coordination, long-lead items) BEFORE generating the Excel register. The register is a derived output from the spec, not the source of truth.

### Draft Email .md Cleanup Rule
- **NEVER leave draft email .md files in the project** — Mohamed explicitly removed all `_Email_to_*.md` and `draft_email_*.md` files. If you draft email text, deliver it in the conversation reply, not as a file. Email drafts are transient communication, not project records.
- Cleanup command pattern: `find <project_root> -iname "*draft*email*" -o -iname "*_email_to_*" 2>/dev/null | grep -i "\.md$" | xargs rm`

### 2-Week Look-Ahead Tool
When asked to generate a short-term design programme:
1. Create a **2-Week Look-Ahead** Excel with two sheets
2. **Sheet 1** — Prioritized tasks (P0/P1/P2/P3) with: Priority, Package, Submittal/Task, Responsible, Target Date, Dependencies, Status, Action Required
3. **Sheet 2** — Daily Actions — day-by-day tasks for the next 14 days
4. Priority levels: P0=Today, P1=Critical this week (🔴), P2=By week 2 (🟡), P3=Within 2 weeks (🟢)
5. Base it on what's not yet submitted at the current stage (cross-reference the Master Register)

### Mermaid Gantt Export
When generating a schedule, also produce a **Mermaid `.mmd` Gantt script** that renders in Obsidian/GitHub/VS Code:
1. Each subcontractor package = one section
2. Stage durations mapped from DMP day milestones (D0→D35→D65→D82→D88)
3. Use `dateFormat YYYY-MM-DD` with `axisFormat %d-%b`
4. Emoji section headers for visual scanning
5. Save to same location as the Excel programme file
6. Deploy to all subcontractor `_MANAGER_DASHBOARD/` folders

### DMP Milestone Integration for Design Programme

When generating a **Design Schedule Programme** from master register data:
1. Reference DMP Rev C04 milestone days: D0(LOA), D35(50%), D65(90%), D82(IFC NOC), D88(AFC NOC), D90(site), D300(TOC)
2. Use 10-day column increments for Gantt (D0, D10, D20... D90)
3. Flag critical path: MEP (12-16wks, serves all trades) and Showcases (14wks longest procurement)
4. Add dependencies matrix: who depends on whom
5. Legend must reference DMP doc code and dates
6. Deploy to all subcontractor `_MANAGER_DASHBOARD/` folders alongside Master Register

### Master Register Generation

After all individual package registers exist:
1. Generate `Master_Submittal_Register.xlsx` with **professional format** — 4 reference sheets + package sheets:
   - **Cover** — doc control block (SAM-MSR-001, Rev, Date), DMP gate summary table
   - **Dashboard** — all packages with auto-filter, status colour-coding (🟢🟡🔴), alternating rows, totals row
   - **DMP Reference** — mapped sections from DMP Rev C04 to register items
   - **Legend** — column descriptions, colour key, user guide
   - **01–21** — individual package registers
2. Dashboard columns: #, Package, DMP Gate, Doc Type, 50%, 90%, 100%, IFC, Total, Status, Lead Time, Contractor, Flag
3. Generator script at `02_Submittals/Master_Submittal_Register.py`
4. Deploy to `Docs/09_Registers/_Master_Submittal_Register/` and all subcontractor `_MANAGER_DASHBOARD/` folders

### QC Gate Before Delivery (Mandatory)

Before presenting ANY register to the user:
1. **Self-review**: verify stage assignments, long-lead flags, SOW wording accuracy, 50% package thickness
2. **Delegate QC to Kimi** (`delegate_task` with the generator script) — ask specifically about:
   - Completeness against SOW scope
   - Appropriate stage assignments (50% too thin? items in wrong stage?)
   - Missing long-lead items
   - Cross-package coordination gaps
3. **Apply QC findings before presenting** — Mohamed expects thorough packages
4. If the user said "next" repeatedly, QC is still mandatory **on the batch** before reporting

### Subcontractor Numbering Per Appendix B
- **ALWAYS** use `Subcontractors/_assets/APPendix B.pdf` as the authoritative subcontractor list, NOT the README
- Number folders to match Appendix B sequence, not arbitrary or README order
- Related packages grouped together (technology cluster, MEP cluster, structural cluster, fit-out cluster)
- Use temp names during renumbering to avoid conflicts on OneDrive:
  ```
  mv 03_AV_IT zz_temp
  mv 08_Graphics 03_Graphics
  mv zz_temp 04_AV_IT
  ```
- Update ALL generator script paths after any renumbering, then regenerate all registers
- Non-Appendix-B folders merged into related main packages (e.g., Oddy → Exhibition Fit-Out QA)

### 09_Registers Serialization Rules
- `_Master_Register_Index/` and `_Master_Submittal_Register/` have NO serial numbers (`_` prefix sorts first)
- Real registers get `01_` to `NN_` serial prefixes
- No loose `.xlsx` files at root — every file in its own subfolder
- `Specialist/` folder with design consultants kept as separate group

#### Register Creation from External Source Data (Non-SOW/ER)

When creating a submittal register from an **existing project plan or schedule** (not directly from SOW/ER PDFs):

1. **Map source columns to target** — the standard target columns are: Ref #, Submittal/Deliverable, Discipline, 50%, 90%, 100%, IFC/AFC, Sub-Package, Remarks. Map source data accordingly:
   - Drawing Package → Submittal/Deliverable (keep the drawing number prefix: `1100 - Existing GA Plans`)
   - Level/Zone + Package → combine in description (`1100 - Existing GA Plans — Basement Floor`)
   - Gate/Stage value → convert to [50%,90%,100%,IFC] mask
   - Submission Category → Sub-Package
   - Status or Remarks column → Remarks

2. **Determine stage from Gate/Phase column** — typical mappings:
   | Source Phase | Target Sheets |
   |---|---|
   | Gate 1 / Detailed Design / 50%/90%/100% | All three DD sheets: [1,1,1,0] |
   | Gate 2 / Material Approval | IFC only: [0,0,0,1] |
   | Gate 3 / Coordinated IFC / IFC | IFC only: [0,0,0,1] |
   | BIM / Standalone (covers all phases) | All four: [1,1,1,1] |

3. **Create unique ref numbers** — use a discipline prefix (AR-, ST-, ME-, etc.) with sequential numbering. Group by category (A=Existing, B=Proposed, C=Sections, etc.)
   - Ref range boundaries should align with category breaks for the category header system: `{1:'A — CATEGORY NAME', 13:'B — NEXT CATEGORY'}`
   - Ensure the group size in `cn = {...}` matches the range (e.g., `rn + 12` for a 12-item category)

4. **Handle repeated items across levels** — when the same drawing package set repeats per floor/level:
   - Create one item PER LEVEL (not one item for all levels)
   - Include the level name in the description
   - Group by drawing type category, not by level

5. **Category header logic** — the generator uses `cn = {ref_start: 'CATEGORY NAME'}` dictionary. The `for ref, desc, disc, mask, spkg, rm in its:` loop checks `if rn in cn` and inserts a merged-row category header. Set the search range (`rn + 12` etc.) wide enough to catch all items in that category.

6. **Stage mask patterns** — each item has `[50%, 90%, 100%, IFC]`:
   - `[1,1,1,0]` — appears in all three DD sheets
   - `[0,0,0,1]` — appears only in IFC/AFC sheet
   - `[1,1,1,1]` — appears in all sheets
   - Items filter by matching `mask[index]==1` for each sheet

### Dynamic Category Boundaries with `next_cat`

For date-based registers with non-uniform category sizes (e.g., 16 items per floor, then 1 item, then 2 items), replace hardcoded range arithmetic with a computed dict:

```python
cn = {0:'PRELIMINARY — ITEM', 1:'A — FLOOR', 17:'B — NEXT FLOOR',
      33:'C — NEXT FLOOR', 49:'D — NEXT FLOOR', 65:'E — BIM',
      67:'F — MATERIAL', 68:'G — COORD IFC'}
cn_keys = sorted(cn.keys())
next_cat = {k: cn_keys[i+1] if i+1 < len(cn_keys) else 999
            for i, k in enumerate(cn_keys)}

# In the generation loop:
if rn in cn:
    grp = [it for it in its
           if int(it[0].split('-')[1]) >= rn
           and int(it[0].split('-')[1]) < next_cat[rn]
           and it[3][si] != '—']
```

This pattern handles any mix of category sizes without manual range arithmetic. Works with both mask-based (`it[3][si] != '—'`) and date-based filters.

### Digital Material Board as stand-alone preliminary item

When the user asks for a cross-platform deliverable (digital material board, VR tour, etc.), add it as a **separate row** in the register, not appended to an existing description:

```python
# At top, before floor loop:
its.append((f'AR-{ref:03d}', 'Digital Material Board — Basement Floor',
            'Architectural', ['29/06/2026', '—', '—', '—'], '3D Viz', ''))
ref += 1

# Category header for it:
cn = {0:'PRELIMINARY — DIGITAL MATERIAL BOARD', 1:'A — BASEMENT FLOOR', ...}
```

Rules:
- Give it its own category header (PRELIMINARY, before category A)
- Use ref AR-000 so it sorts before floor items
- 50% only unless user specifies otherwise
- Same date as the floor it belongs to (or earlier if "before DD of its floor")
- Sub-Package should match the related discipline (e.g., '3D Viz')

7. **Legend sheet** — always include: Column → Description, Ref # → prefix pattern, Scope → brief description of the register's coverage.

8. **Per-level vs consolidated** — external plans often list per-level items separately. The register format works best with individual items per level (easier to track per-level status) rather than consolidated "all levels" items. Exception: coordinated IFC items that truly apply to all levels at once.

### .py Generator Data Recovery from .xlsx

When a .py generator script's data tuples are corrupted (e.g., commas inside strings were treated as tuple separators by a bad regex, or the entire `its = [...]` block was mangled):

**BEST APPROACH: Rebuild from the matching .xlsx file**

The .xlsx files are the source of truth for register data. The .py scripts are generators. If the .py data is broken, read from the clean .xlsx:

```python
import openpyxl

# Open cleaned xlsx (data_only=True for computed values)
wb = openpyxl.load_workbook(register_xlsx_path, data_only=True)
ws = wb.active

# Extract headers and data rows
headers = [str(ws.cell(row=1, column=c).value or '') for c in range(1, ws.max_column+1)]
rows = []
for row_idx in range(2, ws.max_row + 1):
    row_vals = [ws.cell(row=row_idx, column=col).value for col in range(1, ws.max_column + 1)]
    if any(v for v in row_vals if v is not None and str(v).strip()):
        rows.append(row_vals)

# Format as Python tuple strings, then replace the its = [...] block
for row_vals in rows:
    t = '(' + ', '.join(repr(v) for v in row_vals) + '),'
    tuple_lines.append(f"{inner_indent}{t}")
```

**Key steps for .py recovery:**
1. Fix headers line (`hdrs = [...]`) — remove SOW/ER columns
2. Fix column widths (`cww = [...]`) — remove width entries
3. Rebuild data tuples from .xlsx data
4. Fix for-loop unpacking (`for ref, desc, sow, er, disc, mask, spkg, rm` → `for ref, desc, disc, mask, spkg, rm`)
5. Fix `vs = [ref, desc, sow, er, disc, ...]` line
6. Verify with `python3 -c "compile(open('file.py').read(), 'file.py', 'exec')"`
7. Check no SOW/§ remain: `grep -n 'SOW\\|§' file.py`

**NEVER split on commas** to parse Python tuple strings. Use `ast.literal_eval()` for individual tuples or read from the .xlsx as shown above.

See `references/aseer-architecture-register-creation.md` for a worked example.

## Mohamed Essa — Register Tracking Preference (June 2026)
- Mohamed ONLY tracks/maintains **ASM_Master_Material_Submittal_Register** for QC/Equipment items
- **Do NOT** update other material/sample registers (Material Sample Register, MSR, BOQ Materials Register, etc.) alongside it unless explicitly asked
- If the user says "i only follow on this :ASM..." — that is a correction. Stop immediately and revert/undo changes to other registers
- For Aseer Museum specifically: the `09_Registers/` copy and the `03_Submittals/03.3_Material_Submittals/` copy of ASM_Master_Material_Submittal_Register have DIFFERENT column structures. Always check which version the user is referring to before updating

### Time Tracking After Every Task
When working on an Odoo task (project.task), **always log session time** to the task's timesheet (`account.analytic.line`) via XML-RPC after completing work. Record:
- `task_id` — the Odoo task ID
- `project_id` — the project ID (e.g., 219 for Aseer Museum)
- `unit_amount` — duration in hours (estimate based on session effort)
- `name` — brief description of work done
- `date` — the work date

```python
m.execute_kw(db, uid, password, 'account.analytic.line', 'create', [{
    'task_id': 3211,
    'project_id': 219,
    'unit_amount': 4.0,
    'name': 'Description of work done',
    'date': '2026-06-16',
}])
```

This is a standing requirement — Mohamed explicitly corrected: "always update the time sheet in the task with session time, always track my time in task by session time"

### Aseer AV Submittal Register (June 2026)
See `references/aseer-av-submittal-register-creation.md` for the full reference — source documents, SOW/ER sections mapped, package breakdown, deployment locations, and AV systems matrix. Generated as a 4-sheet register (50%/90%/100%/IFC).

## KPR/Register Classification: Appendix B Mapping

When mapping contract Appendix B requirements against a Key Personnel Register or Stakeholder Plan:

### Step 1: Understand the Two-Column Structure
Appendix B typically has two distinct columns:
- **Left column: "Specialist Contractor Packages"** — subcontractor companies that do packages of work (supply, install, or both)
- **Right column: "Specialists"** — individual consultants/experts providing design or advisory services

### Step 2: Determine Designer vs Contractor/Installer Split
For each package, determine if it is a **combined entity** or a **split**:

| Pattern | Meaning | Example |
|---------|---------|---------|
| **Combined** | One entity does design + supply + install | Samaya Graphit (graphics), Glasbau Hahn (showcases), Samaya Factory Replica Dept (models & props) |
| **Split** | Designer is a different entity from the supplier/installer | ZNA (lighting design) vs M&E Contractor (lighting fixture install) |

Never assume one pattern or the other — ask the user or check meeting records.

### Step 3: Classify Each Row by Who Hires
Not every role in Appendix B is Samayas responsibility to fill. Classify each as:

| Category | Meaning | KPR Placement |
|----------|---------|---------------|
| **Samaya internal** | Samaya employees (PM, BIM, QA/QC, HSSE, site team, factory staff) | Main section, Tier 1 |
| **Samaya hires** | Subconsultants or subcontractors Samaya appoints (structural eng, MEP, AV, lighting, etc.) | Main section, Tier 2 |
| **Samaya must appoint** | Independent third-party roles Samaya must contract (ITCA) | Main section with note |
| **Authority / Statutory** | Government/regulatory bodies that approve design or issue permits (SEC, MOI, CITC, Municipality) | **Separate section** at bottom - tracked as reference, not Samaya hires |

DO NOT add rows for roles Samaya does not need to fill (e.g., FF&E supplier if not in scope). Always ask if unclear.

### Step 4: Document the Split in KPR Notes
When updating the KPR with Designer/Installer splits, use clear notes:
- For designers: "[Role] - design only. Installation by [Installer]."
- For installers: "[Role] - supply and install. Design by [Designer]."
- For combined: "[Role] - full scope: design, production and installation."

### Example: M&E Package
KPR R9  - MEP Specialist           = AD Engineering (design only, Code B)
KPR R10 - M&E Contractor (Install) = TBC (installs MEP + FLS + lighting fixtures)

## Bulk Register Cleaning (Remove SOW/ER/§ from Existing Registers)

When asked to remove SOW § / ER §b columns and all SOW/ER references from ALL existing register files (both .xlsx and .py):

### Strategy: xlsx First (Deliverable), Then .py (Generator)

The .xlsx files are the primary deliverables. The .py scripts are generators that produce the .xlsx output. Clean xlsx first, then fix .py scripts.

### xlsx Cleaning Workflow

1. **Walk all sheets** — registers have multiple sheets (50%, 90%, 100%, IFC, Legend). Each needs separate handling.

2. **Find SOW/ER columns by header text** — check row 1 of each sheet for headers containing "SOW" or "ER":

```python
cols_to_delete = []
for col in range(1, ws.max_column + 1):
    val = ws.cell(row=1, column=col).value
    if val and str(val).strip() in ['SOW', 'ER', 'SOW §', 'ER §', 'ER §b']:
        cols_to_delete.append(col)
```

3. **Delete columns right-to-left** — after `delete_cols()`, all subsequent column indices shift. Use EXACT header matching, NEVER substring matching:
   - `str(val).strip() in ['SOW', 'ER', 'SOW §', 'ER §', 'ER §b']` ✓
   - `'SOW' in str(val).upper()` ✗ — catches "Submittal / Deliverable (per SOW)" and deletes the description column

```python
for col in reversed(cols_to_delete):
    ws.delete_cols(col)
```

4. **Clean all cells** — iterate ALL cells across ALL sheets, remove:
   - `§` symbol
   - `\xa7` escape
   - `(per SOW)`, `(per SOW / ER)` 
   - `(SOW 6.22)`, `[SOW ...]` pattern references
   - `SOW 6.22.2 / 6.22.4` section references
   - `SOW/ER` standalone references
   - `per SOW` / `per ER` phrases

Use regex patterns in order, then cleanup:

```python
sow_er_patterns = [
    r'\(per SOW(?: / ER)?\)',
    r'\s*\(SOW[^)]*\)',
    r'\s*SOW\s+[\d.]+[/\d.]*',
    r' per SOW[^,\')]*',
    r', SOW[^,\')]*',
    r'SOW/ER',
]
for pat in sow_er_patterns:
    new = re.sub(pat, '', new)
```

5. **Verify** — re-open each xlsx and scan all cells for any remaining `§` or `SOW` (excluding false positives like "SHOWCASE", "ALLOW", "WINDOW", "KNOWS"):

```python
if 'SOW' in val.upper() and 'ALLOW' not in val.upper() and 'SHOW' not in val.upper():
    print(f"  SOW: {fname}/{sn} R{r}C{c}: {val[:80]}")
```

6. **Save in-place** — `wb.save(fp)` with the same path.

### .py Generator Script Cleaning

The `.py` files are generated with embedded data tuples. They follow a template with `its = [...]` or `items = [...]` arrays. Cleaning them requires:

1. **Fix headers** — remove `'SOW \xa7'`, `'ER \xa7'` from `hdrs = [...]`
2. **Fix column widths** — remove the two width entries from `cww = [...]`
3. **Fix data tuples** — remove the sow/er fields (indices 2 and 3) from each tuple in `its = [...]`
4. **Fix unpacking** — change `for ref, desc, sow, er, disc, mask, spkg, rm in its:` → `for ref, desc, disc, mask, spkg, rm in its:`
5. **Fix row building** — change `vs = [ref, desc, sow, er, disc, ...]` → `vs = [ref, desc, disc, ...]`
6. **Remove §** from all strings
7. **Clean docstrings/comments** referencing SOW/ER
8. **Clean Legend entries** referencing SOW/ER

**CRITICAL: Never use comma-splitting to restructure Python data tuples.** Tuples with string fields may contain commas inside quoted strings (e.g., `'description with, comma inside'`). Splitting on commas destroys the data. Always use one of:

- **`ast.literal_eval()`** — parse each tuple line, modify the parsed tuple, then `repr()` it back
- **Read from the already-cleaned .xlsx** — open the cleaned xlsx with openpyxl, extract data rows, format as Python tuple strings, replace the `its = [...]` block
- **Read with openpyxl** from the matching .xlsx (they have the same name):
```python
wb = openpyxl.load_workbook(xlsx_path, data_only=True)
ws = wb.active
# Extract rows, skip header
rows = []
for row_idx in range(2, ws.max_row + 1):
    row_vals = [ws.cell(row=row_idx, column=col).value
                for col in range(1, ws.max_column + 1)]
    if any(v for v in row_vals):
        rows.append(row_vals)
# Format as Python tuple
for row_vals in rows:
    t = '(' + ', '.join(repr(v) for v in row_vals) + '),'
```

### .py File Verification

After all changes:
```bash
# Check syntax
python3 -c "compile(open('file.py').read(), 'file.py', 'exec')"
# Check for remaining SOW/§
grep -n 'SOW\|§\|\\\\xa7' *.py
```

### Common Issues

- **Openpyxl only reads `data_only=True`** — use this to get computed values not formulas
- **Legend sheets** have different column structures — they're 2-column (name, description) not register columns. Don't try to delete columns from them; just clean cell content
- **Category names** may be in merged cells (column A) with SOW references like `A — TECHNICAL DESIGN: AV HARDWARE (SOW 6.22.2 / 6.22.4)`. These need regex cleaning, not column deletion
- **Some registers have `headers = [...]` instead of `hdrs = [...]`** (e.g., Oddy_Testing uses `headers`). Check both patterns
- **Some registers have different tuple structures** (e.g., Oddy has 11-field tuples with stage/status columns). Adjust field indices per file
- **`delete_cols()` may leave empty trailing columns** — verify final column count matches expected header count after cleaning
- **xlsx column deletion pitfall: NEVER substring-match column headers** — `'SOW' in str(val).upper()` catches "Submittal / Deliverable (per SOW)" and **deletes the entire description column**. Always use exact match: `str(val).strip() in ['SOW', 'ER', 'SOW §', 'ER §', 'ER §b']`. Verify after deletion: 'Submittal' or 'Deliverable' must still exist in headers.

## Date-Based Stage Columns (Alternative to Stage Masks)

The default format uses stage masks `[1,1,0,0]` with blank/`—` stage indicators. An alternative format uses **planned dates** in the stage columns:

### When to use dates instead of masks

- User asks "what are the 50%/90%/100%/IFC columns for?"
- User wants to track submission deadlines per stage
- User says "plan all submissions" with a target IFC date

### Data format

Each item uses date strings instead of binary masks:

```python
# Old (mask-based):  (ref, desc, disc, [1,1,0,0], spkg, rm)
# New (date-based):  (ref, desc, disc, ['29/06/2026','29/07/2026','28/08/2026','—'], spkg, rm)
```

- `'—'` = N/A at this stage (item won't appear in that stage's sheet)
- Date string = planned submission date at that stage
- No blanket blanks — every cell is explicitly a date or `'—'`

### Template changes

1. **Column widths** — widen stage columns for dates (7 → 14):
   ```python
   cww = [7, 50, 14, 14, 14, 14, 14, 20, 28]
   ```

2. **Stage index variable** — iterate with index, not lambda:
   ```python
   stages = [('50% Design', p50, 0), ('90% Design', p90, 1),
             ('100% Design', p100, 2), ('IFC  AFC  Construction', pifc, 3)]
   ```

3. **Filter by date, not mask** — replace `if not ff(mask): continue`:
   ```python
   dt = dates[si]
   if dt == '—': continue
   ```

4. **Only show the relevant stage's date per sheet** — other stage columns get `'—'`:
   ```python
   show_dates = ['—', '—', '—', '—']
   show_dates[si] = dates[si]
   vs = [ref, desc, disc, show_dates[0], show_dates[1],
         show_dates[2], show_dates[3], spkg, rm]
   ```

5. **Category visibility check** — the category header only appears if at least one item in its range has a non-`'—'` date at this stage:
   ```python
   if rn in cn:
       grp = [it for it in its
              if int(it[0].split('-')[1]) >= rn
              and int(it[0].split('-')[1]) < (rn + 12 if rn < 65 else 100)
              and it[3][si] != '—']
       if grp:
           # insert category header
   ```

### Staggered submission scheduling

When building a register from a plan organized by level/floor, stagger dates per level to create a 7-day review buffer:

| Floor | 50% | 90% (+30d) | 100% (+30d) |
|-------|-----|------------|-------------|
| Basement | 29/06 | 29/07 | 28/08 |
| Lower Ground | 06/07 (+7d) | 05/08 | 04/09 |
| Ground | 13/07 (+14d) | 12/08 | 11/09 |
| First Floor | 20/07 (+21d) | 19/08 | 18/09 |

Implementation pattern — define floor dates once, reuse in loop:

```python
FLOOR_DATES = {
    'Basement Floor':      ['29/06/2026', '29/07/2026', '28/08/2026', '—'],
    'Lower Ground Floor':  ['06/07/2026', '05/08/2026', '04/09/2026', '—'],
    'Ground Floor':        ['13/07/2026', '12/08/2026', '11/09/2026', '—'],
    'First Floor (Structure)': ['20/07/2026', '19/08/2026', '18/09/2026', '—'],
}

for floor_name, d in FLOOR_DATES.items():
    for pkg_name, subpkg in PKGS:
        dates = list(d)  # copy — don't mutate the floor template
        # Per-item overrides (e.g. 50%-only items)
        if 'Visualisation Shots' in pkg_name:
            dates = [d[0], '—', '—', '—']
        desc = f'{pkg_name} — {floor_name}'
        # Per-item description additions
        if floor_name == 'Basement Floor':
            desc += ' + Digital Material Board'
        its.append((f'AR-{ref:03d}', desc, 'Architectural', dates, subpkg, ''))
        ref += 1
```

Category boundaries must align with ref numbering. For level-based grouping:
```python
cn = {1:'A — BASEMENT FLOOR', 17:'B — LOWER GROUND FLOOR', ...}
```
Each level gets 16 items (all drawing packages), so next level starts at ref 17, 33, 49, etc.

### IFC-only items

QA/Commissioning/Handover items get IFC-only dates:
```python
['—', '—', '—', '28/08/2026']
```

### BIM/Standalone items covering all stages:
```python
['27/07/2026', '26/08/2026', '25/09/2026', '28/08/2026']
```

### Legend entry for date-based registers

```python
('Schedule', '50%: floors staggered 7d apart. 90%=+30d, 100%=+30d, IFC=+60d max.')
```

### Bulk date shift (+1 day)

When the user says "start from [date]" instead of the current baseline, shift all dates in ALL generator scripts:

```python
import os, re
from datetime import datetime, timedelta

SCRIPTS = '/path/to/scripts/'
date_pat = re.compile(r'(\d{2})/(\d{2})/(\d{4})')

def shift_date(m):
    day, mon, year = int(m.group(1)), int(m.group(2)), int(m.group(3))
    dt = datetime(year, mon, day) + timedelta(days=1)
    return dt.strftime('%d/%m/%Y')

for fname in os.listdir(SCRIPTS):
    if not fname.endswith('.py'): continue
    fp = os.path.join(SCRIPTS, fname)
    with open(fp, 'r') as f: content = f.read()
    new_content = date_pat.sub(shift_date, content)
    if new_content != content:
        with open(fp, 'w') as f: f.write(new_content)
```

Then re-run all scripts to regenerate xlsx files. Note: the scripts save to `/tmp/DATED_REGISTERS/` — copy from there to OneDrive via Finder AppleScript.

### OneDrive xlsx deployment: Use AppleScript `duplicate`

Scripts save xlsx to `/tmp/`. Deploy to OneDrive via Finder, NOT direct `cp` or `wb.save()` to OneDrive path:

```python
# Generate xlsx to /tmp
tmp = '/tmp/Register_Name.xlsx'
wb.save(tmp)

# Deploy via AppleScript
osascript -e f'tell application "Finder"
    set src to POSIX file "/tmp/Register_Name.xlsx"
    set destFolder to POSIX file "{base}/Register_Name/"
    duplicate src to destFolder with replacing
end tell'
```

Direct writes to OneDrive (`CloudStorage/` path) produce corrupt placeholder files. Verify after copy with `xxd -l 8` (must start `PK\x03\x04`).

### OneDrive scripts folder naming

On this project, the scripts folder is `_scripts` (underscore prefix sorts first), NOT `scripts`. Always `ls` the parent directory first to confirm the actual folder name before running batch operations like `grep`, `sed`, or batch runs.

### Graphics and Model Maker: No Dates (RFI Pending)

Graphics and Model Maker registers use **mask-based format** (blank/—), NOT dates. RFI raised to client for research/data. Legend should note: "Dates TBC — RFI raised to client for research/data."

Check memory for `Graphics and Model Maker submittal registers: NO dates` before adding or shifting dates in these two registers.

When a user mentions "digital material board" or similar cross-platform deliverable, add it as a description suffix on the relevant register item:

```python
desc = f'{pkg_name} — {floor_name}'
if 'Visualisation Shots' in pkg_name and floor_name == 'Basement Floor':
    desc += ' + Digital Material Board'
```

### Design vs Procurement Register Scope

Not every discipline needs a design submittal register. Before creating one:

1. **Check the BOQ** — if the BOQ has no sheet for that discipline, the register may be out of scope. The project's `05_BOQ/` file has sheets: Design, Enabling, Finishes, Furniture, Display Cases, Lighting & Power, Security/Data/Life Safety, Plumbing & Mechanical, Graphics, Models & Replicas, AV Hardware, AVS, Setworks, Mockups.
2. **Who designs vs who procures?** — NRS (Nissen Richards Studio) designs are already in Architecture register. Don't duplicate.
3. **Three register types**:
   - **Design register** — drawings, specs, schedules (NRS scope → Architecture)
   - **Procurement register** — vendor catalogs, TDS, samples, compliance (e.g., FFE loose furniture)
   - **QA/Handover register** — ITP, AFC, Commissioning, O&M, Training, Spares (consolidated across packages)

See `references/aseer-register-scope-validation.md` for Aseer Museum register-to-scope mapping.

### Subcontractor Data Validation (June 2026)

Before populating any register, **always check the actual subcontractor folder** at `24_Subcontractors/NN_xxx_Contractor/` for:

1. **Existing submittal register** — `*_Submittal_Register/*.xlsx` in the subcontractor's folder is the source of truth. Compare item counts and descriptions; if the 04_Registers version is empty or differs, use the subcontractor's version.
2. **Schedule and BOQ** — `01_Schedule_and_BOQ/` may contain actual schedules. Use these item lists, not SOW-derived guesses.
3. **Returned Submittals** — `05_Returned_Submittals/` shows what's already been submitted and returned with comments. If shop drawings were already submitted (e.g., Showcase Sub-01 to Sub-11 from Apr-Jun), the register dates should reflect that.
4. **Scope of Work** — `00_Scope_of_Work_from_04/` has the actual scope document.

**Validation checklist:** Check if subcontractor has a register already, if BOQ has a sheet for this discipline, if actual submissions have been made, and if scope is covered by NRS (Architecture register) — if so, don't duplicate.

### MOC Drawing Numbering System

When the user provides a *Drawing Numbering System* document, apply the format to registers that track actual drawing sets:

```
MOC-ASE-{Disc}-{SubDisc}-{Floor}-{Stage}-{Cat}-{Rev}
```

**Apply to:** Architecture (drawings by floor+categories), MEP (their actual LOD uses MOC refs)
**Do NOT apply to:** FLS, AV, Lighting, etc. (system-based deliverables, not per-floor drawings)
**Category numbers:** 1000-1999 plans, 2000-2999 details, 4000-4999 sections, 5000-5999 elevations, 6000-6999 schedules
**Floor code:** GEN for non-floor items. Stage: DDD for 50%, IFC for IFC.

### Dependency-Based Date Logic (Internal Item Tiers)

Items within a single register have **internal dependencies**. Define tiers:

| Tier | Logic | Example | Date |
|------|-------|---------|------|
| **Immediate** | No dependency — design basis, methodology | Design criteria, load estimates, SLD | Day 0 |
| **After Survey** | Needs site survey | Slab assessment, MEP layouts | After cloud survey |
| **After Arch GA** | Needs Arch plans | AV system design, lighting layouts | After Arch 50% |
| **After Assessment** | Needs structural assessment + Arch GA | MEP per-floor layouts, rigging | After slab assessment |
| **After Arch 90%** | Needs Arch finalized | Landscaping | After Arch 90% |
| **Coordination** | Needs multiple disciplines | MEP coordination, lighting/AV | After all at ~90% |
| **IFC only** | Close-out only | ITP, AFC, O&M, Training, Spares | IFC milestone |

**Implementation:** Use parallel date variables (D1, D2, D3) and a `mk()` helper function.

### 7-Day Review Buffer

Between every dependent stage, add **7 days for client review**:

| Dependency | Buffer | Example |
|-----------|--------|---------|
| Arch BF → LGF | +7d | 29 Jun → 06 Jul |
| Arch 50% → 90% | +37d (30d prod + 7d review) | 29 Jun → 06 Aug |
| Survey → Assessment | +14d | 13 Jul → 27 Jul |

Implementation: `REVIEW = 7` constant, compute with `add_days(d, 30+REVIEW)`.

### Parallel Submission Tracks

Multiple packages can submit same day if no dependency. Organize into groups:

| Group | Name | Depends On | Example |
|-------|------|-----------|---------|
| 0 | Foundation | Nothing | Arch BF, Acoustic, CITC, Oddy, FFE, FLS Strategy, Structural Surveys, Showcase |
| 1 | Structural-feed | Structural surveys | MEP layouts, structural assessment |
| 2 | Arch-feed | Arch 50%+ | AV system design, lighting, FLS active/passive, interactives |
| 3 | Late | Arch 90% | Landscaping |
| 4 | Client-dep | Client RFI | Graphics, Model Maker |
| 5 | IFC | All disciplines done | QA/Commissioning |

### Register Merger / Consolidation

When two subcontractors have overlapping scope, merge registers into the dominant one.

**Merger workflow:**
1. Identify dominant register
2. Add new category section with updated ref numbers
3. Add dependency notes in Remarks
4. Delete absorbed register folder + xlsx + script
5. Regenerate dominant register

**Known mergers:** Rigging → Structural. Exhibition Fit-Out → deleted (redundant with Architecture/NRS).

### Icon/Emoji-Free Policy (Enforced)

**Every generated file MUST have zero icons, emoji, or Unicode dingbats.** Replace:
- `⏳` → "BLOCKED" or "PENDING"
- `✅` → "[OK]" or text
- `🔴🟡🟢` → text status labels
- `▲` in headers → remove (e.g., "▲ 50% Design" → "50% Design")
- `─═` box-drawing → ASCII hyphens/equals
- `█` block → "##"

Run comprehensive detection before delivery (scan all .py files for Unicode ranges 0x2500-0x27BF, 0x1F000-0x1FFFF, etc.).

### Design Change Register (DCR) — New Register Type

DCR tracks deviations between approved Stage 3 baseline and Stage 4 detailed design. See `design-change-control` skill for the full process.

**When to create a DCR (not a submittal register):**
- A Stage 4/DD submission differs from approved Stage 3 design
- CG reviews Stage 4 and asks "why change?"
- User asks "do we need to update the Stage 3 audit?"
- Multiple design changes need tracking through CG approval

**DCR structure:** 5 sheets: Design Change Register (9+ columns), Audit Closure Tracker, Legend, Reference Photos, Embedded Images.

**Key difference from submittal register:** DCR tracks changes FROM an approved baseline, not planned submissions TO a stage.

**The `design-change-control` skill has the full workflow, the Backup Report template, and a worked example from Aseer Museum Showcase (Jun 2026).**

### Register-Specific Rules Reference

| Register | Date Start | Special Rules |
|----------|-----------|---------------|
| Architecture | 29 Jun (BF) | +7d stagger per floor. MOC refs. Viz in 2 batches (BF+LGF, GF+1F). |
| Structural | 29 Jun (surveys) | Surveys immediate, assessment 27 Jul, design 28 Aug |
| MEP | 01 Jul (1st sub) | MOC refs. Tiers: design basis 01 Jul, layouts 27 Jul, details 28 Aug |
| FLS | 29 Jun (strategy) | Staggered per sub-package +7d |
| AV | 01 Jul (1st sub) | Philosophy 01 Jul, system design 29 Jul |
| Lighting | 10 Jul | Conservation BLOCKED on client object list |
| Interactives | 15 Jul | 6 objects, +7d stagger |
| Showcase | 29 Jun | Shop drawings ALREADY SUBMITTED |
| Landscaping | 29 Jul | After Arch 90% |
| FFE | 29 Jun | Procurement only (catalog/TDS/samples). No design (NRS covers). |
| Graphics | TBC | NO DATES — client RFI pending |
| Model Maker | TBC | NO DATES — client RFI pending |
| QA/Commissioning | IFC 28 Aug | Consolidated across all packages |

### BIM Deliverables (per BEP)

Per BEP section 3.3.C, BIM is split into **two models per discipline**:

| Model | LOD | Duration |
|-------|-----|----------|
| **Existing Conditions** | 300 | 15 Jul → 14 Aug |
| **Scope/Design Model** | 300→350→500 | 15 Jul → IFC |

**Disciplines with both:** Architecture, Structural, MEP
**Design model only:** FLS, AV (no existing survey needed)
**Clash Detection:** Weekly, starting before 100% stage, parallel with 90% stage

### Architecture Floor Submission Pattern

Architecture submits per floor, staggered +7d for client review buffer. Viz (3D renders) in 2 batches.

| Floor | 50% Date | Drawings | Viz |
|-------|---------|----------|-----|
| BF | 29 Jun | 16 drawings | Batch 1 (BF+LGF) |
| LGF | 06 Jul | 16 drawings | Already done with BF |
| GF | 13 Jul | 16 drawings | Batch 2 (GF+1F) |
| 1F | 20 Jul | 16 drawings | Already done with GF |

### Pitfalls

### MergedCell write error

When openpyxl raises `AttributeError: 'MergedCell' object attribute 'value' is read-only`, it means you're trying to write to a cell inside a merged range that isn't the anchor cell (top-left). 

**Fix in two steps:**
1. Unmerge ALL cells in the sheet before making structural changes
2. After writing all data, optionally re-merge section headers

```python
# Step 1: Unmerge before any writes
for mc in list(ws.merged_cells.ranges):
    ws.unmerge_cells(str(mc))

# Step 2: Do all data writes (insert_rows, value assignments, etc.)

# Step 3: Optionally re-merge section headers (if the format requires it)
# ws.merge_cells('A2:I2')
```

**When insert_rows fails on merged-cell workbooks:**
`ws.insert_rows()` on a workbook with merged cells can corrupt adjacent cell data — descriptions go blank, dates become None, sub-package values disappear. The corrupted cells are NOT predictable (depends on merged range boundaries).

**Alternative: Rebuild the sheet from scratch in memory:**
```python
# 1. Read ALL data including merged cells
all_data = []
for r in range(1, ws.max_row + 1):
    row_vals = [ws.cell(row=r, column=c).value for c in range(1, 10)]
    all_data.append(row_vals)

# 2. Unmerge
for mc in list(ws.merged_cells.ranges):
    ws.unmerge_cells(str(mc))

# 3. Build new ordered list in Python (renumber, insert, reorder)
new_data = manipulate_in_memory(all_data)

# 4. Clear all rows and write cleanly
for r in range(ws.max_row, 0, -1):
    ws.delete_rows(r, 1)

for ri, vals in enumerate(new_data):
    r = ri + 1
    for ci in range(9):
        cell = ws.cell(row=r, column=ci + 1, value=vals[ci] if ci < len(vals) else None)
        # Reapply styles if needed
```

This avoids insert_rows corruption entirely. The trade-off is losing original merged cell formatting — re-apply section-header merges afterward if required.

### Floor-zone reorganization (copying Arch pattern)

When reorganizing a register from **discipline-based sections** (A - HVAC GENERAL, C - FIRE FIGHTING) to **floor-zone sections** (A — Basement Floor, C — Ground Floor), match the Architecture register pattern:

```
A — Basement Floor              ← all disciplines per floor
B — Lower Ground Floor
C — Ground Floor
D — First Floor
E — Second Floor
F — Upper-Roof Floor
G — General                     ← non-floor items (DBR, CALC, GEN, BIM, Materials)
```

Within each floor section, items sort by discipline (HVAC → FF → WS → DRN) and then by ref number. Section headers use em-dash (`—`), green font (#375623) on light green fill (#E2EFDA).

```python
def get_floor(ref):
    ref_s = str(ref)
    if '-BF-' in ref_s: return 'BF'
    if '-LGF-' in ref_s: return 'LGF'
    if '-GF-' in ref_s: return 'GF'
    if '-1F-' in ref_s: return '1F'
    if '-2F-' in ref_s: return '2F'
    if '-RF-' in ref_s: return 'RF'
    return 'GEN'

FLOOR_LABELS = {
    'BF': 'A — Basement Floor',
    'LGF': 'B — Lower Ground Floor',
    'GF': 'C — Ground Floor',
    '1F': 'D — First Floor',
    '2F': 'E — Second Floor',
    'RF': 'F — Upper-Roof Floor',
    'GEN': 'G — General',
}
```

### NEVER rebuild an Excel file from scratch

When updating registers, **NEVER** create a new workbook and copy cell values. This destroys:
- Embedded images and logos (Cover sheets)
- Merged cells and frozen panes
- Custom column widths, fonts, and color schemes
- Conditional formatting and data validation
- Named ranges and formula references

**Always copy data VALUES into the existing formatted template:**

```python
# CORRECT: Open the formatted backup/template, paste values only
wb_src = openpyxl.load_workbook(current_file)  # has correct data
wb_tmpl = openpyxl.load_workbook(backup_file)  # has formatting + logos

ws_src = wb_src['Sheet1']
ws_tmpl = wb_tmpl['Sheet1']

for row in range(1, ws_src.max_row + 1):
    for col in range(1, ws_src.max_column + 1):
        ws_tmpl.cell(row=row, column=col).value = ws_src.cell(row=row, column=col).value

wb_tmpl.save(current_file)
```

If rebuilding was necessary for structural changes (e.g., insert_rows corruption from merged cells), use the **in-memory rebuild** pattern above, then apply formatting from a backup template.

### Update Dashboard/Summary sheets after any data change

After modifying the data sheet of a KPR or register:
1. Update the Cover sheet revision number and date
2. Update Summary formulas if new status categories were introduced
3. Verify formula ranges match the new data row count

### Always verify names against email evidence before populating

Never populate a person's name from a CV filename, KPR original data, or unverified source. Cross-reference against Outlook emails to confirm:
- The person was formally appointed (not just proposed)
- The appointment was approved by CG/MoC
- The CV submission status (pending / Code B / Code C)

If no email evidence exists, mark as "TBC" with a note about the source of the name reference.

### Avoid write_file PYEOF trap

When creating Python scripts via `write_file` for openpyxl operations, ensure the file does NOT contain a trailing `PYEOF` line. `PYEOF` is only valid in heredoc `<< 'PYEOF'` blocks in terminal commands. In a standalone `.py` file written via `write_file`, `PYEOF` at the end causes a `NameError: name 'PYEOF' is not defined`.

**Fix:** Always review the written file before running with `terminal()`. Use `read_file(path, offset=-5)` to check the last 5 lines.

### Subagent File Safety: Never allow subagents to write to source files directly

When delegating file editing to subagents (via `delegate_task`), subagents may accidentally **overwrite the source file** with test content, audit reports, or corrupted data. To prevent this:

1. **Copy the file to a temp location** and instruct the subagent to work on the copy only
2. Tell the subagent explicitly: "DO NOT write to the original file at [path] — work on the copy at /tmp/xxx"
3. After the subagent completes, apply only the VALUES to the original formatted file (see "NEVER rebuild an Excel file from scratch" above)
4. For HTML files: save a .bak copy before delegating any work

```python
# Safe delegation pattern for file editing
shutil.copy2(source_path, '/tmp/work_copy.html')
subagent_result = delegate_task(...)  # subagent works on /tmp/work_copy.html
# Then merge changes manually into source_path
If a file is open in Excel, openpyxl writes may silently fail or corrupt the file. Always check:
- Ask the user to close the file first
- Or use a temp copy, modify, then replace after confirming the source is closed
- After writing, verify by re-reading with openpyxl before reporting success

### Delete rows in reverse order when using openpyxl.delete_rows()
When deleting multiple rows, always process from highest to lowest row number. After each delete_rows(), all rows below shift up — so sequential deletions from top to bottom will delete wrong rows.

```python
# WRONG - deletes wrong rows after index shifts
ws.delete_rows(25)
ws.delete_rows(25)  # now deletes what was R26

# RIGHT - reverse order
ws.delete_rows(27)
ws.delete_rows(26)
ws.delete_rows(25)
```

### openpyxl not available in execute_code sandbox
`execute_code` sandbox does NOT have `openpyxl` — it will raise `ModuleNotFoundError`. Use `terminal(python3 -c "...")` instead, pointing to the system Python 3.13 which has openpyxl installed.

### openpyxl sheet discovery
Many register files have multiple sheets (e.g., `['Cover', 'Drawing']`). The data lives in the **second sheet**, not the first (`Cover`). Always call `wb.sheetnames` first, then pick the right sheet.

### Duplicate IDs on re-run
When re-running register updates, the same entries get appended again with duplicate IDs (e.g., `DWG-005` appearing twice). **Always de-duplicate before appending** — check existing IDs in the sheet and skip entries already present.

### Reading XLSB (Binary Excel) Files

`.xlsb` files are NOT readable by openpyxl. Use **pyxlsb** instead — installed on system Python via `pip3 install pyxlsb`. Only for reading; pyxlsb has no write support.

```python
from pyxlsb import open_workbook

with open_workbook(path) as wb:
    print(wb.sheets)  # list available sheets
    with wb.get_sheet('RFI') as sheet:
        for row in sheet.rows():
            vals = [item.v for item in row]
```

**Key patterns when reading project registers:**
- **Multi-sheet workbooks** — always inspect `wb.sheets` first. Registers typically have a Cover/Dashboard sheet plus a data sheet (named `RFI`, `Drawing`, `Material Submittal`, etc.).
- **Header offset** — data may not start at row 0. Check for status-code legend rows, title blocks, or summary tables at the top. The RFI register has headers at row 11 (0-indexed), with status code definitions in rows 2-7.
- **Excel serial dates** — dates come as integers (serial number). Convert with:
  ```python
  from datetime import datetime, timedelta
  serial_date = 46163  # e.g. from cell value
  epoch = datetime(1899, 12, 30)
  actual_date = epoch + timedelta(days=serial_date)
  ```
  Always wrap in try/except — non-date cells (text, None) will raise.
- **None values** — empty cells read as `None`. Check before formatting.
- **Row skipping** — merged cells or section headers in the source produce rows where most columns are `None`. Detect by checking column count or specific key column.

### Presenting Register Data to User

After extracting, display as compact tables — the user prefers drill-down filtering (list all → filter category → filter status). **Always end with an action table.** The user's "what action needed" means: synthesize findings into concrete next steps with owner assignment, not just a data dump. Every reconciliation or status check must conclude with who-owns-what action items.

```python
print(f"  PR-{n:03d} | {status:20s} | {updated if updated else '-':12s} | {desc:40s}")
```

### Register mtime check (efficiency)

Before deep-scanning Outlook for register updates, check `os.path.getmtime()` on the Excel file. If modified within 3-5 days, skip scanning and report current. Register files are often already current — don't waste time on SQLite + attachment extraction when nothing has changed since last modification.

### Patching the Right Register Version

The `09_Registers/` copy and subcontractor `06_RFIs/` copy of the same register may have **different column structures**. Always check which version the user is referring to before updating. The `09_Registers/` master is usually the one Mohamed tracks for cross-subcon view; the per-subcon copy is for that subcontractor only.
def fmt_date(serial):
    try:
        return (datetime(1899, 12, 30) + timedelta(days=serial)).strftime('%Y-%m-%d')
    except: return '-'

def fmt_val(v):
    return str(v) if v is not None else '-'

# Build rows list, then format
for r in rows:
    print(f"{r['ref']:25s} | {r['status']:10s} | {r['subject']:35s} | {r['days_open']:>4d}d")
```

### OneDrive sync-lock on .xlsb files
OneDrive's sync engine holds exclusive file locks on `.xlsb` files — direct `dd`/`cp` reads fail with `Resource deadlock avoided`. The file cannot be copied or read directly while open in OneDrive.
- **Workaround**: Ask the user to open the `.xlsb` in Excel and Save As `.xlsx` to Desktop (or a local path), then operate on the copy
- **Alternative**: Ask the user to Share the file via Telegram directly, which bypasses OneDrive's lock
- **Alternative for read-only**: `pyxlsb` can read `.xlsb` files even under OneDrive lock (tested with `open_workbook()`). Use this for data extraction without modifying the original.

### OneDrive cloud stubs cause "File is not a zip file" on .xlsx registers

OneDrive "Files On-Demand" placeholders (~6.5 KB, `com.apple.FinderInfo` xattr present but `com.apple.provenance` MISSING) are NOT real xlsx files. `openpyxl.load_workbook()` fails with "File is not a zip file" because the local file is just a cloud stub — the actual content was never downloaded.

**Detection** — check if the file is a valid ZIP before opening with openpyxl:
```python
import zipfile
def is_valid_register(path):
    if not os.path.exists(path):
        return False
    try:
        with zipfile.ZipFile(path) as z:
            return len(z.filelist) > 0
    except Exception:
        return False
```

**Symptoms:**
- All register files in a project's `Docs/09_Registers/` are exactly ~6-7 KB
- `xattr` shows `com.apple.FinderInfo` only (no `com.apple.provenance`)
- `file` command reports "Microsoft Excel 2007+" but the file isn't a real ZIP
- Attempting `dd`/`cp`/`cat` on the file gives "Resource deadlock avoided"

**Fix:** Open the register files manually in Excel (triggers OneDrive to download the real content), or mark the `Docs/09_Registers/` folder as "Always keep on this device" in OneDrive settings.

**Script fix:** Add `is_valid_register()` check before every `openpyxl.load_workbook()` call. This is what `bim_watchdog.py` now does — it skips with a WARNING when a stub is detected, so the rest of the scan can continue.

### Labor CLI timeouts
Claude Code and Kimi CLI both timeout on complex file scanning tasks when max-turns is insufficient. For **file enumeration** (listing, counting, scanning), use direct `os.walk` Python instead of delegating to a labor agent. Reserve labor agents for **content analysis and decision-making** only.
