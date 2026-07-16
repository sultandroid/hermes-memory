---
name: consultant-comment-response
description: Handling consultant review comments on submittals.
---

# Consultant Comment Response

## Overview
Handling consultant review comments on submittals: extracting comments from PDFs, mapping to responsible parties via RACI, drafting internal action assignment emails and external reply emails to the consultant. Covers the full workflow from PDF extraction to email composition.

## Workflow
1. **Extract comments** from the PDF using `pdftotext -layout`
2. **Read the RACI matrix** (Excel) to understand party responsibilities
3. **Map each comment** to the responsible party and determine status
4. **Draft internal email** assigning actions to each party with deadlines
5. **Draft external reply** to the consultant with a table of responses

## Extended Workflow: CG Schedule/Register Processing

When CG sends an Excel/PDF schedule (object schedule, drawing register, submission plan):

1. **Extract & map** — Use `openpyxl` for Excel, `pdftotext -layout` for PDFs. Build a clean object-to-showcase mapping table
2. **Version comparison** — Compare against the previous version. Identify new, removed, reassigned, split, and unassigned items
3. **Gap analysis** — Check which galleries/areas have complete mapping vs missing. Flag contradictory notes, missing dimensions, color coding violations
4. **Multi-party routing** — Draft ONE email with a responsibility table (NRS / Glasbau Hahn / Structural Engineer)
5. **Decide whether to query CG** — If entire galleries are missing assignments, query CG before routing. If minor TBCs, proceed and flag
6. **Handle designer pushback** — NRS will flag inconsistencies, request curator meetings, and claim additional fees. Forward to CG, support the fee claim

See `references/cg-schedule-processing.md` for the full workflow with templates and pitfalls.

## Key Files
- `templates/internal-action-email.md` — Template for internal action assignment
- `templates/external-reply-email.md` — Template for external reply to consultant
- `references/comment-extraction-technique.md` — Detailed technique for extracting and mapping comments
- `references/cg-schedule-processing.md` — Processing CG Excel/PDF schedules (object schedules, drawing registers): extraction, version comparison, gap analysis, multi-party routing, handling designer pushback
- `references/design-study-handling.md` — Handling NRS Design Study submissions with cost notifications and team assignment templates

## Extended Workflow: CR Sheet (Comment Response Register) Excel

When the task is to produce a structured CR Sheet mapping consultant comments to responses:

1. **Extract CG comments** — `pdftotext` the CG review PDF. Read the full text. Group by discipline (Architecture, Structure, MEP, etc.)
2. **Extract designer input** — Pull from email (Outlook SQLite + AppleScript for full body) or from a response PDF. The designer's email often contains point-by-point responses embedded in the reply chain
3. **Read supporting documents** — Before accepting or rejecting a claim, read the referenced drawings/documents. The designer may claim "already exists at Stage 3" — verify by reading the actual Stage 3 PDFs
4. **Build the CR Sheet** — Use `openpyxl` to create a 2-sheet workbook:
   - **Sheet 1: CR Register** — Columns: CR#, CG Comment, CG Reference, Response, Position, Status, Action Required, Supporting Documents
   - **Sheet 2: Summary** — Status breakdown, key positions, recommended next steps
5. **Status classification** — Use these categories:
   - **Acknowledged** — comment noted, no further action
   - **Already covered by Stage 3** — existing approved documents address the comment
   - **To be included in subsequent stages** — item will be developed from 50% to 90% to IFC
   - **To be provided under relevant scope** — belongs to another discipline/specialist
   - **N/A** — comment belongs to another discipline
6. **Color coding** — Yellow=Partial, Red=Not part of this submission, Blue=Acknowledged, Grey=N/A
7. **Cross-reference verification** — When designer says "already exists at Stage 3", verify by reading the referenced PDFs. Note the drawing numbers and document titles in the Supporting Documents column
8. **Propose next steps** — For each CR, state what needs to happen: confirm with CG, coordinate with specialist, appoint supplier, etc.

### CRITICAL: Response Voice Rules

**The CR Sheet speaks as the contractor (Samaya), not the designer (NRS).** This is the most common mistake. Follow these rules:

