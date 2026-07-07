# Email Deliverables → Submission Plan / Register Workflow

When email attachments contain design deliverables (drawings, reports, samples) that need to be logged into the project's CG submission plan and tracked against the baseline schedule.

## Trigger

- User asks you to "make submission plan" or "update submission plan" from files received
- User asks to "check gaps" between what was supposed to be submitted vs what was actually received
- A batch of design deliverables arrives and needs filing + registration

## Three-Track Workflow

### Track 1 — Identify Deliverables from Email

```sql
-- Recent emails with attachments in a project folder
SELECT m.Record_RecordID as id,
       datetime(m.Message_TimeReceived, 'unixepoch', 'localtime') as received,
       m.Message_SenderList as sender,
       m.Message_NormalizedSubject as subject,
       m.Message_HasAttachment as att
FROM Mail m JOIN folders f ON m.Record_FolderID = f.Record_RecordID
WHERE f.Folder_Name = '<Project Folder>'
  AND date(m.Message_TimeReceived, 'unixepoch') >= date('now', '-7 days', 'localtime')
  AND m.Message_HasAttachment = 1
ORDER BY m.Message_TimeReceived DESC;
```

Check for WeTransfer links in the `Message_Preview` column — these contain the actual files (see WeTransfer pitfall in SKILL.md).

### Track 2 — Extract & Catalog Files

Use AppleScript (`osascript`) to extract attachments to `/tmp/`:

```applescript
tell application "Microsoft Outlook"
    set msg to message id <ID>
    set atts to (every attachment of msg)
    repeat with att in atts
        set attName to name of att
        if attName ends with ".pdf" then
            set savePath to "/tmp/project_submittals/" & attName
            do shell script "touch " & quoted form of savePath
            set saveFile to POSIX file savePath as alias
            save att in saveFile
        end if
    end repeat
end tell
```

**Key naming convention for extracted files:** prefix with serial (01_, 02_, etc.) and source (sender/purpose) so the file manifest is self-documenting.

### Track 3 — Build the Register

**Step 3a — Parse DIS (Document Issue Sheet) cover sheets**

Many design packages include a DIS PDF that lists every drawing in the batch. This is the most efficient source for the register:

```python
import subprocess, re
result = subprocess.run(["pdftotext", "-raw", dis_pdf_path, "-"], capture_output=True, text=True)
for line in result.stdout.split('\n'):
    m = re.match(r'(MOC-ASE-AR-ARC-(\w+)-DDD-(\d+))\s+(.+?)\s+((?:\d+:\d+(?:/\d+:\d+)?))\s+(A[01])', line)
    if m:
        # drawing_no = m.group(1), floor_code = m.group(2), num = int(m.group(3))
        # title = m.group(4).strip(), scale = m.group(5), size = m.group(6)
        pass
```

**Step 3b — Classify by section (drawing number ranges)**

```python
section_ranges = [
    (1100, 1104, "Existing GA Plans"),
    (1150, 1164, "Demolition Plans"),
    (1200, 1253, "Proposed Plans"),
    (2550, 2559, "Stairs Details"),
    (2700, 2761, "Setwork Details"),
    (2800, 2820, "Showcase Details"),
    (4000, 4053, "Sections"),
    (5510, 5537, "Room Elevations"),
    (6890, 6896, "Schedules - Finishes"),
]
```

**Step 3c — Cross-reference against existing submission plan**

Load the existing `Aseer_Submission_Plan.xlsx` and compare:

| Existing Plan Says | Actual Status | Action |
|---|---|---|
| Planned date = Dec 2025 | Received Jun 2026 | Update status to PARTIALLY RECEIVED, add actual date |
| Generic "Architectural design" | 246 specific drawings | Break into 7+ sub-items (GA, Sections, Setworks, etc.) |
| Not listed at all | Received | Add new rows |
| Listed but never received | Overdue | Flag as OVERDUE, mark red |

**Step 3d — Add new columns to the Submission Plan**

Insert after "Planned Submission Date":
- `Actual Submission Date` — when the files actually arrived
- `Last Updated` — date of this update

### Building the Output Excel

Use openpyxl with the following style conventions:

| Status | Color | Hex |
|--------|-------|-----|
| RECEIVED / PARTIALLY RECEIVED | Green fill | `E2EFDA` |
| OVERDUE | Red fill | `FCE4EC` |
| IN PROGRESS | Amber fill | `FFF3CD` |
| Planned (no change) | No fill | — |

**Header style:** White text on dark blue (`2F5496`), Calibri 10 bold
**Body:** Calibri 9, thin borders (`#CCCCCC`)
**Section headers:** Light blue (`D6E4F0`), dark blue text

### File Destination

Updated submission plan goes to:
1. Desktop (for user's quick access)
2. Project registers folder: `04_Docs/02_Plans_and_Procedures/02.2_BEP_MIDP_TIDP/04_Registers/`

Do NOT modify the original Excel file (user preference). Save as `_Updated_<date>.xlsx`.

### Example: Gap Analysis Output

```
Items updated (existing rows changed from "Planned"): 6
New items added: 15
  - NRS DD packages (7): GA Plans, Sections, Stairs, Setworks, Showcases, Details, Visuals
  - NRS Missing Drawings (2): 20 items overdue — escalate
  - MEP Designer (1): ADENG kick-off
  - Display Cases actuals (2): GH Submittal 13 + Brass Sample
  - Structural actuals (2): BOD Report + Loading Plans DWG
  - Project Management (1): Meeting Minutes
```

### Pitfalls

- **Excel serial dates:** Excel stores dates as serial numbers (days since 1899-12-30). Convert: `base + timedelta(days=serial)`. Use readable format (`26 Jun 2026`) in the updated file.
- **DIS PDFs are sometimes identical** — the same cover sheet may be attached to multiple emails. Only create one register entry per unique DIS.
- **WeTransfer files arrive as .zip or .7z** — check filename extension; 7z requires `7z x` (not `unzip`). The unzip may use "Zippy" compression which is standard.
- **File counts explode** — large DD packages can be 10,000+ files. Focus the register on the PDF drawings and schedules listed in the DIS, not every bitmap in DWG subfolders.
- **Arabic subject translations** — when email subjects contain Arabic, translate to concise English for the register. Never present raw Arabic text to the user.
- **Two identical DIS files with different subjects** — both "Basement" and "LG Floor" emails from NRS contained the same DIS PDF. The difference was in the WeTransfer-linked drawing files behind each link, not in the attached cover sheet.
