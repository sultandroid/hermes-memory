# CR Sheet Workflow — CG Comments → Response Register

## When to use
CG has reviewed a submission plan or deliverable and issued comments. The designer has responded via email. You need a structured Comment Response Register (CR Sheet) Excel to track resolution.

## Source extraction

### CG comments
- Usually a PDF attachment in the CG's email
- Extract with `pdftotext "/path/to/CG Comments.pdf" /tmp/cg_comments.txt`
- Group by discipline (Architecture, Structure, MEP, etc.) — CG often sends one PDF with multiple sections
- Structure comments may be included even though they're not the architectural designer's responsibility — still capture them as N/A

### Designer input
- Often embedded in an email reply chain (Outlook SQLite)
- Query: `SELECT m.Record_RecordID, substr(m.Message_Preview, 1, 500) FROM Mail m JOIN folders f ON m.Record_FolderID = f.Record_RecordID WHERE m.Message_NormalizedSubject LIKE '%keyword%' AND m.Message_SenderAddressList LIKE '%nissenrichards%'`
- For full body: use AppleScript `plain text content of message id <ID>`
- The response may be a multi-page PDF (the designer's reply forwarded as attachment) — extract with pdftotext
- Designer responses are often point-by-point, each addressing a specific CG comment

### Supporting documents
When the designer claims "already exists at Stage 3", verify by reading the referenced PDFs:
- `XX_BF_0006-Accessibility GA.pdf` — Stage 3 Accessibility drawing
- `XX_BF_0012-Wayfinding GA.pdf` — Stage 3 Wayfinding drawing
- `XX_BF_0008-MEWP Access GA.pdf` — Stage 3 Maintenance Access drawing
- `6930_Aseer_Accessibility.pdf` — Stage 3 Access, Maintenance & Accessibility report
- `6930_Aseer_Exhibit Schedule.pdf` — Stage 3 Exhibit Schedule

## CRITICAL: Response Voice Rules

**The CR Sheet speaks as the contractor (Samaya), not the designer (NRS).** This is the most common mistake.

- **No sub-consultant scope splits.** Never say "NRS scope" vs "Samaya scope" — everything is under Samaya. The CG does not need to know internal sub-consultant allocations.
- **No "our design scope covers" framing.** The contractor's scope covers everything. Items not yet developed are "to be coordinated and included in subsequent stages" not "outside our scope."
- **Items to be developed later:** Say "will be coordinated and included in subsequent stages from 50% to 90% to IFC. Supplier to be appointed." Do not say "outside NRS scope" or "being sourced by Samaya."
- **Items handled by specialists:** Say "will be provided under the relevant scope, coordinated with the [specialist name] specialist." Do not say "by others" or "outside NRS scope."
- **Items already covered by Stage 3:** Say "was defined and approved at Stage 3. The existing Stage 3 document already addresses this. To be confirmed with CG whether sufficient." Do not say "NRS confirms" or "NRS position."
- **Column header:** Use "Response" not "Designer Response" or "NRS Response."
- **Designer input is raw material only.** Extract the designer's technical position from their email, then rephrase it as the contractor's response. The designer's frustration ("this is pointless", "not what RIBA defines") stays in the source — do not carry it into the CR Sheet.

## CR Sheet structure (openpyxl)

### Sheet 1: CR Register

| Column | Content | Notes |
|--------|---------|-------|
| CR # | CR-01, CR-02, ... | Sequential |
| CG Comment | Full text of the CG comment | Verbatim from PDF |
| CG Reference | Source reference | e.g. "CG Comment 1 (Architecture) - 27 Jun 2026" |
| Response | Contractor's response | Rephrased from designer input — speaks as Samaya |
| Position | One-line summary | e.g. "Already covered by Stage 3" |
| Status | Classification | See below |
| Action Required | What needs to happen | Specific steps |
| Supporting Documents | Referenced docs | Drawing numbers, PDF names |

### Status classification

| Status | Meaning | Color |
|--------|---------|-------|
| Acknowledged | Comment noted, no further action | Blue (#D6E4F0) |
| Already covered by Stage 3 | Existing approved documents address the comment | Yellow (#FFF2CC) |
| To be included in subsequent stages | Item will be developed from 50% to 90% to IFC | Yellow (#FFF2CC) |
| To be provided under relevant scope | Belongs to another discipline/specialist | Red (#FCE4EC) |
| N/A | Comment belongs to another discipline | Grey (#F2F2F2) |

### Staging Pattern for Items Not Yet Developed

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

### Simple Acceptance Pattern

When a CG comment is straightforward and accepted without debate:

- Response: `"Noted. [Specific action] to be prepared."`
- Position: `"Accepted"`
- Status: `"Accepted"`
- Open/Closed: `"Closed"` (green)
- Action Required: The specific action to take

Example: CR-07 (Rigging register) → "Noted. Separate submittal register for rigging works to be prepared."

### Cross-Referencing Structural Registers

When structural CG comments reference existing registers (Structural Submittal Register, Consultant Comment Register):

1. Read both registers to extract the actual status and response
2. Update the CR Sheet response to reflect the register data
3. Reference the register file name in Supporting Documents (without parenthetical notes)
4. For comments already in progress (core testing, geotechnical), set Open/Closed to "Open" with red fill
5. For comments accepted without debate, set to "Closed" with green fill

### Sheet 2: Summary
- Date generated, project name, CG reference
- Status breakdown counts
- Key positions (bulleted)
- Recommended next steps (numbered)

## openpyxl patterns

```python
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

wb = Workbook()
ws = wb.active
ws.title = "CR Sheet"

# Styles
header_font = Font(name='Calibri', bold=True, size=11, color='FFFFFF')
header_fill = PatternFill(start_color='1F3864', end_color='1F3864', fill_type='solid')
body_font = Font(name='Calibri', size=10)
wrap_align = Alignment(wrap_text=True, vertical='top')
thin_border = Border(
    left=Side(style='thin'), right=Side(style='thin'),
    top=Side(style='thin'), bottom=Side(style='thin')
)

# Status fills
status_fills = {
    'Partial': PatternFill(start_color='FFF2CC', end_color='FFF2CC', fill_type='solid'),
    'Not part': PatternFill(start_color='FCE4EC', end_color='FCE4EC', fill_type='solid'),
    'Acknowledged': PatternFill(start_color='D6E4F0', end_color='D6E4F0', fill_type='solid'),
    'N/A': PatternFill(start_color='F2F2F2', end_color='F2F2F2', fill_type='solid'),
}

# Write headers
for col, h in enumerate(headers, 1):
    cell = ws.cell(row=1, column=col, value=h)
    cell.font = header_font
    cell.fill = header_fill
    cell.alignment = Alignment(wrap_text=True, vertical='center', horizontal='center')
    cell.border = thin_border

# Write rows with status coloring
for r, row_data in enumerate(rows, 2):
    for c, val in enumerate(row_data, 1):
        cell = ws.cell(row=r, column=c, value=val)
        cell.font = body_font
        cell.alignment = wrap_align
        cell.border = thin_border
    # Color status column
    status_cell = ws.cell(row=r, column=6)
    for key, fill in status_fills.items():
        if key in str(status_cell.value):
            status_cell.fill = fill
            break
```

## Splitting a Submittal Register into a Separate Register

When CG asks for a separate submittal register for a specialized scope (e.g., Rigging Systems per CR-07):

1. **Extract the relevant rows** from the main register — both DD and IFC sections
2. **Create a new workbook** with the same column structure and header styling
3. **Add a title row** explaining the purpose
4. **Add section headers** for DD and IFC groups
5. **Remove the rows from the main register** — but first unmerge any merged cells that overlap those rows
6. **Add reference notes** in the main register pointing to the new file
7. **Save both files**

### openpyxl pattern for unmerging and clearing

```python
for merge_range in list(ws.merged_cells.ranges):
    for r in range(start_row, end_row + 1):
        if merge_range.min_row <= r <= merge_range.max_row:
            ws.unmerge_cells(str(merge_range))
            break

for row in range(start_row, end_row + 1):
    for col in range(1, max_col + 1):
        try:
            ws.cell(row=row, column=col).value = None
        except:
            pass

ws.cell(row=start_row, column=1).value = 'Scope — See separate Register'
ws.cell(row=start_row, column=1).font = Font(name='Calibri', bold=True, italic=True, size=10, color='1F3864')
```

### Closing a CR When Designer Provides Drafts After Pushback

When the designer initially disagrees with a CG comment ("not Stage 4 scope", "already exists") but then prepares draft drawings anyway:

1. **Update the CR to reflect the actual outcome**, not the initial position
2. Change status from "Partial - needs CG confirmation" to "Closed - draft submitted"
3. List the actual drawing numbers in Supporting Documents
4. Keep Action Required focused on what remains (e.g., "Update title sheet and submit final")
5. The designer's frustration or pushback language stays in the source email — do not carry it into the CR Sheet

### Template Preservation When Editing Existing Registers

When editing an existing Excel register (not creating from scratch):

1. **Only modify the specific cells/rows needed.** Do not rebuild the file from scratch.
2. **Unmerge merged cells** in the affected rows before clearing values — use `ws.unmerge_cells(str(merge_range))` after iterating `ws.merged_cells.ranges`
3. **Preserve all original formatting** — header styles, column widths, merged cells in unaffected rows, section colors, borders, fonts
4. **Add reference notes as plain text** in the first column of cleared rows. Do not apply special formatting.
5. **Verify** by re-reading the file after saving to confirm only intended changes were made.

### Cross-Referencing Between Registers

When multiple registers exist for the same project:

1. **Read all relevant registers** before writing responses. The Consultant Comment Register may contain detailed responses that should inform the CR Sheet.
2. **Reference file names only** in the Supporting Documents column — no parenthetical internal notes
3. **Put specific references** (comment numbers, section references) in the Action Required column instead
4. **Update all registers** when a CR status changes — the CR Sheet, submission plan, and discipline-specific register should all reflect the same status

## Pitfalls
- CG comments PDF may contain both Architecture and Structure comments in one file — separate them
- Designer responses may be in a PDF attachment (forwarded email) rather than inline in the email body
- Always verify "already exists" claims by reading the referenced documents — don't take the designer's word alone
- Some CRs are N/A for the architectural designer but still need to be tracked for other parties
- Dates in submission plan Excel may be serial numbers (Excel date format) — convert with `datetime.fromordinal(datetime(1900, 1, 1).toordinal() + serial - 2)`
- The modified submission plan may have duplicate rows (same item repeated across floors) — deduplicate when building the CR Sheet
- **Most common mistake: writing the response from the designer's perspective instead of the contractor's.** Always rephrase. The CG sees one contractor, not a collection of sub-consultants.