- **No sub-consultant scope splits.** Never say "NRS scope" vs "Samaya scope" — everything is under Samaya. The CG does not need to know internal sub-consultant allocations.
- **No "our design scope covers" framing.** The contractor's scope covers everything. Items not yet developed are "to be coordinated and included in subsequent stages" not "outside our scope."
- **Items to be developed later:** Say "will be coordinated and included in subsequent stages from 50% to 90% to IFC. Supplier to be appointed." Do not say "outside NRS scope" or "being sourced by Samaya."
- **Items handled by specialists:** Say "will be provided under the relevant scope, coordinated with the [specialist name] specialist." Do not say "by others" or "outside NRS scope."
- **Items already covered by Stage 3:** Say "was defined and approved at Stage 3. The existing Stage 3 document already addresses this. To be confirmed with CG whether sufficient." Do not say "NRS confirms" or "NRS position."
- **Column header:** Use "Response" not "Designer Response" or "NRS Response."
- **Designer input is raw material only.** Extract the designer's technical position from their email, then rephrase it as the contractor's response. The designer's frustration ("this is pointless", "not what RIBA defines") stays in the source — do not carry it into the CR Sheet.

### CRITICAL: No AI Fingerprints in CR Sheets

The user explicitly rejects any machine-generated formatting. Follow these rules strictly:

- **No emoji anywhere.** Not in status columns, not in summaries, not in legends. Use plain text: CLOSED, OPEN, PARTIAL, REQUESTED.
- **No special/unicode characters.** Replace all:
  - Em-dash (U+2014) -> plain hyphen
  - En-dash (U+2013) -> plain hyphen
  - Arrow (U+2192) -> plain >
  - Bullet (U+2022) -> plain -
  - Section symbol -> remove
  - Smart quotes -> straight quotes
  - Multiplication sign (U+00D7) -> lowercase x
- **No AI-sounding phrasing.** Avoid: "demonstrates full compliance", "globally recognised", "museum-grade", "well-known manufacturer". Use plain engineer language: "meets spec", "datasheet attached", "submitted per schedule".
- **No ALL-CAPS for emphasis.** Dont write SEPARATE, NOW, IN PROGRESS, LOOK AND FEEL. Use normal sentence case.
- **No does NOT depend or is NOT a blocker.** Use lowercase: does not depend, is not a blocker.
- **No spaced hyphens used as em-dash substitutes mid-sentence.** Use commas instead.
- **No dot as bullet separator in summary lines.** Use semicolons or plain commas.
- **Status labels only:** CLOSED, OPEN, PARTIAL, REQUESTED. No emoji prefixes, no colored dots.
- **Verify before delivering.** Run a hex check: scan all cell values for any character with ord(c) > 127. If any found, replace them before saving.

### CR Sheet: Stating Facts vs Claiming Closure

When a CG comment references a related document or instruction (e.g. SI-007, a previous submittal):

- **Do NOT claim the referenced item is closed or resolved** unless CG explicitly stamped it closed. The CR Sheet is not the authority on other documents status.
- **Do state the facts:** what was submitted, when, and what CGs response was (if any).
- **Example (wrong):** "SI-007 was closed at SI level on 27-Apr-2026 (R1)."
- **Example (right):** "3D render (ZD-0033 Rev.01) and material board (ZD-0030 Rev.01) already submitted and approved by CG."
- **The CR Sheet addresses the specific comment only.** Dont expand into other documents lifecycle status. If CG wants to know SI-007 status, they will ask separately.

### CR Sheet: Compact to One Page

- **Row heights:** 50px max per row. No verbose paragraphs.
- **Column widths:** Tight. 35 chars for response column, 18 for status/remarks.
- **Content:** Short sentences. One idea per cell. No multi-paragraph responses.
- **Fit to page:** Set ws.page_setup.fitToWidth = 1 and ws.page_setup.orientation = landscape.
- **Summary line:** One line at bottom, no line breaks. Use semicolons as separators.

### CR Sheet: Email Thread References

