---
name: project-scope-verification
description: "Answer whether a specific requirement, test, deliverable, or inspection is contractually in-scope for a construction/museum project by systematically searching contract docs, ERs, SoW, BOQ, specifications, and management plans."
version: 1.0.0
author: hermes
license: MIT
platforms: [macos, linux]
metadata:
  hermes:
    tags: [scope, contract, requirement, verification, document-search, construction]
    examples: ["is X test required", "check if Y is in scope", "scope verification"]
---

# Project Scope Verification

Use when the user asks "is X required/test/inspection/deliverable in our project?" — verify contractual scope by systematically searching project documentation.

## Process

### 1. Confirm the project path

Identify the project root. For Samaya BIM projects (Aseer, Zamzam, etc.) these live under:
- `OneDrive-SAMAYAINVESTMENT/Samaya/Technical Office/Bim Unit/<Project>/`
- `OneDrive-SAMAYAINVESTMENT/ASEER MUSEUM - Consultant Requirement/`

Check `_Project_Memory/PROJECT_MEMORY.md` first — it often contains a fast answer for common scope questions.

### 2. Search in priority order

Contractual authority hierarchy (higher overrides lower):
1. **Contract** (main agreement + annexes) — the ultimate scope definition
2. **Employer's Requirements (ER)** — technical scope + specifications
3. **Scope of Work (SoW)** — detailed work description
4. **BOQ / Pricing Schedule** — if costed, it's in scope
5. **Specifications** (CSI MasterFormat + project-specific) — technical detail
6. **Method Statements & Management Plans** (PEP, HSE Plan, QMP, DMP) — execution detail
7. **Registers** (submittal, material, T&C) — what's actually being tracked

### 3. Search technique per file type

| File Type | Method | Notes |
|-----------|--------|-------|
| `.md`, `.txt` | `find . -maxdepth N -name '*.md' -exec grep -li 'term' {} +` | Fastest. Limit depth to avoid timeout. |
| `.pdf` | `pdfminer.high_level.extract_text()` then search | Can miss tables, diagrams, scanned pages |
| `.xlsx` | `openpyxl` with `read_only=True, data_only=True` | Iterate rows, search joined cell text |
| `.eml` | `grep -i` directly | Email text is plaintext-searchable |
| `.csv` | `grep -i` or python csv reader | |
| `.md` email archives | `grep` on subject filename → body content check → reference file `email-archive-search.md` | Many emails have only YAML frontmatter (corrupted body). Check file size (>400 bytes) first. Scope/pricing requests often embedded in email threads, not formal contract docs. |

### 4. Handling grep timeouts

Large OneDrive directories cause `grep`/`find` to timeout. Mitigations:
- Limit depth: `find . -maxdepth 4 -type f -name '*.md' ...`
- Limit file types: exclude `.pdf`, `.xlsx`, `.eml` from broad greps
- Search subdirectories independently rather than the whole tree
- Use `-exec` instead of piping to `xargs` for better timeout control
- If `search_files` tool times out (>60s), fall back to `terminal` with `find` + `grep`

### 5. Interpreting results

| Finding | Interpretation |
|---------|---------------|
| Explicitly mentioned as a requirement | ✅ Contractually required |
| Listed as unchecked/conditional prerequisite (e.g. `[ ] Asbestos survey if applicable`) | ⚠️ Not formally required, but recommended practice |
| Found in BOQ / Pricing Schedule as a line item | ✅ Costed = required |
| Mentioned as a "missing spec" in audit reports | 🟡 In scope but not yet specified — technically required |
| Not mentioned anywhere, not excluded | ❓ Likely not required, but verify with SoW/ER scope boundaries |
| Explicitly listed in "Scope Exclusions" / "Out of Scope" | ❌ Not required |

With evidence

Always cite the specific document, section, file, and line where the requirement is found or ruled out. Example:

> **No — hazmat screening is NOT explicitly required.** Contract §X only mentions hazardous material handling for packaging/storage (not building screening). MS-02 lists asbestos survey as an unchecked conditional prerequisite. No BOQ line item exists.

## Material / Product Compliance Check

Use when the user asks "does this product/material comply with our project?" — evaluating a supplier's datasheet, test certificate, or product profile against project specifications.

### Acoustic/Ceiling Finishes Compliance

