# Incoming Document Triage — Aseer Museum / Samaya

Workflow for receiving a batch of new project documents from Downloads, studying them, filing them, and updating knowledge.

## Trigger

User provides a list of file paths in Downloads (PDFs, DOCXs, incomplete downloads). Files follow the `MOC-MUS-ASE-{Disc}-{Type}-{Num}` naming convention.

## Process

### 1. Study — extract and identify

Batch-extract text from all files in parallel:

```bash
cd /Users/mohamedessa/Downloads
for f in file1.pdf file2.pdf; do
  pdftotext -layout "$f" "/tmp/${f%.pdf}.txt" 2>&1 | tail -1
  wc -l "/tmp/${f%.pdf}.txt"
done
```

For DOCX files, use Python zipfile + xml.etree to extract `word/document.xml`.

Read the first 20-30 lines of each text file to identify:
- **Cover sheet**: submittal number, revision, date, discipline, subcontractor name, CG status code (A/B/C/D)
- **Description**: what the document covers (products, scope, CVs, reports)
- **CG comments**: approval conditions

### 2. Determine filing location

Map by document code prefix:

| Code | Discipline | OneDrive Submittals Subfolder |
|------|-----------|------------------------------|
| `1A0` | Architecture | `09_Prequalifications/` or `02_Material_Samples/Architecture/` |
| `1E0` | Electrical | `09_Prequalifications/` or `01_Shop_Drawings/Electrical/` |
| `1M0` | Mechanical | `09_Prequalifications/` or `01_Shop_Drawings/Mechanical/` |
| `1C0` | Civil/Structure | `09_Prequalifications/` or `01_Shop_Drawings/Structure/` |
| `1K0` | General | `09_Prequalifications/` or `01_Shop_Drawings/General/` |

Document type suffixes:
- `PQ` → Prequalification → `09_Prequalifications/`
- `MA` → Material Submittal → `02_Material_Samples/{Discipline}/`
- `ZD` → Shop Drawing / Document Submittal → `01_Shop_Drawings/{Discipline}/`
- `MS` → Method Statement → `08_Method_Statements/`
- SOW docs, emails, contracts → `03_Design_Files/{Category}/`

### 3. Move files — USE `mv`, NOT `cp`

**CRITICAL PITFALL**: Always use `mv` (move), not `cp` (copy). The user expects files to leave Downloads. `cp -n` leaves originals behind and requires a second pass.

```bash
# Correct:
mv "$DOWNLOADS/file.pdf" "$ONEDRIVE_BIM/09_Prequalifications/"

# Wrong — leaves originals in Downloads:
cp -n "$DOWNLOADS/file.pdf" "$ONEDRIVE_BIM/09_Prequalifications/"
```

Two destinations:
1. **Primary**: OneDrive BIM path (`~/Library/CloudStorage/OneDrive-SAMAYAINVESTMENT/Samaya/Technical Office/Bim Unit/Aseer-Museum/02_Submittals/`)
2. **Working copy**: Document Control (`~/Documents/Asher_Regional_Museum_Document_Control/04_Submittals/`) — use `cp` here since it's a copy

Handle duplicates:
- `(1)` suffix files → check if same content; delete if duplicate
- `Unconfirmed *.crdownload` → incomplete download; delete and advise re-download

### 4. Update memory

Save to `memory` (not `user` profile):
- Newly prequalified suppliers and their CG status
- Design responsibility splits
- Any new document codes or conventions discovered

### 5. Advise user

Report:
- What was moved where (table)
- What was skipped/deleted and why
- What needs manual follow-up (registers to update, CG status to verify visually)
- Any anomalies (wrong contract number, duplicates, incomplete files)

## Register Updates

The following registers need manual entries (Excel files — use openpyxl or advise user):

| Register | New Entries |
|----------|-------------|
| Arch_Submittal_Register | PQ-0007 (Jotun), PQ-0015 (Unitech IKK), PQ-0030 (NRS), PQ-0075 (Al Wataniya), PQ-0079 (Saveto) |
| Electrical_Submittal_Register | PQ-0044 (Peerless AV), PQ-0036 (Samsung), PQ-0046 (MSD), PQ-0055 (Epson), ZD-0074, ZD-0075 |
| Mechanical_Submittal_Register | PQ-0021 (EES), PQ-0061 (SFFECO), ZD-0063, ZD-0065 |
| Structural_Submittal_Register | PQ-0068 (Rajhi), PQ-0070 (ALSSAD), MS-0007 |
| General Submittal Register | PQ-0049 (ACES), PQ-0076 (ABAK), ZD-0069, ZD-0071, ZD-0072 |

## Pitfalls

- **`mv -n` skips existing files**: If you previously `cp`-ed files to the destination, `mv -n` will silently skip them. Use `mv` (force overwrite) instead.
- **CG status not always readable**: PDF text extraction often can't read the status code (A/B/C/D) from the cover sheet. Advise user to open PDFs visually.
- **Wrong contract number**: Some files may have a different contract number (e.g., 4800000960 instead of 0010003521). Flag for verification.
- **OneDrive sync**: Moving files into OneDrive is safe (same filesystem). Moving files within OneDrive is NOT safe (use web UI).