- **Do NOT include .txt files** of email threads in the support folder.
- **Reference emails by date and sender only** in the CR Sheet cells. E.g. "Glasbau Hahn reply 29-Apr-2026" or "NRS Jim Richards 19-Jun-2026".
- If the user wants the email content preserved, print the email to PDF from Outlook and include the PDF, not a .txt file.

### Submission Plan vs CR Sheet — Separation of Concerns

**Critical distinction:** The submission plan and the CR sheet serve different purposes and must NOT mix content:

| Document | Purpose | Content |
|----------|---------|---------|
| **Submission Plan** | Forward schedule — what we will submit and when | Deliverable name, brief description, responsibility, planned date, status. No explanations, no Stage 3 references, no commentary. |
| **CR Sheet** | Response to CG comments — positions, explanations, evidence | Full response text, position statement, status, action required, supporting documents. |

**Submission Plan description rules:**
- State only the deliverable: "Scenography drawing showing showcase locations, circulation paths, and key interaction points."
- Do NOT add: "Completed at Stage 3. NRS draft included in submission plan." — that belongs in the CR Sheet
- Do NOT add: "Wayfinding discrepancies flagged by NRS to be resolved." — that belongs in the CR Sheet
- Do NOT add: "FF and E supplier to be appointed. To be included from 50% to 90% to IFC stages." — keep it as "FF and E layout plan."
- Remarks column: use only for scheduling notes (e.g., "FF and E supplier to be appointed"), not for commentary

**CR Sheet description rules:**
- Full response: "This was completed at Stage 3. NRS prepared a draft copy (MOC-...) for reference. Will be included in the submission plan and drawing register."
- Action required: "Include in submission plan and drawing register"
- Supporting documents: List the actual file names

### Staging Pattern for Items Not Yet Developed

When CG asks for items that were not in the original submission plan:

| Item Type | Response Pattern |
|-----------|-----------------|
| FF&E layouts | "Will be coordinated and included in subsequent stages from 50% to 90% to IFC. Supplier to be appointed." |
| Signage/Graphics | "Included in the 50% gate. Will be submitted separately, coordinated with the signage and graphics specialist." |
| Life Safety | "Will be provided under the relevant scope, coordinated with the Life Safety specialist." |
| Structural items | "To be included as part of the structural submission." |
| Simple acceptance | "Noted. [Action] to be prepared." — Status: Accepted |

### Open/Closed/Noted Status Column

After building the CR Sheet, add a status column with three values:

| Status | Meaning | Color |
|--------|---------|-------|
| **Open** | Action pending — supplier to be appointed, specialist to coordinate, information pending | Red (#FCE4EC) |
| **Closed** | Resolved — draft submitted, CG confirmed, item accepted | Green (#E2EFDA) |
| **Noted** | Acknowledged — process requirement, no further action | Blue (#D6E4F0) |

Insert this column between the Status column and Action Required column. Use `ws.insert_cols(7)` to shift existing columns right.

### Supporting Documents Column Rules

- List only file names and paths — no parenthetical internal notes
- Wrong: `Consultant_Comment_Register_Revised.xlsx (Comment 3)`
- Right: `Consultant_Comment_Register_Revised.xlsx`
- If a document reference is internal (e.g., a specific comment number), put it in the Action Required column instead
- Use `N/A` when no supporting document exists

### Cross-Referencing Between Registers

When multiple registers exist for the same project (CR Sheet, Consultant Comment Register, Structural Submittal Register, etc.):

1. **Read all relevant registers** before writing responses. The Consultant Comment Register may contain detailed responses that should inform the CR Sheet.
2. **Reference file names only** in the Supporting Documents column — no parenthetical internal notes (e.g. use `Consultant_Comment_Register_Revised.xlsx` not `Consultant_Comment_Register_Revised.xlsx (Comment 3)`).
3. **Put specific references** (comment numbers, section references) in the Action Required column instead.
4. **Update all registers** when a CR status changes — the CR Sheet, submission plan, and discipline-specific register should all reflect the same status.

### Register Split Pattern (Specialized Scope)

When CG requests a separate register for a specialized scope (e.g., rigging systems):

1. **Create a new register file** — Extract the relevant rows from the main register into a new workbook with its own title and section headers.
2. **Reference in the main register** — Replace the extracted rows with a single reference note: `"[Scope] — See separate [Register Name]"`
3. **Preserve template formatting** — Only clear the specific rows being moved. Do NOT rebuild the entire workbook. Unmerge any merged cells in those rows first, then clear cell values. Leave all other formatting, merged cells, colors, and styles untouched.
4. **Name the new file** consistently — `[Discipline]_Submittal_Register/[Scope]_Submittal_Register.xlsx`

### Template Preservation Rule

When editing an existing Excel register or submission plan:

- **Only modify the specific cells/rows needed.** Do not rebuild the file from scratch.
- **Unmerge merged cells** in the affected rows before clearing values.
- **Preserve all original formatting** — header styles, column widths, merged cells in unaffected rows, section colors, borders.
- **Add reference notes as plain text** in the first column of cleared rows. Do not apply special formatting to these notes.
- **Verify** by re-reading the file after saving to confirm only intended changes were made.

### Closing a CR When Designer Provides Drafts

When the designer initially pushes back on a CG comment but then prepares draft drawings anyway:

- **Update the CR to reflect the actual outcome**, not the initial position.
- Change status from "Partial - needs CG confirmation" to "Closed - draft submitted"
- List the actual drawing numbers in Supporting Documents
- Keep the Action Required focused on what remains (e.g., "Update title sheet and submit final")
- The designer's frustration or pushback language stays in the source email — do not carry it into the CR Sheet

### Simple Acceptance Pattern

When a CG comment is straightforward and accepted without debate:

- Response: `"Noted. [Specific action] to be prepared."`
- Position: `"Accepted"`
- Status: `"Accepted"`
- Open/Closed: `"Closed"` (green)
- Action Required: The specific action to take

Example: CR-07 (Rigging register) → "Noted. Separate submittal register for rigging works to be prepared."

See `references/cr-sheet-workflow.md` for the complete technique with openpyxl patterns and status classification rules.

## Extended Workflow: MAR Compliance Sheet Resubmission

When the consultant returns a **Code C (Revise and Resubmit)** on a Material Approval Request (MAR) with comments about the compliance sheet:

### The Core Rule: Achieved Values + Test Report References

The most common and critical CG comment on MARs is: **"Compliance sheet shall include the achieved values and the corresponding test report references."**

This means:
- **Status markers are NOT acceptable.** Do not use "Partial", "Gap", "Supported", "Compliant", or any qualitative status in the compliance column.
- **Every row must have an actual number** — density in kg/m³, modulus in MPa/N/mm², thickness in mm, moisture content in %, flame spread index, formaldehyde emission class, etc.
- **Every value must cite a source** — the exact file name and page/section of the datasheet, test report, or certificate that proves it.

### Compliance Sheet Structure

| Column | Content | Example |
|--------|---------|---------|
| Spec Clause | Exact clause reference | 061000 2.1.A |
| Parameter | What is being measured | Density (air-dry) |
| Required Value | From the spec | ≥ 640 kg/m³ |
| Achieved Value | From the datasheet | 680 kg/m³ |
| Test Standard | ASTM/BS/EN ref | ASTM D2395 |
| Source Reference | File name + page | Garnica_Duraply_TDS.pdf p.3 |
| Compliance | ✓ or ✗ only | ✓ |

### Workflow

1. **Extract spec requirements** — `pdftotext` the spec PDFs (e.g., 061000, 064023). List every clause with a numerical requirement: density, modulus, thickness, moisture content, fire rating, formaldehyde emission, screw withdrawal, etc.
2. **Extract achieved values** — `pdftotext` every datasheet PDF in the submission. Build a table of Manufacturer → Product → Parameter → Achieved Value → Test Standard → Source File.
3. **Cross-reference** — For each spec clause, find the matching achieved value from the datasheets. If no datasheet covers a required parameter, that's a real gap to flag.
4. **Build the compliance sheet** — One row per spec clause. Every row has a number in the Achieved Value column and a file reference in the Source column.
5. **Update the MAR checklist** — Items that were "No" or "N/A" should be upgraded to "Yes" once the evidence is in place.

### Common Gaps Found in Practice

| Gap | What's Needed |
|-----|--------------|
| Fire test report | Product TDS is NOT a fire test report. Need a lab report (UL, Intertek, Warringtonfire) explicitly stating Class A flame spread (≤ 25) and smoke developed (≤ 450) per ASTM E84 or equivalent. |
| Metal component datasheets | Blum hinges/runners alone are not enough. Need datasheets for ALL metal: brackets, anchors, screws, tracks, connectors, fasteners. |
| Adhesive TDS | Brand-family evidence is not enough. Need the exact product TDS showing EN 204 D3 or ASTM D4317 Type II compliance. |
| Hardware schedule | No itemized project hardware schedule = gap. Need a schedule listing every handle, lock, hinge, runner, and fixing with model numbers. |
| Shop drawings | Approved shop drawings showing framing, furring, locations, dimensions, and attachments. |

### Pitfalls (MAR-specific)
- **"Compliant" is not a value.** The engineer will reject any compliance sheet that uses words instead of numbers.
- **Product TDS ≠ test report.** A manufacturer datasheet states design values; a test report from a recognized lab proves actual performance. Fire ratings especially need the latter.
- **Partial compliance = non-compliance.** If even one clause lacks a verified achieved value, the whole submission gets Code C.
- **Metal components are often forgotten.** The spec requires all metal to have datasheets — not just the branded hardware (Blum) but also generic brackets, screws, and anchors.
- **Check the MAR checklist too.** The consultant's checklist items (Testing, Certifications, Method Statement) must all be upgraded to "Yes" with evidence, not left as "No" or "N/A".
- **"Not just noted" — the engineer wants numbers.** When the engineer says "achieved values shall be clearly reflected", they mean actual numerical values in every row. Status markers like "Partial" or "Supported" are not acceptable. Every row must have a number (kg/m³, MPa, mm, %) and a source file reference.
- **EN vs ASTM fire standards need bridging.** Greenlam/Garnica provide EN 13501-1 B-s1,d0 (European Class A equivalent) but the spec calls for ASTM E84. A cross-reference letter or direct ASTM E84 test report from the manufacturer is needed — don't assume the engineer will accept the EN classification without explanation.
- **Blum/Henkel catalogs don't state BHMA/EN grades explicitly.** Blum catalogs show load capacities and cycle durability but not BHMA A156.9 Grade 1. Henkel TDSs show viscosity and lap shear but not EN 204 D3. A manufacturer declaration letter is needed for each — don't assume the catalog data alone satisfies the spec.
- **Consolidate evidence into one folder.** Create `10_Compliance_Evidence/` with subfolders `Datasheets/` (organized by manufacturer) and `Certificates/`. Update all file references in the compliance sheet and MAR checklist to point to this consolidated folder. This makes the resubmission package self-contained and easy for the engineer to audit.

### Subcontractor Compliance Sheet — Fill the Engineer's Form, Do Not Create a New One

When you are a subcontractor responding to a Code C on a MAR, the Engineer wants you to fill their existing compliance template, not create a new one from scratch. The user will correct you if you create a new file: "he said just fill my form only."

#### Workflow

1. **Use the Engineer's own compliance format.** The Engineer provides an Excel template with spec text already written in. It has columns: No., Section, Specifications, Manufacturer/Supplier Statement, Compliance, Remarks. Only fill the last three columns. Do not modify the spec text, section numbering, header rows, signature blocks, or merged cells.

2. **Only fill material data rows, not company data rows.** As a subcontractor, your compliance sheet addresses only material-specific spec clauses:
   - MDF physical properties (density, MOR, MOE, IB, swelling, screw holding)
   - Fire ratings (flame spread, smoke developed)
   - Formaldehyde emissions (NAUF, CARB, E1)
   - Hardware (hinges, slides — BHMA compliance)
   - Adhesives (EN 204 D3, UF-free)
   - Plywood/panel products (BS EN 636, marine grade)
   - Coatings/finishes (fire retardant, VOC)

   Do NOT fill rows for company-level items:
   - Fabricator qualifications (years of experience)
   - Installer qualifications
   - Warranty periods
   - Installation tolerances
   - Product data submittals (1.3.A)
   - Product certificates (1.3.E)
   - Environmental limitations

   These are the main contractor's responsibility. The user will correct you: "only fill the materials data not company data."

3. **Evidence in Remarks column.** Every filled row must have a source reference in the Remarks column — the exact file name of the datasheet, test report, or certificate that supports the achieved value. Do not leave Remarks empty. The user will correct you: "add in Remarks the evidence of the comply, not just tell comply."

4. **No subcontractor datasheets for main contractor items.** The main contractor provides their own company certificates (ISO, CR, VAT, GOSI, Saudization) and general submittal documents. The subcontractor only provides their own material datasheets and test reports. The user will correct you: "no need to add Ola paper because we are subcontractor and the main contractor will add his papers."

5. **Keep the Engineer's original structure intact.** The Engineer's Excel has merged cells, signature rows, and section headers. Only fill the Manufacturer Statement, Compliance, and Remarks columns. Do not modify the spec text, section numbering, header rows, or signature blocks. Preserve all original formatting.

6. **No symbols or AI fingerprints in compliance sheets.** Use plain text status labels: "Compliant", "Partial", "Pending". No emoji, no checkmarks, no unicode symbols. Remarks should reference file names directly — no AI-sounding phrases like "demonstrates full compliance" or "exceeds minimum by 20%". Write like an engineer: "Verdo FR MDF TDS - Density 800.80 kg/m3".

## Forwarding CG Comments to Designers (Pre-CR-Sheet Routing)

Before building the CR Sheet, CG comments often need to be **filtered and forwarded to the designer** (NRS, AD Engineering, etc.) for their input. This is a distinct workflow step.

### Workflow

1. **Read the full CRS** — Extract all comments from the CG's Excel/PDF
2. **Map each comment to a party** — Use the scope split, not assumptions:
   - **Designer scope** (NRS): Drawing content, title blocks, QA notes, sheet layout standards, dimensions, room names, section details, showcase design, finishes schedule format, material specifications
   - **Contractor scope** (Samaya): Cloud survey, demolition methodology, mock-ups, material samples, BIM coordination, subcontractor appointments, site logistics
   - **Specialist scope**: Graphic housing, AV, lighting (ZNA), life safety — route to the relevant specialist
3. **Verify responsibility from past emails** — Before assigning a comment to a party, check Outlook for prior correspondence on the same topic. The designer may have already addressed it or pushed back. Use `Conversation_ConversationID` to find the full thread.
4. **Draft a filtered email** — Only include items that belong to the designer. Do NOT dump the entire CRS on them.

### What Belongs to the Designer

The designer produces the drawings, so these are on them:
- Title block content (dates, revision schedule, drawing numbers, reviewer names)
- QA notes and sheet layout standards compliance
- Missing dimensions, room/space names on sections
- Showcase design details (opening mechanisms, finishes, dimensions)
- Finishes schedule format and content
- Space labeling (FFL, CIL, space codes)

### What Belongs to the Contractor

These are Samaya/contractor responsibilities:
- Cloud survey (pending — note it in the email for context)
- Demolition methodology and ceiling removal clarification
- On-site mock-ups and material samples
- BIM coordination and clash resolution
- Subcontractor appointments (Glasbau Hahn, etc.)
- Site logistics and access

### Email Structure to Designer

```
Subject: NRS Input Required — [SUBMITTAL REF] CRS ([FLOOR] Only)

Dear [Name],

CG returned the CRS for the [Floor] [Discipline] DD submittal (overall C).
We are preparing our response and will address the items on our side
([list contractor-side items]) directly with CG.

The following items need [Designer] design input:

[Section Heading (Reviewer Name)]:
- #[N] — [Brief description of comment]
- #[N] — [Brief description of comment]

Please review and advise so we can prepare the resubmission.

Regards,
[Name]
```

### Key Rules

- **Mention pending contractor items** (cloud survey, etc.) in one line so the designer knows the context — but don't list them as action items for the designer
- **Check past emails** before assigning — the designer may have already responded to a similar comment in a previous round
- **Name the floor** in the subject — CG often reviews one floor at a time
- **Group by reviewer** (Eng. Maged Zamzam, Eng. Islam Mostafa, Eng. Abdrabo) for clarity
- **Keep it short** — the designer doesn't need to see all 89 comments, only their ~15-20

### CRS Item Mapping — Designer vs Contractor

Before forwarding, map each CRS item to the correct party. Do NOT dump the entire CRS on the designer.

**Designer (NRS) scope — send to NRS:**
- Title block content (dates, revision schedule, drawing numbers, reviewer names)
- QA notes and sheet layout standards compliance
- Missing dimensions, room/space names on sections
- Showcase design details (opening mechanisms, finishes, dimensions, perspective views)
- Finishes schedule format and content
- Space labeling (FFL, CIL, space codes)
- Expansion joint detailing in finishes
- Stairs solution and finishes

**Contractor (Samaya) scope — handle internally:**
- Cloud survey (pending — note in email for context only)
- Audit report coordination
- On-site mock-ups and material samples
- BIM coordination and clash resolution
- Demolition methodology and ceiling removal clarification
- Subcontractor appointments (Glasbau Hahn, etc.)
- Site logistics and access
- Shop drawings for doors/stairs (contractor to produce from design intent)

**Specialist scope — route separately:**
- Graphic housing — route to signage/graphics specialist
- AV coordination — route to AV specialist (Rawasin)
- Lighting — route to ZNA
- Life safety — route to life safety specialist

### Floor Verification Step

Before forwarding, verify which floor(s) the CRS covers:

1. Check the document title in the CRS header (row 7-8 of the Excel)
2. Check drawing number prefixes in the Sheet column:
   - `BF` = Basement Floor
   - `LG` = Lower Ground
   - `GF` = Ground Floor
   - `GEN` = General (cross-floor)
3. If all drawing numbers use one prefix, the CRS covers that floor only
4. Name the correct floor in the email subject line

## Pitfalls
- PDFs can be very large (>100k lines); use `pdftotext -layout` and read in chunks
- Comments may have inline status markers like "OK", "OK - comply with Ad.", "OK - Update in DL" — these need careful parsing
- The RACI matrix defines who is responsible for what; always consult it before assigning actions
- Some comments are duplicates ("Same comment #N") — handle by referencing the original
- Always include a table in the external reply for clarity
- Deadlines should be realistic (typically 5-7 working days for resubmission)
- **Don't assume scope split** — title blocks, QA notes, and sheet layout standards are on the designer (they produce the drawings), not the contractor. Cloud survey is on the contractor, not the designer. Verify from past emails before assigning.
- **Name the floor** in the subject line — CG often reviews one floor at a time. Check drawing number prefixes (BF, LG, GF) to confirm which floor the CRS covers.

## User Preferences (Mohamed Sultan Abbas)
- Formal, professional tone in both internal and external communications
- Arabic/English bilingual headers in submittal documents (preserve original formatting)
- Prefers detailed action tables with clear party assignments
- Wants "In Progress" vs "Closed" status clearly distinguished
- Expects all comments to be addressed even if just "Noted — no further action"
- Uses specific terminology: "CG" for consultant, "AD" for MEP designer, "DL" for drawing list
- Prefers deadlines to be explicit (date-specific, not relative)
- Attachments should be listed at the end of external replies
- **Single consolidated email** — when routing to multiple parties (NRS, GBH, Structural), send ONE email with a responsibility table, not separate emails per party
- **Check SOW yourself** — before asking a subcontractor if something is in their scope, check their SOW/contract first. Only ask them for timeline/dates, not scope confirmation
- **Don't debate scope in the routing email** — when forwarding CG comments, just state the comment and ask for proposed dates. Don't ask "is this in your scope?" — that's your job to determine from the contract
- **Direct action framing** — emails to subs should say "please review and suggest dates" not "please confirm if this is in your scope"