Use when reviewing **acoustic sprays, plasters, or ceiling panels** against project TOS (Technical Outline of Services) or ER (Employer's Requirements).

#### Process

1. **Extract TOS/ER requirements** for acoustic performance:
   - **NRC** (Noise Reduction Coefficient)
   - **CAC** (Ceiling Attenuation Class)
   - **STC** (Sound Transmission Class)
   - **Fire rating** (e.g., Class A, BS 476)
   - **VOC emissions** (LEED/Mostadam compliance)
   - **Thickness** (e.g., 25mm spray, 40mm plaster)
   - **Application method** (spray, trowel, panel)

2. **Extract product data** from supplier submittal:
   - Test reports (e.g., ASTM C423 for NRC, ASTM E1414 for CAC)
   - Fire certificates (e.g., EN 13501-1)
   - VOC test reports (e.g., LEED EQ C4.2)
   - Installation instructions (thickness, substrate prep)

3. **Cross-reference** product data against TOS/ER:
   - **NRC ≥ X** → Check ASTM C423 test report
   - **CAC ≥ Y** → Check ASTM E1414 test report
   - **Fire rating Class A** → Check EN 13501-1 or BS 476 certificate
   - **VOC ≤ Z g/L** → Check LEED EQ C4.2 or Mostadam test report
   - **Thickness** → Check installation instructions

4. **Flag deviations** with evidence:
   - **Critical**: Missing test reports, fire certificates, or VOC compliance
   - **Moderate**: Thickness or application method mismatch
   - **Low**: Minor test report formatting issues

5. **Report per product** with compliance matrix:

   ```
   **BoSpray 25mm Acoustic Spray**
   - ✅ NRC 0.85 (TOS requires ≥0.80) — ASTM C423 test report
   - ✅ CAC 35 (TOS requires ≥35) — ASTM E1414 test report
   - ✅ Fire rating Class A — EN 13501-1 certificate
   - ✅ VOC 4 g/L (LEED EQ C4.2 compliant) — Test report
   - ❓ Thickness: 25mm (TOS specifies 25mm) — Confirm substrate prep
   - → **Conditionally compliant** — Verify substrate compatibility
   ```

#### Pitfalls

1. **Binary PDF extraction** — Acoustic test reports are often PDFs with tables. Use `read_file` with `offset`/`limit` to extract text; avoid `web_extract`.
2. **Test report age** — Check if the project requires current-year testing (e.g., 2026 vs. 2017 reports).
3. **LEED/Mostadam documentation** — A VOC test report alone may not satisfy full LEED submittal requirements. Verify project-specific LEED documentation needs.
4. **Thickness vs. performance** — A product may meet NRC/CAC at 20mm but the TOS requires 25mm. Flag as a deviation.
5. **Fire rating vs. acoustic performance** — Some acoustic products sacrifice fire rating for performance. Check both.

### Process

1. **Confirm the project** — ask or cross-reference. With multiple active projects (e.g. Aseer Museum vs Moqtana/Tqanny), never assume context. Verify before searching.

2. **Identify the project's material requirements**:
   - **Specifications** (CSI MasterFormat sections, particularly Divisions 07–12)
   - **ER / SoW** clauses governing materials (performance criteria, certifications, sustainability)
   - **BOQ line items** — costed items are mandatory
   - **Room Data Sheets** — finish schedules, material types per space
   - **Applicable codes** (SBC, SASO, NFPA, ASHRAE, Mostadam/LEED)

3. **Map product properties against requirements**:

   | Product Property | Check Against | Example |
   |-----------------|---------------|---------|
   | VOC content | Local code limits (SASO, SCAQMD), LEED/Mostadam thresholds | PU sanding sealer @ 216 g/L vs clear wood coating limit ≤275 g/L → ✅ |
   | Certifications | Project sustainability requirements (LEED EQ, Mostadam, Catas) | LEED EQ C4.2 certified → ✅ if project targets LEED |
   | Material type (water/solvent) | Indoor air quality / museum environment specs | Water-based preferred for museum galleries → ✅ |
   | Fire rating | SBC / NFPA / Civil Defence requirements | Fire-rated coating certification needed if in egress paths |
   | Weather resistance | Applicable for exterior elements | EN 927-3 test → ✅ if exterior wood is in scope |
   | Manufacturer standing | ER prequalification clauses | ISO-certified mfr, international presence → ✅ |

4. **Report per material with evidence**:

   ```
   **RITVER WT73X0 Wood Topcoat**
   - ✅ Catas certified (VOC 4%, LEED EQ C4.2)
   - ✅ EN 927-3 weathering test passed
   - ✅ Water-based — good for museum IAQ
   - ❓ Need project spec to confirm: required gloss level, recoat compatibility with specified primer, SASO VOC limit
   - → **Conditionally compliant** — technically sound, verify against finish schedule
   ```

### Pitfalls

1. **Assume wrong project** — When a user has multiple active projects (Aseer, Moqtana, Tqanny, Zamzam), the conversation context can be ambiguous. Before searching for specs, confirm: "This is for Aseer Museum?" Never proceed on assumption. The user's memory has a strict project-separation rule — if you cross-reference, you will be corrected.
2. **Locked xlsx / corrupt PDF** — BOQ files are often open in Excel on the user's machine, causing openpyxl `Resource deadlock avoided` errors. The PDF mirror may also be corrupted or inaccessible. When both fail, ask the user directly for the relevant spec section.
3. **No spec ≠ pass** — Absence of a specific paint/coating clause in ER/SoW does not mean the product qualifies. Check BOQ line items, Room Data Sheets, and finish schedules.
4. **Certificate age** — Test reports from 2017 (as in this session) may be stale. Check whether the project requires current-calendar-year testing or accepts legacy certs.
5. **LEED/Mostadam documentation gap** — A LEED VOC test cert alone does not satisfy a full LEED submittal. Check whether the project requires product-specific LEED documentation or just a test report.

## Multi-Contractor Scope Gap Analysis (NEW)

Use when a subcontractor excludes an item from their scope and you need to determine whether another contractor covers it or it falls through as a gap.

### Process

1. **List all contractors with potential overlap** — check the project's subcontractor directory (e.g., `Subcontractors/` in BIM root). Each numbered subfolder (02_Lighting_Designer, 05_Showcases_Contractor, 10_MEP_Contractor, 13_MEP_Designer, etc.) is a party.

2. **Map each exclusion against every other contractor's SOW** in priority order:
   - CG/Consultant requirements (submittal responses, comment sheets)
   - MEP Designer SOW (for base-build systems — lighting, power, HVAC, fire)
   - MEP Contractor SOW (for installation scope)
   - Specialist Contractor SOW (showcase, AV, graphics, fit-out)
   - Lead Designer / Exhibition Designer SOW
   - Main Contract ER/SOW (the ultimate catch-all)

3. **Categorize each exclusion**:

   | Finding | Meaning |
   |---------|---------|
   | Explicitly listed in another contractor's scope | ✅ Covered — no gap |
   | Referenced as "by others" or "coordination only" in both scopes | 🟡 Disputed — clarify who designs vs who installs |
   | Not mentioned in any SOW but CG requires it | 🔴 GAP — no one contracted for it |
   | Implied by "all reasonably required works" clause | 🟡 Contractually required but not specifically assigned — assign to most relevant party |
   | Listed as installation-only in one scope, design not assigned | 🔴 GAP — installation exists but no design authority |

4. **Check for the "coordination only" trap** — When a specialist says "coordination only" for an item (e.g., showcase lighting), it means they'll comment on others' work but won't produce their own design. Verify that another party is producing that design. If no one produces it, it's a gap.

5. **Verify design-vs-install split** — Many exclusions are actually design vs installation boundaries:
   - Contractor supplies hardware + installs → they NEED design specs from someone
   - Designer produces specs + layout → they NEED someone to install
   - If designer says "not in scope" and contractor says "supply only per spec" → both point at each other → 🔴 GAP

6. **Report with evidence chain** — For each gap, cite the specific document lines:
   > **Showcase lighting design**: ZNA SOW email says "coordination only" (line X). GBH profile shows LED spots/strips integrated in case (line Y) but no lux/color temp/conservation design. CG comment #1 requires "showcase and display lighting." MEP Designer SOW §2.2 explicitly excludes exhibition lighting. → **🔴 GAP — no one designs showcase lighting.**

### Example chain (Aseer Museum)

```
ZNA exclusion "showcase lighting = coordination only"
  → Check GBH (Showcases) SOW: provides LED hardware in cases, no design
  → Check MEP Designer SOW: "exhibition lighting by 02_Lighting_Designer" [explicit exclusion]
  → Check CG comment #1: "showcase and display lighting" required from ZNA
  → Check Main Contract ER: "all reasonably required works"
  → Verdict: 🔴 GAP — no one provides showcase lighting design
```

### Critical Baseline Rule — Submitted Scope, Not Internal Revisions

**🚨 This is the #1 correction trigger with this user.** 🚨

When analyzing a subcontractor's scope gaps:

1. **Baseline = the SOW that was submitted to CG and approved (Code B/C)** — that document is the agreed contractual scope between you and the client
2. **Do NOT compare against internal revisions you never submitted** — the user will be frustrated if you call gaps against an enhanced internal SOW they prepared but never sent to CG
3. **The user's own internal review said "substantially compliant"** — trust that. If CG approved it with only minor comments (Code B), the core scope is sound. Focus gaps on the specific CG comments and contractual requirements, not an internal wish-list
4. **If you find yourself about to say "this only covers X%", verify what document you're comparing against** — if you're comparing the submitted scope against an un-submitted internal revision, you're generating noise, not signal

**Pattern of the correction the user gives:**
- "but we already submitted the draft sow to cg and they approve"
- "ok we will base only the submitted scope of work"
- → Re-anchor immediately to the submitted-SOW-as-baseline

### Designer vs Installer Split — Don't Call False Gaps

Many apparent scope gaps are actually **design vs installation boundaries**, not real gaps where no one covers the work:

| Pattern | Meaning | Not a Gap If... |
|---------|---------|-----------------|
| Designer says "design only" | They produce specs/layouts — someone else installs | Another contractor is contracted for installation |
| Contractor says "supply per spec" | They provide hardware — someone else designs | A designer is contracted to produce specs |
| Both point at each other | 🔴 **Real gap** — no one assigned | Cross-reference both SOWs to find the gap |
| "Coordination only" | Will comment but not produce design | ✅ Must verify SOMEONE ELSE produces the actual design |

**Common split patterns on Aseer Museum:**
- **Lighting**: ZNA designs → M&E Contractor supplies + installs (not a gap — correct split)
- **MEP**: AD Engineering designs → M&E Contractor installs (not a gap — correct split)
- **FLS**: Nama Consulting designs → M&E Contractor installs (not a gap — correct split)
- **AV**: NRS/AVD designs → Rawasen supplies + installs (not a gap — correct split)

**Always check the split before reporting a gap.** If the designer carves out installation and a contractor exists for installation, it's a boundary, not a gap.

### Payment Schedule Milestones

When evaluating a subcontractor's payment schedule alongside their scope:

**Milestone structure rules:**
- Payment milestones must be tied to **submittal register approval gates** (50%/90%/100% IFC), not the subcontractor's internal progress percentage
- **Front-loading is a red flag** — >40% before 90% delivery means they get paid most of their fee before the design is actually approved
- **Stage 5 (IFC/AFC review) should be in the base fee**, not optional at 50%+ of design fee — construction support is a standard professional obligation, not a premium service
- **Stage 6 (as-built/aftercare) must be costed or explicitly excluded** — leaving it unmentioned creates a post-appointment gap

**IFC/AFC effort** (what the subcontractor actually does in Stage 5):
- Review contractor's shop drawings against design intent (check, not produce)
- Respond to RFIs during installation
- Review material substitution requests
- Possibly attend site for mock-up review
- Witness commissioning tests

That's it — no new drawings, no design production. Fee should reflect this as a watching brief (typically 10-15% of design fee), not 50%.

**When the user asks "what efforts will they do?" — answer with concrete activities like the list above, not percentages or abstract descriptions.**

### Pitfalls (specific to this workflow)

1. **Do not compare against unsubmitted revisions** — Baseline = CG-approved submitted SOW. Using an internal Rev 01 that was never sent to CG as the comparison standard will generate spurious gaps and frustrate the user.

## RACI-Based Scope Verification (NEW)

Use when a subcontractor submits their own SOW and you need to validate it against the project's RACI matrix — the definitive "who does what" document.

### When to Use
- Subcontractor sends a self-authored scope document for review
- You have a project RACI matrix (MEP/BMS/ICT/AV Interfaces or similar)
- Need to identify overreach (subcontractor claiming scope that belongs to a specialist) AND gaps (missing items that ARE their responsibility)

### Workflow

**Step 1: Extract the RACI matrix first**
```bash
python3 -c "
import openpyxl
wb = openpyxl.load_workbook('path/to/RACI.xlsx', data_only=True)
ws = wb['RACI Matrix']  # or the correct sheet name
for row in ws.iter_rows(min_row=1, max_row=ws.max_row, values_only=False):
    vals = [(c.value, c.coordinate) for c in row if c.value is not None]
    if vals: print(' | '.join([f'{c}:{v}' for c,v in vals]))
"
```
The RACI columns typically show each party's role (R/A/C/I) per interface activity. Identify which column is the subcontractor under review.

**Step 2: Extract the subcontractor's SOW**
Read the .docx, list all scope items they claim responsibility for.

**Step 3: Build a three-column comparison**

| Subcontractor's Claim | RACI Says | Verdict |
|-----------------------|-----------|---------|
| "Fully responsible for BMS design" | AD = C (Consulted), BMS/ICT = R | ❌ **Overreach** — specialist leads BMS |
| "Responsible for CCTV/ACS" | AD = R for power only, specialist = R for system | ❌ **Overreach** — power/containment only |
| "Responsible for PAVA" | AD = C, BMS/ICT = R, Namaa = R | ❌ **Overreach** — specialist scope |
| "Responsible for ICT structured cabling" | AD = C, BMS/ICT = R | ❌ **Overreach** — specialist scope |
| "Responsible for BIM/Revit models" | Samaya = R (DC-06/07), AD provides CAD input | ❌ **Overreach** — Samaya BIM Unit handles |
| "Responsible for construction support" | Samaya = R (TC/DH rows), AD = I | ❌ **Overreach** — AD is informed only |
| "Responsible for power distribution" | AD = R (PC-01→06) | ✅ **Correct** |
| "Responsible for earthing/lightning" | AD = R (PC-06) | ✅ **Correct** |
| "Responsible for HVAC design" | AD = R (DC-01→05, FL-02→04) | ✅ **Correct** |
| "Responsible for fire alarm power" | AD = R for power, specialist = R for system | ✅ **Correct** (power-only is the right boundary) |

**Step 4: Identify the "fully responsible" language trap**

When a subcontractor's SOW uses "fully responsible" for items the RACI assigns to a specialist, this is a **scope creep risk**:

- If signed as-is, the subcontractor could claim they own that system's design
- They could then bill extra when the specialist produces their own design ("coordination effort")
- They could claim delays because the specialist didn't submit to them
- The "fully responsible" language creates ambiguity about who leads vs who supports

**Step 5: Identify the "blanket clause" trap**

Watch for clauses like:
> *"Any engineering service, drawing, calculation, report, specification, schedule, BIM deliverable, BOQ item, coordination activity or technical document reasonably required to complete the [discipline] Design and obtain final approval, whether specifically stated herein or reasonably implied by good engineering practice, shall be deemed to be included within the Consultant's Scope of Services without additional cost to the Employer."*

This is dangerous because:
- It creates an open-ended scope obligation
- Combined with "fully responsible" language for specialist systems, it could be interpreted as requiring the subcontractor to produce specialist designs
- It removes the subcontractor's ability to claim a variation for scope that was "reasonably implied"
- It shifts the burden of scope definition entirely onto the employer

**Step 6: Report with clear verdicts**

For each item, state:
- **✅ Correct** — matches RACI, no change needed
- **❌ Overreach** — subcontractor claims scope that belongs to a specialist per RACI. Must be removed or downgraded.
- **🔴 Missing** — item is the subcontractor's R responsibility per RACI but absent from their SOW. Must be added.
- **⚠️ Language risk** — "fully responsible" or blanket clause creates ambiguity. Needs narrowing.

### Example output

```
AD Engineering Electrical SOW — RACI Verification

✅ Correct (8 items):
  - Power distribution (PC-01→06) — AD = R
  - Earthing/lightning (PC-06) — AD = R
  - Emergency/exit lighting (LS-03) — AD = R
  - Fire detection power — AD = R for power
  - Lighting FOH/exhibition = by Others — matches ZNA = R
  - AV system = by Others — matches RAWASIN = R

❌ Overreach (5 items — must remove):
  - BMS design (§29) — AD = C only, BMS/ICT = R
  - ICT/structured cabling (§24) — AD = C only, BMS/ICT = R
  - CCTV/security (§25) — AD = C only, specialist = R
  - Access control (§30) — AD = C only, specialist = R
  - PAVA (§28) — AD = C only, BMS/ICT = R
  - BIM/Revit models (§36) — Samaya = R

⚠️ Language risk (2 items):
  - "Fully responsible" used 8 times — creates ambiguity on specialist boundaries
  - Blanket "deemed included" clause (§48) — open-ended scope obligation
```

### Pitfalls

1. **RACI is the definitive source** — Check the RACI before flagging any gap. If the RACI says the subcontractor is only "C" (Consulted) or "I" (Informed) for a system, their SOW should NOT claim full responsibility for it.
2. **"Power distribution only" is correct** — When the RACI shows AD = R for power/containment and a specialist = R for system design, the subcontractor's "power only" language is CORRECT. Do not flag as a gap.
3. **"Fully responsible" is a red flag** — A subcontractor claiming full responsibility for a system the RACI assigns to a specialist is overreaching, not being thorough.
4. **Blanket clauses hide scope creep** — "Reasonably required" + "deemed included" + "without additional cost" is a triple trap. Flag it explicitly.
5. **RACI may have multiple sheets** — Check all sheets. The main matrix may be on one sheet, with party role descriptions and LOD definitions on a "Notes" sheet.
6. **RACI columns may not be in party-name order** — The columns may be ordered by role (Samaya first, then designers, then specialists, then surveyors). Read the header row carefully.

## Single Subcontractor Scope Document Review (SOW/ER Adequacy Check)

Use when the user asks "check this scope document against SOW and ER" — reviewing a single subcontractor's submitted scope document (often bilingual AR/EN .docx) against the project's governing SOW and ER documents to identify what's missing.

### When to Use
- User sends a subcontractor scope document (Arabic/English) and asks "check this against SOW and ER"
- Evaluating a candidate's self-authored scope before contract award
- Verifying a scope document covers specialist integration boundaries correctly
- Similar to Phase 2 Technical Offer Gap Analysis but focused on **scope document content** rather than proposal pricing

### Workflow

**Step 1: Extract the subcontractor's scope document**
```bash
python3 -c "
import docx
doc = docx.Document('path/to/scope.docx')
for p in doc.paragraphs: print(p.text)
for t in doc.tables:
    for r in t.rows: print(' | '.join(c.text for c in r.cells))
"
```
Bilingual documents (Arabic/English .docx) are common — python-docx handles them but check for duplicate section headings (e.g., "Mechanical" title appearing twice with different content underneath — signals copy-paste errors).

**Step 2: Read the project's SOW and ER for that discipline**
- The project's SOW (e.g., `MOC-ASEER-SAM-SOW-SC-013_R01.docx`) — what Samaya asked the subcontractor to do
- Relevant ER sections (e.g., ER §3.1–3.9 for MEP) — what the Employer requires
- Other subcontractors' SOWs for adjacent/specialist trades (e.g., CITC Telecom SOW SC-014, ZNA Lighting SOW)

**Step 3: Determine if each system is MEP design scope vs specialist scope — BEFORE flagging gaps**

**🚨 This is the most common error.** Before flagging any item as a gap in the MEP scope document, you MUST determine whether that system is actually the MEP Designer's responsibility.

The correct approach is:

1. **Check the project's subcontractor directory** (`Subcontractors/` numbered folders) — does a specialist exist for this system?
2. **If a specialist contractor exists → MEP provides power distribution, containment, and coordination ONLY** (not system design). "Power Distribution Only" is CORRECT, not a gap.
3. **If no specialist exists → MEP may need to design the full system.**

**Common MEP-vs-Specialist boundaries for this project:**

| System | Who Designs It | MEP's Role |
|--------|---------------|------------|
| **Lighting** | 02_Lighting_Designer (ZNA) | Power, containment, coordination only |
| **AV / Audio & Video** | AV/IT Contractor (Rawasin) | Power, containment, coordination only |
| **PAVA (Voice Evacuation)** | AV/IT Contractor (Rawasin) | Power, containment, coordination only |
| **Fire Alarm Detection** | Specialist (drawings in LOD) | Power distribution only |
| **CCTV** | MOI/Security Specialist | Power distribution only |
| **Access Control** | Security Specialist | Power distribution only |
| **BMS** | Specialist (drawings in LOD) | Electrical infrastructure only |
| **ELV (intercom, MATV)** | Specialist | Out of MEP scope |
| **Telecom/IT** | CITC-registered telecom engineer (separate) | Not MEP design scope |
| **FLS / Fire Life Safety** | FLS Specialist Consultant | Coordination only |

**The "Power Distribution Only" pattern is NORMAL, not a gap** — when the MEP scope says "Fire Alarm Power Distribution" or "CCTV Power Distribution," this is CORRECT. The system design belongs to a specialist. Do NOT flag this as a gap.

**Step 4: Assess per-system coverage against the CORRECT baseline**

Create a table. For each system listed in the scope doc, determine:

```
| System | Subcontractor Says | Expected for MEP | Assessment |
|--------|-------------------|-----------------|------------|
| Fire Alarm | "Power Distribution" | Power/containment only (specialist designs) | ✅ Correct |
| PAVA | "Power Distribution" | Power/containment only (AV specialist designs) | ✅ Correct |
| Telecom | "ICT Power" | Power only (CITC subconsultant does design) | ✅ Correct |
```

Only flag as a gap if:
- The scope doc omits something that is **definitively MEP's responsibility** (no specialist exists)
- The scope doc has structural errors (wrong heading, copy-paste)
- The scope doc omits mandatory code/standard references

**Step 5: Check for museum-specific items that ARE MEP scope**

These are often missing from standard MEP scopes and ARE legitimate gaps:

- **Power distribution** — MV/LV, transformers, generators, UPS, SLDs, containment, earthing, lightning protection
- **HVAC** — load calcs (including gallery conditions in HAP), ductwork, CHW, ventilation, smoke management, BMS control wiring
- **Fire protection** — sprinkler, hose reel, clean agent (FM200 as part of firefighting, no split)
- **Plumbing** — limited toilets (correct as-is), water supply, drainage, condensate drain
- **Documents** — DBR, design criteria, load calculations, specifications, BOQ, drawing register, schedules

Items that may look missing but are actually covered:
- **Gallery environmental conditions** — in HAP load calculations (not a separate drawing)
- **Kitchen/café HVAC** — in floor ventilation drawings (not a separate section)
- **BMS control schematics** — in BMS drawing list section
- **Fire alarm design** — in fire alarm drawing list section (designed by specialist, not MEP)
- **Existing services data** — provided by site PM team as input (designer doesn't survey)

**Step 6: Cross-reference against what specialist contractors cover**

Before flagging ANY gap, check whether a specialist exists for that system:

| If the MEP scope says "power only"... | Check this specialist... | If specialist exists → ✅ boundary, NOT a gap |
|--------------------------------------|------------------------|---------------------------------------------|
| Lighting power only | 02_Lighting_Designer (ZNA) | ✅ Correct split |
| AV power only | AV/IT Contractor (Rawasen) | ✅ Correct split |
| PAVA power only | AV/IT Contractor (Rawasen) | ✅ Correct split |
| Fire alarm power only | Fire alarm specialist (drawings in LOD) | ✅ Correct split |
| CCTV power only | Security/CCTV specialist | ✅ Correct split |
| ACS power only | Security/ACS specialist | ✅ Correct split |
| BMS infrastructure only | BMS specialist (drawings in LOD) | ✅ Correct split |
| Telecom power only | CITC-registered telecom engineer | ✅ Correct split |

**Step 7: Document quality check**

Flag document issues that undermine the scope statement:
- Duplicate section headings with different content underneath
- Title/heading mismatch (e.g., heading says "Mechanical" but content is Electrical)
- Vague phrasing ("limited toilets" vs. specific plumbing scope)
- Unnamed specialist parties ("specialist designers" vs. naming ZNA, Rawasen)

**Step 8: Synthesize and prioritize**

Group findings into:
- **🔴 Critical** — Entire scope sections missing, role mismatch, regulatory requirements absent
- **🟠 High** — Major subsystems missing, timeline incompatibility
- **🟡 Moderate** — Partial coverage, insufficient specificity
- **🟢 Low** — Minor omissions, can be accepted

End with specific recommendations (which clauses to add, which sections to expand).

### Where the Knowledge Lives

MEP specialist integration boundaries are project-specific and evolve with contract scope definitions. Project-specific boundary details (exact ER/SOW clauses, subcontractor names, fee status) belong in `references/` files under this skill. The SKILL.md captures the reusable METHOD that works across any project.

### Common Pitfalls

- **Don't call false gaps on design-vs-install split** — If the subcontractor excludes installation and an M&E contractor is contracted for installation, it's a boundary, not a gap
- **Don't flag BIM exclusion as a gap** — Samaya BIM Unit handles Revit modelling from 2D CAD. Designer exclusion of BIM is correct per Samaya's operating model
- **Don't call survey scope a gap** — The existing-services intrusive survey may be site PM scope, not the designer's. Verify who's contracted for it before flagging
- **Check document chronology** — If the SOW was revised after the subcontractor submitted their scope, the revision represents added scope they haven't priced
- **Arabic/English .docx extraction** — python-docx works but may have garbled right-to-left text in terminal. Cross-check section structure rather than raw text order
- **Section heading duplication is a red flag** — if a heading appears twice with different content underneath, the document has a structural error (copy-paste from a template)
- **"Power distribution only" is the NORMAL pattern for specialist systems** — Do NOT flag "Fire Alarm Power Distribution" as a gap. The specialist designs the system; MEP only provides power, containment, and coordination. This is the correct arrangement, not an omission. The most common error is incorrectly expanding MEP scope by claiming specialist systems should be fully designed by MEP. **When in doubt, check the project's subcontractor directory before concluding.**
- **Verify specialist boundaries before flagging MEP scope gaps** — Before marking a system as a critical MEP gap, check whether a specialist contractor exists who covers that system's design:
  * PAVA → AV specialist (Rawasin) handles design, NOT MEP
  * Lighting design → ZNA handles design, NOT MEP
  * Audio & Video → Rawasin handles design, NOT MEP
  * Fire alarm detection → specialist covers design (drawings exist in project LOD)
  * CCTV, ACS, ELV → out of MEP design scope entirely
  * BMS network/control → specialist covers (drawings exist in BMS LOD)
  * Telecom/IT → CITC-registered telecom engineer (separate subconsultant)
  * When uncertain, check the subcontractor directory (numbered folders under `Subcontractors/`). If a numbered folder exists for that system, there's a specialist — MEP scope should be power-only.
- **English-only output** — This user communicates exclusively in English. Never use Arabic in responses, even when reviewing Arabic-language documents. All analysis, annotations, and commentary must be in English.
- **Gallery environmental conditions are in HAP calcs, not a separate drawing** — Do not flag as missing scope; they're covered by the HVAC load calculation deliverable.
- **"Limited toilets" may be correct** — Don't assume vague phrasing is an error. Verify with the user before expanding scope.
- **Kitchen hood suppression, grease interceptors, fire extinguisher schedule, external works — these are NOT MEP design scope** for this project. Do not include them in MEP scope expansion recommendations.

### Pitfalls

1. **grep times out on OneDrive** — cloud storage sync makes large directory searches slow. Narrow scope aggressively.
2. **PDF text extraction is lossy** — tables, scanned pages, and complex layouts may not extract as plain text. Cross-reference with other sources.
   - **For large PDFs**: Use `read_file(path, offset=N, limit=100)` to extract text in chunks. Avoid `web_extract` for non-textual content.
3. **Missing spec ≠ out of scope** — audit reports (e.g. Specification Scope Judgment Report) may identify items that are contractually in scope but haven't been specified yet. Check the "Missing Specifications" section.
4. **ER overrides specs** — in case of conflict, Employer's Requirements take precedence over reference specifications.
5. **BOQ is definitive for costed items** — if something has a BOQ line, it's in scope regardless of what specs say (or don't say).
6. **Method statements include conditional prerequisites** — unchecked items in MS checklists are proposals, not contractual requirements.
7. **Multiple project root paths** — Aseer has both `Samaya/Technical Office/Bim Unit/Aseer-Museum/` and `ASEER MUSEUM - Consultant Requirement/`. Contract docs are typically under the `Contracts/` subdirectory of the BIM Unit path.
8. **Odoo task names ≠ actual drawing deliverables** — When auditing whether a CG-requested deliverable exists, do NOT rely on Odoo task names alone. Odoo tasks are administrative placeholders created for workflow tracking. They may have descriptive names (e.g. \"SC-001 — Showcase schedule\") but no corresponding PDF/DWG file exists. Always cross-reference Odoo task records against actual filesystem paths and the official drawing list before claiming a deliverable is \"covered.\" If you find only an Odoo task with no matching file, report it as \"Task placeholder exists — actual drawing not yet submitted\" not \"Covered.\"
9. **User preference for terseness** — This user prefers:
   - **Fix-not-describe**: Verdicts, not edits. State compliance status upfront.
   - **Action tables**: Use tables for party assignments, deadlines, and status.
   - **Formal construction PM English**: No emoji, icons, or informal language.
   - **Consolidated emails**: Group findings by discipline/system, not per-file.
9. **Drawing codes in task names may be internal only** — "SC-001", "SC-002" etc. may be project-team shorthand in Odoo, not the actual file naming convention used by the Lead Designer (e.g., NRS uses A2742-xxxx, DT_4000 series). Verify the actual drawing numbering convention from the project's DMP or BEP before interpreting task names as deliverable codes.
10. **DD deliverables are organized by drawing PACKAGE TYPE per SOW §6.22, NOT by floor level** — On Aseer Museum, SOW §6.22 and §2.4 define DD packages as GA, Walls, Floor Finishes, Ceilings, Sections, Elevations, Showcases, etc. The actual folder structure (`02_Submittals/03_DD Documents/Arch DD Drawing/`) uses drawing-type codes (1200, 1220, 1230, 1250...). CG may request "basement priority" or "staggered by floor" — this contradicts the SOW package structure. When building submission schedules, rows must be drawing-type packages, not floors. Reference: `aseer-document-control/references/sow-622-deliverables-packages.md`.

## Drawing Deliverable Verification

When CG/PMC requests a set of drawings and asks you to check whether they're covered by the current submission:

### Step 1: Parse the request
Extract each requested deliverable from the CG email. Group by discipline (Architecture, Showcases, Lighting, AV, Graphics, MEP, FLS, etc.).

### Step 2: Check three sources independently

| Source | What It Tells You | Limitation |
|--------|------------------|------------|
| **Odoo task tree** (project packages) | What work packages are planned and tracked | Tasks may be placeholders — existence of a task ≠ existence of a drawing file |
| **File system** (actual PDF/DWG files) | What has actually been submitted/received on disk | May be incomplete if files arrived outside the working directory or were renamed |
| **Drawing register / Drawing List** (if one exists) | The master inventory of all formal drawing submissions | May be stale; verify against file system |

### Step 3: Map each request to the three sources
Build a matrix:

| Requested Drawing | Odoo Package | Files Found? | Drawing Register Entry? | Verdict |
|-------------------|-------------|-------------|------------------------|---------|
| Showcase Layout Plan | 09 — Showcases (SC-001 task) | DT_4000 series in Pre-Appt folder, no SC-001 file | Not listed | 🟡 Partial — type drawings exist, no coordinated layout plan |
| Building Sections | No dedicated Odoo package | A2742-18xx series are GA plans, no sections found | None | 🔴 Gap — not submitted in current DD |

### Step 4: Classify each item
| Verdict | Meaning | Action |
|---------|---------|--------|
| ✅ Covered | File exists, matches request, current revision | Note location and revision |
| 🟡 Partial | Related files exist but not the exact deliverable | Describe what exists vs what's missing |
| 🔴 Gap | No Odoo task, no files, no register entry | Flag for NRS or new scope |
| ⏳ Premature | SOW/phase indicates this isn't due yet | Reference phase plan, advise when due |

### Step 5: Verify physical file existence
Run `find /path/to/project -maxdepth 3 -type f \\( -name '*.pdf' -o -name '*.dwg' \\) 2>/dev/null | grep -i 'term'` for each requested item. Don't rely on memory or Odoo descriptions.

### Step 6: Report with evidence
Always cite WHERE each file was found (full path) or state "no matching file found on disk." Include Odoo task references as context, not as evidence of delivery.

## Reference files

- `references/email-archive-search.md` — searching project email archives for scope/pricing info; detecting corrupted archived emails; project code references (1311, 22047, P00444)
- `references/material-compliance-example.md` — worked example: evaluating Ritver paint/coating products against Aseer Museum project specs, including the "confirm which project" pitfall

## Cross-Contract Scope Conflict Audit

Use when a new RFP or scope package is issued and you need to audit it against ALL other subcontractor scopes for conflicts — overlaps, contradictions, interface gaps, and responsibility ambiguities. This is distinct from scope verification (is X in scope?) — it's about finding contradictions BETWEEN scopes.

### When to Use
- A new RFP is issued (e.g., Acoustic Ceiling Finishes) and you need to check it against MEP, FLS, AV, Lighting, Structural, Telecom, and other packages
- A subcontractor's scope document arrives and you need to check it against adjacent trades
- Before IFC submission, to catch coordination issues early

### Workflow

**Step 1: Read the target RFP/scope document thoroughly**
Extract all scope items, exclusions, deliverables, and coordination interfaces. Note the specific products, materials, and systems involved (e.g., BoSpray 25mm spray-on, Kvadrat Soft Cells fabric, USG Celebretto baffles).

**Step 2: Identify all potentially-affected subcontractors**
Scan the project's subcontractor directory (e.g., `Subcontractors/` numbered folders). For each, ask: does this subcontractor touch the ceiling, mount things in the ceiling, penetrate the ceiling, or provide services above/below the ceiling?

Typical affected parties for a ceiling package:
- **MEP Contractor** — ducts, sprinklers, diffusers, grilles, TAB
- **MEP Designer** — duct silencer spec, NC/NR criteria, ceiling void coordination
- **FLS Specialist** — PAVA speakers, fire detectors, emergency lighting in ceiling
- **AV/IT Contractor** — ceiling speakers, projectors, WAPs
- **Lighting Designer** — lighting fixtures, cut-outs, RCP coordination
- **Structural/Rigging Contractor** — suspension anchors, M6 rods, baffle loading
- **CITC Telecom / BMS-ICT** — WAPs, sensors, data points in ceiling
- **Showcases Contractor** — floor-to-ceiling case interfaces
- **Exhibition Fit-Out** — wall-ceiling junctions, setwork integration

**Step 3: Read each subcontractor's scope document**
For each affected party, read their SPEC.md, SCOPE_REQUEST.md, and any SOW documents. Extract:
- What they install in/through/above the ceiling
- What they exclude (explicit exclusions)
- Their coordination interfaces (who they expect to coordinate with)
- Their current status (appointed? pending? design complete?)

**Step 4: Identify conflicts by type**

| Conflict Type | What to Look For | Example |
|--------------|-----------------|---------|
| **Scope overlap** | Two contractors both claiming the same work | Both acoustic and rigging claiming baffle suspension anchors |
| **Scope gap** | Neither contractor covers a required item | Duct silencers not in MEP BoQ, not in acoustic scope |
| **Physical incompatibility** | One contractor's product prevents another's installation | Fabric acoustic ceiling (Soft Cells) cannot support PAVA speakers or fire detectors |
| **Mounting surface conflict** | Ceiling finish unsuitable for mounted equipment | Spray-on acoustic (BoSpray) cannot support speaker weight; seamless plaster (BoCoustic) needs pre-formed recesses |
| **Sequencing conflict** | One contractor's work must happen before another's but timing is uncoordinated | Acoustic spray must be applied before MEP routing, or vice versa |
| **Responsibility ambiguity** | "Coordination only" or "by others" without clear assignment | "Integrated lighting" in plasterboard ceiling — undefined who provides cut-outs |
| **Design-vs-install split unclear** | Designer says "design only," installer says "supply per spec" — no one produces the actual design | Showcase lighting: ZNA says "coordination only," GBH provides hardware but no lux/color temp design |
| **Performance target conflict** | One contractor's target contradicts another's capability | NR 30 target requires duct silencers, but MEP BoQ has no silencer line item |
| **Void/space conflict** | Ceiling type eliminates the void MEP services need | BoSpray applied directly to soffit — no ceiling void for ducts/cables |

**Step 5: Categorize severity**

| Severity | Criteria | Example |
|----------|----------|---------|
| 🔴 **High** | Blocks installation, creates life-safety risk, requires scope change, or is already an open issue | PAVA speakers cannot mount in Soft Cells (open issue F-03); NR 30 unachievable without silencers |
| 🟡 **Medium** | Creates ambiguity, requires coordination to resolve, timing risk | "Integrated lighting" undefined; WAPs in acoustic ceiling need mounting plates |
| 🟢 **Low** | Manageable with standard detailing, limited to specific locations | Floor-to-ceiling showcase interface with acoustic ceiling |

**Step 6: Check for already-open issues**
Search the project's issue registers, NRS comment disposition sheets, and RFI registers. Some conflicts may already be documented (e.g., F-03: "Detectors in fabric acoustic ceiling — unsuitable mounting surface"). Reference these as "already open" rather than newly discovered.

**Step 7: Produce structured conflict register**

Format as a table with columns:
| ID | Subcontractor | Issue | Severity | Recommended Resolution |

For each conflict:
1. **Describe the conflict** — what each scope says, where they contradict
2. **Explain the impact** — what goes wrong if unresolved
3. **Recommend resolution** — specific action, owner, and deliverable

**Step 8: Identify cross-cutting themes**
Look for patterns across multiple conflicts. Common themes:
- **Specialist not appointed** — acoustic consultant (SC-0019) pending, blocking NR criteria coordination
- **No coordinated ceiling plan** — multiple trades (FLS, AV, Lighting, BMS) all need ceiling element positions
- **Unsuitable mounting surfaces** — Soft Cells, BoCoustic, BoSpray all problematic for mounted equipment
- **Undefined scope splits** — "integrated lighting," baffle suspension anchors

### Reference file

See `references/aseer-acoustic-ceiling-conflict-audit.md` for a worked example: 12 conflicts identified across 7 subcontractor packages for the Aseer Museum Acoustic Ceiling RFP.

### Pitfalls

1. **Don't stop at the target RFP's exclusions** — The RFP may say "PAVA excluded" but that doesn't mean PAVA is covered elsewhere. Verify the responsible party actually has it in scope.
2. **Check for already-open issues** — Some conflicts may already be documented in NRS comment registers or RFI logs. Reference these rather than rediscovering them.
3. **Don't assume "coordination only" means covered** — If a subcontractor says "coordination only" for an item, verify that SOMEONE ELSE is producing the actual design/installation.
4. **Check appointment status** — A conflict may be low-severity if the responsible party isn't appointed yet (they can be directed). It's high-severity if the party IS appointed and their scope is locked.
5. **Physical incompatibility is the most dangerous** — Two scopes can both be correct individually but physically incompatible (e.g., fabric ceiling + PAVA speaker). These are the hardest to catch and most expensive to fix.
6. **The "no ceiling void" trap** — Spray-on and seamless acoustic finishes eliminate the ceiling void. MEP services that assumed a void (ducts, cables, sprinkler pipes) need rerouting. This is often missed because the RCP shows the finish, not the void.

## Verification

Use when comparing contract requirements (appendices, org charts, specialist matrices) against project registers (KPR, Stakeholder Register, subcontractor directory) to identify gaps and classification issues.

### Process

#### 1. Read the source document
Identify the contract appendix/diagram (e.g., Appendix B — Specialist Packages). Extract all listed items with their positions/layout — the layout often reveals tier classification:

- **Left column** = Contractor Specialist Packages (companies/subcontractors doing packages of work)
- **Right column** = Specialists (individual experts/consultants)
- **Bottom/center** = Integrated packages combining management + works

#### 2. Map each item to the current register

Create a mapping table:

| App B Item | Current KPR Row | Current Name | App B Classification | Issues |
|------------|----------------|--------------|---------------------|--------|
| M&E Contractor | R9 | MEP Specialist | Contractor Package | ↓ see below |

#### 3. Determine Designer vs Contractor/Installer split for each package

For each item, determine whether it's a **combined** or **split** arrangement:

| Pattern | Meaning | Example |
|---------|---------|---------|
| **Combined** | One entity does design + supply + install | Samaya Graphit (graphics design, production, installation) |
| **Split: Designer** | Specialist consultant designs only | ZNA (lighting design), AD Engineering (MEP design), Nama Consulting (FLS design) |
| **Split: Installer** | Contractor package supplies + installs | M&E Contractor (installs MEP + FLS + lighting fixtures) |

Common patterns:
- **M&E Contractor** often covers a BROAD installation scope: MEP works + FLS installation + lighting fixture supply/install
- **Showcase Contractor** is typically combined (supply + install, with design review by the Lead Designer)
- **AV Contractor** is typically combined (supply + install, design by Lead Designer or MoC-appointed specialist)
- **Designers are separate specialists** — the contractor package does not include design authority

#### 4. Tier classification rules

| Tier | Appendix B Column | Type | KPR Classification |
|------|-------------------|------|--------------------|
| Tier 1 | — | Management | Samaya's own management team |
| Tier 2 (left) | Contractor Specialist Packages | Companies/subcontractors | Contractor/Installer, supply + install |
| Tier 2 (right) | Specialists | Individual consultants | Designer/Consultant, design only |
| Tier 3 | — | Testing & Authority | Independent agents, statutory roles |

**CRITICAL: Never mix types.**
- A "Specialist" (right column) is an individual consultant providing design/advice — NOT the same as a "Contractor Specialist Package" (left column) which is a company doing installation works
- If an individual is doing coordination-only (not design), move them to NOTES, not the Name field
- The Name field in KPR should capture the DESIGN AUTHORITY (whoever is contractually responsible for the design)
- Coordination-only roles go in Notes with clear "coordination only" flag

#### 5. Verify scope boundaries

For each item, check:
- Is this Samaya's responsibility to fill? Not all contract org chart items are. Items like FF&E Supplier, Specialist Rigging may be out of scope.
- Is the designer the same as the installer? If not, two register entries needed.
- Is there a "coordination only" trap? Someone saying they just coordinate doesn't mean someone else is designing.

#### 6. Update registers

After gap analysis:
1. **KPR**: Update Name (design authority), Status (approval code), Notes (coordination roles, scope boundaries)
2. **Stakeholder Register**: Add new stakeholders, update role classifications
3. **PROJECT_MEMORY.md**: Update the specialist status table with latest appointments and gaps

### Pitfalls

1. **Do not mix Specialist (individual) with Contractor Package (company)** — They are different tiers/columns. A company listed under Specialists (right column) should be reviewed for correct classification.
2. **KPR Name field = Design Authority** — Individuals doing coordination-only go in Notes, not the Name field. The Name field identifies who is contractually responsible for that scope.
3. **Not all contract org chart items are Samaya's scope** — Some are MoC-appointed, some are reference/context only. Verify before adding rows.
4. **Designer ≠ Installer** — Do not assume one entity does both. Many packages are split: a design consultant produces specs, a different contractor installs.
5. **M&E Contractor is often a broad umbrella** — May cover MEP installation + FLS installation + lighting fixture supply/install. Track this in Notes.
6. **Combined packages exist** — Some entities do design + supply + install (e.g., Samaya Graphit, Glasbau Hahn). These are fine as-is.
7. **"Coordination only" is a trap** — If a role says "coordination only", verify that SOMEONE ELSE is producing the actual design. If no one does, it's a gap.

## Deliverable: Inline Annotated .docx

When the user asks you to "add comments in the same file with highlight" or otherwise mark up the reviewed document, produce a **copy** with color-coded annotations inserted directly after each identified gap paragraph.

### Naming convention

Copy original → `ORIGINAL_NAME_REVIEWED.docx` (save alongside the original to avoid overwriting).

### Color scheme

| Color | Meaning | Used For |
|-------|---------|----------|
| 🟥 RED | Critical gap | Entire scope sections missing, regulatory requirements absent, role mismatch |
| 🟨 YELLOW | Moderate gap | Partial coverage, insufficient specificity, missing subsystems |
| 🟩 GREEN | Confirmed correct | Properly handled items to reinforce correct clauses |
| 🟦 TURQUOISE | Note | Clarifications, boundary reminders, scope split explanations |
| 🩷 PINK | Document issue | Structural errors (copy-paste, heading mismatches, title errors) |

### Annotation format

Each annotation is a single paragraph inserted **after** the paragraph it comments on:
- **Bold label** with magnifying-glass icon: `🔍 CRITICAL GAP — Telecom/IT Design`
- **Italic body** in 9pt with highlight color
- Label in bold with matching dark color, body in black

### Python technique (oxml-based)

`python-docx` has no `insert_paragraph_after()` method on the Paragraph object. Use oxml directly:

```python
from copy import deepcopy
from docx.oxml.ns import qn

def insert_paragraph_after(paragraph):
    """Insert an empty paragraph after the given paragraph, return it."""
    new_p_elem = deepcopy(paragraph._element.getparent().makeelement(qn('w:p'), {}))
    paragraph._element.addnext(new_p_elem)
    return type(paragraph)(new_p_elem, paragraph._parent)
```

For highlighted text, construct the runs with oxml elements — `w:highlight` with `w:val` set to the highlight color name (`'red'`, `'yellow'`, `'green'`, `'cyan'`, `'magenta'`).

### Full annotation script template

Available as `scripts/docx-annotate.py` under this skill. Usage:

```bash
python3 <skill_dir>/scripts/docx-annotate.py \
  --input /path/to/review.docx \
  --output /path/to/review_REVIEWED.docx
```

Edit the `annots` list in the script to define which paragraph indices, labels, bodies, and colors to insert.

### Steps

1. **Extract and index** — Read all paragraphs with `list(doc.paragraphs)`, print each with its index and first 150 chars
2. **Map annotations** — Build a list of `(para_index, label, body_text, color)` tuples
3. **Sort descending** — Sort by index descending so inserts don't shift positions
4. **Apply** — Loop and insert annotation paragraphs
5. **Save** — `doc.save(output_path)` with `_REVIEWED` suffix

### Pitfalls

- **`insert_paragraph_after` doesn't exist** — Must use oxml `addnext()`. `insert_paragraph_before()` exists but inserts before, not after.
- **Descending sort is critical** — If you insert from top to bottom, every insertion shifts all subsequent indices. Always sort descending by paragraph index.
- **Arabic filename paths** — Arabic characters may render differently in terminal vs the actual filesystem path. Use `os.listdir()` to discover the exact filename rather than hardcoding.
- **python-docx in sandbox** — The `execute_code` sandbox has no `python-docx`. Run annotation scripts via `terminal()` with `python3` not the sandbox.

### Verification

```bash
# Fast check: does term exist in any project text file?
find /path/to/project -maxdepth 5 -name '*.md' -exec grep -li 'your-term' {} + 2>/dev/null

# Check BOQ for line item
python3 -c "
import openpyxl
wb = openpyxl.load_workbook('/path/to/boq.xlsx', read_only=True, data_only=True)
for s in wb.sheetnames:
    for row in wb[s].iter_rows(values_only=True):
        if 'your-term' in str(row).lower():
            print(f'{s}: {row}')
"
```

## Variant: Create COMPLIANT Revision

After the REVIEWED annotation pass, the user may ask you to incorporate the corrections directly into a new document version. Produce a COMPLIANT copy that fixes the actual scope text, not just annotations.

### Naming convention

`ORIGINAL_NAME_COMPLIANT.docx` — saved alongside the original.

### What to change (vs annotated REVIEWED version)

| Change Type | Example | How |
|-------------|---------|-----|
| **Fix heading errors** | "Scope of Mechanical & Fire Fighting" → "Scope of Electrical Systems Design" | Direct text replacement in the paragraph runs |
| **Add new scope items** — ONLY if definitively MEP scope | Gallery environmental conditions in HAP, kitchen/café ventilation | Insert italic grey supplementary paragraph after the original line |
| **Fix vague wording** — ONLY if user confirms it's an error | "limited toilets" → only change if user says so | Direct text replacement in runs |
| **Clarify specialist boundaries** — when user confirms | "PAVA Power Distribution" → add note that AV specialist handles design, MEP provides power only | Insert italic supplementary paragraph |

### 🚨 CRITICAL: What NOT to change (most common mistake)

**DO NOT add scope items that are handled by other specialists.** This is the #1 error pattern.

❌ **WRONG** — Adding to MEP scope:
- Full fire alarm detection system design (specialist covers this)
- Full CCTV/ACS system design (security specialist covers)
- Full BMS network design (BMS drawings already in LOD)
- ELV systems design (out of MEP scope)
- Telecom/IT structured cabling design (CITC subconsultant)
- Kitchen hood suppression (kitchen/fire specialist)
- Grease interceptors (installed by plumbing contractor, not designed by MEP)
- Fire extinguisher schedule (FLS specialist)
- External works coordination (separate scope)
- Existing services survey clarification (site PM scope)
- Construction support extension (not MEP scope)

✅ **CORRECT** — What to fix:
- Heading errors (e.g., "Mechanical" → "Electrical" when content doesn't match)
- Only if user confirms: expanding vague items that are actually MEP scope

**The "Power Distribution Only" pattern is CORRECT, not a gap.** When the MEP scope says "Fire Alarm Power Distribution" or "CCTV Power Distribution," this accurately reflects the MEP designer's role — power and containment only, with system design by a specialist.

### 🚨🚨 Specific Errors Repeatedly Made in This Session (Capture Them)

These are exact patterns from the conversation that triggered user corrections. Learn them to avoid repeating:

| What I incorrectly flagged as an MEP gap | Why it was wrong | The correct understanding |
|-----------------------------------------|-----------------|--------------------------|
| PAVA system design should be full MEP scope | PAVA is an audio system — AV specialist (Rawasin) handles it | MEP provides power distribution, containment, coordination only |
| Fire alarm detection design is missing from MEP scope | FA design exists in project drawing list, designed by specialist | MEP provides power distribution only to FA |
| CCTV full security design is missing | CCTV/security is specialist scope, not MEP | MEP provides power distribution only |
| ACS full design is missing | ACS is specialist scope, not MEP | MEP provides power distribution only |
| BMS network/control design is missing | BMS drawings exist in project LOD (separate section) | MEP provides electrical infrastructure only |
| ELV systems need expansion in MEP scope | ELV (intercom, MATV, AV containment) is specialist scope | Out of MEP design scope entirely |
| Telecom/IT needs CITC clause in MEP scope | Telecom is CITC subconsultant, separate from MEP | MEP provides power distribution only — telecom is NOT MEP design scope |
| FM200/clean agent needs a separate drawing | FM200 is part of firefighting system | No need to split — part of fire protection scope as-is |
| Gallery environmental conditions missing from scope | Covered by HAP load calculation deliverable | Already part of HVAC design, not a separate drawing |
| "Limited toilets" too narrow | This is intentionally limited | Correct as-is — do not expand |
| Kitchen hood suppression missing | This is kitchen/fire specialist scope | Not MEP scope |
| Fire extinguisher schedule missing | This is FLS specialist scope | Not MEP scope |
| External works coordination missing | Separate scope line item | Not MEP design scope |

**The recurring pattern:** If a system has a specialist contractor (check the numbered folders under `Subcontractors/`), MEP provides only power distribution, containment, and coordination — NOT system design. The drawing LOD may list drawings for that system under a specialist's code — that confirms the specialist is designing it. Do not double-claim MEP scope.

### Python technique

```python
def insert_paragraph_after(paragraph, text, italic=False, size=10, color=None):
    """Insert a paragraph after the given paragraph using oxml."""
    new_p_elem = deepcopy(paragraph._element.getparent().makeelement(qn('w:p'), {}))
    paragraph._element.addnext(new_p_elem)
    # ... formatting setup ...
    return new_para  # python-docx Paragraph object
```

Use grey italic text (`color='444444'`, `italic=True`, `size=9`) for supplementary paragraphs so they visually distinguish new scope additions from the original text.

### Workflow

1. Fix headings first (direct text replacement in runs)
2. Fix vague wording ONLY if user confirmed (direct text replacement)
3. Add supplementary paragraphs ONLY for definitively-MEP items
4. **End with verification** — re-read the document and check: "Am I adding scope that belongs to a specialist? If yes, remove it."
5. Save as `_COMPLIANT.docx`

## Variant: Drawing List (LOD) Audit

When the user provides a drawing list / LOD spreadsheet alongside the scope document — validate that the drawing register covers all scope items listed in the SOW/ER.

### Workflow

1. **Extract the drawing list** — open the Excel, iterate sheets (typically split by discipline: Mech LOD, Elec LOD, etc.)
2. **Map drawing codes to scope sections** — Verify each scope item has a corresponding drawing code:
   - HVAC items → HG (general), HD (detail), HR (riser), HS (schedule), VE (ventilation), AC (air conditioning), CH (chilled water), SM (smoke management)
   - Fire fighting → FF
   - Plumbing → PL (supply), SD (drainage — NOT FF!)
   - Power → EP
   - Panels → PD
   - BMS → BMS
   - Lighting → LS
   - Emergency lighting → EL
   - Fire alarm → FA
   - PAVA/PA → PA
   - Security/CCTV → CCTV (or similar unique code)
   - Access control → AC
   - Data/Telecom → DT (not PD)
   - Earthing/LP → EP
   - UPS → UP
3. **Flag duplicate drawing numbers** — Multiple systems sharing the same drawing number prefix (`PD-01` used by Panel Boards, Data, CCTV, ACS, LV cable routing, Earthing, UPS all at once) is a critical document-control issue
4. **Flag wrong codes** — Drainage drawings using `FF` (fire fighting) code is incorrect
5. **Flag missing drawings** — Scope items in SOW/ER without any corresponding drawing entry (clean agent FM200, kitchen suppression, fire extinguisher schedule, gallery environmental zone maps, cold room ventilation)
6. **Flag missing drawing numbers** — Items listed without a number assigned (SPL calculations, Lux calculation, facade lighting)
7. **Flag spelling errors** — "Vedio"→Video, "Adress"→Address, "Contral"→Control, "Daigram"→Diagram, "Eixt"→Exit, "Calaculations"→Calculations, "Mangement"→Management
8. **Annotate the Excel cell** with highlighted comments for each issue found, or provide structured findings list

### Critical check: Drawing number duplication

If the ELE LOD sheet maps Data systems, CCTV, ACS, LV Cable Routing, Earthing & Lightning Protection, and UPS all to `041-SIC-XX-ELEC-PD-01` through `-07` (same as Panel Boards), the drawing register is un-issuable. Each system must have a unique discipline code in the drawing number:

| System | Correct Code |
|--------|-------------|
| Panel Boards | PD |
| Data/Telecom | DT |
| CCTV | CCTV |
| Access Control | AC |
| Cable Routing | CR |
| Earthing/LP | EP |
| UPS | UP |

### Common drawing list pitfalls

- **Drainage using FF code** — The drainage section in Mech sheet often copies the fire fighting drawing number format (`041-SIC-XX-MECH-FF-01`). Should use `PL-SD` or similar drainage-specific code.
- **Calculations and schedules without numbers** — Items like "LUX CALCULATION", "Audio Coverage & SPL Calculations", "Fire Fighting Hydraulic Calculation" often appear as unnumbered rows — assign drawing numbers to these.
- **Section headers embedded in wrong section** — Section headers (e.g., "DATA SYSTEMS LIST OF DRAWING") may appear under the previous section's formatting, not as proper sheet section breaks in the Excel.
- **Section headers in wrong column** — In the revised `MOC-ASE-` numbering format, section headers may be in the Drawing No. column (Col 3) instead of the Description column (Col 2), because merged cells float the header text to a different column. Search both columns 2 AND 3 when scanning for section headers programmatically.
- **Drawing list existence ≠ MEP scope gap** — If a system has drawings listed in the project LOD under a non-MEP discipline code (e.g., `IT-TLC` for data, `IT-TFA` for CCTV, `IT-ACS` for ACS, `AV-TAV` for audio/video), this confirms a specialist IS designing that system. The MEP scope showing "Power Distribution only" for that system is CORRECT — do not flag as a gap. The LOD is evidence of the specialist's scope, not evidence that MEP should do more.