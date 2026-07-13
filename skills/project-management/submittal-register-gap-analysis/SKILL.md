---
name: submittal-register-gap-analysis
description: Systematic process for auditing project submittal registers against consultant comments to identify missing deliverables and required updates.
---

# Submittal Register Gap Analysis

## Trigger
Use this skill when a user provides a submittal register (Excel/Plan) and requests a "study", "gap analysis", or "fix" to identify missing items. Two common patterns:

1. **Consultant Comment Review**: User provides a consultant's comment document (PDF/Text) + existing register.
2. **Subcontractor Register Review**: User provides a subcontractor's submitted register and asks to check completeness against contractual scope.

## Workflow

### Phase 1: Understand the Source Documents
1. **Read the register** — understand structure, columns, numbering scheme, dates, statuses.
2. **Identify the reference scope** — what are we comparing against?
   - For **consultant comments**: extract all requirements from the comment document.
   - For **subcontractor registers**: identify the contractual scope docs (SOW, SCOPE_REQUEST.md, DMP, ER, Div specs, concept design packages).

### Phase 2: Cross-Reference Against Scope
Cross-reference each register item (or missing item) against the **contractual scope documents** (ER, SOW, pre-contract design reports, DMP, SCOPE_REQUEST.md). This identifies:

- **Scope Gap**: The source demands X, but the ER/SOW/design report explicitly excludes X from contractor scope. The register is correct — the gap is in the contractual scope, not the register.
- **Contractor Omission**: The source demands X, and the ER/SOW requires it, but the register doesn't list it. This is a genuine gap.
- **Stage Mismatch**: The source demands X, but X belongs to a later stage (e.g., CG asks for IFC-level detail during DD submission).
- **Pre-Contract Exclusion Confirmed**: The pre-contract design report explicitly states "X to be done by D&B contractor" — the source is now demanding X, confirming it IS in scope. The register needs to add it.

### Phase 3: Gap Identification
Classify each item as:

- **Present**: Item exists and meets the requirement.
- **Partial**: Item exists but lacks specific detail (e.g., "missing per-floor breakdown").
- **Missing — In Scope**: No corresponding item exists, but the scope docs require it. Must be added.
- **Missing — Out of Scope**: No corresponding item exists, and the scope docs don't require it. Flag for commercial/contractual resolution.
- **Explicitly Excluded**: The pre-contract design report explicitly excluded this item. The source demanding it is a scope addition, not a register gap.

### Phase 4: Produce the Corrected Register
When the user says "fix" or "can you fix", the deliverable is a **working corrected Excel file**, not just a gap table.

1. **Preserve original formatting** — keep the subcontractor's column structure, colors, merged cells, fonts. Build on their file.
2. **Add missing items** — insert rows for every "Missing — In Scope" item with proper codes, descriptions, and realistic dates.
3. **Fix structural issues**:
   - Add proper drawing/package codes (e.g., ASE-AV-xxx) where missing.
   - Stagger per-floor IFC packages instead of lumping all on one date.
   - Add BIM submittals (LOD300/350/500) if missing.
   - Add post-install deliverables (FAT, SAT, cable tests, cybersecurity, O&M, training, spares).
   - Add coordination submittals (Interface Register, setwork housings, showcase AV interface, DALI/BMS).
4. **Fix dates** — move past-due items to realistic forward dates. Account for CG review durations (typically 7-14 days).
5. **Add status tracking** — mark items as Planned / In Progress / Submitted / Overdue.
6. **Save to the project location** — copy to the OneDrive BIM path under the appropriate submittal register folder.

## Output Format

### For analysis-only requests:
| Source Ref | Requirement | Current Status | Action Required | Priority |
| :--- | :--- | :--- | :--- | :--- |
| [Ref] | [Concise description] | Present / Partial / Missing | [Specific change] | High/Med/Low |

### For fix requests:
The corrected Excel file saved to the project path, plus a summary table showing:
- What was added (count + list)
- What was fixed (dates, codes, structure)
- What was preserved from the original

## Stage-Aware Analysis

**CRITICAL:** Match submittal requirements to the **project stage**, not a generic checklist.

