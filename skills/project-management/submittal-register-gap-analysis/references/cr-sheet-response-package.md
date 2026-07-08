# CR Sheet & Response Package Workflow

## When to Use
CG issues comments on a submission plan → you need to track responses, update registers, and package everything for submission.

## Step 1: Build the CR Sheet

Create an Excel workbook with these columns:

| Column | Content |
|--------|---------|
| CR | Sequential number (CR-01, CR-02...) |
| CG Comment | Verbatim text of the consultant's comment |
| CG Reference | Source document + date |
| Response | Samaya's response (NOT the designer's internal position) |
| Position | Short classification (Accepted / Already covered / To be included later / N/A) |
| Status | Detailed status text |
| Open / Closed | Open / Closed / Noted (color-coded: green=Closed, red=Open, blue=Noted) |
| Action Required | What needs to happen next |
| Supporting Documents | File references |

### Response Voice Rules

- **Samaya is the contractor.** All responses are from Samaya's perspective. Do NOT say "NRS scope" or "AV Designer scope" — CG sees everything as Samaya.
- **No internal sub-consultant splits.** If a designer (NRS, ZNA, etc.) provides input, report it as information received, not as a scope boundary.
- **Items to be included later** → "will be coordinated and included in subsequent stages from 50% to 90% to IFC. [Specialist] to be appointed."
- **Items already covered by Stage 3** → "was defined and approved at Stage 3. To be confirmed with CG whether existing submission is sufficient."
- **Items by other discipline** → "will be provided as part of the overall submission under the relevant scope, coordinated with the [specialist]."

### Status Color Coding

| Status | Fill | Meaning |
|--------|------|---------|
| Closed | Green (#E2EFDA) | Draft submitted, resolved, or accepted |
| Open | Red (#FCE4EC) | Still needs action |
| Noted | Blue (#D6E4F0) | Acknowledged, no further action |

## Step 2: Update Submission Plans

After receiving designer input (e.g., NRS prepared draft drawings), update the submission plan:

- Change status from "Pending" to "Submitted"
- Set actual submission date
- Append description with draft drawing reference
- Add remarks noting draft status and next steps

## Step 3: Split Specialized Scope (if CG requires)

When CG asks for a separate register (e.g., Rigging Systems):

1. Extract items from parent register
2. Create new register with same template structure and section hierarchy
3. Map items to correct sections (Basis of Design → Gallery-Specific → BIM → Material → IFC)
4. Add BIM models and IFC Packages matching the parent's structure
5. Remove items from parent register — clear rows only, add reference note
6. **Preserve template style** — do NOT rebuild the parent workbook from collected data

### Template Style Preservation

When editing an existing register (removing rows after splitting scope):

```python
# CORRECT: unmerge + clear in place
for merge_range in list(ws.merged_cells.ranges):
    for r in range(start_row, end_row + 1):
        if merge_range.min_row <= r <= merge_range.max_row:
            ws.unmerge_cells(str(merge_range))
            break
for row in range(start_row, end_row + 1):
    for col in range(1, max_col + 1):
        try:
            ws.cell(row=row, column=col).value = None
        except AttributeError:
            pass
ws.cell(row=start_row, column=1).value = 'Scope — See separate Register Name'
ws.save(path)
```

**WRONG:** Collecting all rows into a list and rewriting the entire sheet destroys template formatting (merged cells, colors, borders, column widths).

## Step 4: Package Response Folder

Create a dated folder under `02_Submittals/` with this structure:

```
02_Submittals/YYYY-MM-DD_CG_Comments_Response/
├── 01_CR_Sheet/
│   └── Aseer_Arch_CR_Sheet_Responses.xlsx
├── 02_NRS_Draft_Drawings/
│   ├── MOC-ASE-AR-ARC-BF-DDD-XXXX-00_DRAFT.pdf
│   └── ...
├── 03_Registers/
│   ├── Structural_Submittal_Register.xlsx
│   ├── Structural_Submittal_Register_Rev01.xlsx
│   ├── Rigging_Submittal_Register.xlsx
│   ├── Consultant_Comment_Register_Revised.xlsx
│   └── Aseer_Arch_Submission_Plan_Modification.xlsx
└── 04_Correspondence/
    └── Re_ Aseer Museum — CG Comments on Architectural Submission Plan.pdf
```

## Step 5: File to OneDrive

Copy all files to the BIM path:
- CR Sheet → `02_Submittals/04_Registers/`
- Updated submission plans → respective register folders
- Draft drawings → `03_Design_Files/Architecture/Basement/Drafts/`
- Response folder → `02_Submittals/YYYY-MM-DD_CG_Comments_Response/`
