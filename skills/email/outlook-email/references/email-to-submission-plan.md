# Email → CG Submission Plan Workflow

After extracting project deliverables from email attachments, the final step is producing a structured submission plan for the Consultant (CG/PMC). This bridges "what we received" to "what we submit next."

## Trigger

User has received deliverables via email (drawings, specs, samples, reports) and asks for a submission plan, submittal schedule, or "what do we submit to CG from these files."

## Prerequisites

- Extract attachments to `/tmp/` using AppleScript (see SKILL.md → Extracting Attachments)
- `pdftotext` available for reading PDFs
- `openpyxl` available for Excel output
- Existing Deliverables Submission Schedule (if one exists for the project)

## Workflow

### Step 1 — Classify received items

Not every received email attachment goes to CG. Classify each:

| Category | Examples | CG Routing |
|----------|----------|------------|
| Design deliverables | Drawings, specs, 3D visuals, reports | Submit to CG for A-Approval |
| Material submittals | Datasheets, samples, mill certs | Submit to CG under MS-xx item |
| Consultant responses | CG Code B/C/D replies | Already CG-processed — action internally |
| Contract/admin | Invoices, POs, agreements | File only — not a CG submission |
| Meeting minutes | Minutes, action logs | File in project records |
| Kick-off/scope docs | SOW, drawing lists, proposals | File in project records |

### Step 2 — Map to existing schedule

Read the existing Deliverables Submission Schedule (if one exists) to find matching items:

```python
import openpyxl
wb = openpyxl.load_workbook('Aseer_Deliverables_Submission_Schedule_v3.xlsx')
# Read the Ref column and match against received documents
```

Common mapping heuristics for Aseer Museum:

| Received Document Pattern | Schedule Ref(s) |
|--------------------------|-----------------|
| NRS drawings 1100-1200 series (GA plans) | DD-02 (General Arrangement) |
| NRS drawings 1220-1250 series (finishes) | DD-03 / DD-04 / DD-05 |
| NRS drawings 1500-1600 series (sections) | DD-06 / DD-07 |
| NRS drawings 1700-1800 series (setworks) | DD-11 / DD-12 |
| NRS drawings 1800-1900 series (showcase) | DD-15 |
| GH showcase submittal | DD-15 (design) or MS-04 (material) |
| Material datasheets/samples | MS-01 (arch), MS-04 (showcase), etc. |
| MEP drawing list + SOW | DD-24A→E (MEP design package) |
| 3D visuals / renders | DD-27 (Visualization) |

### Step 3 — Read DIS (Document Issue Sheets)

NRS often sends a DIS PDF as the cover sheet while actual drawings are behind WeTransfer. Read the DIS with `pdftotext` to understand:
- **Purpose code** at the bottom: I=Information, A=Approval, C=Construction, T=Tender
- **Drawing register** listing every drawing number and title in the package
- **Revision** number and date
- **Distribution list** showing who received copies

The DIS content tells you:
- If marked **"I" (Information)** — this is for coordination only, needs Samaya review before CG submission
- If marked **"A" (Approval)** — this is directly for CG approval
- The actual drawing files are usually behind the WeTransfer link, not in the DIS PDF itself

```bash
# Extract DIS content to understand the package
pdftotext DIS_file.pdf - | grep -E "(MOC-ASE|Purpose|Existing|Proposed|Showcase|Setworks)"
```

### Step 4 — Build the submission plan Excel

Create a **2-sheet workbook**:

**Sheet 1: CG Submission Plan** with columns:
- # (sequential)
- Schedule Ref (maps to existing items)
- Deliverable (description + drawing codes)
- Received From (sender + company)
- Date Received
- Files / Attachments (filenames + sizes)
- Status / Action Needed
- Route to CG (who reviews first, expected review duration)

Group items into color-coded batches:
- **Batch 1 — For CG Submission** (green): ready or needs brief internal review
- **Batch 2 — Information/Record** (blue): meeting minutes, SOWs, admin
- **Batch 3 — CG Responses Received** (yellow): incoming Code B/C/D, needs internal action
- **Batch 4 — Pending/Follow-up** (red): overdue items, missing deliverables

Batch labels go in column 1 with merged formatting. Use `openpyxl` fills for color coding.

**Sheet 2: File Manifest** with columns:
- # (sequential)
- Filename (prefixed with sequence number)
- Size
- Source Email (sender + subject descriptor)
- Linked Schedule Item

### Step 5 — Route files to project folder

After creating the plan, copy extracted files to the project's submittals folder:

```bash
PROJECT_ROOT="/path/to/Aseer-Museum/02_Submittals/$(date +%d%b%Y)_Batch/"
mkdir -p "$PROJECT_ROOT"
cp /tmp/extracted/* "$PROJECT_ROOT"
```

### Step 6 — Flag critical actions

In the delivery summary to the user, highlight:
- **WeTransfer/cloud links with expiry** — these must be downloaded before they expire
- **CG Code C/E replies** requiring resubmission
- **Overdue items** that block the submission batch

## Pitfalls

**WeTransfer links are not real file attachments.** The email may have an attachment block in Outlook, but it's just the WeTransfer notification PDF or a small cover sheet. The actual drawings are behind the URL. The DIS sheet tells you what drawings exist; the WeTransfer URL is where you download them. Always check if an attachment is a cover sheet vs the actual deliverable.

**Some DIS PDFs are identical across emails.** Francesco sent two emails (Basement + LG Floor) but attached the same DIS cover sheet to both. Don't be confused — the actual content difference is in the WeTransfer links.

**Not all received documents are for CG submission.** Invoices, meeting minutes, internal coordination emails, and ADENG kick-off docs are records, not submittals. Separate them explicitly in the plan.

**Arabic subject/body with Latin-named attachments.** The email subject may be Arabic but the attachment filenames are in English/Latin. Read the attachment list, not the subject, to identify deliverables.

**Schedule refs may not exist for all items.** New subcontractor packages (AV, FLS, Landscape) that were added in v3 of the schedule may not have a matching email. Note these as "—" in the schedule ref column.

## Related Skills & References

- `outlook-email/references/email-triage-pattern.md` — initial inbox review before this workflow
- `outlook-email/references/aseer-email-processing-example.md` — full Aseer batch processing
- `outlook-email/references/cg-deliverables-schedule-response.md` — responding to CG schedule requests
- `outlook-email/references/batch-email-routing.md` — routing extracted files to project folders
