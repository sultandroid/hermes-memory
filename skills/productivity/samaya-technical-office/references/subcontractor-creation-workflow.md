# Subcontractor Folder Creation Workflow

## When to use

A scope gap or new specialist package has been identified (e.g., RFI confirms existing consultant won't cover a scope element, or the T2 allocation table lists a trade not yet set up). You need to create a new numbered subcontractor folder under `Subcontractors/NN_Discipline_Contractor/` with SCOPE_REQUEST.md and supporting reference files.

## Pipeline

### Step 0: Determine the next number

List existing folders in `Subcontractors/` to find the highest `NN_` prefix. The next number is max + 1.

```bash
ls -d Subcontractors/[0-9][0-9]_*/
```

### Step 1: Create folder structure

Per the README.md convention:

```\nSubcontractors/NN_Discipline_Contractor/\n├── SCOPE_REQUEST.docx                ← formal deliverable (SamayaDoc template)\n├── 01_Schedule_and_BOQ/              ← BOQ items, schedules applicable to this package\n├── 02_Reference_Drawings/            ← drawings the sub needs\n├── 03_Specifications_and_Standards/  ← specs the sub must comply with\n├── 04_Reference_Imagery/             ← concept docs, renders, photos\n├── 05_Returned_Submittals/           ← sub → Samaya submissions\n├── 06_RFIs/                          ← sub → Samaya technical queries\n├── 07_Approvals/                     ← Samaya stamps + forwards to CG\n├── Email_Data_Extraction/            ← email records related to this sub\n└── _MANAGER_DASHBOARD/\n    ├── SCOPE_REQUEST.md              ← source markdown (management copy)\n    ├── SITUATION_REPORT.md           ← status tracking\n    ├── _Email_Draft_to_find_lab.md   ← draft email for PM to find vendor\n    └── *.md                          ← all other management notes\n```

### Step 2: Deep multi-source research (before writing SCOPE_REQUEST.md)

Search the entire project for all related documents. Interactive/tactile scopes require data from multiple schedule files simultaneously:

| Data source | What to extract | Search pattern |
|-------------|----------------|----------------|
| **Exhibit Schedule** (`*Exhibit Schedule.*`) | Exhibit ID, name, gallery, description, outcomes, linked component IDs | `ET_XX.XX` |
| **Setwork Schedule** (`*Setwork Schedule*`) | Physical dimensions, materials, setwork IDs linked to the exhibit | `ET_XX.XX_SW_XX` |
| **Tactile/Interactive Schedule** (`*Tactile*`) | Hands-on interactive IDs (HI_XX), type (hybrid/digital/tactile), description | `HI_XX` |
| **Model/Replica Schedule** (`*Model & Replica*`) | Replica objects (RE_XX) that integrate with the interactive | `RE_XX` |
| **Media Schedule** (`*Media Schedule*`) | AV content, digital media panels linked to the exhibit | `AV_XX`, `DI_XX` |
| **Drawing Register** (`drawing_system.md`) | NRS drawing number ranges for the discipline (e.g., 1860-1882 = Tactiles) | `A2742-XXXX` |
| **Acoustic Strategy** | RT60 targets, noise criteria for the gallery | Gallery code (e.g., G9) |
| **RFI Register** (`*RFI_Register*`) | Prior RFIs on the same topic — question summary, routing, status | Interactive keyword, gallery code |
| **Email intel** (`email_intel_30d.md`) | Correspondence threads already in progress | Gallery code, trade name |
| **File Register Index** (`File_Register_Index.csv`) | NRS drawing files (PDF, DWG, RVT, RFA) for the subject | Drawing number range |
| **Stakeholder/T2 table** (`Knowledge Notes - Stakeholder Mgmt Plan*`) | Who is contractually responsible for this scope | `T2-XX` |

**Pro tip for filenames with `&` or spaces:** Use `execute_code` with `shlex.quote()` from `hermes_tools` rather than bare terminal commands — `&` in filenames is interpreted as backgrounding by bash.

### Step 3: Author SCOPE_REQUEST.md (in _MANAGER_DASHBOARD/)

Write SCOPE_REQUEST.md directly in `_MANAGER_DASHBOARD/` — never at sub root. Follow the **Samaya standard 10-section template**:

```
# Scope of Work Request — [Discipline Title]

**Project:** Aseer Regional Museum — Abha, Aseer Region, KSA
**Main Contractor (Issuer):** Samaya Investment — Technical Office, BIM Unit
**Issued to:** [Target audience description]
**Issue date:** [current YYYY-MM-DD]
**Reply by:** [timeframe] from issue — [deliverables expected]
**Discipline:** [type] Sub-Contractor under Main Contract `0010003521`
**Key Personnel Register ID:** [KPR reference if applicable]
**Subcontractor Register ID:** [D-XX or Prequal Register ref]

> **Privity note.** Issued under Samaya–Sub-Contractor agreement only. No privity with MoC, PMC, CG, or NRS. All formal queries route through Samaya.

---

## 1. Purpose of this request

[Why this specialist is needed — what they must design/supply/install/commission. Authority basis paragraph.]

---

## 2. Programme

[Milestone table with target dates, not Day-N. Critical path callout if applicable.]

---

## 3. Scope of Work

[Headline scope — use sub-sections 3.1, 3.2 for material categories, test specs, etc.]

### 3.1 [Category name]

[Table or prose describing scope elements]

### 3.2 [Specification]

[Table of key parameters]

---

## 4. Deliverables

[Per-stage table: concept → engineering → FAT → install → T&C → handover]

---

## 5. Sub-Contractor Submission Requirements

[Numbered list: pre-qualification pack, priced proposal, technical proposal, etc.]

---

## 6. Reference Files (in this folder)

[Table mapping folder paths to content descriptions — EVERY reference must have a corresponding file in the subfolder]

---

## 7. Workflow & Communication

[Single point of contact, CDE, naming convention, RFI process]

---

## 8. Sign-offs Required

[Table: sign-off, owner, trigger]

---

## 9. Commercial Terms

[Payment terms, currency, confidentiality, IP, authority basis]

---

## 10. Action

[Confirm receipt timeframe, proposal deadline]

---

*Drafted by:* Samaya Technical Office — BIM Unit
*Issue Date:* [date]
*Linked Plans:* [DMP, KPR, etc.]
```

**Critical rules:**
- All `.md` files (SCOPE_REQUEST.md, SITUATION_REPORT.md, email drafts, research notes, contract status) go in `_MANAGER_DASHBOARD/` — never at sub root level
- The only file at sub root is `SCOPE_REQUEST.docx` (formal deliverable)
- The "Reference Files" section (§6) MUST only list files that actually exist in the subfolder. After writing the SOW, verify each referenced path has a real file — if not, either copy the file in or remove the reference.
- Programme dates should be calendar dates (not Day-N from LOA) unless the SOW is written during the early programme phase.
- The metadata block must include KPR and Subcontractor Register IDs where applicable.
- Use `|` tables extensively (not prose paragraphs)
- Keep the privity note at the top as a blockquote
- Reference specific exhibit IDs, drawing numbers, and document codes

**Exhibit context section pattern** (for interactive/tactile/fabrication scopes derived from NRS schedules):

When the interactive or exhibit is already defined in NRS schedules, include a dedicated section listing:
- All component IDs linked to the exhibit (setworks, replicas, graphics, AV, hands-on interactive IDs)
- Physical dimensions and materials from the setwork schedule
- Replica objects that integrate with the interactive
- Reference to specific NRS drawings (A2742-XXXX series)
- Prior RFI history on the same element (with RFI IDs and dates)
- The RAL colours/finishes specified (from NRS comment sheets)

Example from ET_09.03 Flowersmen Sensory Interactive:
```markdown
| Component ID | Description | Material/Finish |
|-------------|-------------|-----------------|
| **09.03_SW_01** | Counter: 2200×850×650mm | Solid surface |
| **09.03_SW_02** | 3× glass cases: 400×400×500mm | Glass |
| **09.03_RE_01** | 3× replica flower crowns | Model/Replica |
| **09.03_RE_02** | 9× replica herbs/flowers | Model/Replica |
```

**BOQ section mapping** — always map the scope to Main Contract BOQ sections at the top of the scope section. Interactive scope typically spans:
- §010 Models & Replicas (Tactiles & Interactives)
- §011 AV Hardware (Digital Interactives hardware)
- §014 Mock-ups, Samples & Prototypes

If no dedicated BOQ line exists for a service, state it explicitly so the pricing proposal can split costs correctly.

### Step 3: Deep research — find all related documents

Before writing SCOPE_REQUEST.md, search the entire project for relevant documents:

```bash
# Search file contents for keywords
rg -il "interactiv|G9|Flowersmen|scent|smell" --type pdf --type md --type xlsx

# Check project memory for drawing codes and BOQ references
grep "Tactile\|Interactiv" Scripts/PROJECT_MEMORY.md

# Check exhibit schedules for the specific exhibit
grep "ET_09" Design Files/*Schedule*/Xcel/*.md

# Check Drawing Register for NRS drawing numbers
grep "A2742-1721\|1860-1882" Scripts/notes/drawing_system.md

# Check email intelligence
grep "RAW-RFI-G9\|interactiv" Scripts/notes/email_intel_30d.md

# Check RFI register
grep "interactiv\|G9\|Flowersmen" Scripts/output/ms_file_previews/*RFI_Register*.md

# Check subcontractor register
grep "T2-09\|Interactives" Scripts/notes/Knowledge\ Notes\ -\ Stakeholder\ Mgmt\ Plan\ Rev02.md
```

### Step 4: Copy reference files

Copy relevant files from their source locations into the subcontractor folder's subdirectories:

| File type | Source | Destination |
|-----------|--------|-------------|
| RFIs, correspondence | `Correspondence/` or `Completed Tender Package From NRS/05_Correspondence_Archive/` | `02_Reference_Drawings/` |
| NRS drawings | `Completed Tender Package From NRS/06_Drawing_Source_Folders/` | `02_Reference_Drawings/` |
| Tactile/interactive schedules | `Design Files/03_AS_Pre-Appointment Exhibition Schedules_250313/` | `01_Schedule_and_BOQ/` or `03_Specifications_and_Standards/` |
| Acoustic / specs | `Subcontractors/NN_Discipline/` | `03_Specifications_and_Standards/` |
| SoW extracts | `Contracts/01_Main_Contract/` | `03_Specifications_and_Standards/` |

### Step 5: Create situation report

Create `_MANAGER_DASHBOARD/SITUATION_REPORT.md` with:
- Status (🟢🟡🔴) and last updated date
- Current state table: procurement status, contract status, programme position
- Open actions table: action, owner, target date
- Key documents table: folder paths with descriptions
- Risk items / critical issues
- Timeline snapshot of key dates

### Step 5b: Verify SOW references match actual files

After writing SCOPE_REQUEST.md, audit the reference files section:
1. For every file path listed in §6 (Reference Files), check it exists in the subfolder
2. If a referenced file is missing, either copy it from its source or remove the reference
3. Ensure the SOW accurately describes what's in each subfolder

### Step 5d: Create email draft for PM

Create `_MANAGER_DASHBOARD/_Email_Draft_to_find_lab.md` with:
- Subject line: `Action Required — Find & Engage [Discipline] (Sub NN)`
- To: [Name], From: Project Manager
- Bullet list of what's needed (scope summary, key deliverables)
- Deadline for candidate shortlist
- Reference to the SOW in the subfolder

### Step 5e: Update Key Personnel Register (if applicable)

If this subcontractor maps to a Tier 2 role in the KPR that was previously TBC:
- Add the company/person name to the KPR xlsx
- Update the Summary sheet (total roles, tier counts, pending count)
- Bump revision number (Rev C02 → C03 etc.)
- Update issue date
- Add relevant notes to the Lock-in Notes column (scope references, sub number)

### Step 5f: Resolve duplicate numbering (if needed)

If the new sub's `NN_` prefix conflicts with an existing folder:
- Keep the existing sub at `NN_Name` (it was created first)
- Use suffix for the new sub: `NNa_Name` or `NNb_Name`
- Convention: `a` = trade/construction, `b` = purchasing/material/vendor
- Example: `10_Oddy_Testing_Lab` + `10b_Purchasing_Patinated_Brass`, `14_Rigging_Contractor` + `14a_MEP_Contractor`

### Step 5b: Create formal SOW DOCX (for issue to bidders)

The .docx goes at **sub root level** (NOT inside `_MANAGER_DASHBOARD/`). The .md source stays in `_MANAGER_DASHBOARD/`.

After SCOPE_REQUEST.md is finalized, create a formal .docx version following the **Samaya Doc Style Guide v1.0** (`_Style-Guides/Doc Style Guide/`):

1. **Use the SamayaDoc class** from `samaya_doc_template.py` — header/footer with doc ref, rev, date, project name, confidential marking
2. **Include a Document Control (DC) block** after the title — table with these fields (order matters): Document Ref, Revision, Issue Date, Prepared By (Samaya Investment — Technical Office / BIM Unit), Reviewed By (Technical Office Manager), Approved By (Projects Director), Document Type, Project (with contract number), Discipline, T2 Allocation, Distribution (CG · PMC · MoC · Sub · Samaya TO), Classification (Confidential — Samaya Investment)
3. **Authoring rules for formal SOW documents:**
   - Only reference **approved source documents** (ER, SOW, Contract, DMP, approved submittals, CG responses, NRS approved drawings)
   - **Never state scope exemptions, inclusions, or requirements** based on inference — if no approved doc clause supports a claim, omit it or flag as TBC
   - **NRS drawing references**: define NRS drawing numbers (e.g., A2742-1721/1722) **once** in the DC block or exhibit ID section. After that, refer to NRS as **"the Design Lead"** throughout the document body. NRS document codes (RFI numbers, drawing codes) belong only in the Authority Basis section where source documents are formally cited.
   - **Interfaces**: only list interfaces that are documented in approved source docs (ER, SoW, DMP, contracts). Do NOT infer or add interface rows (e.g., acoustics, sustainability) based on general project knowledge — if no approved doc assigns a coordination requirement, omit it.
   - Repeat NRS references only in the Authority Basis section where source documents are listed
4. **Sections to include** (following SOW Template pattern): Purpose, Background, Exhibit Context, Scope of Work (8 sub-systems), Key Design Parameters, Prequalification Requirements, Programme Milestones, Open Technical Questions (if any), Quality Requirements, Required Manpower, Restrictions, Obligations (Sub-contractor + Samaya), Critical Interfaces, BOQ References, Authority Basis
4. **Save location**: `Subcontractors/NN_Discipline_Contractor/SCOPE_REQUEST.docx` (sub root, NOT inside `_MANAGER_DASHBOARD/`)

### Step 6: Update README.md

Add a new row to the subcontractors register table in `Subcontractors/README.md`:

```markdown
| NN | **Discipline** (description) | [`NN_Discipline/`](NN_Discipline/) | **NEW · YYYY-MM-DD** — brief status + trigger ref | lead time |
```

Also update the "Last updated" line at the top.

### Step 7: Migrate from Specialist/ folder (if applicable)

When a specialist from `Docs/09_Registers/Specialist/` needs to become an active subcontractor:

1. **If the specialist maps to an existing sub** (e.g., Rawasin → 03_AV_IT_Contractor, GLASBAU HAHN → 02_Showcases_Contractor):
   - Copy prequalification PDFs into the existing sub's `03_Specifications_and_Standards/`
   - Verify the sub already has SCOPE_REQUEST.md covering the specialist's scope

2. **If the specialist is a new trade** (e.g., ZNA studio → 20_Lighting_Designer):
   - Create the numbered subfolder with full 9-dir structure
   - Move prequal docs into `03_Specifications_and_Standards/`
   - Create SCOPE_REQUEST.md following the Samaya 10-section template
   - Create SITUATION_REPORT.md in `_MANAGER_DASHBOARD/`

3. **Clean up Specialist/ folder:**
   - Remove migrated specialist folders (GLASBAU HAHN, Rawasin, ZNA studio)
   - Keep only reference entities: NRS (Designer, not a sub), Design Methodology (NRS deliverables)

### Step 8: Update memory

Add a compact memory entry recording the new subcontractor number, discipline, trigger document, and date created.

## Pitfalls

- **Do not reuse an existing numbered folder** — just because scope overlaps doesn't mean it's the same package. Check the Project directory structure for the specific discipline.
- **SCOPE_REQUEST.md must be original** — do not copy another subcontractor's scope verbatim. The template structure is reusable; the content must be specific to this trade.
- **Deep research is not optional** — the project has thousands of files across `Design Files/`, `Completed Tender Package From NRS/`, `Correspondence/`, `Contracts/`, and `Scripts/notes/`. A quick search often misses key references.
- **NRS drawing numbers follow rules** — drawing codes 1860-1882 = Tactiles/Interactives. Reference drawings exist under `A2742-1721+` for the Floral Crown Smell Table.
- **T2 allocation comes first** — before writing any scope assignment, check the T2 table in `Scripts/notes/Knowledge Notes - Stakeholder Mgmt Plan Rev02.md`. Interactive = T2-09 (Rawasin umbrella). AV = T2-10 (AVD). If the new sub sits under an existing umbrella, state the relationship clearly.
- **Use execute_code or terminal with shell_quote for filenames with special chars** — filenames with `&`, spaces, or special characters need quoting. Prefer `shlex.quote()` from `hermes_tools` when running `cp` in bash.
- **Analysis files go alongside PDFs** — when placing the RFI in the sub's folder, also consider whether it needs an analysis note. The original location may already have one.
- **BIM families exist** — check `Completed Tender Package From NRS/01_Registers_and_Logs/File_Register_Index.csv` for RVT/RFA family files that may contain interactive component models.
- **Formal DOCX must only cite approved source docs** — never state scope exemptions, inclusions, or requirements based on inference. If no approved document (ER, SOW, Contract, DMP, approved submittal, CG response) supports a claim, omit it or flag as TBC. Unsourced claims in formal documents will be caught and must be corrected.
- **NRS over-referencing** — listing NRS drawing numbers and RFI codes in every section clutters the document. Define them once in the DC block/exhibit ID, then use "the Design Lead" throughout. Reserve full document codes for the Authority Basis section.
- **SOW §6 reference-to-file verification** — the Reference Files section MUST only list files that actually exist in the subfolder. After authoring the SOW, walk through every path in §6 and confirm the file is present. Missing files = invalid SOW. Copy them in or remove the reference.
- **SITUATION_REPORT.md keeps programme dates current** — every time you touch a subfolder, update the dates in the SitRep. Stale dates (e.g., referencing 2025 LOA in mid-2026) make the report unreliable.
- **Duplicate approval docs** — `07_Approvals/` may contain the same file under two names: original-received (`2026-05-08_GGG_1000_*.pdf`) and project-registered (`MOC-ASEER-MS-FB-001_*.pdf`). Compare MD5 hashes; keep the project-registered version only. Verify no broken references after removal.
- **Supplier-provided cert ≠ independent test** — compliance certs from suppliers (Greenguard, manufacturer Oddy) are supporting evidence only. They do not substitute for independent BM 3-month Oddy testing. Flag this distinction in the SOW and SITUATION_REPORT.