| Stage | What's Expected | What's NOT Expected |
|-------|----------------|---------------------|
| Stage 2-3 (Concept/Developed) | Design philosophy, UX strategy, system architecture narrative | Technical drawings, detailed schedules |
| Stage 4 (Technical Design) | Drawings, schedules, calculations, diagrams, rack elevations | Design Basis Report, concept philosophy docs |
| Stage 5 (IFC/Construction) | Per-floor IFC packages, specs, ITP, commissioning plans | Detailed design studies |

**Common mistake:** Recommending a Design Basis Report for Stage 4. CG reviews technical content at this stage — drawings, schedules, and calculations are the deliverable, not design narrative. The concept designer (e.g., DHD Services) already produced the philosophy at Stage 2-3.

## Drawing Code Floor Prefix — Do NOT Assume

**Pitfall:** Drawing codes like `MOC-ASE-AV-TAV-BF-DDD-1230-00` may use `BF` as a **project prefix** (e.g., "Building Fit-out" or project code), NOT "Basement Floor". The actual floor is in the title block text.

**Always verify by reading the title block** — extract text from the PDF/DWG title block area to find the actual floor name. In the Aseer Museum AV case, all 8 drawings had `-BF-` in the code but actually covered 4 different floors (Basement, Lower Ground, Ground, First). The `BF` was a project code, not a floor indicator.

## CG-Facing Register — No Internal Responsibility Split

When submitting a register to CG, do NOT show internal responsibility splits (subcontractor vs main contractor). CG sees everything as "Samaya". Use only 3 status values: `Submitted` (green), `Pending` (yellow), `Future Gate` (grey). Set all Responsibility column values to `'Samaya'`.

## Responsibility Split Pattern

