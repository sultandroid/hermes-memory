# NRS Comments Investigation — Reference

When the user asks about NRS (Nissen Richards Studio) comments or review feedback on design drawings, follow this investigation pipeline.

## Sources to Search (in order)

### 1. Risk Register / Design Discipline Register
Check for risk items mentioning NRS comments:

- `01_Registers/risk_register.md` — PRR themes
- `01_Registers/design_discipline_risk_register.md` — DDR-ARC-002 "NRS comments unresolved on 57 pre-contract drawings"
- `02_Schedule/submission_plan_risk_assessment.md` — QA-Q-005

### 2. Outlook SQLite (Email Previews)
The Outlook database at `~/Library/Group Containers/UBF8T346G9.Office/Outlook/Outlook 15 Profiles/Main Profile/Data/Outlook.sqlite` contains email previews. Search `Message_NormalizedSubject` and `Message_Preview`:

```sql
SELECT datetime(Message_TimeReceived, 'unixepoch') as dt,
       Message_NormalizedSubject, Message_SenderAddressList,
       substr(Message_Preview, 1, 500) as preview
FROM Mail
WHERE Message_NormalizedSubject LIKE '%NRS%comment%'
ORDER BY Message_TimeReceived DESC;
```

Key email threads to look for:
- "NRS Comments-Fire Alarm Drawings" — sent by mohamed_kamal31074@yahoo.com / m.hakami@samayainvest.com
- "NRS Comments-Audio Visual Drawings-Public Address" — sent by m.hakami
- "Stage 4 Architectural Package Remarks Table" — from francesco.b@nissenrichardsstudio.com (actual NRS comments attachment)
- "Aseer Regional Museum - Stage 4 Architectural Package Remarks Table" — back-and-forth between NRS and Samaya

### 3. Outlook Attachment Cache
Cached PDFs of NRS-stamped drawings live at:
`~/Library/Group Containers/UBF8T346G9.Office/Outlook/Outlook 15 Profiles/Main Profile/Files/S0/*/Attachments/0/`

Search by filename patterns:
```bash
find "~/Library/Group Containers/UBF8T346G9.Office/Outlook/Outlook 15 Profiles/Main Profile/Files" \
  -name "*NRS*comment*" -o -name "*NRS_stamp*" -o -name "*REBA*"
```

Common NRS comment PDFs:
- `FIRE_ALARM_PACKAGE__NRS_comments_260413_stamped.pdf` — Fire alarm redline comments
- `Audio_Visual_System__Shop_Drawings_set140426_NRS_comments_260415.pdf` — AV system comments
- `EL_03__PA__SOUND_GROUND_NRS_comments_260413.pdf` — PA sound comments
- `SLF-0001/0002/0003/0004_NRS_comments_[date]_stamped.pdf` — Life safety comments
- `A2742-1250/1251/1252/1253.pdf` — NRS architectural drawing redlines

### 4. Project Document Control Folder
Markdown stubs for NRS-related PDFs live at:
`~/Documents/Asher_Regional_Museum_Document_Control/06_PDFs/General/`

Search for files containing "NRS", "REBA", "Remarks", "A2742" in their names. Note: most are OneDrive placeholders (0 bytes, deadlock on read).

Actual A2742 drawing PDFs may be cached at:
`~/Documents/Asher_Regional_Museum_Document_Control/06_PDFs/Markdown/`

### 5. Project Folder (OneDrive Placeholders)
`Design Files/99_NRS_Drops_2026-04-05/` contains subfolders:
- `01_PA_Sound_NRS_Comments_260413/` — PA sound drawings with NRS comments
- `02_AV_System_NRS_Comments_260415-260427/` — AV system drawings with NRS comments
- `03_NRS_Drawings_A2742-1250-1253_260413/` — NRS architectural drawing set (A2742 series)

## Key NRS Personnel (from emails)
- Francesco Bitelli — Senior Associate (francesco.b@nissenrichardsstudio.com)
- Emmy Bacharach — Architect (emmy.b@nissenrichardsstudio.com)
- Jim Richards (jim.r@nissenrichardsstudio.com)

## Handling Image-Based PDFs
NRS comments are typically **stamped redlines on drawings** — image-based, not extractable by pdftotext. Options:
1. Use `pdftoppm` to convert to PNG, then OCR with tesseract (works if there's text, not just markups)
2. Open in a PDF viewer manually on the machine
3. Use browser_vision on rendered screenshots (fallback when vision model supports images)

## Risk Context
The "57 pre-contract drawings" with unresolved NRS comments are documented as risk QA-Q-005 (Medium, P3×S3=9). Action: build a comment disposition matrix with owner/date per unresolved item. Register DDR-ARC-002 tracks this in the design discipline risk register.
