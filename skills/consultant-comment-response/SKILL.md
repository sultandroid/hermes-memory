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

## Pitfalls
- PDFs can be very large (>100k lines); use `pdftotext -layout` and read in chunks
- Comments may have inline status markers like "OK", "OK - comply with Ad.", "OK - Update in DL" — these need careful parsing
- The RACI matrix defines who is responsible for what; always consult it before assigning actions
- Some comments are duplicates ("Same comment #N") — handle by referencing the original
- Always include a table in the external reply for clarity
- Deadlines should be realistic (typically 5-7 working days for resubmission)

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