When a subcontractor's scope doesn't cover all submittals (e.g., AV Designer doesn't do BIM or coordination drawings), split the register by party:

1. **AV Designer scope** — their contractual deliverables (drawings, schedules, calculations, diagrams, rack elevations, control requirements, testing, handover)
2. **Samaya scope** — items Samaya handles (BIM models, structural calcs, IT/ELV, acoustic, coordination, Interface Register, cybersecurity)

Use color coding (green tint = AV Designer, blue tint = Samaya) and section headers to make the split visually clear. This lets you send the AV Designer only their section while keeping the full picture internally.

## CG Comment Response Workflow — Submission Plan Review

When CG issues comments on a submission plan (e.g., "add scenography drawings", "add furniture layouts"), follow this sequence:

### Response Voice Rules

- **Samaya is the contractor.** All responses are from Samaya's perspective. Do NOT say "NRS scope" or "AV Designer scope" — CG sees everything as Samaya.
- **No internal sub-consultant splits.** If a designer (NRS, ZNA, etc.) provides input, report it as information received, not as a scope boundary.
- **Items to be included later** → "will be coordinated and included in subsequent stages from 50% to 90% to IFC. [Specialist] to be appointed."
- **Items already covered by Stage 3** → "was defined and approved at Stage 3. To be confirmed with CG whether existing submission is sufficient."
- **Items by other discipline** → "will be provided as part of the overall submission under the relevant scope, coordinated with the [specialist]."

### Full CR Sheet + Response Package Workflow

See `references/cr-sheet-response-package.md` for the complete workflow: building the CR Sheet, updating submission plans, splitting specialized scope registers, packaging the response folder, and filing to OneDrive.

### Step 1: Check the Designer's SOW/Contract FIRST

**Do NOT ask the designer "is this in your scope?"** — the user will correct you. Check the signed SOW, responsibility matrix, and contract documents before writing to the designer.

**Where to check (Aseer Museum NRS example):**
- `01_Contracts/02_NRS_Contract/01_Signed_Agreements/Nissen SOW_OPTION_01_updated.xlsx` — responsibility matrix
- `01_Contracts/02_NRS_Contract/01_Signed_Agreements/Nissen SOW responsibilty matrix.pdf` — detailed scope breakdown

**NRS SOW Responsibility Matrix (reference):**

| Item | NRS Role |
|------|----------|
| Scenography | Design & SD ✓ |
| FF&E (Furniture & Furnishings) | Design & SD ✓ |
| Display Cases & open displays | Design & SD ✓ |
| Setworks & Fit-Out | Design & SD ✓ |
| Life & Safety / Civil Defense | Samaya Design & SD — NRS coordinates on base plans |
| Universal Access / Accessibility | Not listed — potential gap |
| Signage & Graphics | NRS scope (locations on GA plans) |
| Maintenance Access | Defined by Stage 3 — NRS can copy annotations |

### Step 2: Prepare the Modified Submission Plan Yourself

Do NOT ask the designer to prepare the revised plan. The user (Samaya) updates the submission plan with new items added, then sends to the designer for date suggestions only.

**New items to add (from CG comments):**
- Scenography Drawing
- Furniture Layout (FF&E)
- Signage & Graphics Plan
- Universal Access Drawings
- Maintenance Access Plan

Set responsibility to `NRS` and dates to `'as Nrs Date'` or similar placeholder.

### Step 3: Send Concise Email to Designer

Format: point-by-point, no scope questions, just request dates.

```
Subject: [Project] — CG Comments on Submission Plan / Revised Plan for Review

Dear [Designer],

CG has reviewed the [Discipline] Submission Plan and issued the following comments:

1. [Comment 1]
2. [Comment 2]
...

We have updated the submission plan and added the following new items:
- [Item 1]
- [Item 2]
...

Please review the attached revised submission plan and suggest the proposed dates for these new items so we can finalise and submit to CG.

Regards,
[Name]
```

### Step 4: Forward Designer's Response to CG

When the designer responds with their position (e.g., "scenography already in Stage 4 pack", "furniture by others"), forward their email to CG with a summary. Do NOT try to resolve scope disputes yourself — let CG and the designer negotiate.

### Common NRS Positions on CG Comments (from actual response)

| CG Comment | NRS Position |
|------------|--------------|
| Scenography drawings | Already in Stage 4 pack — not a Stage 4 requirement per RIBA |
| Furniture layouts | NRS only does bespoke setwork furniture. Other FF&E by Samaya |
| Universal Access Drawings | Defined by Stage 3 — no changes proposed |
| Access & Evacuation Plans | Life safety is outside NRS scope — prepared by others |
| Signage & Graphics | Locations on GA plans. Graphics content outside NRS scope |
| Maintenance Access Plan | Defined by Stage 3 — can copy annotations from Stage 3 doc |

## Pitfalls
- **Vague Mapping**: Avoid saying "it's there." Specify which drawing number or item # corresponds to the requirement.
- **Missing Context**: For "Partial" status, explicitly state what is missing from the existing deliverable.
- **Formatting**: Use formal construction project management English. No emojis or conversational filler.
- **Don't just analyze — fix**: When the user says "fix", produce the corrected file. A gap table alone is not the deliverable.
- **Don't overwrite blindly**: Preserve the subcontractor's original formatting and structure. Build on their work, don't replace it.
- **Check for already-submitted items**: The register may start from scratch and omit items already submitted (e.g., IFC-0008). Add them with "Submitted" status.
- **BIM is often forgotten**: Subcontractors frequently omit BIM submittals (LOD300/350/500). Add them explicitly.
- **Per-floor IFC**: Subcontractors often lump all floors into one IFC package. Split into per-floor packages with staggered dates.
- **Post-install deliverables**: FAT, SAT, cable test certs, network config, cybersecurity — these are often missing from subcontractor registers.

## Verification
- Cross-reference the final register against the original scope docs to ensure 100% coverage.
- Verify all items have proper codes, realistic dates, and assigned responsibility.
- Confirm the file opens correctly and preserves the original's formatting.

## Bank-vs-mirror execution mechanics

The framework above describes what to do. This section describes **how** — the step-by-step mechanics for actually extracting text from PDFs, dating the documents, and writing back to the repo. The agent who gets asked "go read Adel Darwish's bank and tell me if there's new info" should follow this without re-deriving the approach.

### Hard rule — no binaries in the repo

> **The repo is a coordination hub, not an archive. Never copy PDF/Excel/Word files from any external bank into the repo. Extract text + metadata into markdown registers and reference the OneDrive path.**

The user repeated this preference verbatim in 2026-07-13 ("don't upload binary files you have to read files and understand and update info to the repo one by one"). Treat it as a session-level hard rule. If the repo AGENTS.md already states this (it does in `aseer-museum-pm/AGENTS.md`), the skill reinforces it; if not, restate it in the register frontmatter under `source:`.

### Read path — temp scratch on /Volumes/MIcro

For any session involving reading dozens of large bank PDFs:

1. Create a scratch directory: `mkdir -p /Volumes/MIcro/.aseer-tmp/text_extracts/<topic>/`
2. Use **Python `os.listdir` / `subprocess.run(['pdftotext', ...])`** — NOT bash `for` loops. OneDrive paths on this Mac contain spaces, parentheses, em-dashes, and apostrophes that break bash quoting even when the literal looks clean. The bash quibble tool will silently produce empty output or "ambiguous redirect" errors.
3. **Copy first, never `mv`**. OneDrive won't let you move files (Operation not permitted); use `cp`, but accept that the binary stays in OneDrive.
4. **Extract per known primary doc**, not per-folder. For each SI/MS/MA folder, identify the file whose name matches the doc ref (e.g., `MOC-MUS-CG-ASE-1KN-MA-008.pdf`); ignore Response/, Rev.01/, Closing/, etc. unless the primary is wrong.
5. **Read the extracted `.txt` with `read_file`** — never embed PDFs in the conversation.
6. **Delete the scratch directory after the session** if it contains large files (`rm -rf /Volumes/MIcro/.aseer-tmp/text_extracts/<topic>/`).

### Text extraction patterns to use

| Goal | Pattern |
|------|---------|
| Get ISO YYYY-MM-DD date | `re.findall(r'(20\d{2}-\d{2}-\d{2})', text[:6000])` |
| Get D/M/Y or M/D/Y | `re.findall(r'(\d{1,2}[-/]\d{1,2}[-/]20\d{2})', text[:6000])` |
| Get doc ref | `re.findall(r'MOC-MUS-CG-ASE-1KN-[A-Z0-9]+-\d+', text)` plus `re.findall(r'SI-CG-\d+', text)` |
| Get approval status | look for "Approved", "Approved as Noted", "Not Approved" keywords near "Acceptance of Action" |
| Topic signal | first 2-3 sentences after "Description of Site Instruction" or "Subject:" if layout is bilingual (English + Arabic noise) |

**Bilingual PDFs (Arabic embedded)**: keep both English and Arabic script in the extracted text. pdftotext will preserve Arabic glyphs but the layout garbles them. Match English phrases and ignore Arabic lines unless the doc has a clear English block after the Arabic header.

### Bank inventory script (reference implementation)

```python
import os, subprocess
out = '/Volumes/MIcro/.aseer-tmp/text_extracts/<topic>'
os.makedirs(out, exist_ok=True)

src = '<OneDrive bank root>'  # contains spaces — keep raw

# Build list of {folder_name → primary_docl} mapping
for folder_name in sorted(os.listdir(src)):
    folder = os.path.join(src, folder_name)
    if not os.path.isdir(folder): continue
    # filter out non-doc folders
    pdfs = [f for f in sorted(os.listdir(folder))
            if f.lower().endswith('.pdf')
            and not any(k in f.lower() for k in ['response','reply','rev.','closing'])]
    if not pdfs: continue
    primary = pdfs[0]
    primary_path = os.path.join(folder, primary)
    subprocess.run(['pdftotext', '-layout', primary_path, f'{out}/{folder_name}.txt'])
    print(f"  {folder_name} -> {primary} ({sum(1 for _ in open(f'{out}/{folder_name}.txt'))} lines)")
```

Same script structure handles MA/MS/SI/MoM/Letter banks.

### Date-typo hunting

Source PDFs frequently have wrong/random dates — do **not** trust the first regex hit blindly. Common typos on Aseer Museum docs:
- "18/5/2027" → should be 2026 (off-by-100 year)
- "22-Jun-2026" → 22-Feb-2026 (wrong month — was a copy/paste from another row)
- "02-Sep-2026" → 02-Mar-2026 (wrong month)
- "29/12/2026" → text-format D/M/Y, normalize to ISO when comparing

Always cross-verify against the register log date before quoting in commit messages or memos. If the PDF date disagrees with the register, log both values in the register enrichment row and flag the discrepancy — do not silently overwrite.

### Assessment file format (corrected)

The 2026-07-13 assessment at `~/aseer-museum-pm/09_Agent_Workspace/adel_execution_bank_assessment.md` follows the canonical structure:

1. **YAML frontmatter** (last_updated, owner_agent, status, source path)
2. **Bank inventory table** — every sub-folder + root file, with count + mirror status
3. **What is genuinely new** (ranked by value)
4. **What's already mirrored** (so user verifies completeness)
5. **Summary actionable updates** — file path + 1-line change for each proposed commit

Future agents should clone this structure when writing their own bank-vs-mirror survey output.

### Verification
- Re-confirm mirror after each register enrichment by reading the register frontmatter `last_updated` date — should be 2026-07-13 or later after a bank audit session.
- Re-list the bank's top-level layout to ensure no new folders were added during the audit.
- Confirm no PDFs from the bank were committed to the repo: `git log --stat | grep '.pdf$' | wc -l` should return 0 for any bank audit commit.

### Pitfalls specific to the execution mechanics
- **Bash path escaping breaks silently.** When bash escapes fail, you'll see "ambiguous redirect" or empty files. Switch to Python `os.listdir` + `subprocess.run` immediately. Don't spend iterations debugging shell quoting.
- **`mv` fails on OneDrive with "Operation not permitted."** Always use `cp`. The original stays in OneDrive — that's fine, redundancy is by design.
- **`pdftotext` with `-layout` is the right flag.** Without it, column alignment is destroyed and finding dates/regex patterns becomes harder.
- **Date-only filter (`grep -c '2026'`) is unreliable.** PDFs without dates default to ISO build dates or footer page numbers which look like dates. Always use combination patterns.
- **OneDrive files have hidden macOS `.DS_Store` and `._filename` duplicates** at folder roots. Filter these out before listing.
- **Reserve judgement on Date discrepancies until you have the register row + register frontmatter both open** — both can be stale; only the Aconex CDE is authoritative, and Aconex dates may also be stale if the doc was re-submitted but the CDE wasn't updated.

### Cross-skill linkage
- `materials-register-management` — for the MA enrichment pattern when bank has material submittal folders
- `aseer-document-control` — for bilingual PDF routing table and QiD/OneDrive doc code conventions
- `compliance-system` — if the bank audit surfaces approved-spec changes, feed them directly into compliance matrix updates

## Bank-vs-Mirror Survey (External Document Bank Audit)

Use when a user hands over a OneDrive document bank (someone's personal folder, a subcontractor's drop, an inherited archive) and asks "is there anything new I need to push to the repo?"

**Terminology:**
- **Bank** = the external folder tree being audited (e.g., "Adel Darwish's files - 01- Execution Documents")
- **Mirror** = the repo's existing register/log of the same documents

### Phase 1 — Bank inventory

1. List the bank's top-level layout: sub-folders + any loose root files. **Master schedules named after the project abbreviation often live at root, NOT inside a sub-folder** — don't miss them. Use `cp` to `/tmp/` before opening (NEVER `mv` on OneDrive files — corrupts sync).
2. For each sub-folder: count folders/files, capture chronology if dates are in names (e.g., `02- WEEKLY MEETING 02 (05-01-2026).pdf`).
3. Note "control" sub-folders: Letters (IN/OUT), SI (Site Instructions), NCR, IR, SNA, SOR, MIR. Missing mirrors here are usually a register gap, not dead files.

### Phase 2 — Build the bank × mirror matrix

For each bank item answer four questions:

| Question | Where to check |
|----------|----------------|
| Does the mirror have a register for this document type? | `01_Registers/` repo folder |
| Is the mirror back-filled to current count? | Compare last ref in mirror vs last folder number in bank |
| Are dates/statuses current in the mirror? | `last_updated` frontmatter vs bank file dates |
| Are there structural columns/data the mirror doesn't capture? | Bank doc columns vs mirror table columns |

Output as a table:

| # | Bank folder | Count | Mirror register | Last ref match? | Action |
|---|-------------|------:|-----------------|-----------------|--------|
| 05 | RFI/TQ | 19 | `rfi_register.md` | ✓ | none |
| 06 | Weekly Meeting MOM | 12 | `meeting_minutes.md` | ✗ (14 vs 02-13) | back-fill |
| 10 | CG SI | 20 | `si_register.md` (empty) | ✗ | populate |

### Phase 3 — Value-add signal mining

When scanning working files in the bank, look for:

1. **Target-date sanity check.** Schedules with delivery columns must be checked against the contractual handover date. **Dates past handover are mis-labeled** — either "for-installation" (Excel tracks installation, not contract) or the schedule drifted and needs a red flag. Don't silently pass 2027 dates in a contract ending 2026.

2. **Rejected/Not-Submitted concentrations.** Group counts of `Rejected` and `Not Submitted` in a single column usually reveal a **package with a known problem** (e.g., 13 of 14 rejected rows on one MA ref = a single CG rejection cascading through a package). Hunt the master register for the root cause before logging each rejected item individually.

3. **Submittal-ref gaps.** Working files often show items with NO submittal reference column filled. Count them. If >50% lack a submittal ref, **the pipeline isn't flowing yet** — this is a procurement warning, not a data quality issue.

4. **Status columns uniformly empty.** If the rightmost "actual status" column is None across the file, the Excel is **planning/structural only** — declare it as a working file, NOT the register of record. Reference the proper register in the repo.

5. **Naming-consistency drift.** Code prefixes diverge across the project lifecycle: bank uses older `MOC-Asser-SIC-1A0-…` while repo/Aconex uses current `MOC-MUS-ASE-1A0-…`. Both are valid historical refs; cross-check ref numbering against the official scheme.

### Phase 4 — Write the assessment

Deliver a single assessment file in `09_Agent_Workspace/` (NOT in the registers themselves — this is scratch output):

1. **Bank inventory table** (sub-folders + root files).
2. **What's NEW** — genuine gaps in the mirror, ranked by priority.
3. **What's already mirrored** — list explicitly so the user can verify build completeness.
4. **Actionable updates table** — file path + one-line change description.

**Format constraints:**
- Source traceability: every claim cites the bank path or the repo path (matches the project's `AGENTS.md` rule).
- Do NOT modify repo registers from the assessment file alone. Propose the change; let the user confirm scope.
- Use Code C / Code A conventions per `cg-response-protocol` skill when reviewing MA/MS items surfaced in a bank.

### Bank-vs-mirror pitfall — don't conflate working file with register

A common mistake: treating the bank's working Excel as the source of truth and overwriting the repo's register on first inspection. The bank's working file is usually **one person's planning view**; the repo's mirror is the consolidated team view. **Confirm with the user before any overwrite.**

## Bank Survey — Aseer Museum Reference

A worked example from 2026-07-13 lives at:
`~/aseer-museum-pm/09_Agent_Workspace/adel_execution_bank_assessment.md`

Common findings on Aseer Museum surveys:
- Working schedule delivery dates land in 2027 vs contract handover 30-Sep-2026 — flag as planning-vs-contract ambiguity.
- 85%+ of architectural items have no MA submittal ref — door & ceiling packages typically unsubmitted.
- Historical Weekly Meeting MOMs back-fill one PDF at a time from a steady MoM cadence (02 → 13 → 14).
- CG Site Instruction register is most often the missing mirror — populate before pursuing action items.

## Cross-Skill Linkage

- `consultant-comment-response` — for handling CG comments on items the bank survey surfaces.
- `cg-response-protocol` — for code status conventions (Code A/B/C/D/E/F/U) on MA/MS items found in a bank.
