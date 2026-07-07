# Aseer Museum Email Processing — Worked Example

This reference documents the systematic email processing workflow used on 2026-06-11 for 10 Aseer Museum emails.

## Workflow

1. Query Outlook SQLite for all project emails (by folder name or doc code prefix)
2. For each email: read preview → extract attachments via AppleScript → read PDF content → route to project folder
3. Use sub-agents in batches of 3 for parallel processing
4. Track progress with todo list

## AppleScript Extraction (reliable)

```applescript
tell application "Microsoft Outlook"
    set theMsg to message id <Record_RecordID>
    set atts to (every attachment of theMsg)
    set outFolder to "/tmp/outlook_extracts/"
    do shell script "mkdir -p " & quoted form of outFolder
    repeat with att in atts
        set attName to name of att
        set savePath to outFolder & "<ID>_" & attName
        do shell script "touch " & quoted form of savePath
        set saveFile to POSIX file savePath as alias
        save att in saveFile
    end repeat
end tell
```

## Binary Extraction (fallback — when AppleScript fails or no Automation permissions)

The `.olk15MsgAttachment` file has a proprietary header (~285 bytes) followed by base64-encoded content starting with `JVBER` for PDFs:

```python
import base64, re
with open('file.olk15MsgAttachment', 'rb') as f:
    data = f.read()
idx = data.find(b'JVBER')
if idx >= 0:
    b64_text = data[idx:].decode('ascii', errors='ignore')
    b64_clean = re.sub(r'[^A-Za-z0-9+/=]', '', b64_text)
    pdf_data = base64.b64decode(b64_clean)
    with open('output.pdf', 'wb') as out:
        out.write(pdf_data)
```

## Aseer Document Code Routing

The document code format is: `MOC-MUS-ASE-{DISCIPLINE}-{TYPE}-{NUMBER}`

| Code Pattern | Document Type | Project Folder |
|------|--------------|----------------|
| `1K0-PL-xxxx` | Plan (Schedule/Master) | `02_Plans_and_Procedures/02.8_Master_Programme/02_CG_Responses/` |
| `1E0-ZD-xxxx` | General (Electrical) | `Subcontractors/02_Lighting_Designer/05_Returned_Submittals/` |
| `1KH-PL-xxxx` | HSE Plan | `02_Plans_and_Procedures/02.5_HSE_Plan/01_Source_Files/` |
| `1K0-MI-xxxx` | Mobilization Items | `02_Plans_and_Procedures/02.16_Mobilization_Plan/01_Source_Files/` |
| `1KN-1E0-xxx` | Site Instruction (SI) | `05_SIs/05.1_Issued_by_CG/` |
| `1K0-ZD-xxxx` | Sustainability / General cross-disc | `02_Plans_and_Procedures/02.12_Sustainability_Strategy/` |
| `1K0-PQ-xxxx` | Prequalification | `09_Registers/27_Subcontractor_Prequalification_Register/{Company}/` |
| `1M0-MS-xxxx` | Method Statement | `02_Plans_and_Procedures/02.15_Method_Statements/` |
| `1M0-ZD-xxxx` | Mechanical General | `02_Plans_and_Procedures/02.16_Mobilization_Plan/` |
| `1C0-IR-xxxx` | Inspection Request | `Docs/03_Inspection_Requests/` |
| `1A0-ZD-xxxx` | Architecture General | `02_Submittals/Architecture/` or `Design Files/` |
| `1A0-ZD-0033` | 3D Render Sample | `02_Submittals/Architecture/3D_Renders/` |
| `1A0-ZD-0060/61/62` | DD Architecture Pkg | `02_Submittals/03_DD Documents/Arch DD Drawing/` |
| `NC-1A0-xxx` | Non-Conformance Report | `Docs/10_Test_and_Inspection/10.3_NCRs/` |

**Placement rule for CG responses:**
- **Status B** (Approved with Comments) → `02_CG_Responses/` subfolder
- **Status C** (Revise and Resubmit) → `02_CG_Responses/` subfolder, flag for user attention
- **Status A** (Approved) → may stay in `01_Source_Files/` or `02_CG_Responses/` depending on context

**Code numbers:** ZD-0056, ZD-0038, ZD-0051 with same pattern → route by discipline (1E0=Electrical, 1M0=Mechanical, 1A0=Architecture, 1KH=HSE, 1K0=General/Management, 1C0=Civil, 1KN=Security)

**Uncategorised / misc submissions** (e.g. invoices, Sharepoint links): file in `09_Correspondence/` or `Docs/04_Financial/Invoices/` with an `.md` memo noting the routing.

**CG Response Status Codes:**
- **B** = Approved with Comments — file in `02_CG_Responses/`
- **C** = Revise and Resubmit — file in `02_CG_Responses/`, flag for user attention
- The `Message_Preview` typically includes the status code (e.g. "B - Approved with Comments")

## Email Thread Analysis

For procurement/action-required emails, always check the full thread:

```sql
SELECT m.Record_RecordID, datetime(m.Message_TimeReceived, 'unixepoch', 'localtime'),
       m.Message_SenderList, substr(m.Message_Preview, 1, 300)
FROM Mail m
WHERE m.Message_NormalizedSubject = '<exact subject>'
ORDER BY m.Message_TimeReceived ASC;
```

## Team Contact Index

To build a project contact directory:

```sql
SELECT DISTINCT m.Message_SenderList, m.Message_SenderAddressList
FROM Mail m JOIN folders f ON m.Record_FolderID = f.Record_RecordID
WHERE f.Folder_Name = '<ProjectFolder>'
ORDER BY m.Message_SenderList;
```
